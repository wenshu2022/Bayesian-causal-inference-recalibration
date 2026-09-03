function [predData, sim_post, sim_post_noise, post_C1, updatedShift_A, bi_xA, bi_xV, bi_sA_hat, bi_sV_hat] = simAllConds(config, stiPar, nIntSamples, cond, force_zero)


ncond = size(cond, 1);

varV = stiPar.sig_V_AV^2;
varA = stiPar.sig_A_AV^2;
varP = stiPar.sig_P^2;

% Variances of estimates given common or independent causes
varVA_hat = 1/(1/varV + 1/varA + 1/varP);
varV_hat = 1/(1/varV + 1/varP);
varA_hat = 1/(1/varA + 1/varP);

% Variances used in computing probability of common or independent causes
var_common = varV * varA + varV * varP + varA * varP;
varV_indep = varV + varP;
varA_indep = varA + varP;

% repmat the conditions so that it repeats several times for each conditions
cond_rep = reshape(repmat(cond', nIntSamples, 1), 4, [])';

bi_sA_remap =  cond_rep(:, 1) * stiPar.a_A + stiPar.b_A;
bi_sV_remap =  cond_rep(:, 2);    

bi_xA = bi_sA_remap + stiPar.sig_A_AV * randn(nIntSamples * ncond,1);
if force_zero
    bi_xV = bi_sV_remap + zeros(nIntSamples * ncond,1); % force x_v to be all zeros
else 
    bi_xV = bi_sV_remap + stiPar.sig_V_AV * randn(nIntSamples * ncond,1);
end

% Estimates given common or independent causes
bi_s_hat_common = (bi_xV/varV + bi_xA/varA + stiPar.mu_P/varP) * varVA_hat;
bi_sV_hat_indep = (bi_xV/varV + stiPar.mu_P /varP) * varV_hat;
bi_sA_hat_indep = (bi_xA/varA + stiPar.mu_P /varP) * varA_hat;

% Probability of common or independent causes
quad_common = (bi_xV-bi_xA).^2 * varP + (bi_xV-stiPar.mu_P).^2 * varA + (bi_xA-stiPar.mu_P).^2 * varV;
quadV_indep = (bi_xV-stiPar.mu_P).^2;
quadA_indep = (bi_xA-stiPar.mu_P).^2;

% Likelihood of observations (xV,xA) given C, for C=1 and C=2
likelihood_common = exp(-quad_common / (2*var_common)) / (2*pi*sqrt(var_common));
likelihoodV_indep = exp(-quadV_indep / (2*varV_indep)) / sqrt(2*pi*varV_indep);
likelihoodA_indep = exp(-quadA_indep / (2*varA_indep)) / sqrt(2*pi*varA_indep);
likelihood_indep =  likelihoodV_indep .* likelihoodA_indep;

% True Posterior probability of C given observations (xV,xA)
post_common = likelihood_common * stiPar.p_com;
post_indep = likelihood_indep * (1-stiPar.p_com);
post_C1 = post_common./(post_common + post_indep); % posterior prob of the  common judgement
sim_post = [post_C1, 1 - post_C1];


%% 1. read out of the location estimation (could be used in the next phase)
%% this happens before or after the decision noise

if strcmp(config.AV_readout, 'MA')% Overall estimates: weighted averages
    bi_sV_hat = post_C1 .* bi_s_hat_common + (1-post_C1) .* bi_sV_hat_indep;
    bi_sA_hat = post_C1 .* bi_s_hat_common + (1-post_C1) .* bi_sA_hat_indep;

elseif strcmp(config.AV_readout, 'MS')% Model selection
    bi_sV_hat=(post_C1>0.5).*bi_s_hat_common + (post_C1<=0.5).*bi_sV_hat_indep;
    bi_sA_hat=(post_C1>0.5).*bi_s_hat_common + (post_C1<=0.5).*bi_sA_hat_indep;

elseif strcmp(config.AV_readout, 'PM')% PROBABILITY MATCHING
    eta = rand(nIntSamples * ncond,1);
    bi_sV_hat=(post_C1>eta).*bi_s_hat_common + (post_C1<=eta).*bi_sV_hat_indep;
    bi_sA_hat=(post_C1>eta).*bi_s_hat_common + (post_C1<=eta).*bi_sA_hat_indep;

elseif strcmp(config.AV_readout, 'na')% the spatial estimate is not read-out (only for fixed-ratio model)
    bi_sA_hat = nan;
    bi_sV_hat = nan;
end

% Different ways to inject decision noise for bayes model
% sim_post for read out for causal decision - the name can be misleading as sim_post could also be noised.
% sim_post_noise for read-out of causal confidence 
if config.dec_noise_flag == 1 
    %Inject the same beta decision noise for both causal decision and causal confidence

    beta_c = 10^stiPar.logbeta; %Beta inference noise
    sim_post = gamrnd(sim_post * beta_c ,1);
    sim_post = sim_post./sum(sim_post, 2);
    sim_post_noise = sim_post; % the noise is add for both causal decision and confidence

elseif config.dec_noise_flag == 2 
    %Inject beta decision noise only for causal confidence

    beta_conf = 10^stiPar.logbeta_conf; %Beta inference noise
    sim_post_noise = gamrnd(sim_post * beta_conf ,1);
    sim_post_noise = sim_post_noise./sum(sim_post_noise, 2); % the noise is add for only confidence, keep the original 

elseif config.dec_noise_flag == -1
    % Inject different beta decision noise for causal confidence and causal confidence

    beta_c = 10^stiPar.logbeta; %Beta inference noise for causal decision
    beta_conf = 10^stiPar.logbeta_conf; %Beta inference noise for causal confidence
    %for confidence
    sim_post_noise = gamrnd(sim_post * beta_conf ,1);
    sim_post_noise = sim_post_noise./sum(sim_post_noise, 2); 

    % for causal decision
    sim_post = gamrnd(sim_post * beta_c ,1);
    sim_post = sim_post./sum(sim_post, 2);

else %config.dec_noise_flag=0

    % no decision noise for both 
    sim_post_noise = sim_post;
    
end


%% 2. read out of the casual decision
if strcmpi(config.C_readout, 'p') 
    % Bayesian posterior probability read-out : max posterior
    % a\) - causal decision read-out
    [~, bi_pC_resp] = max(sim_post,[],2); %MAX prob and casual decision
    resp(:, 1) = bi_pC_resp; % output 1 - response common (one) source; 2 - two (separate) source

else
    % Non-Bayesian read-out
    if strcmp(config.C_readout, 'xdiff')
    % measurement difference
        nb_c = abs(bi_xA - bi_xV);
    elseif strcmp(config.C_readout, 'sdiff')
    % spatial estimate difference
        nb_c = abs(bi_sA_hat - bi_sV_hat);
    end

    resp(:, 1) = (nb_c >= stiPar.epsilon) + 1; % output 1 - response common (one) source; 2 - two (separate) source
    
end


%% 3. read out of the casual confidence
if  strcmpi(config.Conf_readout, 'p') 

        % Bayesian posterior probability read-out : max posterior
        % b\) read out of the confidence level 
        %Get probability map given a set of stiPareter value
        if config.conf_b_nr==2
            k    = sort([0.49 stiPar.conf_bin_k1  stiPar.conf_bin_k2 Inf]);
            [sim_c_map, ~] = max(sim_post_noise,[],2); %MAX prob and casual decision
            simRespConf = discretize(sim_c_map, k);
            resp(:,2) = max(min(simRespConf,3),1); %prevent some numerical issue (if ever happens)
    
        elseif config.conf_b_nr==4
            %INIT 
            resp(:,2) = zeros(size(bi_pC_resp));
            [sim_c_map, ~] = max(sim_post_noise,[],2); %MAX prob and casual decision
            %disect the common verse separate cases and cal confidence separately. 
            resp_com = bi_pC_resp ==1;
    
            k1    = sort([0.49 stiPar.conf_bin_k1  stiPar.conf_bin_k2 Inf]);
            simRespConfCom = discretize(sim_c_map(resp_com), k1);
            resp(resp_com,2) = max(min(simRespConfCom,3),1);
    
            k2    = sort([0.49 stiPar.conf_bin_k3  stiPar.conf_bin_k4 Inf]);
            simRespConfNoCom = discretize(sim_c_map(~resp_com), k2);
            resp(~resp_com,2) = max(min(simRespConfNoCom,3),1);
    
        end
    
else
        % Non-Bayesian read-out
        if strcmp(config.Conf_readout, 'xdiff')
        % measurement difference
            nb_c = abs(bi_xA - bi_xV);
        elseif strcmp(config.Conf_readout, 'sdiff')
        % spatial estimate difference
            nb_c = abs(bi_sA_hat - bi_sV_hat);
        end
           
        abs_dist = abs(nb_c - stiPar.epsilon); % the abs distance between the threshold epsilon and the measurement/estimate difference
    
        % confidence
        if config.conf_b_nr==2
            k    = sort([0 stiPar.conf_bin_k1  stiPar.conf_bin_k2 stiPar.epsilon]);
            simRespConf = discretize(abs_dist, k);
            resp(:,2) = max(min(simRespConf,3),1); %prevent some numerical issue (if ever happens)
            %0<=k1<=k2<=epsilon
    
        elseif config.conf_b_nr==4
            % more bins
            %INIT 
            resp(:,2) = zeros(size(nb_c));
            
            %disect the common verse separate cases and cal confidence separately. 
            resp_com = resp(:, 1) ==1;
    
            k1    = sort([0 stiPar.conf_bin_k1  stiPar.conf_bin_k2 stiPar.epsilon]);
            simRespConfCom = discretize(abs_dist(resp_com), k1);
            resp(resp_com,2) = max(min(simRespConfCom,3),1);
    
            k2    = sort([0 stiPar.conf_bin_k3  stiPar.conf_bin_k4 Inf]);
            simRespConfNoCom = discretize(abs_dist(~resp_com), k2);
            resp(~resp_com,2) = max(min(simRespConfNoCom,3),1);
    
            %0<=k1<=k2<=epsilon and 0<=k3<=k4
        end  

end


%%% update shift 
if strcmp(config.shift_update, 'FR')
    updatedShift_A =  stiPar.alp_shift_A * (bi_xV - bi_xA); 
    updatedShift_V =  stiPar.alp_shift_V * (bi_xA - bi_xV); 

elseif strcmp(config.shift_update, 'CI')
    updatedShift_A =  stiPar.alp_shift_A * (bi_sA_hat - bi_xA); 
    updatedShift_V =  stiPar.alp_shift_V * (bi_sV_hat - bi_xV);

else 
    updatedShift_A = zeros(size(bi_xA));
    updatedShift_V = zeros(size(bi_xV));
end

% visual bias - not included in the final model
if strcmpi(config.vs, 'xv')
    new_mu = stiPar.mu_P + stiPar.alpha_vs * bi_xV;
elseif strcmpi(config.vs, 'sa')
    new_mu = stiPar.mu_P + stiPar.alpha_vs * bi_sA_hat;
elseif strcmpi(config.vs, 'sv')
    new_mu = stiPar.mu_P + stiPar.alpha_vs * bi_sV_hat;
elseif strcmpi(config.vs, 'sav')
    bi_sAV = (bi_sA_hat + bi_sV_hat) /2;
    new_mu = stiPar.mu_P + stiPar.alpha_vs * bi_sAV;
elseif strcmpi(config.vs, '') % no visual bias
    new_mu = repmat(stiPar.mu_P, size(bi_xA));
end

%%% the uni-modal phase
% for auditory blocks
cond_aud = cond_rep(:, 4)==1;
n_cond_aud = sum(cond_aud);
if ~strcmp(config.shift_update, 'FR_CF')
    %uni_sA_remap =  cond_rep(cond_aud ,3) * stiPar.a_A +  stiPar.b_A + updatedShift_A(cond_aud);
    if config.sato==1
        uni_sA_remap =  (1-stiPar.alp_shift_A) .* (cond_rep(cond_aud ,3) * stiPar.a_A +  stiPar.b_A) + updatedShift_A(cond_aud);
    else
        uni_sA_remap =  cond_rep(cond_aud ,3) * stiPar.a_A +  stiPar.b_A + updatedShift_A(cond_aud);
    end
    %mu_sA_hat = (uni_sA_remap / (stiPar.sig_A_A^2) + stiPar.mu_P / varP ) / (1/varP + 1/(stiPar.sig_A_A^2));
    mu_sA_hat = (uni_sA_remap / (stiPar.sig_A_A^2) + new_mu(cond_aud) / varP ) / (1/varP + 1/(stiPar.sig_A_A^2));
    var_sA_hat = ((1/varP + 1/(stiPar.sig_A_A^2))^2) / (stiPar.sig_A_A^2);
    uni_sA_hat = normrnd(mu_sA_hat, sqrt(var_sA_hat));
    
    %find the response location closest to sV_hat and
    %sA_hat, ie with minimum deviation
    [~,tA]=min(abs(repmat(uni_sA_hat,1,stiPar.resp_loc_len) - repmat(stiPar.resp_loc, n_cond_aud, 1)),[],2);
    resp(cond_aud,3)=stiPar.resp_loc(tA);

elseif strcmp(config.shift_update, 'FR_CF') % closed form solution
    uni_sA_remap =  cond_rep(cond_aud ,3) * stiPar.a_A +  stiPar.b_A;
    %uni_sA_remap =  (1-stiPar.alp_shift_A) .* (cond_rep(cond_aud ,3) * stiPar.a_A +  stiPar.b_A) + updatedShift_A(cond_aud);
    w_a = (stiPar.sig_A_A^(-2))/ (stiPar.sig_P^(-2) + stiPar.sig_A_A^(-2));
    w_p = (stiPar.sig_P^(-2))/ (stiPar.sig_P^(-2) + stiPar.sig_A_A^(-2));
    mu_resp = w_a * (uni_sA_remap + stiPar.alp_shift_A * (cond_rep(cond_aud, 2) - cond_rep(cond_aud, 1))) + w_p * stiPar.mu_P;
    var_resp = (w_a^2) * (stiPar.alp_shift_A^2) * (stiPar.sig_V_AV^2 + stiPar.sig_A_AV^2) + ...
        w_a/(stiPar.sig_A_A^(-2) + stiPar.sig_P^(-2));
    uni_sA_hat = mu_resp + sqrt(var_resp) * randn(n_cond_aud, 1);
    [~,tA]=min(abs(repmat(uni_sA_hat,1,stiPar.resp_loc_len) - repmat(stiPar.resp_loc, n_cond_aud, 1)),[],2);
    resp(cond_aud,3)=stiPar.resp_loc(tA);

end

% for visual blocks
cond_vis = cond_rep(:,4)==0;
if config.sato==1
    uni_sV_remap =  (1-stiPar.alp_shift_V) .* cond_rep(cond_vis ,3) + updatedShift_V(cond_vis);
else
    uni_sV_remap =  cond_rep(cond_vis ,3) + updatedShift_V(cond_vis);
end
%mu_sV_hat = (uni_sV_remap / (stiPar.sig_V_V^2) + stiPar.mu_P / varP ) / (1/varP + 1/(stiPar.sig_V_V^2));
mu_sV_hat = (uni_sV_remap / (stiPar.sig_V_V^2) + new_mu(cond_vis) / varP ) / (1/varP + 1/(stiPar.sig_V_V^2));
var_sV_hat = ((1/varP + 1/(stiPar.sig_V_V^2))^2) / (stiPar.sig_V_V^2);
uni_sV_hat = normrnd(mu_sV_hat, sqrt(var_sV_hat));

%find the response location closest to sV_hat and
%sA_hat, ie with minimum deviation
[~,tV]=min(abs(repmat(uni_sV_hat,1,stiPar.resp_loc_len) - repmat(stiPar.resp_loc, sum(cond_vis), 1)),[],2);
resp(cond_vis,3)=stiPar.resp_loc(tV);

predData = [cond_rep, resp];

end

% helper function
% function y = logit(p)
%     % Ensure p is strictly between 0 and 1 to avoid log(0) or division by zero
%     eps_val = 1e-10;
%     p = min(max(p, eps_val), 1 - eps_val);
%     y = log(p ./ (1 - p));
% end
function y = sigmoid(x, k, L)
    y = L ./ (1 + exp(-x .* k));
end