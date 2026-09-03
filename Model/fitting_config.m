function [stiPar, param_names, lb, ub, plb, pub, nonbcon] = fitting_config(config, stiPar)

%% set the range of tunable parameters and the value of non-tunable parameters
if  config.NLL_ty ~= 4
    error('Not the new fitting function')

% Bayesian confidence /decision with same decision noise
elseif (config.dec_noise_flag==1) && strcmpi(config.Conf_readout, 'p') && strcmpi(config.C_readout, 'p') && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && ismissing(config.vs)

    % non-tuning pars
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;

    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'logbeta', 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2'};  
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A ( same for bi- and uni- modal phases )
    % par(2)             :  sigma V ( same for bi- and uni- modal phases )
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  decision noise (log10(beta) here) - for bayes: causal decision
    % par(7)             :  the constant shift b_A
    % par(8)             :  learning rates, \alpha_V
    % par(9) - par(10)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,     1,    -3,  -4,  1e-8, 0.5, 0.5];
    ub =  [  24,    4,    1.5, 1-1e-4,    60,     3,   4,  0.06,   1,   1];
    plb = [   4,    1,   1e-4,    0.3,     5,  -0.5,  -2,  1e-8, 0.5, 0.7];
    pub = [  20,    2,    0.8,    0.7,    30,   1.5,   1,  1e-2, 0.7,   1];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,9) > x(:,10);

% Bayesian confidence /decision with different decision noise
elseif (config.dec_noise_flag==-1) && strcmpi(config.Conf_readout, 'p') && strcmpi(config.C_readout, 'p') && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && ismissing(config.vs)

    % non-tuning pars
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;

    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'logbeta', 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2', 'logbeta_conf'};  
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A ( same for bi- and uni- modal phases )
    % par(2)             :  sigma V ( same for bi- and uni- modal phases )
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  decision noise (log10(beta) here) - for bayes: causal decision
    % par(7)             :  the constant shift b_A
    % par(8)             :  learning rates, \alpha_V
    % par(9) - par(10)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % par(11)             :  decision noise (log10(beta) here) - for bayes: causal confidence
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,     1,    -3,  -4,  1e-8, 0.5, 0.5,    -3];
    ub =  [  24,    4,    1.5, 1-1e-4,    60,     3,   4,  0.06,   1,   1,     3];
    plb = [   4,    1,   1e-4,    0.3,     5,  -0.5,  -2,  1e-8, 0.5, 0.7,  -0.5];
    pub = [  20,    2,    0.8,    0.7,    30,   1.5,   1,  1e-2, 0.7,   1,   1.5];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,9) > x(:,10);

% Bayesian confidence and non-bayesian decision
elseif (config.dec_noise_flag==1) && strcmpi(config.Conf_readout, 'p') && (~strcmpi(config.C_readout, 'p')) && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && ismissing(config.vs)

    % non-tuning pars
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;

    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'logbeta', 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2', 'epsilon'};  
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A ( same for bi- and uni- modal phases )
    % par(2)             :  sigma V ( same for bi- and uni- modal phases )
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  decision noise (log10(beta) here) - for bayes: causal decision
    % par(7)             :  the constant shift b_A
    % par(8)             :  learning rates, \alpha_V
    % par(9) - par(10)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % par(11)               : epsilon - for non-bayes causal decision
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,     1,    -3,  -4,  1e-8, 0.5, 0.5, 1e-1];
    ub =  [  24,    4,    1.5, 1-1e-4,    60,     3,   4,  0.06,   1,   1,   24];
    plb = [   4,    1,   1e-4,    0.3,     5,  -0.5,  -2,  1e-8, 0.5, 0.7,    1];
    pub = [  20,    2,    0.8,    0.7,    30,   1.5,   1,  1e-2, 0.7,   1,   24];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,9) > x(:,10);

% bayesian decision and non-bay confidence
elseif (config.dec_noise_flag==1) && (~strcmpi(config.Conf_readout, 'p')) && strcmpi(config.C_readout, 'p') && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && ismissing(config.vs)
    % non-tuning pars
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;

    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'epsilon', 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2', 'logbeta'}; 
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A (same for bi- and uni- modal phases) p(1)>p(2)
    % par(2)             :  sigma V (same for bi- and uni- modal phases)
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  epsilon - for non-bayes causal confidence p(10)<=p(6)
    % par(7)             :  the constant shift b_A
    % par(8)             :  learning rates, \alpha_V
    % par(9) - par(10)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % par(11)             :  decision noise (log10(beta) here) - for bayes: causal decision
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,     1,  1e-1,  -4,  1e-8, 1e-1, 1e-1,    -3];
    ub =  [  24,    4,    1.5, 1-1e-4,    60,    24,   4,  0.06,   24,   24,     3];
    plb = [   4,    1,   1e-4,    0.3,     5,     1,  -2,  1e-8,    1,    1,  -0.5];
    pub = [  20,    2,    0.8,    0.7,    30,    24,   1,  1e-2,   24,   24,   1.5];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,9) > x(:,10) | x(:,10) > x(:,6);

% non-bay decision and confidence
elseif (config.dec_noise_flag==0) && (~strcmpi(config.Conf_readout, 'p')) && (~strcmpi(config.C_readout, 'p')) && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && ismissing(config.vs)

     % non-tuning pars
     stiPar.a_A                  =        1; 
     stiPar.mu_P                 =        0;
     %stiPar.alp_shift_V          =        0;
     stiPar.laps                 =        0.01;
 
     % tuning par
     param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'epsilon', 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2'}; 
     %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
     % bounded par
     % free parameters for the fitting
     % --------------------------------------------------------
     % par(1)             :  sigma A (same for bi- and uni- modal phases) p(1)>p(2)
     % par(2)             :  sigma V (same for bi- and uni- modal phases)
     % par(3)             :  learning rates, \alpha_A
     % par(4)             :  prior probability of a common cause
     % par(5)             :  the spatial prior sigma P 
     % par(6)             :  epsilon - for non-bayes causal confidence p(10)<=p(6)
     % par(7)             :  the constant shift b_A
     % par(8)             :  learning rates, \alpha_V
     % par(9) - par(10)    :  confidence bound 1 and 2 with (p(9) <= p(10))
     % --------------------------------------------------------
     lb =  [1e-1, 1e-3,   1e-8,   1e-4,     1,  1e-1,  -4,  1e-8, 1e-1, 1e-1];
     ub =  [  24,    4,    1.5, 1-1e-4,    60,    24,   4,  0.06,   24,   24];
     plb = [   4,    1,   1e-4,    0.3,     5,     1,  -2,  1e-8,    1,    1];
     pub = [  20,    2,    0.8,    0.7,    30,    24,   1,  1e-2,   24,   24];
 
     % non bonunded conditions
     % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
     nonbcon = @(x) x(:,1) < x(:,2) | x(:,9) > x(:,10) | x(:,10) > x(:,6);

% bay confidence and decision with only noise on confidence 
elseif (config.dec_noise_flag==2) && strcmpi(config.Conf_readout, 'p') && strcmpi(config.C_readout, 'p') && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && ismissing(config.vs) % Bayesian confidence 

    % non-tuning pars
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;
    
    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'logbeta', 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2'};  
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A ( same for bi- and uni- modal phases )
    % par(2)             :  sigma V ( same for bi- and uni- modal phases )
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  decision noise (log10(beta) here) - for bayes: causal confidence
    % par(7)             :  the constant shift b_A
    % par(8)             :  learning rates, \alpha_V
    % par(9) - par(10)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,     1,    -3,  -4,  1e-8, 0.5, 0.5];
    ub =  [  24,    4,    1.5, 1-1e-4,    60,     3,   4,  0.06,   1,   1];
    plb = [   4,    1,   1e-4,    0.3,     5,  -0.5,  -2,  1e-8, 0.5, 0.7];
    pub = [  20,    2,    0.8,    0.7,    30,   1.5,   1,  1e-2, 0.7,   1];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,9) > x(:,10);

% bay confidence and decision with zero noise
elseif (config.dec_noise_flag==0) && strcmpi(config.Conf_readout, 'p') && strcmpi(config.C_readout, 'p') && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && ismissing(config.vs) % Bayesian confidence 

    % non-tuning pars
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;
    
    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2'};  
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A ( same for bi- and uni- modal phases )
    % par(2)             :  sigma V ( same for bi- and uni- modal phases )
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  the constant shift b_A
    % par(7)             :  learning rates, \alpha_V
    % par(8) - par(9)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,   1, -4,  1e-8, 0.5, 0.5];
    ub =  [  24,    4,    1.5, 1-1e-4,  60,  4,  0.06,   1,   1];
    plb = [   4,    1,   1e-4,    0.3,   5, -2,  1e-8, 0.5, 0.7];
    pub = [  20,    2,    0.8,    0.7,  30,  1,  1e-2, 0.7,   1];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,8) > x(:,9);

elseif  (config.dec_noise_flag==1) && strcmpi(config.Conf_readout, 'p') && strcmpi(config.C_readout, 'p') && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && (~ismissing(config.vs))% visual bias model 
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;

    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'logbeta', 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2', 'alpha_vs'};  
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A ( same for bi- and uni- modal phases )
    % par(2)             :  sigma V ( same for bi- and uni- modal phases )
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  decision noise (log10(beta) here) - for bayes: causal decision
    % par(7)             :  the constant shift b_A
    % par(8)             :  learning rates, \alpha_V
    % par(9) - par(10)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % par(11)             : alpha for visual bias
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,     1,    -3,  -4,  1e-8, 0.5, 0.5, 1e-8];
    ub =  [  24,    4,    1.5, 1-1e-4,    60,     3,   4,  0.06,   1,   1,    1];
    plb = [   4,    1,   1e-4,    0.3,     5,  -0.5,  -2,  1e-8, 0.5, 0.7, 1e-4];
    pub = [  20,    2,    0.8,    0.7,    30,   1.5,   1,  1e-2, 0.7,   1,  0.5];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,9) > x(:,10);

elseif (config.dec_noise_flag==-1) && strcmpi(config.Conf_readout, 'p') && strcmpi(config.C_readout, 'p') && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && (~ismissing(config.vs))

    % non-tuning pars
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;

    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'logbeta', 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2', 'logbeta_conf', 'alpha_vs'};  
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A ( same for bi- and uni- modal phases )
    % par(2)             :  sigma V ( same for bi- and uni- modal phases )
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  decision noise (log10(beta) here) - for bayes: causal decision
    % par(7)             :  the constant shift b_A
    % par(8)             :  learning rates, \alpha_V
    % par(9) - par(10)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % par(11)             :  decision noise (log10(beta) here) - for bayes: causal confidence
    % par(12)             : alpha for visual bias
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,     1,    -3,  -4,  1e-8, 0.5, 0.5,    -3, 1e-8];
    ub =  [  24,    4,    1.5, 1-1e-4,    60,     3,   4,  0.06,   1,   1,     3,    1];
    plb = [   4,    1,   1e-4,    0.3,     5,  -0.5,  -2,  1e-8, 0.5, 0.7,  -0.5, 1e-4];
    pub = [  20,    2,    0.8,    0.7,    30,   1.5,   1,  1e-2, 0.7,   1,   1.5,  0.5];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,9) > x(:,10);

elseif (config.dec_noise_flag==0) && strcmpi(config.Conf_readout, 'p') && strcmpi(config.C_readout, 'p') && config.long_term_ef && config.free_alp_V && (config.conf_b_nr==2) && (~ismissing(config.vs))% Bayesian confidence 

    % non-tuning pars
    stiPar.a_A                  =        1; 
    stiPar.mu_P                 =        0;
    %stiPar.alp_shift_V          =        0;
    stiPar.laps                 =        0.01;
    
    % tuning par
    param_names = {'sig_A_AV', 'sig_V_AV' , 'alp_shift_A', 'p_com', 'sig_P' , 'b_A', 'alp_shift_V', 'conf_bin_k1', 'conf_bin_k2', 'alpha_vs'};  
    %% NOTE! The order of param_names, par and lb/ub/plb/pub should be the same!
    % bounded par
    % free parameters for the fitting
    % --------------------------------------------------------
    % par(1)             :  sigma A ( same for bi- and uni- modal phases )
    % par(2)             :  sigma V ( same for bi- and uni- modal phases )
    % par(3)             :  learning rates, \alpha_A
    % par(4)             :  prior probability of a common cause
    % par(5)             :  the spatial prior sigma P 
    % par(6)             :  the constant shift b_A
    % par(7)             :  learning rates, \alpha_V
    % par(8) - par(9)    :  confidence bound 1 and 2 with (p(9) <= p(10))
    % par(10)             : alpha for visual bias
    % --------------------------------------------------------
    lb =  [1e-1, 1e-3,   1e-8,   1e-4,   1, -4,  1e-8, 0.5, 0.5, 1e-8];
    ub =  [  24,    4,    1.5, 1-1e-4,  60,  4,  0.06,   1,   1,    1];
    plb = [   4,    1,   1e-4,    0.3,   5, -2,  1e-8, 0.5, 0.7, 1e-4];
    pub = [  20,    2,    0.8,    0.7,  30,  1,  1e-2, 0.7,   1,  0.5];

    % non bonunded conditions
    % the first condition, because our visual signals are highly reliable, the plausible variance should be p(1) >= p(2);
    nonbcon = @(x) x(:,1) < x(:,2) | x(:,8) > x(:,9);

else

    error('invalid model number input!')

end

end % EOF
