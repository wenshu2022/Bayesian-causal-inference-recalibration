# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:04:09 2024

@author: wenlou
"""
import pandas as pd
import numpy as np
import os
import matplotlib.patches as mpatches
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
data_path = "P:/3026008.01/Data/"
os.chdir(work_path)
from help_function import *
import json


#read subject list 
sub_id_lst = read_sub_lst()

model_config = pd.read_excel('M:/MATLAB/Model/m_config.xlsx')
metrics = 'BIC'
m_score = pd.read_csv('M:/MATLAB/Model/check_performance/AIC_BIC_update.csv')

# search for model config in the table
m_lst = m_score.m_id.unique()

m_conf_sel = model_config[model_config.m_id.isin(m_lst)].reset_index(drop = True)
m_conf_sel.columns

# model components:
    # recalibration type - shift_update : CIMA or CIMS or SCC
    # causal decision/confidence read-out - C_readout : p or xDiff

# concat the labels
m_score = m_score.merge(m_conf_sel[['shift_update', 'C_readout', 'AV_readout','Conf_readout', 'm_id']], how = 'outer', on = 'm_id')
m_score.loc[m_score['shift_update']=='CI', 'Recal_model'] = m_score.loc[m_score['shift_update']=='CI', 'shift_update'].str.replace('CI', 'Bay')  + m_score.loc[m_score['shift_update']=='CI', 'AV_readout']
m_score.loc[m_score['shift_update']!='CI', 'Recal_model'] = m_score.loc[m_score['shift_update']!='CI', 'shift_update'].str.replace('FR', 'xDiff') 
m_score['C_readout'] = m_score['C_readout'].str.replace('p','Bay').str.replace('xdiff', 'xDiff')
m_score['Conf_readout'] = m_score['Conf_readout'].str.replace('p','Bay').str.replace('xdiff', 'xDiff')
m_score['label'] =  m_score['C_readout'] + '-' + m_score['Conf_readout']
m_score.sort_values(by = ['sub_id', 'label', 'Recal_model'], ascending=False, inplace = True)
m_score.label=pd.Categorical(m_score.label,categories=m_score['label'].unique())

# compute the BIC difference - baseline model is SCC-xDiff-xDiff
ref_BIC = m_score[(m_score.Recal_model=='xDiff') & (m_score.C_readout=='xDiff') & (m_score.Conf_readout=='xDiff')].copy()
ref_BIC.rename(columns = {'BIC':'refBIC'}, inplace = True)
m_score = m_score.merge(ref_BIC[['sub_id', 'refBIC']], how = 'outer', on = 'sub_id')
m_score['BICdiff'] = m_score['refBIC'] - m_score['BIC']

### load in the bayesian comparison results
with open('./Figure2-modelCompare/bms_fac_BIC.json', 'r') as f:
    bms_fac_BIC = json.load(f)  # Load the JSON as a Python dictionary
    
fnames = {"Recalibration model" : ["xDiff", "BayMA", "BayMS"], 
                "Causal decision" : ["Bay", "xDiff"], 
                "Causal confidence" : ["Bay", "xDiff"]}

flist = ["Recalibration model", "Causal decision",  "Causal confidence"]

###################################################################################
fig = plt.figure(figsize=(12, 10))
gs = fig.add_gridspec(3, 4, height_ratios = [4, 1, 2], width_ratios = [3.8, 3, 3, 2], hspace=0.2, wspace=0.4) 
fontsize = 16

ax1 = fig.add_subplot(gs[0, :3])
# box plot with lines overlay
hue_order = ['xDiff', 'BayMS', 'BayMA']
color_order = ['#a64dff', '#555555', '#3333FF']
boxplot = sns.boxplot(data = m_score, 
                      x= "label", 
                      y='BICdiff', 
                      order=m_score['label'].unique(),
                      hue = 'Recal_model', 
                      hue_order = hue_order, 
                      gap=.1, 
                      linecolor = 'black', 
                      linewidth = 0.5, 
                      palette = color_order, 
                      legend = None, 
                      ax = ax1)
# Adjust the transparency of the first two boxes
for i, artist in enumerate(boxplot.patches):
    if i in [0, 1, 4, 5, 8, 9]:  
        artist.set_alpha(0.4)  
    if i in [1, 3, 5, 7, 9, 11]:
        artist.set_edgecolor('black')  # Add black borders to boxes
        artist.set_linewidth(3)

# get the a positions and x labels for each model
x_positions = ax1.get_xticks()            # Numeric positions on the x-axis
x_labels = [tick.get_text() for tick in ax1.get_xticklabels()]  # Corresponding label names
x_poses = [[pos-0.25, pos, pos+0.25] for pos in x_positions ]
x_poses_flat = sum((pos for pos in x_poses), [])
# # add lines for each individuals
for sub_id in sub_id_lst:
    sub_data = m_score.loc[(m_score.sub_id==sub_id)]
    sub_data.label=pd.Categorical(sub_data.label,categories=x_labels)
    ax1.plot(x_poses_flat,  sub_data['BICdiff'], color='grey', lw=0.3, alpha=0.7)


 # Create custom legend handles
ax1_le = fig.add_subplot(gs[0, 3])

leg_handles = [
    mpatches.Patch(facecolor=color_order[0], linewidth=0.5, edgecolor='black', label='xDiff'),
    mpatches.Patch(facecolor=color_order[1], linewidth=0.5, edgecolor='black', label='BayMS'),
    mpatches.Patch(facecolor=color_order[2], linewidth=0.5, edgecolor='black', label='BayMA'),
]

# Add legend with a title
ax1_le.legend(
    handles=leg_handles,
    ncol=1,
    prop={'family': 'Arial', 'style': 'normal', 'size': fontsize},
    fontsize=fontsize,
    bbox_to_anchor=(1.5, 0.5),
    loc='right',
    frameon=False,
    title="Recalibration models:",  # Adding a title
    title_fontsize=fontsize,  # Ensure title uses the same font size
)

# bayesian comparison three plots
axs2 =[None, None, None]
axs2[0] = fig.add_subplot(gs[2, 0])
axs2[1] = fig.add_subplot(gs[2, 1], sharey=axs2[0])
axs2[2] = fig.add_subplot(gs[2, 2], sharey=axs2[0])

for f_id in range(3):

    # Bar plot
    pxp_value = bms_fac_BIC[f_id]['pxp'][0]
    axs2[f_id].bar(fnames[flist[f_id]], 
                   bms_fac_BIC[f_id]['pxp'], 
                   width=0.4, 
                   color='k')

    # Error bar plot
    exp_r_value = bms_fac_BIC[f_id]['exp_r']
    errh = np.sqrt(np.diag(bms_fac_BIC[f_id]['cov_r']))
    axs2[f_id].errorbar(
        fnames[flist[f_id]],
        exp_r_value,
        yerr=errh,
        fmt='-s',
        markersize=8,
        linestyle='',
        color=[0.7, 0.7, 0.7]
    )
    # axs2[f_id].spines['top'].set_visible(False)
    # axs2[f_id].spines['right'].set_visible(False)
    # axs2[f_id].tick_params(axis='both', which='major', direction='in', left=True, bottom=True, labelsize=16)
    axs2[f_id].set_title(flist[f_id], fontsize = fontsize)

# Create custom legend handles
ax2_le = fig.add_subplot(gs[2, 3])
leg_handles = [mlines.Line2D([], [], color=[0.7, 0.7, 0.7], linestyle='-', marker = 's'),
               mpatches.Patch(color = 'black')]
leg_labels = ['Posterior frequencies', 'Protected exceedance \n probability']
ax2_le.legend(leg_handles, leg_labels, ncol=1, prop = {'family':'Arial','style':'normal', 'size' : fontsize}, fontsize=fontsize,  bbox_to_anchor=(2.25, 0.5), loc='right', frameon=False)


for ax in [ax1] + axs2[:]:
    ax.spines[['top', 'right']].set_visible(False)
    ax.tick_params(axis='both', which='major', direction='in', left=True, bottom=True, labelfontfamily = 'Arial', labelsize=fontsize)
    ax.set_xlabel('')
    ax.set_ylabel('')
    
ax1.set_xticks([])
    

for ax in [ax1_le, ax2_le]:
    ax.spines[:].set_visible(False)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_xticks([])
    ax.set_yticks([])

ax1.set_ylabel('Relative BIC', fontsize = fontsize)
#ax1.set_ylabel('BIC differences', fontsize = fontsize)
axs2[0].set_ylabel('Probability', fontsize = fontsize)

plt.savefig(os.path.join(work_path, "plot4paper/model_compare_big.png"), dpi=300, bbox_inches='tight')  # Adjust dpi for print quality
plt.show()




