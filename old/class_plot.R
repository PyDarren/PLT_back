# Created by: Chen Da
# Created on: 2019/9/12

library(tidyverse)

predicts <- read.csv('C:/Users/pc/OneDrive/PLTTECH/Project/20191024肝癌预测/Output/prediction.csv')
# predicts_all <- read.csv('C:/Users/pc/OneDrive/PLTTECH/Project/20190910肝癌胃癌分类/Output/肝癌&胃癌VS正常/predicts_all.csv')
# predicts_train <- read.csv('C:/Users/pc/OneDrive/PLTTECH/Project/20190912心血管早筛/Output/predicts_train.csv')

predicts$class <- as.factor(predicts$class)
# predicts_all$class <- as.factor(predicts_all$class)
# predicts_train$class <- as.factor(predicts_train$classID)

colnames(predicts) <- c("X", "id", "class", "pro")
# colnames(predicts_all) <- c("X", "id", "pro", "class" )
# colnames(predicts_train) <- c("id", "pro", "classID", "class" )

ggplot() +
  geom_point(predicts, mapping = aes(x = id, y = pro, color = class), size=3) +
  scale_color_discrete(labels = c('Healthy', 'Unhealthy')) +
  theme_bw() +
  geom_hline(aes(yintercept=0.5), linetype='dashed') +
  theme(axis.text.x = element_text(angle = 90)) +
  xlab('Sample ID') +
  ylab('Predict Probability')


# ggplot() +
#   geom_point(predicts_all, mapping = aes(x = id, y = pro, color = class), size=3) +
#   scale_color_discrete(labels = c('Healthy', 'Unhealthy')) +
#   theme_bw() +
#   geom_hline(aes(yintercept=0.5), linetype='dashed') +
#   theme(axis.text.x = element_text(angle = 90)) +
#   xlab('Sample ID') +
#   ylab('Predict Probability')


# ggplot() +
#   geom_point(predicts_train, mapping = aes(x = id, y = pro, color = class), size=3) +
#   scale_color_discrete(labels = c('NC', 'CHD')) +
#   theme_bw() +
#   geom_hline(aes(yintercept=0.5), linetype='dashed') +
#   theme(axis.text.x = element_text(angle = 90)) +
#   xlab('Sample ID') +
#   ylab('Predict Probability')



#########################################################################
# test_score <- read.csv('C:/Users/pc/OneDrive/PLTTECH/Project/20190910肝癌胃癌分类/Output/肝癌&胃癌VS正常/test_score_distribution.csv')
# 
# ggplot() +
#   #geom_histogram(test_score, mapping = aes(x = accuracy), fill = 'skyblue') +
#   theme_bw() +
#   xlab('Validation Accuracy') +
#   ylab('Frequency') +
#   geom_density(test_score, mapping = aes(x = accuracy), fill = 'blue', alpha = 0.2)