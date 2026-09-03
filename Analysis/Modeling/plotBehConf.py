# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:20:05 2024

@author: wenlou
"""
import pandas as pd
import numpy as np
import os
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
#pred_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
R_path = "C:/Users/wenlou/Documents/R scripts/RecaliProject/output"
os.chdir(work_path)
from help_function import *

##### load behaviour data
df_beh = pd.read_csv(os.path.join(R_path, 'fix_effect_conf.csv'))
df_rand = pd.read_csv(os.path.join(R_path, 'rand_effect_conf.csv'))
# load in the count data
df_beh_cnt = pd.read_csv(os.path.join(R_path, 'beh_count_conf.csv'))

def plot_conf_beh(sel,color):

    if sel=='Total':
        sem_conf = df_rand['intr12_t'].sem()
    else:
        sem_conf = df_rand['intr24'].sem()
    
    ##plot
    fig, axs = plt.subplots(figsize=(5.5,5))
     
    # 1st plot - beh
    sns.lineplot(data = df_beh.loc[df_beh.ComSourLbl==sel, ], x = "abs_delta_VA", y = "effects", style = "ConfLbl", color = color,
                 style_order= hue_order, linewidth=3, ci = None)
    axs.errorbar(df_beh.loc[(df_beh.ConfLbl=="High") & (df_beh.ComSourLbl==sel), 'abs_delta_VA'], df_beh.loc[(df_beh.ConfLbl=="High") & (df_beh.ComSourLbl==sel),'effects'], 
                 yerr=sem_conf*4,  fmt='o', capsize=5, color = color)
    axs.errorbar(df_beh.loc[(df_beh.ConfLbl=="Medium") & (df_beh.ComSourLbl==sel), 'abs_delta_VA'], df_beh.loc[(df_beh.ConfLbl=="Medium") & (df_beh.ComSourLbl==sel),'effects'], 
                 yerr=sem_conf*4,  fmt='s', capsize=5, color = color)
    axs.errorbar(df_beh.loc[(df_beh.ConfLbl=="Low") & (df_beh.ComSourLbl==sel), 'abs_delta_VA'], df_beh.loc[(df_beh.ConfLbl=="Low") & (df_beh.ComSourLbl==sel),'effects'], 
                 yerr=sem_conf*4,  fmt='^', capsize=5, color = color)

    # make invisible some edges
    clean_axs(axs)

    axs.set_ylabel('Bias (\u00B0)', fontsize = 20)
    axs.set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 20)
    #axs.text(0.03, 0.88, 'Behavior-' + sel, transform=axs[0].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
    axs.legend(title='', loc = 'upper left', ncol=1, fontsize = 20,  frameon=False)
  
    # Adjust layout
    #plt.subplots_adjust(left=0.25)     
    # Save the plot
    plt.savefig(os.path.join(work_path, "Modeling", "output", "confBeh" +  sel + "wocnt.png"), dpi=300)  # Adjust dpi for print quality
    plt.show()


hue_order = [ "High", "Medium", "Low"]
markers = ['o', 's', '^'] 

# sel = 'Total'
# plot_conf_beh(sel)
colors = {'Total':'black', 'Common':'red', 'Separate':'blue'}
sel='Separate'
plot_conf_beh(sel, colors[sel])

#for sel in ['Total', 'Common', 'Separate']:
#    plot_conf_beh(sel, colors[sel])

