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
m_id = 20


##########################################################
######  process prediction data ##########################
##########################################################
def process_sub_data(sub_id, m_id, flip):
    # read in sub prediction data
    df_pred = pd.read_csv(os.path.join(data_path, 'm' + str(m_id) ,'pred_sub_' + str(sub_id) + '.csv'))   
    
    #select the auditory block
    #df_pred = df_pred.loc[df_pred.tr_f==1, :]
    df_pred['delta_VA'] = df_pred['s_v'] - df_pred['s_a']
    df_pred.loc[df_pred.prob>0.5, 'ComSourLbl'] = 'Common'
    df_pred.loc[df_pred.prob<=0.5, 'ComSourLbl'] = 'Separate'
    
    df_pred.loc[df_pred.R_conf==1, 'ConfLbl'] = 'Low'
    df_pred.loc[df_pred.R_conf==2, 'ConfLbl'] = 'Medium'
    df_pred.loc[df_pred.R_conf==3, 'ConfLbl'] = 'High'

    if flip:
        mask = df_pred['delta_VA'] < 0
        df_pred.loc[mask, 'rec'] = -df_pred.loc[mask, 'rec']
        df_pred['delta_VA'] = df_pred['delta_VA'].abs()

    ### stat level data
    custom_agg = {
        'rec': [ 'mean'],
        'ComSourLbl': [ 'count']
    }
    ## group by common source label and delta_VA
    mean_data_sub = df_pred.groupby(['ComSourLbl', 'ConfLbl', 'delta_VA']).agg(custom_agg).reset_index()
    mean_data_sub.columns = mean_data_sub.columns.droplevel(1)
    # rename the count col 
    current_columns = mean_data_sub.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_sub.columns = current_columns

    ## apart from the common/separate, we also compute the "Total" category
    mean_data_t = df_pred.groupby(['delta_VA','ComSourLbl']).agg(custom_agg).reset_index()
    mean_data_t.columns = mean_data_t.columns.droplevel(1)
    current_columns = mean_data_t.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_t.columns = current_columns
    mean_data_t['ConfLbl'] = "Total"
    
    # concat the two stat
    mean_data_sub = pd.concat([mean_data_sub, mean_data_t], ignore_index=True)
    # to calculate the ratio, first merge the total count
    mean_data_sub = pd.merge(mean_data_sub, mean_data_t[['delta_VA','ComSourLbl', 'count']], how = 'outer', on = ['delta_VA' ,'ComSourLbl'])
    mean_data_sub.rename(columns = {'count_x':'count', 'count_y':'count_total'}, inplace = True)
    mean_data_sub['ratio'] = mean_data_sub['count']/mean_data_sub['count_total'] *100
    mean_data_sub['sub_id']= sub_id
    mean_data_sub['m_id']= m_id

    return mean_data_sub



# two-step average
temp_list = []
for sub_id in sub_id_lst:
    # 1 - average within subjects
    sub_data = process_sub_data(sub_id, m_id, 1)
    temp_list.append(sub_data)
df_all_flipped = pd.concat(temp_list, ignore_index=True)


# 2 - average across subjects
custom_agg = {
    'rec': [ 'mean'],
    'count': [ 'sum'],
    'count_total':['sum']
}
df_avg = df_all_flipped[['m_id', 'ComSourLbl', 'ConfLbl', 'delta_VA', 'rec', 'count', 'count_total']].groupby(['m_id', 'ComSourLbl', 'ConfLbl', 'delta_VA']).agg(custom_agg).reset_index()
df_avg.columns = df_avg.columns.droplevel(1)
df_avg['ratio'] = df_avg['count']/df_avg['count_total']*100


##########################################################
##########################################################

##########################################################
##########################################################
######  process beh data #################################
##########################################################

R_path = "C:/Users/wenlou/Documents/R scripts"
data_path = "P:/3026008.01/Data/"

#####
##### load behaviour data
df_R_raw = pd.read_csv(os.path.join(R_path, 'coef_raw_VAE_conf_wo_com.csv'))
# count the cases in real data 
#df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all_w_VAE_norm.pkl"))  
df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))  

#sub_id_lst = pd.read_pickle(os.path.join(data_path, "exp1_sub_lst.pkl"))
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


## simple plotting 

hue_order = [ "High", "Medium", "Low"]
color_order = ['red', 'blue', 'green']
markers = ['o', 's', '^'] 

# sns.lineplot(data= df_avg.loc[df_avg.ComSourLbl=='Common', :], x="delta_VA", y="rec", hue="ConfLbl", style="ConfLbl", 
#              hue_order=hue_order, style_order=hue_order, 
#              linewidth=2, palette=color_order, ci=None, markers = markers)
# plt.title('Common')
# plt.show()
# sns.lineplot(data= df_avg.loc[df_avg.ComSourLbl=='Separate', :], x="delta_VA", y="rec", hue="ConfLbl", style="ConfLbl", 
#              hue_order=hue_order, style_order=hue_order, 
#              linewidth=2, palette=color_order, ci=None, markers = markers)
# plt.title('Separate')
# plt.show()
# sns.lineplot(data= df_avg, x="delta_VA", y="rec", hue="ConfLbl", style="ConfLbl", 
#              hue_order=hue_order, style_order=hue_order, 
#              linewidth=2, palette=color_order, ci=None, markers = markers)
# plt.title('Total')
# plt.show()


######################
######################
######  CCN plot
fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(10, 10), gridspec_kw={'height_ratios': [2, 2]})

# 1st plot - beh
for ax in axs:
    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)

sns.lineplot(data = df_R_raw, x = "abs_delta_VA", y = "new_coef", hue = "conf_label", hue_order = hue_order, style = "conf_label", 
             style_order= hue_order, linewidth=2, palette = color_order, markers = markers, ci = None, ax=axs[0])

sns.lineplot(data=df_avg, x="delta_VA", y="rec", hue="ConfLbl", style="ConfLbl", 
             hue_order=hue_order, style_order=hue_order, 
             linewidth=2, palette=color_order, ci=None, ax=axs[1], markers = markers, legend=None)

# count plots
#sns.lineplot(data = df_avg[df_avg.ComSourLbl=="Common"], x="delta_VA", y = 'ratio',  color='gray', linewidth=2, ax=axs[2], linestyle = ":", label = 'Prediction - M' + str(m_id))
#sns.lineplot(data = count[count.ComSourLbl=="Common"], x="abs_delta_VA", y = 'ratio', color = 'gray', linewidth=2, ax=axs[2], label = 'Behavior')

# make invisible some edges
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(8))

for ax in axs[:2]:
    ax.set_xlabel('')
    ax.set_ylabel('Bias (\u00B0)')
    ax.xaxis.set_ticklabels([])
    #ax.tick_params(axis='x', which='major', pad=1)

axs[0].text(0.03, 0.88, 'Behavior', transform=axs[0].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
axs[1].text(0.03, 0.88, 'Model ' + str(m_id), transform=axs[1].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))

axs[1].set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 12)
#axs[2].set_ylabel(r'% $C = 1$', fontsize = 12)

axs[0].legend(title='', loc = 'lower center', ncol=3, fontsize = 12, bbox_to_anchor=(0.25, -0.25), frameon=False)
#axs[2].legend(title='', loc = 'lower center', fontsize = 12, bbox_to_anchor=(0.75, -0.95), ncol = 2, frameon=False)

# Adjust layout
plt.subplots_adjust(top=0.9, bottom=0.15, left = 0.1, right = 0.9)
 
# Save the plot
plt.savefig(os.path.join(work_path, "output", "Model_" + str(m_id) + "_validation_conf.png"), dpi=300)  # Adjust dpi for print quality
plt.show()






