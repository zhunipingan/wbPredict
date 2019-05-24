import os
import readdata
import word2vec
import Lstm_Model as lstm_model
import numpy as np
import tensorflow as tf



#文件路径
current_path=os.path.abspath(os.curdir)
test_file_path="./data//test.txt"
embedding_model_path="./data////sgns.weibo.bigram-char"# embedding_64.bin"
train_data_path="./data//lstm//training_params.pickle"


#模型超参
class config():
    test_sample_percentage=0.03
    num_labels=2
    embedding_size=300#0517修改64
    dropout_keep_prob=1
    batch_size= 64 #0517修改64
    num_epochs=80
    max_sentences_length=40
    num_layers=2
    max_grad_norm=5
    l2_rate=0.0001


def get_lstm_result():
    if not os.path.exists(embedding_model_path):
        print("word2vec model is not found")

    if not os.path.exists(train_data_path):
        print("train params is not found")

    params = readdata.loadDict(train_data_path)
    train_length = int(params['max_sentences_length'])



    # test_sample_lists = readdata.get_cleaned_list(test_file_path)
    test_sample_lists_all = readdata.get_mysql_data() #两列 分别时id和内容
    test_sample_lists,max_sentences_length = readdata.padding_sentences(test_sample_lists_all['content'],padding_token='<PADDING>',padding_sentence_length=train_length)
    test_sample_arrays=np.array(word2vec.get_embedding_vector(test_sample_lists,embedding_model_path,False))#原来没有第三个参数
    testconfig=config()
    testconfig.max_sentences_length=max_sentences_length


    sess=tf.InteractiveSession()
    lstm=lstm_model.TextLSTM(config=testconfig)

    saver = tf.train.Saver()
    saver.restore(sess, "./data/lstm/text_model051802")

    #定义测试函数
    def test_step(x_batch):
        feed_dict={
            lstm.input_x:x_batch,
            lstm.dropout_keep_prob:testconfig.dropout_keep_prob
        }
        predictions,scores=sess.run(
            [lstm.predictions,lstm.softmax_result],
            feed_dict=feed_dict
        )
        return (predictions,scores)

    predictions, scores=test_step(test_sample_arrays)
    test_sample_lists_all['is_positive'] = predictions


    sentiment_score_list = [str(i[0])+","+str(i[1]) for i in scores]
    test_sample_lists_all['sentiment_score'] = sentiment_score_list
    # return np.array(predictions) #版本1
    return test_sample_lists_all
    #print("(0->neg & 1->pos)the result is:")
    #print(predictions)
    #print("********************************")
    #print("the scores is:")
    #print(scores)

from visual import show_emtion
from sqlalchemy import create_engine
if __name__ == '__main__':
    prediction = get_lstm_result()
    insert_conn = create_engine(
        'mysql+pymysql://' + 'root' + ':' + '123456' + '@' + 'localhost' + ':' + '3306' + '/' + 'weibosimple' + '?charset=utf8mb4')  # + '?charset=utf8mb4'?charset=utf8mb4
    prediction.to_sql('sentiment_weibo_result051802', insert_conn, if_exists='replace', index=False)
    print('保存训练对比数据完成')
    prediction = prediction['is_positive'].values.tolist()
    show_emtion(prediction)
             