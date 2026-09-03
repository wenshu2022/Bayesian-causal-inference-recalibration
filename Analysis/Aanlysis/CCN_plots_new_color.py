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
work_path = "C:/Users/wenlou/Documents/Python Scripts"
mat_data_path = 'C:/Users/wenlou/Documents/MATLAB/Model_local/plotTimFigue4CCN'
#data_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction/adhoc'
os.chdir(work_path)

sub_id = 15
m_id = 25
####################################
####################################
### CI model########################
####################################
####################################

### create the distribution plots - like tim fig 4

def process_df(ds):
    df_sim = pd.read_csv(os.path.join(mat_data_path, 'simualted_data_xv0_baseline_' + ds +'_1504.csv'))   
    #df_sim = pd.read_csv(os.path.join(data_path, 'pred_sub_' + str(sub_id) + '_m_' + str(m_id) + '.csv'))   
    df_sim['delta_VA'] = df_sim['s_v'] - df_sim['s_a']
    df_sim.loc[df_sim.prob>0.5, 'ComSourLbl'] = 'Common'
    df_sim.loc[df_sim.prob<=0.5, 'ComSourLbl'] = 'Separate'
    df_sim['diff_s_x'] = df_sim['sA_hat'] - df_sim['x_A']
    
    ### stat level data
    custom_agg = {
        'rec': [ 'mean'],
        'sA_hat': ['mean'],
        'x_A': ['mean'],
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
    
    mean_data_all = pd.concat([mean_data_all, mean_data_t]).reset_index()
    # tocalculate the ratio, first merge the total count
    mean_data_all = pd.merge(mean_data_all, mean_data_t[['delta_VA', 'count']], how = 'outer', on = 'delta_VA')
    mean_data_all['ratio'] = mean_data_all['count_x']/mean_data_all['count_y'] *100
    return df_sim, mean_data_all

df_sim_MA, mean_data_MA = process_df('CI_MA')
df_sim_MS, mean_data_MS = process_df('CI_MS')


####################################
# add jitter to the data so that the distribution is more obvious
df_sim_MA_jittered = df_sim_MA.copy()
jitter_amount = 0.3
df_sim_MA_jittered['delta_VA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_MA_jittered))
df_sim_MA_jittered['sA_hat'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_MA_jittered))
df_sim_MA_jittered['x_A'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_MA_jittered))
#df_sim_jittered['diff_s_x'] = df_sim_jittered['sA_hat'] - df_sim_jittered['x_A']
df_sim_MA_com = df_sim_MA_jittered[df_sim_MA_jittered.prob > 0.5]
df_sim_MA_dis = df_sim_MA_jittered[df_sim_MA_jittered.prob <= 0.5]


df_sim_MS_jittered = df_sim_MS.copy()
df_sim_MS_jittered['delta_VA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_MS_jittered))
df_sim_MS_jittered['sA_hat'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_MS_jittered))
df_sim_MS_jittered['x_A'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_MS_jittered))
#df_sim_jittered['diff_s_x'] = df_sim_jittered['sA_hat'] - df_sim_jittered['x_A']
df_sim_MS_com = df_sim_MS_jittered[df_sim_MS_jittered.prob > 0.5]
df_sim_MS_dis = df_sim_MS_jittered[df_sim_MS_jittered.prob <= 0.5]

# Create a LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('custom_cmap', ['lightgreen', 'darkgreen']) # from blue (Separate) to red (common)
norm = plt.Normalize(min(df_sim_MA.prob), max(df_sim_MA.prob))

##### CNN figure
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.1])
#plt.subplots_adjust(hspace=0.1,wspace=0.05)

# Plot both scatter plots
axs1 = fig.add_subplot(gs[0, 0])
axs1.minorticks_on()
axs1.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)
pcm1 = axs1.scatter(df_sim_MA_dis.delta_VA + 0.4, df_sim_MA_dis.x_A, c=df_sim_MA_dis.prob, cmap=cmap, norm=norm,  s = 1)
axs1.scatter(df_sim_MA_com.delta_VA - 0.4, df_sim_MA_com.x_A, c=df_sim_MA_com.prob, cmap=cmap, norm=norm,  s = 1)

# Add major and minor ticks to axs1
axs1.xaxis.set_major_locator(MultipleLocator(5))
axs1.yaxis.set_major_locator(MultipleLocator(10))


sns.lineplot(data = mean_data_MA[mean_data_MA.ComSourLbl=='Common'], x = "delta_VA", y = "x_A",  
              linestyle="--", color = 'darkgreen', linewidth=2,   ci = None, ax = axs1, legend = None)
sns.lineplot(data = mean_data_MA[mean_data_MA.ComSourLbl=='Separate'], x = "delta_VA", y = "x_A",  
              linestyle="--", color = 'lightgreen', linewidth=2,   ci = None, ax = axs1, legend = None)

sns.lineplot(data = mean_data_MA[mean_data_MA.ComSourLbl=='Common'], x = "delta_VA", y = "sA_hat",
              dashes = False, color = 'darkblue',  linewidth=2,  ci = None, ax = axs1, legend = None)
sns.lineplot(data = mean_data_MA[mean_data_MA.ComSourLbl=='Separate'], x = "delta_VA", y = "sA_hat",
              dashes = False, color = 'steelblue',  linewidth=2,  ci = None, ax = axs1, legend = None)

# sns.lineplot(data = mean_data_MA[mean_data_MA.ComSourLbl!='Total'], x = "delta_VA", y = "sA_hat", hue = "ComSourLbl", hue_order = hue_order, 
#              dashes = False, palette = color_order,  linewidth=2,  ci = None, ax = axs1, legend = None)
# sns.lineplot(data = mean_data_MA[mean_data_MA.ComSourLbl!='Total'], x = "delta_VA", y = "x_A", hue = "ComSourLbl", hue_order = hue_order,  
#              linestyle="--", palette = color_order, linewidth=2,   ci = None, ax = axs1, legend = None)
axs1.set_ylabel('Spatial location (\u00B0)', fontsize = 12)
axs1.set_xlabel('')
axs1.text(0.25, 1, 'Causal Inference (MA)', transform=axs1.transAxes, fontsize=15, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))


#axs1.yaxis.set_major_locator(plt.MultipleLocator(5))
#axs1.yaxis.set_minor_locator(plt.MultipleLocator(1))

axs1.spines['top'].set_visible(False)
axs1.spines['right'].set_visible(False)

axs2 = fig.add_subplot(gs[0, 1])
axs2.minorticks_on()
axs2.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)
axs2.scatter(df_sim_MS_dis.delta_VA + 0.4, df_sim_MS_dis.x_A, c=df_sim_MS_dis.prob, cmap=cmap, norm=norm,  s = 1)
axs2.scatter(df_sim_MS_com.delta_VA - 0.4, df_sim_MS_com.x_A, c=df_sim_MS_com.prob, cmap=cmap, norm=norm,  s = 1)

axs2.xaxis.set_major_locator(MultipleLocator(5))
#axs2.xaxis.set_minor_locator(MultipleLocator(1))
axs2.yaxis.set_major_locator(MultipleLocator(10))

#ADD THE AVERAGE LINE
sns.lineplot(data = mean_data_MS[mean_data_MS.ComSourLbl=='Common'], x = "delta_VA", y = "x_A",  
              linestyle="--", color = 'darkgreen', linewidth=2,   ci = None, ax = axs2, legend = None)
sns.lineplot(data = mean_data_MS[mean_data_MS.ComSourLbl=='Separate'], x = "delta_VA", y = "x_A",  
              linestyle="--", color = 'lightgreen', linewidth=2,   ci = None, ax = axs2, legend = None)

sns.lineplot(data = mean_data_MS[mean_data_MS.ComSourLbl=='Common'], x = "delta_VA", y = "sA_hat",
              dashes = False, color = 'darkblue',  linewidth=2,  ci = None, ax = axs2, legend = None)
sns.lineplot(data = mean_data_MS[mean_data_MS.ComSourLbl=='Separate'], x = "delta_VA", y = "sA_hat",
              dashes = False, color = 'steelblue',  linewidth=2,  ci = None, ax = axs2, legend = None)


# sns.lineplot(data = mean_data_MS[mean_data_MS.ComSourLbl!='Total'], x = "delta_VA", y = "sA_hat", hue = "ComSourLbl", hue_order = hue_order, 
#              dashes = False, palette = color_order,  linewidth=2,  ci = None, ax = axs2, legend = None)
# sns.lineplot(data = mean_data_MS[mean_data_MS.ComSourLbl!='Total'], x = "delta_VA", y = "x_A", hue = "ComSourLbl", hue_order = hue_order,  
#              linestyle="--", palette = color_order, linewidth=2,   ci = None, ax = axs2, legend = None)

axs2.text(0.25, 1, 'Causal Inference (MS)', transform=axs2.transAxes, fontsize=15, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
axs2.set_xlabel('')
axs2.set_ylabel('')
axs2.yaxis.set_ticklabels([])

axs2.spines['top'].set_visible(False)
axs2.spines['right'].set_visible(False)


# Colorbar
cax = fig.add_subplot(gs[0, 2])
cbar = plt.colorbar(pcm1, cax=cax, label=r'$P(C=1|x_A, x_V)$')

# Create custom legend handles
# Add legend with custom handles

custom_legend_handles = [mlines.Line2D([], [], color='darkblue', linestyle='-'),
                         mlines.Line2D([], [], color='steelblue', linestyle='-'),
                         mlines.Line2D([], [], color='darkgreen', linestyle='--'), 
                         mlines.Line2D([], [], color='lightgreen', linestyle='--'), 
                         mlines.Line2D([], [], color='darkgreen', marker='o', linestyle=''),
                         mlines.Line2D([], [], color='lightgreen', marker='o', linestyle='')]

# Define the row labels (invisible)
row_labels = [
    mlines.Line2D([], [], linestyle='', marker=''),
    mlines.Line2D([], [], linestyle='', marker='')
]

# Combine row labels and custom legend handles
all_handles = row_labels + custom_legend_handles
all_labels = [r'$P(C=1|x_A,x_V)>0.5$' + ' :', r'$P(C=1|x_A,x_V) \leq 0.5$' + ' :', 
              r'$mean(\hat{s}_{A})$', r'$mean(\hat{s}_{A})$', 
              r'$mean(x_{A})$', r'$mean(x_{A})$',  
              r'$x_A$', r'$x_A$']

fig.legend(handles=all_handles, 
           labels=all_labels,
           ncol=4, fontsize=12, bbox_to_anchor=(0.5, 0), loc='lower center', frameon=False)


# Adjust layout
plt.subplots_adjust(wspace=0.1, hspace=0.1, top=0.9, bottom=0.2, left = 0.1, right = 0.9)

fig.text(0.5, 0.155, 'Spatial disparity (V - A , visual angle \u00B0)', ha='center', fontsize = 16)

#plt.xticks([0, 5, 10, 15])

plt.savefig(os.path.join(work_path, "Aanlysis/output/CI_2models.png"), dpi=360)  # Adjust dpi for print quality
# Show the plot
plt.show()

####################################
########FR model##################
####################################
### WITHOUT THE SOLID LINE

df_sim_MA, mean_data_MA = process_df('CI_MA')
####################################
# add jitter to the data so that the distribution is more obvious
df_sim_MA_jittered = df_sim_MA.copy()
jitter_amount = 0.3
df_sim_MA_jittered['delta_VA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_MA_jittered))
df_sim_MA_jittered['x_A'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_MA_jittered))
#df_sim_jittered['diff_s_x'] = df_sim_jittered['sA_hat'] - df_sim_jittered['x_A']
df_sim_MA_com = df_sim_MA_jittered[df_sim_MA_jittered.prob > 0.5]
df_sim_MA_dis = df_sim_MA_jittered[df_sim_MA_jittered.prob <= 0.5]


# Create a LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('custom_cmap', ['lightgreen', 'darkgreen']) # from blue (Separate) to red (common)
norm = plt.Normalize(min(df_sim_MA.prob), max(df_sim_MA.prob))


##### CNN figure
fig = plt.figure(figsize=(6, 6))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.05])
#plt.subplots_adjust(hspace=0.1,wspace=0.05)

# Plot both scatter plots
axs1 = fig.add_subplot(gs[0, 0])
axs1.minorticks_on()
axs1.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)
pcm1 = axs1.scatter(df_sim_MA_dis.delta_VA + 0.4, df_sim_MA_dis.x_A, c=df_sim_MA_dis.prob, cmap=cmap, norm=norm,  s = 1)
axs1.scatter(df_sim_MA_com.delta_VA - 0.4, df_sim_MA_com.x_A, c=df_sim_MA_com.prob, cmap=cmap, norm=norm,  s = 1)

# Add major and minor ticks to axs1
axs1.xaxis.set_major_locator(MultipleLocator(5))
axs1.yaxis.set_major_locator(MultipleLocator(10))

sns.lineplot(data = mean_data_MA[mean_data_MA.ComSourLbl=='Common'], x = "delta_VA", y = "x_A",  
              linestyle="--", color = 'darkgreen', linewidth=2,   ci = None, ax = axs1, legend = None)
sns.lineplot(data = mean_data_MA[mean_data_MA.ComSourLbl=='Separate'], x = "delta_VA", y = "x_A",  
              linestyle="--", color = 'lightgreen', linewidth=2,   ci = None, ax = axs1, legend = None)
axs1.set_ylabel('Spatial location (\u00B0)', fontsize = 12)
axs1.set_xlabel('')
#axs1.text(0.25, 1, 'Fixed-ratio', transform=axs1.transAxes, fontsize=15, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))

axs1.spines['top'].set_visible(False)
axs1.spines['right'].set_visible(False)
    
# Colorbar
cax = fig.add_subplot(gs[0, 1])
cbar = plt.colorbar(pcm1, cax=cax, label=r'$P(C=1|x_A, x_V)$')

# Create custom legend handles
# Add legend with custom handles

custom_legend_handles = [mlines.Line2D([], [], color='darkgreen', linestyle='--'), 
                         mlines.Line2D([], [], color='lightgreen', linestyle='--'), 
                         mlines.Line2D([], [], color='darkgreen', marker='o', linestyle=''),
                         mlines.Line2D([], [], color='lightgreen', marker='o', linestyle='')]

# Define the row labels (invisible)
row_labels = [
    mlines.Line2D([], [], linestyle='', marker=''),
    mlines.Line2D([], [], linestyle='', marker='')
]

# Combine row labels and custom legend handles
all_handles = row_labels + custom_legend_handles
all_labels = [r'$P(C=1|x_A,x_V)>0.5$' + ' :', r'$P(C=1|x_A,x_V) \leq 0.5$' + ' :', 
              r'$mean(x_{A})$', r'$mean(x_{A})$',  
              r'$x_A$', r'$x_A$']

fig.legend(handles=all_handles, 
           labels=all_labels,
           ncol=3, fontsize=12, bbox_to_anchor=(0.5, 0), loc='lower center', frameon=False)


# Adjust layout
plt.subplots_adjust(wspace=0.1, hspace=0.1, top=0.9, bottom=0.2, left = 0.1, right = 0.9)

fig.text(0.5, 0.15, 'Spatial disparity (V - A , visual angle \u00B0)', ha='center', fontsize = 12)


plt.savefig(os.path.join(work_path, "output/inf_ccn_fr0616_v2.png"), dpi=300)  # Adjust dpi for print quality
# Show the plot
plt.show()


####################################
####################################
####################################
####################################
####################################
### FIGURE 2####
# Same style plots: beh and sim with counts

R_path = "C:/Users/wenlou/Documents/R scripts"
data_path = "P:/3026008.01/Data/"


def process_data_flipped(ds):
    df_sim = pd.read_csv(os.path.join(mat_data_path, 'simualted_data_all_baseline_' + ds +'_1504.csv'))
    df_sim['delta_VA'] = df_sim['s_v'] - df_sim['s_a']
    df_sim.loc[df_sim.prob>0.5, 'ComSourLbl'] = 'Common'
    df_sim.loc[df_sim.prob<=0.5, 'ComSourLbl'] = 'Separate'
    df_sim['diff_s_x'] = df_sim['sA_hat'] - df_sim['x_A']

    df_sim["flipRec"]= df_sim.rec.copy()
    df_sim.loc[df_sim.delta_VA < 0, "flipRec"] = -df_sim.loc[df_sim.delta_VA < 0, "rec"]
    df_sim["abs_delta_VA"] = abs(df_sim.delta_VA)

    ### stat level data
    custom_agg = {
        'flipRec': [ 'mean'],
        'sA_hat': ['mean'],
        'x_A': ['mean'],
        'diff_s_x': [ 'mean'],
        'ComSourLbl': [ 'count'] 
    }
    ## group by common source label and delta_VA
    mean_data_all = df_sim.groupby(['ComSourLbl', 'abs_delta_VA']).agg(custom_agg).reset_index()
    mean_data_all.columns = mean_data_all.columns.droplevel(1)
    # rename the count col 
    current_columns = mean_data_all.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_all.columns = current_columns

    ## group by delta_VA
    mean_data_t = df_sim.groupby('abs_delta_VA').agg(custom_agg).reset_index()
    mean_data_t.columns = mean_data_t.columns.droplevel(1)
    current_columns = mean_data_t.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_t.columns = current_columns
    mean_data_t['ComSourLbl'] = "Total"

    mean_data_all = pd.concat([mean_data_all, mean_data_t]).reset_index()
    # tocalculate the ratio, first merge the total count
    mean_data_all = pd.merge(mean_data_all, mean_data_t[['abs_delta_VA', 'count']], how = 'outer', on = 'abs_delta_VA')
    mean_data_all['ratio'] = mean_data_all['count_x']/mean_data_all['count_y'] *100
    mean_data_all['ComSourLbl'] = mean_data_all['ComSourLbl'] + " - " + ds

    return mean_data_all


#####
##### load behaviour data

df_R_raw = pd.read_csv(os.path.join(R_path, 'coef_raw_VAE.csv'))
# change name
df_R_raw.loc[df_R_raw.com_label=='Distinct','com_label'] = 'Separate'
# count the cases in real data 
df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all_w_VAE_norm.pkl"))  
#sub_id_lst = pd.read_pickle(os.path.join(data_path, "exp1_sub_lst.pkl"))
count = df_A[['ComSourLbl', 'abs_delta_VA']].value_counts().reset_index()
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


######
##### load simulated data
df_FR = process_data_flipped('FR')
df_MS = process_data_flipped('CI_MS')
df_MA = process_data_flipped('CI_MA')


hue_order = [ "Total", "Separate", "Common"]
color_order = ['black', 'silver', 'darkslategray']
markers = ['o', 's', '^'] 

######################
######################
######  CCN plot
fig, axs = plt.subplots(ncols=1, nrows=4, figsize=(10, 8), gridspec_kw={'height_ratios': [2, 2, 2, 2]})
#plt.subplots_adjust(hspace=0.1,wspace=0.1)

# 1st plot - beh
for ax in axs:
    ax.minorticks_on()
    ax.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)

sns.lineplot(data = df_R_raw, x = "abs_delta_VA", y = "new_coef", hue = "com_label", hue_order = hue_order, style = "com_label", 
             style_order= hue_order, linewidth=2, palette = color_order, markers = markers, ci = None, ax=axs[0])
# hue_order = [ "Total", "Separate", "Common"]
# color_order = ['black', 'blue', 'red']
# markers = ['o', 's', '^'] 
# sns.lineplot(data = df_R_raw, x = "abs_delta_VA", y = "new_coef", hue = "com_label", hue_order = hue_order, style = "com_label", 
#               style_order= hue_order, linewidth=2, palette = color_order, markers = markers)
# plt.xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 12)
# plt.ylabel('Bias (\u00B0)')
# plt.legend(title='',  fontsize = 12,frameon=False)
sns.lineplot(data=df_FR, x="abs_delta_VA", y="flipRec", hue="ComSourLbl", style="ComSourLbl", 
             hue_order=["Total - FR", "Separate - FR", "Common - FR"], style_order=["Total - FR", "Separate - FR", "Common - FR"], 
             linewidth=2, palette=color_order, ci=None, ax=axs[1], markers = markers, legend=None)

sns.lineplot(data=df_MS, x="abs_delta_VA", y="flipRec", hue="ComSourLbl", style="ComSourLbl", 
             hue_order=["Total - CI_MS", "Separate - CI_MS", "Common - CI_MS"], style_order=["Total - CI_MS", "Separate - CI_MS", "Common - CI_MS"], 
             linewidth=2, palette=color_order, ci=None, ax=axs[2], markers = markers, legend=None)

sns.lineplot(data=df_MA, x="abs_delta_VA", y="flipRec", hue="ComSourLbl", style="ComSourLbl", 
             hue_order=["Total - CI_MA", "Separate - CI_MA", "Common - CI_MA"], style_order=["Total - CI_MA", "Separate - CI_MA", "Common - CI_MA"], 
             linewidth=2, palette=color_order, ci=None, ax=axs[3], markers = markers, legend=None)

# count plots
# sns.lineplot(data = df_FR[df_FR.ComSourLbl=="Common - FR"], x="abs_delta_VA", y = 'ratio',  color='gray', linewidth=2, ax=axs[4], linestyle = ":", label = 'Simulation')
# sns.lineplot(data = count[count.ComSourLbl=="Common"], x="abs_delta_VA", y = 'ratio', color = 'gray', linewidth=2, ax=axs[4], label = 'Behavior')

# make invisible some edges
for ax in axs:
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(5))

for ax in axs[:4]:
    ax.set_xlabel('')
    ax.set_ylabel('Bias (\u00B0)')
    ax.xaxis.set_ticklabels([])
    #ax.tick_params(axis='x', which='major', pad=1)

axs[0].text(0.03, 0.88, 'Behavior', transform=axs[0].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
axs[1].text(0.03, 0.88, 'Sensory Cue Conflict', transform=axs[1].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
axs[2].text(0.03, 0.88, 'Causal Inference (MS)', transform=axs[2].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
axs[3].text(0.03, 0.88, 'Causal Inference (MA)', transform=axs[3].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white'))

axs[3].set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 12)
#axs[4].set_ylabel(r'% $C = 1$', fontsize = 12)

axs[0].legend(title='', loc = 'lower center', ncol=3, fontsize = 12, bbox_to_anchor=(0.25,-4.4), frameon=False)
#axs[3].legend(title='', loc = 'lower center', fontsize = 12, bbox_to_anchor=(0.75, -1.8), ncol = 2, frameon=False)

# Adjust layout
plt.subplots_adjust(top=0.95, bottom=0.15, left = 0.1, right = 0.95)
 
# Save the plot
plt.savefig(os.path.join(work_path, "Aanlysis/output/beh_sim_new_color.png"), dpi=360)  # Adjust dpi for print quality
plt.show()

