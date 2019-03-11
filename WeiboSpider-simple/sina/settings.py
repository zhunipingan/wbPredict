# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False

# 请将Cookie替换成你自己的Cookie
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':'_T_WM=4fa783161019163220f8424e3ea2b267; ALF=1554859517; SCF=AtHaPSPb88FNlnqQd9yQ8zSh2F9fsK3mj3yqqBA4CNYIjvzpkIjTrr4GSjRTUrNWCqPbafPTbCwy_zFb9Jm4OEs.; SUB=_2A25xgcitDeRhGeNI7lsX8ibNzjqIHXVSjejlrDV6PUNbktAKLWPQkW1NSFoXVxdDY9uWm7wfRsYsOz2vNkZp7uzK; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhB.v8aPKOi8PVk412PjS2h5JpX5KzhUgL.Fo-cSK.ceonpSKq2dJLoIE9iPEH8SEHWSC-4xFH8SFHFxFHWeFH8SCHF1CHFeEH8SCHWxC-R1Btt; SUHB=0FQrUXqfRg0QKy; SSOLoginState=1552267517'
}

# 当前是单账号，所以下面的 CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 请不要修改

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}

ITEM_PIPELINES = {
    'sina.pipelines.ToMysqlTwistedPipeline': 300,
}

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Sina'

# 数据库地址
MYSQL_HOST = 'localhost'
# 数据库用户名:
MYSQL_USER = 'root'
#数据库密码
MYSQL_PASSWORD = '123456'
#数据库端口
MYSQL_PORT = 3306
#数据库名称
MYSQL_DBNAME = 'weibosimple'
#数据库编码
MYSQL_CHARSET = 'utf8'