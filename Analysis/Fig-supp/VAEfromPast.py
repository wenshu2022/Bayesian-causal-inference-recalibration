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

#read data
df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))

def plot1sub(df, var, ax):
    agg_df_A = df.groupby(['sub_id', var])['VAE'].mean().reset_index()
    sns.lineplot(data = agg_df_A,
                 x = var,
                 y = 'VAE',
                 errorbar = 'se',
                 err_style = 'band',
                 color = 'b',
                 ax = ax
                 )
    ax.axhline(y=0, color='black', linewidth=0.8, linestyle='--')
    ax.axvline(x=0, color='black', linewidth=0.8, linestyle='--')
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    clean_axs(ax)

fig, axs = plt.subplots(ncols = 2, figsize = (8, 4), sharey = True, gridspec_kw = {'wspace' : 0.1})

plot1sub(df_A, 'delta_VA', axs[0])
plot1sub(df_A, 'back_1_delta_VA', axs[1])
fig.supylabel('VAE', fontsize = fontsize)
axs[0].set_xlabel('Spatial disparity (V - A , deg)', fontsize = fontsize)
axs[1].set_xlabel('Back 1 spatial disparity', fontsize = fontsize)
plt.subplots_adjust(top = 0.9, bottom = 0.2, right = 0.9)
plt.savefig(os.path.join('C:/Users/wenlou/Documents/Python Scripts/plot4paper/sup', 'past_influ.png'), dpi = 300)
plt.show()