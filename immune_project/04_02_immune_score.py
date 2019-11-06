# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019/11/4



import pandas as pd
import numpy as np
import os,sys

def min_max_trans(num):
    '''
    依据文献，对dpt进行归一化
    '''
    min_ = np.min(dcs['dpt'])
    max_ = np.max(dcs['dpt'])
    return (num - min_) / (max_ - min_)

if __name__ == '__main__':
    raw_path = 'C:/Users/pc/OneDrive/PLTTECH/Project/00_immune_age_project/Output/immune_impairment/'
    path = 'C:/Users/pc/OneDrive/PLTTECH/Project/00_immune_age_project/Output/immune_impairment/stage2_data/'
    file_names = os.listdir(path)
    for info in file_names:
        df = pd.DataFrame()
        dcs = pd.read_csv(path + info).iloc[:, 1:]
        # dcs = dcs.sort_values(by='age', ascending=False)
        dcs['dpt'] = dcs['dpt'].apply(min_max_trans)
        # dcs = dcs.sort_values(by='id')
        new_sample = dcs.iloc[-1, :]
        df = df.append(new_sample)
        df = df.loc[:, ['id', 'age', 'dpt']]
        print(df)
        df.to_excel(raw_path + 'final_score/%s_immune_score.xlsx' % info[:-4],  index=False)

