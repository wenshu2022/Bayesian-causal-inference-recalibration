# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:52:27 2024

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

##############################################################################################################
###Localization responses as a function of the localization responses in the previous trial###################

## step 1: create new fields for the look back trials
# make sure the dataframe is sorted temporally
# df_A = df_A.sort_values(by=['sub_id', 'sesNr', 'trialNr'])
# df_A.loc[: ,'back_1_respPos'] = df_A.loc[:,'respPos'].shift(1)
# df_A.loc[df_A.trialNr==1 ,'back_1_respPos'] = np.NaN
# df_A.loc[: ,'back_1_ComSourFlag'] = df_A.loc[:,'ComSourFlag'].shift(1)
# df_A.loc[df_A.trialNr==1 ,'back_1_ComSourFlag'] = np.NaN
# df_A.loc[: ,'back_1_confLvl'] = df_A.loc[:,'confLvl'].shift(1)
# df_A.loc[df_A.trialNr==1 ,'back_1_confLvl'] = np.NaN


# #back 2
# df_A = df_A.sort_values(by=['sub_id', 'sesNr', 'trialNr'])
# df_A.loc[: ,'back_2_respPos'] = df_A.loc[:,'respPos'].shift(2)
# df_A.loc[df_A.trialNr<=2 ,'back_2_respPos'] = np.NaN
# df_A.loc[: ,'back_2_ComSourFlag'] = df_A.loc[:,'ComSourFlag'].shift(2)
# df_A.loc[df_A.trialNr<=2 ,'back_2_ComSourFlag'] = np.NaN
# df_A.loc[: ,'back_2_confLvl'] = df_A.loc[:,'confLvl'].shift(2)
# df_A.loc[df_A.trialNr<=2 ,'back_2_confLvl'] = np.NaN

# df_A.loc[: ,'back_2_delta_VA'] = df_A.loc[:,'delta_VA'].shift(2)
# df_A.loc[df_A.trialNr<=2 ,'back_2_delta_VA'] = np.NaN

# df_A.to_pickle(os.path.join(data_path, "exp1_A_all_w_VAE.pkl"))
# df_A.to_csv(os.path.join(data_path, "exp1_A_all_w_VAE.csv"), index = False)
##############################################################################################################
###Casual decision response as a function of the casual decision response in the previous trial









##############################################################################################################
###Casual confidence response as a function of the casual confidence response in the previous trial
sns.violinplot(data = df_A, x = 'back_1_confLvl', y = 'confLvl')
plt.xlabel('confidence level (back 1 trial)')
plt.ylabel('confidence level (current trial)')
plt.savefig(os.path.join(work_path, 'output/conf_past.png'))
plt.show()


##############################################################################################################
### VAE as a function of spatial disparity in the previous trial
## step 1: create new fields for the look back trials
# make sure the dataframe is sorted temporally
# df_A = df_A.sort_values(by=['sub_id', 'sesNr', 'trialNr'])
# df_A.loc[: ,'back_1_delta_VA'] = df_A.loc[:,'delta_VA'].shift(1)
# df_A.loc[df_A.trialNr==1 ,'back_1_delta_VA'] = np.NaN

# ## save data.
# df_A.to_pickle(os.path.join(data_path, "exp1_A_all_w_VAE.pkl"))  
# ## also save csv
# df_A.to_csv(os.path.join(data_path, "exp1_A_all_w_VAE.csv"), index = False )
#back 1
mean_sem_data_all = df_A.groupby(['sub_id', 'back_1_delta_VA'])['VAE'].mean().reset_index()
mean_sem_data_all = mean_sem_data_all.groupby([ 'back_1_delta_VA'])['VAE'].agg(['mean', 'std']).reset_index()
plt.errorbar(x=mean_sem_data_all['back_1_delta_VA'], y=mean_sem_data_all['mean'], yerr=mean_sem_data_all['std'], fmt='o')

plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
# Set finer x-tick positions and labels
x_positions = mean_sem_data_all['back_1_delta_VA'].unique()
plt.xticks(ticks=x_positions)
plt.yticks(ticks=range(-2,3))
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('VAE (mean)')
plt.title("Back 1 trial")
plt.savefig(os.path.join(work_path, "output/tt_vae_BACK1.png"))
plt.show()

#back 2
mean_sem_data_all = df_A.groupby(['sub_id', 'back_2_delta_VA'])['VAE'].mean().reset_index()
mean_sem_data_all = mean_sem_data_all.groupby([ 'back_2_delta_VA'])['VAE'].agg(['mean', 'std']).reset_index()
plt.errorbar(x=mean_sem_data_all['back_2_delta_VA'], y=mean_sem_data_all['mean'], yerr=mean_sem_data_all['std'], fmt='o')

plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
# Set finer x-tick positions and labels
x_positions = mean_sem_data_all['back_2_delta_VA'].unique()
plt.xticks(ticks=x_positions)
plt.yticks(ticks=range(-2,3))
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('VAE (mean)')
plt.title("Back 2 trial")
plt.savefig(os.path.join(work_path, "output/tt_vae_BACK2.png"))
plt.show()

##############################################################################################################
#relationship between current and previous delta

import scipy.stats
scipy.stats.pearsonr(df_A.delta_VA.loc[~pd.isnull(df_A.back_1_delta_VA)], df_A.back_1_delta_VA[~pd.isnull(df_A.back_1_delta_VA)])
#(-0.017349317069556808, 5.846393410832451e-05)

scipy.stats.pearsonr(df_A.delta_VA.loc[~pd.isnull(df_A.back_2_delta_VA)], df_A.back_2_delta_VA[~pd.isnull(df_A.back_2_delta_VA)])
#(-0.01642810128733097, 0.00014366384169595578)




