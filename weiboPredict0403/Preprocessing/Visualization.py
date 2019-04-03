import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
import IOData.DataToMysql as DataToMysql


def visual_total_distribution(data):
    # data = DataToMysql.get_handled_train_data(100)
    print(data)
    sns.catplot(x="level_interact", kind="count", palette="ch:.25", data=data)
    plt.show()
    print('visual_total_distribution')

def analyse_data():
    train_data = DataToMysql.get_handled_train_data(100)
    predict_data = DataToMysql.get_handled_predict_data(100)
    print(train_data.describe())
    print(predict_data.describe())
    print()



if __name__ == '__main__':
    train_data = DataToMysql.get_handled_train_data(100)
    predict_data = DataToMysql.get_handled_predict_data(100)
    # print(train_data.info())
    # print(predict_data.info())
    user_group = train_data.groupby('uid')['']





