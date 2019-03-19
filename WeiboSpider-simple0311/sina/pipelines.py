# -*- coding: utf-8 -*-
import pymongo
from pymongo.errors import DuplicateKeyError
from sina.settings import LOCAL_MONGO_HOST, LOCAL_MONGO_PORT, DB_NAME

import time
import codecs
# class MongoDBPipeline(object):
#     def __init__(self):
#         client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
#         db = client[DB_NAME]
#         self.Information = db["Information"]
#         self.Tweets = db["Tweets"]
#         self.Comments = db["Comments"]
#         self.Relationships = db["Relationships"]
#
#     def process_item(self, item, spider):
#         """ 判断item的类型，并作相应的处理，再入数据库 """
#         # today = time.strftime('%Y-%m%d',time.localtime())
#         # fileName = "weiobosimple"+today+'.txt'
#         #
#         # with codecs.open(fileName,'a','utf-8') as fp:
#         #     fp.write("%s \t %s \t %s \t" %(item['_id'],item['weibo_url'],item['content']))
#         # return item
#         if isinstance(item, RelationshipsItem):
#             self.insert_item(self.Relationships, item)
#         elif isinstance(item, TweetsItem):
#             self.insert_item(self.Tweets, item)
#         elif isinstance(item, InformationItem):
#             self.insert_item(self.Information, item)
#         elif isinstance(item, CommentItem):
#             self.insert_item(self.Comments, item)
#         return item
#
#     @staticmethod
#     def insert_item(collection, item):
#         try:
#             collection.insert(dict(item))
#         except DuplicateKeyError:
#             """
#             说明有重复数据
#             """
#             pass

import pymysql
import copy
from sina.items import RelationshipsItem, WeiboItem, InformationItem, CommentItem
#这是异步存入数据
from pymysql import cursors
from twisted.enterprise import adbapi


class ToMysqlTwistedPipeline(object):

    # 初始化函数
    def __init__(self, db_pool):
        self.db_pool = db_pool

    # 从settings配置文件中读取参数
    @classmethod
    def from_settings(cls, settings):
        # 用一个db_params接收连接数据库的参数
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)

        # 返回一个pipeline对象
        return cls(db_pool)

    # 处理item函数
    def process_item(self, item, spider):

        if isinstance(item, RelationshipsItem):
            self.insert_item(self.Relationships, item)
        elif isinstance(item, WeiboItem):
            asynItem = copy.deepcopy(item)
            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_weibo, asynItem)
            # 如果sql执行发送错误,自动回调addErrBack()函数
            query.addErrback(self.handle_error, asynItem, spider)

        elif isinstance(item, InformationItem):
            # 深拷贝,解决因爬取和存数据库速度不同，造成的数据重复问题
            asynItem = copy.deepcopy(item)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_information, asynItem)
            # 如果sql执行发送错误,自动回调addErrBack()函数
            query.addErrback(self.handle_error, asynItem, spider)
            # self.insert_information(asynItem)
        elif isinstance(item, CommentItem):
            self.insert_item(self.Comments, item)

        # # 把要执行的sql放入连接池
        # query = self.db_pool.runInteraction(self.insert_into, item)
        # # 如果sql执行发送错误,自动回调addErrBack()函数
        # query.addErrback(self.handle_error, item, spider)
        # 返回Item
        return item

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO qisuu (book_classsify,book_name,book_click,book_size,book_type,book_date,book_rate,book_author,book_run,book_onlin) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            item['book_classsify'], item['book_name'], item['book_click'], item['book_size'], item['book_type'],
            item['book_date'], item['book_rate'], item['book_author'], item['book_run'], item['book_onlin'])
        # 执行sql语句
        cursor.execute(sql)
        # 错误函数

    def insert_information(self,cursor,item):
        _id = item['_id']
        nick_name = item['nick_name']
        gender = item['gender']  # 性别
        province = item[
            'province']  # 所在省 gender,province,city,brief_introduction,birthday,tweets_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication,person_url,crawl_time,labels
        city = item['city']  # 所在城市
        brief_introduction = item['brief_introduction']  # 简介
        birthday = item['birthday']  # 生日
        weibo_num = item['weibo_num']  # 微博数
        follows_num = item['follows_num']  # 关注数
        fans_num = item['fans_num']  # 粉丝数
        sex_orientation = item['sex_orientation']  # 性取向
        sentiment = item['sentiment']  # 感情状况
        vip_level = item['vip_level']  # 会员等级
        authentication = item['authentication']  # 认证
        person_url = item['person_url']  # 首页链接
        crawl_time = item['crawl_time']  # 抓取时间戳
        labels = item['labels']  # 标签

        mysqlmd = "insert into information(_id,nick_name,gender,province,city,brief_introduction,birthday," \
                  "weibo_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication," \
                  "person_url,crawl_time,labels) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                  "'%s','%s','%s','%s','%s','%s','%s');" % (_id, nick_name, gender, province, city, brief_introduction,
                                                            birthday, weibo_num, follows_num, fans_num,
                                                            sex_orientation, sentiment,
                                                            vip_level, authentication, person_url, crawl_time, labels)
        cursor.execute(mysqlmd)

    def insert_weibo(self,cursor,item):
        _id = item['_id']
        weibo_url = item['weibo_url']
        created_at = item['created_at']
        like_num = item['like_num']  # 所在省 gender,province,city,brief_introduction,birthday,tweets_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication,person_url,crawl_time,labels
        repost_num = item['repost_num']  # 所在城市
        comment_num = item['comment_num']  # 简介
        content = item['content']  # 生日
        user_id = item['user_id']  # 微博数
        crawl_time = item['crawl_time']  # 关注数

        mysqlmd = "insert into weibo(_id,weibo_url,created_at,like_num,repost_num,comment_num,content," \
                  "user_id,crawl_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
                  _id, weibo_url, created_at, like_num, repost_num, comment_num,
                  content, user_id, crawl_time)

        cursor.execute(mysqlmd)

    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print(failure)


#这是同步存数据
class MysqlPipeline(object):
    def process_item(self,item,spider):
        self.conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='weibosimple',
            charset='utf8')
        self.cur = self.conn.cursor()
        print('******************mysql数据库初始化完成**************************')
        if isinstance(item, RelationshipsItem):
            self.insert_item(self.Relationships, item)
        elif isinstance(item, WeiboItem):
            asynItem = copy.deepcopy(item)
            self.insert_weibo(asynItem)
        elif isinstance(item, InformationItem):
            # 深拷贝,解决因爬取和存数据库速度不同，造成的数据重复问题
            asynItem = copy.deepcopy(item)
            self.insert_information(asynItem)
        elif isinstance(item, CommentItem):
            self.insert_item(self.Comments, item)

        self.cur.close()
        self.conn.commit()
        self.conn.close()
        return item

    def insert_information(self,item):
        _id = item['_id']
        nick_name = item['nick_name']
        gender = item['gender']  # 性别
        province = item[
            'province']  # 所在省 gender,province,city,brief_introduction,birthday,tweets_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication,person_url,crawl_time,labels
        city = item['city']  # 所在城市
        brief_introduction = item['brief_introduction']  # 简介
        birthday = item['birthday']  # 生日
        weibo_num = item['weibo_num']  # 微博数
        follows_num = item['follows_num']  # 关注数
        fans_num = item['fans_num']  # 粉丝数
        sex_orientation = item['sex_orientation']  # 性取向
        sentiment = item['sentiment']  # 感情状况
        vip_level = item['vip_level']  # 会员等级
        authentication = item['authentication']  # 认证
        person_url = item['person_url']  # 首页链接
        crawl_time = item['crawl_time']  # 抓取时间戳
        labels = item['labels']  # 标签

        mysqlmd = "insert into information(_id,nick_name,gender,province,city,brief_introduction,birthday," \
                  "weibo_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication," \
                  "person_url,crawl_time,labels) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                  "'%s','%s','%s','%s','%s','%s','%s');" % (_id, nick_name, gender, province, city, brief_introduction,
                                                            birthday, weibo_num, follows_num, fans_num,
                                                            sex_orientation, sentiment,
                                                            vip_level, authentication, person_url, crawl_time, labels)
        self.cur.execute(mysqlmd)

    def insert_weibo(self, item):
        _id = item['_id']
        weibo_url = item['weibo_url']
        created_at = item['created_at']
        like_num = item['like_num']  # 所在省 gender,province,city,brief_introduction,birthday,tweets_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication,person_url,crawl_time,labels
        repost_num = item['repost_num']  # 所在城市
        comment_num = item['comment_num']  # 简介
        content = item['content']  # 生日
        user_id = item['user_id']  # 微博数
        crawl_time = item['crawl_time']  # 关注数

        mysqlmd = "insert into weibo(_id,weibo_url,created_at,like_num,repost_num,comment_num,content," \
                  "user_id,crawl_time) values('%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (
                  _id, weibo_url, created_at, like_num, repost_num, comment_num,
                  content, user_id, crawl_time)

        self.cur.execute(mysqlmd)

