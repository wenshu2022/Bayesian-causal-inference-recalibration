# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:50:57 2024

@author: wenlou
"""

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn.metrics import mean_squared_error, r2_score
sns.set_theme(style="darkgrid")

## data path
data_path = "P:/3026008.01/Data/"
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"

df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all_w_VAE.pkl"))  
# df_A.loc[df_A.ComSourFlag==1,'ComSourLbl'] = 'Common'
# df_A.loc[df_A.ComSourFlag==0,'ComSourLbl'] = 'Distinct'

#########note: this is also not correct!!!! because no two-stage average!!!
#######
#plor function

def plot_rec(df_A_rec, filename):

    sns.lineplot(data=df_A_rec, x="delta_VA", y="VAE",color='skyblue')
    plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')

    # Set finer x-tick positions and labels
    x_positions = df_A_rec['delta_VA'].unique()
    plt.xticks(ticks=x_positions)
    #plt.yticks(ticks=yrange)
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('VAE (mean)')
    plt.title('Mean VAE in recalibration trials (95% CI)')
    #plt.legend()
    plt.savefig(filename + '.png')
    plt.show()
    
    hue_order = ["Distinct", "Common"]
    sns.lineplot(data=df_A_rec, x="delta_VA", y="VAE",hue = "ComSourLbl", color='skyblue', hue_order=hue_order)
    plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')

    # Set finer x-tick positions and labels
    x_positions = df_A_rec['delta_VA'].unique()
    plt.xticks(ticks=x_positions)
    #plt.yticks(ticks=yrange)
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('VAE (mean)')
    plt.title('Mean VAE in recalibration trials (95% CI)')
    plt.legend()
    plt.savefig(filename + '_com_sour.png')
    plt.show()
    

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Section VII :  Bias V.S. recalibration
## STEP 1: Select the trials statisfying case 1 and case 2
rec_idx = ((df_A.VPosInAV - df_A.APosInAV < 0) & (df_A.truePos <= df_A.VPosInAV)) | \
         ((df_A.VPosInAV - df_A.APosInAV > 0) & (df_A.truePos >= df_A.VPosInAV))
df_A_rec = df_A.loc[rec_idx, :]
#df_A_rec.shape
#plot_rec(df_A_rec, os.path.join(work_path, 'output/test/bias_rec'), range(-2, 3), 1)
plot_rec(df_A_rec, os.path.join(work_path, 'output/bias_rec'))

## STEP 2: calculate statistics and plot
# sns.lineplot(data=df_A_rec, x="delta_VA", y="VAE",color='skyblue')
# plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
# plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')

# # Set finer x-tick positions and labels
# x_positions = df_A_rec['delta_VA'].unique()
# plt.xticks(ticks=x_positions)
# plt.yticks(ticks=range(-6,6))
# plt.xlabel('Spatial disparity (V - A , deg)')
# plt.ylabel('VAE (mean)')
# plt.title('Mean VAE in recalibration trials (95% CI)')
# #plt.legend()
# plt.savefig(os.path.join(work_path, 'output/bias_rec.png'))
# plt.show()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Section VII :  Bias V.S. recalibration (complimentary)
df_A_rec_comp = df_A.loc[~rec_idx, :]
plot_rec(df_A_rec_comp, os.path.join(work_path, 'output/bias_rec_comp'))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
## case 3 and 4
rec_idx2 = ((df_A.VPosInAV - df_A.APosInAV < 0) & (df_A.truePos <= df_A.APosInAV)) | \
         ((df_A.VPosInAV - df_A.APosInAV > 0) & (df_A.truePos >= df_A.APosInAV))

plot_rec(df_A.loc[rec_idx2, :], os.path.join(work_path, 'output/bias_rec_case3n4'), range(-4, 4))


## opposite of case 3 and 4
plot_rec(df_A.loc[~rec_idx2, :], os.path.join(work_path, 'output/bias_rec_case3n4_op'), range(-1, 1))

sum(~rec_idx2)
















