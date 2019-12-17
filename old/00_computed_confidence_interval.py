# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019/11/3


import pandas as pd
import numpy as np


def func(subset, names, raw_confidence, sample_name):
    vals = list(subset.values)
    arrows_95 = list()
    arrows_99 = list()
    for i in range(len(vals)):
        name = names[i]
        reference = raw_confidence[raw_confidence['subset']==name]
        if vals[i] > reference['upper_95'].values[0]:
            arrows_95.append('↑')
        elif vals[i] < reference['low_95'].values[0]:
            arrows_95.append('↓')
        else:
            arrows_95.append(' ')
    for i in range(len(vals)):
        name = names[i]
        reference = raw_confidence[raw_confidence['subset']==name]
        if vals[i] > reference['upper_99'].values[0]:
            arrows_99.append('↑')
        elif vals[i] < reference['low_99'].values[0]:
            arrows_99.append('↓')
        else:
            arrows_99.append(' ')
    sample_df = pd.DataFrame([names, arrows_95, arrows_99]).T
    sample_df.columns = ['subset', 'confidence_95_%s'%sample_name, 'confidence_99_%s'%sample_name]
    return sample_df



if __name__ == '__main__':
    path = 'C:/Users/pc/OneDrive/PLTTECH/Project/00_immune_age_project/'
    raw_confidence = pd.read_excel(path+'Rawdata/confidence_output.xlsx')
    file_name = 'test'
    # file_name = input("请输入数据集文件名：")
    df = pd.read_excel(path+'Newdata/'+file_name+'.xlsx')
    select_subsets_df = pd.read_excel(path+'Rawdata/置信区间选择.xlsx')
    select_subsets = list(select_subsets_df['subset'].values)

    names = list(df.iloc[:, 0].values)
    new_confidence_df = raw_confidence.iloc[:, :3]

    for i in range(1, df.shape[1]):
        subset = df.iloc[:, i]
        sample_name = df.columns[i]
        sample_df = func(subset, names, raw_confidence, sample_name)
        new_confidence_df = pd.merge(new_confidence_df, sample_df, on='subset')

    columns_id = [0, 1]
    columns_id.extend([i for i in range(3, new_confidence_df.shape[1]) if i % 2 != 0])
    final_df = new_confidence_df.iloc[:, columns_id]
    final_df = final_df[final_df['subset'].isin(select_subsets)]
    final_df = pd.merge(select_subsets_df, final_df, on='subset')


    new_confidence_df.to_excel(path+'Output/'+'00_confidence_%s_all.xlsx'%file_name, index=False)
    final_df.to_excel(path+'Output/'+'00_confidence_%s.xlsx'%file_name, index=False)
