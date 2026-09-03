import pandas as pd
import numpy as np
import os
import matplotlib.patches as mpatches
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
data_path = "P:/3026008.01/Data/"
os.chdir(work_path)


m_score = pd.read_csv('M:/MATLAB/Model/check_performance/AIC_BIC_update.csv')

#read subject list 
sub_id_lst = m_score.sub_id.unique().tolist()

# 1 best model by sub
best_m_by_sub = m_score.loc[m_score.groupby('sub_id')['BIC'].idxmin().reset_index(drop=True).tolist()]
best_m_by_sub.value_counts('m_id')
# m_id
# 70    13
# 73     8
# 74     5
# 71     4
# 93     2
# 87     1
# 90     1
best_m_by_sub.to_csv(os.path.join(work_path, "plot4paper/best_model.csv"), index = False)

# 2 BIC for each model
m_lst = m_score.m_id.unique()
model_config = pd.read_excel('M:/MATLAB/Model/m_config.xlsx')
m_conf_sel = model_config[model_config.m_id.isin(m_lst)].reset_index(drop = True)

# concat the labels
m_score = m_score.merge(m_conf_sel[['shift_update', 'C_readout', 'AV_readout','Conf_readout', 'm_id']], how = 'outer', on = 'm_id')
m_score.loc[m_score['shift_update']=='CI', 'Recal_model'] = m_score.loc[m_score['shift_update']=='CI', 'shift_update'].str.replace('CI', 'Bay')  + m_score.loc[m_score['shift_update']=='CI', 'AV_readout']
m_score.loc[m_score['shift_update']!='CI', 'Recal_model'] = m_score.loc[m_score['shift_update']!='CI', 'shift_update'].str.replace('FR', 'SCC') 
m_score['C_readout'] = m_score['C_readout'].str.replace('p','Bay').str.replace('xdiff', 'xDiff')
m_score['Conf_readout'] = m_score['Conf_readout'].str.replace('p','Bay').str.replace('xdiff', 'xDiff')
m_score['label'] =  m_score['Recal_model'] + '-' + m_score['C_readout'] + '-' + m_score['Conf_readout']

m_score.groupby('label')['BIC'].agg(['mean', 'sem'])