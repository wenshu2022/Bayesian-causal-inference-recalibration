# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 14:31:47 2024

@author: wenlou
"""

import pandas as pd
import numpy as np
import os
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts/"
pred_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
#R_path = "C:/Users/wenlou/Documents/R scripts/output"
os.chdir(work_path)
from help_function import *

#read subject list 
sub_id_lst = read_sub_lst()

colors = {'Total':'black', 'Common':'red', 'Separate':'blue'}

#plot prediction
def plot_conf_pred(sel, sub_id_lst, m_id, color, legend = None):
    # two-step average
    temp_list = []
    for sub_id in sub_id_lst:
        # 1 - average within subjects
        sub_data = agg_pred_conf_by_sub(sub_id, m_id, 1, sel)
        temp_list.append(sub_data)
    df_all_flipped = pd.concat(temp_list, ignore_index=True)

    # 2 - average across subjects
    custom_agg = {
        'rec_mean': [ 'mean', 'sem'],
        'count': [ 'sum']
    }
    df_pred_avg = df_all_flipped[['m_id', 'ConfLbl', 'delta_VA', 'rec_mean', 'count']].groupby(['m_id',  'ConfLbl', 'delta_VA']).agg(custom_agg).reset_index()
    df_pred_avg.columns = ['m_id', 'ConfLbl', 'delta_VA', 'rec_mean', 'rec_sem', 'count']
   # df_pred_avg['ratio'] = df_pred_avg['count']/df_pred_avg['count_total']*100
    df_pred_avg['ComSourLbl'] = sel

    #####plot for model 
    fig, axs = plt.subplots(figsize=(5.5,5))
    # 1st plot - beh
    clean_axs(axs)
    
    sns.lineplot(data = df_pred_avg, x = "delta_VA", y = "rec_mean",  style = "ConfLbl",  color = color,
                style_order= hue_order, linewidth=3,  errorbar = None, ax=axs, legend = legend)

    axs.errorbar(df_pred_avg.loc[df_pred_avg.ConfLbl=="High", 'delta_VA'], df_pred_avg.loc[df_pred_avg.ConfLbl=="High",'rec_mean'], 
                yerr=df_pred_avg.loc[df_pred_avg.ConfLbl=="High",'rec_sem'],  fmt='o', capsize=5, color = color)

    axs.errorbar(df_pred_avg.loc[df_pred_avg.ConfLbl=="Medium", 'delta_VA'], df_pred_avg.loc[df_pred_avg.ConfLbl=="Medium",'rec_mean'], 
                yerr=df_pred_avg.loc[df_pred_avg.ConfLbl=="Medium",'rec_sem'],  fmt='^', capsize=5, color = color)

    axs.errorbar(df_pred_avg.loc[df_pred_avg.ConfLbl=="Low", 'delta_VA'], df_pred_avg.loc[df_pred_avg.ConfLbl=="Low",'rec_mean'], 
                yerr=df_pred_avg.loc[df_pred_avg.ConfLbl=="Low",'rec_sem'],  fmt='s', capsize=5, color = color)


    axs.set_ylabel('Bias (\u00B0)', fontsize = 18)
    axs.set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 18)
    #axs[0].text(0.03, 0.88, 'Model-' + str(m_id), transform=axs[0].transAxes, fontsize=18, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
    axs.legend(title='', loc = 'lower center', ncol=3, fontsize = 18, bbox_to_anchor=(0.45, -0.35), frameon=False)
    axs.set_title(sel, fontsize = fontsize)
    # Adjust layout
    #plt.subplots_adjust(left=0.25) 
    # Save the plot
    if len(sub_id_lst)>1:
        plt.savefig(os.path.join(work_path, "Modeling", "output", "confModel" + str(m_id) + sel + "wocnt.png"), dpi=300)  # Adjust dpi for print quality
    else:
        plt.savefig(os.path.join(work_path, "Modeling", "output", "sub_pred_conf",  "confModel_" + str(m_id) + "_sub" + str(sub_id) + "_" + sel + ".png"), dpi=300)  # Adjust dpi for print quality

    plt.show()

    #return df_pred_avg



hue_order = [ "High", "Medium", "Low"]
markers = ['o', 's', '^'] 

#sel = 'Separate'
#plot_conf_pred(sel, sub_id_lst, 85, colors[sel], 'auto')
# for sel in ['Common', 'Separate']: 
#     for sub_id in sub_id_lst:
#         plot_conf_pred(sel, [sub_id],115, colors[sel], 'auto')
        
for sel in ['Common', 'Separate', 'Total']: 
    plot_conf_pred(sel, sub_id_lst, 100, colors[sel], 'auto')

    
plot_conf_pred('Separate', [41], 109, colors['Separate'], 'auto')    
