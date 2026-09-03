# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 16:19:56 2024

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
data_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction/adhoc'
os.chdir(work_path)
sub_id = 12
m_id = 25

def process_df(sub_id, m_id):
    df_sim = pd.read_csv(os.path.join(data_path, 'pred_sub_' + str(sub_id) + '_m_' + str(m_id) + '.csv'))   
    df_sim['delta_VA'] = df_sim['s_v'] - df_sim['s_a']
    df_sim.loc[df_sim.prob>0.5, 'ComSourLbl'] = 'Common'
    df_sim.loc[df_sim.prob<=0.5, 'ComSourLbl'] = 'Separate'
    df_sim['diff_s_x'] = df_sim['bi_sA_hat'] - df_sim['bi_xA']
    
    # df_sim.loc[df_sim.R_conf<3, 'ConfLbl'] = 'Not High'
    # df_sim.loc[df_sim.R_conf==3, 'ConfLbl'] = 'High'

    ### stat level data
    custom_agg = {
        'rec': [ 'mean'],
        'bi_sA_hat': ['mean'],
        'bi_xA': ['mean'],
        'diff_s_x': [ 'mean'],
        'ComSourLbl': [ 'count'] 
    }
    ## group by common source label and delta_VA
    mean_data_all = df_sim.groupby(['ComSourLbl', 'delta_VA']).agg(custom_agg).reset_index()
    mean_data_all.columns = mean_data_all.columns.droplevel(1)
    # rename the count col 
    current_columns = mean_data_all.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_all.columns = current_columns
    
    ## group by delta_VA
    mean_data_t = df_sim.groupby('delta_VA').agg(custom_agg).reset_index()
    mean_data_t.columns = mean_data_t.columns.droplevel(1)
    current_columns = mean_data_t.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_t.columns = current_columns
    mean_data_t['ComSourLbl'] = "Total"
    
    mean_data_all = pd.concat([mean_data_all, mean_data_t]).reset_index(drop = True)
    # tocalculate the ratio, first merge the total count
    mean_data_all = pd.merge(mean_data_all, mean_data_t[['delta_VA', 'count']], how = 'outer', on = 'delta_VA')
    mean_data_all['ratio'] = mean_data_all['count_x']/mean_data_all['count_y'] *100
    return df_sim, mean_data_all


df_sim, mean_data_all = process_df(sub_id, m_id)

####################################
# add jitter to the data so that the distribution is more obvious
df_sim_jittered = df_sim.copy()
mean_data_T = mean_data_all[mean_data_all.ComSourLbl!='Total'].copy()
#df_sim_jittered.prob = 1 - df_sim_jittered.prob

jitter_amount = 0.3
df_sim_jittered['delta_VA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))
df_sim_jittered['bi_sA_hat'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))
df_sim_jittered['bi_xA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))
#df_sim_jittered['diff_s_x'] = df_sim_jittered['sA_hat'] - df_sim_jittered['bi_xA']

df_sim_com = df_sim_jittered[df_sim_jittered.prob > 0.5]
df_sim_sep = df_sim_jittered[df_sim_jittered.prob <= 0.5]

hue_order = [ "Common", "Separate"]
color_order = [ 'LightCoral', 'blue']
markers = ['o', 's'] 
# Create a LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('custom_cmap', ['blue', 'LightCoral']) # from blue (Separate) to red (common)
norm = plt.Normalize(min(df_sim_jittered.prob), max(df_sim_jittered.prob))


fig = plt.figure(figsize=(8, 8))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.1])
#plt.subplots_adjust(hspace=0.1,wspace=0.05)

# Plot both scatter plots
axs1 = fig.add_subplot(gs[0, 0])
axs1.minorticks_on()
axs1.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)
pcm1 = axs1.scatter(df_sim_com.loc[:,'delta_VA'] + 0.5, df_sim_com.loc[:,'bi_xA'], 
                    c=df_sim_com.loc[:,'prob'], cmap=cmap, norm=norm,  s = 0.1)
axs1.scatter(df_sim_sep.loc[:,'delta_VA'] - 0.5, df_sim_sep.loc[:,'bi_xA'], 
             c=df_sim_sep.loc[:,'prob'], cmap=cmap, norm=norm,  s = 0.1)

# Add major and minor ticks to axs1
axs1.xaxis.set_major_locator(MultipleLocator(4))
axs1.yaxis.set_major_locator(MultipleLocator(8))

sns.lineplot(data = mean_data_T, x = "delta_VA", y = "bi_sA_hat", hue = "ComSourLbl", hue_order = hue_order, 
             dashes = False, palette = color_order,  linewidth=2,  ci = None, ax = axs1, legend = None)
sns.lineplot(data = mean_data_T, x = "delta_VA", y = "bi_xA", hue = "ComSourLbl", hue_order = hue_order,  
             linestyle="--", palette = color_order, linewidth=2,   ci = None, ax = axs1, legend = None)
axs1.set_ylabel('Spatial location (\u00B0)', fontsize = 12)
axs1.set_xlabel('')
#axs1.text(0.25, 1, 'Common', transform=axs1.transAxes, fontsize=15, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))

axs1.spines['top'].set_visible(False)
axs1.spines['right'].set_visible(False)

# Colorbar
cax = fig.add_subplot(gs[0, 1])
cbar = plt.colorbar(pcm1, cax=cax, label=r'$P(C=1|x_A, x_V)$')
# Create custom legend handles
# Add legend with custom handles

custom_legend_handles = [mlines.Line2D([], [], color='LightCoral', linestyle='-'),
                         mlines.Line2D([], [], color='blue', linestyle='-'),
                         mlines.Line2D([], [], color='LightCoral', linestyle='--'), 
                         mlines.Line2D([], [], color='blue', linestyle='--'), 
                         mlines.Line2D([], [], color='LightCoral', marker='o', linestyle=''),
                         mlines.Line2D([], [], color='blue', marker='o', linestyle='')]

# Define the row labels (invisible)
row_labels = [
    mlines.Line2D([], [], linestyle='', marker=''),
    mlines.Line2D([], [], linestyle='', marker='')
]

# Combine row labels and custom legend handles
all_handles = row_labels + custom_legend_handles
all_labels = ['Common', 'Separate', 
              r'$mean(\hat{s}_{A})$', r'$mean(\hat{s}_{A})$', 
              r'$mean(x_{A})$', r'$mean(x_{A})$',  
              r'$x_A$', r'$x_A$']
# all_labels = [r'$P(C=1|x_A,x_V)>0.5$' + ' :', r'$P(C=1|x_A,x_V) \leq 0.5$' + ' :', 
#               r'$mean(\hat{s}_{A})$', r'$mean(\hat{s}_{A})$', 
#               r'$mean(x_{A})$', r'$mean(x_{A})$',  
#               r'$x_A$', r'$x_A$']
fig.legend(handles=all_handles, 
           labels=all_labels,
           ncol=4, fontsize=12, bbox_to_anchor=(0.5, 0), loc='lower center', frameon=False)


# Adjust layout
plt.subplots_adjust(wspace=0.1, hspace=0.1, top=0.9, bottom=0.2, left = 0.1, right = 0.9)

fig.text(0.5, 0.155, 'Spatial disparity (V - A , visual angle \u00B0)', ha='center', fontsize = 16)

plt.savefig(os.path.join(work_path, "output/dist_m" + str(m_id) + '_sub' + str(sub_id) + ".png"), dpi=300)  # Adjust dpi for print quality
# Show the plot
plt.show()