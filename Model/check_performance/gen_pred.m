clc;clear;
work_dir ='M:\MATLAB\Model\check_performance';
est_par_path = 'M:\MATLAB\Model\Fitting\output';
out_path = 'C:\Users\wenlou\Documents\MATLAB\Prediction';
cd(work_dir)
addpath('..')

% the condition combo - shared for all models
resp_loc = [-12, -4, 4, 12];
resp_loc_len = length(resp_loc);
cond_A = [combvec(resp_loc, resp_loc, resp_loc)' ones(resp_loc_len *resp_loc_len *resp_loc_len , 1)]; % [A in AV, V in AV, A/V in uni, A(1) or V(0) block]
cond_V = [combvec(resp_loc, resp_loc, resp_loc)' zeros(resp_loc_len *resp_loc_len *resp_loc_len , 1)]; % [A in AV, V in AV, A/V in uni, A(1) or V(0) block]
cond = [cond_A; cond_V];
  
m_id = 70; 

% get model configuration
[config, stiPar, ~, ~] = model_config('..', 0, m_id, 0);

[stiPar, param_names, ~, ~, ~, ~, ~] = fitting_config(config, stiPar);


% read subject list 
fileID = fopen('P:\3026008.01\data_for_fitting\sub_id_exp1.txt','r');
sub_lst = fscanf(fileID, '%f');
fclose(fileID);


%% 2nd step: generate prediction
if isfolder([out_path '\m' num2str(m_id)])
    rmdir([out_path '\m' num2str(m_id)], 's'); 
end
mkdir([out_path '\m' num2str(m_id)]);

for i = 1:numel(sub_lst)
   sub_data = load(fullfile(est_par_path, ['m_' num2str(m_id) '_sub_' num2str(sub_lst(i)) '.mat' ]));
   % select the best run
   [~, idx] = min(sub_data.minNLL);
   bestP = sub_data.estimatedP(idx,:);
   save_name = fullfile(out_path, ['m' num2str(m_id)], ['pred_sub_' num2str(sub_lst(i)) '.csv']);
   res = predict_model(bestP, stiPar, param_names, config, cond, save_name, 0, 0, 100);
end





