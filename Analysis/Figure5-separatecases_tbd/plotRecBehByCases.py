#This script produces plot A, C, F in figure 2 - behaviour recalibration data

import pandas as pd
import numpy as np
import os

# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
R_path = "C:/Users/wenlou/Documents/R scripts/RecaliProject/output/"
os.chdir(work_path)

from help_function import *


def plot_recalibration_by_cases(suffix, legend = 'auto'):
    ##### load behaviour data
    df_beh = pd.read_csv(os.path.join(R_path, 'fix_effect' + suffix + '.csv'))
       
    fig, axs = plt.subplots()
    sns.lineplot(data = df_beh, x = "abs_delta_VA", y = "effects", hue = "ComSourLbl", hue_order = hue_order, 
               linewidth=3, palette = color_order, errorbar = None, legend = legend)

    # standard error from the regression coefcient
    axs.errorbar(df_beh.loc[df_beh.ComSourLbl=="Total", 'abs_delta_VA'], df_beh.loc[df_beh.ComSourLbl=="Total",'effects'], 
          yerr=df_beh.loc[df_beh.ComSourLbl=="Total", 'std.err'],  capsize=0, ls = '', color = 'black')
    axs.errorbar(df_beh.loc[df_beh.ComSourLbl=="Common", 'abs_delta_VA'], df_beh.loc[df_beh.ComSourLbl=="Common",'effects'], 
          yerr=df_beh.loc[df_beh.ComSourLbl=="Common", 'std.err'], capsize=0, ls = '', color = 'red')
    axs.errorbar(df_beh.loc[df_beh.ComSourLbl=="Separate", 'abs_delta_VA'], df_beh.loc[df_beh.ComSourLbl=="Separate",'effects'], 
                yerr=df_beh.loc[df_beh.ComSourLbl=="Separate", 'std.err'], capsize=0, ls = '', color = 'blue')
    clean_axs(axs)
    axs.set_xlabel('Absolute Spatial disparity (visual angle \u00B0)', fontsize = fontsize)
    axs.set_ylabel('Bias (\u00B0)', fontsize=fontsize)
    axs.legend(title='', loc = 'lower right', ncol=1, fontsize = fontsize, bbox_to_anchor=(1, 0.1), frameon=False)

    plt.subplots_adjust(left=0.15, bottom = 0.15, right = 0.95)
    # Save the plot
    plt.savefig(os.path.join(work_path, "plot4paper", "behRecalibration" + suffix + ".png"), dpi=300)  # Adjust dpi for print quality
    plt.show()

fontsize=18
hue_order = [ "Total", "Separate", "Common"]
color_order = ['black', 'blue', 'red']

plot_recalibration_by_cases('_rec')
plot_recalibration_by_cases('_opp', None)
