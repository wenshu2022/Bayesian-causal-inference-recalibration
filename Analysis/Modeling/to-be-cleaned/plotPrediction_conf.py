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
#from sklearn.linear_model import LinearRegression
#from scipy import stats
#from sklearn import preprocessing
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.lines as mlines
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

sns.set_theme(style="white")
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts/Modeling"
data_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
os.chdir(work_path)

#read subject list 
with open('P:/3026008.01/data_for_fitting/sub_id_exp1.txt', 'r') as file:
    lines = file.readlines()
    
sub_id_lst = [int(line.strip()) for line in lines]
# the model number 
m_id = 47


##########################################################
######  process prediction data ##########################
##########################################################
def process_sub_data(sub_id, m_id, flip, sel):
    # read in sub prediction data
    df_pred = pd.read_csv(os.path.join(data_path, 'm' + str(m_id) ,'pred_sub_' + str(sub_id) + '.csv'))   
    
    #select the auditory block
    #df_pred = df_pred.loc[df_pred.tr_f==1, :]
    df_pred['delta_VA'] = df_pred['s_v'] - df_pred['s_a']
    df_pred.loc[df_pred.R_pc==1, 'ComSourLbl'] = 'Common'
    df_pred.loc[df_pred.R_pc==2, 'ComSourLbl'] = 'Separate'
    
    
    df_pred.loc[df_pred.R_conf==1, 'ConfLbl'] = 'Low'
    df_pred.loc[df_pred.R_conf==2, 'ConfLbl'] = 'Medium'
    df_pred.loc[df_pred.R_conf==3, 'ConfLbl'] = 'High'

    if sel != 'Total':
        df_pred = df_pred.loc[ df_pred.ComSourLbl == sel,]    
        
    if flip:
        mask = df_pred['delta_VA'] < 0
        df_pred.loc[mask, 'rec'] = -df_pred.loc[mask, 'rec']
        df_pred['delta_VA'] = df_pred['delta_VA'].abs()

    custom_agg = {
        'rec': [ 'mean'],
        'ConfLbl': [ 'count']
    }
        
    ## group by common source label and delta_VA
    mean_data_sub = df_pred.groupby([ 'ConfLbl', 'delta_VA']).agg(custom_agg).reset_index()
    mean_data_sub.columns = mean_data_sub.columns.droplevel(1)
    # rename the count col 
    current_columns = mean_data_sub.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_sub.columns = current_columns

    ## apart from the common/separate, we also compute the "Total" category
    mean_data_t = df_pred.groupby(['delta_VA']).agg(custom_agg).reset_index()
    mean_data_t.columns = mean_data_t.columns.droplevel(1)
    current_columns = mean_data_t.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_t.columns = current_columns
    mean_data_t['ConfLbl'] = "Total"
    
    # concat the two stat
    mean_data_sub = pd.concat([mean_data_sub, mean_data_t], ignore_index=True)
    # to calculate the ratio, first merge the total count
    mean_data_sub = pd.merge(mean_data_sub, mean_data_t[['delta_VA', 'count']], how = 'outer', on = ['delta_VA' ])
    mean_data_sub.rename(columns = {'count_x':'count', 'count_y':'count_total'}, inplace = True)
    mean_data_sub['ratio'] = mean_data_sub['count']/mean_data_sub['count_total'] *100

    mean_data_sub['sub_id']= sub_id
    mean_data_sub['m_id']= m_id

    return mean_data_sub


sel = 'Separate'
# two-step average
temp_list = []
for sub_id in sub_id_lst:
    # 1 - average within subjects
    sub_data = process_sub_data(sub_id, m_id, 1, sel)
    temp_list.append(sub_data)
df_all_flipped = pd.concat(temp_list, ignore_index=True)



# 2 - average across subjects
custom_agg = {
    'rec': [ 'mean', 'sem'],
    'count': [ 'sum'],
    'count_total':['sum']
}
df_avg = df_all_flipped[['m_id', 'ConfLbl', 'delta_VA', 'rec', 'count', 'count_total']].groupby(['m_id',  'ConfLbl', 'delta_VA']).agg(custom_agg).reset_index()
df_avg.columns = ['m_id', 'ConfLbl', 'delta_VA', 'rec_mean', 'rec_sem', 'count', 'count_total']

df_avg['ratio'] = df_avg['count']/df_avg['count_total']*100



# hue_order = [ "High", "Medium", "Low"]
# color_order = ['red', 'blue', 'green']
# markers = ['o', 's', '^'] 

hue_order = [ "High", "Medium", "Low"]
color_order = ['darkblue', 'steelblue', 'skyblue']
markers = ['o', 's', '^'] 

######################
######################
#####plot for model 
fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(10, 10), gridspec_kw={'height_ratios': [2, 2]})

# 1st plot - beh
for ax in axs:
    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)

sns.lineplot(data = df_avg, x = "delta_VA", y = "rec_mean", hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", 
             style_order= hue_order, linewidth=2, palette = color_order, markers = markers, ci = None, ax=axs[0])

axs[0].errorbar(df_avg.loc[df_avg.ConfLbl=="High", 'delta_VA'], df_avg.loc[df_avg.ConfLbl=="High",'rec_mean'], 
             yerr=df_avg.loc[df_avg.ConfLbl=="High",'rec_sem'],  fmt='o', capsize=5, color = 'darkblue')

axs[0].errorbar(df_avg.loc[df_avg.ConfLbl=="Medium", 'delta_VA'], df_avg.loc[df_avg.ConfLbl=="Medium",'rec_mean'], 
             yerr=df_avg.loc[df_avg.ConfLbl=="Medium",'rec_sem'],  fmt='^', capsize=5, color = 'steelblue')

axs[0].errorbar(df_avg.loc[df_avg.ConfLbl=="Low", 'delta_VA'], df_avg.loc[df_avg.ConfLbl=="Low",'rec_mean'], 
             yerr=df_avg.loc[df_avg.ConfLbl=="Low",'rec_sem'],  fmt='s', capsize=5, color = 'skyblue')



# count plots
sns.lineplot(data = df_avg, x="delta_VA", y = 'ratio', hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", style_order= hue_order, palette = color_order, markers = markers, linewidth=2, ax=axs[1], ci = None, legend = None)

# Add annotations
for line in axs[1].get_lines():
    for x, y in zip(line.get_xdata(), line.get_ydata()):
        axs[1].text(x, y, f'{y:.0f}', fontsize=9, verticalalignment='bottom', horizontalalignment='right',
                    bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none'))

# make invisible some edges
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(8))

for ax in axs[:1]:
    ax.set_xlabel('')
#    ax.set_ylabel('Bias (\u00B0)')
    ax.xaxis.set_ticklabels([])
    #ax.tick_params(axis='x', which='major', pad=1)

axs[0].set_ylabel('Bias (\u00B0)')
axs[1].set_ylabel('% cases (per spatial disparity)')
axs[0].text(0.03, 0.88, 'Model-' + sel, transform=axs[0].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
#axs[1].text(0.03, 0.88, 'Model ' + str(m_id), transform=axs[1].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))

axs[1].set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 12)
#axs[2].set_ylabel(r'% $C = 1$', fontsize = 12)

axs[0].legend(title='', loc = 'lower center', ncol=3, fontsize = 12, bbox_to_anchor=(0.25, -0.15), frameon=False)
#axs[2].legend(title='', loc = 'lower center', fontsize = 12, bbox_to_anchor=(0.75, -0.95), ncol = 2, frameon=False)

# Adjust layout
plt.subplots_adjust(top=0.9, bottom=0.15, left = 0.1, right = 0.9)
 
# Save the plot
plt.savefig(os.path.join(work_path, "output", "model_" + str(m_id) + '_' + sel + ".png"), dpi=300)  # Adjust dpi for print quality
plt.show()




##########################################################
##########################################################
######  process beh data #################################
##########################################################

R_path = "C:/Users/wenlou/Documents/R scripts"
data_path = "P:/3026008.01/Data/"

#####
##### load behaviour data
df_R_raw = pd.read_csv(os.path.join(R_path, 'fix_effect_conf_wo_com.csv'))
# count the cases in real data 
#df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all_w_VAE_norm.pkl"))  
df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))  

count = df_A[['confLvl', 'abs_delta_VA']].value_counts().reset_index()
current_columns = count.columns.tolist()
current_columns[-1] = 'num'
count.columns = current_columns

## group by delta_VA
count_t = df_A[['abs_delta_VA']].value_counts().reset_index()
current_columns = count_t.columns.tolist()
current_columns[-1] = 'num'
count_t.columns = current_columns

# to calculate the ratio, first merge the total count
count = pd.merge(count, count_t[['abs_delta_VA', 'num']], how = 'outer', on = 'abs_delta_VA')
count['ratio'] = count['num_x']/count['num_y'] *100
count.rename(columns = {'num_x':'count', 'num_y':'count_total'}, inplace = True)

count.loc[count.confLvl==1, 'ConfLbl'] = 'Low'
count.loc[count.confLvl==2, 'ConfLbl'] = 'Medium'
count.loc[count.confLvl==3, 'ConfLbl'] = 'High'

## join data
beh_data = pd.merge(df_R_raw.loc[:, ['new_coef', 'confLvl', 'abs_delta_VA']], count, how = 'outer', on = ['confLvl', 'abs_delta_VA'])

##### deal with random intercept
# read in random effect 
df_R_rand = pd.read_csv(os.path.join(R_path, 'rand_effect_conf_wo_com.csv'))
df_R_rand.sem() #0.063388


## simple plotting 

hue_order = [ "High", "Medium", "Low"]
color_order = ['darkblue', 'steelblue', 'skyblue']
markers = ['o', 's', '^'] 


######################
######################
######  CCN plot
fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(10, 10), gridspec_kw={'height_ratios': [2, 2]})

# 1st plot - beh
for ax in axs:
    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)

sns.lineplot(data = beh_data, x = "abs_delta_VA", y = "new_coef", hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", 
             style_order= hue_order, linewidth=2, palette = color_order, markers = markers, ci = None, ax=axs[0])

axs[0].errorbar(beh_data.loc[beh_data.ConfLbl=="High", 'abs_delta_VA'], beh_data.loc[beh_data.ConfLbl=="High",'new_coef'], 
             yerr=[0.063388]*4,  fmt='o', capsize=5, color = 'darkblue')
axs[0].errorbar(beh_data.loc[beh_data.ConfLbl=="Medium", 'abs_delta_VA'], beh_data.loc[beh_data.ConfLbl=="Medium",'new_coef'], 
             yerr=[0.063388]*4,  fmt='s', capsize=5, color = 'steelblue')
axs[0].errorbar(beh_data.loc[beh_data.ConfLbl=="Low", 'abs_delta_VA'], beh_data.loc[beh_data.ConfLbl=="Low",'new_coef'], 
             yerr=[0.063388]*4,  fmt='^', capsize=5, color = 'skyblue')

# count plots
#sns.lineplot(data = df_avg[df_avg.ComSourLbl=="Common"], x="delta_VA", y = 'ratio',  color='gray', linewidth=2, ax=axs[2], linestyle = ":", label = 'Prediction - M' + str(m_id))
sns.lineplot(data = beh_data, x="abs_delta_VA", y = 'ratio', hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", style_order= hue_order, palette = color_order, markers = markers, linewidth=2, ax=axs[1], legend = None)

# Add annotations
for line in axs[1].get_lines():
    for x, y in zip(line.get_xdata(), line.get_ydata()):
        axs[1].text(x, y, f'{y:.0f}', fontsize=9, verticalalignment='bottom', horizontalalignment='right',
                    bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none'))

# make invisible some edges
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(8))

for ax in axs[:1]:
    ax.set_xlabel('')
#    ax.set_ylabel('Bias (\u00B0)')
    ax.xaxis.set_ticklabels([])
    #ax.tick_params(axis='x', which='major', pad=1)

axs[0].set_ylabel('Bias (\u00B0)')
axs[1].set_ylabel('% cases (per spatial disparity)')
axs[0].text(0.03, 0.88, 'Behavior-Total', transform=axs[0].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
#axs[1].text(0.03, 0.88, 'Model ' + str(m_id), transform=axs[1].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))

axs[1].set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 12)
#axs[2].set_ylabel(r'% $C = 1$', fontsize = 12)

axs[0].legend(title='', loc = 'lower center', ncol=3, fontsize = 12, bbox_to_anchor=(0.25, -0.15), frameon=False)
#axs[2].legend(title='', loc = 'lower center', fontsize = 12, bbox_to_anchor=(0.75, -0.95), ncol = 2, frameon=False)

# Adjust layout
plt.subplots_adjust(top=0.9, bottom=0.15, left = 0.1, right = 0.9)
 
# Save the plot
plt.savefig(os.path.join(work_path, "output", "beh_no_com.png"), dpi=300)  # Adjust dpi for print quality
plt.show()




######################################
######################################
######################################
######################################
# another plot when seperate common vs separate
#####
##### load behaviour data
df_R_w_com = pd.read_csv(os.path.join(R_path, 'fix_effect_conf_w_com.csv'))
df_R_w_com.rename(columns = {'com_flag':'ComSourFlag','com_label': 'ComSourLbl', 'conf_label':'ConfLbl'}, inplace = True)

# count the cases in real data 
df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))  

count = df_A[['confLvl', 'ComSourFlag', 'abs_delta_VA']].value_counts().reset_index()
current_columns = count.columns.tolist()
current_columns[-1] = 'num'
count.columns = current_columns

## group by delta_VA
count_t = df_A[['abs_delta_VA', 'ComSourFlag']].value_counts().reset_index()
current_columns = count_t.columns.tolist()
current_columns[-1] = 'num'
count_t.columns = current_columns

# to calculate the ratio, first merge the total count
count = pd.merge(count, count_t[['abs_delta_VA', 'ComSourFlag', 'num']], how = 'outer', on = ['abs_delta_VA', 'ComSourFlag'])
count['ratio'] = count['num_x']/count['num_y'] *100
count.rename(columns = {'num_x':'count', 'num_y':'count_total'}, inplace = True)

## join data
beh_data = pd.merge(df_R_w_com.loc[:, ['new_coef', 'confLvl', 'ComSourFlag', 'ComSourLbl', 'abs_delta_VA','ConfLbl']], count, how = 'outer', on = ['confLvl', 'abs_delta_VA', 'ComSourFlag'])

##### deal with random intercept
# read in random effect 
df_R_rand = pd.read_csv(os.path.join(R_path, 'rand_effect_conf_w_com.csv'))
df_R_rand.sem() #0.05466


hue_order = [ "High", "Medium", "Low"]
color_order = ['darkblue', 'steelblue', 'skyblue']
markers = ['o', 's', '^'] 

fig, axs = plt.subplots(ncols=1, nrows=4, figsize=(10, 10), gridspec_kw={'height_ratios': [2, 2, 2, 2]})

# 1st plot - beh
for ax in axs:
    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)

sns.lineplot(data = beh_data.loc[beh_data.ComSourFlag==1, ], x = "abs_delta_VA", y = "new_coef", hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", 
             style_order= hue_order, linewidth=2, palette = color_order, markers = markers, ci = None, ax=axs[0])
sns.lineplot(data = beh_data.loc[beh_data.ComSourFlag==0, ], x = "abs_delta_VA", y = "new_coef", hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", 
             style_order= hue_order, linewidth=2, palette = color_order, markers = markers, ci = None, ax=axs[2], legend = None)

axs[0].errorbar(beh_data.loc[(beh_data.ComSourFlag==1) & (beh_data.ConfLbl=="High"), 'abs_delta_VA'], beh_data.loc[(beh_data.ComSourFlag==1) & (beh_data.ConfLbl=="High"),'new_coef'], 
             yerr=[0.05466]*4,  fmt='o', capsize=5, color = 'darkblue')
axs[0].errorbar(beh_data.loc[(beh_data.ComSourFlag==1) & (beh_data.ConfLbl=="Medium"), 'abs_delta_VA'], beh_data.loc[(beh_data.ComSourFlag==1) & (beh_data.ConfLbl=="Medium"),'new_coef'], 
             yerr=[0.05466]*4,  fmt='s', capsize=5, color = 'steelblue')
axs[0].errorbar(beh_data.loc[(beh_data.ComSourFlag==1) & (beh_data.ConfLbl=="Low"), 'abs_delta_VA'], beh_data.loc[(beh_data.ComSourFlag==1) & (beh_data.ConfLbl=="Low"),'new_coef'], 
             yerr=[0.05466]*4,  fmt='^', capsize=5, color = 'skyblue')

axs[2].errorbar(beh_data.loc[(beh_data.ComSourFlag==0) & (beh_data.ConfLbl=="High"), 'abs_delta_VA'], beh_data.loc[(beh_data.ComSourFlag==0) & (beh_data.ConfLbl=="High"),'new_coef'], 
             yerr=[0.05466]*4,  fmt='o', capsize=5, color = 'darkblue')
axs[2].errorbar(beh_data.loc[(beh_data.ComSourFlag==0) & (beh_data.ConfLbl=="Medium"), 'abs_delta_VA'], beh_data.loc[(beh_data.ComSourFlag==0) & (beh_data.ConfLbl=="Medium"),'new_coef'], 
             yerr=[0.05466]*4,  fmt='s', capsize=5, color = 'steelblue')
axs[2].errorbar(beh_data.loc[(beh_data.ComSourFlag==0) & (beh_data.ConfLbl=="Low"), 'abs_delta_VA'], beh_data.loc[(beh_data.ComSourFlag==0) & (beh_data.ConfLbl=="Low"),'new_coef'], 
             yerr=[0.05466]*4,  fmt='^', capsize=5, color = 'skyblue')
# count plots
sns.lineplot(data = beh_data.loc[beh_data.ComSourFlag==1, ], x="abs_delta_VA", y = 'ratio', hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", style_order= hue_order, palette = color_order, markers = markers, linewidth=2, ax=axs[1], legend = None)
sns.lineplot(data = beh_data.loc[beh_data.ComSourFlag==0, ], x="abs_delta_VA", y = 'ratio', hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", style_order= hue_order, palette = color_order, markers = markers, linewidth=2, ax=axs[3], legend = None)

# Add annotations
for ax in axs[[1,3]]:
    for line in ax.get_lines():
        for x, y in zip(line.get_xdata(), line.get_ydata()):
            ax.text(x, y, f'{y:.0f}', fontsize=9, verticalalignment='bottom', horizontalalignment='right',
                        bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none'))

# make invisible some edges
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(8))

for ax in axs[:3]:
    ax.set_xlabel('')
#    ax.set_ylabel('Bias (\u00B0)')
    ax.xaxis.set_ticklabels([])
    #ax.tick_params(axis='x', which='major', pad=1)

axs[0].set_ylabel('Bias (\u00B0)')
axs[2].set_ylabel('Bias (\u00B0)')
axs[1].set_ylabel('% cases (per spatial disparity)')
axs[3].set_ylabel('% cases (per spatial disparity)')
axs[0].text(0.03, 0.88, 'Behavior-Common', transform=axs[0].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
axs[2].text(0.03, -1.55, 'Behavior-Separate', transform=axs[0].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))

#axs[1].text(0.03, 0.88, 'Model ' + str(m_id), transform=axs[1].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))

axs[3].set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 12)
#axs[2].set_ylabel(r'% $C = 1$', fontsize = 12)

axs[0].legend(title='', loc = 'lower center', ncol=3, fontsize = 12, bbox_to_anchor=(0.25, -4.15), frameon=False)
#axs[2].legend(title='', loc = 'lower center', fontsize = 12, bbox_to_anchor=(0.75, -0.95), ncol = 2, frameon=False)

# Adjust layout
plt.subplots_adjust(top=0.9, bottom=0.15, left = 0.1, right = 0.9)
 
# Save the plot
plt.savefig(os.path.join(work_path, "output", "beh_com.png"), dpi=300)  # Adjust dpi for print quality
plt.show()
