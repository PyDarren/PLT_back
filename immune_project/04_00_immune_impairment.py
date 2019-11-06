# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019/11/6

'''
处理新数据的合并问题
'''

import pandas as pd
import numpy as np
import os


def normalization(df, feature):
    '''
    1、Calculated the mean and s.d. of frequency values between the 10th and 90th percentiles;
    2、Normalize cellular frequencies by subtraction of the mean and division by s.d.
    :param feature:  The feature to normalized.
    :return:
    '''
    f_list = list(df[feature])
    f_list = [i for i in f_list if i != 0]              # NA values are not computed
    quantile_10 = np.quantile(f_list, 0.1)
    quantile_90 = np.quantile(f_list, 0.9)
    nums_to_calcu = [i for i in f_list if i >= quantile_10 and i <= quantile_90]
    f_mean = np.mean(nums_to_calcu)
    f_std = np.std(nums_to_calcu)
    df[feature] = df[feature].apply(lambda x : (x - f_mean) / f_std)


def scaling(df):
    for subset in df.columns[4:]:
        normalization(df, subset)
        print('Cell subset "%s" has finished.' % subset)




if __name__ == '__main__':
    path = 'C:/Users/pc/OneDrive/PLTTECH/Project/00_immune_age_project/'
    # file_name = input("请输入原始数据的名称：")
    file_name = 'impairment_test'
    data_path = path + 'Newdata/%s' % file_name + '.xlsx'
    raw_df = pd.read_csv(path + 'Rawdata/diffusion_original.csv')
    new_df = pd.read_excel(data_path)

    os.makedirs(path+'Output/immune_impairment')
    os.makedirs(path+'Output/immune_impairment/per_sample_data/')
    os.makedirs(path+'Output/immune_impairment/stage2_data/')
    os.makedirs(path+'Output/immune_impairment/final_score/')

    for i in range(new_df.shape[0]):
        sample_id = new_df.iloc[i, :]['subject id']
        sample_df = raw_df.append(new_df.iloc[i, :])
        sample_df = sample_df.fillna(0)

        scaling(sample_df)

        #### Select 18 Cell Subset to build trajectory
        cell_subsets = ['B.cells', 'CD161negCD45RApos.Tregs', 'CD161pos.NK.cells', 'CD28negCD8pos.T.cells',
                        'CD57posCD8pos.T.cells', 'CD57pos.NK.cells', 'effector.CD8pos.T.cells',
                        'effector.memory.CD4pos.T.cells', 'effector.memory.CD8pos.T.cells',
                        'HLADRnegCD38posCD4pos.T.cells', 'naive.CD4pos.T.cells', 'naive.CD8pos.T.cells',
                        'PD1posCD8pos.T.cells', 'T.cells', 'CXCR5+CD4pos.T.cells', 'CXCR5+CD8pos.T.cells',
                        'Th17 CXCR5-CD4pos.T.cells', 'Tregs']

        cell_subsets.extend(['subject id', 'year', 'visit number', 'age'])
        print(cell_subsets)
        new_data = sample_df.loc[:, cell_subsets]

        year_list = [2012, 2013, 2014, 2015, 2019]
        new_data = new_data[new_data['year'].isin(year_list)]

        new_data.to_csv(path+'Output/immune_impairment/per_sample_data/%s.csv' % sample_id,
                         index=False)




