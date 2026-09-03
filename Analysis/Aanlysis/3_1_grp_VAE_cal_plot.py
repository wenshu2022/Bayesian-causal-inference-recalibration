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
from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn.metrics import mean_squared_error, r2_score
sns.set_theme(style="darkgrid")

## data path
data_path = "P:/3026008.01/Data/"
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"

df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all.pkl"))  

######################################################################################################
## VAE calculation
## step 1:
## calculate the mean response location for correspoding A true loc Mean(R_A) as above
meanReportedSoundLocationAllSub = df_A.loc[:, ['sub_id','respPos', 'truePos']].groupby( ['sub_id', 'truePos']).mean()
meanReportedSoundLocationAllSub.reset_index(drop=False, inplace=True)
## rename to reduce confusion
meanReportedSoundLocationAllSub.columns = ['sub_id', 'truePos', 'meanRespPos']
meanReportedSoundLocationAllSub[meanReportedSoundLocationAllSub.sub_id==21]

## step 2:
# concat the meanRespPos from the summary into the auditory table
df_A = pd.merge(df_A, meanReportedSoundLocationAllSub, on=['sub_id','truePos'], how='outer')
df_A.head()

## check if the concat works as intended
df_A.loc[df_A.sub_id==21, ['sub_id','respPos', 'truePos']].groupby( ['sub_id', 'truePos']).mean()

## step 3:
## calculate VAE for each trial : R_A - mean(R_A)
# for ALL trials, subtract the reponse by the corresponding meanRespPos
df_A['VAE'] = df_A['respPos'] - df_A['meanRespPos']


## save data.
#df_A.to_pickle(os.path.join(data_path, "exp1_A_all_w_VAE.pkl"))  
## also save csv
#df_A.to_csv(os.path.join(data_path, "exp1_A_all_w_VAE.csv"), index = False )

df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all_w_VAE.pkl"))  
######################################################################################################

# Section IV :  VAE as a function of audio-visual spatial disparity
## step 1
# Calculate mean and SEM per VA discrepancy in both common source and non-common source for each subject 
mean_sem_data_Allsub = df_A.groupby(['sub_id', 'delta_VA', 'ComSourFlag'])['VAE'].mean().reset_index()
#create a label for plotting
mean_sem_data_Allsub.loc[mean_sem_data_Allsub.ComSourFlag==1,'ComSourLbl'] = 'Common'
mean_sem_data_Allsub.loc[mean_sem_data_Allsub.ComSourFlag==0,'ComSourLbl'] = 'Distinct'
mean_sem_data_Allsub[mean_sem_data_Allsub.sub_id==15]

## step 2 then group average by subject
mean_sem_data_by_sub = mean_sem_data_Allsub.groupby([ 'delta_VA', 'ComSourFlag'])['VAE'].agg(['mean', 'sem']).reset_index()
#create a label for plotting
mean_sem_data_by_sub.loc[mean_sem_data_by_sub.ComSourFlag==1,'ComSourLbl'] = 'Common'
mean_sem_data_by_sub.loc[mean_sem_data_by_sub.ComSourFlag==0,'ComSourLbl'] = 'Distinct'
mean_sem_data_by_sub

## step 3
# Plotting mean with SEM error bars for each category
for cat in ['Distinct', 'Common']:
    category_data = mean_sem_data_by_sub[mean_sem_data_by_sub['ComSourLbl'] == cat]
    plt.errorbar(x=category_data['delta_VA'], y=category_data['mean'], yerr=category_data['sem'],
                 label=cat, fmt='o')

plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
# Set finer x-tick positions and labels
x_positions = mean_sem_data_by_sub['delta_VA'].unique()
plt.xticks(ticks=x_positions)
#plt.yticks(ticks=range(-6,6))
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('VAE (mean)')
#plt.title('Mean VAE with SEM Error Bars')
plt.legend()
plt.savefig(os.path.join(work_path, "output/com_dis_vae.png"))
plt.show()


#### combing the common and distinct together 
# Plotting mean with SEM error bars
#all together
mean_sem_data_all = df_A.groupby(['sub_id', 'delta_VA'])['VAE'].mean().reset_index()
mean_sem_data_all = mean_sem_data_all.groupby([ 'delta_VA'])['VAE'].agg(['mean', 'std']).reset_index()
plt.errorbar(x=mean_sem_data_all['delta_VA'], y=mean_sem_data_all['mean'], yerr=mean_sem_data_all['std'], fmt='o')

plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
# Set finer x-tick positions and labels
x_positions = mean_sem_data_all['delta_VA'].unique()
plt.xticks(ticks=x_positions)
plt.yticks(ticks=range(-6,6))
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('VAE (mean)')
plt.savefig(os.path.join(work_path, "output/tt_vae.png"))
plt.show()


#### PLOT for each confidence level
#conf=2
for conf in np.arange(1, 4):
    df_A_conf = df_A.loc[df_A.confLvl==conf]
    ### repeat the plotting
    ## step 1
    # Calculate mean and SEM per VA discrepancy in both common source and non-common source for each subject 
    mean_sem_data_Allsub = df_A_conf.groupby(['sub_id', 'delta_VA', 'ComSourFlag'])['VAE'].mean().reset_index()
    #create a label for plotting
    mean_sem_data_Allsub.loc[mean_sem_data_Allsub.ComSourFlag==1,'ComSourLbl'] = 'Common'
    mean_sem_data_Allsub.loc[mean_sem_data_Allsub.ComSourFlag==0,'ComSourLbl'] = 'Distinct'
    
    ## step 2 then group average by subject
    mean_sem_data_by_sub = mean_sem_data_Allsub.groupby([ 'delta_VA', 'ComSourFlag'])['VAE'].agg(['mean', 'sem']).reset_index()
    #create a label for plotting
    mean_sem_data_by_sub.loc[mean_sem_data_by_sub.ComSourFlag==1,'ComSourLbl'] = 'Common'
    mean_sem_data_by_sub.loc[mean_sem_data_by_sub.ComSourFlag==0,'ComSourLbl'] = 'Distinct'
    #mean_sem_data_by_sub
    
    ## step 3
    # Plotting mean with SEM error bars for each category
    for cat in ['Distinct', 'Common']:
        category_data = mean_sem_data_by_sub[mean_sem_data_by_sub['ComSourLbl'] == cat]
        plt.errorbar(x=category_data['delta_VA'], y=category_data['mean'], yerr=category_data['sem'],
                     label=cat, fmt='o')
    
    plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
    # Set finer x-tick positions and labels
    x_positions = mean_sem_data_by_sub['delta_VA'].unique()
    plt.xticks(ticks=x_positions)
    plt.yticks(ticks=range(-6,6))
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('VAE (mean)')
    plt.title('Mean VAE with SEM Error Bars (confidence level ' + str (conf) + ")")
    plt.legend()
    plt.savefig(os.path.join(work_path, "output/com_dis_vae_conf" + str (conf)+ ".png"))
    plt.show()
