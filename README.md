#### 项目过程

###### 1.[云服务器配置](https://www.jianshu.com/p/d70b7fe36646)
###### 2.[Scrapy爬虫撸代码](https://www.jianshu.com/p/022c88c4a8b3)
###### 3.[ProxyPool动态IP代理池](https://www.jianshu.com/p/6c9d712be5e7)
###### 4.[云服务器调度](https://www.jianshu.com/p/d51163f71318)   

#### 工具
- Pycharm
- Xshell
- Python 3.6
- 阿里云Centos 7
----
##### 2.Scrapy爬虫代码（京东搜索零食）
强烈推荐公众号 **皮克啪的铲屎官**
此部分代码基本都来自他发布的文章[《PeekpaHub》 全栈开发](https://mp.weixin.qq.com/s?__biz=MzI2ODYwNjE5NQ==&mid=2247484173&idx=1&sn=1e75beb71a1fb8dfb18eacf054f85bdc&chksm=eaec4c91dd9bc587dbc4c52602745b3eadf36094f4d1cec8b7ec8bb58a7796e6ea5edd688dcc&mpshare=1&scene=1&srcid=1118glsp0bRvHlfCATZjQzj8&pass_ticket=Lp13fNr4gSxnOFRce%2BtyJ2Jfm62QxBknaCE7tAmCj6PrD30pxVt%2F4sjQOCV6dMTb#rd)
不仅仅是爬虫 服务器的配置等都是从这里学习的
当然除了京东爬虫外 他还有很多有意思的爬虫 关注有惊喜 感谢作者皮克啪的铲屎官的提供的帮助和学习
----
下面是我一些补充 
*talking is short  show me  your code*
**废话少说 放码过来**
[京东零食爬虫Github](https://github.com/sadjjk/jdGoodsSpider)

###### 爬虫主要文件 [jdSpider.py](https://github.com/sadjjk/jdGoodsSpider/blob/master/jdGoodsSpider/spiders/jdSpider.py)
原作者是使用BeautifulSoup进行html解析 我觉还是用xpath更方便简洁一些  于是改写成了xpath解析 实现的最终效果是一样的 
还有个地方可以提一下   
通常都是这么写 在items定义好后一个一个赋值上去![](https://upload-images.jianshu.io/upload_images/3290281-9127a830e28bad98.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)可以改成如下更简洁(这种写法出自崔庆才老师的爬虫教程 也感谢这位老师 )
```
 for field in goods.fields:
      try:
        goods[field] = eval(field)
      except NameError:
        self.logger.debug("Field is Not Defined " + field)
 yield goods
```
###### [items.py](https://github.com/sadjjk/jdGoodsSpider/blob/master/jdGoodsSpider/items.py)
这个文件最简单了 定义一下就好了 没什么说的![](https://upload-images.jianshu.io/upload_images/3290281-ca3b123d986ba125.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
###### [piplines.py](https://github.com/sadjjk/jdGoodsSpider/blob/master/jdGoodsSpider/pipelines.py)
![](https://upload-images.jianshu.io/upload_images/3290281-37320b2861e0438d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
这里```MONGO_URL```会在settings.py中申明 实际填的就是服务器内网IP 
一旦填了服务器内网IP后 上传到服务器中运行 是没有问题的 **但在本地是无法跑通测试这个项目的 会报数据库连接不上的错误**
要想成功在本地测试项目代码 两种修改：
- MONGO_URL改成localhost本地 并且本地要安装MongoDB并启动
- 依然连接服务器中MongoDB 存储到服务器的MongoDB数据库中 不过代码上要做如下修改 添加ssh跳转![](https://upload-images.jianshu.io/upload_images/3290281-91a0feb63da5fdee.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
下载三方库sshtunnel 填写公网IP、用户名、密码和内网IP 在打开和关闭数据库的时候 要添加```self.server.start()```和```self.server.stop()```![](https://upload-images.jianshu.io/upload_images/3290281-f844ad4d8f3adcd6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)其他保持不变 这样就可以在本地运行爬虫 并保存在服务器中的MongoDB中
**注意：若这个项目要上传到服务器中 在服务器中运行 则不用做修改**
###### [middiewares.py](https://github.com/sadjjk/jdGoodsSpider/blob/master/jdGoodsSpider/middlewares.py)
**尤其是在云服务器上运行时  要保证爬虫的健壮稳定**
中间件需要增加很多异常处理 就要防止爬虫各种意外排取失败
常用三招：
- 第一招：随机使用各种各样的User-Agent![](https://upload-images.jianshu.io/upload_images/3290281-467fc59c2e57e548.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)agents就是一系列User-Agent列表 可自行百度 也可使用如下
```
agents = [
    "Mozilla/5.0 (Linux; U; Android 2.3.6; en-us; Nexus S Build/GRK39F) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/532.5 (KHTML, like Gecko) Chrome/4.0.249.0 Safari/532.5",
    "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/532.9 (KHTML, like Gecko) Chrome/5.0.310.0 Safari/532.9",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.7 (KHTML, like Gecko) Chrome/7.0.514.0 Safari/534.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/9.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.14 (KHTML, like Gecko) Chrome/10.0.601.0 Safari/534.14",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.20 (KHTML, like Gecko) Chrome/11.0.672.2 Safari/534.20",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.27 (KHTML, like Gecko) Chrome/12.0.712.0 Safari/534.27",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.24 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.120 Safari/535.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
    "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre) Gecko/2008072421 Minefield/3.0.2pre",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10",
]
``` 
- 第二招：使用Cookies
这里不使用Cookies也能抓取 故暂未添加

- 第三招：使用代理IP
尤其是京东搜索屏蔽了阿里云的IP  所以不得不使用代理IP 要使用代理IP 就需要构建代理池 代理池的构建下一篇再讲 这里直接调用已经生成好的代理IP地址
需要导入各种可能导致异常的方法![](https://upload-images.jianshu.io/upload_images/3290281-fdac6f5951077c19.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)首先在获取网页时就使用代理IP  
然后捕获状态码异常 再更换IP 常见的错误状态码503，110，111(可自行添加)  或者甭管什么状态码只要不是200 就更换IP重连![](https://upload-images.jianshu.io/upload_images/3290281-39583abacd99bba0.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)**最后还是可能会报异常错误**如超时错误```twisted.internet.error .TimeoutError```等等(免费的代理IP就是问题多) 依然甭管什么错 通通更换IP重连 简单粗暴
![](https://upload-images.jianshu.io/upload_images/3290281-68f91febe7a7550c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

**爬虫三招全都用上 基本上都能顺利爬取**

###### [settings.py](https://github.com/sadjjk/jdGoodsSpider/blob/master/jdGoodsSpider/settings.py)
最后一个文件 这个就非常简单
简单的设置下 
- 默认遵守robots协议 修改为```False```
```ROBOTSTXT_OBEY = False```
- 开启中间件
```
DOWNLOADER_MIDDLEWARES = {
   'jdGoodsSpider.middlewares.UserAgentMiddleware': 543,
   'jdGoodsSpider.middlewares.ProxyMiddleware': 200,
}
```
- 开启pipelines
```
ITEM_PIPELINES = {
   'jdGoodsSpider.pipelines.MongoPipeline': 300,
}
```
```
# 爬取最大页数
MAX_PAGE_NUM = 100
#开始页
START_URL = ['https://search.jd.com/Search?keyword=%E9%9B%B6%E9%A3%9F&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=lingshi&stock=1&click=0&page=1']
#禁止重定向
REDIRECT_ENABLED = False
#超时时间20s
DOWNLOAD_TIMEOUT = 20
#下载延迟1s
DOWNLOAD_DELY = 1
#服务器mongodb内网IP
MONGO_URL = 'mongodb://XXX.XX.XXX.XX/'
#数据库表名
MONGO_DB = 'JD'
```
###### Scrapy代码部分就结束了  
[Github源码](https://github.com/sadjjk/jdGoodsSpider)

##### 下一篇  [ProxyPool动态IP代理池](https://www.jianshu.com/p/6c9d712be5e7)




  









