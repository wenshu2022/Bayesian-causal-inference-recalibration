function trialpar = DefineTrial2(trial_design, iTrial, Stimuli)

	% the output of trial_design.trial_order is a 5 * ntrial matrix
    % for experiment 1
    % 1st row: move type - exp1 static (1)
    % 2nd row: Auditory location in AV phase
    % 3rd row: Visual location in AV phase 
    % 4th row: Auditory/visual location in A/V phase
    % 5th row: 1 - AV-A Trial; 2 - AV-V Trial

    % for experiment 2 - increasing/decreasing move
    % 1st row: move type - exp2 dynamic (2)
    % 2nd row: Auditory location in AV phase
    % 3rd row: disparity change type : 1 - increasing; 2 - decreasing; 
    % 4th row: Auditory/visual location in A/V phase
    % 5th row: 1 - AV-A Trial; 2 - AV-V Trial

    % for experiment 2 - crossing type
    % 1st row: move type - exp2 dynamic crossing (3)
    % 2nd row: Auditory location in AV phase
    % 3rd row: AV displacement 1 - VA, 2 - AV. (starting dispalcement) x
    % 4th row: Auditory/visual location in A/V phase
    % 5th row: 1 - AV-A Trial; 2 - AV-V Trial

    % for experiment 2 - congruent
    % 1st row: move type - static and congruent (4)
    % 2nd row: Auditory location in AV phase
    % 3rd row: visual location in AV phase (same as A)
    % 4th row: Auditory/visual location in A/V phase
    % 5th row: 1 - AV-A Trial; 2 - AV-V Trial
	
	%% define the move tracjectory for this specific trial
	
	%%%%%%%%%%%%%%%%%
	%%%%%%point%%%%%%
	%%%%%%%%%%%%%%%%%
	% the par trav_time_in_flips can be move to a higher-order par var when the whole design is setteled and no need for explore
	% par aud_duration can also be put into a high-order function later on
	% code to be simplified
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
	
	%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%Define the AV Phase%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%
	
	if trial_design.trial_order(1, iTrial) == 1 || trial_design.trial_order(1, iTrial) == 4  % experiment 1 - the static condition  
                                                                                             % OR  the congruent condition in exp 2
		trialpar.vis_trajectory = repmat(trial_design.trial_order(3, iTrial), [Stimuli.stim_dur_in_flips 1]);
		
	elseif 	trial_design.trial_order(1, iTrial) == 3 % experiment 2 - move type crossing
		speed = 4;
		trav_dist = 8 * speed; % must be integer

		v_loc = zeros(2, 1);
		
		% the crossing condition has in total 4 types :2 (A loc) * 2 (AV displacement)
		if trial_design.trial_order(3, iTrial) == 1
		% VA
			v_loc(1) = trial_design.trial_order(2, iTrial) - trav_dist/2; 
			v_loc(2) = trial_design.trial_order(2, iTrial) + trav_dist/2; 
		
		elseif trial_design.trial_order(3, iTrial) == 2 
		% AV
			v_loc(1) = trial_design.trial_order(2, iTrial) + trav_dist/2; 
			v_loc(2) = trial_design.trial_order(2, iTrial) - trav_dist/2; 

		end
		trialpar.vis_trajectory = linspace(v_loc(1), v_loc(2), Stimuli.stim_dur_in_flips)';
	
	elseif	trial_design.trial_order(1, iTrial) == 2 % experiment 2 - increasing/decreasing move

		v_loc = zeros(2, 1);
		
		if trial_design.trial_order(2, iTrial) < 0 % if A in AV is on the left side, the underlying displacement is A V . 
			v_loc(1) = trial_design.trial_order(2, iTrial) + Stimuli.min_dis; 
			v_loc(2) = trial_design.trial_order(2, iTrial) + Stimuli.max_dis; 
			
		else % if A in AV is on the right side, the underlying displacement is V A . 
			v_loc(1) = trial_design.trial_order(2, iTrial) - Stimuli.min_dis; 
			v_loc(2) = trial_design.trial_order(2, iTrial) - Stimuli.max_dis; 
		end
		
		if trial_design.trial_order(3, iTrial) == 2 % if type decreasing
			v_loc = flip(v_loc);
		end

		trialpar.vis_trajectory = linspace(v_loc(1), v_loc(2), Stimuli.stim_dur_in_flips)';
		
	end
	
	
	trialpar.trial_type = trial_design.trial_order(5, iTrial); %1 - AV-A Trial; 2 - AV-V Trial
	trialpar.aud_loc = trial_design.trial_order(2, iTrial);
	
	
	if trialpar.trial_type == 1

		%%%%%%%%%%%%%%%%%%%%%%%%%%%
		%%%%Define the A Phase%%%%
		%%%%%%%%%%%%%%%%%%%%%%%%%%%
		
		%the auditory location of A trial
		trialpar.aud_test_loc = trial_design.trial_order(4, iTrial);
	
	elseif trialpar.trial_type == 2
	
		%%%%%%%%%%%%%%%%%%%%%%%%%%%
		%%%%Define the V Phase%%%%
		%%%%%%%%%%%%%%%%%%%%%%%%%%%
		trialpar.vis_test_loc = trial_design.trial_order(4, iTrial);
		
	else
	
	%warning 
	
	end

	trialpar.iTrial = iTrial;
	trialpar.iBlock = trial_design.trial_order(6, iTrial);
	%trialpar.move_type = trial_design.trial_order(1, iTrial); % if not use, remove 
	
	
end