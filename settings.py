class Settings():
    '''包括项目所有的自定义设置项'''
    def __init__(self):

        # bing图片API
        self.bing_start_url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'
        # bing域名，用于合成图片全链接
        self.bing_domian = 'https://cn.bing.com'

        # 图片保存地址
        self.save_path = 'F:/bingpic/'
        # 是否保存日志，其中包括时间、图片id、图片地址与描述信息
        self.save_log = True
        # 日志地址与名称
        self.log_path = self.save_path + 'log.csv'
        # 是否发布过此次图片，注意信息来自于日志
        self.pic_saved_flag = False
        # 使用2k图片，额外保存2k图片并在微博中使用2k图片地址
        self.hd_pic = True

        # 微博分享接口
        self.weibo_start_url = "https://api.weibo.com/2/statuses/share.json"
        # 微博安全地址，注意需与微博开发平台设置相同
        self.myurl = 'https://www.weibo.com/u/6015545982'
        # 微博口令
        self.access_token = "xiaoqiangjun"


if __name__ == "__main__":
    my_setting = Settings()
    print(my_setting.bing_start_url)