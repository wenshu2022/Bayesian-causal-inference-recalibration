import pandas as pd
import numpy as np
import os
# import matplotlib.pyplot as plt
# import seaborn as sns
#from sklearn.linear_model import LinearRegression
#from scipy import stats
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts/"
data_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction/force_zero'
os.chdir(work_path)
from help_function import *

sns.set_theme(style="white")

sub_id = 45
m_id = 109

df_sim, mean_data_all = process_force0_data(m_id,sub_id, 'ConfLbl', 0)

## plot recalibration
hue_order = [ "High", "Medium", "Low"]
color_map = {"Common": 'red', "Separate" : 'blue'}

def plotAvgRec(df_mean, sel, ax):
    sns.lineplot(data = df_mean.loc[df_mean.ComSourLbl==sel], x = "delta_VA", y = "rec", style = "ConfLbl",  color = color_map[sel], 
                        style_order= hue_order,  linewidth=2,  errorbar='se', ax = ax)

fig, axs = plt.subplots(nrows = 1, ncols = 2)
plotAvgRec(mean_data_all, 'Common', axs[0])
plotAvgRec(mean_data_all, 'Separate', axs[1])
for ax in axs:
    ax.set_ylabel('')
    ax.set_xlabel('V-A, degree', fontsize = fontsize)
    clean_axs(ax)
axs[1].set_title('Separate', fontsize = fontsize)
axs[0].set_title('Common', fontsize = fontsize)
axs[0].set_ylabel('Recalibration', fontsize = fontsize)

plt.show()


sns.lineplot(data = mean_data_all, x = "delta_VA", y = "rec",   hue = "ComSourLbl", palette=["red", "blue"], 
                    hue_order= ["Common", "Separate"],  linewidth=2,  errorbar='se')
plt.show()

####################################
# add jitter to the data so that the distribution is more obvious

# hue_order = [ "High", "Medium", "Low"]
# color_map = {"Common": 'red', "Separate" : 'blue'}
markers = ['o', 's'] 
# Create a LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('custom_cmap', [ 'blue', 'red']) # from blue (Separate) to red (High)
norm = plt.Normalize(min(df_sim.prob_conf), max(df_sim.prob_conf))

# df_sim['bi_xA_p'] = df_sim['bi_xA'] * df_sim['prob_or']
# df_sim['bi_sA_hat_p'] = df_sim['bi_sA_hat'] * df_sim['prob_or']

def plotconfdist(df , df_mean, sel, ax, dotVar):
    
    #cmap = LinearSegmentedColormap.from_list('custom_cmap', cmap_map[dotVar]) # from blue (Separate) to red (High)
    if dotVar == 'bi_xA':
        sns.lineplot(data = df_mean.loc[df_mean.ComSourLbl==sel], x = "delta_VA", y = "bi_sA_hat", style = "ConfLbl",  color = 'black', 
                      style_order= hue_order,  linewidth=2,  errorbar=None, ax = ax, legend = None)
        sns.lineplot(data = df_mean.loc[df_mean.ComSourLbl==sel], x = "delta_VA", y = "bi_xA",  style = "ConfLbl",  color = color_map[sel], style_order= hue_order, 
                    linewidth=2,   errorbar=None, ax = ax, legend = None)
        # sns.lineplot(data = df_mean.loc[df_mean.ComSourLbl==sel], x = "delta_VA", y = "rec",  style = "ConfLbl",  color = color_map[sel], style_order= hue_order, 
        #             linewidth=2,   errorbar=None, ax = ax, legend = None)
        #cmap = LinearSegmentedColormap.from_list('custom_cmap', [ 'blue', 'red']) # from blue (Separate) to red (High)
        pcm1 = ax.scatter(df.loc[(df.ConfLbl == 'High') & (df.ComSourLbl==sel), 'delta_VA'] + 1, df.loc[(df.ConfLbl == 'High') & (df.ComSourLbl==sel), dotVar], 
                            c=df.loc[(df.ConfLbl == 'High') & (df.ComSourLbl==sel), 'prob_conf'], cmap=cmap, norm=norm,  s = 0.1)
        ax.scatter(df.loc[(df.ConfLbl == 'Medium') & (df.ComSourLbl==sel), 'delta_VA'], df.loc[(df.ConfLbl == 'Medium') & (df.ComSourLbl==sel), dotVar], 
                            c=df.loc[(df.ConfLbl == 'Medium') & (df.ComSourLbl==sel), 'prob_conf'], cmap=cmap, norm=norm,  s = 0.1)
        ax.scatter(df.loc[(df.ConfLbl == 'Low') & (df.ComSourLbl==sel), 'delta_VA'] - 1, df.loc[(df.ConfLbl == 'Low') & (df.ComSourLbl==sel), dotVar], 
                            c=df.loc[(df.ConfLbl == 'Low') & (df.ComSourLbl==sel), 'prob_conf'], cmap=cmap, norm=norm,  s = 0.1)
        return pcm1
    else:    
        ax.scatter(df.loc[(df.ConfLbl == 'High') & (df.ComSourLbl==sel), 'delta_VA'] + 1, df.loc[(df.ConfLbl == 'High') & (df.ComSourLbl==sel), dotVar], 
                             color = 'black',  s = 0.1)
        ax.scatter(df.loc[(df.ConfLbl == 'Medium') & (df.ComSourLbl==sel), 'delta_VA'], df.loc[(df.ConfLbl == 'Medium') & (df.ComSourLbl==sel), dotVar], 
                            color = 'black',  s = 0.1)
        ax.scatter(df.loc[(df.ConfLbl == 'Low') & (df.ComSourLbl==sel), 'delta_VA'] - 1, df.loc[(df.ConfLbl == 'Low') & (df.ComSourLbl==sel), dotVar], 
                             color = 'black',  s = 0.1)
    
    ax.set_title(sel)
    ax.set_xlabel('location')
    ax.set_ylabel('V-A, degree')

    
        
fig = plt.figure(figsize=(8, 8))
gs = fig.add_gridspec(1, 3, width_ratios=[1,1, 0.1])
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1], sharey = ax1)
cax = fig.add_subplot(gs[0, 2])
#plt.subplots_adjust(hspace=0.1,wspace=0.05)
#sel='Common'
pcm1 = plotconfdist(df_sim, mean_data_all, 'Separate', ax1, 'bi_xA')
plotconfdist(df_sim, mean_data_all, "Common", ax2, 'bi_xA')

cbar = plt.colorbar(pcm1, cax=cax, label=r'$P(C=1|x_A, x_V)$')
# Create custom legend handles
custom_legend_handles = [mlines.Line2D([], [], color='black', linestyle='-'),
                        mlines.Line2D([], [], color='black', linestyle='--'),
                        mlines.Line2D([], [], color='black', linestyle=':'),
                        mlines.Line2D([], [], color='black', marker='o', linestyle=''),
                        mlines.Line2D([], [], color=color_map['Common'], linestyle='-'), 
                        mlines.Line2D([], [], color=color_map['Common'], linestyle='--'), 
                        mlines.Line2D([], [], color=color_map['Common'], linestyle=':'), 
                        mlines.Line2D([], [], color=color_map['Common'], marker='o', linestyle=''),
                        mlines.Line2D([], [], color=color_map['Separate'], linestyle='-'), 
                        mlines.Line2D([], [], color=color_map['Separate'], linestyle='--'), 
                        mlines.Line2D([], [], color=color_map['Separate'], linestyle=':'), 
                        mlines.Line2D([], [], color=color_map['Separate'], marker='o', linestyle='')]
row_labels = [
    mlines.Line2D([], [], linestyle='', marker=''),
    mlines.Line2D([], [], linestyle='', marker=''),
    mlines.Line2D([], [], linestyle='', marker=''),
    mlines.Line2D([], [], linestyle='', marker='')]
all_handles = row_labels + custom_legend_handles
all_labels = [r'$High \quad confidence :$' , r'$Medium \quad confidence :$', r'$Low \quad confidence :$', r'$\quad$', 
            r'$mean(\hat{S}_{A,AV} * p_{C1})$', r'$mean(\hat{S}_{A,AV}* p_{C1}))$', r'$mean(\hat{S}_{A,AV}* p_{C1}))$', r'$\hat{S}_{A,AV}$', 
            r'$mean(x_{A,AV}* p_{C1}))$', r'$mean(x_{A,AV}* p_{C1}))$',  r'$mean(x_{A,AV}* p_{C1}))$', r'$x_{A,AV}$', 
            r'$mean(x_{A,AV}* p_{C1}))$', r'$mean(x_{A,AV}* p_{C1}))$',  r'$mean(x_{A,AV}* p_{C1}))$', r'$x_{A,AV}$']
# all_labels = [r'$High \quad confidence :$' , r'$Medium \quad confidence :$', r'$Low \quad confidence :$', r'$\quad$', 
#             r'$mean(\hat{S}_{A,AV})$', r'$mean(\hat{S}_{A,AV})$', r'$mean(\hat{S}_{A,AV})$', r'$\hat{S}_{A,AV}$', 
#             r'$mean(x_{A,AV}^{})$', r'$mean(x_{A,AV}^{})$',  r'$mean(x_{A,AV}^{})$', r'$x_{A,AV}$', 
#             r'$mean(x_{A,AV}^{})$', r'$mean(x_{A,AV}^{})$',  r'$mean(x_{A,AV}^{})$', r'$x_{A,AV}$']
fig.legend(handles=all_handles, 
        labels=all_labels,
        ncol=4, fontsize=fontsize, bbox_to_anchor=(0.5, -0.02), loc='lower center', frameon=False)

for ax in [ax1, ax2]:
    ax.set_ylabel('')
    ax.set_xlabel('V-A, degree', fontsize = fontsize)
    clean_axs(ax)
ax1.set_title('Separate', fontsize = fontsize)
ax2.set_title('Common', fontsize = fontsize)
ax1.set_ylabel('location', fontsize = fontsize)
#fig.suptitle(sel, fontsize = fontsize)
fig.subplots_adjust(bottom = 0.3)
#plt.savefig(os.path.join(work_path, "plot4paper", "conf_dist_" + sel + ".png"), dpi=300)  # Adjust dpi for print quality
plt.show()



# hue_order = [ "Separate", "Common"]
# color_order = [ 'blue', 'red']
# markers = ['o', 's'] 
# # Create a LinearSegmentedColormap
# cmap = LinearSegmentedColormap.from_list('custom_cmap', [ 'blue', 'red']) # from blue (Separate) to red (High)
# norm = plt.Normalize(min(df_sim.prob_dec), max(df_sim.prob_dec))
# ##### distribution figure
# fig = plt.figure(figsize=(6, 6))
# gs = fig.add_gridspec(1, 2,width_ratios = [1, 0.1], wspace=0.4) 

# axs00 = fig.add_subplot(gs[0])
# #cmap = LinearSegmentedColormap.from_list('custom_cmap', cmap_map[dotVar]) # from blue (Separate) to red (High)
# pcm1 = axs00.scatter(df_sim.loc[df_sim.ComSourLbl == 'Common', 'delta_VA'] + 0.5, df_sim.loc[df_sim.ComSourLbl == 'Common', 'bi_xA'], 
#                     c=df_sim.loc[df_sim.ComSourLbl == 'Common', 'prob_dec'], cmap=cmap, norm=norm,  s = 0.1)
# axs00.scatter(df_sim.loc[df_sim.ComSourLbl != 'Common', 'delta_VA'] - 0.5, df_sim.loc[df_sim.ComSourLbl != 'Common', 'bi_xA'], 
#                     c=df_sim.loc[df_sim.ComSourLbl != 'Common', 'prob_dec'], cmap=cmap, norm=norm,  s = 0.1)

# sns.lineplot(data = mean_data_all, x = "delta_VA", y = "bi_sA_hat", hue = "ComSourLbl", hue_order = hue_order, 
#              dashes = False, palette = color_order,  linewidth=2,  errorbar=None, ax = axs00, legend = None)
# sns.lineplot(data = mean_data_all, x = "delta_VA", y = "bi_xA", hue = "ComSourLbl", hue_order = hue_order,  
#              linestyle="--", palette = color_order, linewidth=2,   errorbar=None, ax = axs00, legend = None)
    
# # Colorbar
# cax = fig.add_subplot(gs[1])
# cbar = plt.colorbar(pcm1, cax=cax)
# cbar.set_label(r'$P(C=1|x_{A,AV},x_{V,AV})$', fontsize=fontsize)  # Adjust label font size
# cbar.ax.tick_params(labelsize=fontsize)  

# custom_legend_handles = [mlines.Line2D([], [], color='red', linestyle='-'),
#                          mlines.Line2D([], [], color='blue', linestyle='-'),
#                          mlines.Line2D([], [], color='red', linestyle='--'), 
#                          mlines.Line2D([], [], color='blue', linestyle='--'), 
#                          mlines.Line2D([], [], color='red', marker='o', linestyle=''),
#                          mlines.Line2D([], [], color='blue', marker='o', linestyle='')]
# # Define the row labels (invisible)
# row_labels = [
#     mlines.Line2D([], [], linestyle='', marker=''),
#     mlines.Line2D([], [], linestyle='', marker='')
# ]
# # Combine row labels and custom legend handles
# all_handles = row_labels + custom_legend_handles
# all_labels = [r'$P(C=1|x_{A,AV},x_{V,AV})>0.5$' + ' :', r'$P(C=1|x_{A,AV},x_{V,AV}) \leq 0.5$' + ' :', 
#               r'$mean(\hat{S}_{A,AV})$', r'$mean(\hat{S}_{A,AV})$', 
#               r'$mean(x_{A,AV})$', r'$mean(x_{A,AV})$',  
#               r'$x_{A, AV}$', r'$x_{A, AV}$']
# fig.legend(handles=all_handles, 
#            labels=all_labels,
#            ncol=4, fontsize=fontsize, bbox_to_anchor=(0.45, -0.01), loc='lower center', frameon=False)

# axs00.set_ylabel('Spatial location (\u00B0)', fontsize = fontsize)
# axs00.set_xlabel('V-A, degree', fontsize = fontsize)
# clean_axs(axs00)
# fig.subplots_adjust(hspace=0.2, wspace=0.4, bottom=0.25,top = 0.9, left = 0.1,  right = 0.9)

# plt.show()