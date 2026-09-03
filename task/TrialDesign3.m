function [trial_design, V_design_half] = TrialDesign3(exp, ses_nr, V_design_half, loc_pool, A_pre_loc)

% Force the random number generator to a unique state
rng('shuffle');
% design matrix, determines the order of the trials
nperAblock = 64; 
nAblock = 8; % for one session : 2 visaul 8 auditory blocks
nVblock = 2;
% for visual: 4 times repetitions spread out over multiple sessions

%%%%%waved according to 'project_slide_0828.pptx'%%%%%
if exp == 1 && ses_nr == 1 % 
	nperVblock = 84/2;
	v_trial_idx = 1:(84/2);
elseif exp == 1 && ses_nr == 2 % 
	nperVblock = 86/2;   
	v_trial_idx = (84/2+1):(84/2+86/2);
elseif exp == 1 && ses_nr == 3 % 
	nperVblock = 86/2;   
	v_trial_idx = (84/2+86/2+1):(64*2);
	
elseif exp == 2 && ses_nr == 1
	nperVblock = 64/2;
	v_trial_idx = 1:(64/2);
elseif exp == 2 && ses_nr == 2
	nperVblock = 64/2;
	v_trial_idx = (64/2+1):64;
end 

totTri   = nperAblock * nAblock + nperVblock* nVblock;   

A_blocks = [1 2 4 5 6 7 9 10];
V_blocks = [3 8];
design   = zeros(6, totTri);
design(6,:) = sort([repmat(A_blocks, 1, nperAblock), repmat(V_blocks, 1, nperVblock)]);%mark the block no

% 5th row: 1 - AV-A Trial; 2 - AV-V Trial
% the 3rd and 8th is the visual block
design(5, ismember(design(6,:), A_blocks)) = 1;
design(5, ismember(design(6,:), V_blocks)) = 2;

if exp == 1 % the first experiment
    % the output of trial_design.trial_order is a 5 * ntrial matrix
    % for experiment 1
    % 1st row: move type - exp1 static (1)
    % 2nd row: Auditory location in AV phase
    % 3rd row: Visual location in AV phase 
    % 4th row: Auditory/visual location in A/V phase
    % 5th row: 1 - AV-A Trial; 2 - AV-V Trial
    % 6th row: block number
    
    %the first experiment, 1- static
    design(1,:) = 1;
    
	if ses_nr == 1 % only gen this matrix once
		%For V block - generate for all session - 4 repetition in total, which means 2 repetions generated, 2 repetition is the mirrow
		V_design_half = zeros(3, 64*2);
		[V_design_half(1, :), V_design_half(2, :), V_design_half(3, :)] =  BalanceFactors(2, 5, loc_pool , loc_pool , loc_pool);
	end

    % 4 * 4 * 4 possibilities for the AV, A displacement
    % for A block [1 2 4 5], generate a new sequence every time
    for block_id = [1 2 4 5]
        [design(2, design(6,:)==block_id), design(3, design(6,:)==block_id), design(4, design(6,:)==block_id)] = ...
                    BalanceFactors(1, 5, loc_pool , loc_pool , loc_pool);
    end

	%3rd block is visual
	design(2:4, design(6,:)==3) = V_design_half(:,v_trial_idx);

    % for block 6:10, the sequence is the mirror of 11-n (for example, block 10 is the mirror of block 1)
    for block_id = 6:10
        design(2:4, design(6,:)==block_id) = flip(design(2:4, design(6,:)==11-block_id), 2);
    end


elseif exp == 2 % the second experiment
	
	if ses_nr == 1 % only gen this matrix once
		%For V block - generate one block ()
		V_design_half = wave_one_block(loc_pool, A_pre_loc);
	end
	
    % for A block [1 2 4 5], generate a new sequence every time
    for block_id = [1 2 4 5]
        % wave one block
        design(1:4, design(6,:)==block_id) = wave_one_block(loc_pool, A_pre_loc);
    end			

	%3rd block is visual
	design(1:4, design(6,:)==3) = V_design_half(:,v_trial_idx);
	
    % for block 6-10, the sequence is the mirror of 11-n (for eaxample, block 10 is the mirror of block 1)
    for block_id = 6:10
        design(1:4, design(6,:)==block_id) = flip(design(1:4, design(6,:)==11-block_id), 2);
    end

end

trial_design.trial_order = design;
trial_design.total_trial_nr = size( design, 2);

end %EOF

%helper function: wave one block for experiemnt 2
function one_block = wave_one_block(test_loc, A_pre_loc)

    %% test_loc is the location of testing A or V location in A/V phase
	%% A_pre_loc is the location of A presentation in AV phase
	
	% for experiment 2 - increasing/decreasing move
	% 1st row: move type - exp2 dynamic (2)
	% 2nd row: Auditory location in AV phase
	% 3rd row: disparity change type : 1 - increasing; 2 - decreasing; 
	% 4th row: Auditory/visual location in A/V phase
	% 5th row: 1 - AV-A Trial; 2 - AV-V Trial

	% for experiment 2 - crossing type
	% 1st row: move type - exp2 dynamic crossing (3)
	% 2nd row: Auditory location in AV phase
	% 3rd row: AV displacement 1 - VA, 2 - AV. (starting dispalcement) 
	% 4th row: Auditory/visual location in A/V phase
	% 5th row: 1 - AV-A Trial; 2 - AV-V Trial

	% for experiment 2 - congruent
	% 1st row: move type - static and congruent (4)
	% 2nd row: Auditory location in AV phase
	% 3rd row: visual location in AV phase (same as A)
	% 4th row: Auditory/visual location in A/V phase
	% 5th row: 1 - AV-A Trial; 2 - AV-V Trial
    
    %inc/dec type 2 % repeat twice
    move_type_2 = zeros(4, 32);
    move_type_2(1, :) = 2;
    [move_type_2(2,:), move_type_2(3,:), move_type_2(4,:)] =  BalanceFactors(2, 5, A_pre_loc , [1, 2] , test_loc);

    %crossing type 3 % repeat once
    move_type_3 = zeros(4, 16);
    move_type_3(1, :) = 3;
    [move_type_3(2,:), move_type_3(3,:), move_type_3(4,:)] =  BalanceFactors(1, 5, A_pre_loc , [1, 2] , test_loc);

    %congruent % repeat twice
    move_type_4 = zeros(4, 16);
    move_type_4(1, :) = 4;
    [move_type_4(2,:), move_type_4(4,:)] =  BalanceFactors(2, 5, A_pre_loc , test_loc);
    move_type_4(3,:) = move_type_4(2,:);

    one_block = [move_type_2, move_type_3, move_type_4];
    %random order
    one_block = one_block(:, randperm(64));

end %EOF