# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 14:36:52 2024

@author: wenlou
"""
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.lines as mlines
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator, PercentFormatter)

fontsize = 16
#import matplotlib as mpl
#mpl.rc('font', family='arial', style='italic', size=18)  # Example: serif font, italic style, size 12
#mpl.rcdefaults()
# from matplotlib import rc
# #rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# rc('font',**{'family':'cursive','style':'normal', 'size' : 18})
# rc('text', usetex=True)

sns.set_theme(style="white")

pred_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
est_par_path = 'M:/MATLAB/Model/Fitting/output'
data_path = "P:/3026008.01/Data/"

def clean_axs(ax,fontsize=16):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(8))
    ax.tick_params(axis='both', which='major', direction='in', left=True, bottom=True, labelsize=fontsize)

def ax_noXlabel(ax):
    ax.set_xlabel('')
    ax.xaxis.set_ticklabels([])

def ax_noYlabel(ax):
    ax.set_ylabel('')
    ax.yaxis.set_ticklabels([])

def label_df(df, type, fieldname):
    if type=='conf':
        df.loc[df[fieldname]==1, 'ConfLbl'] = 'Low'
        df.loc[df[fieldname]==2, 'ConfLbl'] = 'Medium'
        df.loc[df[fieldname]==3, 'ConfLbl'] = 'High'
    elif type=='c':
        df.loc[df[fieldname]==1, 'ComSourLbl'] = 'Common'
        df.loc[df[fieldname]==2, 'ComSourLbl'] = 'Separate'
    return df

def read_sub_lst():
    with open('P:/3026008.01/data_for_fitting/sub_id_exp1.txt', 'r') as file:
        lines = file.readlines()
        
    sub_id_lst = [int(line.strip()) for line in lines]
        
    return sub_id_lst

# select sub group 
def sub_group_lst(m_id):
    #group subject
    sub_group = pd.read_csv('C:/Users/wenlou/Documents/Python Scripts/plot4paper/best_model.csv')
    sub_group = sub_group.loc[sub_group.m_id==m_id, 'sub_id'].reset_index(drop=True)
    return sub_group

def agg_pred_by_sub(sub_id, m_id, flip, select = None):
    # read in sub prediction data
    df_pred = pd.read_csv(os.path.join(pred_path, 'm' + str(m_id) ,'pred_sub_' + str(sub_id) + '.csv'))   
    
    df_pred['rec_case'] = (
        ((df_pred['s_v'] - df_pred['s_a'] <= 0) & (df_pred['s_uni'] <= df_pred['s_v'])) | \
        ((df_pred['s_v'] - df_pred['s_a'] >= 0) & (df_pred['s_uni'] >= df_pred['s_v']))
    )
    df_pred['opp_case'] = (
        ((df_pred['s_v'] - df_pred['s_a'] <= 0) & (df_pred['s_uni'] >= df_pred['s_v'])) | \
        ((df_pred['s_v'] - df_pred['s_a'] >= 0) & (df_pred['s_uni'] <= df_pred['s_v']))
    )    
    #select cases, default is none
    if select == 'rec':
        df_pred = df_pred[df_pred.rec_case==1]
    elif select == 'opp':
        df_pred = df_pred[df_pred.opp_case==1]
        
    #select the auditory block
    #df_pred = df_pred.loc[df_pred.tr_f==1, :]
    df_pred['delta_VA'] = df_pred['s_v'] - df_pred['s_a']
    df_pred = label_df(df_pred, 'c', 'R_pc')
    # df_pred.loc[df_pred.R_pc==1, 'ComSourLbl'] = 'Common'
    # df_pred.loc[df_pred.R_pc==2, 'ComSourLbl'] = 'Separate'
    nsim = df_pred.shape[0]
    
    if flip:
        mask = df_pred['delta_VA'] < 0
        df_pred.loc[mask, 'rec'] = -df_pred.loc[mask, 'rec']
        df_pred['delta_VA'] = df_pred['delta_VA'].abs()

    ### stat level data
    custom_agg = {
        'rec': [ 'mean'],
        'ComSourLbl': [ 'count'] 
    }
    ## group by common source label and delta_VA
    mean_data_sub = df_pred.groupby(['ComSourLbl', 'delta_VA']).agg(custom_agg).reset_index()
    mean_data_sub.columns = ['ComSourLbl', 'delta_VA', 'rec_mean', 'count']

    ## apart from the common/separate, we also compute the "Total" category
    mean_data_t = df_pred.groupby('delta_VA').agg(custom_agg).reset_index()
    mean_data_t.columns = ['delta_VA', 'rec_mean', 'count_total']
    mean_data_t['ComSourLbl'] = "Total"
    
    # concat the two stat
    mean_data_sub = pd.concat([mean_data_sub, mean_data_t[['ComSourLbl','delta_VA', 'rec_mean']]], ignore_index=True)
    mean_data_sub = pd.merge(mean_data_sub, mean_data_t[['delta_VA', 'count_total']], how = 'outer', on = 'delta_VA').reset_index(drop=True)
    
    mean_data_sub['ratio'] = mean_data_sub['count']/mean_data_sub['count_total']
    
    mean_data_sub['nsim']= nsim
    mean_data_sub['sub_id']= sub_id
    mean_data_sub['m_id']= m_id

    return mean_data_sub


def agg_pred_conf_by_sub(sub_id, m_id, flip, sel):
    # read in sub prediction data
    df_pred = pd.read_csv(os.path.join(pred_path, 'm' + str(m_id) ,'pred_sub_' + str(sub_id) + '.csv'))   
    ntrials = df_pred.shape[0] # total number of trials
    df_pred['delta_VA'] = df_pred['s_v'] - df_pred['s_a']
    df_pred = label_df(df_pred, 'c', 'R_pc')
    df_pred = label_df(df_pred, 'conf', 'R_conf')

    if sel != 'Total':
        df_pred = df_pred.loc[ df_pred.ComSourLbl == sel,]    
        
    if flip:
        mask = df_pred['delta_VA'] < 0
        df_pred.loc[mask, 'rec'] = -df_pred.loc[mask, 'rec']
        df_pred['delta_VA'] = df_pred['delta_VA'].abs()

    custom_agg = {
        'rec': [ 'mean'],
        'ConfLbl': [ 'count']
    }
        
    ## group by common source label and delta_VA
    mean_data_sub = df_pred.groupby([ 'ConfLbl', 'delta_VA']).agg(custom_agg).reset_index()
    mean_data_sub.columns = ['ConfLbl', 'delta_VA', 'rec_mean', 'count']
    mean_data_sub['ratio'] = mean_data_sub['count']/ntrials
    
    mean_data_sub['ComSourLbl'] = sel
    mean_data_sub['sub_id']= sub_id
    mean_data_sub['m_id']= m_id

    return mean_data_sub


def process_force0_data(m_id, groupbyvar='ComSourLbl', noise = 0, sample = 0, sub_id=None):
    data_path = "C:/Users/wenlou/Documents/MATLAB/Prediction/force_zero"
    if groupbyvar=='ComSourLbl':
        df_sim = pd.read_csv(os.path.join(data_path, 'pred_force0_m_' + str(m_id) + '.csv'))   
    elif noise == 1:
        df_sim = pd.read_csv(os.path.join(data_path, 'pred_force0_m_' + str(m_id) + '_conf_noised.csv'))
    elif noise == 0:
        df_sim = pd.read_csv(os.path.join(data_path, 'pred_force0_m_' + str(m_id) + '_conf_unoise.csv'))
        
    if sample !=0:
        df_sim = df_sim.groupby(['s_a', 'R_pc']).sample(sample, random_state = 42, replace=True).reset_index(drop=True)
        
    df_sim['delta_VA'] = df_sim['s_v'] - df_sim['s_a']
    df_sim = label_df(df_sim, 'c', 'R_pc')
    df_sim = label_df(df_sim, 'conf', 'R_conf')
    df_sim['diff_s_x'] = df_sim['bi_sA_hat'] - df_sim['bi_xA']
    
    # df_sim['bi_xA_p'] = df_sim['bi_xA'] * df_sim['prob_or']
    # df_sim['bi_sA_hat_p'] = df_sim['bi_sA_hat'] * df_sim['prob_or']
    
    if groupbyvar!='ComSourLbl':
        df_sim['max_prob'] = np.maximum(df_sim.prob_conf, 1-df_sim.prob_conf)
    ### stat level data
    custom_agg = {
        'rec': [ 'mean'],
        'bi_sA_hat': ['mean'],
        'bi_xA': ['mean'],
        'diff_s_x': [ 'mean']
    }
    ## group by common source label and delta_VA
    if groupbyvar=='ComSourLbl':
        mean_data_all = df_sim.groupby([groupbyvar, 'delta_VA']).agg(custom_agg).reset_index()
        #mean_data_all.columns = mean_data_all.columns.droplevel(1)
    else:
        mean_data_all = df_sim.groupby(['ComSourLbl', 'ConfLbl', 'delta_VA']).agg(custom_agg).reset_index()
    
    mean_data_all.columns = mean_data_all.columns.droplevel(1)
    df_sim_jittered = df_sim.copy() # jitter to make the dots more scattered 
    jitter_amount = 0.3
    df_sim_jittered['delta_VA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))
    #df_sim_jittered['bi_sA_hat'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))
    #df_sim_jittered['bi_xA'] += np.random.uniform(-jitter_amount, jitter_amount, size=len(df_sim_jittered))

    # df_sim_com = df_sim_jittered[df_sim_jittered.ComSourLbl == 'Common']
    # df_sim_sep = df_sim_jittered[df_sim_jittered.ComSourLbl == 'Separate']

    return df_sim_jittered, mean_data_all

def processBehDat():
    df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))  
    #df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc_outlier_m.csv"))  
    
    df_V = pd.read_csv(os.path.join(data_path, "exp1_V_all_exc.csv"))  
    df_A['ComSourFlag'] = 2 - df_A['ComSourFlag']
    df_V['ComSourFlag'] = 2 - df_V['ComSourFlag'] # tranform beh data bc it is differently coded...
    df_V = label_df(df_V, 'c', 'ComSourFlag')
    df_beh = pd.concat([df_A[['sub_id', 'delta_VA', 'confLvl', 'ComSourLbl', 'ComSourFlag', 'APosInAV', 'VPosInAV']], df_V[['sub_id','delta_VA', 'confLvl', 'ComSourLbl', 'ComSourFlag', 'APosInAV', 'VPosInAV']]])
    df_beh = label_df(df_beh, 'conf', 'confLvl')
    df_beh.rename(columns={ 'APosInAV':'s_a', 'VPosInAV':'s_v'}, inplace = True)
    return df_beh

def processPredDat(m_id, sub_id_lst):
    temp_list = []
    for sub_id in sub_id_lst:
        #df_pred = pd.read_csv(os.path.join(pred_path, 'explainAV', 'pred_explainAV_m_' + str(m_id) + '_sub_' + str(sub_id) + '.csv')) 
        df_pred = pd.read_csv(os.path.join(pred_path, 'm' + str(m_id) ,'pred_sub_' + str(sub_id) + '.csv')) 
        df_pred['sub_id'] = sub_id
        temp_list.append(df_pred)
    df_sim_allsub = pd.concat(temp_list, ignore_index=True)
    #nsim = df_pred.shape[0]
    df_sim_allsub['delta_VA'] = df_sim_allsub['s_v'] - df_sim_allsub['s_a']
    df_sim_allsub = label_df(df_sim_allsub, 'c', 'R_pc')
    df_sim_allsub = label_df(df_sim_allsub, 'conf', 'R_conf')
    return df_sim_allsub

def cntBehConf(df_beh, abs_del = False):
    ## count cases
    if abs_del:
        df_beh['delta_VA'] = abs(df_beh['delta_VA'])
    cnt_df_by_sub = df_beh.groupby(['sub_id', 'delta_VA','ComSourLbl', 'ConfLbl'])['confLvl'].count().reset_index()
    ntrials = df_beh.loc[df_beh.sub_id ==1].shape[0]
    cnt_df_by_sub['ratio'] = cnt_df_by_sub['confLvl'] / ntrials
    return cnt_df_by_sub

def cntPredConf(df):
    cntConfPredCom = df.groupby(['sub_id', 'delta_VA','ComSourLbl','ConfLbl'])['R_conf'].count().reset_index()
    nsim = df.loc[df.sub_id ==1].shape[0]
    cntConfPredCom['ratio'] = cntConfPredCom['R_conf']/nsim
    return cntConfPredCom