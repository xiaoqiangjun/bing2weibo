import requests
import re
import os
from calendar import timegm
from time import *


def wait_on_time(wkt):
    wkt_list = list(gmtime(time()))
    if wkt[0] == 0 and wkt[1] == 0:
        wkt_list = list(gmtime(time()+86400))
    wkt_list[3] = wkt[0]
    wkt_list[4] = wkt[1]
    wkt_list[5] = wkt[2]
    
    work_time = timegm(tuple(wkt_list))
    print(strftime('work at: UTC %Y-%m-%d %H:%M:%S', tuple(wkt_list)))
    now_time = time()
    print(strftime('now its: UTC %Y-%m-%d %H:%M:%S', gmtime(time())))
    remain_time = work_time - now_time
    if remain_time < 0 or remain_time > 3600:
        print('OUT OF WORK TIME!')
        return None
    while remain_time > 0:
        if remain_time > 100:
            sleep(77)
            print('long time sleep...')
            print('time remians:', '{:0>2d}'.format(round(remain_time)), 's')
            remain_time = work_time - time()
            continue
        print('time remians:', '{:0>2d}'.format(round(remain_time)), 's',end='')
        sleep(1)
        print("\r",end='',flush = True)
        remain_time = work_time - time()
 
    print('*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')
    print(strftime('WORK STARTING SUCCESSFULLY AT UTC %Y-%m-%d %H:%M:%S', gmtime(time())))
    print('*-*-*-*-*-*-*-**-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*')


def get_bing():
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN'
    response = requests.get(url).json()['images'][0]
    dicts = {}
    dicts['date'] = response['enddate']
    dicts['id'] = re.search(r'=(.*?)_1', response['url']).group(1)
    dicts[
        'url'] = 'https://cn.bing.com/th?id=' + dicts['id'] + '_1920x1080.jpg'
    dicts['copyright'] = response['copyright']
    return dicts


def post_weibo(dicts):
    url = "https://api.weibo.com/2/statuses/share.json"
    payload = {
        "access_token":
        os.environ['WEIBO_TOKEN'],
        "status":
        dicts['copyright'] + '\n我的主页： http://t.cn/A6bpoKJC' +
        ' \n图片地址： ' + dicts['url']
    }
    files = requests.get(dicts['url']).content
    r = requests.post(url, data=payload, files={'pic': files})
    return r.json()


def save_log(dicts):
    data = dicts['date'] + ',' + dicts['id'] + ',' + dicts[
        'url'] + ',' + dicts['copyright'] + '\n'
    if not os.path.exists('log.csv'):
        with open('log.csv', 'w', encoding='utf8') as log_file:
            log_file.write('date,id,url,copyright\n')
            log_file.write(data)
    else:
        with open('log.csv', 'a', encoding='utf8') as log_file:
            log_file.write(data)


if __name__ == "__main__":
    # 提前启动，等待整点，参数为实际想要的UTC时间
    wait_on_time((13,25,20))
    # 解析bing内容
    dicts = get_bing()
    # 发布微博
    response = post_weibo(dicts)
    # 结果保存与输出
    print(response)
    if 'created_at' in response:
        #save_log(dicts)
        print('Success! Created at: ' + str(response['created_at']))