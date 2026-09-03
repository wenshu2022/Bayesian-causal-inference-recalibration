import pandas as pd
import numpy as np
import os
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"

os.chdir(work_path)
from help_function import *

m_label = {'SCC': 87, 'BMS': 70, 'BMA': 91}

df_sim_SCC, df_mean_SCC = process_force0_data(m_label['SCC'])
df_sim_BMS, df_mean_BMS = process_force0_data(m_label['BMS'])
df_sim_BMA, df_mean_BMA = process_force0_data(m_label['BMA'])
df_mean_SCC['rec'] = 0.25* df_mean_SCC['rec']

fontsize = 18

hue_order = [ "Separate", "Common"]
color_order = [ 'blue', 'red']
# Create a LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('custom_cmap', color_order) # from blue (Separate) to red (common)
norm = plt.Normalize(0, 1)

##### distribution figure
fig = plt.figure(figsize=(14, 8))
gs = fig.add_gridspec(2, 7, height_ratios = [2,1], width_ratios = [1, 0.3, 1, 0.3, 1, 0.15, 0.05], hspace=0.2, wspace=0) 

# Plot both scatter plots
axs00 = fig.add_subplot(gs[0, 0])
pcm1 = axs00.scatter(df_sim_BMA.loc[df_sim_BMA.ComSourLbl == 'Common', 'delta_VA'] + 0.5, df_sim_BMA.loc[df_sim_BMA.ComSourLbl == 'Common', 'bi_xA'], 
                    c=df_sim_BMA.loc[df_sim_BMA.ComSourLbl == 'Common', 'prob'], cmap=cmap, norm=norm,  s = 0.1)
axs00.scatter(df_sim_BMA.loc[df_sim_BMA.ComSourLbl != 'Common', 'delta_VA'] - 0.5, df_sim_BMA.loc[df_sim_BMA.ComSourLbl != 'Common', 'bi_xA'], 
                    c=df_sim_BMA.loc[df_sim_BMA.ComSourLbl != 'Common', 'prob'], cmap=cmap, norm=norm,  s = 0.1)

sns.lineplot(data = df_mean_BMA, x = "delta_VA", y = "bi_sA_hat", hue = "ComSourLbl", hue_order = hue_order, 
             dashes = False, palette = color_order,  linewidth=2,  errorbar=None, ax = axs00, legend = None)
sns.lineplot(data = df_mean_BMA, x = "delta_VA", y = "bi_xA", hue = "ComSourLbl", hue_order = hue_order,  
             linestyle="--", palette = color_order, linewidth=2,   errorbar=None, ax = axs00, legend = None)


axs01 = fig.add_subplot(gs[0, 2], sharey=axs00)
axs01.scatter(df_sim_BMS.loc[df_sim_BMS.ComSourLbl == 'Common', 'delta_VA'] + 0.5, df_sim_BMS.loc[df_sim_BMS.ComSourLbl == 'Common', 'bi_xA'], 
                    c=df_sim_BMS.loc[df_sim_BMS.ComSourLbl == 'Common', 'prob'], cmap=cmap, norm=norm,  s = 0.1)
axs01.scatter(df_sim_BMS.loc[df_sim_BMS.ComSourLbl != 'Common', 'delta_VA'] - 0.5, df_sim_BMS.loc[df_sim_BMS.ComSourLbl != 'Common', 'bi_xA'], 
                    c=df_sim_BMS.loc[df_sim_BMS.ComSourLbl != 'Common', 'prob'], cmap=cmap, norm=norm,  s = 0.1)
sns.lineplot(data = df_mean_BMS, x = "delta_VA", y = "bi_sA_hat", hue = "ComSourLbl", hue_order = hue_order, 
             dashes = False, palette = color_order,  linewidth=2,  errorbar=None, ax = axs01, legend = None)
sns.lineplot(data = df_mean_BMS, x = "delta_VA", y = "bi_xA", hue = "ComSourLbl", hue_order = hue_order,  
             linestyle="--", palette = color_order, linewidth=2,  errorbar=None, ax = axs01, legend = None)


# without the solid line
axs02 = fig.add_subplot(gs[0, 4], sharey=axs00)
axs02.scatter(df_sim_SCC.loc[df_sim_SCC.ComSourLbl == 'Common', 'delta_VA'] + 0.5, df_sim_SCC.loc[df_sim_SCC.ComSourLbl == 'Common', 'bi_xA'], 
                    c=df_sim_SCC.loc[df_sim_SCC.ComSourLbl == 'Common', 'prob'], cmap=cmap, norm=norm,  s = 0.1)
axs02.scatter(df_sim_SCC.loc[df_sim_SCC.ComSourLbl != 'Common', 'delta_VA'] - 0.5, df_sim_SCC.loc[df_sim_SCC.ComSourLbl != 'Common', 'bi_xA'], 
                    c=df_sim_SCC.loc[df_sim_SCC.ComSourLbl != 'Common', 'prob'], cmap=cmap, norm=norm,  s = 0.1)
sns.lineplot(data = df_mean_SCC, x = "delta_VA", y = "bi_xA", hue = "ComSourLbl", hue_order = hue_order,  
             linestyle="--", palette = color_order, linewidth=2,   errorbar=None, ax = axs02, legend = None)
axs02.axhline(y=0, color='black', linestyle=':', linewidth=1.5)  # Horizontal line

axs00.set_title('BayMA-Bay-Bay',fontsize=fontsize)
axs01.set_title('BayMS-Bay-Bay',fontsize=fontsize)
axs02.set_title('xDiff-Bay-Bay',fontsize=fontsize)


# Colorbar
cax = fig.add_subplot(gs[0,6])
cbar = plt.colorbar(pcm1, cax=cax)
cbar.set_label(r'$P(C=1|x_{A,AV},x_{V,AV})$', fontsize=fontsize)  # Adjust label font size
cbar.ax.tick_params(labelsize=fontsize)
#cax.set_title("Spatial disparity (V - A , visual angle \u00B0)", fontsize=fontsize)

# three plots of prediction 
axs10 = fig.add_subplot(gs[1, 0])
axs11 = fig.add_subplot(gs[1, 2], sharey=axs10)
axs12 = fig.add_subplot(gs[1, 4], sharey=axs10)
sns.lineplot(data=df_mean_BMA, x="delta_VA", y="rec", hue="ComSourLbl", 
             hue_order=hue_order, errorbar=None,marker = '^',markersize=10,
             linewidth=2, palette=color_order, ax=axs10, legend = None)
sns.lineplot(data=df_mean_BMS, x="delta_VA", y="rec", hue="ComSourLbl", 
             hue_order=hue_order, errorbar=None,marker = '^',markersize=10,
             linewidth=2, palette=color_order, ax=axs11, legend = None)
sns.lineplot(data=df_mean_SCC, x="delta_VA", y="rec", hue="ComSourLbl", 
             hue_order=hue_order, errorbar=None,marker = '^', markersize=10,
             linewidth=2, palette=color_order, ax=axs12, legend = None)

# axs10.set_title('BayMA-Bay-Bay',fontsize=fontsize)
# axs11.set_title('BayMS-Bay-Bay',fontsize=fontsize)
# axs12.set_title('SCC-Bay-Bay',fontsize=fontsize)


for ax in [axs00, axs01, axs02, axs10, axs11, axs12]:
    clean_axs(ax)
    ax.set_xlabel('')
    ax.set_ylabel('')
    
# Create custom legend handles
# Add legend with custom handles
custom_legend_handles = [mlines.Line2D([], [], color='red', linestyle='-'),
                         mlines.Line2D([], [], color='blue', linestyle='-'),
                         mlines.Line2D([], [], color='red', linestyle='--'), 
                         mlines.Line2D([], [], color='blue', linestyle='--'), 
                         mlines.Line2D([], [], color='red', marker='o', linestyle=''),
                         mlines.Line2D([], [], color='blue', marker='o', linestyle=''),
                         mlines.Line2D([], [], color='red', marker='^', linestyle='-'),
                         mlines.Line2D([], [], color='blue', marker='^', linestyle='-')]
# Define the row labels (invisible)
row_labels = [
    mlines.Line2D([], [], linestyle='', marker=''),
    mlines.Line2D([], [], linestyle='', marker='')
]
# Combine row labels and custom legend handles
all_handles = row_labels + custom_legend_handles
all_labels = [r'$P(C=1|x_{A,AV},x_{V,AV})>0.5$' + ' :', r'$P(C=1|x_{A,AV},x_{V,AV}) \leq 0.5$' + ' :', 
              r'$mean(\hat{S}_{A,AV})$', r'$mean(\hat{S}_{A,AV})$', 
              r'$mean(x_{A,AV})$', r'$mean(x_{A,AV})$',  
              r'$x_{A, AV}$', r'$x_{A, AV}$',
              r'$mean(\Delta_A)$', r'$mean(\Delta_A)$']
fig.legend(handles=all_handles, 
           labels=all_labels,
           ncol=5, fontsize=fontsize, bbox_to_anchor=(0.45, -0.01), loc='lower center', frameon=False)

axs00.set_ylabel('Spatial location (\u00B0)', fontsize = fontsize)
axs10.set_ylabel('Simulated bias (\u00B0)', fontsize = fontsize)
fig.text(0.35, 0.19, 'Spatial disparity (V - A , visual angle \u00B0)', fontsize = fontsize)

#fig.text(0.45, 0.4, "Spatial disparity (V - A , visual angle \u00B0)", fontsize=20, va='center')

# Adjust layout
fig.subplots_adjust(hspace=0.2, wspace=0.4, bottom=0.25,top = 0.9, left = 0.1,  right = 0.9)

plt.savefig(os.path.join(work_path, "plot4paper", "three_models_dist.png"), dpi=300)  # Adjust dpi for print quality
# Show the plot
plt.show()

#############################################
#### plot prediction 
# fig, axs = plt.subplots(figsize=(12, 6), ncols = 3)
# sns.lineplot(data=df_mean_SCC, x="delta_VA", y="rec", hue="ComSourLbl", 
#              hue_order=hue_order, errorbar=None,marker = 'o',
#              linewidth=3, palette=color_order, ax=axs[0])
# sns.lineplot(data=df_mean_BMS, x="delta_VA", y="rec", hue="ComSourLbl", 
#              hue_order=hue_order, errorbar=None,marker = 'o',
#              linewidth=3, palette=color_order, ax=axs[1], legend = None)
# sns.lineplot(data=df_mean_BMA, x="delta_VA", y="rec", hue="ComSourLbl", 
#              hue_order=hue_order, errorbar=None,marker = 'o',
#              linewidth=3, palette=color_order, ax=axs[2], legend = None)

# # make invisible some edges
# for ax in axs:
#     clean_axs(ax)
#     ax.set_xlabel('')
#     ax.set_ylabel('')
# fig.supylabel('Simulated Bias (\u00B0)', fontsize=18)
# fig.supxlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 18)
# axs[0].legend(title='', loc = 'upper right', ncol=1, fontsize = 18, bbox_to_anchor=(0.6, -.15), frameon=False)
# axs[0].set_title('Bayesian - MA',fontsize=16, fontweight='bold')
# axs[1].set_title('Bayesian - MS',fontsize=16, fontweight='bold')
# axs[2].set_title('Sensory Cue Conflict',fontsize=16, fontweight='bold')
# # Adjust layout
# #plt.subplots_adjust(bottom=0.2)
# # Save the plot
# plt.savefig(os.path.join(work_path, "plot4paper", "three_models_pred.png"), dpi=300)  # Adjust dpi for print quality
# plt.show()
