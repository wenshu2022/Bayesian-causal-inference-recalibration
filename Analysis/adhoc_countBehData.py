# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:20:05 2024

@author: wenlou
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.lines as mlines
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

sns.set_theme(style="white")
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts/"
R_path = "C:/Users/wenlou/Documents/R scripts/output/"
data_path = "P:/3026008.01/Data/"
os.chdir(work_path)


# this script is to count behaviour instances for further plotting



###########################################################################
# count instance for beh data
df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))  
# rename distinct to separate in labels for consistency
# df_A.loc[df_A.ComSourLbl=='Distinct', 'ComSourLbl'] = 'Separate'
# df_A.to_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"), index = False)
# exclude subject for df_V as well.
# df_V = pd.read_csv(os.path.join(data_path, "exp1_V_all.csv"))  
# exclude_sub = 30;
# df_V = df_V[df_V.sub_id!=exclude_sub];
# df_V.to_csv(os.path.join(data_path, "exp1_V_all_exc.csv"), index = False)
df_A.loc[df_A.confLvl==1, 'ConfLbl'] = 'Low'
df_A.loc[df_A.confLvl==2, 'ConfLbl'] = 'Medium'
df_A.loc[df_A.confLvl==3, 'ConfLbl'] = 'High'

#count
count_unity = df_A[['ComSourLbl', 'abs_delta_VA']].value_counts().reset_index()
count_unity.columns = ['ComSourLbl', 'abs_delta_VA', 'count']

count_total = df_A[['abs_delta_VA']].value_counts().reset_index()
count_total.columns = ['abs_delta_VA', 'count_total']

# to calculate the ratio, first merge the total count
count_ci = pd.merge(count_unity, count_total, how = 'outer', on = 'abs_delta_VA')
count_ci['ratio'] = count_ci['count']/count_ci['count_total'] *100

###########################################################################
# for confidence
count_conf = df_A[['ConfLbl', 'abs_delta_VA']].value_counts().reset_index()
count_conf.columns = ['ConfLbl', 'abs_delta_VA', 'count']
count_conf = pd.merge(count_conf, count_total, how = 'outer', on = 'abs_delta_VA')
count_conf['ratio'] = count_conf['count']/count_conf['count_total'] *100
count_conf['ComSourLbl'] = 'Total'

count_conf_ci = df_A[['ConfLbl', 'ComSourLbl', 'abs_delta_VA']].value_counts().reset_index()
count_conf_ci.columns = ['ConfLbl', 'ComSourLbl', 'abs_delta_VA', 'count']
count_conf_ci = pd.merge(count_conf_ci, count_unity, how = 'outer', on = ['abs_delta_VA', 'ComSourLbl'])
count_conf_ci.rename(columns = {'count_x':'count', 'count_y':'count_total'}, inplace = True)
count_conf_ci['ratio'] = count_conf_ci['count']/count_conf_ci['count_total'] *100
count_conf = pd.concat([count_conf_ci, count_conf]).reset_index(drop=True)

## write the count to two csv file - to where the behaviour data is saved (R path)
count_ci.to_csv(os.path.join(R_path, 'beh_count_ci.csv'), index = False)
count_conf.to_csv(os.path.join(R_path, 'beh_count_conf.csv'), index = False)


