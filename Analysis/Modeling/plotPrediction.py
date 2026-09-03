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
m_id =100

def plot_sublst_recalpred(m_id, sub_id_lst):

    ########################
    #####data prepare ######
    ##process prediction data 
    # two-step average
    temp_list = []

    for sub_id in sub_id_lst:
        # 1 - average within subjects
        sub_data = agg_pred_by_sub(sub_id, m_id, 1)
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
    if len(sub_id_lst)>1:
        # Save the plot
        plt.savefig(os.path.join(work_path, "Modeling", "output", "Model_" + str(m_id) + "_vali_ncnt.png"), dpi=300)  # Adjust dpi for print quality
    else:
        plt.savefig(os.path.join(work_path, "Modeling", "output", "sub_pred",  "Model_" + str(m_id) + "_sub" + str(sub_id) + "_vali_ncnt.png"), dpi=300)  # Adjust dpi for print quality

    plt.show()



# for sub_id in sub_id_lst:
#     plot_sublst_recalpred(m_id, [sub_id])
plot_sublst_recalpred(m_id, sub_id_lst)