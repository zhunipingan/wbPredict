import pandas as pd
import numpy as np
import IOData.DataToMysql as DataToMysql
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

#将新用户从预测集里挑出来
def process_new_user(train_data,predict_data):
    train_data_user_set = set(train_data['uid'])#.unique()
    predict_data_user_set = set(predict_data['uid'])#.unique
    new_user_set = predict_data_user_set - train_data_user_set
    print('process 训练集里的用户数',len(train_data_user_set))
    print('process 预测集里的用户数',len(predict_data_user_set))
    print('process 预测集里的新用户数',len(new_user_set))
    predict_data = predict_data[~(predict_data.uid.isin(new_user_set))]
    print('process 预测集去除新用户后的条数',len(predict_data))
    return predict_data,new_user_set

def get_user_sum_interact(train_data):
    user_group = train_data.groupby('uid')
    user_interact = user_group.sum_interact.sum().reset_index(name='user_interact')
    user_weibo_count = user_group.size().reset_index(name='user_weibo_count')
    user_interact_weibo_count = pd.merge(user_interact,user_weibo_count,on = 'uid',how='left')
    user_interact_weibo_count['avg_interact'] =  user_interact_weibo_count['user_interact']/user_interact_weibo_count['user_weibo_count']
    print(user_interact_weibo_count.describe()['avg_interact'])
    print(len(user_interact_weibo_count[user_interact_weibo_count.avg_interact <= 0.2]))
    # user_interact_weibo_count = user_interact_weibo_count.sort_values(by=['avg_interact'], axis=0, ascending=True)
    # sns.catplot(x="avg_interact", kind="count", palette="ch:.25", data=user_interact_weibo_count[user_interact_weibo_count. avg_interact])
    user_0_weibo_count = train_data[train_data.sum_interact == 0].groupby('uid').size().reset_index(name='user_0_weibo_count')

    train_data = pd.merge(train_data,user_interact,on='uid',how='left')
    train_data = pd.merge(train_data,user_weibo_count,on='uid',how='left')
    train_data = pd.merge(train_data,user_0_weibo_count,on='uid',how='left')
    interact_0_user = set(train_data[train_data.user_interact == 0]['uid'])
    print('互动量为0用户数',len(interact_0_user))
    print('互动量为0用户的记录数',len(train_data[train_data.uid.isin(interact_0_user)]))
    weibo_count_300_user = set(train_data[train_data.user_weibo_count > 100]['uid'])
    print('微博数大于300用户', len(weibo_count_300_user))
    weibo_count_300_and_interact_0_user = interact_0_user & weibo_count_300_user
    print('微博数大于300且互动量为0用户',len(weibo_count_300_and_interact_0_user))
    print('微博数大于300且互动量为0记录数',len(train_data[train_data.uid.isin(weibo_count_300_and_interact_0_user)]))
    # sns.catplot(x="user_interact", kind="count", palette="ch:.25", data=user_interact[user_interact.user_interact < 200])
    # sns.catplot(x="user_weibo_count", kind="count", palette="ch:.25", data=user_weibo_count[user_weibo_count.user_weibo_count < 200])
    # interact_0_user = user_interact[user_interact.user_interact == 0]['uid']
    # print('互动量为0用户数',len(interact_0_user))
    # weibo_count_300_user = user_weibo_count[user_weibo_count.user_weibo_count >100]['uid']
    # print('微博数大于300用户',len(weibo_count_300_user))
    weibo_count_300_and_interact_0_user = np.intersect1d(interact_0_user,weibo_count_300_user)
    # print('微博数大于300且互动量为0用户',len(weibo_count_300_and_interact_0_user))
    # print((user_0_weibo_count.describe()))
    # print((user_weibo_count.describe()))
    train_data['weibo_0_percent'] = train_data['user_0_weibo_count']/train_data['user_weibo_count']
    # sns.catplot(x="weibo_0_percent", kind="count", palette="ch:.25", data=train_data)
    train_data.describe()
    plt.show()


def process_low_interact_user(train_data,predict_data):
    user_group = train_data.groupby('uid')
    #总互动量
    user_interact = user_group.sum_interact.sum().reset_index(name='user_interact')
    #总微博数
    user_weibo_count = user_group.size().reset_index(name='user_weibo_count')
    #连接上面两个结果
    user_interact_weibo_count = pd.merge(user_interact, user_weibo_count, on='uid', how='left')
    #平均互动数
    user_interact_weibo_count['avg_interact'] = user_interact_weibo_count['user_interact'] / user_interact_weibo_count[
        'user_weibo_count']
    # print(user_interact_weibo_count.describe()['avg_interact'])
    #低互动用户名单
    low_interact_user_set = set(user_interact_weibo_count[user_interact_weibo_count.avg_interact <= 5]['uid'])#0.16
    print('process 低互动用户名单',len(low_interact_user_set))
    #训练集删去低互动用户
    train_data = train_data[~(train_data.uid.isin(low_interact_user_set))]
    #预测集删去低互动用户
    predict_data = predict_data[~(predict_data.uid.isin(low_interact_user_set))]

    return train_data,predict_data,low_interact_user_set

def print_data_shape(train_data,predict_data):
    print('*'*20)
    print('训练集shape',train_data.shape)
    print('预测集shape', predict_data.shape)
    print('*' * 20)


if __name__ == '__main__':
    nrows = 0
    train_data = DataToMysql.get_handled_train_data(nrows)
    predict_data = DataToMysql.get_handled_predict_data(nrows)
    print_data_shape(train_data, predict_data)

    predict_data = process_new_user(train_data,predict_data)
    train_data,predict_data = process_low_interact_user(train_data,predict_data)
    print_data_shape(train_data, predict_data)
    # get_user_sum_interact(train_data)
