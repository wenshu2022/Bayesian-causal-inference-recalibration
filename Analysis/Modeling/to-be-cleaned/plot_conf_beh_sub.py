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
data_path = "P:/3026008.01/Data/"
os.chdir(work_path)

#read subject list 
with open('P:/3026008.01/data_for_fitting/sub_id_exp1.txt', 'r') as file:
    lines = file.readlines()
    
sub_id_lst = [int(line.strip()) for line in lines]


hue_order = [ "High", "Medium", "Low"]
color_order = ['darkblue', 'steelblue', 'skyblue']
markers = ['o', 's', '^'] 

df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))  

df_A.loc[df_A.confLvl==1, 'ConfLbl'] = 'Low'
df_A.loc[df_A.confLvl==2, 'ConfLbl'] = 'Medium'
df_A.loc[df_A.confLvl==3, 'ConfLbl'] = 'High'

df_A.loc[df_A.ComSourFlag==1, 'ComSourLbl'] = 'Common'
df_A.loc[df_A.ComSourFlag!=1, 'ComSourLbl'] = 'Separate'


# sub_id = 1
# sel = 'Common'
def draw_sub_beh(sub_id,sel):
    ## select dataframe by sub
    df_A_sub = df_A.loc[df_A.sub_id == sub_id]

    if sel != 'Total':
        df_A_sub = df_A_sub.loc[df_A_sub.ComSourLbl == sel]

    count = df_A_sub[['ConfLbl', 'abs_delta_VA']].value_counts().reset_index()
    current_columns = count.columns.tolist()
    current_columns[-1] = 'num'
    count.columns = current_columns

    ## group by delta_VA
    count_t = df_A_sub[['abs_delta_VA']].value_counts().reset_index()
    current_columns = count_t.columns.tolist()
    current_columns[-1] = 'num'
    count_t.columns = current_columns

    # to calculate the ratio, first merge the total count
    count = pd.merge(count, count_t[['abs_delta_VA', 'num']], how = 'outer', on = 'abs_delta_VA')
    count['ratio'] = count['num_x']/count['num_y'] *100
    count.rename(columns = {'num_x':'count', 'num_y':'count_total'}, inplace = True)


    fig, axs = plt.subplots(ncols=1, nrows=2, figsize=(10, 10))
    for ax in axs:
            ax.minorticks_on()
            ax.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)

    sns.lineplot(data = df_A_sub, x = "abs_delta_VA", y = "flipVAE", hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", 
                style_order= hue_order, linewidth=2, palette = color_order, markers = markers, ax=axs[0])

    # count plots
    sns.lineplot(data = count, x="abs_delta_VA", y = 'ratio', hue = "ConfLbl", hue_order = hue_order, style = "ConfLbl", 
                style_order= hue_order, palette = color_order, markers = markers, linewidth=2, ax=axs[1], legend = None)

    # Add annotations
    for line in axs[1].get_lines():
        for x, y in zip(line.get_xdata(), line.get_ydata()):
            axs[1].text(x, y, f'{y:.0f}', fontsize=9, verticalalignment='bottom', horizontalalignment='right',
                        bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none'))


    # make invisible some edges
    for ax in axs:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.xaxis.set_major_locator(MultipleLocator(8))

    for ax in axs[:1]:
        ax.set_xlabel('')
    #    ax.set_ylabel('Bias (\u00B0)')
        ax.xaxis.set_ticklabels([])
        #ax.tick_params(axis='x', which='major', pad=1)

    axs[0].set_ylabel('Bias (\u00B0)')
    axs[1].set_ylabel('% cases (per spatial disparity)')
    axs[0].text(0.03, 2.1, 'Behavior-'+sel, transform=axs[1].transAxes, fontsize=12, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))

    axs[1].set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = 12)
    #axs[2].set_ylabel(r'% $C = 1$', fontsize = 12)

    axs[0].legend(title='', loc = 'lower center', ncol=3, fontsize = 12, bbox_to_anchor=(0.25, -0.15), frameon=False)

    axs[0].set_title('Subject ' + str(sub_id))
    plt.subplots_adjust(top=0.9, bottom=0.15, left = 0.1, right = 0.9)
    
    plt.savefig(os.path.join(work_path, "output", 'sub_beh', "sub_" + str(sub_id) +'_' + sel + ".png"), dpi=300)  # Adjust dpi for print quality
    plt.show()



for sub_id in sub_id_lst:
    for sel in ['Total', 'Common', 'Separate']:
        draw_sub_beh(sub_id, sel)