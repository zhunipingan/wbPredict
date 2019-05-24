import os
import readdata
import word2vec
import Lstm_Model as lstm_model
import numpy as np
import tensorflow as tf

import time



#文件路径
current_path=os.path.abspath(os.curdir)
data_path="./data"
positive_file_path="./data//pos.txt"
negative_file_path="./data//neg.txt"
embedding_model_path="./data//sgns.weibo.bigram-char" #embedding_64.bin
train_data_path="./data//lstm//training_params.pickle"
log_path="./summary//lstm"

weibo_file_path = "./data//weibo_senti_100k.csv"


#模型超参
class config():
    test_sample_percentage=0.03
    num_labels=2
    embedding_size= 300#0516 修改64
    dropout_keep_prob=0.6
    batch_size=64#0516修改 64
    num_epochs=5#0516修改 80
    max_sentences_length=40
    num_layers = 2
    max_grad_norm=5
    l2_rate=0.0001

#加载数据
# all_sample_lists,all_label_arrays,max_sentences_length=readdata.get_all_data_from_file(positive_file_path,negative_file_path,force_len=40)
all_sample_lists,all_label_arrays,max_sentences_length=readdata.get_weibo_data_from_file2(weibo_file_path,force_len=40)
all_sample_arrays=np.array(word2vec.get_embedding_vector(all_sample_lists,embedding_model_path,False))#返回的是词向量列表
del all_sample_lists
print("sample.shape = {}".format(all_sample_arrays.shape))
print("label.shape = {}".format(all_label_arrays.shape))
trainconfig=config()
trainconfig.max_sentences_length=max_sentences_length
testconfig=config()
testconfig.max_sentences_length=max_sentences_length
testconfig.dropout_keep_prob=1.0

#存储训练参数
params={"num_labels":trainconfig.num_labels,"max_sentences_length":max_sentences_length}
readdata.save(params,train_data_path)

# 打乱样本顺序
np.random.seed(10)
random_index=np.random.permutation(np.arange(len(all_label_arrays))) #这种打乱方式返回的打乱的下标，并不影响原数组
random_sample_arrays=all_sample_arrays[random_index]
del all_sample_arrays
random_label_arrays=all_label_arrays[random_index]
# random_sample_arrays=all_sample_arrays
# del all_sample_arrays
# random_label_arrays=all_label_arrays

#按比例抽取测试样本
num_tests=int(trainconfig.test_sample_percentage*len(all_label_arrays))
del all_label_arrays
test_sample_arrays=random_sample_arrays[:num_tests]
train_sample_arrays=random_sample_arrays[num_tests:]
del random_sample_arrays
train_label_arrays=random_label_arrays[num_tests:]
test_label_arrays=random_label_arrays[:num_tests]
del random_label_arrays
print("Train/Test split: {:d}/{:d}".format(len(train_label_arrays), len(test_label_arrays)))


#开始训练
with tf.Graph().as_default():
    sess=tf.Session() # 创建会话
    with sess.as_default():
        lstm=lstm_model.TextLSTM(config=trainconfig)

        #初始化参数
        train_writer = tf.summary.FileWriter(log_path + '/train', sess.graph)
        test_writer = tf.summary.FileWriter(log_path + '/test')
        step_num=0
        sess.run(tf.global_variables_initializer())
        saver=tf.train.Saver()


        #定义训练函数
        def train_step(x_batch,y_batch):
            feed_dict={
                lstm.input_x:x_batch,
                lstm.input_y:y_batch,
                lstm.dropout_keep_prob:config.dropout_keep_prob,
            }
            merged,loss,accuracy,_=sess.run(
                [lstm.summary_op,lstm.loss,lstm.accuracy,lstm.train_op],
                feed_dict=feed_dict
            )
            return (merged,loss,accuracy)

        #定义测试函数
        def test_step(x_batch,y_batch):
            feed_dict={
                lstm.input_x:x_batch,
                lstm.input_y:y_batch,
                lstm.dropout_keep_prob:testconfig.dropout_keep_prob
            }
            merged,loss, accuracy,_=sess.run(
                [lstm.summary_op,lstm.loss,lstm.accuracy,lstm.train_op],
                feed_dict=feed_dict
            )
            return (merged,loss,accuracy)

        #生成批数据
        batches=readdata.batch_iter(
            list(zip(train_sample_arrays,train_label_arrays)),trainconfig.batch_size,trainconfig.num_epochs)

        #正式开始训练啦
        for batch in batches:
            step_num += 1
            x_batch,y_batch=zip(*batch)
            merged,loss,accuracy=train_step(x_batch,y_batch)
            if step_num % 100 == 0:
                train_writer.add_summary(merged, step_num)
                print("For train_samples: step %d, loss %g, accuracy %g" % (step_num, loss, accuracy),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
                if step_num % 200 ==0:
                    merged,loss,accuracy = test_step(test_sample_arrays, test_label_arrays)
                    test_writer.add_summary(merged, step_num)
                    print("For test_samples: step %d, loss %g, accuracy %g" % (step_num, loss, accuracy),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))


        saver.save(sess,"data/lstm/text_model051802")
    # os.environ[“CUDA_VISIBLE_DEVICES”] = "-1"
    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'