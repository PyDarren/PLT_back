# Created by: Chen Da
# Created on: 2019/8/12

library(tidyverse)
library(readxl)
library(utils)
library(readr)
library(readxl)
library(ggplot2)
library(reshape2)
library(plyr)
library(dplyr)
library(RColorBrewer)
# library(Cairo)
library(ggpubr)



#################################################
#### Data preprocess
df <- read_csv('C:/Users/pc/OneDrive/PLTTECH/Project/02_Disease_early_screening/liver_cancer/rawdata/raw_data.csv')
# df <- read_csv('/Users/chenda/OneDrive/PLTTECH/Project/20191205_lung_cancer/rawdata/all.csv')
df$class <- as.factor(df$class)


################################################
#### Boxplot
box_plot_p <- function(df, test_type="p") {
  group_name <- levels(df$class)
  group1_index <- which(df$class == group_name[1])
  group2_index <- which(df$class == group_name[2])
  
  # t test
  pval <- apply(df[, 2:(dim(df)[2]-1)], 2, function(x) t.test(x[group1_index], x[group2_index], alternative = "two.sided")$p.value)
  pval_adjust <- p.adjust(pval, method = "BH")
  pval_cut <- cut(pval, breaks = c(0, 0.001, 0.01, 0.05, 1),
                  labels = c("***", "**", "*", ""))
  
  pval_adjust_cut <- cut(pval_adjust, breaks = c(0, 0.001, 0.01, 0.05, 1),
                         labels = c("***", "**", "*", ""))
  
  
  # Data for plot
  
  ggdf_plot <- melt(df[, -dim(df)[2]], id.vars = "id", variable.name = "Subsets", value.name = "Frequency")
  
  mm <- match(ggdf_plot$id, df$id)
  ggdf_plot$Condition <- df$class[mm]
  
  ggdf_plot <- data.frame(Cluster = as.factor(ggdf_plot$Subsets),
                          Sample_id = as.factor(ggdf_plot$id),
                          Frequency = as.numeric(ggdf_plot$Frequency),
                          Condition = as.factor(ggdf_plot$Condition))
  
  
  # Data 1: Original p-values
  ggdf_plot1 <- ggdf_plot
  
  # Add varibles
  ggdf_plot1$pval <- rep(pval_cut, each = nrow(df))
  ggdf_plot1$maxfrequency <- rep(apply(df[,2:(dim(df)[2]-1)], 2, max), each = nrow(df))
  ggdf_plot1$linex <- rep(c(1:2), length.out = nrow(ggdf_plot1))
  ggdf_plot1$linex[which(ggdf_plot1$pval == "")] <- NA
  
  # Data 2: BH Adjusted p-values
  ggdf_plot2 <- ggdf_plot
  
  # Add variables
  ggdf_plot2$pval <- rep(pval_adjust_cut, each = nrow(df))
  ggdf_plot2$maxfrequency <- ggdf_plot1$maxfrequency
  ggdf_plot2$linex <- rep(c(1:2), length.out = nrow(ggdf_plot2))
  ggdf_plot2$linex[which(ggdf_plot2$pval == "")] <- NA
  
  # plot
  if (test_type == "p") {
    ggplot(ggdf_plot1) +
      geom_boxplot(aes(x = Condition, y = Frequency, color = Condition, fill = Condition),
                   position = position_dodge(), alpha = 0.5, outlier.color = NA) +
      geom_point(aes(x = Condition, y = Frequency, color = Condition),
                 alpha = 0.8, position = position_jitterdodge()) +
      geom_text(aes(x = 1.5, y = maxfrequency, label = pval)) +
      geom_line(aes(x = linex, y = maxfrequency)) +
      theme_bw() +
      facet_wrap(~ Cluster, nrow = 6) +
      labs(title = "Boxplot with original p-values", y = "Frequency (%)") +
      theme(plot.title = element_text(hjust = 0.5)) +
      scale_fill_discrete(labels = c("Healthy", "Unhealthy"))
  }
  else{
    ggplot(ggdf_plot2) +
      geom_boxplot(aes(x = Condition, y = Frequency, color = Condition, fill = Condition),
                   position = position_dodge(), alpha = 0.5, outlier.color = NA) +
      geom_point(aes(x = Condition, y = Frequency, color = Condition),
                 alpha = 0.8, position = position_jitterdodge()) +
      geom_text(aes(x = 1.5, y = maxfrequency, label = pval)) +
      geom_line(aes(x = linex, y = maxfrequency)) +
      theme_bw() +
      facet_wrap(~ Cluster, nrow = 6) +
      labs(title = "Boxplot with BH adjusted p-values", y = "Frequency (%)") +
      theme(plot.title = element_text(hjust = 0.5)) +
      scale_fill_discrete(labels = c("Healthy", "Unhealthy"))
  }
}

box_plot_p(df, test_type = "p")


#####################################################
####                Robust Plot
# iqr <- 0.7413 * IQR(df$`effector CD4+ T cells`)
# iqr <- apply(df[, 2:10], 2, function(x) 0.7413 * IQR(x))
# med <- apply(df[, 2:10], 2, function(x) median(x))
# 
# robust_plot <- function(index) {
#   z <- (df[, index+1] - med[[index]]) / iqr[[index]]
#   z_df <- as.data.frame(z)
#   colnames(z_df) <- colnames(df)[index+1]
#   z_df
# }
# 
# robust_df <- as.data.frame(df$id)
# colnames(robust_df) <- "id"
# for (i in c(1:9)) {
#   robust_df[colnames(df)[i+1]] <- robust_plot(i)
# }
# robust_df$class <- df$class
# 
# box_plot_p(df = robust_df)
# 
# box_plot_p(df = robust_df, test_type = "bh")
