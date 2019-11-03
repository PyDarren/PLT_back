# Title     : TODO
# Objective : TODO
# Created by: Chen Da
# Created on: 2019/11/3



import pandas as pd
import numpy as np




def getOutliers(subset):
    '''
    获取亚群非异常值和异常值的列表。
    --------------
    subset: 亚群名称
    --------------
    return: (非异常值列表, 异常值列表)
    '''
    subset_vals = sorted(subset.values[1:])
    sub_mean = np.mean(subset_vals)
    sub_std = np.std(subset_vals)
    percentile = np.percentile(subset_vals, (25, 50, 75), interpolation='midpoint')
    Q1 = percentile[0]              # 上四分位数
    Q3 = percentile[2]              # 下四分位数
    IQR = Q3 - Q1                   # 四分位距
    upper_lim = Q3 + 1.5*IQR         # 上限  非异常范围的最大值
    low_lim = Q1 - 1.5*IQR           # 下限  非异常范围的最小值
    low_outliers = sorted([i for i in subset_vals if i < low_lim], reverse=True)
    upper_outliers = sorted([i for i in subset_vals if i > upper_lim])
    no_outliers = list(set(subset_vals).difference(set(low_outliers)))
    no_outliers = list(set(no_outliers).difference(set(upper_outliers)))
    no_outliers = [i for i in subset_vals if i in no_outliers]
    R_range = np.max(subset_vals) - np.min(subset_vals)
    low_index = 0
    while low_index < len(low_outliers):
        val = low_outliers[low_index]
        D_range = subset_vals[subset_vals.index(val)+1] - val
        if D_range / R_range < 1/3:
            no_outliers.append(val)
            low_index += 1
        else:
            break
    upper_index = 0
    while upper_index < len(upper_outliers):
        val = upper_outliers[upper_index]
        D_range = val - subset_vals[subset_vals.index(val)-1]
        if D_range / R_range < 1/3:
            no_outliers.append(val)
            upper_index += 1
        else:
            break
    outliers = list(set(subset_vals).difference(set(no_outliers)))
    no_outliers = sorted(no_outliers)
    print('异常值为: %s' % outliers)
    print('非异常值为: %s' % no_outliers)
    return no_outliers, outliers



def confidenceInterval(subset):
    '''
    非参数法计算95%和99%水平上的置信区间
    :param subset:
    :return:
    '''
    no_outliers = sorted(getOutliers(subset)[0])
    percentile = np.percentile(no_outliers, (0.5, 2.5, 97.5, 99.5), interpolation='midpoint')
    confidence_95 = [percentile[1], percentile[2]]
    confidence_99 = [percentile[0], percentile[3]]
    print('百分之95的置信区间为：%s' % confidence_95)
    print('百分之99的置信区间为：%s' % confidence_99)
    return confidence_95, confidence_99



if __name__ == '__main__':
    path = 'C:/Users/pc/OneDrive/PLTTECH/Project/20191103亚群置信区间/'
    # file_name = 'test'
    file_name = input("请输入数据集文件名：")
    df = pd.read_excel(path+'Rawdata/'+file_name+'.xlsx')

    subset_name = list()
    confidence_95 = list()
    confidence_99 = list()
    low_95 = list()
    upper_95 = list()
    low_99 = list()
    upper_99 = list()

    for i in range(df.shape[0]):
        subset_name.append(df['subset'].values[i])
        subset = df.iloc[i, :]
        confidence_95.append(str(round(confidenceInterval(subset)[0][0], 2))+' -- '
                             + str(round(confidenceInterval(subset)[0][1], 2)))
        confidence_99.append(str(round(confidenceInterval(subset)[1][0], 2))+' -- '
                             + str(round(confidenceInterval(subset)[1][1], 2)))
        low_95.append(confidenceInterval(subset)[0][0])
        upper_95.append(confidenceInterval(subset)[0][1])
        low_99.append(confidenceInterval(subset)[1][0])
        upper_99.append(confidenceInterval(subset)[1][1])

    final_df = pd.DataFrame([subset_name, confidence_95, confidence_99, low_95, upper_95, low_99, upper_99]).T
    final_df.columns = ['subset', 'confidence_95', 'confidence_99', 'low_95', 'upper_95', 'low_99', 'upper_99']

    final_df.to_excel(path+'Output/'+'confidence_output.xlsx', index=False)

