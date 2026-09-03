function  NLL  = NLLsimAllConds(par, stiPar, param_names, config, nIntSamples, behData, cond)

% update the full parameter set
for i = 1:length(param_names)
    stiPar.(param_names{i}) = par(i); 
end

%if the sigmas in two phases are the same
if config.same_var_2phase 
    stiPar.sig_A_A = stiPar.sig_A_AV;
    stiPar.sig_V_V = stiPar.sig_V_AV;
end 

[predData, ~, ~, ~, ~, ~, ~, ~, ~] = simAllConds(config, stiPar, nIntSamples,cond, 0);

%%%%%%%%%%%%%%%%%%% part II %%%%%%%%%
%%% compute negtive loglikihood
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% for tasks in the bi-modal phases 
ncat = 2; % level of causal decisions
nr = 3; % level of confidence
% for tasks in the uni-modal phase
ns = 4; % level of spatial locations

NLL = 0;% init NLL

for cidx = 1:size(cond, 1) 
    %%%%%%%%%%for one condition%%%%%%%%%%
    % Extract condition values
    c_ = cond(cidx, :);
    cond_mask_pred = (predData(:, 1) == c_(1)) & (predData(:, 2) == c_(2)) & (predData(:, 3) == c_(3)) & (predData(:, 4) == c_(4));
    cond_mask_beh = (behData(:, 1) == c_(1)) & (behData(:, 2) == c_(2)) & (behData(:, 3) == c_(3)) & (behData(:, 4) == c_(4));
    pred_resp = predData(cond_mask_pred, 5:7);
    data_cond = behData(cond_mask_beh, 5:7);

    % joint NLL - causal decision * confidence * spatial location
    % Calculate predicted probabilities for each causal decision, confidence level and spatial locations
    % map the spatial locations into 1,2,3,4
    [~, pred_spatial_mapped] = ismember(pred_resp(:, 3), stiPar.resp_loc);
    pred_indices = sub2ind([ncat, nr, ns], pred_resp(:, 1), pred_resp(:, 2), pred_spatial_mapped);
    pMat_counts = accumarray(pred_indices, 1, [ncat * nr * ns, 1]);
    temp_probs = reshape(pMat_counts, [ncat, nr, ns])/ nIntSamples; 

    pMat = (1 - stiPar.laps) * temp_probs + stiPar.laps * (1 / (ncat * nr * ns));
    %pMat = max(pMat, eps);
    % normalize and make sure none is zero for later log computation
    pMat = pMat + eps;
    pMat = pMat/sum(pMat, 'all');

    % Calculate counts of trials for each causal decision and confidence level and each spatial location (real data)
    [~, data_spatial_mapped] = ismember(data_cond(:, 3), stiPar.resp_loc);
    data_indices = sub2ind([ncat, nr, ns], data_cond(:, 1), data_cond(:, 2), data_spatial_mapped);
    cntMat = reshape(accumarray(data_indices, 1, [ncat * nr * ns, 1]), [ncat, nr, ns]);

    % calc NLL
    NLL = -sum(cntMat .* log(pMat), 'all') + NLL; 

end % END FOR CONDITION

end%EOF