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
    raw_confidence = pd.read_excel('C:/Users/pc/OneDrive/PLTTECH/Project/20191103亚群置信区间/Rawdata/confidence_output.xlsx')

    path = 'C:/Users/pc/OneDrive/PLTTECH/Project/20191103亚群置信区间/'
    # file_name = 'test'
    file_name = input("请输入数据集文件名：")
    df = pd.read_excel(path+'Rawdata/'+file_name+'.xlsx')

    names = list(df.iloc[:, 0].values)
    new_confidence_df = raw_confidence.iloc[:, :3]

    for i in range(1, df.shape[1]):
        subset = df.iloc[:, i]
        sample_name = df.columns[i]
        sample_df = func(subset, names, raw_confidence, sample_name)
        new_confidence_df = pd.merge(new_confidence_df, sample_df, on='subset')

    new_confidence_df.to_excel(path+'Output/'+'sample_%s.xlsx'%file_name, index=False)
