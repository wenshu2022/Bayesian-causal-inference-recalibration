import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.lines as mlines
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

sns.set_theme(style="white")
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts/Modeling"
data_path = 'C:/Users/wenlou/Documents/MATLAB/Prediction'
os.chdir(work_path)

#read subject list 
with open('P:/3026008.01/data_for_fitting/sub_id_exp1.txt', 'r') as file:
    lines = file.readlines()
    
sub_id_lst = [int(line.strip()) for line in lines]

# the model number 
m_id = 30
#sub_id = 1

##########################################################
######  check visual prediction accuracy #################
##########################################################
# read in sub prediction data
for sub_id in sub_id_lst:
    df_pred = pd.read_csv(os.path.join(data_path, 'm' + str(m_id) ,'pred_sub_' + str(sub_id) + '.csv'))   
    #select the visual block
    df_pred = df_pred.loc[df_pred.tr_f==0, :].reset_index()
    df_pred['vis_acc'] = df_pred.R_s == df_pred.s_uni
    acc_rt = df_pred['vis_acc'].sum() / df_pred.shape[0]
    
    print(f"The visual accuracy of subject {sub_id} is {acc_rt}")