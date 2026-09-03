import pandas as pd
import numpy as np
import os
import matplotlib.patches as mpatches
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
data_path = "P:/3026008.01/Data/"
os.chdir(work_path)
from help_function import *

#read subject list 
sub_id_lst = read_sub_lst()

model_config = pd.read_excel('M:/MATLAB/Model/m_config.xlsx')
metrics = 'BIC'
m_score = pd.read_csv('M:/MATLAB/Model/check_performance/AIC_BIC_update.csv')

# search for model config in the table
m_lst = m_score.m_id.unique()


################
#define model id
#m_id = 70

for m_id in m_lst:
    ########################
    #####data prepare ######
    ##process prediction data 
    # two-step average
    temp_list = []
    for sub_id in sub_id_lst:
        # 1 - average within subjects
        sub_data = agg_pred_by_sub(sub_id, m_id, 1)
        temp_list.append(sub_data)
    df_all_flipped = pd.concat(temp_list, ignore_index=True)


    ########################

    fontsize=16
    #########################
    ##Plotting 
    hue_order = [ "Total", "Separate", "Common"]
    color_order = ['black', 'blue', 'red']


    # figure 1A - beh recalibration with cnt 
    fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(6, 6), gridspec_kw={ 'height_ratios' : [2,1]})

    #predict
    sns.lineplot(data=df_all_flipped, x="delta_VA", y="rec_mean", hue="ComSourLbl", 
                hue_order=hue_order, errorbar='se',err_style = 'bars',
                linewidth=2, palette=color_order, ax=axs[0],legend = None)

    # 2nd count plots
    sns.lineplot(data = df_all_flipped[df_all_flipped.ComSourLbl=="Common"], x="delta_VA", y = 'ratio',  
                errorbar = 'se', err_style = 'bars',
                color='gray', linewidth=2, ax=axs[1])



    for ax in axs.flatten():
        clean_axs(ax)
        ax.set_xlabel('')
   
    axs[0].set_ylabel('Bias (\u00B0)', fontsize=fontsize)
    axs[1].set_ylabel(r'% $C = 1$', fontsize = fontsize)
    axs[1].set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = fontsize)
    axs[1].yaxis.set_major_formatter(PercentFormatter(xmax=1, decimals = 0))
    #axs[0].set_title('m_'+str(m_id))
    #axs[0].set_title('BayMS-sDiff-Bay', fontsize = 16)
    #axs[0].legend(title='', loc = 'lower right', ncol=1, fontsize = fontsize, frameon=False)
    plt.subplots_adjust(left=0.15, right = 0.92, top = 0.92, bottom = 0.11)
    # Save the plot
    plt.savefig(os.path.join(work_path, "plot4paper", "sup", "recali_w_cnt" + str(m_id) + ".png"), dpi=300)  # Adjust dpi for print quality
    plt.show()
