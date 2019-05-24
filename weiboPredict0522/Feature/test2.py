import numpy as np
from gensim import corpora, models, similarities
from pprint import pprint
import time

f = open('../data/test2.txt')

stop_list = set('for a of the and to in'.split())
texts = [[word for word in line.strip().lower().split() if word not in stop_list] for line in f]
print ('Text = ')
pprint(texts)


dictionary = corpora.Dictionary(texts)
print(dictionary)

V = len(dictionary) # 字典的长度


# 根据字典，将每行文档都转换为索引的形式
corpus = [dictionary.doc2bow(text) for text in texts]
# 逐行打印
for line in corpus:
       print (line)


corpus_tfidf = models.TfidfModel(corpus)[corpus]

#逐行打印
print ('TF-IDF:')
for c in corpus_tfidf:
    print (c)



print ('\nLDA Model:')
# 设置主题的数目
num_topics = 2
# 训练模型
lda = models.LdaModel(corpus_tfidf, num_topics=num_topics, id2word=dictionary,alpha='auto', eta='auto', minimum_probability=0.001)


doc_topic = [a for a in lda[corpus_tfidf]]
print('Document-Topic:\n')
pprint(doc_topic)


for topic_id in range(num_topics):
    print ('Topic', topic_id)
    pprint(lda.show_topic(topic_id))



similarity = similarities.MatrixSimilarity(lda[corpus_tfidf])
print ('Similarity:')
pprint(list(similarity))