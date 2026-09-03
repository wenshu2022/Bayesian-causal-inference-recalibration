# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:20:05 2024

@author: wenlou
"""

import ast 
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
# df_A.to_pickle(os.path.join(data_path, "exp1_A_all_w_VAE.pkl"))  
# ## also save csv
# df_A.to_csv(os.path.join(data_path, "exp1_A_all_w_VAE.csv"), index = False )

#read subject list 
sub_id_lst = pd.read_pickle(os.path.join(data_path, "exp1_sub_lst.pkl"))

#sub_id = 1
######################################################################################################
# Section IV :  VAE as a function of audio-visual spatial disparity
for sub_id in sub_id_lst:

    ## select dataframe by sub
    df_A_sub = df_A.loc[df_A.sub_id == sub_id]

    ## PLOT 1 - com_ratio
    sns.lineplot( data=df_A_sub, x='delta_VA', y='ComSourFlag')
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('% common source')
    plt.xticks(df_A_sub.delta_VA.unique())
    plt.title('Subject ' + str(sub_id))
    plt.savefig(os.path.join(work_path, "output/by_sub/sub_" + str(sub_id) + "_com_ratio.png"))
    plt.show()


    ## PLOT 2 - confidence level
    hue_order = ["Distinct", "Common"]
    sns.lineplot( data=df_A_sub, x='delta_VA', y='confLvl', hue = "ComSourLbl", hue_order=hue_order, style = 'ComSourLbl',
                markers=True, dashes=False)
    plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
    plt.axhline(y=1, color='black', linewidth=0.8, linestyle='--')
    plt.axhline(y=3, color='black', linewidth=0.8, linestyle='--')
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('Confidence Level')
    plt.xticks(df_A_sub.delta_VA.unique())
    plt.legend()
    plt.title("Subject " + str(sub_id))
    plt.savefig(os.path.join(work_path, "output/by_sub/sub_" + str(sub_id) + "_com_confi.png"))
    plt.show()
    
    ##plot 3 - spatial localization
    #AV
    sns.lineplot( data=df_A_sub.loc[(df_A_sub.delta_VA>=0),:],  x='truePos', y='respPos',  
                 hue='delta_VA', style = 'delta_VA',
                markers=True, dashes=False,  ci=None,
                palette=['orange', 'y', 'g', 'b'])
    plt.xlabel('Physical locations ($s_{A,A}$)')
    plt.ylabel('Localization responses')
    plt.title('For each AV spatial disparity (V - A >= 0) - Sub ' + str(sub_id))
    plt.legend()
    plt.savefig(os.path.join(work_path, "output/by_sub/sub_" + str(sub_id) + "_AV_raw.png"))
    plt.show()
    #VA
    sns.lineplot( data=df_A_sub.loc[(df_A_sub.delta_VA<=0),:],  x='truePos', y='respPos',  
                 hue='delta_VA', style = 'delta_VA',
                markers=True, dashes=False, ci= None,
                palette=['b', 'g', 'y', 'orange'])
    plt.xlabel('Physical locations ($s_{A,A}$)')
    plt.ylabel('Localization responses')
    plt.title('For each AV spatial disparity (V - A <= 0) - Sub ' + str(sub_id))
    plt.legend()
    plt.savefig(os.path.join(work_path, "output/by_sub/sub_" + str(sub_id) + "_VA_raw.png"))
    plt.show()

    ## plot 4 - VAE 
    sns.lineplot( data=df_A_sub,  x='delta_VA', y='VAE',  
                markers=True, dashes=False)
    plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
    plt.xticks(df_A_sub.delta_VA.unique())
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('VAE (mean)')
    plt.title('Subject ' + str(sub_id))
    plt.savefig(os.path.join(work_path, "output/by_sub/sub_" + str(sub_id) + "_VAE.png"))
    plt.show()


######################################################################################################
# additional :  
for sub_id in sub_id_lst:

    ## select dataframe by sub
    df_A_sub = df_A.loc[df_A.sub_id == sub_id]

    ## PLOT 1 - VAE as a function of audio-visual spatial disparity for both common and distinct sources
    hue_order = ["Distinct", "Common"]
    sns.lineplot( data=df_A_sub, x='delta_VA', y='VAE', hue = "ComSourLbl", hue_order=hue_order, style = 'ComSourLbl',
                markers=True, dashes=False)

    plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
    # Set finer x-tick positions and labels
    x_positions = df_A['delta_VA'].unique()
    plt.xticks(ticks=x_positions)
    #plt.yticks(ticks=range(-6,6))
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('VAE (mean)')
    plt.legend()
    plt.title('Subject ' + str(sub_id) + ' - com v.s. dist')
    plt.savefig(os.path.join(work_path, "output/by_sub/sub_" + str(sub_id) + "_VAE_com_dis.png"))
    plt.show()

    ## recalibration plot
    rec_idx = ((df_A_sub.VPosInAV - df_A_sub.APosInAV < 0) & (df_A_sub.truePos <= df_A_sub.VPosInAV)) | \
             ((df_A_sub.VPosInAV - df_A_sub.APosInAV > 0) & (df_A_sub.truePos >= df_A_sub.VPosInAV))
    df_A_rec = df_A_sub.loc[rec_idx, :]
    
    sns.lineplot( data=df_A_rec, x='delta_VA', y='VAE', hue = "ComSourLbl", hue_order=hue_order, style = 'ComSourLbl',
                markers=True, dashes=False)

    plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
    # Set finer x-tick positions and labels
    plt.xticks(ticks=x_positions)
    #plt.yticks(ticks=range(-6,6))
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('VAE (mean)')
    plt.legend()
    plt.title('Subject ' + str(sub_id) + ' - recal cases')
    plt.savefig(os.path.join(work_path, "output/by_sub/sub_" + str(sub_id) + "_VAE_com_dis_rec.png"))
    plt.show()
    
    df_A_rec_op = df_A_sub.loc[~rec_idx, :]
    sns.lineplot( data=df_A_rec_op, x='delta_VA', y='VAE', hue = "ComSourLbl", hue_order=hue_order, style = 'ComSourLbl',
                markers=True, dashes=False)

    plt.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
    # Set finer x-tick positions and labels
    plt.xticks(ticks=x_positions)
    #plt.yticks(ticks=range(-6,6))
    plt.xlabel('Spatial disparity (V - A , deg)')
    plt.ylabel('VAE (mean)')
    plt.legend()
    plt.title('Subject ' + str(sub_id) + ' - non-recal cases')
    plt.savefig(os.path.join(work_path, "output/by_sub/sub_" + str(sub_id) + "_VAE_com_dis_rec_op.png"))
    plt.show()
