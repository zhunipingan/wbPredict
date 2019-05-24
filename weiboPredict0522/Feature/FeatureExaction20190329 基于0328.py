import pandas as pd
import numpy as np
import IOData.DataToMysql as dataToMysql
from datetime import datetime,timedelta
from pandas import DataFrame
import re

#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)
#设置value的显示长度为100，默认为50
pd.set_option('max_colwidth',100000)


def math_divide(a,b):
    if b == 0 :
        return 0
    else:
        return float(a/b)

def get_user_feature(weibo_data):
    # weibo_data = dataToMysql.get_handled_train_data(rows)
    # weibo_data = dataToMysql.get_handled_predict_data(10)
    userGroup = weibo_data.groupby('uid')#按用户分组，统计各个用户的用户特征
    # weibo_data['sum_weibo'] = np.random.random(100)

    userSum = userGroup.sum()
    userMax = userGroup['sum_interact','forward_count','comment_count','like_count'].max()
    userMin = userGroup['sum_interact','forward_count','comment_count','like_count'].min()
    userAvg = userGroup.mean()
    userLevelGroup = weibo_data.groupby(['uid','level_interact'],as_index=False)
    # print(userLevelGroup.count().info())
    userWeiboCount = userGroup['mid'].count()#userGroup.count()
    # userInteractAverage = userSum/userGroup.count()[['forward_count','comment_count','like_count']]
    userInteractAverage = userGroup.mean()[['forward_count','comment_count','like_count']]
    userInteractAverage = userInteractAverage.applymap(lambda x : round(x))
    # 分别获得每个人的平均转发评论 点赞
    userInteractAverage.columns = ['user_mean_of_forward','user_mean_of_comment','user_mean_of_like']
    #获取每个人的发的微博总数(当series与dataframe的index不一样时是无法添加一列成功的)
    userInteractAverage['user_sum_weibo'] = userWeiboCount
    #用户总互动数
    userInteractAverage['user_sum_interact'] = userSum['sum_interact']
    #用户历史平均互动数
    userInteractAverage['user_avg_interact'] = (userInteractAverage['user_sum_interact']/userInteractAverage['user_sum_weibo']).astype("float")
    #用户平均互动数
    # userInteractAverage['user_avg_interact'] = userAvg['sum_interact']
    #用户总转发数
    userInteractAverage['user_sum_forward'] = userSum['forward_count']
    #用户总点赞数
    userInteractAverage['user_sum_like'] = userSum['like_count']
    #用户总评论数
    userInteractAverage['user_sum_comment'] = userSum['comment_count']
    #用户转发数占比
    userInteractAverage['user_percent_forward'] = userInteractAverage.apply(lambda x : math_divide(x.user_sum_forward,x.user_sum_interact),axis=1)
    #用户评论数占比
    userInteractAverage['user_percent_comment'] = userInteractAverage.apply(lambda x : math_divide(x.user_sum_comment,x.user_sum_interact),axis=1)
    #用户点赞数占比
    userInteractAverage['user_percent_like'] = userInteractAverage.apply(lambda x : math_divide(x.user_sum_like,x.user_sum_interact),axis=1)
    #用户最高互动数
    userInteractAverage['user_max_interact'] = userMax['sum_interact']
    #用户最低互动数
    userInteractAverage['user_min_interact'] = userMin['sum_interact']
    #用户最大评论数
    userInteractAverage['user_max_comment'] = userMax['comment_count']
    #用户最小评论数
    userInteractAverage['user_min_comment'] = userMin['comment_count']
    #用户平均评论数user_mean_of_comment重复
    # userInteractAverage['user_avg_comment'] = userAvg['comment_count']
    #用户最大转发数
    userInteractAverage['user_max_forward'] = userMax['forward_count']
    #用户最小转发数
    userInteractAverage['user_min_forward'] = userMin['forward_count']
    #用户平均转发数
    # userInteractAverage['user_avg_forward'] = userAvg['forward_count']
    #用户最大点赞数
    userInteractAverage['user_max_like'] = userMax['like_count']
    #用户最小点赞数
    userInteractAverage['user_min_like'] = userMin['like_count']
    #用户平均点赞数
    # userInteractAverage['user_avg_like'] = userAvg['like_count']
    #用户三无微博的条数
    userInteractAverage['user_zero_interact'] = weibo_data[weibo_data.sum_interact == 0].groupby('uid')['mid'].count()
    res1 = userLevelGroup.count().set_index('uid')
    #用户位于一档的互动微博数
    userInteractAverage['user_level1_weibo'] = res1[res1['level_interact'] == 1]['mid']
    #用户位于2档的互动微博数
    userInteractAverage['user_level2_weibo'] = res1[res1['level_interact'] == 2]['mid']
    #用户位于3档的互动微博数
    userInteractAverage['user_level3_weibo'] = res1[res1['level_interact'] == 3]['mid']
    #用户位于4档的互动微博数
    userInteractAverage['user_level4_weibo'] = res1[res1['level_interact'] == 4]['mid']
    #用户位于5档的互动微博数
    userInteractAverage['user_level5_weibo'] = res1[res1['level_interact'] == 5]['mid']
    # 填充空值
    userInteractAverage = userInteractAverage.fillna(0)
    #用户位于一档的互动微博数占比
    userInteractAverage['user_percent_level1_weibo'] = userInteractAverage['user_level1_weibo']/userInteractAverage['user_sum_weibo']
    #用户位于2档的互动微博数占比
    userInteractAverage['user_percent_level2_weibo'] = userInteractAverage['user_level2_weibo']/userInteractAverage['user_sum_weibo']
    #用户位于3档的互动微博数占比
    userInteractAverage['user_percent_level3_weibo'] = userInteractAverage['user_level3_weibo']/userInteractAverage['user_sum_weibo']
    #用户位于4档的互动微博数占比
    userInteractAverage['user_percent_level4_weibo'] = userInteractAverage['user_level4_weibo']/userInteractAverage['user_sum_weibo']
    #用户位于5档的互动微博数占比
    userInteractAverage['user_percent_level5_weibo'] = userInteractAverage['user_level5_weibo']/userInteractAverage['user_sum_weibo']
    #用户三无的互动微博数占比
    userInteractAverage['user_percent_zero_interact'] = userInteractAverage['user_zero_interact']/userInteractAverage['user_sum_weibo']

    return userInteractAverage



def get_blog_time_feature2(weibo_data,userInteractAverage):
    weibo_data.sort_values(['uid', 'time'], axis=0, ascending=True, inplace=True)
    last_uid = None
    i = 0
    user_dataframe = pd.DataFrame(
        columns=['mid', 'blog_1day_sum_weibo', 'blog_3day_sum_weibo', 'blog_7day_sum_weibo', 'blog_15day_sum_weibo',
                 'blog_30day_sum_weibo', 'blog_60day_sum_weibo'])
    features = []
    for index, row in weibo_data.iterrows():
        if i % 5000 == 0:
            print('这是第', i, datetime.datetime.now())

        # if i % 10000 == 0:
        #     weibo_data = pd.merge(weibo_data, user_dataframe, how='left', on='mid')
        #     user_dataframe = pd.DataFrame(
        #         columns=['mid', 'blog_1day_sum_weibo', 'blog_3day_sum_weibo', 'blog_7day_sum_weibo',
        #                  'blog_15day_sum_weibo',
        #                  'blog_30day_sum_weibo', 'blog_60day_sum_weibo'])
        time_i = row['time']
        date_i = row['date']
        uid_i = row['uid']
        mid_i = row['mid']

        if last_uid != None and last_uid == uid_i:
            pass
        else:
            the_user_data = weibo_data[(weibo_data.uid == uid_i)]

            last_uid = uid_i
        i = i + 1
        user_dict = {}
        the_user_data_60day = the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= (time_i - timedelta(days=60)))]
        the_user_data_30day = the_user_data_60day[(the_user_data_60day.time >= (time_i - timedelta(days=30)))]
        the_user_data_15day = the_user_data_30day[(the_user_data_30day.time >= (time_i - timedelta(days=15)))]
        the_user_data_7day = the_user_data_15day[(the_user_data_15day.time >= (time_i - timedelta(days=7)))]
        the_user_data_3day = the_user_data_7day[(the_user_data_7day.time >= (time_i - timedelta(days=3)))]
        the_user_data_1day = the_user_data_3day[(the_user_data_3day.time >= (time_i - timedelta(days=1)))]
        user_dict['mid'] = mid_i
        # print(the_user_data_60day.shape[0])
        user_dict['blog_1day_sum_weibo'] = the_user_data_1day.shape[0]
        user_dict['blog_3day_sum_weibo'] = the_user_data_3day.shape[0]
        user_dict['blog_7day_sum_weibo'] = the_user_data_7day.shape[0]
        user_dict['blog_15day_sum_weibo'] = the_user_data_15day.shape[0]
        user_dict['blog_30day_sum_weibo'] = the_user_data_30day.shape[0]
        user_dict['blog_60day_sum_weibo'] = the_user_data_60day.shape[0]

        user_dict['blog_7day_sum_days'] = len(set(the_user_data_7day['date']))
        user_dict['blog_15day_sum_days'] = len(set(the_user_data_15day['date']))
        user_dict['blog_30day_sum_days'] = len(set(the_user_data_30day['date']))
        user_dict['blog_60day_sum_days'] = len(set(the_user_data_60day['date']))
        features.append(user_dict)
        # user_dataframe = user_dataframe.append(user_dict,ignore_index=True)


    print('开始转化为dataframe', datetime.datetime.now())
    user_dataframe = pd.DataFrame(features)
    print('转化为了dataframe',datetime.datetime.now())
    weibo_data = pd.merge(weibo_data,user_dataframe,how='left',on='mid')
    # print(weibo_data[weibo_data.blog_1day_sum_weibo == 0].blog_day_sum_weibo)

    #近七天平均发博条数
    weibo_data['blog_7day_avg_weibo'] = weibo_data['blog_7day_sum_weibo']/weibo_data['blog_7day_sum_days']
    #近15天平均发博条数
    weibo_data['blog_15day_avg_weibo'] = weibo_data['blog_15day_sum_weibo']/weibo_data['blog_15day_sum_days']
    #近30天平均发博条数
    weibo_data['blog_30day_avg_weibo'] = weibo_data['blog_30day_sum_weibo']/weibo_data['blog_30day_sum_days']
    #近60天平均发博条数
    weibo_data['blog_60day_avg_weibo'] = weibo_data['blog_60day_sum_weibo']/weibo_data['blog_60day_sum_days']


    #用户习惯
    #在1-8点发博数目
    weibo_data['blog_1-8hour_sum_weibo'] = the_user_data[(the_user_data.hour >= 1) & (the_user_data.hour <=8)]['mid'].count()
    #在9-17点发博数目
    weibo_data['blog_9-17hour_sum_weibo'] = the_user_data[(the_user_data.hour >= 9) & (the_user_data.hour <=17)]['mid'].count()
    #在18-0点发博数目
    weibo_data['blog_18-0hour_sum_weibo'] = the_user_data[(the_user_data.hour >= 18) | (the_user_data.hour ==0)]['mid'].count()
    #在周末发博数目
    weibo_data['blog_weekend_sum_weibo'] = the_user_data[the_user_data.weekday >= 5]['mid'].count()
    #在周一发博数目
    weibo_data['blog_week1_sum_weibo'] = the_user_data[the_user_data.weekday == 0]['mid'].count()
    #在周二发博数目
    weibo_data['blog_week2_sum_weibo'] = the_user_data[the_user_data.weekday == 1]['mid'].count()
    #在周三发博数目
    weibo_data['blog_week3_sum_weibo'] = the_user_data[the_user_data.weekday == 2]['mid'].count()
    #在周四发博数目
    weibo_data['blog_week4_sum_weibo'] = the_user_data[the_user_data.weekday == 3]['mid'].count()
    #在周五发博数目
    weibo_data['blog_week5_sum_weibo'] = the_user_data[the_user_data.weekday == 4]['mid'].count()

    weibo_data = pd.merge(weibo_data,userInteractAverage,how='left',on='uid')

    #在1-8点发博数目占比
    weibo_data['blog_1-8hour_percent_weibo'] = weibo_data['blog_1-8hour_sum_weibo']/weibo_data['user_sum_weibo']
    #在9-17点发博占比
    weibo_data['blog_9-17hour_percent_weibo'] = weibo_data['blog_9-17hour_sum_weibo']/weibo_data['user_sum_weibo']
    #在18-0点发博占比
    weibo_data['blog_18-0hour_percent_weibo'] = weibo_data['blog_18-0hour_sum_weibo']/weibo_data['user_sum_weibo']
    #在周末发博占比
    weibo_data['blog_weekend_percent_weibo'] = weibo_data['blog_weekend_sum_weibo']/weibo_data['user_sum_weibo']
    #在周一发博占比
    weibo_data['blog_week1_percent_weibo'] = weibo_data['blog_week1_sum_weibo']/weibo_data['user_sum_weibo']
    #在周二发博占比
    weibo_data['blog_week2_percent_weibo'] = weibo_data['blog_week2_sum_weibo']/weibo_data['user_sum_weibo']
    #在周三发博占比
    weibo_data['blog_week3_percent_weibo'] = weibo_data['blog_week3_sum_weibo']/weibo_data['user_sum_weibo']
    #在周四发博占比
    weibo_data['blog_week4_percent_weibo'] = weibo_data['blog_week4_sum_weibo']/weibo_data['user_sum_weibo']
    #在周五发博占比
    weibo_data['blog_week5_percent_weibo'] = weibo_data['blog_week5_sum_weibo']/weibo_data['user_sum_weibo']
    # print(weibo_data.info())

    weibo_data = weibo_data.fillna(0)
    # print(weibo_data.info())
    return weibo_data




        # temp_user_weibo_data = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.time < time_i)]

def get_blog_time_feature3(weibo_data,userInteractAverage):
    weibo_data.insert(10,'blog_1day_sum_weibo',None)
    weibo_data.insert(11,'blog_3day_sum_weibo',None)
    weibo_data.insert(12,'blog_7day_sum_weibo',None)
    weibo_data.insert(13,'blog_15day_sum_weibo',None)
    weibo_data.insert(14,'blog_30day_sum_weibo',None)
    weibo_data.insert(15,'blog_60day_sum_weibo',None)

    # print(weibo_data.info())
    user_array = weibo_data.values
    i = 0
    for row in user_array:
        if i % 1000 ==0:
            print('这是第',i,datetime.datetime.now())
        i = i + 1
        uid = row[0]
        mid = row[1]
        time = row[2]
        date = row[7]
        hour = row[8]
        weekday = row[9]
        row[10] = 12
        row[11] = 12
        row[12] = 12
        row[13] = 12
        row[14] = 12


        # row[10] = [(user_array[:,2] <= time_i) & (the_user_data.time >= (time_i - timedelta(days=60)))]
        # user_array_slice = user_array[(user_array[:, 2] <= time) & (user_array[:, 2] >= (time - timedelta(days=60))), :]
        # row[10] = len(user_array[(user_array[:, 2] <= time) & (user_array[:, 2] >= (time - timedelta(days=60))), :])
        # row[11] = len(user_array[(user_array[:, 2] <= time) & (user_array[:, 2] >= (time - timedelta(days=30))), :])
        # row[12] = len(user_array[(user_array[:, 2] <= time) & (user_array[:, 2] >= (time - timedelta(days=15))), :])
        # row[13] = len(user_array[(user_array[:, 2] <= time) & (user_array[:, 2] >= (time - timedelta(days=7))), :])
        # row[14] = len(user_array[(user_array[:, 2] <= time) & (user_array[:, 2] >= (time - timedelta(days=3))), :])
        # row[15] = len(user_array[(user_array[:, 2] <= time) & (user_array[:, 2] >= (time - timedelta(days=1))), :])

    data  = pd.DataFrame(user_array)
    # print(data)

def get_blog_time_feature4(weibo_data,userInteractAverage):
    i = 0
    for index,row in weibo_data.iterrows():
        if i % 1000 == 0:
            print('这是第',i,datetime.datetime.now())
        i=i+1

def get_content_feature_http(content):
    pattern = re.compile(r'http')
    res = pattern.findall(str(content))
    return len(res)


def get_content_feature_at(content):
    pattern = re.compile(r'@')
    res = pattern.findall(str(content))
    return len(res)


def get_content_feature_topic(content):
    pattern = re.compile(r'#[^#]+#')
    res = pattern.findall(str(content))
    return len(res)


def is_have_zhuanfa_or_dianzan(content,tempStr):
    if tempStr in str(content):
        return 1
    return 0


def is_have_emoji(content):
    pattern = re.compile(r'\[(.{1,10})\].*\[(.{1,10})\]')
    if pattern.search(str(content)):
        return 1
    return 0


def get_content_length(content):
    return len(str(content))


import LDA.lda as lda
def get_blog_content_feature(weibo_data):
    weibo_data['http_number'] = weibo_data.content.apply(lambda x:get_content_feature_http(x,))
    weibo_data['at_number'] = weibo_data.content.apply(lambda x:get_content_feature_at(x))
    weibo_data['weibo_topic_number'] = weibo_data.content.apply(lambda x:get_content_feature_topic(x))
    weibo_data['is_have_zhuanfa'] = weibo_data.content.apply(lambda  x:is_have_zhuanfa_or_dianzan(x,'转发'))
    weibo_data['is_have_dianzan'] = weibo_data.content.apply(lambda  x:is_have_zhuanfa_or_dianzan(x,'点赞'))
    weibo_data['is_have_emoji'] = weibo_data.content.apply(lambda  x:is_have_emoji(x))
    weibo_data['content_length'] = weibo_data.content.apply(lambda  x:get_content_length(x))
    # for index,row in weibo_data.iterrows():
    #     pass

    # weibo_data = lda.do_LDA(weibo_data)
    # print(weibo_data.is_have_emoji)
    return weibo_data


from sklearn.metrics import fbeta_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import shuffle
import datetime
import Preprocessing.Preprocess as Preprocess

nrows = 0
starttime = datetime.datetime.now()
# print(userInteractAverage.info())
weibo_train_data = dataToMysql.get_handled_train_data(nrows)
weibo_predict_data = dataToMysql.get_handled_predict_data(nrows)
# weibo_train_data['content'].astype(str)
# weibo_predict_data['content'].astype(str)
endtime = datetime.datetime.now()
print('read用时'+str((endtime-starttime).seconds))
weibo_predict_data_old = weibo_predict_data.copy()
#数据预处理
weibo_predict_data,new_user_set = Preprocess.process_new_user(weibo_train_data,weibo_predict_data)
weibo_train_data,weibo_predict_data,low_interact_user_set = Preprocess.process_low_interact_user(weibo_train_data,weibo_predict_data)

extra_predict_user = new_user_set | low_interact_user_set
extra_weibo_predict_data = weibo_predict_data_old[weibo_predict_data_old.uid.isin(extra_predict_user)]

#只对在训练集中的用户进行处理
# weibo_predict_data_isin_userList = weibo_psort_values(['uid', 'time'], axis=0, ascending=True, inplace=True)redict_data[weibo_predict_data.uid.isin(set(weibo_train_data.uid))]
starttime1 = datetime.datetime.now()
userInteractAverage = get_user_feature(weibo_train_data)
endtime1 = datetime.datetime.now()
print('userFeature用时'+str((endtime1-starttime1).seconds))

starttime2 = datetime.datetime.now()
weibo_train_data = get_blog_time_feature2(weibo_train_data,userInteractAverage)
endtime2 = datetime.datetime.now()
weibo_train_data.to_csv('../data/weibo_train_data_0402.csv', index=False)
print('blogFeature1用时'+str((endtime2-starttime2).seconds))
starttime3 = datetime.datetime.now()
weibo_predict_data = get_blog_time_feature2(weibo_predict_data,userInteractAverage)
weibo_predict_data.to_csv('../data/weibo_predict_data_0402.csv', index=False)
endtime3 = datetime.datetime.now()
print('blogFeature2用时'+str((endtime3-starttime3).seconds))

#3计算额外内容基本特征
weibo_train_data = get_blog_content_feature(weibo_train_data)
weibo_predict_data = get_blog_content_feature(weibo_predict_data)


target = ['forward_count', 'comment_count', 'like_count']
dropped_train_dataset = ['created_at','uid', 'mid', 'time', 'date', 'sum_interact', 'level_interact','content','content_no_stopwords_list']
dropped_predict_datastet = ['created_at','uid', 'mid', 'time', 'date','content','content_no_stopwords_list']

predictors = [x for x in weibo_train_data.columns if x not in target + dropped_train_dataset]
for item in target:
    weibo_predict_data[item] = 0
    extra_weibo_predict_data[item] = 0
starttime4 = datetime.datetime.now()
# weibo_predict_data_isin_userList = weibo_predict_data[weibo_predict_data.uid.isin(set(weibo_train_data.uid))]
# print(weibo_predict_data_isin_userList.empty)
# if not weibo_predict_data_isin_userList.empty:
from sklearn.model_selection import cross_val_score
#0328交叉验证
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(weibo_train_data[predictors], weibo_train_data['like_count'], test_size=0.2, random_state=42)
# rf = RandomForestRegressor()  # 这里使用了默认的参数设置 0321
# rf.fit(X_train,y_train)
# res = rf.predict(X_test)
# dataframe = X_test.copy()
# dataframe['true_res'] = y_test
# dataframe['predict_res'] = res
# dataframe.to_csv('../data/weibo_res_0328.csv')
from sklearn.externals import joblib


for i in range(len(target)):
    rf = RandomForestRegressor()
    rf.fit(weibo_train_data[predictors], weibo_train_data[target[i]])  # 进行模型的训练
    predict_df_predictions = rf.predict(weibo_predict_data[predictors])
    predict_df_predictions = [int(item) for item in predict_df_predictions]
    weibo_predict_data[target[i]] = predict_df_predictions
    # print(weibo_predict_data[target[i]])

    # print(cross_val_score(rf, weibo_train_data[predictors], weibo_train_data[target[i]], cv=5))
    # 保存model
    # 下面是决策树可视化
    Estimators = rf.estimators_
    print(sorted(zip(map(lambda x: round(x, 4), rf.feature_importances_), predictors), reverse=True))
    print("Model save...")
    model_name = "rf"+str(i)+"train_model0402.m"
    model_save_path = '../model'+ model_name
    joblib.dump(rf,model_save_path)

    train_df_predictions = rf.predict(weibo_train_data[predictors])
    train_df_predictions = [int(item) for item in train_df_predictions]
    weibo_train_data[target[i] + '_new'] = train_df_predictions
train_result = weibo_train_data.loc[:, ['mid', 'uid', 'forward_count', 'comment_count', 'like_count','forward_count_new', 'comment_count_new', 'like_count_new']]
train_result.to_csv(r'D:\graduation project\weiboPredict\train_result0402.csv')
print('保存训练对比数据完成')

endtime4 = datetime.datetime.now()
print('预测用时'+str((endtime4-starttime4).seconds))

#weibo_predict_data.append(weibo_predict_data_old这样不对吧，old就是原来所有的数据
weibo_predict_data = weibo_predict_data.append(extra_weibo_predict_data,sort=False)
result = weibo_predict_data.loc[:, ['mid', 'uid', 'forward_count', 'comment_count', 'like_count']]
# make_feature(1)
result.to_csv(r'D:\graduation project\weiboPredict\result_0402.csv')

text = open('D:\graduation project\weiboPredict\out0402.txt', 'w')
i = 0
len_result = len(result)
for index, item in result.iterrows():
    # print((i * 1.0) / len_result)
    mid = str(item['mid'])
    uid = str(item['uid'])
    forward_count = str(item['forward_count'])
    comment_count = str(item['comment_count'])
    like_count = str(item['like_count'])

    # forward_count = '0'
    # comment_count = '0'
    # like_count = '0'
    out_put = uid + '\t' + mid + '\t' + forward_count + ',' + comment_count + ',' + like_count
    print(out_put, file=text)
text.close()
