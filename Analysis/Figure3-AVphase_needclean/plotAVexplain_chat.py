# -*- coding: utf-8 -*-
"""
Created on Wed Mar 26 11:34:55 2025

@author: wenlou
"""

import pandas as pd
import numpy as np
import os
from matplotlib import cm
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
#import matplotlib.lines as mlines
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, PercentFormatter)
from mpl_toolkits.axes_grid1 import make_axes_locatable

# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
data_path = "C:/Users/wenlou/Documents/MATLAB/Prediction/explainAV"
#pred_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
os.chdir(work_path)
from help_function import *

sub_lst = read_sub_lst()

m_label = {'Bay-Bay': 70, 'xDiff-xDiff': 74}
extent = (-12, 12, 12, -12)
#prepare datas

# process data
# df_sim = pd.read_csv(os.path.join(data_path, 'pred_explainAV_m_' + str(m_label['Bay-Bay']) + '.csv')) 
# #update common judgement to 0 - separate, 1 - common
# df_sim['R_pc'] = 2 - df_sim['R_pc']
# agg_chat = df_sim.groupby(['s_a', 's_v'])[['R_pc']].mean().reset_index()
#average of all prediction data.
sub_id = 38
sub_lst = [sub_id]
df_sim_bay = processPredDat(70, sub_lst)
df_sim_bay['R_pc'] = 2 - df_sim_bay['R_pc']

df_sim_xdiff = processPredDat(74, sub_lst)
df_sim_xdiff['R_pc'] = 2 - df_sim_xdiff['R_pc']

def avg_z(df, varC, varConf, n=4):
    agg_bysub = df.groupby(['s_a', 's_v', 'sub_id'])[[varC, varConf]].mean().reset_index()
    agg = agg_bysub.groupby(['s_a', 's_v'])[[varC, varConf]].mean().reset_index()
    Z_bay = agg[varC].values.reshape(n, -1).T
    Zconf_bay = agg[varConf].values.reshape(n, -1).T
    return Z_bay, Zconf_bay

Z_bay, Zconf_bay = avg_z(df_sim_bay, 'R_pc', 'R_conf')
Z_bay_com, Zconf_bay_com = avg_z(df_sim_bay.loc[df_sim_bay.R_pc==1], 'R_pc', 'R_conf')
Z_bay_sep, Zconf_bay_sep = avg_z(df_sim_bay.loc[df_sim_bay.R_pc==0], 'R_pc', 'R_conf')

Z_xdiff, Zconf_xdiff = avg_z(df_sim_xdiff, 'R_pc', 'R_conf')
Z_xdiff_com, Zconf_xdiff_com = avg_z(df_sim_xdiff.loc[df_sim_xdiff.R_pc==1], 'R_pc', 'R_conf')
Z_xdiff_sep, Zconf_xdiff_sep = avg_z(df_sim_xdiff.loc[df_sim_xdiff.R_pc==0], 'R_pc', 'R_conf')


# beh
df_beh = processBehDat()
df_beh['ComSourFlag'] = 2 - df_beh['ComSourFlag']
#df_beh = df_beh.loc[df_beh.sub_id == 45]#10
Z_beh, Zconf_beh = avg_z(df_beh, 'ComSourFlag','confLvl')
Z_beh_com, Zconf_beh_com = avg_z(df_beh.loc[(df_beh.ComSourFlag==1)&(df_beh.sub_id==sub_id)], 'ComSourFlag','confLvl')
Z_beh_sep, Zconf_beh_sep = avg_z(df_beh.loc[(df_beh.ComSourFlag==0)&(df_beh.sub_id==sub_id)], 'ComSourFlag','confLvl')

# agg_beh_bysub = df_beh.groupby(['s_a', 's_v', 'sub_id'])[['ComSourFlag','confLvl']].mean().reset_index()
# agg_beh = agg_beh_bysub.groupby(['s_a', 's_v'])[['ComSourFlag','confLvl']].mean().reset_index()
# Z_beh = agg_beh['ComSourFlag'].values.reshape(4, -1).T
# Zconf_beh = agg_beh['confLvl'].values.reshape(4, -1).T

norm_c = cm.colors.Normalize(vmax=1, vmin=0)
norm_conf = cm.colors.Normalize(vmax=3, vmin=1)
new_cmap = cm.viridis(np.linspace(0, 1, 256))
custom_cmap = LinearSegmentedColormap.from_list("viridis_low", new_cmap)
fig, _axs = plt.subplots(figsize = (16, 10), nrows=2, ncols=3)
fig.subplots_adjust(hspace=0.3, wspace = 0.3, left=0.05, right = 0.95, top=0.9, bottom = 0.1)
axs = _axs.flatten()

#c =  [None, None, None, None ]
im = [None, None, None, None , None, None]
cbar=[None, None, None, None , None, None]

def plot_t():
    im[0] = axs[0].imshow(Z_beh, extent=extent, interpolation= None, cmap=cm.Spectral.reversed(), norm = norm_c)
    ylim = axs[0].get_ylim()
    im[1]=axs[1].imshow(Z_bay, extent = extent, interpolation = None, cmap= cm.Spectral.reversed(), norm = norm_c)
    im[2]=axs[2].imshow(Zconf_beh, extent=extent, interpolation=None, cmap=custom_cmap, norm = norm_conf)
    im[3]=axs[3].imshow(Zconf_bay, extent = extent, interpolation = None, cmap= custom_cmap, norm = norm_conf)
    return ylim
def set_labl_t():
    cbar[0].set_label(r'$mean(C_{report})$', fontsize=16)   
    cbar[3].set_label(r'$mean(\hat{conf})$', fontsize=16)  
    cbar[1].set_label(r'$mean(\hat{C})$', fontsize=16)   
    cbar[2].set_label(r'$mean(conf_{report})$', fontsize=16) 

def plot_com_sep():
    im[0] = axs[0].imshow(Zconf_beh_com, extent=extent, interpolation= None, cmap=cm.viridis, norm = norm_conf)
    ylim = axs[0].get_ylim()
    im[1]=axs[1].imshow(Zconf_bay_com, extent = extent, interpolation = None, cmap= cm.viridis, norm = norm_conf)
    im[2]=axs[2].imshow(Zconf_xdiff_com, extent = extent, interpolation = None, cmap= cm.viridis, norm = norm_conf)
    im[3]=axs[3].imshow(Zconf_beh_sep, extent=extent, interpolation=None, cmap=cm.viridis, norm = norm_conf)
    im[4]=axs[4].imshow(Zconf_bay_sep, extent = extent, interpolation = None, cmap= cm.viridis, norm = norm_conf)
    im[5]=axs[5].imshow(Zconf_xdiff_sep, extent = extent, interpolation = None, cmap= cm.viridis, norm = norm_conf)
    return ylim
def set_labl_both():
    cbar[0].set_label(r'$mean(conf_{report})$', fontsize=16) 
    cbar[4].set_label(r'$mean(\hat{conf})$', fontsize=16)  
    cbar[1].set_label(r'$mean(\hat{conf})$', fontsize=16)  
    cbar[2].set_label(r'$mean(\hat{conf})$', fontsize=16) 
    cbar[3].set_label(r'$mean(conf_{report})$', fontsize=16) 
    cbar[5].set_label(r'$mean(\hat{conf})$', fontsize=16)  

ylim = plot_com_sep() 
for i in np.arange(6):
    divider = make_axes_locatable(axs[i])
    cax = divider.append_axes("right", size="5%", pad=0.1)  # Adjust size and padding
    cbar[i] = fig.colorbar(im[i], cax= cax)
    cbar[i].ax.tick_params(labelsize=16)

for ax in axs:
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(4))
    ax.tick_params(axis='both', which='major', direction='out', left=True, bottom=True, labelsize=16)
    ax.set_ylim(ylim[::-1])
    ax.set_xlabel(r'$S_{A,AV}$',fontsize = 16)
    ax.set_ylabel(r'$S_{V,AV}$',fontsize = 16, labelpad=1)
set_labl_both()
#plt.savefig(os.path.join(work_path, 'plot4paper', 'AV_explain_chat.png'), dpi=300)
plt.show()


ylim = plot_t() 
for i in np.arange(4):
    divider = make_axes_locatable(axs[i])
    cax = divider.append_axes("right", size="5%", pad=0.1)  # Adjust size and padding
    cbar[i] = fig.colorbar(im[i], cax= cax)
    cbar[i].ax.tick_params(labelsize=16)

for ax in axs:
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(4))
    ax.tick_params(axis='both', which='major', direction='out', left=True, bottom=True, labelsize=16)
    ax.set_ylim(ylim[::-1])
    ax.set_xlabel(r'$S_{A,AV}$',fontsize = 16)
    ax.set_ylabel(r'$S_{V,AV}$',fontsize = 16, labelpad=1)
set_labl_t()
#plt.savefig(os.path.join(work_path, 'plot4paper', 'AV_explain_chat.png'), dpi=300)
plt.show()