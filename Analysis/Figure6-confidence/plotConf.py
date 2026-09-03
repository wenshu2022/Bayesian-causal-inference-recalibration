import pandas as pd
import numpy as np
import os
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
#pred_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
R_path = "C:/Users/wenlou/Documents/R scripts/RecaliProject/output"
os.chdir(work_path)
from help_function import *

sub_id_lst = read_sub_lst()
fontsize = 14
####################
## data preparation
####################
##########BEH ###
df_beh = pd.read_csv(os.path.join(R_path, 'fix_effect_conf.csv'))
# df_rand = pd.read_csv(os.path.join(R_path, 'rand_effect_conf.csv'))
# sem_conf = df_rand['intr24'].sem()
# count the confidence cases
cntConfCombySub = cntBehConf(processBehDat(), True)

def agg_pref_conf_all(m_id, sel, sub_id_lst):
    # two-step average
    temp_list = []
    for sub_id in sub_id_lst:
        sub_data = agg_pred_conf_by_sub(sub_id, m_id, 1, sel)
        temp_list.append(sub_data)
    df_all_flipped = pd.concat(temp_list, ignore_index=True)
    return df_all_flipped

def plot_conf_beh(df_beh, df_beh_cnt, sel,color, axs):    
    # 1st plot - beh
    sns.lineplot(data = df_beh.loc[df_beh.ComSourLbl==sel, ], x = "abs_delta_VA", y = "effects", style = "ConfLbl", color = color,
                 style_order= hue_order, linewidth=2, errorbar = None, ax=axs[0], legend = None)
    
    axs[0].errorbar(df_beh.loc[(df_beh.ConfLbl=="High") & (df_beh.ComSourLbl==sel), 'abs_delta_VA'], 
                    df_beh.loc[(df_beh.ConfLbl=="High") & (df_beh.ComSourLbl==sel),'effects'], 
                 yerr=df_beh.loc[(df_beh.ConfLbl=="High") & (df_beh.ComSourLbl==sel),'std.err'], color = color, capsize=0, ls = '')
    axs[0].errorbar(df_beh.loc[(df_beh.ConfLbl=="Medium") & (df_beh.ComSourLbl==sel), 'abs_delta_VA'], 
                    df_beh.loc[(df_beh.ConfLbl=="Medium") & (df_beh.ComSourLbl==sel),'effects'], 
                 yerr=df_beh.loc[(df_beh.ConfLbl=="Medium") & (df_beh.ComSourLbl==sel), 'std.err'], color = color, capsize=0, ls = '')
    axs[0].errorbar(df_beh.loc[(df_beh.ConfLbl=="Low") & (df_beh.ComSourLbl==sel), 'abs_delta_VA'], 
                    df_beh.loc[(df_beh.ConfLbl=="Low") & (df_beh.ComSourLbl==sel),'effects'], 
                 yerr=df_beh.loc[(df_beh.ConfLbl=="Low") & (df_beh.ComSourLbl==sel),'std.err'],  color = color, capsize=0, ls = '')

    # 2nd plot - count
    sns.lineplot(data = df_beh_cnt.loc[df_beh_cnt.ComSourLbl==sel, ],
                  x="delta_VA", y = 'ratio',
                  style = "ConfLbl", style_order= hue_order, 
                  color = 'gray',  linewidth=2, ax=axs[1], 
                   errorbar = 'se', err_style = 'bars',legend=None)  


def plot_conf_pred(axs, sel, sub_id_lst, m_id,color):
    df = agg_pref_conf_all(m_id, sel, sub_id_lst)
    # 1st plot - beh
    
    sns.lineplot(data = df, x = "delta_VA", y = "rec_mean",  style = "ConfLbl",  color = color,
                style_order= hue_order, linewidth=2,  
                errorbar = 'se', 
                err_style = 'bars',
                ax=axs[0],legend = None)

    # count plots
    sns.lineplot(data = df, x="delta_VA", y = 'ratio',  style = "ConfLbl", color = 'gray', 
                 style_order= hue_order, linewidth=2, ax=axs[1], 
                 errorbar = 'se', err_style = 'bars',legend = None)



sel_order = ["Common", "Separate"]
color_order = ['red', 'blue']
hue_order = [ "High", "Medium", "Low"]

fig, _axs = plt.subplots(figsize=(10, 10), nrows = 4, ncols = 2, gridspec_kw={'hspace': 0.3, 'wspace': 0.7, 'height_ratios' : [2,1,2,1]})
axs = _axs.flatten()

plot_conf_beh(df_beh, cntConfCombySub, sel_order[0],color_order[0], axs[[0,2]])
plot_conf_beh(df_beh, cntConfCombySub, sel_order[1],color_order[1], axs[[4,6]])

plot_conf_pred(axs[[1, 3]], sel_order[0], sub_id_lst, 70, color_order[0])
plot_conf_pred(axs[[5, 7]], sel_order[1], sub_id_lst, 70, color_order[1])
for ax in axs:
    clean_axs(ax)
    ax.set_xlabel('')
for ax in axs[[0,1,4,5]]:
    ax.set_ylabel('Bias (\u00B0)', fontsize = fontsize)
    ax.yaxis.set_major_locator(MultipleLocator(1))
for ax in axs[[2, 3, 6, 7]]:
    ax.set_ylabel('# cases / # total trials', fontsize = fontsize)
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals = 0))
    ax.yaxis.set_major_locator(MultipleLocator(0.05))
for ax in axs[[6, 7]]:
    ax.set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = fontsize)

style_legend = [
        mlines.Line2D([0], [0], color='black', linestyle='-', label='High'),
        mlines.Line2D([0], [0], color='black', linestyle='--', label='Medium'),
        mlines.Line2D([0], [0], color='black', linestyle=':', label='Low')
    ]
axs[0].legend(handles=style_legend, title="Confidence:", loc = 'upper left', title_fontsize=fontsize, fontsize = fontsize, bbox_to_anchor=(0.07, 1.2), frameon=False)
plt.subplots_adjust(right = 0.92, top = 0.92, bottom = 0.07)
#plt.savefig(os.path.join(work_path, "plot4paper", "Figure_conf.png"), dpi=300)  # Adjust dpi for print quality
plt.show()
