bing2weibo —— 自动获取必应每日图片并发布到微博
===========
本项目基于`python3.x`与`requests`模块。利于Bing与微博的原生API实现了下面的功能：  

- 保存每日必应图片
- 保存图片链接与id
- 支持获取高清（UHD）图片
- 自动发布图片与描述信息到微博  

---  
## 一、安装要求  
```
    python 3.x
    requests
```
项目在本机`pyhton3.8.5`以及`requests2.24.0`测试通过。
  
  
## 二、使用方法
大部分的参数无需改动，且都位于``settings.py``文件，并都编写了详细的注释。  
最关键的参数是自动发布到微博需要的`access_token`，需要自行获取并修改。综合参阅[Python自动化发微博](https://www.itengli.com/python_weibo/)与[Python脚本实现自动发送微博](https://mp.weixin.qq.com/s?__biz=MzAxMjU0ODQ2OA==&mid=2649232112&idx=1&sn=0acd8ce0022c547a2ef3de15a5ac678a&chksm=83ac92ebb4db1bfdc734804467be6f97b055a16a35fe958c1c31332b668bee5e6d4e0c2dce42&mpshare=1&scene=23&srcid=0109I4LbC080MuG2PgFpCwBw&sharer_sharetime=1578552780662&sharer_shareid=c88278dffa79e5c1af81d7fc6e6b5305#rd)，得到下面步骤。说明如下：    
1. 在[微博开发平台](https://open.weibo.com/)注册成为`个人`开发者；
2. 申请**微链接**-**移动应用**-**网页应用**，并填写名称；
3. 在控制台中编辑应用基本信息，**强烈建议**将安全域名填写为`www.weibo.com`，这样无需修改更多的配置；（除非你拥有自己的域名，且仅支持`.com`,`.cn`,`.net`）
4. 在控制台中修改高级应用设置，将**授权回调页**与**取消授权回调页**设置为`https://api.weibo.com/oauth2/default.html`；
5. 在控制台复制你的`App Key`，这里还有`App Secret`会用到；
6. 在**浏览器**中打开网页`https://api.weibo.com/oauth2/authorize?client_id=你复制的App key&redirect_uri=https://api.weibo.com/oauth2/default.html&response_type=code`;
7. 页面跳转后，复制地址栏`code=`**后面**的字符串;
8. 新建一个python文件如下：
```python
import requests

url_get_token = "https://api.weibo.com/oauth2/access_token"
#构建POST参数
payload = {
"client_id":"填入你的App Key",
"client_secret":"填入你的App Secret",
"grant_type":"authorization_code",
"code":"上面获得的code",
"redirect_uri":"https://api.weibo.com/oauth2/default.html"
}
#POST请求
r = requests.post(url_get_token,data=payload)
#输出响应信息
print r.text
```
9. 运行上面的文件，输出结果如下，其中`access_token`键的值就是我们需要的！
```json
{"access_token":"我们要记下的","remind_in":"157679999","expires_in":157679999,"uid":"1739207845"
```
10. 修改`settings.py`中`self.access_token`的值。  

到这里，你已经可以运行`bing2weibo.py`了，代码将自动发布一条带图的微博，注意微博中的主页地址，你可以在`settings.py`中修改为你自己的，但是这个地址必须在前面第3点中设置的**安全域名**下。你可以自己尝试一并修改后，发布你自己的域名。

## To-Do List
- [] 每天定时发布
- [] ~~微博中加入每日一句~~（在[weibogugubot]( '还没做呢')中实现

## License
GPL
