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
os.chdir(work_path)
from help_function import *
data_path = "C:/Users/wenlou/Documents/MATLAB/Prediction/explainAV"
#pred_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'

m_label = {'Bay-Bay': 70, 'xDiff-xDiff': 74}

#prepare data

# the image value is the mean prob
delta = 0.5    
sa = np.arange(-12.0, 12.001, delta)
SA, SV = np.meshgrid(sa, sa)
extent = (-12, 12, 12, -12)

# process sim data
df_sim = pd.read_csv(os.path.join(data_path, 'pred_explainAV_m_' + str(m_label['Bay-Bay']) + '.csv')) 
agg_prob = df_sim.groupby(['s_a', 's_v'])[['prob']].mean().reset_index()
Z_bay = agg_prob['prob'].values.reshape(49, -1).T
Zconf_bay = np.maximum(Z_bay, 1-Z_bay)
Zconfcom_bay = np.where(Z_bay>0.5, Z_bay, np.nan)
Zconfsep_bay = np.where(Z_bay<=0.5, 1-Z_bay, np.nan)

df_sim = pd.read_csv(os.path.join(data_path, 'pred_explainAV_m_' + str(m_label['xDiff-xDiff']) + '.csv')) 
df_sim['xdiff'] = abs(df_sim['bi_xA'] - df_sim['bi_xV'])
agg_xdiff = df_sim.groupby(['s_a', 's_v'])[['xdiff']].mean().reset_index()
epsilon = 11
Z_xdiff = epsilon - agg_xdiff['xdiff'].values.reshape(49, -1).T
Zconf_xdiff = abs(Z_xdiff)
Zconfcom_xdiff = np.where(Z_xdiff>0, Z_xdiff, np.nan) 
Zconfsep_xdiff = np.where(Z_xdiff<=0, -Z_xdiff, np.nan) 

# process beh data 
def avg_z(df, varC, varConf, n=4):
    agg_bysub = df.groupby(['s_a', 's_v', 'sub_id'])[[varC, varConf]].mean().reset_index()
    agg = agg_bysub.groupby(['s_a', 's_v'])[[varC, varConf]].mean().reset_index()
    Z_bay = agg[varC].values.reshape(n, -1).T
    Zconf_bay = agg[varConf].values.reshape(n, -1).T
    return Z_bay, Zconf_bay

df_beh = processBehDat()
df_beh['ComSourFlag'] = 2 - df_beh['ComSourFlag']
#df_beh = df_beh.loc[df_beh.sub_id == 45]#10
Z_beh, Zconf_beh = avg_z(df_beh, 'ComSourFlag','confLvl')
Z_beh_com, Zconf_beh_com = avg_z(df_beh.loc[df_beh.ComSourFlag==1], 'ComSourFlag','confLvl')
Z_beh_sep, Zconf_beh_sep = avg_z(df_beh.loc[df_beh.ComSourFlag==0], 'ComSourFlag','confLvl')


fig, _axs = plt.subplots(figsize = (18, 10), nrows=2, ncols=3)
fig.subplots_adjust(hspace=0.3, wspace = 0.3, left=0.05, right = 0.95, top=0.9, bottom = 0.1)
axs = _axs.flatten()

#norm_prob = cm.colors.Normalize(vmax=max(abs(Z_bay).max(), abs(Zconf_bay).max()), vmin=min(abs(Z_bay).min(), abs(Zconf_bay).min()))
#norm_xdiff = cm.colors.Normalize(vmax=max(abs(Z_xdiff).max(), abs(Zconf_xdiff).max()), vmin=min(abs(Z_xdiff).min(), abs(Zconf_xdiff).min()))
cmap = cm.Spectral  

c =  [None]*6
im = [None]*6
cbar=[None]*6

im[0] = axs[0].imshow(Z_beh, extent=extent, interpolation= None, cmap=cm.Spectral.reversed(), norm = cm.colors.Normalize(vmax=1, vmin=0))
ylim = axs[0].get_ylim()

c[1] = axs[1].contour(SA, SV, Z_bay, (0.5, ),  colors='k', linewidths=2)
im[1] = axs[1].imshow(Z_bay, extent=extent, interpolation='bilinear', cmap=cm.Spectral.reversed(), norm = cm.colors.Normalize(vmax=1, vmin=0))
# ylim = axs[0].get_ylim()

c[2]=axs[2].contour(SA, SV, Z_xdiff, (0,), colors = 'k', linewidths= 2)
im[2]=axs[2].imshow(Z_xdiff, extent = extent, interpolation = 'bilinear', cmap= cm.Spectral.reversed())

im[3]=axs[3].imshow(Zconf_beh, extent=extent, interpolation=None, cmap=cm.viridis, norm = cm.colors.Normalize(vmax=3, vmin=1))

c[4] = axs[4].contour(SA, SV, Zconf_bay, (0.58,  0.75 ), colors='k', linewidths=2)
im[4]=axs[4].imshow(Zconf_bay, extent=extent, interpolation='bilinear', cmap=cm.viridis, norm = cm.colors.Normalize(vmax=1, vmin=0.5))

c[5]=axs[5].contour(SA, SV, Zconf_xdiff, (1, 4.2), colors = 'k', linewidths= 2)
im[5]=axs[5].imshow(Zconf_xdiff, extent = extent, interpolation = 'bilinear', cmap= cm.viridis)
#new
# im[0]=axs[0].imshow(Zconf_beh_com, extent=extent, interpolation=None, cmap=cm.viridis, norm = cm.colors.Normalize(vmax=3, vmin=1))
# ylim = axs[0].get_ylim()

# c[1] = axs[1].contour(SA, SV, Zconfcom_bay, (0.6,  0.75 ), colors='k', linewidths=2)
# im[1]=axs[1].imshow(Zconfcom_bay, extent=extent, interpolation='bilinear', cmap=cm.viridis, norm = cm.colors.Normalize(vmax=1, vmin=0.5))

# c[2]=axs[2].contour(SA, SV, Zconfcom_xdiff, (1, 4.2), colors = 'k', linewidths= 2)
# im[2]=axs[2].imshow(Zconfcom_xdiff, extent = extent, interpolation = 'bilinear', cmap= cm.viridis)

# im[3]=axs[3].imshow(Zconf_beh_sep, extent=extent, interpolation=None, cmap=cm.viridis, norm = cm.colors.Normalize(vmax=3, vmin=1))

# c[4] = axs[4].contour(SA, SV, Zconfsep_bay, (0.6,  0.75 ), colors='k', linewidths=2)
# im[4]=axs[4].imshow(Zconfsep_bay, extent=extent, interpolation='bilinear', cmap=cm.viridis.reversed())

# c[5] = axs[5].contour(SA, SV, Zconfsep_xdiff, (1, 4.2), colors='k', linewidths=2)
# im[5]=axs[5].imshow(Zconfsep_xdiff, extent=extent, interpolation='bilinear', cmap=cm.viridis.reversed())

fontsize=18
for i in np.arange(6):
    divider = make_axes_locatable(axs[i])
    cax = divider.append_axes("right", size="5%", pad=0.1)  # Adjust size and padding
    if i not in [0, 3]:
        axs[i].clabel(c[i], fontsize=fontsize)
    cbar[i] = fig.colorbar(im[i], cax= cax)
    cbar[i].ax.tick_params(labelsize=fontsize)

for ax in axs:
    ax.xaxis.set_major_locator(MultipleLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(4))
    ax.tick_params(axis='both', which='major', direction='out', left=True, bottom=True, labelsize=16)
    ax.set_ylim(ylim[::-1])
    ax.set_xlabel(r'$S_{A,AV}$',fontsize = fontsize)
    ax.set_ylabel(r'$S_{V,AV}$',fontsize = fontsize, labelpad=1)

for ax in [axs[0], axs[3]]:
    ax.set_xticks([-12, -4, 4, 12])
    ax.set_yticks([-12, -4, 4, 12])
    
cbar[0].set_label(r'$mean(C_{report})$', fontsize=fontsize) 
cbar[3].set_label(r'$mean(Conf_{report})$', fontsize=fontsize) 
cbar[1].set_label(r'$P(C=1|x_{A,AV},x_{V,AV})$', fontsize=fontsize)   
cbar[2].set_label(r'$\epsilon - |x_{A,AV} - x_{V,AV}|$', fontsize=fontsize)  
cbar[4].set_label(r'$max(P(C=1|x_{A,AV},x_{V,AV}), $' '\n\t' 
                  r'$P(C=2|x_{A,AV},x_{V,AV}))$', fontsize=fontsize)  
cbar[5].set_label(r'$abs(\epsilon - |x_{A,AV} - x_{V,AV}|)$', fontsize=fontsize)  

plt.savefig(os.path.join(work_path, 'plot4paper', 'AV_explain0417.png'), dpi=300)
plt.show()