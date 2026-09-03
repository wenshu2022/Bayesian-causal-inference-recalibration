%%%%%%%%%%%%%%%%%%
%%% Initialize %%% 
%%%%%%%%%%%%%%%%%%

delete(findobj(allchild(0), '-regexp', '3', '^Msgbox_'))                  %close all Message/Warning/Error boxes
close all;                                                                  %close all open figures
clear variables;                                                                  %clear all variables in the workspace
fclose('all');                                                              %close all open files (that were previously opened by MATLAB)
clc;                                                                        %clear the text in the command window                                     
sca;

%%%set something for 
%for testing - disable for the real stuff
Screen('Preference', 'SkipSyncTests', 1);

% set the verbosity level for PTB: level 2 or 3 for debugging;  level 0 or 1 for real experiments
level  = 2;
Screen('Preference', 'Verbosity', level);
% Seed the random number generator. Here we use the an older way to be
% compatible with older systems.
rng('shuffle');

%Are we testing the scripts for AVsynchrony or the stimuli velocity? (normally not!)
add_flag.testAVsynchrony = 0; % store all the additional flag in add_flag

%%%get relative
set_path;
%add_flag.new_par=1;
Stimuli = DefinePresent;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Set Subj_nr, task and main conditions %%% 
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

if ~add_flag.testAVsynchrony 

	[SubjectData, F] = SetSubjIDandTask(pwd);                %This is an interactive function defining experiment nr, session nr, subject id , etc. 

	% the output of trial_design.trial_order is a 5 * ntrial matrix
	% for experiment 1
	% 1st row: move type - exp1 static (1)
	% 2nd row: Auditory location in AV phase
	% 3rd row: Visual location in AV phase 
	% 4th row: Auditory/visual location in A/V phase
	% 5th row: 1 - AV-A Trial; 2 - AV-V Trial
	% 6th row: block number
	
	% for experiment 2 - increasing/decreasing move
	% 1st row: move type - exp2 dynamic (2)
	% 2nd row: Auditory location in AV phase
	% 3rd row: disparity change type : 1 - increasing; 2 - decreasing; 
	% 4th row: Auditory/visual location in A/V phase
	% 5th row: 1 - AV-A Trial; 2 - AV-V Trial
	% 6th row: block number
	
	% for experiment 2 - crossing type
	% 1st row: move type - exp2 dynamic crossing (3)
	% 2nd row: Auditory location in AV phase
	% 3rd row: AV displacement 1 - VA, 2 - AV. (starting dispalcement) x
	% 4th row: Auditory/visual location in A/V phase
	% 5th row: 1 - AV-A Trial; 2 - AV-V Trial
	% 6th row: block number
	
	% for experiment 2 - congruent
	% 1st row: move type - static and congruent (4)
	% 2nd row: Auditory location in AV phase
	% 3rd row: visual location in AV phase (same as A)
	% 4th row: Auditory/visual location in A/V phase
	% 5th row: 1 - AV-A Trial; 2 - AV-V Trial
	% 6th row: block number
	
	% NOTE:
	%% for the common source question, we counterbalance the displacement of yes and no in left/right hands
	%% for even number mod(x,2)==0, the displacement is left-yes, right-no
	%% for odd number mod(x,2)==1, the displacement is right-yes, left-no

	add_flag.odd_flag = mod(str2double(SubjectData.sub_id), 2);

	if  strcmp(SubjectData.exp_type, 'train') % traning session 

		%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		%%%%%%%training session%%%%%
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%

		% Make sure we're running on PTB-3
		AssertOpenGL;

		%Debug?
		%PsychDebugWindowConfiguration;
		eye_par.dummymode = 1;
		%load the training program. 
		R = train_session(Stimuli, SubjectData.tr_nr, add_flag.odd_flag);

	else % 
		
		if strcmp(SubjectData.exp_type, 'prac') 
			
			%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			%%%%%%%for demonstration/practice purpose%%%%%%%
			%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			
			add_flag.test_exp=1; eye_par.dummymode = 1; eye_par.edfFile='test.edf';
			eye_par.header_msg = 'prac ses';
			F.dataFileName = [F.rootPath filesep 'Data' filesep 'Training' filesep 'Prac_Subj_' num2str(SubjectData.sub_id) '.mat'];
			trial_design.trial_order = readmatrix('./task/trial_order.csv');
			trial_design.total_trial_nr = size( trial_design.trial_order, 2);

		elseif  strcmp(SubjectData.exp_type, 'main') % 
			
			%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			%%%%%%%main experiment %%%%%
			%%%%%%%%%%%%%%%%%%%%%%%%%%%%

			%trial_design.testing = 0;
			add_flag.test_exp = 0; eye_par.dummymode = 1;
			F.dataFileName = [F.SubjPath filesep 'exp' num2str(SubjectData.exp_nr) filesep 'session_' num2str(SubjectData.ses_nr) '_response.mat' ];

			% check if the selection has already been tested
			if exist(F.dataFileName, 'file') == 2
				errordlg('ERROR: The session/exp you selected is already tested, check and choose another');      
				error('ERROR: The session/exp you selected is already tested, check and choose another');
			else 
				% load the pre-generated design matrix
				load([F.SubjPath filesep 'exp' num2str(SubjectData.exp_nr) filesep 'session_' num2str(SubjectData.ses_nr) '_design.mat']);
			end

			%eye_par.edfFile = ['Subj_' num2str(SubjectData.sub_id) '_session_' num2str(SubjectData.ses_nr) '.edf'];
			%1-8 characters for edf file name
			eye_par.edfFile = ['S' num2str(SubjectData.sub_id) 't' num2str(SubjectData.exp_nr) num2str(SubjectData.ses_nr) '.edf'];
			eye_par.header_msg = ['exp ' num2str(SubjectData.exp_nr) ',ses ' num2str(SubjectData.ses_nr) ',subjID ' num2str(SubjectData.sub_id)];

		end
		
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		%%% Call Psychtoolbox script %%%
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

		% Make sure we're running on PTB-3
		AssertOpenGL;
		
		if add_flag.test_exp
		%Debug?
		%PsychDebugWindowConfiguration;
		end
		
		tic
		add_flag.resp = 1; % resp - 0 : mouse response; resp - 1 : keyboard response; resp - 2 : bitsi
		
		%exp
		[R, Stimuli,trialpar]= PresentStim(Stimuli, trial_design, eye_par, add_flag); 
		% at this stage, save more than needed. In the future, only save R
		toc
		
	end


	%save response data - for now, written as save also practice data. 
	if ~strcmp(SubjectData.exp_type, 'train')
		save(F.dataFileName, 'R', 'SubjectData');
	end
	%save eyelink data
	if ~eye_par.dummymode && strcmp(SubjectData.exp_type, 'main')
		eyelink_closesave(1,[F.SubjPath filesep 'exp' num2str(SubjectData.exp_nr) filesep 'eyetrack' filesep 'session_' num2str(SubjectData.ses_nr) '_eyedata' ], eye_par.edfFile);

	elseif ~eye_par.dummymode && strcmp(SubjectData.exp_type, 'prac')
		eyelink_closesave(1,'M:\wenlou\MATLAB\Data\Training\prac_raw', eye_par.edfFile);
	end

	%eyelink_closesave(1,'M:\wenlou\MATLAB\Data\Training', eye_par.edfFile);
	%eyelink_closesave(1,'M:\wenlou\MATLAB\Data\Training\prac_raw2', eye_par.edfFile);


else % test AV sync

	add_flag.test_exp=1; eye_par.dummymode = 1; 

	trial_design.trial_order = readmatrix('./task/trial_order_AV.csv');
	trial_design.total_trial_nr = size( trial_design.trial_order, 2);
	
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%% Call Psychtoolbox script %%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	% Make sure we're running on PTB-3
	AssertOpenGL;

	add_flag.resp = 1; % resp - 0 : mouse response; resp - 1 : keyboard response; resp - 2 : bitsi

	%exp
	[R, Stimuli,trialpar]= PresentStim(Stimuli, trial_design, eye_par, add_flag); 
	
	mean_vis_diff = mean([R.AVTrialOnset{:}] - [R.AVStimOnset{:}]);
	disp(['second part of D is ' num2str(mean_vis_diff)]);

	
end