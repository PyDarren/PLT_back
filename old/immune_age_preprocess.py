# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019-07-31

import pandas as pd
import numpy as np
import os, sys, warnings

warnings.filterwarnings('ignore')

path_file = input('Please input the path file name:')
file_name = input("Please input the name of data file:")
raw_data = 'C:/Users/pc/OneDrive/PLTTECH/Project/immune_age/Data/rawdata/%s.csv' % file_name

df = pd.read_csv(raw_data)

for info in df.columns[1:]:
    # 对每个样本创建一个文件夹
    os.mkdir('C:/Users/pc/OneDrive/PLTTECH/Project/immune_age/Result/%s/%s' % (path_file, info[:]))
    #取出样本数据并生成固定格式的数据框
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
    feature_df.to_csv('C:/Users/pc/OneDrive/PLTTECH/Project/immune_age/Result/%s/%s'
                      % (path_file, info[:]) + '/NewData_Sample_%s' % info[:] + '.csv', index=False)