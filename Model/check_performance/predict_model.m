function res = predict_model(bestP, stiPar, param_names, config, cond, out_name, full,force_0, numSim)

% select the best run
% [~, idx] = min(sub_data.minNLL);
% bestP = sub_data.estimatedP(idx,:);
if nargin <=8
    numSim = 500;
end
% update the full parameter set
for i = 1:length(param_names)
    stiPar.(param_names{i}) = bestP(i); 
end

%if the sigmas in two phases are the same
if config.same_var_2phase 
    stiPar.sig_A_A = stiPar.sig_A_AV;
    stiPar.sig_V_V = stiPar.sig_V_AV;
end 

n_cond = size(cond, 1);
nrep = 10; % repeat the simulation process several times so to reduce the variance caused by random seed (?)

% initiate
res_mat = NaN(n_cond*numSim*nrep, 15);

for irep = 1:nrep

   [predData, sim_post, sim_post_noise, post_C1, updatedShift_A, bi_xA, bi_xV, bi_sA_hat, bi_sV_hat] = simAllConds(config, stiPar, numSim, cond, force_0);
    
    % save results
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 1) = sim_post(:, 1);
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 2) = updatedShift_A;
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 3:9) = predData;
    
    % the full version for distribution plot
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 10) = bi_xA;
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 11) = bi_xV;
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 12) = bi_sA_hat;
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 13) = bi_sV_hat;
    if force_0
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 14) = sim_post_noise(:, 1);
    res_mat(n_cond*numSim*(irep-1)+1:n_cond*numSim*irep, 15) = post_C1;
    end
    
end

if ~full 
    res = array2table(res_mat(:, 1:9), 'VariableNames', {'prob', 'rec', 's_a', 's_v', 's_uni', 'tr_f', 'R_pc', 'R_conf', 'R_s'});
else
    res = array2table(res_mat, 'VariableNames', {'prob_dec', 'rec', 's_a', 's_v', 's_uni', 'tr_f', 'R_pc', 'R_conf', 'R_s', 'bi_xA', 'bi_xV', 'bi_sA_hat', 'bi_sV_hat' , 'prob_conf', 'prob_or'});
end
    
writetable(res, out_name)

end