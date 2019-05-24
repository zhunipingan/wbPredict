import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
import IOData.DataToMysql as DataToMysql
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体设置-黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
sns.set(font='SimHei')  # 解决Seaborn中文显示问题


#获取不同等级微博占比
def visual_total_distribution(data):
    # data = DataToMysql.get_handled_train_data(100)
    # print(data)
    # sns.catplot(x="level_interact", kind="count", palette="ch:.25", data=data)
    # sns.countplot(x = data['level_interact'])
    sns.factorplot(x='level_interact',data = data,kind = 'count')
    plt.title('微博互动量等级分布图')
    plt.xlabel('互动量等级')
    plt.ylabel('总数量')
    plt.show()

    print('visual_total_distribution完成')

def analyse_data():
    train_data = DataToMysql.get_handled_train_data(100)
    predict_data = DataToMysql.get_handled_predict_data(100)
    print(train_data.describe())
    print(predict_data.describe())
    print()



if __name__ == '__main__':
    train_data = DataToMysql.get_handled_train_data(100)
    predict_data = DataToMysql.get_handled_predict_data(100)
    visual_total_distribution(train_data)
    # print(train_data.info())
    # print(predict_data.info())
    # user_group = train_data.groupby('uid')['']





