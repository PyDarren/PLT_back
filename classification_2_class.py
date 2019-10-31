# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import random, warnings
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from collections import Counter

warnings.filterwarnings('ignore')
plt.style.use('seaborn-colorblind')



def split_func(data_frame, size=0.9):
    """
    Split the data into two data set
    :param data_frame: the name of input data
    :param size : the size of train data
    :return: train_data, test_data
    """
    data_frame = pd.DataFrame(data_frame.values,
                              index=[i for i in range(data_frame.values.shape[0])],
                              columns=data_frame.columns)
    healthy_data = data_frame[data_frame["class"] == 0]
    unhealthy_data = data_frame[data_frame["class"] == 1]
    healthy_index = list(healthy_data.index)
    unhealthy_index = list(unhealthy_data.index)
    healthy_train_data_index = random.sample(healthy_index, int(size * len(healthy_index)))
    unhealthy_train_data_index = random.sample(unhealthy_index, int(size * len(unhealthy_index)))
    healthy_test_data_index = list(set(healthy_index).difference(set(healthy_train_data_index)))
    unhealthy_test_data_index = list(set(unhealthy_index).difference(set(unhealthy_train_data_index)))
    train_index = list(set(healthy_train_data_index).union(set(unhealthy_train_data_index)))
    test_index = list(set(healthy_test_data_index).union(set(unhealthy_test_data_index)))
    train = data_frame.iloc[train_index, :]
    test = data_frame.iloc[test_index, :]
    return train, test


def balance_train(data_frame, more_label=0, less_label=1):
    '''
    Balance number of positive and negative cases in data_frame
    :param data_frame:
    :return:
    '''
    more_class = data_frame[data_frame['class'] == more_label]
    less_class  = data_frame[data_frame['class'] == less_label]
    num = len(more_class) - len(less_class)
    for i in range(num):
        less_index = list(less_class.index)
        index_choose  = random.sample(less_index, 1)[0]
        more_class = more_class.append(less_class.loc[index_choose])
    more_class = more_class.append(less_class)
    data_frame = pd.DataFrame(more_class.values, index=[i for i in range(len(more_class))],
                              columns=more_class.columns)
    return data_frame



def lr_regression(df, penalty='l1', C=1):
    train_df_raw, test_df = split_func(df)
    train_df = balance_train(train_df_raw)
    # stdc = StandardScaler()
    # x_train = stdc.fit_transform(train_df.iloc[:, 1:-1])
    # x_test = stdc.transform(test_df.iloc[:, 1:-1])
    x_train = train_df.iloc[:, 1:-1]
    x_test = test_df.iloc[:, 1:-1]
    lr = LogisticRegression(penalty=penalty, C=C)
    lr.fit(x_train, train_df['class'].values.astype('int'))
    # print(lr.coef_)
    train_score = lr.score(x_train, train_df['class'].values.astype('int'))
    test_score = lr.score(x_test, test_df['class'].values.astype('int'))
    print('Train score is %s' % train_score)
    print('Test score is %s' % test_score)
    return train_score, test_score, lr.coef_, lr.intercept_




def feature_select(df, features_num=52):
    '''
    Repeat modeling to select the feature that appears most frequently
    :param data: model_data
    :param features_num: Number of features intended to be selected
    :return: The index of the selected features
    '''
    coefs_dict = dict()
    intercept_dict = dict()
    score_train_dict = dict()
    score_test_dict = dict()
    all_test_score = dict()
    feature_dict = dict()
    feature_list = list()
    for i in range(5000):
        train_score, test_score, coefs, intercept = lr_regression(df)
        all_test_score[i] = test_score
        if test_score >= 0.7:
            coefs_dict[i] = coefs
            intercept_dict[i] = intercept
            score_train_dict[i] = train_score
            score_test_dict[i] = test_score
            coef_list = list(coefs[0, :])
            select_feature_index = [coef_list.index(i) for i in coef_list if i != 0]
            feature_dict[i] = select_feature_index
            feature_list.extend(select_feature_index)
        else:
            continue
        print("Model %s has finished." % i)
        print('*' * 30)
    feature_counter = Counter(feature_list)
    print(feature_counter)
    features_frequency = sorted(feature_counter.items(), key=lambda item: item[1], reverse=True)[:features_num]
    features_index = [i[0] for i in features_frequency]
    return features_index, all_test_score, feature_counter


def coef_caculate(data):
    coefs_dict = dict()
    intercept_list = list()
    all_train_score = dict()
    all_test_score = dict()
    for i in range(5000):
        train_score, test_score, coefs, intercept = lr_regression(data, penalty='l2')
        all_train_score[i] = train_score
        all_test_score[i] = test_score
        if test_score >= 0.75:
            coefs_dict[i] = coefs
            intercept_list.append(intercept)
        else:
            continue
        print("Model %s has finished." % i)
        print('*' * 30)
    coef_df = pd.DataFrame()
    for i in coefs_dict.keys():
        df_i = pd.DataFrame(coefs_dict[i][0, :]).T
        coef_df = coef_df.append(df_i)
    coef_final = list(np.mean(coef_df).values)
    intercept_final = np.mean(intercept_list)
    test_score_df = pd.DataFrame(all_test_score, index=['accuracy'])
    plt.hist(test_score_df)
    plt.show()
    return coef_final, intercept_final, test_score_df


def final_model(df):
    predict_score = list()
    for info in range(df.shape[0]):
        new_data = df.iloc[info, :].values[1:-1]
        z = np.dot(new_data, coef_final) + intercept_final
        y = 1 / (1 + np.exp(-z))
        predict_score.append(y)
    predict_df = pd.DataFrame(predict_score, columns=['pro'])
    df.index = [i for i in range(df.shape[0])]
    predict_df['id'] = df['id']
    predict_df['class'] = df['class']
    predict_df = predict_df.reindex(columns=['id', 'pro', 'class'])
    positive = predict_df[predict_df['class'] == 1]
    negtive = predict_df[predict_df['class'] == 0]
    plt.scatter(x=positive['id'], y=positive['pro'], color='red')
    plt.scatter(x=negtive['id'], y=negtive['pro'], color='blue')
    plt.axhline(y=0.5, color='grey', linestyle='--', alpha=0.6)
    plt.xticks(rotation=90)
    plt.grid()
    plt.show()
    return predict_df



if __name__ == '__main__':
    path = input('请输入项目路径:')
    df_name = input('请输入数据文件名:')
    df = pd.read_excel(path + 'Rawdata/' + df_name + '.xlsx')


    # 亚群选择
    features_index, all_test_score, feature_counter = feature_select(df)
    feature_all = list(df.columns[1:-1])
    print(sorted(feature_counter.items(), key=lambda x:x[1], reverse=True))
    select_feature_num = input('请输入所选特征个数:')
    select_feature_name = [feature_all[i] for i in features_index[:int(select_feature_num)]]
    print(select_feature_name)

    select_feature_name.insert(0, 'id')
    select_feature_name.append('class')
    select_df = df.loc[:, select_feature_name]
    select_train_df_raw, select_test_df = split_func(select_df)
    select_train_df = balance_train(select_train_df_raw)


    # 训练模型
    coef_final, intercept_final, test_score = coef_caculate(data=select_train_df)

    predicts = final_model(df=select_test_df)
    predicts_all = final_model(df=select_df)


    # 对流程中的数据进行保存
    test_score.T.to_csv(path + 'Output/test_score_distribution.csv')
    predicts.to_csv(path + 'Output/predicts.csv')
    predicts_all.to_csv(path + 'Output/predicts_all.csv')

    coef_df = pd.DataFrame(select_feature_name[1:-1], columns=['Subsets'])
    coef_df['coefs'] = coef_final
    coef_df.to_csv(path + 'Output/coef_df.csv')

    intercept_list = list()
    intercept_list.append(intercept_final)
    pd.DataFrame(intercept_list, columns=['intercept']).to_csv(path + 'Output/intercept_df.csv')

    select_df.columns = select_feature_name
    select_df.to_csv(path + 'Output/select_df.csv', index=False)

    select_test_df.to_csv(path + 'Output/select_test.csv', index=False)
    select_train_df_raw.to_csv(path + 'Output/select_train.csv', index=False)

