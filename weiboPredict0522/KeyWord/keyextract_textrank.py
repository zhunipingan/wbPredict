#!/usr/bin/python
# coding=utf-8
# 采用TextRank方法提取文本关键词
import sys
import pandas as pd
import jieba.analyse
"""
       TextRank权重：

            1、将待抽取关键词的文本进行分词、去停用词、筛选词性
            2、以固定窗口大小(默认为5，通过span属性调整)，词之间的共现关系，构建图
            3、计算图中节点的PageRank，注意是无向带权图
"""

# 处理标题和摘要，提取关键词
def getKeywords_textrank(data,topK):
    idList,titleList = data['mid'],data['content']
    ids, titles, keys = [], [], []
    for index in range(len(idList)):
        text = '%s。' % (titleList[index]) # 拼接标题和摘要
        jieba.analyse.set_stop_words(r'../LDA/GlobalStopWords.txt') # 加载自定义停用词表
        # print ("\"",titleList[index],"\"" , " 10 Keywords - TextRank :")
        keywords = jieba.analyse.textrank(text, topK=topK, allowPOS=('n','nz','v','vd','vn','l','a','d'))  # TextRank关键词提取，词性筛选
        word_split = " ".join(keywords)
        # print (word_split)
        keys.append(word_split.encode("utf-8"))
        ids.append(idList[index])
        titles.append(titleList[index])

    result = pd.DataFrame({"weibo_id": ids, "title": titles, "key_word": keys},columns=['weibo_id','title','key_word'])
    return result

def main():
    import IOData.DataToMysql as DataToMysql
    from sqlalchemy import create_engine

    data = DataToMysql.get_train_data(100000)
    result = getKeywords_textrank(data,10)
    # result.to_csv("result/keys_TextRank.csv",index=False)
    insert_conn = create_engine(
        'mysql+pymysql://' + 'root' + ':' + '123456' + '@' + 'localhost' + ':' + '3306' + '/' + 'weibosimple' + '?charset=utf8mb4')  # + '?charset=utf8mb4'?charset=utf8mb4
    result.to_sql('train_key_word_textrank', insert_conn, if_exists='replace', index=False)
    print('保存关键词数据完成')

if __name__ == '__main__':
    main()
