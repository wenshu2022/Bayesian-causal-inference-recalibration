clc;clearvars;

%define path 
rms_path = 'C:\Users\wenlou\Documents\MATLAB\rbms_Acerbi';
work_dir ='M:\MATLAB\Model\check_performance';
est_path = 'M:\MATLAB\Model\Fitting\\output\';

addpath(rms_path)
cd(work_dir)

% read subject list 
fileID = fopen('P:\3026008.01\data_for_fitting\sub_id_exp1.txt','r');
sub_lst = fscanf(fileID, '%f');
fclose(fileID);

% the model to be compared 
m_lst = [87:94, 70, 71, 73, 74];
% init a matrix, save all the AIC, BIC
n_model = numel(m_lst);
n_sub = numel(sub_lst);
res_mat = zeros(n_model * n_sub, 4);


for i = 1:n_model
    
    m_id = m_lst(i);
    res_mat((i-1)*n_sub+1:i*n_sub, 1) = zeros(n_sub, 1) + m_id;
    res_mat((i-1)*n_sub+1:i*n_sub, 2) = sub_lst';
    
    for j = 1:n_sub
        % read in the AIC and BIC
        sub_data = load(fullfile(est_path, ['m_' num2str(m_id) '_sub_' num2str(sub_lst(j)) '.mat' ]));
        [~, idx] = min(sub_data.minNLL);
        res_mat((i-1)*n_sub+j, 3) = sub_data.ev.AIC(idx);
        res_mat((i-1)*n_sub+j, 4) = sub_data.ev.BIC(idx);
    end
end


res_T = array2table(res_mat, 'VariableNames', {'m_id', 'sub_id', 'AIC', 'BIC'});

%writetable(res_T, 'AIC_BIC_update.csv')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% relative comparison
% transfor into n_sub * nmodel
AIC  = reshape(res_mat(ismember(res_T.m_id, m_lst), 3), n_sub, n_model);
BIC  = reshape(res_mat(ismember(res_T.m_id, m_lst), 4), n_sub, n_model);

% Run a "fixed effects" (FFX) analysis based on a sum across subjects
summed_AIC = sum(AIC);                                                       %Lower is better (because log-likelihoods were negated)             
summed_BIC = sum(BIC);                                                       
bootstrapFFX(-.5*AIC);                                                      %Note multiplication by -.5 to convert information criteria back to log-model-evidence
bootstrapFFX(-.5*BIC);                                                      %The bootstrap ensures that outlier participants are taken care of
    
% Run a "random effects" (RFX) analysis for AIC and BIC
bms_AIC = bms_Acerbi(-.5*AIC);                                              %Use David Meijer's bms_Acerbi function 
bms_BIC = bms_Acerbi(-.5*BIC);    

bms_BIC.bor
bms_BIC.pxp


model_config_tbl = readtable("M:\MATLAB\Model\m_config.xlsx");
[isInList, idxInTbl] = ismember(m_lst, model_config_tbl.m_id);
% Filter and reorder the table based on the indices
model_config_tbl_sel = model_config_tbl(idxInTbl(isInList), :);
%rename
model_config_tbl_sel.shift_update(strcmpi(model_config_tbl_sel.shift_update, 'FR')) = {'SCC'};
model_config_tbl_sel.C_readout(strcmpi(model_config_tbl_sel.C_readout, 'p')) = {'Bay'};
model_config_tbl_sel.C_readout(strcmpi(model_config_tbl_sel.C_readout, 'xdiff')) = {'xDiff'};
model_config_tbl_sel.Conf_readout(strcmpi(model_config_tbl_sel.Conf_readout, 'p')) = {'Bay'};
model_config_tbl_sel.Conf_readout(strcmpi(model_config_tbl_sel.Conf_readout, 'xdiff')) = {'xDiff'};

model_config_tbl_sel.recal_model(strcmpi(model_config_tbl_sel.shift_update, 'CI')) = ...
    strcat('Bay', model_config_tbl_sel.AV_readout(strcmpi(model_config_tbl_sel.shift_update, 'CI')));

model_config_tbl_sel.recal_model(~strcmpi(model_config_tbl_sel.shift_update, 'CI')) = model_config_tbl_sel.shift_update(~strcmpi(model_config_tbl_sel.shift_update, 'CI'));


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% factor comparison
num_factors = 3; 
% 1st factor: recalibration type : sensroy cue conflict and Causal inference Model averaging, CI Model selection
% 2nd factor: causal decision read-out : bayes, non-bayes xdiff
% 3rd factor: causal confidence read-out : bayes, non-bayes xdiff
num_factor_components = [3, 2, 2];
f_names = cell(1,num_factors);
f_names{1} = ["SCC", "BayMA", "BayMS"];
f_names{2} = ["Bay", "xDiff"];
f_names{3} = ["Bay", "xDiff"];
factor_names = ["Recalibration model", "Causal decision",  "Causal confidence"];


factors = cell(1,num_factors);
% 1st factor: recalibration type : sensroy cue conflict and CIMA, CIMS
factors{1} =[strcmp(model_config_tbl_sel.recal_model, f_names{1}{1})';strcmp(model_config_tbl_sel.recal_model, f_names{1}{2})'; strcmp(model_config_tbl_sel.recal_model, f_names{1}{3})'];
% 2nd factor: causal decision read-out : bayes, non-bayes xdiff
factors{2} =[strcmp(model_config_tbl_sel.C_readout, f_names{2}{1})';strcmp(model_config_tbl_sel.C_readout, f_names{2}{2})'];
% 3rd factor: causal  confidence read-out : bayes, non-bayes xdiff
factors{3} =[strcmp(model_config_tbl_sel.Conf_readout, f_names{3}{1})';strcmp(model_config_tbl_sel.Conf_readout, f_names{3}{2})'];

% Perform group-level Bayesian Model Factor Selection 
[~,bms_fac_AIC] = bms_Acerbi(-.5*AIC,factors);                              %Request the second output argument
[~,bms_fac_BIC] = bms_Acerbi(-.5*BIC,factors);   

% save data so that it can be plotted in py
jsonData = jsonencode(bms_fac_BIC);
fid = fopen('C:\Users\wenlou\Documents\Python Scripts\Figure2-modelCompare\bms_fac_BIC.json', 'w');
fprintf(fid, '%s', jsonData);
fclose(fid);

%save('C:\Users\wenlou\Documents\Python Scripts\Figure2-modelCompare\bms_fac_BIC.mat', 'bms_fac_BIC')

%simple plot
set(gcf,'position',[0,0,700,360])
t = tiledlayout(1,3);
for f_id = 1:3
 
    %FIGURE
    nexttile;
    bar( categorical(f_names{f_id}), bms_fac_BIC{f_id}.pxp, 0.4, 'k','DisplayName','Protected exceedance probability')
    hold on;
    errh = sqrt(diag(bms_fac_BIC{f_id}.cov_r))';
    er = errorbar(categorical(f_names{f_id}),bms_fac_BIC{f_id}.exp_r,errh,errh,  "-s","MarkerSize",5,'LineWidth',2,'DisplayName','Posterior frequencies');    
    er.Color = [.7 .7 .7];                            
    er.LineStyle = 'none';  
    er.CapSize = 0;
    %text(2, 1,'dy/dx = 0') Text add by ADOBE 
    hold off;
    % ax = gca;
    % ax.XAxis.FontSize = 14;
    % ax.YAxis.FontSize = 14;
    if f_id==2
        lgd = legend('boxoff');
        lgd.FontSize = 14;
        lgd.NumColumns = 2;
        lgd.Location = 'northoutside';
        %set(lgd, 'Position', [0.8, 1.2, 1.1, 1.1], 'Units', 'normalized');
    end
    ylabel('Probability','fontsize',14)
    ylim([0 1]);
    title(factor_names(f_id),'fontweight','bold','fontsize',14);
    set(gca, 'FontSize', 14, 'fontweight','bold');
    disp(['BOR = ' num2str(bms_fac_BIC{f_id}.bor)])
end

saveas(gcf, fullfile('C:\Users\wenlou\Documents\Python Scripts\plot4paper', 'factor_compare_update'), 'png');


% BOR = 1.1552e-08
% BOR = 0.79257
% BOR = 0.20015

% expected posterior model frequencies - EXP_R
% covariance matrix of posterior model - cov_r
% Bayesian Omnibus Risk - BOR
% protected exceedance probabilities - PXP








