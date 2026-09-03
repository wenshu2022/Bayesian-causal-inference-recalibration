import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.lines as mlines
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import itertools

sns.set_theme(style="white")
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
R_path = "C:/Users/wenlou/Documents/R scripts/RecaliProject/output"
data_path = "P:/3026008.01/Data/"
os.chdir(work_path)


#####################################################################
# barplot - for aggregated level spatial bias for each AV disparity
def plot_effect_bar(fix_effect, outname):
    # for each spatial disparity, bar height for the fix effect with signs, stars for p-value(whether it is significantly different from 0), error bar is the std.err f
    # LME
    fig, ax = plt.subplots()
    ax.bar(fix_effect.loc[fix_effect.delta_VA != -99, 'delta_VA'], 
        fix_effect.loc[fix_effect.delta_VA != -99, 'effects'], width = 5, color = '0.5'
        )

    # Add error bars
    plt.errorbar(
        fix_effect.loc[fix_effect.delta_VA != -99, 'delta_VA'], 
        fix_effect.loc[fix_effect.delta_VA != -99, 'effects'], 
        yerr=fix_effect.loc[fix_effect.delta_VA != -99, 'std.err'], 
        fmt='none', 
        c='black', 
        capsize=3
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_major_locator(MultipleLocator(8))
    plt.tick_params(axis='both', which='major', direction='in', length=4, width=1.2, colors='black',
        left=True, bottom=True)

    ax.grid(True, which='major', axis='y', linestyle='--', alpha=0.7)
    ax.set_xlabel("Spatial disparity (V - A, visual angle \u00B0)", fontsize=12)
    ax.set_ylabel("Bias (\u00B0)", fontsize=12)

    plt.tight_layout()
    plt.savefig(os.path.join(work_path, "plot4paper", outname + ".png"), dpi=300)  # Adjust dpi for print quality
    plt.show()


# for auditory blocks
fix_effect = pd.read_csv(os.path.join(R_path, "raw_resp_fix_effect.csv"))
plot_effect_bar(fix_effect, "fixEffectRawResp")

# for visual blocks
fix_effect = pd.read_csv(os.path.join(R_path, "vis_raw_resp_fix_effect.csv"))
plot_effect_bar(fix_effect, "visFixEffectRawResp")


#####################################################################
# lineplot for each spatial disparity with random effect line for each sub

fix_effect = pd.read_csv(os.path.join(R_path, "raw_resp_fix_effect.csv"))
rand_effect = pd.read_csv(os.path.join(R_path, "raw_resp_rand_effect.csv"))

x=np.array([-12, -4, 4, 12])

def plotALine(ax,a,b,color,width=0.5,alp=1):
    ax.plot(x, a+b*x, linewidth=width, color=color,alpha = alp)
    
fig, axs = plt.subplots(nrows=2, ncols=4, figsize=(10, 6), gridspec_kw={'hspace': 0.4})

axs[1, 3].set_visible(False)
axs_flat = axs.flatten()

#sps = fix_effect.loc[fix_effect.delta_VA!=-99, 'delta_VA'].sort_values().tolist()
sps=np.array([-24, -16, -8, 0, 24, 16, 8])

for idx, sp in enumerate(sps):
    
    a=fix_effect.loc[fix_effect.delta_VA==sp, 'effects'].values[0]
    b=fix_effect.loc[fix_effect.delta_VA==-99, 'effects'].values[0]# special code for the trupos coeficient
    ax = axs_flat[idx]

    #fix effect
    plotALine(ax,a,b,'0',width=2)
    #random effect
    for i in np.arange(34):
        plotALine(ax,rand_effect.iloc[i,0] +a,rand_effect.iloc[i,1] +b,'0.1',0.1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks(x)
    ax.set_yticks(x)
    ax.tick_params(axis='both', which='major', direction='in', length=4, width=1.2, colors='black',
        left=True, bottom=True)
    ax.set_title(r'$V - A = {}^\circ$'.format(sp))

fig.supxlabel("True Sound Location (visual angle \u00B0)")
fig.supylabel("Predicted response Locations (visual angle \u00B0)")

plt.tight_layout()
plt.savefig(os.path.join(work_path, "plot4paper", "randEffectRawResp.png"), dpi=300)  # Adjust dpi for print quality
plt.show()


#####################################################################
# lineplot - true location against report locations - average mean 
# still to add an error bar sem
x=np.array([-12, -4, 4, 12])
def agg_df(df):
    ## step 1: avergae within subjects
    mean_data_by_sub  = df.groupby(['sub_id', 'taskAV', 'delta_VA', 'truePos'])['respPos'].mean().reset_index()
    ## step 2: average across subjects
   # mean_data_all_sub  = mean_data_by_sub.groupby(['taskAV', 'delta_VA', 'truePos'])['respPos'].agg(['mean', 'sem']).reset_index()
    #mark postive av
    mean_data_by_sub['postive_AV'] = mean_data_by_sub.delta_VA>=0

    return mean_data_by_sub

def plot_avg_line(df, postive, ax, pa):
    if postive:
        palette = ['grey'] + pa[:3]
        markers = ['o', 's', '^', 'D']
        title = r'Block AV-{} : $V - A \geq 0 ^\circ$'.format(df.taskAV.unique()[0])
    else:
        palette = pa[::-1][:3] + ['grey']
        markers = ['D', '^', 's', 'o']
        title = r'Block AV-{} : $V - A \leq 0 ^\circ$'.format(df.taskAV.unique()[0])
        
    legend = None if df.taskAV.unique()[0] == 'A' else 'auto'
    sns.lineplot( data=df.loc[(df.postive_AV==postive) | (df.delta_VA==0) , : ],  
                x='truePos', y='respPos',
                hue='delta_VA', style = 'delta_VA',
                markers=markers, dashes=False, ax = ax, legend = legend, 
                palette=palette, errorbar='se',err_style='bars')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xticks(x)
    ax.set_yticks(x)
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.set_title(title)
    ax.tick_params(axis='both', which='major', direction='in', length=4, width=1.2, colors='black',
    left=True, bottom=True)

df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))  
df_V = pd.read_csv(os.path.join(data_path, "exp1_V_all_exc.csv"))  
pa = sns.color_palette("dark:#5A9_r", n_colors=6) 
 
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(12, 8), gridspec_kw={'hspace': 0.4})
axs_flat = axs.flatten()
ax_id = 0
# for df in [df_A, df_V]:
#     for postive in [0, 1]:
#         ax = axs_flat[ax_id]
#         plot_avg_line(agg_df(df), postive, ax, pa)
#         ax_id+=1
for postive in [0, 1]:
    for df in [df_A, df_V]:
        ax = axs_flat[ax_id]
        plot_avg_line(agg_df(df), postive, ax, pa)
        ax_id+=1
fig.supxlabel("True Location (visual angle \u00B0)")
fig.supylabel("Localization responses (visual angle \u00B0)")

handles2D= [ax.get_legend_handles_labels()[0] for ax in axs[:,1]]
handles = list(itertools.chain.from_iterable(handles2D))
labels2D= [ax.get_legend_handles_labels()[1] for ax in axs[:,1]]
labels = list(itertools.chain.from_iterable(labels2D))
by_label = dict(zip(labels, handles)) 
axs[0,1].legend('', frameon=False)
axs[1,1].legend(by_label.values(), by_label.keys(), title="", loc='lower center', ncol=4, bbox_to_anchor=(-1, -0.4), frameon=False)

plt.tight_layout()
plt.savefig(os.path.join(work_path, "plot4paper", "avgRawRespAV.png"), dpi=300)  # Adjust dpi for print quality
plt.show()


#####################################################################
# across-session homogeneity analysis
from statsmodels.tsa.stattools import adfuller

df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))  
sub_lst = df_A.sub_id.unique().tolist()
for sub_id in sub_lst:
    for D in np.array([0, 8, 16, 24]):
        statResult = adfuller(df_A.loc[(df_A.abs_delta_VA == D) & (df_A.sub_id==sub_id), 'flipVAE'], autolag='BIC')
        if statResult[1]>0.01:
            print('sub {}:'.format(sub_id))
            print('disparity {}:'.format(D))
            print('ADF Statistic:', statResult[0])
            print('p-value:', statResult[1])
            print('Critical Values:', statResult[4])
            
  #None      
        

