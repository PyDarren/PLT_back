# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019/11/5


import pandas as pd
import numpy as np
import os, sys


def linear_pre(lv1, lv2, lv3):
    immune_age = 40.1322 - 0.6259*lv1 + 0.2941*lv2 - 0.0356*lv3
    print(immune_age)
    return immune_age

def caculate_lv(new_data):
    features = new_data.iloc[:, 2:].values
    lv1 = np.sum(np.dot(features, formula_lvs['LV1'].values))
    lv2 = np.sum(np.dot(features, formula_lvs['LV2'].values))
    lv3 = np.sum(np.dot(features, formula_lvs['LV3'].values))
    return lv1, lv2, lv3

def predict_age(sample_file, file_name, path):
    age_dict = dict()
    for file in sample_file:
        data_file = os.listdir(path+'Output/immune_age/%s' % file)
        new_data = pd.read_csv(path+'Output/immune_age/%s' % file+'/'+data_file[0])
        lv1, lv2, lv3 = caculate_lv(new_data)
        immune_age = linear_pre(lv1, lv2, lv3)
        age_dict[file] = immune_age
    age_df = pd.DataFrame(age_dict, index=['Age Prediction']).T
    return age_df


if __name__ == '__main__':
    path = 'C:/Users/pc/OneDrive/PLTTECH/Project/00_immune_age_project/'
    # file_name = input('请输入新数据集名称：')
    file_name = 'test'
    os.mkdir(path+'Output/immune_age')
    raw_df = pd.read_excel(path+'Newdata/' + file_name + '.xlsx')
    name_df = pd.read_excel(path+'Rawdata/亚群对应.xlsx')
    formula_lvs = pd.read_csv(path+'Rawdata/formula_LVs.csv')

    new_names = list(name_df['new_names'].values)
    old_names = list(name_df['old_names'].values)

    df = raw_df[raw_df['subset'].isin(new_names)]
    df = df.set_index('subset')
    df = df.reindex(new_names)

    df['Feature'] = old_names
    df = df.set_index('Feature').T
    df.index.name = 'Feature'
    df = df.T

    df.to_excel(path+'Output/%s_34_subsets.xlsx' % file_name)


    ####################
    ##  preprocessing ##
    ####################
    for info in df.columns[:]:
        # 对每个样本创建一个文件夹
        os.mkdir(path+'Output/immune_age/%s' % info[:-4])
        # 取出样本数据并生成固定格式的数据框
        feature_list = list(df[info])
        feature_list.insert(0, 'x')
        feature_list.insert(0, 'Sample_%s' % info[:-4])
        feature_df = pd.DataFrame(feature_list).T
        feature_df.columns = ['Patient.ID', 'age', 'B cells', 'CD161+CD4+ T cells',
                              'CD161+CD8+ T cells', 'CD161-CD45RA+ Tregs', 'CD161-CD45RA- Tregs',
                              'CD20- CD3- lymphocytes', 'CD28+CD8+ T cells', 'CD4+ T cells',
                              'CD4+CD28+ T cells', 'CD8+ T cells', 'CD85j+CD8+ T cells',
                              'IgD+CD27+ B cells', 'IgD+CD27- B cells', 'IgD-CD27+ B cells',
                              'IgD-CD27- B cells', 'NK cells', 'NKT cells', 'T cells', 'Tregs',
                              'central memory CD4+ T cells', 'central memory CD8+ T cells',
                              'effector CD4+ T cells', 'effector CD8+ T cells',
                              'effector memory CD4+ T cells', 'effector memory CD8+ T cells',
                              'gamma-delta T cells', 'lymphocytes', 'memory B cells', 'monocytes',
                              'naive B cells', 'naive CD4+ T cells', 'naive CD8+ T cells',
                              'transitional B cells', 'viable/singlets']
        feature_df.to_csv(path+'Output/immune_age/%s' % info[:-4] + '/NewData_Sample_%s' % info[:-4] + '.csv', index=False)


    ########################
    #### age prediction ####
    ########################
    sample_file = os.listdir(path+'Output/immune_age')

    age_df = predict_age(sample_file, file_name, path)
    age_df = age_df.sort_index()
    print('-'*80)
    print(age_df)
    age_df.to_excel(path+'Output/01_Age_Prediction_' + file_name + '.xlsx', index=False)


