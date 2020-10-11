import requests
import re
import os


def get_bing():
    url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
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
        '2.00M_cGZGr37H4Eefabde1e10crEAoD',
        "status":
        dicts['copyright'] + '\n我的主页： https://www.weibo.com/u/6015545982' +
        ' \n图片地址： ' + dicts['url']
    }
    files = requests.get(dicts['url']).content
    r = requests.post(url, data=payload, files={'pic': files})
    return r.json()


def save_log(dicts):
    data = dicts['date'] + ',' + dicts['id'] + ',' + dicts[
        'url'] + ',' + dicts['copyright'] + '\n'
    if not os.path.exists('log.csv'):
        with open('log.csv', 'w', encoding='gb18030') as log_file:
            log_file.write('date,id,url,copyright\n')
            log_file.write(data)
    else:
        with open('log.csv', 'a', encoding='gb18030') as log_file:
            log_file.write(data)


if __name__ == "__main__":
    # 解析bing内容
    dicts = get_bing()
    # 发布微博
    response = post_weibo(dicts)
    # 结果保存与输出
    if 'created_at' in response:
        save_log(dicts)
        print('Success! Created at: ' + str(response['created_at']))