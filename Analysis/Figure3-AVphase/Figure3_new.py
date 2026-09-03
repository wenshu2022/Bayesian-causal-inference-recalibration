import pandas as pd
import numpy as np
import os
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
data_path = "P:/3026008.01/Data/"
pred_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
os.chdir(work_path)
from help_function import *

#read subject list     
sub_id_lst = read_sub_lst()

#############################
m_id = 70
#sub_id_lst = sub_group_lst(m_id)
fontsize = 14
####################
## data preparation
####################

######  BEH 
df_beh = processBehDat()

# Data for fig A  - average confidence by sub
meanBehConfBySub = df_beh.groupby(['sub_id', 'delta_VA','ComSourLbl'])['confLvl'].agg(['mean', 'count']).reset_index()
meanBehConfBySub.columns = ['sub_id', 'delta_VA','ComSourLbl', 'avgConfLvl', 'count']

# Data for fig C  - percent of common for each disparity
cntBehBySub = df_beh.groupby(['sub_id', 'delta_VA'])['confLvl'].count().reset_index()
cntBehBySub.columns = ['sub_id', 'delta_VA', 'countByDel']
cntBehComBySub = pd.merge(meanBehConfBySub.loc[meanBehConfBySub.ComSourLbl=='Common'], cntBehBySub, how = 'outer', on = ['sub_id', 'delta_VA']).reset_index(drop=True)
cntBehComBySub['pect_C1'] = cntBehComBySub['count'] / cntBehComBySub['countByDel']

# Data for fig E  - count confidence cases
#cntConfCombySub = cntBehConf(df_beh)

#########Model Prediction
df_sim_allsub = processPredDat(m_id, sub_id_lst)

# Data for fig B  - average confidence by sub
meanPredConfBySub = df_sim_allsub.groupby(['sub_id', 'delta_VA','ComSourLbl'])['R_conf'].agg(['mean', 'count']).reset_index()
meanPredConfBySub.columns = ['sub_id', 'delta_VA','ComSourLbl', 'avgConfLvl', 'count']

# Data for fig D  - percent of common for each disparity
cntPredBySub = df_sim_allsub.groupby(['sub_id', 'delta_VA'])['R_conf'].count().reset_index()
cntPredBySub.columns = ['sub_id', 'delta_VA', 'countByDel']
cntPredComBySub = pd.merge(meanPredConfBySub.loc[meanPredConfBySub.ComSourLbl=='Common'], cntPredBySub, how = 'outer', on = ['sub_id', 'delta_VA']).reset_index(drop=True)
cntPredComBySub['pect_C1'] = cntPredComBySub['count'] / cntPredComBySub['countByDel']

# Data for fig F  - count confidence cases
# cntConfPredCom = df_sim_allsub.groupby(['sub_id', 'delta_VA','ComSourLbl','ConfLbl'])['R_conf'].count().reset_index()
# cntConfPredCom['ratio'] = cntConfPredCom['R_conf']/nsim
#cntConfPredCom = cntPredConf(df_sim_allsub)

### plot AB style
def plot_avg_conf(df, ax, legend = 'auto'):
    sns.lineplot( data=df,  
                x='delta_VA', 
                y='avgConfLvl',
                hue_order = hue_order, 
                palette = color_order, 
                linewidth = 2,
                hue='ComSourLbl', 
                dashes=False, 
                ax = ax, 
                errorbar='se',
                marker = 'o',
                err_style='bars',
                legend = legend)
    ax.set_ylim(1, 3)
    ax.yaxis.set_major_locator(MultipleLocator(1))
    ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)
    ax.legend(title='', loc = 'lower right', fontsize = fontsize, frameon=False)
    ax.set_xlabel("Spatial disparity (V - A, visual angle \u00B0)", fontsize=fontsize)
    ax.set_ylabel("Mean confidence", fontsize=fontsize)

## figure C, D - Percentage of common responses
def plotCNT_common(df, ax):
    sns.lineplot(data=df,  
                x='delta_VA', 
                y='pect_C1', 
                linewidth=2, 
                errorbar='se', 
                err_style='bars', 
                color='black'  # Set all lines to black
                ,ax = ax
                )

    #clean_axs(ax)
    ax.set_xlabel("Spatial disparity (V - A, visual angle \u00B0)", fontsize=fontsize)
    ax.set_ylabel('% common report', fontsize = fontsize)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.yaxis.set_major_locator(MultipleLocator(0.2))
    ax.set_ylim(0, 1)
    
#plot EF
def plotCNT(df, ax, label, color):  
    sns.lineplot(data=df.loc[df.ComSourLbl == label],  
                x='delta_VA', 
                y='ratio', 
                style='ConfLbl', 
                style_order=[ "High", "Medium", "Low"],  # Order for styles
                ax=ax, 
                linewidth=2, 
                errorbar='se', 
                err_style='bars', 
                color=color  # Set all lines to black
                ,legend = None
                )

    ax.set_title(label, fontsize=fontsize, color = color)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
    ax.set_xlabel('')
    ax.set_ylabel('')



hue_order = ["Common", "Separate"]
color_order = ['red', 'blue']


fig, _axs = plt.subplots(figsize=(10, 6), nrows = 2, ncols = 2, gridspec_kw={'hspace': 0.4, 'wspace': 0.8})
#height_ratios = [4, 3], width_ratios = [3.8, 3, 3, 2], hspace=0.4, wspace=0.4
axs = _axs.flatten()

plot_avg_conf(meanBehConfBySub, axs[2])
plot_avg_conf(meanPredConfBySub, axs[3], None)

plotCNT_common(cntBehComBySub, axs[0])
plotCNT_common(cntPredComBySub, axs[1])

# plotCNT(cntConfCombySub, axs[4], hue_order[0], color_order[0])
# plotCNT(cntConfCombySub, axs[6], hue_order[1], color_order[1])
# plotCNT(cntConfPredCom, axs[5], hue_order[0], color_order[0])
# plotCNT(cntConfPredCom, axs[7], hue_order[1], color_order[1])

for ax in axs:
    clean_axs(ax, fontsize)
    ax.set_xticks([-24, -16, -8, 0, 8, 16, 24])

#add x and y for the two smaller plots
# fig.text(0.045, 0.2, "# cases / # total trials", fontsize=fontsize, va='center', rotation='vertical')
# fig.text(0.55, 0.2, "# cases / # total trials", fontsize=fontsize, va='center', rotation='vertical')

for ax in axs[6:]:
    ax.yaxis.set_major_locator(MultipleLocator(0.025))
    ax.set_xlabel("Spatial disparity (V - A, visual angle \u00B0)", fontsize=fontsize)

style_legend = [
        mlines.Line2D([0], [0], color='black', linestyle='-', label='High'),
        mlines.Line2D([0], [0], color='black', linestyle='--', label='Medium'),
        mlines.Line2D([0], [0], color='black', linestyle=':', label='Low')
    ]
#axs[4].legend(handles=style_legend, title="Confidence:", loc = 'upper left', title_fontsize=fontsize, fontsize = fontsize, bbox_to_anchor=(0.62, 1.4), frameon=False)
plt.subplots_adjust(right = 0.9, top = 0.95, bottom = 0.1)
plt.savefig(os.path.join(work_path, "plot4paper", "Figure3-AVphase.png"), dpi=300)  # Adjust dpi for print quality
plt.show()