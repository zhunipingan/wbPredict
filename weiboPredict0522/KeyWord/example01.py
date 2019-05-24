#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from KeyWord import TextRank4Keyword

tr4w = TextRank4Keyword.TextRank4Keyword()
import IOData.DataToMysql as DataToMysql
from sqlalchemy import create_engine
import pandas as pd
import re
import pymysql

# data = DataToMysql.get_train_data(10)
conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123456',
        db='weibosimple'  # charset='utf8'
    )
cursor = conn.cursor()
select_weibo_sql = "select _id as mid,content from weibo"
reCount = cursor.execute(select_weibo_sql)  # 返回受影响的行数
data = cursor.fetchall()  # 返回数据,返回的是tuple类型
data = pd.DataFrame(list(data),columns=[x[0] for x in cursor.description])
print(data.columns)
#0509修改 去除网址
data['content'] = data.content.apply(lambda x:re.sub('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]','',x))
ids, contents, words, weights = [], [], [],[]
for index,row in data.iterrows():
    tr4w.analyze(text=row['content'], lower=True, window=2)  # py3中必须是utf8编码的bytes或者str对象
    word = []
    weight = []
    for item in tr4w.get_keywords(10, word_min_len=2): #关键词数量
        word.append(item.word)
        weight.append(str(item.weight))
    word_str = ','.join(word)
    weight_str = ','.join(weight)

    ids.append(row['mid'])
    contents.append(row['content'])
    words.append(word_str)
    weights.append(weight_str)
insert_conn = create_engine(
    'mysql+pymysql://' + 'root' + ':' + '123456' + '@' + 'localhost' + ':' + '3306' + '/' + 'weibosimple' + '?charset=utf8mb4')  # + '?charset=utf8mb4'?charset=utf8mb4
result = pd.DataFrame({"weibo_id": ids, "content": contents, "word": words, "weight":weights}, columns=['weibo_id', 'content', 'word','weight'])
# print(result['word'])
result.to_sql('train_key_word_textrank', insert_conn, if_exists='replace', index=False)
print('保存关键词数据完成')