function [sub_id, m_id, estimatedP, minNLL, ev] = fit_for_individual(sub_id, m_id, num_runs)

if nargin<3
    num_runs = 30;
end

work_dir ='C:\Users\wenlou\Documents\01.Projects\1.Recalibration\Writing_final\Code\Model\Fitting';
bads_path = 'M:\MATLAB\Model\bads-master';
data_path = 'P:\3026008.01\data_for_fitting';

cd(work_dir)
addpath('..')
addpath(bads_path)


% load subject data
sub_file = fullfile(data_path, ['Subj' num2str(sub_id) '_exp1_Beh_fit.mat']);
load(sub_file, 'behData');

numSim=10000;% number of simulation
[config, stiPar, ~, ~] = model_config('..', 0, m_id, 0);

%The combo of all conds
cond_A = [combvec(stiPar.resp_loc, stiPar.resp_loc, stiPar.resp_loc)' ones(stiPar.resp_loc_len *stiPar.resp_loc_len *stiPar.resp_loc_len , 1)]; % [A in AV, V in AV, A/V in uni, A(1) or V(0) block]
cond_V = [combvec(stiPar.resp_loc, stiPar.resp_loc, stiPar.resp_loc)' zeros(stiPar.resp_loc_len *stiPar.resp_loc_len *stiPar.resp_loc_len , 1)]; % [A in AV, V in AV, A/V in uni, A(1) or V(0) block]
cond = [cond_A; cond_V];

% set fitting configuration
[stiPar, param_names, lb, ub, plb, pub, nonbcon] = fitting_config(config, stiPar);
%%%%%%%%%%%%%%%%%


k=length(plb);%number of parameters

%num_runs = 1;
minNLL          = NaN(1, num_runs);
estimatedP      = NaN(num_runs, k);

objFunc = @(x)NLLsimAllConds(x, stiPar, param_names, config, numSim, behData, cond);


disp(['----------------START subject id : ' num2str(sub_id) '  ------------------------']);

for i = 1:num_runs

    disp(['----------------START run : ' num2str(i) '  ------------------------']);

    % init par0
    %rng(sub_id+ i*100);
    randseed = rand(1,k);
    par0 = plb + randseed.*(pub-plb);
    par0(1:2) = sort(par0(1:2), 'descend');
    par0(6:7) = sort(par0(6:7));
    if ~strcmpi(config.Conf_readout, 'p') 
        par0(6:8) = sort(par0(6:8));
    end
    disp('initial par: ');
    disp(par0)

    options = bads('defaults');
    options.UncertaintyHandling = true;
    options.MaxIter=150;
    try
        tic
        [estimatedP(i,:), minNLL(i), ~, ~] = bads(objFunc,par0,lb,ub,plb,pub,nonbcon, options);      
        toc

        disp('estimated par: ');
        disp(estimatedP);
        disp(['NLL: ' num2str(round(minNLL,4))]);
        % disp('The returned OUTPUT structure is:');
        % output

    catch
        disp('Error!')
    end

    disp(['----------------END run : ' num2str(i) '  ------------------------']);

end% end run

disp(['----------------END subject id : ' num2str(sub_id) '  ------------------------']);

ev.AIC = 2*(k + minNLL);
ev.BIC = k * log(size(behData, 1)) + 2 * minNLL;

end