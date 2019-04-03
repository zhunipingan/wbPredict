import pymysql
from sqlalchemy import create_engine
import pandas as pd
import datetime
from sklearn.externals import joblib
import os
import re


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

# # data = pd.read_table(r'D:\graduation project\Weibo Data0223\weibo_train_data.txt',header=None,names=['uid','mid','time','forward_count','comment_count','like_count','content'],nrows=10)
# # print(data)
#
# conn = pymysql.connect(host = 'localhost',port = 3306,user= 'root',password= '123456',database = 'weibo')
# conn = create_engine('mysql+pymysql://' + 'root' + ':' + '123456' + '@' + 'localhost' + ':' + '3306' + '/' + 'weibo'+ '?charset=utf8mb4')#+ '?charset=utf8mb4'?charset=utf8mb4
# # data.to_sql('weibo_data0401',conn,if_exists='append',index = False)

conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='weibosimple'  # charset='utf8'
    )
cursor = conn.cursor()
_id = '1699432410_HkBSGogKg'
user_id = '1699432410'
created_at = '2019-03-24 00:00:00'

select_weibo_sql = "select _id,user_id,created_at,content from weibo"
reCount = cursor.execute(select_weibo_sql)  # 返回受影响的行数
data = cursor.fetchall()  # 返回数据,返回的是tuple类型
# 更新用户特征，用于预测0323，每插入一条微博就更新一次用户特征
# calculate_user_feature_sql = "insert into predict_user_feature " \
#                              "select '%s' as id,new_weibo2.*," \
#                              "IFNULL(user_sum_forward/user_sum_weibo,0) AS user_percent_forward," \
#                              "IFNULL(user_sum_like/user_sum_weibo,0) AS user_percent_like," \
#                              "IFNULL(user_sum_comment/user_sum_weibo,0) AS user_percent_comment," \
#                              "IFNULL(user_zero_interact/user_sum_weibo,0) AS user_percent_zero_interact," \
#                              "IFNULL(user_level1_weibo/user_sum_weibo,0) AS user_percent_level1_weibo," \
#                              "IFNULL(user_level2_weibo/user_sum_weibo,0) AS user_percent_level2_weibo," \
#                              "IFNULL(user_level3_weibo/user_sum_weibo,0) AS user_percent_level3_weibo," \
#                              "IFNULL(user_level4_weibo/user_sum_weibo,0) AS user_percent_level4_weibo," \
#                              "IFNULL(user_level5_weibo/user_sum_weibo,0) AS user_percent_level5_weibo " \
#                              "from" \
#                              "(select " \
#                              "count(*) as user_sum_weibo," \
#                              "SUM(repost_num) as user_sum_forward," \
#                              "SUM(like_num) as user_sum_like," \
#                              "SUM(comment_num) as user_sum_comment," \
#                              "SUM(user_sum_interact) as user_sum_interact," \
#                              "MAX(repost_num) as user_max_forward," \
#                              "MAX(like_num) as user_max_like," \
#                              "MAX(comment_num) as user_max_comment," \
#                              "MAX(user_sum_interact) AS user_max_interact," \
#                              "MIN(repost_num) as user_min_forward," \
#                              "MIN(like_num) as user_min_like," \
#                              "MIN(comment_num) as user_min_comment," \
#                              "MIN(user_sum_interact) as user_min_interact," \
#                              "IFNULL(AVG(repost_num),0) as user_avg_forward," \
#                              "IFNULL(AVG(like_num),0) as user_avg_like," \
#                              "IFNULL(AVG(comment_num),0) as user_avg_comment," \
#                              "IFNULL(AVG(user_sum_interact),0) AS user_avg_interact," \
#                              "COUNT(if(repost_num = 0 and like_num = 0 and comment_num = 0,TRUE,NULL)) as user_zero_interact," \
#                              "COUNT(if(user_sum_interact <= 5,TRUE,NULL)) as user_level1_weibo," \
#                              "COUNT(if(user_sum_interact <= 10 and user_sum_interact >= 6,TRUE,NULL)) as user_level2_weibo," \
#                              "COUNT(if(user_sum_interact <= 50 and user_sum_interact >= 11,TRUE,NULL)) as user_level3_weibo," \
#                              "COUNT(if(user_sum_interact <= 100 and user_sum_interact >= 51,TRUE,NULL)) as user_level4_weibo," \
#                              "COUNT(if(user_sum_interact >= 101,TRUE,NULL)) as user_level5_weibo " \
#                              "from" \
#                              "(" \
#                              "SELECT *,(repost_num+like_num+comment_num) as user_sum_interact " \
#                              "from weibo where user_id = '%s'" \
#                              ") as new_weibo" \
#                              ") as new_weibo2" % (_id, user_id)
# print('特征计算sql', calculate_user_feature_sql)
# cursor.execute(calculate_user_feature_sql)
# print('完成一次用户特征计算（微博）')
#
# calculate_weibo_feature_sql = "insert into predict_weibo_feature " \
#                               "SELECT '%s' as id," \
#                               "blog_1day_sum_weibo,blog_3day_sum_weibo,blog_7day_sum_weibo,blog_15day_sum_weibo," \
#                               "blog_30day_sum_weibo,blog_60day_sum_weibo,blog_7day_sum_days," \
#                               "blog_15day_sum_days,blog_30day_sum_days,blog_60day_sum_days," \
#                               "blog_1_8hour_sum_weibo,blog_9_17hour_sum_weibo,blog_18_0hour_sum_weibo," \
#                               "blog_weekend_sum_weibo,blog_week1_sum_weibo,blog_week2_sum_weibo," \
#                               "blog_week3_sum_weibo,blog_week4_sum_weibo,blog_week5_sum_weibo," \
#                               "IFNULL(blog_7day_sum_weibo/blog_7day_sum_days,0) as blog_7day_avg_weibo," \
#                               "IFNULL(blog_15day_sum_weibo/blog_15day_sum_days,0) as blog_15day_avg_weibo," \
#                               "IFNULL(blog_30day_sum_weibo/blog_30day_sum_days,0) as blog_30day_avg_weibo," \
#                               "IFNULL(blog_60day_sum_weibo/blog_60day_sum_days,0) as blog_60day_avg_weibo," \
#                               "IFNULL(blog_1_8hour_sum_weibo/sum_weibo,0) as blog_1_8hour_percent_weibo," \
#                               "IFNULL(blog_9_17hour_sum_weibo/sum_weibo,0) as blog_9_17hour_percent_weibo," \
#                               "IFNULL(blog_18_0hour_sum_weibo/sum_weibo,0) as blog_18_0hour_percent_weibo," \
#                               "IFNULL(blog_weekend_sum_weibo/sum_weibo,0) as blog_weekend_sum_weibo," \
#                               "IFNULL(blog_week1_sum_weibo/sum_weibo,0) as blog_week1_percent_weibo," \
#                               "IFNULL(blog_week2_sum_weibo/sum_weibo,0) as blog_week2_percent_weibo," \
#                               "IFNULL(blog_week3_sum_weibo/sum_weibo,0) as blog_week3_percent_weibo," \
#                               "IFNULL(blog_week4_sum_weibo/sum_weibo,0) as blog_week4_percent_weibo," \
#                               "IFNULL(blog_week5_sum_weibo/sum_weibo,0) as blog_week5_percent_weibo " \
#                               "from " \
#                               "(SELECT " \
#                               "COUNT(*) as sum_weibo," \
#                               "COUNT(IF(DATE_SUB(CURDATE(), INTERVAL 1 DAY) <= created_at,TRUE,NULL)) as blog_1day_sum_weibo," \
#                               "COUNT(IF(DATE_SUB(CURDATE(), INTERVAL 3 DAY) <= created_at,TRUE,NULL)) as blog_3day_sum_weibo," \
#                               "COUNT(IF(DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= created_at,TRUE,NULL)) as blog_7day_sum_weibo," \
#                               "COUNT(IF(DATE_SUB(CURDATE(), INTERVAL 15 DAY) <= created_at,TRUE,NULL)) as blog_15day_sum_weibo," \
#                               "COUNT(IF(DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= created_at,TRUE,NULL)) as blog_30day_sum_weibo," \
#                               "COUNT(IF(DATE_SUB(CURDATE(), INTERVAL 60 DAY) <= created_at,TRUE,NULL)) as blog_60day_sum_weibo," \
#                               "COUNT(DISTINCT CASE WHEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= created_date then created_date else NULL END) as blog_7day_sum_days," \
#                               "COUNT(DISTINCT CASE WHEN DATE_SUB(CURDATE(), INTERVAL 15 DAY) <= created_date then created_date else NULL END) as blog_15day_sum_days," \
#                               "COUNT(DISTINCT CASE WHEN DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= created_date then created_date else NULL END) as blog_30day_sum_days," \
#                               "COUNT(DISTINCT CASE WHEN DATE_SUB(CURDATE(), INTERVAL 60 DAY) <= created_date then created_date else NULL END) as blog_60day_sum_days," \
#                               "COUNT(IF(HOUR(created_at) >= 1 and HOUR(created_at) <= 8,TRUE,NULL)) as blog_1_8hour_sum_weibo," \
#                               "COUNT(IF(HOUR(created_at) >= 9 and HOUR(created_at) <= 17,TRUE,NULL)) as blog_9_17hour_sum_weibo," \
#                               "COUNT(IF(HOUR(created_at) >= 18 or HOUR(created_at) = 0,TRUE,NULL)) as blog_18_0hour_sum_weibo," \
#                               "COUNT(IF(DAYOFWEEK(created_at) = 6 or DAYOFWEEK(created_at) = 7,TRUE,NULL)) as blog_weekend_sum_weibo," \
#                               "COUNT(IF(DAYOFWEEK(created_at) = 1,TRUE,NULL)) as blog_week1_sum_weibo," \
#                               "COUNT(IF(DAYOFWEEK(created_at) = 2,TRUE,NULL)) as blog_week2_sum_weibo," \
#                               "COUNT(IF(DAYOFWEEK(created_at) = 3,TRUE,NULL)) as blog_week3_sum_weibo," \
#                               "COUNT(IF(DAYOFWEEK(created_at) = 4,TRUE,NULL)) as blog_week4_sum_weibo," \
#                               "COUNT(IF(DAYOFWEEK(created_at) = 5,TRUE,NULL)) as blog_week5_sum_weibo " \
#                               "from weibo WHERE user_id = '%s') as aaaa" % (_id, user_id)
#
# print('特征计算sql', calculate_weibo_feature_sql)
# cursor.execute(calculate_weibo_feature_sql)
# print('完成一次微博特征计算（微博）')
dataframe_list = []
_id_list = []
for weibo in data:
    _id = weibo[0]
    _id_list.append(_id)
    user_id = weibo[1]
    created_at = weibo[2]
    content = weibo[3]

    calculate_feature_sql = "select DAYOFWEEK('%s') as weekday,'%s' as created_at,'%s' as content,new_weibo2.*," \
                            "IFNULL(user_sum_forward/user_sum_weibo,0) AS user_percent_forward," \
                            "IFNULL(user_sum_like/user_sum_weibo,0) AS user_percent_like," \
                            "IFNULL(user_sum_comment/user_sum_weibo,0) AS user_percent_comment," \
                            "IFNULL(user_zero_interact/user_sum_weibo,0) AS user_percent_zero_interact," \
                            "IFNULL(user_level1_weibo/user_sum_weibo,0) AS user_percent_level1_weibo," \
                            "IFNULL(user_level2_weibo/user_sum_weibo,0) AS user_percent_level2_weibo," \
                            "IFNULL(user_level3_weibo/user_sum_weibo,0) AS user_percent_level3_weibo," \
                            "IFNULL(user_level4_weibo/user_sum_weibo,0) AS user_percent_level4_weibo," \
                            "IFNULL(user_level5_weibo/user_sum_weibo,0) AS user_percent_level5_weibo, " \
                            "IFNULL(blog_7day_sum_weibo/blog_7day_sum_days,0) as blog_7day_avg_weibo," \
                            "IFNULL(blog_15day_sum_weibo/blog_15day_sum_days,0) as blog_15day_avg_weibo," \
                            "IFNULL(blog_30day_sum_weibo/blog_30day_sum_days,0) as blog_30day_avg_weibo," \
                            "IFNULL(blog_60day_sum_weibo/blog_60day_sum_days,0) as blog_60day_avg_weibo," \
                            "IFNULL(blog_1_8hour_sum_weibo/user_sum_weibo,0) as blog_1_8hour_percent_weibo," \
                            "IFNULL(blog_9_17hour_sum_weibo/user_sum_weibo,0) as blog_9_17hour_percent_weibo," \
                            "IFNULL(blog_18_0hour_sum_weibo/user_sum_weibo,0) as blog_18_0hour_percent_weibo," \
                            "IFNULL(blog_weekend_sum_weibo/user_sum_weibo,0) as blog_weekend_percent_weibo," \
                            "IFNULL(blog_week1_sum_weibo/user_sum_weibo,0) as blog_week1_percent_weibo," \
                            "IFNULL(blog_week2_sum_weibo/user_sum_weibo,0) as blog_week2_percent_weibo," \
                            "IFNULL(blog_week3_sum_weibo/user_sum_weibo,0) as blog_week3_percent_weibo," \
                            "IFNULL(blog_week4_sum_weibo/user_sum_weibo,0) as blog_week4_percent_weibo," \
                            "IFNULL(blog_week5_sum_weibo/user_sum_weibo,0) as blog_week5_percent_weibo " \
                            "from" \
                            "(select count(*) as user_sum_weibo," \
                            "IFNULL(SUM(repost_num),0) as user_sum_forward," \
                            "IFNULL(SUM(like_num),0) as user_sum_like," \
                            "IFNULL(SUM(comment_num),0) as user_sum_comment," \
                            "IFNULL(SUM(user_sum_interact),0) as user_sum_interact," \
                            "IFNULL(MAX(repost_num),0) as user_max_forward," \
                            "IFNULL(MAX(like_num),0) as user_max_like," \
                            "IFNULL(MAX(comment_num),0) as user_max_comment," \
                            "IFNULL(MAX(user_sum_interact),0) AS user_max_interact," \
                            "IFNULL(MIN(repost_num),0) as user_min_forward," \
                            "IFNULL(MIN(like_num),0) as user_min_like," \
                            "IFNULL(MIN(comment_num),0) as user_min_comment," \
                            "IFNULL(MIN(user_sum_interact),0) as user_min_interact," \
                            "IFNULL(AVG(repost_num),0) as user_avg_forward," \
                            "IFNULL(AVG(like_num),0) as user_avg_like," \
                            "IFNULL(AVG(comment_num),0) as user_avg_comment," \
                            "IFNULL(AVG(user_sum_interact),0) AS user_avg_interact," \
                            "COUNT(if(repost_num = 0 and like_num = 0 and comment_num = 0,TRUE,NULL)) as user_zero_interact," \
                            "COUNT(if(user_sum_interact <= 5,TRUE,NULL)) as user_level1_weibo," \
                            "COUNT(if(user_sum_interact <= 10 and user_sum_interact >= 6,TRUE,NULL)) as user_level2_weibo," \
                            "COUNT(if(user_sum_interact <= 50 and user_sum_interact >= 11,TRUE,NULL)) as user_level3_weibo," \
                            "COUNT(if(user_sum_interact <= 100 and user_sum_interact >= 51,TRUE,NULL)) as user_level4_weibo," \
                            "COUNT(if(user_sum_interact >= 101,TRUE,NULL)) as user_level5_weibo, " \
                            "COUNT(IF(DATE_SUB('%s', INTERVAL 1 DAY) <= created_at,TRUE,NULL)) as blog_1day_sum_weibo," \
                            "COUNT(IF(DATE_SUB('%s', INTERVAL 3 DAY) <= created_at,TRUE,NULL)) as blog_3day_sum_weibo," \
                            "COUNT(IF(DATE_SUB('%s', INTERVAL 7 DAY) <= created_at,TRUE,NULL)) as blog_7day_sum_weibo," \
                            "COUNT(IF(DATE_SUB('%s', INTERVAL 15 DAY) <= created_at,TRUE,NULL)) as blog_15day_sum_weibo," \
                            "COUNT(IF(DATE_SUB('%s', INTERVAL 30 DAY) <= created_at,TRUE,NULL)) as blog_30day_sum_weibo," \
                            "COUNT(IF(DATE_SUB('%s', INTERVAL 60 DAY) <= created_at,TRUE,NULL)) as blog_60day_sum_weibo," \
                            "COUNT(DISTINCT CASE WHEN DATE_SUB('%s', INTERVAL 7 DAY) <= created_date then created_date else NULL END) as blog_7day_sum_days," \
                            "COUNT(DISTINCT CASE WHEN DATE_SUB('%s', INTERVAL 15 DAY) <= created_date then created_date else NULL END) as blog_15day_sum_days," \
                            "COUNT(DISTINCT CASE WHEN DATE_SUB('%s', INTERVAL 30 DAY) <= created_date then created_date else NULL END) as blog_30day_sum_days," \
                            "COUNT(DISTINCT CASE WHEN DATE_SUB('%s', INTERVAL 60 DAY) <= created_date then created_date else NULL END) as blog_60day_sum_days," \
                            "COUNT(IF(HOUR(created_at) >= 1 and HOUR(created_at) <= 8,TRUE,NULL)) as blog_1_8hour_sum_weibo," \
                            "COUNT(IF(HOUR(created_at) >= 9 and HOUR(created_at) <= 17,TRUE,NULL)) as blog_9_17hour_sum_weibo," \
                            "COUNT(IF(HOUR(created_at) >= 18 or HOUR(created_at) = 0,TRUE,NULL)) as blog_18_0hour_sum_weibo," \
                            "COUNT(IF(DAYOFWEEK(created_at) = 6 or DAYOFWEEK(created_at) = 7,TRUE,NULL)) as blog_weekend_sum_weibo," \
                            "COUNT(IF(DAYOFWEEK(created_at) = 1,TRUE,NULL)) as blog_week1_sum_weibo," \
                            "COUNT(IF(DAYOFWEEK(created_at) = 2,TRUE,NULL)) as blog_week2_sum_weibo," \
                            "COUNT(IF(DAYOFWEEK(created_at) = 3,TRUE,NULL)) as blog_week3_sum_weibo," \
                            "COUNT(IF(DAYOFWEEK(created_at) = 4,TRUE,NULL)) as blog_week4_sum_weibo," \
                            "COUNT(IF(DAYOFWEEK(created_at) = 5,TRUE,NULL)) as blog_week5_sum_weibo " \
                            "from" \
                            "(" \
                            "SELECT *,IFNULL(repost_num+like_num+comment_num,0) as user_sum_interact " \
                            "from weibo where user_id = '%s' and created_at < '%s'" \
                            ") as new_weibo" \
                            ") as new_weibo2" % (created_at,created_at,content,created_at, created_at, created_at, created_at, created_at
                                    , created_at, created_at, created_at, created_at, created_at,user_id, created_at)
    # print(calculate_feature_sql)
    cursor.execute(calculate_feature_sql)
    data = cursor.fetchall()
    # print(data)
    dataframe_list.extend(data)
    # print(data)
    # print([x[0] for x in cursor.description])
print(dataframe_list)

dataframe = pd.DataFrame(dataframe_list,columns=[x[0] for x in cursor.description])
# 0401去除多余的列
# dataframe = init_dataframe([x[0] for x in cursor.description if x[0] not in ['id']])
print(dataframe)
print(dataframe.columns)
print('完成一次微博特征计算（微博）')
cursor.close()
conn.commit()
conn.close()

dataframe.rename(columns={'blog_1_8hour_percent_weibo': 'blog_1-8hour_percent_weibo', 'blog_9_17hour_percent_weibo': 'blog_9-17hour_percent_weibo', 'blog_18_0hour_percent_weibo': 'blog_18-0hour_percent_weibo'}, inplace=True)
# print(dataframe)
dataframe['hour'] = dataframe['created_at'].apply(lambda x:str(x).split(' ')[1].split(':')[0])
# dataframe['user_mean_of_forward'] = dataframe['user_avg_forward']
# dataframe['user_mean_of_like'] = dataframe['user_avg_like']
# dataframe['user_mean_of_comment'] = dataframe['user_avg_comment']

dataframe['http_number'] = dataframe.content.apply(lambda x:get_content_feature_http(x,))
dataframe['at_number'] = dataframe.content.apply(lambda x:get_content_feature_at(x))
dataframe['weibo_topic_number'] = dataframe.content.apply(lambda x:get_content_feature_topic(x))
dataframe['is_have_zhuanfa'] = dataframe.content.apply(lambda  x:is_have_zhuanfa_or_dianzan(x,'转发'))
dataframe['is_have_dianzan'] = dataframe.content.apply(lambda  x:is_have_zhuanfa_or_dianzan(x,'点赞'))
dataframe['is_have_emoji'] = dataframe.content.apply(lambda  x:is_have_emoji(x))
dataframe['content_length'] = dataframe.content.apply(lambda  x:get_content_length(x))



dropped_train_dataset = ['uid', 'mid', 'created_at', 'date', 'sum_interact', 'level_interact', 'content']
model_save_dir = "D:\graduation project\weiboPredict"
predictors = [x for x in dataframe.columns if x not in dropped_train_dataset]
target = ['repost_num', 'comment_num', 'like_num']

print('开始预测啦')
res_dataframe = pd.DataFrame({'id':_id_list})
for i in range(len(target)):
    starttime4 = datetime.datetime.now()
    model_name = "modelrf"+str(i)+"train_model0403rf.m"
    rf = joblib.load(os.path.join(model_save_dir,model_name))
    predict_df_predictions = rf.predict(dataframe[predictors])
    predict_df_predictions = [int(item) for item in predict_df_predictions]
    print('预测结果',predict_df_predictions)
    res_dataframe[target[i]] = predict_df_predictions
    # print(cross_val_score(rf, weibo_train_data[predictors], weibo_train_data[target[i]], cv=5))
    endtime4 = datetime.datetime.now()
    print('预测用时'+str((endtime4-starttime4).seconds))
print('res_dataframe',res_dataframe)
# insert_conn = pymysql.connect(host = 'localhost',port = 3306,user= 'root',password= '123456',database = 'weibosimple')
insert_conn = create_engine('mysql+pymysql://' + 'root' + ':' + '123456' + '@' + 'localhost' + ':' + '3306' + '/' + 'weibosimple'+ '?charset=utf8mb4')#+ '?charset=utf8mb4'?charset=utf8mb4
res_dataframe.to_sql('predict_weibo_result',insert_conn,if_exists='replace',index = False)
# insertsql = "insert into predict_weibo_result(id,repost_num,comment_num,like_num) values('%s','%s','%s','%s');" %(_id,res[0],res[1],res[2])
# conn = pymysql.connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     passwd='123456',
#     db='weibosimple'  # charset='utf8'
# )
# cursor = conn.cursor()
# cursor.execute(insertsql)
# cursor.close()
# conn.commit()
# conn.close()