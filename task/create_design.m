%create and save design for each subject
%sub_id = 1;

for sub_id = 1:10

	SubjPath = ['..' filesep 'Data' filesep 'Subj_' num2str(sub_id)];

	%make folder for exp1, exp 2
	%if not(isfolder(SubjPath ))
	mkdir(SubjPath)
	mkdir([SubjPath filesep 'exp1'])
	mkdir([SubjPath filesep 'exp2'])
	mkdir([SubjPath filesep 'exp1' filesep 'eyetrack'])
	mkdir([SubjPath filesep 'exp2' filesep 'eyetrack'])
	%end

	loc_pool = [ -12, -4, 4, 12]; % from Stimuli.loc_pool in DefinePresent.m

	%for the first experiment, we have two sessions
	%exp 1, session 1
	[trial_design, V_design_half] = TrialDesign3(1, 1, [], loc_pool, []);
	% save the design matrix in the design folder
	save([SubjPath filesep 'exp1' filesep 'session_' num2str(1) '_design.mat' ], 'trial_design');
	%exp 1, session 2 and 3
	for session = 2:3
		trial_design = [];
		[trial_design, ~] = TrialDesign3(1, session, V_design_half, loc_pool, []);
		% save the design matrix in the design folder
		save([SubjPath filesep 'exp1' filesep 'session_' num2str(session) '_design.mat' ], 'trial_design');
	end

	A_pre_loc = [-6, 6]; 

	% for the second experiment, two sessions
	%exp 2, session 1
	[trial_design, V_design_half] = TrialDesign3(2, 1, [], loc_pool, A_pre_loc);
	save([SubjPath filesep 'exp2' filesep 'session_1_design.mat' ], 'trial_design');
	%exp 2, session 2
	trial_design = [];
	[trial_design, ~] = TrialDesign3(2, 2, V_design_half, loc_pool, A_pre_loc);
	save([SubjPath filesep 'exp2' filesep 'session_2_design.mat' ], 'trial_design');

end