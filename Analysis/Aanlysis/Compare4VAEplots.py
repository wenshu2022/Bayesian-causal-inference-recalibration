# -*- coding: utf-8 -*-
"""
Created on Sat Feb  3 15:20:05 2024

@author: wenlou
"""
### these plots compare the VAE generate by different methods (mean of raw, mean of normalized, LLM coef from raw, LLM coef from normalized)

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
#from sklearn.linear_model import LinearRegression
from scipy import stats
from sklearn import preprocessing

#from sklearn.metrics import mean_squared_error, r2_score
#sns.set_theme(style="darkgrid")
sns.set_theme(style="white")
## data path
data_path = "P:/3026008.01/Data/"
# working dir
work_path = "C:/Users/wenlou/Documents/Python Scripts"
os.chdir(work_path)

########################
#####NORMALIZED#########
########################
df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all_w_VAE.pkl"))  
sub_id_lst = pd.read_pickle(os.path.join(data_path, "exp1_sub_lst.pkl"))

## STEP 1: NORMALIZE vae FOR EACH SUBJECT
#flip the spatial disparity 
df_A["flipVAE"]= df_A.VAE.copy()
df_A.loc[df_A.delta_VA < 0, "flipVAE"] = -df_A.loc[df_A.delta_VA < 0, "VAE"]
df_A["abs_delta_VA"] = abs(df_A.delta_VA)

x_positions = df_A['abs_delta_VA'].unique()

## standardized
# Initialize the RobustScaler outside the loop
transformer = preprocessing.RobustScaler(with_centering=False)
# Loop through each sub_id
for sub_id in sub_id_lst:
    for del_lvl in x_positions:
        # Extract the X values for the current sub_id
        X = df_A.loc[(df_A.sub_id == sub_id) & (df_A.abs_delta_VA == del_lvl), 'flipVAE']
        # Fit the scaler only once
        transformer.fit(X.values.reshape(-1, 1))
        # Transform and update the dataframe
        df_A.loc[(df_A.sub_id == sub_id) & (df_A.abs_delta_VA == del_lvl), 'flipVAE_norm'] = transformer.transform(X.values.reshape(-1, 1))
    
## save data.
#df_A.to_pickle(os.path.join(data_path, "exp1_A_all_w_VAE_norm.pkl"))  
## also save csv
#df_A.to_csv(os.path.join(data_path, "exp1_A_all_w_VAE_norm.csv"), index = False )
    
#### combing the common and distinct together 
# Plotting mean with SEM error bars
#all together
df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all_w_VAE_norm.pkl"))  
x_positions = df_A['abs_delta_VA'].unique()

mean_data_all = df_A.groupby(['sub_id', 'abs_delta_VA'])['flipVAE_norm'].mean().reset_index()
mean_data_all['ComSourLbl'] = 'Total'
mean_data_by_ca = df_A.groupby(['sub_id', 'ComSourLbl', 'abs_delta_VA'])['flipVAE_norm'].mean().reset_index()
mean_data_all = pd.concat([mean_data_all, mean_data_by_ca]).reset_index()
#plot_data = mean_data_all.groupby(['ComSourLbl', 'abs_delta_VA'])['flipVAE_norm'].agg(['mean', 'sem']).reset_index()

hue_order = [ "Total", "Distinct", "Common"]
color_order = ['black', 'blue', 'red']
markers = ['o', 's', '^'] 
sns.lineplot(data = mean_data_all, x = "abs_delta_VA", y = "flipVAE_norm", hue = "ComSourLbl", hue_order = hue_order, style = "ComSourLbl", 
             style_order = hue_order, linewidth=2, palette = color_order, markers = markers, err_style = 'bars')

# for idx in range(3):
#     sub_data = plot_data[plot_data.ComSourLbl==hue_order[idx]]
#     plt.errorbar(x=sub_data['abs_delta_VA'], y=sub_data['mean'], yerr=sub_data['sem'], fmt='', capsize=5,  marker='o', color = color_order[idx])

# Add labels and legend
plt.xticks(ticks=x_positions)
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('Spatial Bias')
plt.title("Normalized flipVAE (mean with 95% CI) - title to be deleted")
# Customize legend title
plt.legend(title='', loc = 'upper left')
# Save the plot
plt.savefig(os.path.join(work_path, "output/tt_vae_normlized_v2.png"), dpi=300)  # Adjust dpi for print quality
# Show the plot
plt.show()

########################
## raw VAE##############
########################

mean_data_all = df_A.groupby(['sub_id', 'abs_delta_VA'])['flipVAE'].mean().reset_index()
mean_data_all['ComSourLbl'] = 'Total'
mean_data_by_ca = df_A.groupby(['sub_id', 'ComSourLbl', 'abs_delta_VA'])['flipVAE'].mean().reset_index()
mean_data_all = pd.concat([mean_data_all, mean_data_by_ca]).reset_index()
#plot_data = mean_data_all.groupby(['ComSourLbl', 'abs_delta_VA'])['flipVAE_norm'].agg(['mean', 'sem']).reset_index()

hue_order = [ "Total", "Distinct", "Common"]
color_order = ['black', 'blue', 'red']
markers = ['o', 's', '^'] 
sns.lineplot(data = mean_data_all, x = "abs_delta_VA", y = "flipVAE", hue = "ComSourLbl", hue_order = hue_order, style = "ComSourLbl", 
             style_order = hue_order, linewidth=2, palette = color_order, markers = markers, err_style = 'bars')

# Add labels and legend
plt.xticks(ticks=x_positions)
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('Spatial Bias (deg)')
plt.title("Raw flipVAE (mean with 95% CI) - title to be deleted")
# Customize legend title
plt.legend(title='', loc = 'upper left')
# Save the plot
plt.savefig(os.path.join(work_path, "output/tt_vae_raw.png"), dpi=300)  # Adjust dpi for print quality
# Show the plot
plt.show()


##########################################
##########################################
## plot using R output - same style
##############################################

R_path = "C:/Users/wenlou/Documents/R scripts"
df_R_raw = pd.read_csv(os.path.join(R_path, 'coef_raw_VAE.csv'))

## calculate the average of the two coefs
coef_all = df_R_raw[df_R_raw.com_label.isin(["Common", "Distinct"])].groupby([ "abs_delta_VA"])['new_coef'].mean().reset_index()
coef_all['com_label'] = 'Avg'

coef_all = pd.concat([df_R_raw[['com_label', 'abs_delta_VA', 'new_coef']],  coef_all]).reset_index()

hue_order = [ "Avg", "Distinct", "Common"]
color_order = ['black', 'blue', 'red']
markers = ['o', 's', '^'] 
sns.lineplot(data = coef_all[coef_all.com_label!='Total'], x = "abs_delta_VA", y = "new_coef", hue = "com_label", hue_order = hue_order, style = "com_label", 
             style_order = hue_order, linewidth=2, palette = color_order, markers = markers, ci = None)
# Add labels and legend
plt.xticks(ticks=[0, 8, 16, 24])
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('Spatial Bias (deg)')
plt.title("Fixed effect from Raw VAE - title to be deleted")
# Customize legend title
plt.legend(title='', loc = 'upper left')

# Save the plot
plt.savefig(os.path.join(work_path, "output/spatial_bias_raw_avg.png"), dpi=300)  # Adjust dpi for print quality
# Show the plot
plt.show()
del df_R_raw

########################
########################
### normalized R output
df_R_norm = pd.read_csv(os.path.join(R_path, 'coef_norm_VAE.csv'))

sns.lineplot(data = df_R_norm, x = "abs_delta_VA", y = "new_coef", hue = "com_label", hue_order = hue_order, style = "com_label", 
             style_order = hue_order, linewidth=2, palette = color_order, markers = markers, ci = None)
# Add labels and legend
plt.xticks(ticks=[0, 8, 16, 24])
plt.xlabel('Spatial disparity (V - A , deg)')
plt.ylabel('Spatial Bias')
plt.title("Fixed effect from Norm VAE - title to be deleted")
# Customize legend title
plt.legend(title='', loc = 'upper left')
# Save the plot
plt.savefig(os.path.join(work_path, "output/spatial_bias_norm.png"), dpi=300)  # Adjust dpi for print quality
# Show the plot
plt.show()


