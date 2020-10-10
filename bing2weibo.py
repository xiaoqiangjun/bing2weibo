import json
import re
from pathlib import Path
from time import sleep, strftime, localtime

import requests

from settings import Settings


def get_bing_dicts(my_settings):
    '''
    获取bing返回的json，并解析出需要的部分：
    date : 图片所在时间
    fullurl : 1080p图片全地址
    id : 图片id，唯一标识并可以生成图片链接
    copyright : 图片介绍与版权信息
    '''
    # 返回字典
    return_dicts = {}

    # 仅在这里测试网络
    try:
        r = requests.get(my_settings.bing_start_url)
    except requests.exceptions.ConnectionError:
        print_error(1, 'No Internet Connection')
        return {}
    else:
        if r.status_code != 200:
            print_error(2, str(r.status))
            return {}

    # bing返回json转化为字典
    r_dicts = r.json()
    r_dicts = r_dicts['images'][0]
    return_dicts['date'] = r_dicts['enddate']
    return_dicts['id'] = re.search(r'id=(.*?)_1920', r_dicts['url']).group(1)
    return_dicts['fullurl'] = my_settings.bing_domian + re.match(
        r'(.*?)&', r_dicts['url']).group(1)
    return_dicts['copyright'] = r_dicts['copyright']

    # 返回关键字典
    return return_dicts


def save_pic(my_settings, main_dicts):
    '''在指定位置保存今日图片与csv格式记录'''
    # 保存图片
    pic_name = main_dicts['date'] + '_' + main_dicts['id'] + '.jpg'
    pic_full_path = my_settings.save_path + pic_name
    response = requests.get(main_dicts['fullurl'])
    with open(pic_full_path, 'wb') as pic_file:
        pic_file.write(response.content)
    
    # 高清图片选项
    if my_settings.hd_pic:
        hd_pic_name = 'HD_' + pic_name
        hd_pic_full_path = my_settings.save_path + hd_pic_name
        response = requests.get(main_dicts['fullurl'].replace('1920x1080', 'UHD'))
        with open(hd_pic_full_path, 'wb') as pic_file:
            pic_file.write(response.content)

    # 保存日志
    if not my_settings.save_log:
        return None
    log_path = my_settings.log_path
    path = Path(log_path)
    log_data = main_dicts['date'] + ',' + main_dicts['id'] + ',' + main_dicts[
        'fullurl'] + ',' + main_dicts['copyright'] + '\n'

    # 不存在日志就创建并加头，否则检测是否已经保存，更改标记，或者附加内容
    if not path.exists():
        with open(log_path, 'w', encoding='gb18030') as log_file:
            head = 'date,id,fullurl,copyright\n'
            log_file.write(head)
            log_file.write(log_data)
    else:
        with open(log_path, 'a+', encoding='gb18030') as log_file:
            log_file.seek(0, 0)
            lines = log_file.readlines()
            if lines[-1].split(',')[0] == strftime("%Y%m%d", localtime()):
                my_settings.pic_saved_flag = True
            else:
                log_file.seek(0, 2)
                log_file.write(log_data)


def post_weibo_pic(my_settings, main_dicts):
    '''利用微博接口发布图片微博'''
    # 是否二次发布
    if my_settings.pic_saved_flag:
        my_settings.pic_saved_flag = False
        s = input(
            "You seem to have posted this Weibo, input 'y' to confirm reposting..."
        )
        if s != 'y':
            print_error((-1, 'Posting Canceled'))
            return None

    # 构建文本类POST参数
    status = main_dicts['copyright']
    my_page = '\n我的主页： ' + my_settings.myurl
    pic_url = ' \n图片地址： ' + main_dicts['fullurl']
    if my_settings.hd_pic:
        pic_url = pic_url.replace('1920x1080', 'UHD')
    payload = {
        "access_token": my_settings.access_token,
        "status": status + my_page + pic_url
    }
    print(payload['status'])

    # 构建二进制图片参数，并发布
    pic_name = main_dicts['date'] + '_' + main_dicts['id'] + '.jpg'
    pic_full_path = my_settings.save_path + pic_name
    pic_obj = open(pic_full_path, "rb")
    files = {"pic": (pic_name, pic_obj)}
    
    # 发布微博，检测返回，输出结果
    url = my_settings.weibo_start_url
    r = requests.post(url, data=payload, files=files)
    pic_obj.close()
    res_dicts = r.json()
    if 'created_at' in res_dicts:
        print_error(
            (0, 'Success! Created at: ' + str(res_dicts['created_at'])))
    else:
        print_error((3, 'Weibo config Error'))


def print_error(error_tuple):
    '''处理输出错误'''
    print('Return Code: ', error_tuple[0])
    print('Message: ', error_tuple[1])


def main():
    '''主函数'''
    # 定义设置
    my_settings = Settings()

    # 获取bing图片关键信息
    main_dicts = get_bing_dicts(my_settings)
    if not main_dicts:
        return None

    # 保存图片
    save_pic(my_settings, main_dicts)

    # 发布图片微博
    post_weibo_pic(my_settings, main_dicts)


if __name__ == "__main__":
    main()