import datetime
import time
import pymysql
from pymysql import cursors
from scrapy import cmdline
import subprocess


def doSth():
    # 把爬虫程序放在这个类里
    print(u'这个程序要开始疯狂的运转啦')

def search_user():
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='weibosimple')
    cur = conn.cursor()
    # sql = "select user_id,crawl_time,frequency_id from observer where is_exist <> 2"
    sql = "select o.user_id,o.crawl_time,f.frequency_value from weibosimple.observer o LEFT JOIN weibosimple.frequency f on o.frequency_id = f.frequency_id where is_exist <> 2"
    reCount = cur.execute(sql)  # 返回受影响的行数
    data = cur.fetchall()  # 返回数据,返回的是tuple类型
    cur.close()
    conn.close()
    user_id_list = []
    for element in data:
        #如果上次抓取时间为空，则马上就进行抓取
        if element[1] is None or element[2] is None :
            user_id_list.append(str(element[0]))
        #否则判断抓取时间是否超过了24小时
        else:
            last_time = element[1]
            frequency = element[2]*3600
            now = datetime.datetime.now()
            # print(frequency, now,last_time,(now - last_time).seconds)
            if (now - last_time).total_seconds() >= frequency:#2790:seconds只是计算忽略了天的差值，total_seconds才是真正的差
                user_id_list.append(str(element[0]))
    # print(user_id_list)
    return user_id_list


def search_weibo_in_observer_table():
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='weibosimple')
    cur = conn.cursor()
    sql = "select user_id,weibo_crawl_time,crawl_time from observer where is_exist <> 2"
    reCount = cur.execute(sql)  # 返回受影响的行数
    data = cur.fetchall()  # 返回数据,返回的是tuple类型
    cur.close()
    conn.close()
    user_id_list = []
    for element in data:
        #如果上次抓取时间为空，则马上就进行抓取
        now = datetime.datetime.now()
        if element[2] is not None and (now - element[2]).total_seconds() >= 900:
            if element[1] is None:
                user_id_list.append(str(element[0]))
            #否则判断抓取时间是否超过了24小时
            else:
                last_time = element[1]
                if (now - last_time).total_seconds() >= 900:
                    user_id_list.append(str(element[0]))
    return user_id_list


def search_weibo():
    conn = pymysql.connect(host='localhost', user='root', passwd='123456', db='weibosimple')
    cur = conn.cursor()
    sql = "select _id,crawl_time from weibo"
    reCount = cur.execute(sql)  # 返回受影响的行数
    data = cur.fetchall()  # 返回数据,返回的是tuple类型
    cur.close()
    conn.close()
    weibo_id_list = []
    for element in data:
        # 如果上次抓取时间为空，则马上就进行抓取,实际这种情况不应该发生，因为这条信息插入时一定有时间
        if element[1] is None:
            weibo_id_list.append(str(element[0]))
        # 否则判断抓取时间是否超过了24小时
        else:
            last_time = element[1]
            now = datetime.datetime.now()
            if (now - last_time).seconds >= 30:
                weibo_id_list.append(str(element[0]))
    return weibo_id_list


def do_crawl_user_or_weibo(user_id_list = [],weibo_id_list = []):
    user_id_list_str = ';'.join(user_id_list)
    weibo_id_list_str = ';'.join(weibo_id_list)
    #scrapy的cmdline.excute执行结束后，会退出当前进程，所以你在一个主进程中执行，会全部退出，后面的也不再执行。
    # cmdline.execute(('scrapy crawl weibo_spider -a user_id_list=' + user_id_list_str).split())
    cmd = 'scrapy crawl weibo_spider -a user_id_list=' + user_id_list_str +' -a weibo_id_list=' + weibo_id_list_str
    subprocess.Popen(cmd)
    return





# 一般网站都是1:00点更新数据，所以每天凌晨一点启动
def main(h=1, m=0):
    i = 0
    while True:
        i = i + 1
        print('正在进行第',i,'次监视...*****************************',datetime.datetime.now())
        user_id_list = search_user()
        weibo_id_list = search_weibo_in_observer_table()
        print('此次爬取的用户个数为', len(user_id_list),'微博条数为',len(weibo_id_list))
        if len(user_id_list) > 0 or len(weibo_id_list) > 0:
            do_crawl_user_or_weibo(user_id_list,weibo_id_list)
            print("*"*10,'爬好一遍了')


        # print(now.hour, now.minute)
        # if now.hour == h and now.minute == m:
        #     doSth()
        # 每隔60秒检测一次
        time.sleep(30)
main()
# search_user()