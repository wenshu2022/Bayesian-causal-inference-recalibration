# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 11:23:45 2024

@author: wenlou
"""
# this script create A and D in figure 2
import pandas as pd
import numpy as np
import os
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts/"
pred_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
R_path = "C:/Users/wenlou/Documents/R scripts/output"
os.chdir(work_path)
from help_function import *

#read subject list     
sub_id_lst = read_sub_lst()

################
#define model id
m_id = 70

def agg_pred_by_sub2(sub_id, m_id, flip):
    df_pred = pd.read_csv(os.path.join(pred_path, 'm' + str(m_id) ,'pred_sub_' + str(sub_id) + '.csv'))   
    #select the auditory block
    df_pred = df_pred.loc[df_pred.tr_f==1, :]
    df_pred['delta_VA'] = df_pred['s_v'] - df_pred['s_a']
    df_pred.loc[df_pred.R_pc==1, 'ComSourLbl'] = 'Common'
    df_pred.loc[df_pred.R_pc==2, 'ComSourLbl'] = 'Separate'

    #baseline
    meanReportedSoundLocationAllSub = df_pred.loc[:, ['R_s', 's_uni']].groupby( 's_uni').mean()
    meanReportedSoundLocationAllSub.reset_index(drop=False, inplace=True)
    ## rename to reduce confusion
    meanReportedSoundLocationAllSub.columns = [ 's_uni', 'meanRespPos']
    ## step 2:
    # concat the meanRespPos from the summary into the auditory table
    df_pred = pd.merge(df_pred, meanReportedSoundLocationAllSub, on=['s_uni'], how='outer')
    df_pred.head()

    ## step 3:
    ## calculate VAE for each trial : R_A - mean(R_A)
    # for ALL trials, subtract the reponse by the corresponding meanRespPos
    df_pred['VAE'] = df_pred['R_s'] - df_pred['meanRespPos']
    if flip:
        mask = df_pred['delta_VA'] < 0
        df_pred.loc[mask, 'VAE'] = -df_pred.loc[mask, 'VAE']
        df_pred['delta_VA'] = df_pred['delta_VA'].abs()
    
    ### stat level data
    custom_agg = {
        'VAE': [ 'mean'],
        'ComSourLbl': [ 'count'] 
    }
    ## group by common source label and delta_VA
    mean_data_sub = df_pred.groupby(['ComSourLbl', 'delta_VA']).agg(custom_agg).reset_index()
    mean_data_sub.columns = ['ComSourLbl', 'delta_VA', 'rec_mean', 'count']
    
    ## apart from the common/separate, we also compute the "Total" category
    mean_data_t = df_pred.groupby('delta_VA').agg(custom_agg).reset_index()
    mean_data_t.columns = ['delta_VA', 'rec_mean', 'count_total']
    mean_data_t['ComSourLbl'] = "Total"
    
    # concat the two stat
    mean_data_sub = pd.concat([mean_data_sub, mean_data_t[['ComSourLbl','delta_VA', 'rec_mean']]], ignore_index=True)
    mean_data_sub = pd.merge(mean_data_sub, mean_data_t[['delta_VA', 'count_total']], how = 'outer', on = 'delta_VA').reset_index(drop=True)
    
    mean_data_sub['sub_id']= sub_id
    mean_data_sub['m_id']= m_id
    return mean_data_sub
########################
#####data prepare ######
##process prediction data 
# two-step average
temp_list = []
for sub_id in sub_id_lst:
    # 1 - average within subjects
    sub_data = agg_pred_by_sub2(sub_id, m_id, 1)
    temp_list.append(sub_data)
df_all_flipped = pd.concat(temp_list, ignore_index=True)
# 2 - mean and sem across subjects
custom_agg = {
    'rec_mean': [ 'mean', 'sem'],
    'count': [ 'sum'],
    'count_total':['sum']
}
df_pred_avg = df_all_flipped[['m_id', 'ComSourLbl', 'delta_VA', 'rec_mean', 'count', 'count_total']].groupby(['m_id', 'ComSourLbl', 'delta_VA']).agg(custom_agg).reset_index()
df_pred_avg.columns = ['m_id', 'ComSourLbl', 'delta_VA', 'rec_mean', 'rec_sem',  'count', 'count_total']
df_pred_avg['ratio'] = df_pred_avg['count']/df_pred_avg['count_total']*100


#########################
##Plotting 
hue_order = [ "Total", "Separate", "Common"]
color_order = ['black', 'blue', 'red']

# figure 1B - Predicted recalibration with cnt 
fig, axs = plt.subplots(figsize=(6, 6))
# 1st plot - beh

sns.lineplot(data=df_pred_avg, x="delta_VA", y="rec_mean", hue="ComSourLbl", 
             hue_order=hue_order, errorbar=None,
             linewidth=3, palette=color_order, ax=axs)
# error bar for sem (???)
#sem error bar - if confidence interval, easily relaized by df_all_flipped and internal ci option
axs.errorbar(df_pred_avg.loc[df_pred_avg.ComSourLbl=="Total", 'delta_VA'], df_pred_avg.loc[df_pred_avg.ComSourLbl=="Total",'rec_mean'], 
             yerr=df_pred_avg.loc[df_pred_avg.ComSourLbl=="Total", 'rec_sem'],  fmt='o', capsize=5, color = 'black')
axs.errorbar(df_pred_avg.loc[df_pred_avg.ComSourLbl=="Common", 'delta_VA'], df_pred_avg.loc[df_pred_avg.ComSourLbl=="Common",'rec_mean'], 
             yerr=df_pred_avg.loc[df_pred_avg.ComSourLbl=="Common", 'rec_sem'],  fmt='^', capsize=5, color = 'red')
axs.errorbar(df_pred_avg.loc[df_pred_avg.ComSourLbl=="Separate", 'delta_VA'], df_pred_avg.loc[df_pred_avg.ComSourLbl=="Separate",'rec_mean'], 
             yerr=df_pred_avg.loc[df_pred_avg.ComSourLbl=="Separate", 'rec_sem'],  fmt='s', capsize=5, color = 'blue')

# make invisible some edges
clean_axs(axs)
axs.set_ylabel('Bias (\u00B0)', fontsize=18)
#axs[0].text(0.03, 0.88, 'Model', transform=axs[0].transAxes, fontsize=18, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
axs.set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 18)
#axs[1].set_ylabel(r'% $C = 1$', fontsize = 16)
axs.legend(title='', loc = 'lower center', ncol=3, fontsize = 18, bbox_to_anchor=(0.45, -.35), frameon=False)
# Adjust layout
plt.subplots_adjust(bottom=0.2)
# Save the plot
plt.savefig(os.path.join(work_path, "Modeling", "output", "Model_" + str(m_id) + "_vali_ncnt_New.png"), dpi=300)  # Adjust dpi for print quality
plt.show()


