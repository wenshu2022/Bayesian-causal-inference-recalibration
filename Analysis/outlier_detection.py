import pandas as pd
import numpy as np
import os 

## data path
data_path = "P:/3026008.01/Data/"
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"

df_A = pd.read_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc.csv"))

#for each condition
df_A.columns

z = 3

uniq_cond = df_A[['APosInAV', 'VPosInAV' , 'truePos', 'sub_id']].drop_duplicates()
    
for i in np.arange(uniq_cond.shape[0]):
    cond = uniq_cond.iloc[i, :]
    idx_A_pre = df_A[(df_A[['APosInAV', 'VPosInAV', 'truePos', 'sub_id']] == cond).all(axis=1)].index.tolist()
    resp_A_pre = df_A.loc[idx_A_pre, 'respPos']
    #subtract the mean from the localization responses
    df_A.loc[idx_A_pre, 'demeaned_respA'] = np.array(resp_A_pre)-np.mean(resp_A_pre)
    std_respError_A = np.std(df_A.loc[idx_A_pre, 'demeaned_respA'])
    zscore_A        = np.array(df_A.loc[idx_A_pre, 'demeaned_respA'])/std_respError_A
    bool_outlier_A  = [1 if (l < -z or l > z) else 0 for l in zscore_A]
    df_A.loc[idx_A_pre, 'outlier'] = bool_outlier_A


for i in df_A['sub_id'].drop_duplicates().tolist():
    outlier_percentage = sum(df_A.loc[df_A['sub_id'] == i, 'outlier']) / df_A.loc[df_A['sub_id'] == i, 'outlier'].shape[0] * 100
    print('sub.{:.0f} has {:.2f}% outlier'.format(i, outlier_percentage))


df_A.to_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm_exc_outlier_m.csv"), index = False )

