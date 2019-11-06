# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019/11/5


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# LR函数
def functionLR(id_data):
    z = intercept + np.dot(coefs, id_data.values[1:-1])
    prob = 1 / (1 + np.exp(-z))
    return prob

# 肝癌预测
def lungCancerPrediction(raw_df, file_name):
    df = raw_df.loc[:, selected_columns]
    prob_list = list()
    for info in df['Feature'].values:
        prob = functionLR(df[df['Feature'] == info].iloc[0, :])
        prob_list.append(prob)
    df_pro = df.loc[:, ['Feature', 'class']]
    df_pro['prob'] = pd.Series(prob_list)
    return df_pro


if __name__ == '__main__':
    path = 'C:/Users/pc/OneDrive/PLTTECH/Project/00_immune_age_project/'
    # file_name = input("请输入原始数据的名称：")
    file_name = 'model_test'
    data_path = path + 'Newdata/%s' % file_name + '.xlsx'
    df = pd.read_excel(data_path)

    # 模型所用变量
    selected_columns = ['Feature',
                        'CD85j+CD8+ T cells',
                        'CD20- CD3- lymphocytes',
                        'monocytes',
                        'T cells',
                        'CD28+CD8+ T cells',
                        'lymphocytes',
                        'B cells',
                        'class']
    # 模型系数
    coefs = [0.3336963252086717,
             -0.009967495181819792,
             0.1359226803758734,
             -0.1125818108473672,
             0.04455083303212085,
             -0.05501862244784657,
             0.08889617447585611]
    intercept = 0.0007974303412539442

    plot_df = lungCancerPrediction(df, file_name)
    print('Finished!')

    plot_df.to_excel(path+'Output/03_lung_cancer_pre_%s.xlsx' % file_name, index=False)