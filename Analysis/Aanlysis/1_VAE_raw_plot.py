# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 14:16:23 2024

@author: wenlou
"""

#import ast 
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


##read in data
df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all.pkl"))  
df_V = pd.read_pickle(os.path.join(data_path, "exp1_V_all.pkl"))  

## first plot
## the relationship between physical and response locations 

## A blocks --- step 1: avergae within subjects
mean_data_by_sub  = df_A.groupby(['sub_id', 'delta_VA', 'truePos'])['respPos'].mean().reset_index()
## step 2: average across subjects
mean_data_all_sub  = mean_data_by_sub.groupby(['delta_VA', 'truePos'])['respPos'].mean().reset_index()
## step3: the avergae og everything
mean_data_all_del  = mean_data_all_sub.groupby(['truePos'])['respPos'].mean().reset_index()
mean_data_all_del.loc[:,'delta_VA_c'] = 'total'
mean_data_all_sub['delta_VA_c']= mean_data_all_sub.delta_VA.astype('str')
mean_data_tt = pd.merge(mean_data_all_sub, mean_data_all_del, on=['delta_VA_c','truePos', 'respPos'], how='outer')

## auditory block
sns.lineplot( data=mean_data_tt.loc[(mean_data_tt.delta_VA>=0) | (mean_data_tt.delta_VA_c=='total'),:], 
             x='truePos', y='respPos',
             hue='delta_VA_c', style = 'delta_VA_c',
             markers=True, dashes=False, 
             palette=['orange', 'y', 'g', 'b','red'])

plt.xlabel('Physical locations ($s_{A,A}$)')
plt.ylabel('Localization responses')
plt.title('For each AV spatial disparity (V - A >= 0)')
plt.legend()
plt.savefig(os.path.join(work_path, "output/AV_raw.png"))
plt.show()

## 
sns.lineplot( data=mean_data_tt.loc[(mean_data_tt.delta_VA<=0) | (mean_data_tt.delta_VA_c=='total'),:], 
             x='truePos', y='respPos',
             hue='delta_VA_c', style = 'delta_VA_c',
             markers=True, dashes=False,
             palette=['b', 'g', 'y', 'orange', 'r'])
plt.xlabel('Physical locations ($s_{A,A}$)')
plt.ylabel('Localization responses')
plt.title('For each AV spatial disparity (V - A <= 0)')
plt.legend()
plt.savefig(os.path.join(work_path, "output/VA_raw.png"))
plt.show()


############################################################################################################
## THE RELATIONSHIP BETWEEN CONGRUENT AND GRAND AVERAGE

#  empirical plots

grand_avg = df_A.groupby(['sub_id', 'truePos'])['respPos'].mean().reset_index()
grand_avg['delta_VA_c'] = 'total'
mean_data_by_sub['delta_VA_c'] = mean_data_by_sub['delta_VA'].astype('str')
mean_cong_tt_by_sub = pd.merge(mean_data_by_sub, grand_avg, \
                            on=['sub_id', 'delta_VA_c','truePos', 'respPos'], how='outer')

mean_cong_tt_by_sub.sort_values(['sub_id', 'delta_VA'], inplace=True)

sns.lineplot( data=mean_cong_tt_by_sub[(mean_cong_tt_by_sub.delta_VA==0)|(mean_cong_tt_by_sub.delta_VA_c=='total')], 
             x='truePos', y='respPos',
             hue='delta_VA_c', style = 'delta_VA_c',
             markers=True, dashes=False,
             palette=[ 'orange', 'red'])
plt.xlabel('Physical locations ($s_{A,A}$)')
plt.ylabel('Response locations')
#plt.title('Response location as a function of physical locations \n for congreunt condition and grand average')
plt.legend(["congruent (empirical)", "grand average (empirical)"])
plt.savefig(os.path.join(work_path, "output/CONG_AVG_RAW.png"))
plt.show()



############################################################################################################
# sub by sub
sns.lineplot( data=mean_cong_tt_by_sub[mean_cong_tt_by_sub.delta_VA==0], 
             x='truePos', y='respPos',
             hue='sub_id', style = 'sub_id',
             markers=True, dashes=False,
             )
plt.xlabel('Physical locations ($s_{A,A}$)')
plt.ylabel('Response locations')
plt.title('Response location as a function of physical locations \n for congreunt condition by subjects')
plt.legend([])
plt.savefig(os.path.join(work_path, "output/CONG_RAW_sub.png"))
plt.show()

sns.lineplot( data=mean_cong_tt_by_sub[mean_cong_tt_by_sub.delta_VA_c=='total'], 
             x='truePos', y='respPos',
             hue='sub_id', style = 'sub_id',
             markers=True, dashes=False,
             )
plt.xlabel('Physical locations ($s_{A,A}$)')
plt.ylabel('Response locations')
plt.title('Response location as a function of physical locations \n for  grand average condition by subjects')
plt.legend([])
plt.savefig(os.path.join(work_path, "output/AVG_RAW_sub.png"))
plt.show()





## visual block############################################################

mean_data_by_subV  = df_V.groupby(['sub_id', 'delta_VA', 'truePos'])['respPos'].mean().reset_index()
## step 2: average across subjects
mean_data_all_subV  = mean_data_by_subV.groupby(['delta_VA', 'truePos'])['respPos'].mean().reset_index()
## step3: the avergae og everything
mean_data_all_delV  = mean_data_all_subV.groupby(['truePos'])['respPos'].mean().reset_index()
mean_data_all_delV.loc[:,'delta_VA_c'] = 'total'
mean_data_all_subV['delta_VA_c']= mean_data_all_subV.delta_VA.astype('str')
mean_data_ttV = pd.merge(mean_data_all_subV, mean_data_all_delV, on=['delta_VA_c','truePos', 'respPos'], how='outer')


sns.lineplot( data=mean_data_ttV.loc[(mean_data_ttV.delta_VA>=0) | (mean_data_ttV.delta_VA_c=='total'),:], 
             x='truePos', y='respPos',
             hue='delta_VA_c', style = 'delta_VA_c',
             markers=True, dashes=False, 
             palette=['orange', 'y', 'g', 'b','red'])

plt.xlabel('Physical locations ($s_{V,V}$)')
plt.ylabel('Localization responses')
plt.title('For each AV spatial disparity (V - A >= 0)')
plt.legend()
plt.savefig(os.path.join(work_path, "output/AV_raw_V.png"))
plt.show()

## 
sns.lineplot( data=mean_data_ttV.loc[(mean_data_ttV.delta_VA<=0) | (mean_data_ttV.delta_VA_c=='total'),:], 
             x='truePos', y='respPos',
             hue='delta_VA_c', style = 'delta_VA_c',
             markers=True, dashes=False,
             palette=['b', 'g', 'y', 'orange', 'r'])
plt.xlabel('Physical locations ($s_{V,V}$)')
plt.ylabel('Localization responses')
plt.title('For each AV spatial disparity (V - A <= 0)')
plt.legend()
plt.savefig(os.path.join(work_path, "output/VA_raw_V.png"))
plt.show()


