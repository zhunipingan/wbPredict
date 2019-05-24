#!/usr/bin/python
# coding=utf-8
# 采用TF-IDF方法提取文本关键词
# http://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting
import sys,codecs
import pandas as pd
import numpy as np
import jieba.posseg
import jieba.analyse
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

import IOData.DataToMysql as DataToMysql
from sqlalchemy import create_engine
"""
       TF-IDF权重：
           1、CountVectorizer 构建词频矩阵
           2、TfidfTransformer 构建tfidf权值计算
           3、文本的关键字
           4、对应的tfidf矩阵
"""
# 数据预处理操作：分词，去停用词，词性筛选
def dataPrepos(text, stopkey):
    l = []
    pos = ['n', ]  # 定义选取的词性 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd'
    seg = jieba.posseg.cut(text)  # 分词
    for i in seg:
        if i.word not in stopkey and i.flag in pos:  # 去停用词 + 词性筛选
            l.append(i.word)
    return l

# tf-idf获取文本top10关键词
def getKeywords_tfidf(data,stopkey,topK):
    idList, titleList, abstractList = data['mid'], data['content'], data['content']
    corpus = [] # 将所有文档输出到一个list中，一行就是一个文档
    for index in range(len(idList)):
        text = '%s。%s' % (titleList[index], abstractList[index]) # 拼接标题和摘要
        text = dataPrepos(text,stopkey) # 文本预处理
        text = " ".join(text) # 连接成字符串，空格分隔
        corpus.append(text)

    # 1、构建词频矩阵，将文本中的词语转换成词频矩阵
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus) # 词频矩阵,a[i][j]:表示j词在第i个文本中的词频
    # 2、统计每个词的tf-idf权值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    # 3、获取词袋模型中的关键词
    word = vectorizer.get_feature_names()
    # 4、获取tf-idf矩阵，a[i][j]表示j词在i篇文本中的tf-idf权重
    weight = tfidf.toarray()
    # 5、打印词语权重
    ids, titles, keys = [], [], []
    for i in range(len(weight)):
        ids.append(idList[i])
        titles.append(titleList[i])
        df_word,df_weight = [],[] # 当前文章的所有词汇列表、词汇对应权重列表
        for j in range(len(word)):
            if weight[i][j] > 0:
                # print(word[j], weight[i][j])
                df_word.append(word[j])
                df_weight.append(weight[i][j])
        df_word = pd.DataFrame(df_word,columns=['word'])
        df_weight = pd.DataFrame(df_weight,columns=['weight'])
        word_weight = pd.concat([df_word, df_weight], axis=1) # 拼接词汇列表和权重列表
        word_weight = word_weight.sort_values(by="weight",ascending = False) # 按照权重值降序排列
        keyword = np.array(word_weight['word']) # 选择词汇列并转成数组格式
        topK_new = min(topK,len(word_weight))
        word_split = [keyword[x] for x in range(0,topK_new)] # 抽取前topK个词汇作为关键词
        word_split = " ".join(word_split)
        keys.append(word_split)#.encode("utf-8")

    result = pd.DataFrame({"weibo_id": ids, "title": titles, "key_word": keys},columns=['weibo_id','title','key_word'])
    return result


def main():
    # 读取数据集
    # dataFile = 'data/sample_data.csv'
    # data = pd.read_csv(dataFile)
    data = DataToMysql.get_train_data(100000)
    # 停用词表
    stopkey = [w.strip() for w in codecs.open(r'../LDA/GlobalStopWords.txt','r',encoding='utf-8').readlines()]
    # tf-idf关键词抽取
    result = getKeywords_tfidf(data,stopkey,10)
    #result.to_csv("result/keys_TFIDF.csv",index=False)
    insert_conn = create_engine(
        'mysql+pymysql://' + 'root' + ':' + '123456' + '@' + 'localhost' + ':' + '3306' + '/' + 'weibosimple' + '?charset=utf8mb4')  # + '?charset=utf8mb4'?charset=utf8mb4
    result.to_sql('train_key_word_tfidf', insert_conn, if_exists='replace', index=False)
    print('保存关键词数据完成')

if __name__ == '__main__':
    main()
