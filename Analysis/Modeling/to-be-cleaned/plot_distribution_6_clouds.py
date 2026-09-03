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
data_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction/adhoc'
os.chdir(work_path)

#read subject list 
with open('P:/3026008.01/data_for_fitting/sub_id_exp1.txt', 'r') as file:
    lines = file.readlines()
    
sub_id_lst = [int(line.strip()) for line in lines]

m_id = 45

def draw_6_process_df(sub_id, m_id):
    df_sim = pd.read_csv(os.path.join(data_path, 'pred_sub_' + str(sub_id) + '_m_' + str(m_id) + '.csv'))   
    df_sim['delta_VA'] = df_sim['s_v'] - df_sim['s_a']
    df_sim.loc[df_sim.prob>0.5, 'ComSourLbl'] = 'Common'
    df_sim.loc[df_sim.prob<=0.5, 'ComSourLbl'] = 'Separate'
    df_sim['diff_s_x'] = df_sim['bi_sA_hat'] - df_sim['bi_xA']
    
    df_sim.loc[df_sim.R_conf==1, 'ConfLbl'] = 'Low'
    df_sim.loc[df_sim.R_conf==2, 'ConfLbl'] = 'Medium'
    df_sim.loc[df_sim.R_conf==3, 'ConfLbl'] = 'High'

    ### stat level data
    custom_agg = {
        'rec': [ 'mean'],
        'bi_sA_hat': ['mean'],
        'bi_xA': ['mean'],
        'diff_s_x': [ 'mean'],
        'ComSourLbl': [ 'count'] 
    }
    ## group by common source label and delta_VA
    mean_data_all = df_sim.groupby(['ComSourLbl', 'ConfLbl', 'delta_VA']).agg(custom_agg).reset_index()
    mean_data_all.columns = mean_data_all.columns.droplevel(1)
    # rename the count col 
    current_columns = mean_data_all.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_all.columns = current_columns
    
    ## group by delta_VA
    mean_data_t = df_sim.groupby(['delta_VA', 'ConfLbl']).agg(custom_agg).reset_index()
    mean_data_t.columns = mean_data_t.columns.droplevel(1)
    current_columns = mean_data_t.columns.tolist()
    current_columns[-1] = 'count'
    mean_data_t.columns = current_columns
    mean_data_t['ComSourLbl'] = "Total"
    
    mean_data_all = pd.concat([mean_data_all, mean_data_t]).reset_index(drop = True)
    # tocalculate the ratio, first merge the total count
    # mean_data_all = pd.merge(mean_data_all, mean_data_t[['delta_VA', 'count']], how = 'outer', on = 'delta_VA')
    # mean_data_all['ratio'] = mean_data_all['count_x']/mean_data_all['count_y'] *100
    #return df_sim, mean_data_all


#df_sim, mean_data_all = process_df(sub_id, m_id)

    ####################################
    # add jitter to the data so that the distribution is more obvious
    df_sim_jittered = df_sim.copy()
    mean_data_T = mean_data_all[mean_data_all.ComSourLbl!='Total'].copy()
    mean_data_T['conf_combo'] = mean_data_T['ComSourLbl'] + '-' +  mean_data_T['ConfLbl'] 
    #df_sim_jittered.prob = 1 - df_sim_jittered.prob
    
    jitter_amount = 0.1
    df_sim_jittered['delta_VA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))
    df_sim_jittered['bi_sA_hat'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))
    df_sim_jittered['bi_xA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))
    #df_sim_jittered['diff_s_x'] = df_sim_jittered['sA_hat'] - df_sim_jittered['bi_xA']
    
    df_sim_high_com = df_sim_jittered.loc[(df_sim_jittered.ConfLbl =='High') & (df_sim_jittered.ComSourLbl=='Common')]
    df_sim_med_com = df_sim_jittered[(df_sim_jittered.ConfLbl =='Medium') & (df_sim_jittered.ComSourLbl=='Common')]
    df_sim_low_com = df_sim_jittered[(df_sim_jittered.ConfLbl =='Low') & (df_sim_jittered.ComSourLbl=='Common')]
    
    df_sim_high_sep = df_sim_jittered[(df_sim_jittered.ConfLbl =='High') & (df_sim_jittered.ComSourLbl!='Common')]
    df_sim_med_sep = df_sim_jittered[(df_sim_jittered.ConfLbl =='Medium') & (df_sim_jittered.ComSourLbl!='Common')]
    df_sim_low_sep = df_sim_jittered[(df_sim_jittered.ConfLbl =='Low') & (df_sim_jittered.ComSourLbl!='Common')]
    
    
    hue_order = [ "Common-High", "Common-Medium", "Common-Low", "Separate-High", "Separate-Medium", "Separate-Low"]
    color_order = [ 'darkred', 'Crimson', 'LightCoral', 'darkblue', 'steelblue', 'skyblue']
    #markers = ['o', 's', '^'] 
    # Create a LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list('custom_cmap', [ 'darkblue', 'LightCoral']) # from blue (Separate) to red (common)
    norm = plt.Normalize(min(df_sim_jittered.prob), max(df_sim_jittered.prob))
    
    
    fig = plt.figure(figsize=(24, 18))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 0.05])
    #plt.subplots_adjust(hspace=0.1,wspace=0.05)
    
    # Plot both scatter plots
    axs1 = fig.add_subplot(gs[0, 0])
    axs1.minorticks_on()
    axs1.tick_params(axis='both', which='major', direction='in', left=True, bottom=True)
    pcm1 = axs1.scatter(df_sim_high_com.loc[:,'delta_VA'] + 1.2, df_sim_high_com.loc[:,'bi_xA'], 
                        c=df_sim_high_com.loc[:,'prob'], cmap=cmap, norm=norm,  s = 0.2)
    axs1.scatter(df_sim_med_com.loc[:,'delta_VA'] + 0.8, df_sim_med_com.loc[:,'bi_xA'], 
                 c=df_sim_med_com.loc[:,'prob'], cmap=cmap, norm=norm,  s = 0.2)
    axs1.scatter(df_sim_low_com.loc[:,'delta_VA'] + 0.4, df_sim_low_com.loc[:,'bi_xA'], 
                 c=df_sim_low_com.loc[:,'prob'], cmap=cmap, norm=norm,  s = 0.2)
    
    axs1.scatter(df_sim_high_sep.loc[:,'delta_VA'] - 1.2, df_sim_high_sep.loc[:,'bi_xA'], 
                 c=df_sim_high_sep.loc[:,'prob'], cmap=cmap, norm=norm,  s = 0.2)
    axs1.scatter(df_sim_med_sep.loc[:,'delta_VA'] - 0.8, df_sim_med_sep.loc[:,'bi_xA'], 
                 c=df_sim_med_sep.loc[:,'prob'], cmap=cmap, norm=norm,  s = 0.2)
    axs1.scatter(df_sim_low_sep.loc[:,'delta_VA'] - 0.4, df_sim_low_sep.loc[:,'bi_xA'], 
                 c=df_sim_low_sep.loc[:,'prob'], cmap=cmap, norm=norm,  s = 0.2)
    
    # Add major and minor ticks to axs1
    axs1.xaxis.set_major_locator(MultipleLocator(4))
    axs1.yaxis.set_major_locator(MultipleLocator(8))
    
    sns.lineplot(data = mean_data_T, x = "delta_VA", y = "bi_sA_hat", hue = "conf_combo", hue_order = hue_order, 
                 dashes = False, palette = color_order,  linewidth=2,  ci = None, ax = axs1, legend = None)
    sns.lineplot(data = mean_data_T, x = "delta_VA", y = "bi_xA", hue = "conf_combo", hue_order = hue_order,  
                 linestyle="--", palette = color_order, linewidth=2,   ci = None, ax = axs1, legend = None)
    axs1.set_ylabel('Spatial location (\u00B0)', fontsize = 12)
    axs1.set_xlabel('')
    #axs1.text(0.25, 1, 'Common', transform=axs1.transAxes, fontsize=15, va='top', ha='left', bbox=dict(facecolor='white', alpha=0.5))
    
    axs1.spines['top'].set_visible(False)
    axs1.spines['right'].set_visible(False)
    
    # Colorbar
    cax = fig.add_subplot(gs[0, 1])
    cbar = plt.colorbar(pcm1, cax=cax, label=r'$P(C=1|x_A, x_V)$')
    # Create custom legend handles
    # Add legend with custom handles
    
    custom_legend_handles = [mlines.Line2D([], [], color='darkblue', linestyle='-'),
                             mlines.Line2D([], [], color='steelblue', linestyle='-'),
                             mlines.Line2D([], [], color='skyblue', linestyle='-'),
                             mlines.Line2D([], [], color='darkred', linestyle='-'),
                             mlines.Line2D([], [], color='Crimson', linestyle='-'),
                             mlines.Line2D([], [], color='LightCoral', linestyle='-'),
                             
                             mlines.Line2D([], [], color='darkblue', linestyle='--'),
                             mlines.Line2D([], [], color='steelblue', linestyle='--'),
                             mlines.Line2D([], [], color='skyblue', linestyle='--'),
                             mlines.Line2D([], [], color='darkred', linestyle='--'),
                             mlines.Line2D([], [], color='Crimson', linestyle='--'),
                             mlines.Line2D([], [], color='LightCoral', linestyle='--')]
                            #  mlines.Line2D([], [], color='darkblue', marker='o', linestyle=''),
                            #  mlines.Line2D([], [], color='LightCoral', marker='o', linestyle='')]
    
    # Define the row labels (invisible)
    # row_labels = [
    #     mlines.Line2D([], [], linestyle='-', marker='', color='darkblue'),
    #     mlines.Line2D([], [], linestyle='-', marker='', color='steelblue'),
    #     mlines.Line2D([], [], linestyle='-', marker='', color='skyblue'),
    #     mlines.Line2D([], [], linestyle='-', marker='', color='darkred'),
    #     mlines.Line2D([], [], linestyle='-', marker='', color='Crimson'),
    #     mlines.Line2D([], [], linestyle='-', marker='', color='LightCoral')]
    
    # Combine row labels and custom legend handles
    all_handles = custom_legend_handles
    # all_labels = ['Common-High', 'Common-Medium','Common-Low','Separate-High','Separate-Medium','Separate-Low', 
    #               r'$mean(\hat{s}_{A})$',  r'$mean(x_{A})$' ]
    all_labels = ['Common-High: ' + r'$mean(\hat{s}_{A})$', 'Common-Medium: ' + r'$mean(\hat{s}_{A})$','Common-Low: ' + r'$mean(\hat{s}_{A})$',
    'Separate-High: '+r'$mean(\hat{s}_{A})$','Separate-Medium: '+r'$mean(\hat{s}_{A})$','Separate-Low: '+r'$mean(\hat{s}_{A})$', 
                 'Common-High: '+r'$mean(x_{A})$', 'Common-Medium: '+r'$mean(x_{A})$','Common-Low: '+r'$mean(x_{A})$','Separate-High: '+r'$mean(x_{A})$',
    'Separate-Medium: '+r'$mean(x_{A})$','Separate-Low: '+r'$mean(x_{A})$']
    # all_labels = [r'$P(C=1|x_A,x_V)>0.5$' + ' :', r'$P(C=1|x_A,x_V) \leq 0.5$' + ' :', 
    #               r'$mean(\hat{s}_{A})$', r'$mean(\hat{s}_{A})$', 
    #               r'$mean(x_{A})$', r'$mean(x_{A})$',  
    #               r'$x_A$', r'$x_A$']
    fig.legend(handles=all_handles, 
               labels=all_labels,
               ncol=4,fontsize=12, bbox_to_anchor=(0.5, 0), loc='lower center', frameon=False)
    
    
    # Adjust layout
    #plt.subplots_adjust(wspace=0.1, hspace=0.1, top=0.9, bottom=0.2, left = 0.1, right = 0.9)
    
    fig.text(0.5, 0.1, 'Spatial disparity (V - A , visual angle \u00B0)', ha='center', fontsize = 16)
    axs1.set_title('sub-' + str(sub_id),fontsize = 16)
    
    plt.savefig(os.path.join(work_path, "output/sub_model_conf/sub_" +str(sub_id) + "_6cloud_dist.png"), dpi=300)  # Adjust dpi for print quality
    # Show the plot
    plt.show()
    
    
    
    
    
for sub_id in sub_id_lst:
    draw_6_process_df(sub_id, m_id)