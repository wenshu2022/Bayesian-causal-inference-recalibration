import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.lines as mlines
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import scipy.io

## this script is to visualize the behaviour prob with predicted prob

pred_path = "C:/Users/wenlou/Documents/MATLAB/Prediction_est"
work_path = "C:/Users/wenlou/Documents/Python Scripts"
#data_path = "P:/3026008.01/Data/"
os.chdir(work_path)

data = dict()

locs = [-12, -4, 4, 12]
# input sub id and model id
m_lst = [25, 45]
sub_id = 1

for m_id in m_lst:
    mat_file_name = os.path.join(pred_path, 'm_' + str(m_id) + '_sub_' +str(sub_id) + '.mat' )
    data['m_'+str(m_id)] = scipy.io.loadmat(mat_file_name)
    
m_lbls = ['m_' + str(m_id) for m_id in m_lst] 
cond = data[m_lbls[0]]['cond']
condNLL = np.column_stack([data[m_lbls[0]]['condNLL'], data[m_lbls[1]]['condNLL']])

np.column_stack([data[m_lbls[0]]['NLL'], data[m_lbls[1]]['NLL']])


df_NLL = pd.DataFrame(index = range(cond.shape[0]*2))
df_NLL.loc[range(cond.shape[0]), 'm_lbl'] = m_lbls[0]
df_NLL.loc[range(cond.shape[0], cond.shape[0]*2) ,'m_lbl'] = m_lbls[1]

df_NLL.loc[range(cond.shape[0]), 'NLL'] = data[m_lbls[0]]['condNLL']
df_NLL.loc[range(cond.shape[0], cond.shape[0]*2) ,'NLL'] = data[m_lbls[1]]['condNLL']
df_NLL[['sa','sv','s_uni','aud_f']] = np.vstack((cond, cond))

aud_f = 0 # aud - 1; vis - 0
fig, axs = plt.subplots(nrows=4, ncols=4, figsize=(8, 8), gridspec_kw={'hspace': 0.4, 'wspace': 0.4})
for i in np.arange(4):
    for j in np.arange(4):
        sns.barplot(df_NLL.loc[(df_NLL.sa==locs[i]) & (df_NLL.sv==locs[j]) & (df_NLL.aud_f==aud_f)], x="s_uni", y="NLL", hue="m_lbl", ax = axs[i,j])
        axs[i,j].set_xlabel('')
        axs[i,j].set_ylabel('')

for ax in axs.flat:
    ax.legend().remove()
    
handles, labels = axs[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4, bbox_to_anchor=(0.2, 0), frameon=False)
# Show the plot
plt.tight_layout() 
plt.show()


### look int odetails of the two conditions
cond_p = [12, -4, 12, 1]
cidx = (cond==cond_p).all(axis=1)

detailNLL0 = np.squeeze(data[m_lbls[0]]['detailNLL'][cidx])
detailNLL1 = np.squeeze(data[m_lbls[1]]['detailNLL'][cidx]) 

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8, 8), gridspec_kw={'hspace': 0.2, 'wspace': 0.2})
for i in np.arange(2):
    for j in np.arange(3):
        #mini dataframe
        df_dll = pd.DataFrame({'NLL': np.append(detailNLL0[i,j,:], detailNLL1[i,j,:]), 'M_id': np.repeat(m_lbls, 4), 
                               'r_s': np.append(locs, locs)})
        sns.barplot(df_dll, x = 'r_s', y = 'NLL', hue = 'M_id', ax = axs[i,j])
        axs[i,j].set_xlabel('')
        axs[i,j].set_ylabel('')
for ax in axs.flat:
    ax.legend().remove()
handles, labels = axs[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4, bbox_to_anchor=(0.2, 0), frameon=False)
# Show the plot
plt.tight_layout() 
plt.show()

# beh against pred
detailBEH = np.squeeze(data[m_lbls[0]]['detailBEH'][cidx])
detailPRED0 = np.squeeze(data[m_lbls[0]]['detailPRED'][cidx])
detailPRED1 = np.squeeze(data[m_lbls[1]]['detailPRED'][cidx])

fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(8, 8), gridspec_kw={'hspace': 0.2, 'wspace': 0.3})
for i in np.arange(2):
    for j in np.arange(3):
        #mini dataframe
        df_dll = pd.DataFrame({'prob': np.concatenate((detailBEH[i,j,:], detailPRED0[i,j,:], detailPRED1[i,j,:])), 
                               'type': np.repeat(['beh', 'pred-' + m_lbls[0], 'pred-' + m_lbls[1]], 4), 
                               'r_s': np.concatenate((locs, locs,locs))})
        sns.barplot(df_dll, x = 'r_s', y = 'prob', hue = 'type', ax = axs[i,j])
        axs[i,j].set_xlabel('')
        axs[i,j].set_ylabel('')
        axs[i,j].set_ylim(0, 1)
for ax in axs.flat:
    ax.legend().remove()
handles, labels = axs[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', ncol=4, bbox_to_anchor=(0.2, 0), frameon=False)
# Show the plot
plt.tight_layout() 
plt.show()



