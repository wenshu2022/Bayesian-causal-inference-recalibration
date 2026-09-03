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
R_path = "C:/Users/wenlou/Documents/R scripts/RecaliProject/output"
os.chdir(work_path)
from help_function import *

#read subject list     
sub_id_lst = read_sub_lst()

################
#define model id
m_id = 70

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


## load beh data from R output
df_beh = pd.read_csv(os.path.join(R_path, 'fix_effect.csv'))
# df_rand = pd.read_csv(os.path.join(R_path, 'rand_effect.csv'))
# sem_ci = df_rand['intr8_c_s'].sem()
# sem_tt = df_rand['intr4_t'].sem()

# load in the count data
#df_beh_cnt = pd.read_csv(os.path.join(R_path, 'beh_count_ci.csv'))
df_beh_cnt = processBehDat()
df_beh_cnt['delta_VA'] = abs(df_beh_cnt['delta_VA'])
cntBehByD = df_beh_cnt.groupby(['sub_id', 'delta_VA'])['ComSourLbl'].count().reset_index()
cntBehByD.columns = ['sub_id', 'delta_VA', 'countByDel']
cntBehByCom = df_beh_cnt.groupby(['sub_id', 'delta_VA','ComSourLbl'])['confLvl'].count().reset_index()
cntBehByCom.columns = ['sub_id', 'delta_VA','ComSourLbl', 'count']

cntBehByCom = pd.merge(cntBehByCom.loc[cntBehByCom.ComSourLbl=='Common'], cntBehByD, how = 'outer', 
                       on = ['sub_id', 'delta_VA']).reset_index(drop=True)
cntBehByCom['pect_C1'] = cntBehByCom['count'] / cntBehByCom['countByDel']

########################

fontsize=16
#########################
##Plotting 
hue_order = [ "Total", "Separate", "Common"]
color_order = ['black', 'blue', 'red']


# figure 1A - beh recalibration with cnt 
fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(10, 5), gridspec_kw={'hspace': 0.2, 'wspace': 0.7, 'height_ratios' : [2,1]})

# beh
sns.lineplot(data = df_beh, x = "abs_delta_VA", y = "effects", hue = "ComSourLbl", hue_order = hue_order,  linewidth=2, 
             palette = color_order, errorbar = None, ax=axs[0, 0])
# standard error from the regression coefcient
axs[0, 0].errorbar(df_beh.loc[df_beh.ComSourLbl=="Total", 'abs_delta_VA'], df_beh.loc[df_beh.ComSourLbl=="Total",'effects'], 
             yerr=df_beh.loc[df_beh.ComSourLbl=="Total", 'std.err'],  capsize=0, ls = '', color = 'black')
axs[0, 0].errorbar(df_beh.loc[df_beh.ComSourLbl=="Common", 'abs_delta_VA'], df_beh.loc[df_beh.ComSourLbl=="Common",'effects'], 
             yerr=df_beh.loc[df_beh.ComSourLbl=="Common", 'std.err'], capsize=0, ls = '', color = 'red')
axs[0, 0].errorbar(df_beh.loc[df_beh.ComSourLbl=="Separate", 'abs_delta_VA'], df_beh.loc[df_beh.ComSourLbl=="Separate",'effects'], 
             yerr=df_beh.loc[df_beh.ComSourLbl=="Separate", 'std.err'], capsize=0, ls = '', color = 'blue')

#count
sns.lineplot(data = cntBehByCom, x="delta_VA", y = 'pect_C1', 
             errorbar = 'se', err_style = 'bars',
             color = 'gray', linewidth=2, ax=axs[1, 0])

#predict
sns.lineplot(data=df_all_flipped, x="delta_VA", y="rec_mean", hue="ComSourLbl", 
             hue_order=hue_order, errorbar='se',err_style = 'bars',
             linewidth=2, palette=color_order, ax=axs[0, 1],legend = None)

# 2nd count plots
sns.lineplot(data = df_all_flipped[df_all_flipped.ComSourLbl=="Common"], x="delta_VA", y = 'ratio',  
             errorbar = 'se', err_style = 'bars',
             color='gray', linewidth=2, ax=axs[1, 1])



for ax in axs.flatten():
    clean_axs(ax)
    ax.set_xlabel('')
#ax_noXlabel(axs[0])

for ax in axs[0,:]:
    ax.set_ylabel('Bias (\u00B0)', fontsize=fontsize)
    #ax.set_ylim(0,3.5)
for ax in axs[1,:]:
    ax.set_ylabel(r'% $C = 1$', fontsize = fontsize)
    ax.set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = fontsize)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals = 0))

axs[0, 0].legend(title='', loc = 'upper left', ncol=1, fontsize = fontsize, bbox_to_anchor=(0.045, 1.2), frameon=False)
# Adjust layout
plt.subplots_adjust(right = 0.92, top = 0.92, bottom = 0.11)
# Save the plot
plt.savefig(os.path.join(work_path, "plot4paper", "recali_w_cnt.png"), dpi=300)  # Adjust dpi for print quality
plt.show()



