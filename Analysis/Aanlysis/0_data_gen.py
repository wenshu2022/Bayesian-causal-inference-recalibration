# -*- coding: utf-8 -*-
"""
Created on Fri Jan 26 14:01:33 2024

@author: wenlou
"""

## read in the subject for a certain experiment 
# importing the module 
import ast 
import pandas as pd
import numpy as np
import os
import pickle

abspath = os.path.abspath("__file__")
dname = os.path.dirname(abspath)
os.chdir(dname)

# reading the data from the file 
with open('sub_id_4_exp.txt') as f: 
    data = f.read() 
  
print("Data type before reconstruction : ", type(data))       
# reconstructing the data as a dictionary 
dict_sub_id_for_exp = ast.literal_eval(data) 
  
print("Data type after reconstruction : ", type(dict_sub_id_for_exp)) 
print(dict_sub_id_for_exp) 

## data path
data_path = "P:/3026008.01/Data/"
## experiment id 
exp_id = 1
key_id = 'exp'+str(exp_id)

# first extract the sub id base on the key word, then convert it into numeric array.
sub_id_lst = list(map(int, dict_sub_id_for_exp[key_id]))

#save 
# with open(os.path.join(data_path, "exp1_sub_lst.pkl"), 'wb') as f:
#     pickle.dump(sub_id_lst, f)
    

dfs = []
### read in data for all subject 
for sub_id in sub_id_lst:
    ## subject id  
    sub_path = data_path+'Subj_' + str(sub_id)+'/exp'+str(exp_id)
    filename = 'Subj' + str(sub_id)+'_exp'+ str(exp_id)+'_BehTabl.csv'
    sub_file = os.path.join(sub_path, filename)

    # Load the CSV file into a Pandas DataFrame
    df_sub = pd.read_csv(sub_file)
    df_sub['sub_id'] = sub_id
    dfs.append(df_sub)
    
df_all = pd.concat(dfs)    


df_all.shape
df_all.head(10)

## seperate the visual and auditory data frame

df_A = df_all[df_all['taskAV']=='A']
df_V = df_all[df_all['taskAV']=='V']


## save two dataframes seperately.
df_A.to_pickle(os.path.join(data_path, "exp1_A_all.pkl"))  
df_V.to_pickle(os.path.join(data_path, "exp1_V_all.pkl"))  


## also save csv
df_A = pd.read_pickle(os.path.join(data_path, "exp1_A_all.pkl"))
df_V = pd.read_pickle(os.path.join(data_path, "exp1_V_all.pkl"))

df_A.to_csv(os.path.join(data_path, "exp1_A_all.csv"), index = False )
df_V.to_csv(os.path.join(data_path, "exp1_V_all.csv"), index = False)





