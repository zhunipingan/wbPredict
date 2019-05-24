import pandas as pd
import numpy as np
import IOData.DataToMysql as dataToMysql
from datetime import datetime,timedelta
from pandas import DataFrame

# #显示所有列
# pd.set_option('display.max_columns', None)
# #显示所有行
# pd.set_option('display.max_rows', None)
# #设置value的显示长度为100，默认为50
# pd.set_option('max_colwidth',100000)


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
    #用户平均评论数
    userInteractAverage['user_avg_comment'] = userAvg['comment_count']
    #用户最大转发数
    userInteractAverage['user_max_forward'] = userMax['forward_count']
    #用户最小转发数
    userInteractAverage['user_min_forward'] = userMin['forward_count']
    #用户平均转发数
    userInteractAverage['user_avg_forward'] = userAvg['forward_count']
    #用户最大点赞数
    userInteractAverage['user_max_like'] = userMax['like_count']
    #用户最小点赞数
    userInteractAverage['user_min_like'] = userMin['like_count']
    #用户平均点赞数
    userInteractAverage['user_avg_like'] = userAvg['like_count']
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

def get_blog_time_feature(weibo_data,userInteractAverage,rows = 10):
    # weibo_data = dataToMysql.get_handled_train_data(10)

    # weibo_data = dataToMysql.get_handled_predict_data(10)
    #当前微博发博时所属活跃度
    # userTimeOfBlog = userGroup['time']
    #对博文进行一下排序，我想这样可以加快遍历速度，inplace=True代表对原dataframe进行了修改，否则不变
    weibo_data.sort_values(['uid','time'],axis = 0,ascending = True,inplace=True)
    weibo_data['user_1day_sum_weibo'] = None
    last_uid = None
    the_user_data = None
    i = 0
    for index,row in weibo_data.iterrows():
        if i%100 == 0:
            print('这是第',i,datetime.datetime.now())
        time_i = row['time']
        date_i = row['date']
        uid_i = row['uid']
        mid_i = row['mid']

        if last_uid != None and last_uid == uid_i:
            pass
        else:
            the_user_data = weibo_data[(weibo_data.uid == uid_i)]
            # the_user_data = weibo_data.iloc[[i]]
            # print(type(the_user_data.uid))
            # j = i + 1
            # while (weibo_data.iloc[[j]]['uid'] == uid_i):
            #     the_user_data.append(weibo_data.iloc[[j]],ignore_index=True)
            #     j = j + 1
            last_uid = uid_i
        i = i + 1

        # temp_user_weibo_data = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.time < time_i)]
        # weibo_data.loc[index,'user_1day_sum_weibo'] = temp_user_weibo_data[(weibo_data.time >= time_i - timedelta(days=1))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
        # 近1,3,7,15,30,60天发博数量
        the_user_data_60day = the_user_data[(the_user_data.time < time_i) & (the_user_data.time >= time_i - timedelta(days=60))]
        the_user_data_30day = the_user_data_60day[(the_user_data_60day.time >= time_i - timedelta(days=30))]
        the_user_data_15day = the_user_data_30day[(the_user_data_30day.time >= time_i - timedelta(days=15))]
        the_user_data_7day = the_user_data_15day[(the_user_data_15day.time >= time_i - timedelta(days=7))]
        the_user_data_3day = the_user_data_7day[(the_user_data_7day.time >= time_i - timedelta(days=3))]
        the_user_data_1day = the_user_data_3day[(the_user_data_3day.time >= time_i - timedelta(days=1))]

        # the_user_data_60day = the_user_data[(the_user_data.time >= time_i - timedelta(days=60))]
        # the_user_data_30day = the_user_data[(the_user_data.time >= time_i - timedelta(days=30))]
        # the_user_data_15day = the_user_data[(the_user_data.time >= time_i - timedelta(days=15))]
        # the_user_data_7day = the_user_data[(the_user_data.time >= time_i - timedelta(days=7))]
        # the_user_data_3day = the_user_data[(the_user_data.time >= time_i - timedelta(days=3))]
        # the_user_data_1day = the_user_data[(the_user_data.time >= time_i - timedelta(days=1))]
        #
        # user_dataframe = pd.DataFrame(columns=['mid','blog_1day_sum_weibo','blog_3day_sum_weibo','blog_7day_sum_weibo','blog_15day_sum_weibo','blog_30day_sum_weibo','blog_60day_sum_weibo'])
        # user_dataframe.append([mid_i,'0','0','0','0','0','0'])
        # weibo_data = pd.merge(weibo_data,user_dataframe,how='left',on='mid')
        weibo_data.loc[index, 'blog_1day_sum_weibo'] = the_user_data_1day.shape[0]
        weibo_data.loc[index, 'blog_3day_sum_weibo'] = the_user_data_3day.shape[0]
        weibo_data.loc[index, 'blog_7day_sum_weibo'] = the_user_data_7day.shape[0]
        weibo_data.loc[index, 'blog_15day_sum_weibo'] = the_user_data_15day.shape[0]
        weibo_data.loc[index, 'blog_30day_sum_weibo'] = the_user_data_30day.shape[0]
        weibo_data.loc[index, 'blog_60day_sum_weibo'] = the_user_data_60day.shape[0]


        # weibo_data.loc[index,'blog_1day_sum_weibo'] = the_user_data[(the_user_data.time >= time_i - timedelta(days=1))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
        # weibo_data.loc[index,'blog_3day_sum_weibo'] = the_user_data[(the_user_data.time >= time_i - timedelta(days=3))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
        # weibo_data.loc[index, 'blog_7day_sum_weibo'] = the_user_data[
        #     (
        #             the_user_data.time >= time_i - timedelta(days=7))]['mid'].count()
        # weibo_data.loc[index, 'blog_15day_sum_weibo'] = the_user_data[
        #     (
        #             the_user_data.time >= time_i - timedelta(days=15))]['mid'].count()
        # weibo_data.loc[index, 'blog_30day_sum_weibo'] = the_user_data[
        #     (
        #             the_user_data.time >= time_i - timedelta(days=30))]['mid'].count()
        # weibo_data.loc[index, 'blog_60day_sum_weibo'] = the_user_data[
        #     (
        #             the_user_data.time >= time_i - timedelta(days=60))]['mid'].count()

        # weibo_data.resample('')
        #近7天登陆天数
        weibo_data.loc[index, 'blog_7day_sum_days'] = len(set(the_user_data[
            (the_user_data.date >= date_i - timedelta(days=7)) ]['date']))
        #近15天登录天数
        weibo_data.loc[index, 'blog_15day_sum_days'] = len(set(the_user_data[
            (the_user_data.date >= date_i - timedelta(days=15)) ]['date']))
        #近30天登录天数
        weibo_data.loc[index, 'blog_30day_sum_days'] = len(set(the_user_data[
            (the_user_data.date >= date_i - timedelta(days=30)) ]['date']))
        #近60天登录天数
        weibo_data.loc[index, 'blog_60day_sum_days'] = len(set(the_user_data[
            (the_user_data.date >= date_i - timedelta(days=60)) ]['date']))
    #近七天平均发博条数
    weibo_data['blog_7day_avg_weibo'] = weibo_data['blog_7day_sum_weibo']/weibo_data['blog_7day_sum_days']
    #近15天平均发博条数
    weibo_data['blog_15day_avg_weibo'] = weibo_data['blog_15day_sum_weibo']/weibo_data['blog_15day_sum_days']
    #近30天平均发博条数
    weibo_data['blog_30day_avg_weibo'] = weibo_data['blog_30day_sum_weibo']/weibo_data['blog_30day_sum_days']
    #近60天平均发博条数
    weibo_data['blog_60day_avg_weibo'] = weibo_data['blog_60day_sum_weibo']/weibo_data['blog_60day_sum_days']
    #
    #
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

    # print(userInteractAverage)

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
    # weibo_data['sum_weibo'] = userWeiboCount
    weibo_data = weibo_data.fillna(0)
    # print(weibo_data)
    return weibo_data

def get_blog_time_feature_group(weibo_data,userInteractAverage):
    userGroup = weibo_data[['uid','mid','time','date','hour','weekday']].groupby('uid')
    new_user_data = pd.DataFrame(columns=['uid', 'mid', 'time','date','hour','weekday'])
    i = 0
    for group in userGroup:
        the_user_data = group[1]#.copy()
        for index,row in the_user_data.iterrows():
            if i % 100 == 0:
                print('这是第', i, datetime.datetime.now())
            i = i+ 1
            # new_user_data = new_user_data.append(row)
            # new_user_data.loc[index,'']
            time_i = row['time']
            date_i = row['date']
            uid_i = row['uid']
            blog_day_sum_weibo = []
            blog_day_sum_weibo.append(
                the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=1))][
                    'mid'].count())
            blog_day_sum_weibo.append(
                the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=3))][
                    'mid'].count())
            blog_day_sum_weibo.append(
                the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=7))][
                    'mid'].count())
            blog_day_sum_weibo.append(
                the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=15))][
                    'mid'].count())
            blog_day_sum_weibo.append(
                the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=30))][
                    'mid'].count())
            blog_day_sum_weibo.append(
                the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=60))][
                    'mid'].count())

            weibo_data.loc[index,'blog_1day_sum_weibo'] = blog_day_sum_weibo[0]
            weibo_data.loc[index,'blog_3day_sum_weibo'] = blog_day_sum_weibo[1]
            weibo_data.loc[index,'blog_7day_sum_weibo'] = blog_day_sum_weibo[2]
            weibo_data.loc[index,'blog_15day_sum_weibo'] = blog_day_sum_weibo[3]
            weibo_data.loc[index,'blog_30day_sum_weibo'] = blog_day_sum_weibo[4]
            weibo_data.loc[index,'blog_60day_sum_weibo'] = blog_day_sum_weibo[5]

            # weibo_data['blog_1day_sum_weibo'] = None
            # weibo_data['blog_3day_sum_weibo'] = None
            # weibo_data['blog_7day_sum_weibo'] = None
            # weibo_data['blog_15day_sum_weibo'] = None
            # weibo_data['blog_30day_sum_weibo'] = None
            # weibo_data['blog_60day_sum_weibo'] = None
            # weibo_data.loc[index, [
            # 'blog_1day_sum_weibo', 'blog_3day_sum_weibo', 'blog_7day_sum_weibo', 'blog_15day_sum_weibo',
            # 'blog_30day_sum_weibo', 'blog_60day_sum_weibo']] = blog_day_sum_weibo

            # 近1,3,7,15,30,60天发博数量
            # 直接yonglen
            # weibo_data.loc[index,'blog_1day_sum_weibo'] = the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=1))].shape[0]#['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
            # weibo_data.loc[index,'blog_3day_sum_weibo'] = the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=3))].shape[0]#['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
            # weibo_data.loc[index, 'blog_7day_sum_weibo'] = the_user_data[
            #     (the_user_data.time <= time_i) & (
            #             the_user_data.time >= time_i - timedelta(days=7))].shape[0]#['mid'].count()
            # weibo_data.loc[index, 'blog_15day_sum_weibo'] = the_user_data[
            #     (the_user_data.time <= time_i) & (
            #             the_user_data.time >= time_i - timedelta(days=15))].shape[0]#['mid'].count()
            # weibo_data.loc[index, 'blog_30day_sum_weibo'] = the_user_data[
            #     (the_user_data.time <= time_i) & (
            #             the_user_data.time >= time_i - timedelta(days=30))].shape[0]#['mid'].count()
            # weibo_data.loc[index, 'blog_60day_sum_weibo'] = the_user_data[
            #     (the_user_data.time <= time_i) & (
            #             the_user_data.time >= time_i - timedelta(days=60))].shape[0]#['mid'].count()

            # weibo_data.resample('')
            #近7天登陆天数
            weibo_data.loc[index, 'blog_7day_sum_days'] = len(set(the_user_data[
                (the_user_data.date >= date_i - timedelta(days=7)) & (
                        the_user_data.date <= date_i)]['date']))
            #近15天登录天数
            weibo_data.loc[index, 'blog_15day_sum_days'] = len(set(the_user_data[
                (the_user_data.date >= date_i - timedelta(days=15)) & (
                        the_user_data.date <= date_i)]['date']))
            #近30天登录天数
            weibo_data.loc[index, 'blog_30day_sum_days'] = len(set(the_user_data[
                (the_user_data.date >= date_i - timedelta(days=30)) & (
                        the_user_data.date <= date_i)]['date']))
            #近60天登录天数
            weibo_data.loc[index, 'blog_60day_sum_days'] = len(set(the_user_data[
                (the_user_data.date >= date_i - timedelta(days=60)) & (
                        the_user_data.date <= date_i)]['date']))

            # 用户习惯
            # 在1-8点发博数目
            weibo_data.loc[index,'blog_1-8hour_sum_weibo'] = the_user_data[(the_user_data.hour >= 1) & (the_user_data.hour <= 8)][
                'mid'].count()
            # 在9-17点发博数目
            weibo_data.loc[index,'blog_9-17hour_sum_weibo'] = \
            the_user_data[(the_user_data.hour >= 9) & (the_user_data.hour <= 17)]['mid'].count()
            # 在18-0点发博数目
            weibo_data.loc[index,'blog_18-0hour_sum_weibo'] = \
            the_user_data[(the_user_data.hour >= 18) | (the_user_data.hour == 0)]['mid'].count()
            # 在周末发博数目
            weibo_data.loc[index,'blog_weekend_sum_weibo'] = the_user_data[the_user_data.weekday >= 5]['mid'].count()
            # 在周一发博数目
            weibo_data.loc[index,'blog_week1_sum_weibo'] = the_user_data[the_user_data.weekday == 0]['mid'].count()
            # 在周二发博数目
            weibo_data.loc[index,'blog_week2_sum_weibo'] = the_user_data[the_user_data.weekday == 1]['mid'].count()
            # 在周三发博数目
            weibo_data.loc[index,'blog_week3_sum_weibo'] = the_user_data[the_user_data.weekday == 2]['mid'].count()
            # 在周四发博数目
            weibo_data.loc[index,'blog_week4_sum_weibo'] = the_user_data[the_user_data.weekday == 3]['mid'].count()
            # 在周五发博数目
            weibo_data.loc[index,'blog_week5_sum_weibo'] = the_user_data[the_user_data.weekday == 4]['mid'].count()
            # the_user_group.loc[index,'blog_1day_sum_weibo'] = the_user_group[(the_user_group.time <= time_i) & (the_user_group.time >= time_i - timedelta(days=1))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
            # #近1,3,7,15,30,60天发博数量
            # the_user_group.loc[index,'blog_3day_sum_weibo'] = the_user_group[(the_user_group.time <= time_i) & (the_user_group.time >= time_i - timedelta(days=3))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
            # the_user_group.loc[index, 'blog_7day_sum_weibo'] = the_user_group[
            #    (the_user_group.time <= time_i) & (
            #            the_user_group.time >= time_i - timedelta(days=7))]['mid'].count()
            # the_user_group.loc[index, 'blog_15day_sum_weibo'] = the_user_group[
            #     (the_user_group.time <= time_i) & (
            #             the_user_group.time >= time_i - timedelta(days=15))]['mid'].count()
            # the_user_group.loc[index, 'blog_30day_sum_weibo'] = the_user_group[
            #     (the_user_group.time <= time_i) & (
            #             the_user_group.time >= time_i - timedelta(days=30))]['mid'].count()
            # the_user_group.loc[index, 'blog_60day_sum_weibo'] = the_user_group[
            #     (the_user_group.time <= time_i) & (
            #             the_user_group.time >= time_i - timedelta(days=60))]['mid'].count()
            #
            # # weibo_data.resample('')
            # #近7天登陆天数
            # the_user_group.loc[index, 'blog_7day_sum_days'] = len(set(the_user_group[
            #     (the_user_group.date >= date_i - timedelta(days=7)) & (
            #             the_user_group.date <= date_i)]['date']))
            # #近15天登录天数
            # the_user_group.loc[index, 'blog_15day_sum_days'] = len(set(the_user_group[
            #     (the_user_group.date >= date_i - timedelta(days=15)) & (
            #             the_user_group.date <= date_i)]['date']))
            # #近30天登录天数
            # the_user_group.loc[index, 'blog_30day_sum_days'] = len(set(the_user_group[
            #     (the_user_group.date >= date_i - timedelta(days=30)) & (
            #             the_user_group.date <= date_i)]['date']))
            # #近60天登录天数
            # the_user_group.loc[index, 'blog_60day_sum_days'] = len(set(the_user_group[
            #     (the_user_group.date >= date_i - timedelta(days=60)) & (
            #             the_user_group.date <= date_i)]['date']))


    #近七天平均发博条数
    weibo_data['blog_7day_avg_weibo'] = weibo_data['blog_7day_sum_weibo']/weibo_data['blog_7day_sum_days']
    #近15天平均发博条数
    weibo_data['blog_15day_avg_weibo'] = weibo_data['blog_15day_sum_weibo']/weibo_data['blog_15day_sum_days']
    #近30天平均发博条数
    weibo_data['blog_30day_avg_weibo'] = weibo_data['blog_30day_sum_weibo']/weibo_data['blog_30day_sum_days']
    #近60天平均发博条数
    weibo_data['blog_60day_avg_weibo'] = weibo_data['blog_60day_sum_weibo']/weibo_data['blog_60day_sum_days']

    # print(userInteractAverage)

    weibo_data = pd.merge(weibo_data, userInteractAverage, how='left', on='uid')

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
    # weibo_data['sum_weibo'] = userWeiboCount
    weibo_data = weibo_data.fillna(0)


        # print(the_user_group)
        # new_user_data = new_user_data.append(the_user_group,ignore_index=True,sort=False)
    # print(weibo_data)
    return weibo_data




from sklearn.metrics import fbeta_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import shuffle
import datetime

nrows = 0
starttime = datetime.datetime.now()
# print(userInteractAverage.info())
weibo_train_data = dataToMysql.get_handled_train_data(nrows)
weibo_predict_data = dataToMysql.get_handled_predict_data(nrows)
endtime = datetime.datetime.now()
print('read用时'+str((endtime-starttime).seconds))
#只对在训练集中的用户进行处理
# weibo_predict_data_isin_userList = weibo_predict_data[weibo_predict_data.uid.isin(set(weibo_train_data.uid))]
starttime1 = datetime.datetime.now()
userInteractAverage = get_user_feature(weibo_train_data)
endtime1 = datetime.datetime.now()
print('userFeature用时'+str((endtime1-starttime1).seconds))

starttime2 = datetime.datetime.now()
weibo_train_data = get_blog_time_feature(weibo_train_data,userInteractAverage)
endtime2 = datetime.datetime.now()
print('blogFeature1用时'+str((endtime2-starttime2).seconds))
starttime3 = datetime.datetime.now()
weibo_predict_data = get_blog_time_feature(weibo_predict_data,userInteractAverage)
endtime3 = datetime.datetime.now()
print('blogFeature2用时'+str((endtime3-starttime3).seconds))


target = ['forward_count', 'comment_count', 'like_count']
dropped_train_dataset = ['uid', 'mid', 'time', 'date', 'sum_interact', 'level_interact','content']
dropped_predict_datastet = ['uid', 'mid', 'time', 'date','content']

predictors = [x for x in weibo_train_data.columns if x not in target + dropped_train_dataset]

for item in target:
    weibo_predict_data[item] = 0
starttime4 = datetime.datetime.now()
weibo_predict_data_isin_userList = weibo_predict_data[weibo_predict_data.uid.isin(set(weibo_train_data.uid))]
# print(weibo_predict_data_isin_userList.empty)
if not weibo_predict_data_isin_userList.empty:
    for i in range(len(target)):
        rf = RandomForestRegressor()  # 这里使用了默认的参数设置
        rf.fit(weibo_train_data[predictors], weibo_train_data[target[i]])  # 进行模型的训练
        predict_df_predictions = rf.predict(weibo_predict_data[predictors])
        predict_df_predictions = [int(item) for item in predict_df_predictions]
        weibo_predict_data[target[i]] = predict_df_predictions
        # print(weibo_predict_data[target[i]])
endtime4 = datetime.datetime.now()
print('预测用时'+str((endtime4-starttime4).seconds))

result = weibo_predict_data.loc[:, ['mid', 'uid', 'forward_count', 'comment_count', 'like_count']]
# make_feature(1)
result.to_csv(r'D:\graduation project\weiboPredict\result.csv')

text = open('D:\graduation project\weiboPredict\out1.txt', 'w')
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
from sklearn.model_selection import cross_val_score
rf = RandomForestRegressor()  # 这里使用了默认的参数设置
print(cross_val_score(rf,weibo_train_data[predictors], weibo_train_data[target[i]], cv=5).mean())





def get_blog_time_feature1(weibo_data,userInteractAverage,rows = 10):
    # weibo_data = dataToMysql.get_handled_train_data(10)

    # weibo_data = dataToMysql.get_handled_predict_data(10)
    #当前微博发博时所属活跃度
    # userTimeOfBlog = userGroup['time']
    #对博文进行一下排序，我想这样可以加快遍历速度
    weibo_data.sort_values(['uid','time'],axis = 0,ascending = True)
    weibo_data['user_1day_sum_weibo'] = None
    for index,row in weibo_data.iterrows():
        time_i = row['time']
        date_i = row['date']
        uid_i = row['uid']
        # the_user_data = weibo_data[(weibo_data.uid == uid_i)
        # temp_user_weibo_data = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.time < time_i)]
        # weibo_data.loc[index,'user_1day_sum_weibo'] = temp_user_weibo_data[(weibo_data.time >= time_i - timedelta(days=1))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
        #近1,3,7,15,30,60天发博数量
        weibo_data.loc[index,'blog_1day_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.time <= time_i) & (weibo_data.time >= time_i - timedelta(days=1))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
        weibo_data.loc[index,'blog_3day_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.time <= time_i) & (weibo_data.time >= time_i - timedelta(days=3))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
        weibo_data.loc[index, 'blog_7day_sum_weibo'] = weibo_data[
            (weibo_data.uid == uid_i) & (weibo_data.time <= time_i) & (
                        weibo_data.time >= time_i - timedelta(days=7))]['mid'].count()
        weibo_data.loc[index, 'blog_15day_sum_weibo'] = weibo_data[
            (weibo_data.uid == uid_i) & (weibo_data.time <= time_i) & (
                        weibo_data.time >= time_i - timedelta(days=15))]['mid'].count()
        weibo_data.loc[index, 'blog_30day_sum_weibo'] = weibo_data[
            (weibo_data.uid == uid_i) & (weibo_data.time <= time_i) & (
                        weibo_data.time >= time_i - timedelta(days=30))]['mid'].count()
        weibo_data.loc[index, 'blog_60day_sum_weibo'] = weibo_data[
            (weibo_data.uid == uid_i) & (weibo_data.time <= time_i) & (
                        weibo_data.time >= time_i - timedelta(days=60))]['mid'].count()

        # weibo_data.resample('')
        #近7天登陆天数
        weibo_data.loc[index, 'blog_7day_sum_days'] = len(set(weibo_data[
            (weibo_data.uid == uid_i) &
            (weibo_data.date >= date_i - timedelta(days=7)) & (
                        weibo_data.date <= date_i)]['date']))
        #近15天登录天数
        weibo_data.loc[index, 'blog_15day_sum_days'] = len(set(weibo_data[
            (weibo_data.uid == uid_i) &
            (weibo_data.date >= date_i - timedelta(days=15)) & (
                        weibo_data.date <= date_i)]['date']))
        #近30天登录天数
        weibo_data.loc[index, 'blog_30day_sum_days'] = len(set(weibo_data[
            (weibo_data.uid == uid_i) &
            (weibo_data.date >= date_i - timedelta(days=30)) & (
                        weibo_data.date <= date_i)]['date']))
        #近60天登录天数
        weibo_data.loc[index, 'blog_60day_sum_days'] = len(set(weibo_data[
            (weibo_data.uid == uid_i) &
            (weibo_data.date >= date_i - timedelta(days=60)) & (
                        weibo_data.date <= date_i)]['date']))
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
    weibo_data['blog_1-8hour_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.hour >= 1) & (weibo_data.hour <=8)]['mid'].count()
    #在9-17点发博数目
    weibo_data['blog_9-17hour_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.hour >= 9) & (weibo_data.hour <=17)]['mid'].count()
    #在18-0点发博数目
    weibo_data['blog_18-0hour_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.hour >= 18) | (weibo_data.hour ==0)]['mid'].count()
    #在周末发博数目
    weibo_data['blog_weekend_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & weibo_data.weekday >= 5]['mid'].count()
    #在周一发博数目
    weibo_data['blog_week1_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & weibo_data.weekday == 0]['mid'].count()
    #在周二发博数目
    weibo_data['blog_week2_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & weibo_data.weekday == 1]['mid'].count()
    #在周三发博数目
    weibo_data['blog_week3_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & weibo_data.weekday == 2]['mid'].count()
    #在周四发博数目
    weibo_data['blog_week4_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & weibo_data.weekday == 3]['mid'].count()
    #在周五发博数目
    weibo_data['blog_week5_sum_weibo'] = weibo_data[(weibo_data.uid == uid_i) & weibo_data.weekday == 4]['mid'].count()

    # print(userInteractAverage)

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
    # weibo_data['sum_weibo'] = userWeiboCount
    weibo_data = weibo_data.fillna(0)
    # print(weibo_data)
    return weibo_data

def get_blog_time_feature2(weibo_data,userInteractAverage,rows = 10):
    # weibo_data = dataToMysql.get_handled_train_data(10)

    # weibo_data = dataToMysql.get_handled_predict_data(10)
    #当前微博发博时所属活跃度
    # userTimeOfBlog = userGroup['time']
    #对博文进行一下排序，我想这样可以加快遍历速度，inplace=True代表对原dataframe进行了修改，否则不变
    weibo_data.sort_values(['uid','time'],axis = 0,ascending = True,inplace=True)
    weibo_data['user_1day_sum_weibo'] = None

    last_uid = None
    the_user_data = None
    i=0
    # for index,row in weibo_data.iterrows():
    #     if i%1000 == 0:
    #         print('这是第',i,datetime.datetime.now())
    #
    #
    #     time_i = row['time']
    #     date_i = row['date']
    #     uid_i = row['uid']
    #     if last_uid != None and last_uid == uid_i:
    #         pass
    #     else:
    #         the_user_data = weibo_data[(weibo_data.uid == uid_i)]
    #         # the_user_data = weibo_data.iloc[[i]]
    #         # print(type(the_user_data.uid))
    #         # j = i + 1
    #         # while (weibo_data.iloc[[j]]['uid'] == uid_i):
    #         #     the_user_data.append(weibo_data.iloc[[j]],ignore_index=True)
    #         #     j = j + 1
    #         last_uid = uid_i
    #     i = i + 1
    #
    #     # temp_user_weibo_data = weibo_data[(weibo_data.uid == uid_i) & (weibo_data.time < time_i)]
    #     # weibo_data.loc[index,'user_1day_sum_weibo'] = temp_user_weibo_data[(weibo_data.time >= time_i - timedelta(days=1))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
    #     #近1,3,7,15,30,60天发博数量
    #     weibo_data.loc[index,'blog_1day_sum_weibo'] = the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=1))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
    #     weibo_data.loc[index,'blog_3day_sum_weibo'] = the_user_data[(the_user_data.time <= time_i) & (the_user_data.time >= time_i - timedelta(days=3))]['mid'].count()#and weibo_data.time >= time_i - timedelta(days=1)
    #     weibo_data.loc[index, 'blog_7day_sum_weibo'] = the_user_data[
    #         (the_user_data.uid == uid_i) &(the_user_data.time <= time_i) & (
    #                 the_user_data.time >= time_i - timedelta(days=7))]['mid'].count()
    #     weibo_data.loc[index, 'blog_15day_sum_weibo'] = the_user_data[
    #         (the_user_data.uid == uid_i) & (the_user_data.time <= time_i) & (
    #                 the_user_data.time >= time_i - timedelta(days=15))]['mid'].count()
    #     weibo_data.loc[index, 'blog_30day_sum_weibo'] = the_user_data[
    #         (the_user_data.time <= time_i) & (
    #                 the_user_data.time >= time_i - timedelta(days=30))]['mid'].count()
    #     weibo_data.loc[index, 'blog_60day_sum_weibo'] = the_user_data[
    #         (the_user_data.time <= time_i) & (
    #                 the_user_data.time >= time_i - timedelta(days=60))]['mid'].count()
    #
    #     # weibo_data.resample('')
    #     #近7天登陆天数
    #     weibo_data.loc[index, 'blog_7day_sum_days'] = len(set(the_user_data[
    #         (the_user_data.date >= date_i - timedelta(days=7)) & (
    #                 the_user_data.date <= date_i)]['date']))
    #     #近15天登录天数
    #     weibo_data.loc[index, 'blog_15day_sum_days'] = len(set(the_user_data[
    #         (the_user_data.date >= date_i - timedelta(days=15)) & (
    #                 the_user_data.date <= date_i)]['date']))
    #     #近30天登录天数
    #     weibo_data.loc[index, 'blog_30day_sum_days'] = len(set(the_user_data[
    #         (the_user_data.date >= date_i - timedelta(days=30)) & (
    #                 the_user_data.date <= date_i)]['date']))
    #     #近60天登录天数
    #     weibo_data.loc[index, 'blog_60day_sum_days'] = len(set(the_user_data[
    #         (the_user_data.date >= date_i - timedelta(days=60)) & (
    #                 the_user_data.date <= date_i)]['date']))
    # #近七天平均发博条数
    # weibo_data['blog_7day_avg_weibo'] = weibo_data['blog_7day_sum_weibo']/weibo_data['blog_7day_sum_days']
    # #近15天平均发博条数
    # weibo_data['blog_15day_avg_weibo'] = weibo_data['blog_15day_sum_weibo']/weibo_data['blog_15day_sum_days']
    # #近30天平均发博条数
    # weibo_data['blog_30day_avg_weibo'] = weibo_data['blog_30day_sum_weibo']/weibo_data['blog_30day_sum_days']
    # #近60天平均发博条数
    # weibo_data['blog_60day_avg_weibo'] = weibo_data['blog_60day_sum_weibo']/weibo_data['blog_60day_sum_days']
    #
    #
    # #用户习惯
    # #在1-8点发博数目
    # weibo_data['blog_1-8hour_sum_weibo'] = the_user_data[(the_user_data.hour >= 1) & (the_user_data.hour <=8)]['mid'].count()
    # #在9-17点发博数目
    # weibo_data['blog_9-17hour_sum_weibo'] = the_user_data[(the_user_data.hour >= 9) & (the_user_data.hour <=17)]['mid'].count()
    # #在18-0点发博数目
    # weibo_data['blog_18-0hour_sum_weibo'] = the_user_data[(the_user_data.hour >= 18) | (the_user_data.hour ==0)]['mid'].count()
    # #在周末发博数目
    # weibo_data['blog_weekend_sum_weibo'] = the_user_data[the_user_data.weekday >= 5]['mid'].count()
    # #在周一发博数目
    # weibo_data['blog_week1_sum_weibo'] = the_user_data[the_user_data.weekday == 0]['mid'].count()
    # #在周二发博数目
    # weibo_data['blog_week2_sum_weibo'] = the_user_data[the_user_data.weekday == 1]['mid'].count()
    # #在周三发博数目
    # weibo_data['blog_week3_sum_weibo'] = the_user_data[the_user_data.weekday == 2]['mid'].count()
    # #在周四发博数目
    # weibo_data['blog_week4_sum_weibo'] = the_user_data[the_user_data.weekday == 3]['mid'].count()
    # #在周五发博数目
    # weibo_data['blog_week5_sum_weibo'] = the_user_data[the_user_data.weekday == 4]['mid'].count()

    # print(userInteractAverage)

    weibo_data = pd.merge(weibo_data,userInteractAverage,how='left',on='uid')

    # #在1-8点发博数目占比
    # weibo_data['blog_1-8hour_percent_weibo'] = weibo_data['blog_1-8hour_sum_weibo']/weibo_data['user_sum_weibo']
    # #在9-17点发博占比
    # weibo_data['blog_9-17hour_percent_weibo'] = weibo_data['blog_9-17hour_sum_weibo']/weibo_data['user_sum_weibo']
    # #在18-0点发博占比
    # weibo_data['blog_18-0hour_percent_weibo'] = weibo_data['blog_18-0hour_sum_weibo']/weibo_data['user_sum_weibo']
    # #在周末发博占比
    # weibo_data['blog_weekend_percent_weibo'] = weibo_data['blog_weekend_sum_weibo']/weibo_data['user_sum_weibo']
    # #在周一发博占比
    # weibo_data['blog_week1_percent_weibo'] = weibo_data['blog_week1_sum_weibo']/weibo_data['user_sum_weibo']
    # #在周二发博占比
    # weibo_data['blog_week2_percent_weibo'] = weibo_data['blog_week2_sum_weibo']/weibo_data['user_sum_weibo']
    # #在周三发博占比
    # weibo_data['blog_week3_percent_weibo'] = weibo_data['blog_week3_sum_weibo']/weibo_data['user_sum_weibo']
    # #在周四发博占比
    # weibo_data['blog_week4_percent_weibo'] = weibo_data['blog_week4_sum_weibo']/weibo_data['user_sum_weibo']
    # #在周五发博占比
    # weibo_data['blog_week5_percent_weibo'] = weibo_data['blog_week5_sum_weibo']/weibo_data['user_sum_weibo']
    # # weibo_data['sum_weibo'] = userWeiboCount
    weibo_data = weibo_data.fillna(0)
    # print(weibo_data)
    return weibo_data

