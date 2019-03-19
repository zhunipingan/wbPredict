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

import time


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
            # charset=settings['MYSQL_CHARSET'],
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

        # if isinstance(item, DailyWeiboItem):
        #     asynItem = copy.deepcopy(item)
        #     # 把要执行的sql放入连接池
        #     query = self.db_pool.runInteraction(self.insert_daily_weibo, asynItem)
        #     # 如果sql执行发送错误,自动回调addErrBack()函数
        #     query.addErrback(self.handle_error, asynItem, spider)

        if isinstance(item, WeiboItem):
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
        elif isinstance(item, RelationshipsItem):
            asynItem = copy.deepcopy(item)
            query = self.db_pool.runInteraction(self.insert_relationship, asynItem)
            query.addErrback(self.handle_error, asynItem, spider)
        elif isinstance(item, CommentItem):
            asynItem = copy.deepcopy(item)
            query = self.db_pool.runInteraction(self.insert_comment, asynItem)
            query.addErrback(self.handle_error, asynItem, spider)

        # # 把要执行的sql放入连接池
        # query = self.db_pool.runInteraction(self.insert_into, item)
        # # 如果sql执行发送错误,自动回调addErrBack()函数
        # query.addErrback(self.handle_error, item, spider)
        # 返回Item
        return item


    def insert_comment(self,cursor,item):
        id = item['_id']
        comment_user_id = item['comment_user_id']
        content = item['content']
        weibo_url = item['weibo_url']
        created_at = item['created_at']
        crawl_time = item['crawl_time']
        get_is_crawled_sql = "select id from comment where id = '%s';" % (id)
        is_crawled = cursor.execute(get_is_crawled_sql)
        if is_crawled == 0:
            insert_relation_sql = "insert into comment(id,comment_user_id,content,weibo_url,created_at,crawl_time)" \
                                  " values('%s','%s','%s','%s','%s','%s');" % (id, comment_user_id, content, weibo_url,created_at,crawl_time)
            cursor.execute(insert_relation_sql)
            print('完成了一次评论表插入')



    def insert_relationship(self,cursor,item):
        _id = item['_id']
        fan_id = item['fan_id']
        followed_id = item['followed_id']
        crawl_time = item['crawl_time']
        get_is_crawled_sql = "select id from relationship where id = '%s';" % (_id)
        is_crawled = cursor.execute(get_is_crawled_sql)
        #如果没有插入过
        if is_crawled == 0:
            insert_relation_sql = "insert into relationship(id,fan_id,followed_id,crawl_time)" \
                                  " values('%s','%s','%s','%s');" %(_id,fan_id,followed_id,crawl_time)
            cursor.execute(insert_relation_sql)
            print('完成了一次粉丝关注关系表插入')


    def insert_information(self,cursor,item):
        _id = item['_id']
        nick_name = item['nick_name']
        gender = item['gender']  # 性别
        province = item['province']  # 所在省 gender,province,city,brief_introduction,birthday,tweets_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication,person_url,crawl_time,labels
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
        portrait = item['portrait']
        try:
            if fans_num is None or follows_num is None or weibo_num is None:
                update_observer = "update observer set crawl_time = '%s',crawl_count = crawl_count + 1,is_exist = 2 where user_id = '%s';" % (
                crawl_time, _id)
                cursor.execute(update_observer)
            else:
                get_is_crawled_sql = "select _id from information where _id = '%s';" % (_id)
                is_crawled =  cursor.execute(get_is_crawled_sql)
                print('is_crawled',is_crawled)
                update_observer = "update observer set crawl_time = '%s',crawl_count = crawl_count + 1,is_exist = 1 where user_id = '%s';" %(crawl_time,_id)

                # print('更新数据sql',update_observer)
                cursor.execute(update_observer)
                if is_crawled == 0:
                    mysqlmd = "insert into information(_id,nick_name,gender,province,city,brief_introduction,birthday," \
                              "weibo_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication," \
                              "person_url,crawl_time,labels,portrait) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'," \
                              "'%s','%s','%s','%s','%s','%s','%s','%s');" % (_id, nick_name, gender, province, city, brief_introduction,
                                                                        birthday, weibo_num, follows_num, fans_num,
                                                                        sex_orientation, sentiment,
                                                                        vip_level, authentication, person_url, crawl_time, labels,portrait)
                    # print('插入个人数据sql', mysqlmd)
                    cursor.execute(mysqlmd)

                else:
                    mysqlmd = "update information set nick_name='%s',gender='%s',province='%s',city='%s'," \
                              "brief_introduction='%s',birthday='%s'," \
                              "weibo_num='%s',follows_num='%s',fans_num='%s',sex_orientation='%s',sentiment='%s'," \
                              "vip_level='%s',authentication='%s'," \
                              "person_url='%s',crawl_time='%s',labels='%s',portrait='%s' where _id = '%s' ;" % (
                              nick_name, gender, province, city, brief_introduction,
                              birthday, weibo_num, follows_num, fans_num,
                              sex_orientation, sentiment,
                              vip_level, authentication, person_url, crawl_time, labels, portrait,_id)
                    print('更新个人information sql', mysqlmd)
                    cursor.execute(mysqlmd)

                insert_into_daily_num_sql = "insert into user_daily_num(weibo_num,follows_num,fans_num,crawl_time,user_id)" \
                                            "values('%s','%s','%s','%s','%s');" % (
                                            weibo_num, follows_num, fans_num, crawl_time, _id)
                cursor.execute(insert_into_daily_num_sql)
                print('完成了一次插入个人信息')
        except Exception as e:
            print('插入个人信息错误',e)

    def insert_weibo(self,cursor,item):
        _id = item['_id']
        weibo_url = item['weibo_url']
        created_at = item['created_at']
        like_num = item['like_num']  # 所在省 gender,province,city,brief_introduction,birthday,tweets_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication,person_url,crawl_time,labels
        repost_num = item['repost_num']  # 所在城市
        comment_num = item['comment_num']  # 简介
        content = item['content']  # 生日
        content = content[:255]
        user_id = item['user_id']  # 微博数
        crawl_time = item['crawl_time']  # 关注数
        last_pic_url = item['last_pic_url']
        pic_url = item['pic_url']
        created_date = created_at.split(' ')[0]
        # if len(last_pic_url)>0:
        #     print('*'*30)
        #     print(type(last_pic_url),str(last_pic_url),type(str(last_pic_url)))
        get_is_crawled_sql = "select _id from weibo where _id = '%s';" % (_id)
        is_crawled = cursor.execute(get_is_crawled_sql)
        if is_crawled == 0:
            mysqlmd = "insert into weibo(_id,weibo_url,created_at,like_num,repost_num,comment_num,content," \
                      "user_id,crawl_time,last_pic_url,pic_url,created_date,crawl_count) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',0);" % (
                      _id, weibo_url, created_at, like_num, repost_num, comment_num,
                      content, user_id, crawl_time, last_pic_url,pic_url,created_date)
            cursor.execute(mysqlmd)
        else:
            mysqlmd = "update weibo set like_num='%s',repost_num='%s',comment_num='%s'," \
                      "crawl_time='%s',crawl_count=crawl_count + 1 where _id = '%s';" % (
                          like_num, repost_num, comment_num,crawl_time,_id)
            cursor.execute(mysqlmd)

        insert_into_daily_num_sql = "insert into weibo_daily_num(weibo_id,like_num,repost_num,comment_num,crawl_time)" \
                                    "values('%s','%s','%s','%s','%s');" % (
                                        _id, like_num, repost_num, comment_num, crawl_time)
        cursor.execute(insert_into_daily_num_sql)

        try:
            # update_weibo_info = "update weibo set crawl_count = crawl_count + 1,crawl_time = '%s' where _id = '%s';"%(crawl_time,weibo_id)
            # cursor.execute(update_weibo_info)
            update_observer_info = "update observer set weibo_crawl_time = '%s' where user_id = '%s';" % (
            crawl_time, _id.split('_')[0])
            cursor.execute(update_observer_info)
            print('完成了一次插入微博互动量', _id)
        except Exception as e:
            print('插入微博互动量错误', e)

    #插入的最新的10条微博的短周期变化,好像与长周期变成一样了，本来不一样，本来想短周期只是小更新
    def insert_daily_weibo(self,cursor,item):
        weibo_id = item['weibo_id']
        like_num = item['like_num']
        repost_num = item['repost_num']
        comment_num = item['comment_num']
        crawl_time = item['crawl_time']

        get_is_crawled_sql = "select _id from weibo where _id = '%s';" % (weibo_id)
        is_crawled = cursor.execute(get_is_crawled_sql)
        #只有在weibo表里已经有这个微博时，才插入
        if is_crawled != 0:
            weibo_url = item['weibo_url']
            created_at = item['created_at']
            content = item['content']  # 生日
            user_id = item['user_id']  # 微博数
            last_pic_url = item['last_pic_url']
            pic_url = item['pic_url']
            created_date = created_at.split(' ')[0]

            mysqlmd = "insert into weibo(_id,weibo_url,created_at,like_num,repost_num,comment_num,content," \
                      "user_id,crawl_time,last_pic_url,pic_url,created_date,crawl_count) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',0);" % (
                          weibo_id, weibo_url, created_at, like_num, repost_num, comment_num,
                          content, user_id, crawl_time, last_pic_url, pic_url, created_date)
            cursor.execute(mysqlmd)

        else:
            mysqlmd = "update weibo set like_num='%s',repost_num='%s',comment_num='%s'," \
                      "crawl_time='%s',crawl_count=crawl_count + 1 where _id = '%s';" % (
                          like_num, repost_num, comment_num, crawl_time, weibo_id)
            cursor.execute(mysqlmd)


        mysqlmd = "insert into weibo_daily_num(weibo_id,like_num,repost_num,comment_num,crawl_time" \
                  ") values('%s','%s','%s','%s','%s');" % (
                  weibo_id,like_num, repost_num, comment_num,crawl_time)
        cursor.execute(mysqlmd)

        try:
            # update_weibo_info = "update weibo set crawl_count = crawl_count + 1,crawl_time = '%s' where _id = '%s';"%(crawl_time,weibo_id)
            # cursor.execute(update_weibo_info)
            update_observer_info = "update observer set weibo_crawl_time = '%s' where user_id = '%s';" % (
            crawl_time, weibo_id.split('_')[0])
            cursor.execute(update_observer_info)
            print('完成了一次插入每日微博互动量', weibo_id)
        except Exception as e:
            print('插入每日微博互动量错误', e)


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
            db='weibosimple'#charset='utf8'
            )
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

