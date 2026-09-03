# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 09:10:47 2024

@author: wenlou
"""
import os
import pandas as pd
#import numpy as np

## data path
data_path = "P:/3026008.01/Data/"
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"

df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all_w_VAE.pkl"))  

cas_path = "M:/wenlou/3026008.01/CASTOR"

df_ca = pd.read_csv(os.path.join(cas_path, 'Causal_inference_in_audio-visual_export_20240318.csv'), sep = ";", header=0)

df_ca = df_ca.loc[1:] # the first row is the test record

#read subject list for exp 1
sub_id_lst = pd.read_pickle(os.path.join(data_path, "exp1_sub_lst.pkl"))
df_ca = df_ca.loc[df_ca.info_general_subid.isin(sub_id_lst)]


### summary of age 
df_ca['age'] = 2023-df_ca.info_general_year

df_ca.age.describe()

# count    35.000000
# mean     24.342857
# std       4.620561
# min      18.000000
# 25%      21.000000
# 50%      23.000000
# 75%      27.500000
# max      36.000000

### summary of handness

df_ca.info_general_hand.value_counts()
# 1 - right ; 2 - left; 3-both

# 1.0    31
# 2.0     3
# 3.0     1

## summary of gender
df_ca.info_general_gender.value_counts()
# 2- female; 1- male

# 2.0    23
# 1.0    12


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
## counting difference categories
df_cat_cnt = df_A[["sub_id", "ComSourLbl", "confLvl"]].value_counts().reset_index()
# ComSourLbl  confLvl
# Common      3          19526
# Distinct    3          16859
# Common      2           7614
# Distinct    2           4368
# Common      1           2751
# Distinct    1           2642

col_name = df_cat_cnt.columns.to_list()
col_name[-1]="count"
df_cat_cnt.columns = col_name

