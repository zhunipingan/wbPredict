doc1 = "Sugar is bad to consume. My sister likes to have sugar, but not my father."
doc2 = "My father spends a lot of time driving my sister around to dance practice."
doc3 = "Doctors suggest that driving may cause increased stress and blood pressure."
doc4 = "Sometimes I feel pressure to perform well at school, but my father never seems to drive my sister to do better."
doc5 = "Health experts say that Sugar is not good for your lifestyle."

# 整合文档数据
doc_complete = [doc1, doc2, doc3, doc4, doc5]

# import nltk
# nltk.download()

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

doc_clean = [clean(doc).split() for doc in doc_complete]

import gensim
from gensim import corpora

# 创建语料的词语词典，每个单独的词语都会被赋予一个索引
dictionary = corpora.Dictionary(doc_clean)

# 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]

# 使用 gensim 来创建 LDA 模型对象
Lda = gensim.models.ldamodel.LdaModel

# 在 DT 矩阵上运行和训练 LDA 模型
ldamodel = Lda(doc_term_matrix, num_topics=4, id2word = dictionary, passes=50)

# 输出结果
print(ldamodel.print_topics(num_topics=4, num_words=4))

# import pandas as pd
# import numpy as np
# import datetime
# import os
# print(os.path.join('asasd','./model','1234.txt'))
# data = pd.read_csv('../data/weibo_predict_data.csv')
# print(data['date'].describe())
# print(data.info())
# data.time = data.uid.apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))

# from multiprocessing import Pool
# from multiprocessing import cpu_count
# import gc
#
# processor=cpu_count()-1
# import pandas as pd
#
# user_dict = {}
# user_dataframe = pd.DataFrame(columns=('mid', 'blog_1day_sum_weibo'))
# user_dict['mid'] = 10
# user_dict['blog_1day_sum_weibo'] = 10
# # s = pd.Series({'mid':10 , 'blog_1day_sum_weibo':'10'})
# # user_dict['the_user_data_30day'] = 10
# # user_dict['the_user_data_15day'] = 10
# # user_dict['the_user_data_7day'] = 10
# # user_dict['the_user_data_3day'] = 10
# # user_dict['the_user_data_1day'] = 10
# user_dataframe = user_dataframe.append(user_dict,ignore_index=True)
# print(user_dataframe.info())
#
#
# import pandas as pd
# from numpy.random import randint
# df = pd.DataFrame(columns=('lib', 'qty1', 'qty2'))
#
# s = pd.Series({'lib':1 , 'qty1':randint(-1,1), 'qty2':randint(-1,1)})
# # 这里 Series 必须是 dict-like 类型
# df = df.append(s, ignore_index=True)
# print(df)


