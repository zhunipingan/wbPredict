import jieba, os
from gensim import corpora, models, similarities
import codecs
import conf
from pprint import pprint
import pandas as pd
import datetime

import tool.printTool as printTool

class Stopwords:
    def __init__(self):
        # 读取global表
        self.stopwords = codecs.open(r'../LDA/GlobalStopWords.txt', 'r', encoding='UTF-8').readlines()
        # 去掉末尾\n符号
        self.stopwords = [word.strip('\n') for word in self.stopwords]

        self.i = 0

        self.word_set = []
    def gene_feature_no_stopwords_list(self,content):
        # # cut函数返回一个python生成器，必须转化为链表才可下一步操作
        word_list = list(jieba.cut(content, cut_all=False))  # false也就是精准模式
        # # 去除停用词
        word_list = [x for x in word_list if x.strip() not in self.stopwords]
        self.word_set.append(word_list)

        if self.i % 5000 == 0:
            print(self.i,datetime.datetime.now())
        self.i = self.i + 1
        return word_list

def do_test_LDA(weibo_data,num_topics = 5):
    stopwords = Stopwords()
    #加载已经保存的模型
    lda_model = models.ldamodel.LdaModel.load(r'D:\graduation project\weiboPredict\lda_model.model')
    #加载保存的词典
    dictionary = corpora.Dictionary.load(r'D:\graduation project\weiboPredict\lda_dict.dict')
    #生成去停用词的分词后博文
    print('开始生成新列 每一句的词list', datetime.datetime.now())
    weibo_data['content_no_stopwords_list'] = weibo_data.content.apply(
        lambda x: stopwords.gene_feature_no_stopwords_list(str(x)))
    print('结束生成新列 每一句的词list', datetime.datetime.now())
    #词典set
    train_set = stopwords.word_set
    #生成词频统计信息
    printTool.print_with_time('开始doc2bow了')
    # 对每一个texts中的词 统计出现的次数， 同时写入到对应的编号中
    corpus = [dictionary.doc2bow(text) for text in train_set]
    print(corpus)
    #构造tf-idf词频信息
    printTool.print_with_time('开始TfidfModel了')
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    print(corpus_tfidf)
    #利用模型生成lda特征
    printTool.print_with_time('开始准备生成dataframe了')
    # print(ldamodel[corpus_tfidf])
    features = []
    for a in lda_model[corpus_tfidf]:
        user_dict = {}
        for i in range(num_topics):
            user_dict['lda_feature' + str(i)] = a[i][1]
        features.append(user_dict)
    lda_dataframe = pd.DataFrame(features)
    #将生成的特征与原数据相连
    printTool.print_with_time('开始连接dataframe了')
    weibo_data = pd.concat([weibo_data, lda_dataframe], axis=1)
    # print(weibo_data)
    print('test lda结束了')
    return weibo_data


def do_train_LDA(weibo_data,num_topics = 5):
    # # 读取global表
    # stopwords = codecs.open(r'../LDA/GlobalStopWords.txt', 'r', encoding='UTF-8').readlines()
    # # 去掉末尾\n符号
    # stopwords = [word.strip('\n') for word in stopwords]
    # # global表合并local表
    # stopwords.extend(conf.LocalStopWords)
    stopwords = Stopwords()
    train_set = []
    # num_topics = 5
    features = []
    print('开始生成新列 每一句的词list',datetime.datetime.now())
    weibo_data['content_no_stopwords_list'] = weibo_data.content.apply(lambda x:stopwords.gene_feature_no_stopwords_list(str(x)))
    print('结束生成新列 每一句的词list',datetime.datetime.now())
    # weibo_data.to_csv(r'D:\graduation project\weiboPredict\ldaresult'+str(datetime.datetime.now().hour)+'.csv')
    # printTool.print_with_time('weibo_data存好了')

    # print('开始筛选停用词了')
    # i = 0
    # for index,row in weibo_data.iterrows():
    #     if(i % 5000 == 0):
    #         print(i,' ',datetime.datetime.now())
    #     i = i + 1
    #     # # # cut函数返回一个python生成器，必须转化为链表才可下一步操作
    #     # word_list = list(jieba.cut(row['content'], cut_all=False))  # false也就是精准模式
    #     # # 去除停用词
    #     # word_list = [x for x in word_list if x.strip() not in stopwords]
    #     train_set.append(row['content_no_stopwords_list'])
    # print('结束筛选停用词了')
    train_set = stopwords.word_set
    printTool.print_with_time('开始构造dictionary了')
    # 统计一共多少中不同字符，同时对每个字符进行编号
    dictionary = corpora.Dictionary(train_set)
    #保存dictionary，在测试集应用lda时使用
    # dictionary.save('lda_dict.dict')
    dictionary.save(r'D:\graduation project\weiboPredict\lda_dict.dict')
    print(dictionary)

    printTool.print_with_time('开始doc2bow了')
    # 对每一个texts中的词 统计出现的次数， 同时写入到对应的编号中
    corpus = [dictionary.doc2bow(text) for text in train_set]
    # print(corpus)
    printTool.print_with_time('开始TfidfModel了')
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    print(corpus_tfidf)

    printTool.print_with_time('开始训练lda了')
    # LDA训练，corpus词向量。在最后查阅id2word，根据词向量训练后得到用户的画像，为词s。在id2word找到词id的实际含义，返回。
    # ldamodel = models.ldamodel.LdaModel(corpus, num_topics=conf.num_topics, id2word=dictionary)
    ldamodel = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary, alpha='auto', eta='auto',
                          minimum_probability=0.001)
    # 模型的保存/ 加载
    # ldamodel.save('lda_model.model')
    ldamodel.save(r'D:\graduation project\weiboPredict\lda_model.model')
    printTool.print_with_time('开始准备生成dataframe了')
    # print(ldamodel[corpus_tfidf])
    for a in ldamodel[corpus_tfidf]:
        user_dict = {}
        for i in range(num_topics):
            user_dict['lda_feature'+str(i)] = a[i][1]
        features.append(user_dict)

    lda_dataframe = pd.DataFrame(features)
    printTool.print_with_time('开始连接dataframe了')
    weibo_data = pd.concat([weibo_data,lda_dataframe],axis = 1)
    # print(weibo_data)
    print('结束了')

    return weibo_data

def do_LDA2(weibo_data):
    # # 读取global表
    # stopwords = codecs.open(r'../LDA/GlobalStopWords.txt', 'r', encoding='UTF-8').readlines()
    # # 去掉末尾\n符号
    # stopwords = [word.strip('\n') for word in stopwords]
    # # global表合并local表
    # stopwords.extend(conf.LocalStopWords)
    stopwords = Stopwords()
    train_set = []
    num_topics = 5
    features = []
    # print('开始生成新列 每一句的词list', datetime.datetime.now())
    # weibo_data['content_no_stopwords_list'] = weibo_data.content.apply(
    #     lambda x: stopwords.gene_feature_no_stopwords_list(str(x)))
    # print('结束生成新列 每一句的词list', datetime.datetime.now())
    # weibo_data.to_csv(r'D:\graduation project\weiboPredict\result' + str(datetime.datetime.now().second) + '.csv')
    # printTool.print_with_time('weibo_data存好了')

    print('开始筛选停用词了')
    i = 0
    for index,row in weibo_data.iterrows():
        if(i % 5000 == 0):
            print(i,' ',datetime.datetime.now())
        i = i + 1
        # print(type(list(row['content_no_stopwords_list'])))
        # # # cut函数返回一个python生成器，必须转化为链表才可下一步操作
        # word_list = list(jieba.cut(row['content'], cut_all=False))  # false也就是精准模式
        # # 去除停用词
        # word_list = [x for x in word_list if x.strip() not in stopwords]
        train_set.append(list(row['content_no_stopwords_list']))
    print('结束筛选停用词了')
    # train_set = stopwords.word_set
    printTool.print_with_time('开始构造dictionary了')
    # 统计一共多少中不同字符，同时对每个字符进行编号
    dictionary = corpora.Dictionary(train_set)
    printTool.print_with_time('开始doc2bow了')
    # 对每一个texts中的词 统计出现的次数， 同时写入到对应的编号中
    corpus = [dictionary.doc2bow(text) for text in train_set]
    printTool.print_with_time('开始TfidfModel了')
    corpus_tfidf = models.TfidfModel(corpus)[corpus]
    printTool.print_with_time('开始训练lda了')
    # LDA训练，corpus词向量。在最后查阅id2word，根据词向量训练后得到用户的画像，为词s。在id2word找到词id的实际含义，返回。
    # ldamodel = models.ldamodel.LdaModel(corpus, num_topics=conf.num_topics, id2word=dictionary)
    ldamodel = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary, alpha='auto', eta='auto',
                               minimum_probability=0.001)
    printTool.print_with_time('开始准备生成dataframe了')
    # print(ldamodel[corpus_tfidf])
    for a in ldamodel[corpus_tfidf]:
        user_dict = {}
        for i in range(num_topics):
            user_dict['lda_feature' + str(i)] = a[i][1]
        features.append(user_dict)

    lda_dataframe = pd.DataFrame(features)
    printTool.print_with_time('开始连接dataframe了')
    weibo_data = pd.concat([weibo_data, lda_dataframe], axis=1)
    # print(weibo_data)
    print('结束了')

    return weibo_data


if __name__ == '__main__':
    data = pd.read_csv(r'D:\graduation project\weiboPredict\result49.csv',nrows=800000)
    do_LDA2(data)



