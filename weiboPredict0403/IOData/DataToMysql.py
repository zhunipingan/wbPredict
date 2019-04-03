import pandas as pd
import pymysql
from datetime import datetime, timedelta
import time


weibo_train_data = None
weibo_predict_data = None


def get_train_data(rows=0):
    global weibo_train_data
    if rows == 0:
        data = pd.read_table(r'D:\graduation project\Weibo Data0223\weibo_train_data.txt', header=None,
                         names=['uid', 'mid', 'time', 'forward_count', 'comment_count', 'like_count', 'content'])#.set_index('mid',False)
    else:
        data = pd.read_table(r'D:\graduation project\Weibo Data0223\weibo_train_data.txt', header=None,nrows=rows,
                             names=['uid', 'mid', 'time', 'forward_count', 'comment_count', 'like_count', 'content'])#.set_index('mid',False)
    weibo_train_data = data
    return data


def get_predict_data(rows=0):
    global weibo_predict_data
    if rows == 0 :
        data = pd.read_table(r'D:\graduation project\Weibo Data0223\weibo_predict_data.txt', header=None,
                         names=['uid', 'mid', 'time', 'content','forward_count', 'comment_count', 'like_count'])#.set_index('mid',False)
    else:
        data = pd.read_table(r'D:\graduation project\Weibo Data0223\weibo_predict_data.txt', header=None,nrows=rows,
                             names=['uid', 'mid', 'time', 'content', 'forward_count', 'comment_count', 'like_count'])#.set_index('mid',False)
    weibo_predict_data = data
    return data

def math_get_sum(a,b,c):
    return a+b+c


def math_divide_sum_interact(number):
    if number >= 0 and number <= 5 :
        return 1
    elif number >= 6 and number <= 10 :
        return 2
    elif number >= 11 and number <= 50 :
        return 3
    elif number >= 51 and number <= 100 :
        return 4
    else:
        return 5




def handle_train_data():
    global weibo_train_data
    # 规范化博文时间
    weibo_train_data.time = weibo_train_data.time.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    weibo_train_data['date'] = weibo_train_data.time.apply(lambda x: datetime.date(x))
    weibo_train_data['hour'] = weibo_train_data.time.apply(lambda x: x.hour)
    weibo_train_data['weekday'] = weibo_train_data.time.apply(lambda x: datetime.weekday(x))
    # 计算每一条博文对应的总互动数
    weibo_train_data['sum_interact'] = weibo_train_data.apply(lambda x : x.forward_count + x.comment_count + x.like_count,axis = 1)
    #计算当前的总互动数所属的等级
    weibo_train_data['level_interact']= weibo_train_data.sum_interact.apply(lambda x : math_divide_sum_interact(x))


def handle_predict_data():
    global weibo_predict_data
    # 规范化博文时间
    weibo_predict_data.time = weibo_predict_data.time.apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    weibo_predict_data['date'] = weibo_predict_data.time.apply(lambda x: datetime.date(x))
    weibo_predict_data['hour'] = weibo_predict_data.time.apply(lambda x: x.hour)
    weibo_predict_data['weekday'] = weibo_predict_data.time.apply(lambda x: datetime.weekday(x))


def get_handled_train_data(rows = 0):
    global weibo_train_data
    get_train_data(rows)
    handle_train_data()
    return weibo_train_data

def get_handled_predict_data(rows = 0):
    global weibo_predict_data
    get_predict_data(rows)
    handle_predict_data()
    return weibo_predict_data

# data = pd.read_table(r'D:\graduation project\Weibo Data0223\weibo_weibo_predict_data.txt',header=None,names=['uid','mid','time','forward_count','comment_count','like_count','content'])
# print(data)
# data.to_csv(r'D:\graduation project\Weibo Data0223\weibo_predict_data.csv')
#
# sqlUtil = MySQLUtil('localhost','3306','root','123456','weibo','weibo_weibo_predict_data')
# sqlUtil.df_write_mysql(data)


# mysql('10.246.40.209',3306,'root','123456','miningtest')
# conn = pymysql.connect(host = '10.246.40.209',port = 3306,user= 'root',password= '123456',database = 'miningtest')
# conn = create_engine('mysql+pymysql://' + 'root' + ':' + '123456' + '@' + 'localhost' + ':' + '3306' + '/' + 'weibo'+ '?charset=utf8mb4')#+ '?charset=utf8mb4'?charset=utf8mb4
# data.to_sql('weibo_data3',conn,if_exists='append',index = False)


