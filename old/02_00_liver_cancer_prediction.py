# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019/11/5



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def functionLR(id_data):
    '''
    LR函数
    :param id_data:
    :return:
    '''
    z = intercept + np.dot(coefs, id_data.values[1:-1])
    prob = 1 / (1 + np.exp(-z))
    return prob


def liverCancerPrediction(raw_df, file_name):
    '''
    肝癌预测模型
    :param raw_df:
    :param file_name:
    :return:
    '''
    df = raw_df.loc[:, selected_columns]
    prob_list = list()
    for info in df['Feature'].values:
        prob = functionLR(df[df['Feature'] == info].iloc[0, :])
        prob_list.append(prob)
    df_pro = df.loc[:, ['Feature', 'class']]
    df_pro['prob'] = pd.Series(prob_list)
    return df_pro


if __name__ == "__main__":
    path = 'C:/Users/pc/OneDrive/PLTTECH/Project/00_immune_age_project/'
    # file_name = input("请输入原始数据的名称：")
    file_name = 'model_test'
    data_path = path + 'Newdata/%s' % file_name + '.xlsx'
    df = pd.read_excel(data_path)

    # 模型所用变量
    selected_columns = ['Feature', 'CD161-CD45RA- Tregs', 'naive CD8+ T cells', 'naive CD4+ T cells',
                        'CD4+ T cells', 'central memory CD4+ T cells', 'IgD+CD27+ B cells',
                        'CD20- CD3- lymphocytes', 'class']
    # 模型系数
    coefs = [-0.475978379, -0.280812209, 0.050472817, 0.122804959, 0.154113988, -0.624092087,
             0.479011313]
    intercept = -0.017998764

    plot_df = liverCancerPrediction(df, file_name)
    print('Finished!')

    plot_df.to_excel(path+'Output/02_liver_cancer_pre_%s.xlsx' % file_name, index=False)
