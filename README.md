# torrent自动下载
Scrapy 高阶玩法：

-  爬取1024社区
-  筛选种子的作者进行爬取
-  将种子和种子配图通过FilesPipeline快速下载到本地
-  将种子和种子配图可以通过Email发送到指定邮箱

### 运行环境
Python 3.6
Scrapy 框架
BeautifulSoup4
Requests

### 安装运行环境
*这里只展示linux的的安装*

首先安装Python
''' shell
Arch系
sudo pacman -S python
Debian系
sudo apt-get install python
''' 

然后安装其它运行环境
<code>pip install scrape beautifulsoup4 requests</code>

### 使用方法

在 settings.py 文件里面，需要配置：

```py
ROOT_URL = "http://t66y.com/"        # 这里需要更新到草榴（第一会所、桃花族）的最新的地址
FILES_STORE = '/home/morzlee/sis_output'  #这里是爬虫的输出文件夹									# 这里是用126邮箱做例子，并不局限126邮箱
SMTP_HOST = "smtp.126.com"          # 发送邮件的smtp服务器
SMTP_USER = "XXXXXX@126.com"       # 用于登录smtp服务器的用户名，也就是发送者的邮箱
SMTP_PWD = "XXXXXXX"             # 授权码，和用户名user一起，用于登录smtp， 非邮箱密码
SMTP_PORT = 25                      # smtp服务器SSL端口号，默认是465，具体是什么，网上一搜邮箱域名和他的smtp就知道了
SMTP_SENDER = "XXXXXX@126.com"      # 发送方的邮箱
SMTP_TO_LIST = ["YYYYYY@126.com", "ZZZZZZ@126.com"]     # 发送目标邮箱地址，是个list
```

还有BLOCK_ID和AUTHOR_NAME信息都要根据自己的实际情况进行修改

同时需要注意，邮箱的配置，目前可以参考[这篇文章](https://www.cnblogs.com/xcblogs-python/p/5727238.html)设置即可，随后会更新文档。

