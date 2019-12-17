# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019-07-31

import pandas as pd
import numpy as np
import os, sys, warnings

warnings.filterwarnings('ignore')

formula_lvs = pd.read_csv('C:/Users/pc/OneDrive/PLTTECH/Project/immune_age/Data/rawdata/formula_LVs.csv')

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

path_file = input('Please input the path of sample:')
sample_file = os.listdir('C:/Users/pc/OneDrive/PLTTECH/Project/immune_age/Result/%s' % path_file)

def predict_age(sample_file):
    age_dict = dict()
    for file in sample_file:
        data_file = os.listdir('C:/Users/pc/OneDrive/PLTTECH/Project/immune_age/Result/%s/%s' % (path_file, file))
        new_data = pd.read_csv('C:/Users/pc/OneDrive/PLTTECH/Project/immune_age/Result/%s/%s' % (path_file, file) + '/' + data_file[0])
        lv1, lv2, lv3 = caculate_lv(new_data)
        immune_age = linear_pre(lv1, lv2, lv3)
        age_dict[file] = immune_age
    age_df = pd.DataFrame(age_dict, index=['Age Prediction']).T
    return age_df

age_df = predict_age(sample_file)
age_df = age_df.sort_index()
day_time = input('Please input the day_time:')
age_df.to_csv('C:/Users/pc/Desktop/Age_Prediction_' + day_time + '.csv')





