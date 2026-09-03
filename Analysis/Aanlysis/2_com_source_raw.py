# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 10:25:35 2024

@author: wenlou
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy import stats
sns.set_theme(style="darkgrid")

## data path
data_path = "P:/3026008.01/Data/"

# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"

##read in data
df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all.pkl"))  
df_V = pd.read_pickle(os.path.join(data_path, "exp1_V_all.pkl"))  
## for the common source part - combine the a and v blocks
df_all = pd.concat([df_A, df_V])

## % common source as a function of spatial disparity
com_pct_all_by_sub = df_all.groupby(['sub_id', 'delta_VA'])['ComSourFlag', 'confLvl'].mean().reset_index()

## plot
sns.lineplot( data=com_pct_all_by_sub, x='delta_VA', y='ComSourFlag')
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('% common source')
plt.xticks(com_pct_all_by_sub.delta_VA.unique())
plt.savefig(os.path.join(work_path, "output/com_ratio.png"))
plt.show()

### confidence level 
com_pct_all_by_sub_com = df_all.groupby(['sub_id', 'delta_VA', 'ComSourFlag'])['confLvl'].mean().reset_index()
#create a label for plotting
com_pct_all_by_sub_com.loc[com_pct_all_by_sub_com.ComSourFlag==1,'ComSourLbl'] = 'Common'
com_pct_all_by_sub_com.loc[com_pct_all_by_sub_com.ComSourFlag==0,'ComSourLbl'] = 'Distinct'
com_pct_all_by_sub['ComSourLbl'] = 'Total'
# concat the total level 
com_pct_all_by_sub_com = pd.concat([com_pct_all_by_sub_com, com_pct_all_by_sub]).reset_index()


## plot - by common source label 
sns.lineplot( data=com_pct_all_by_sub_com, x='delta_VA', y='confLvl', 
             hue='ComSourLbl', style = 'ComSourLbl',
             markers=True, dashes=False)
plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
plt.axhline(y=1, color='black', linewidth=0.8, linestyle='--')
plt.axhline(y=3, color='black', linewidth=0.8, linestyle='--')
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('Confidence Level')
plt.xticks(com_pct_all_by_sub.delta_VA.unique())
plt.legend(loc = 4)
plt.savefig(os.path.join(work_path, "output/com_confi.png"))
plt.show()


## plot - by common source label - exclude the total
sns.lineplot( data=com_pct_all_by_sub_com.loc[com_pct_all_by_sub_com.ComSourLbl!='Total', :], 
             x='delta_VA', y='confLvl', 
             hue='ComSourLbl', style = 'ComSourLbl',
             markers=True, dashes=False)
plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
plt.axhline(y=1, color='black', linewidth=0.8, linestyle='--')
plt.axhline(y=3, color='black', linewidth=0.8, linestyle='--')
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('Confidence Level')
plt.xticks(com_pct_all_by_sub.delta_VA.unique())
plt.legend(loc = 4)
plt.savefig(os.path.join(work_path, "output/com_confi_no_tt.png"))
plt.show()

