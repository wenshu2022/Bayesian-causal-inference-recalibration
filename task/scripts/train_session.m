function R = train_session(Stimuli, train_part_id, odd_flag)

%%%    The train session include three parts (select in train_part_id):
%%% 1) understand the use of keys in the common source questions
%%% 2) map the locations of sound to the fingers/keys
%%% 3) map the locations of blob to the fingers/keys


%try
    %%%%%%%%%%%%%%%%%%
    %%% Initialize %%%
    %%%%%%%%%%%%%%%%%%
    
    % Defining keys for input 
    KbName('UnifyKeyNames');

	P.spaceKey = KbName('Space'); 
	
	resp = 1; %%%% default with keyboard. add if function if changed to other options in the future.  
	
	P.answerKey1 = KbName('Q'); P.answerKey2 = KbName('W'); P.answerKey3 = KbName('E');
	P.answerKey4 = KbName('I'); P.answerKey5 = KbName('O'); P.answerKey6 = KbName('P'); 

	P.regularKeys = [P.spaceKey, P.answerKey1, P.answerKey2, P.answerKey3, P.answerKey4, P.answerKey5, P.answerKey6];
	
    RestrictKeysForKbCheck(P.regularKeys);   
    
    % Initialize Screen
    [P, Stimuli] = SetupScreen(Stimuli,P, 0);
	
	% Set Drawing paramaters
    D = SetDrawingParameters(P, Stimuli, resp); 
	
    % Prepare Audio Device
    %[P, Stimuli] = SetupAudio(Stimuli,P);
    
	%Define the used key list for practice
	P.key_lst = {'Q','W','E','I','O','P'}; % must be from left to right sequentially
	P.key_lst_AV = {'W','E','I','O'}; % must be from left to right sequentially
    % Dummy call to GetSecs (because the first call may take some time and we'll use it later)
    dummy = GetSecs;

	R=[];
	
	if train_part_id == 1 % part 1: use of keyboards for common source quests
	
		block_ann = 'Please put your fingers on the keyboard. Key Q/W/E for the left fingers, and key I/O/P for the right fingers. \n\n In this block, you will practice how to answer to the question "Vis and Aud from common source?" \n\n Please press the SPACE key to continue.';
		
		disp_color = P.yellow;
		qtxt = 'Common source?';
		
		%% in this training, we counterbalance the displacement of yes and no in left/right hands
		%% for even number mod(x,2)==0, the displacement is left-yes, right-no
		%% for odd number mod(x,2)==1, the displacement is right-yes, left-no
		%% odd_flag = mod(sub_id,2);
		
		train_p1(P, D, block_ann, disp_color, qtxt, odd_flag);
		
	elseif train_part_id == 2 % part 2 - map sound to fingers
	
		block_ann = 'Please put your fingers on the keyboard. Key W/E for the left fingers, and key I/O for the right fingers. \n\n In this block, you will practice how to locate a spatial SOUND. \n\n Please press the SPACE key to continue.';

		disp_color = P.green;
		qtxt = 'Locate A' ;

		% Prepare Audio Device
		P = SetupAudio(Stimuli,P);

		% %define trialpar, which is necessay for function MakeSound.m
		% trialpar.aud_duration = 0.0167 * 8 /2;
		% trialpar.aud_ramp_duration = trialpar.aud_duration * 0.1 /2;% ramp-on or ramp-off

		res_lst = train_p2(P, D, Stimuli, block_ann, disp_color, qtxt); %first col - RMSE; second col - RT
		R.RMSE_lst  = res_lst(:,1); R.RT_lst  = res_lst(:,2);
		
	elseif train_part_id == 3 % part 3 - map visual to fingers
	
		block_ann = 'Please put your fingers on the keyboard. Key W/E for the left fingers, and key I/O for the right fingers. \n\n In this block, you will practice how to locate a circlular BLOB. \n\n Please press the SPACE key to continue.';

		disp_color = P.pink;
		qtxt = 'Locate V' ;

		% make gaussian blobs
		P.waitframes = 1; % waitframes = 1 means: Redraw every monitor refresh.  
		%set and translate gaussian blob parameters as in DefinePresent.m
		%blob_width_pxl = floor(P.pxl_per_deg * Stimuli.blob.width); 
		blob_width_pxl = round(tand(Stimuli.blob.width)*P.dist2Screen_nPixWidth);        %in pixels
		blob_height_pxl = round(tand(Stimuli.blob.width)*P.dist2Screen_nPixHeight);
		tot_width = 2*blob_width_pxl+1; % here, we have circulasr shape, so the height and width is the same. 
		tot_height = 2*blob_height_pxl+1;
		%sc_pxl = floor(P.pxl_per_deg * Stimuli.blob.sc); 
		sc_pxl = round(tand(Stimuli.blob.sc)*P.dist2Screen_nPixWidth);
		% Aspect ratio width vs. height:
		aspectratio = 1.0;
		%also save a copy of translated blob pars
		Stimuli.blob.myblobpars = [Stimuli.blob.contrast, sc_pxl, aspectratio, 0]';

		%%%use PTB embedded function to generate gaussian blob
		Stimuli.blob.blobtex = CreateProceduralGaussBlob(P.win, tot_width * 2, tot_height * 2);
		Stimuli.blob.texrect = Screen('Rect', Stimuli.blob.blobtex);
		
		train_p3(P, D, Stimuli, block_ann, disp_color, qtxt);
		
		
	end
	
	
	% Clean up
    Priority(0);                        % Shutdown realtime scheduling:
    ListenChar;                         % Reenable all keys output to Matlab
    RestrictKeysForKbCheck([]);         % Reenable all keys for KbCheck
    if isfield(P,'oldlut')
        Screen('LoadNormalizedGammaTable',P.screenNumber,P.oldlut);
    end
    ShowCursor;                         % Show Cursor
    Screen('CloseAll');                 % Close display(s)
    
    if isfield(P,'AudioHandle')
        PsychPortAudio('Close');        % Shutdown sound driver
    end
%{
catch 

	% Clean up
    Priority(0);                        % Shutdown realtime scheduling:
    ListenChar;                         % Reenable all keys output to Matlab
    RestrictKeysForKbCheck([]);         % Reenable all keys for KbCheck
    if isfield(P,'oldlut')
        Screen('LoadNormalizedGammaTable',P.screenNumber,P.oldlut);
    end
    ShowCursor;                         % Show Cursor
    Screen('CloseAll');                 % Close display(s)
    
    if isfield(P,'AudioHandle')
        PsychPortAudio('Close');        % Shutdown sound driver
    end

end	
%}
end%EOF Main function - train_session

function train_p1(P, D, block_ann, disp_color, qtxt, odd_flag)

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%% PART I: use of keyboards %%%%%%%%%%%%%
	%%%%%%%%  for common source quests %%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	DrawFormattedText(P.win, block_ann, 'center', 'center', disp_color, 80);
	Screen('Flip', P.win);
	KbStrokeWait;
	
	% default is left-yes, right-no
	ans_options = {'Yes\n\nLow confidence', 'Yes\n\nMedium confidence', 'Yes\n\nHigh confidence', 'No\n\nHigh confidence', 'No\n\nMedium confidence', 'No\n\nLow confidence'};

	if odd_flag % if odd sub id, change to left - no, right - yes
		ans_options = flip(ans_options);
	end

	%random order  - Repeat 6 rounds
	round_nr = 6;
	res_lst = zeros(round_nr, 2); 

	for i_round = 1:round_nr

		%for one test run
		acc_acum = 0;RT_acum = 0;
		for key_idx = randperm(numel(P.key_lst)) % iterate a random list
		
			%% Draw common source questions
			boundsText = Screen(P.win,'TextBounds',qtxt); %[L,T,R,B] from [L=0,T=0]
			DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
			%% Draw instruction 
			DrawFormattedText(P.win, ans_options{key_idx}, 'center', 'center', disp_color);
			Screen('DrawingFinished', P.win);                                                                                                 
			Screen('Flip', P.win);

			%check input from the keyboard and give feedback
			[acc, ~, RT] = checkKeyInput(P, D, qtxt, key_idx, disp_color, 1);
			% change color
			if acc
				feedback_color = [71,189,82];%green 
			else 
				feedback_color = [189,55,81];% pink red
			end
			
			%% Draw common source questions
			DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
			%% Draw instruction 
			DrawFormattedText(P.win, ans_options{key_idx}, 'center', 'center', feedback_color);
			Screen('DrawingFinished', P.win);
			Screen('Flip', P.win);
			WaitSecs(0.5);
			
			acc_acum = acc + acc_acum;
			RT_acum = RT + RT_acum;
		end

		res_lst(i_round, 1) = acc_acum / numel(P.key_lst); %acc
		res_lst(i_round, 2) = RT_acum / numel(P.key_lst); %mean response time

		f_txt = sprintf('The overall accuracy is %.2f%%', res_lst(i_round, 1)*100);
		DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
		%% Draw overall feedback 
		DrawFormattedText(P.win, f_txt, 'center', 'center', disp_color);
		Screen('DrawingFinished', P.win);                                                                                                 
		Screen('Flip', P.win);
		WaitSecs(1);
		
	end
	
	plot(res_lst);
	legend('acc','rt');

end %EOF - train_part1


function res_lst = train_p2(P, D, Stimuli, block_ann, disp_color, qtxt)	

	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%% PART II: map sound to fingers %%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	DrawFormattedText(P.win, block_ann, 'center', 'center', disp_color, 80);
	Screen('Flip', P.win);
    KbStrokeWait;
    start=1;
	% each answer and key were iterated from left to right and right to left multiple TIMES
	rep_order = repmat(1:numel(P.key_lst_AV), 1, 2);
	rep_order = [rep_order, flip(rep_order)];
	for key_idx = rep_order
		
		% draw fixation cross 
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x,P.winCenter_y], 1);
		boundsText = Screen(P.win,'TextBounds',qtxt); %[L,T,R,B] from [L=0,T=0]
		DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
		Screen('DrawingFinished', P.win);
		Screen('Flip', P.win);
        if start % the first demonstration, wait some time
            WaitSecs(0.5); start=0;
        end
		%prepare the sound 
		Sound_test= MakeSound2(P, Stimuli, Stimuli.aud_pool_train(key_idx), 0.8, 1)'; %wavDat = MakeSound2(P, Stimuli, aud_loc, volumn, norm)
		% Buffer the Sound 
		PsychPortAudio('FillBuffer',P.AudioHandle, Sound_test);

		PsychPortAudio('Start', P.AudioHandle, [], []);
		% Stop sound playback
		PsychPortAudio('Stop', P.AudioHandle, 1);  
		Sound_test = [];%reset the sound
		
		%check input from the keyboard and give feedback
		checkKeyInput(P, D, qtxt, key_idx, disp_color,0);
		WaitSecs(1);
		
	end % end for
	
	% random order without the hints
	% two types of training stop cr, toggle by the if statement
	
	if 0 % stop when RMSE reach a level
	
		stop_cr = 0; counter = 0;
		RMSE_lst = [];rt_lst=[];
		while ~stop_cr || ~(counter <= 10 && counter >= 5) % set a counter otherwse the while may run forever. at least 5 times, no more than 10 times

			%for one test run
			%initiate a matrix to store all keys and the repnse keys
			key_tt_lst = zeros(numel(P.key_lst_AV), 3); % frst row - real key; second row - response key, Third - response time
			key_tt_lst(:,1) = randperm(numel(P.key_lst_AV));% the given key rder is randomized
			
			for idx = 1:numel(P.key_lst_AV) 
				% draw fixation cross and quest
				Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x, P.winCenter_y], 1);
				DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
				Screen('DrawingFinished', P.win);
				Screen('Flip', P.win);

				key_idx = key_tt_lst(idx,1);% the input key
				%prepare the sound 
				Sound_test= MakeSound2(P, Stimuli, Stimuli.aud_pool_train(key_idx), 0.8, 1)';
				%Sound_test = squeeze(WavDat(key_idx,:,:))';%samples * two channels
				% Buffer the Sound 
				PsychPortAudio('FillBuffer',P.AudioHandle, Sound_test);
				PsychPortAudio('Start', P.AudioHandle, [], []);
				% Stop sound playback
				PsychPortAudio('Stop', P.AudioHandle, 1);  
				Sound_test=[];%reset the sound

				%check input from the keyboard and give feedback
				[~, key_tt_lst(idx,2), key_tt_lst(idx,3)] = checkKeyInput(P, D, qtxt, key_idx, disp_color, 0);
				WaitSecs(1);
			end%end for
			WaitSecs(0.5);
			SquareDiffResp2Target = ((key_tt_lst(:,1) - key_tt_lst(:,2))*8).^2;
			RMSE = sqrt(mean(SquareDiffResp2Target)); % if larger than 5.5 then rej
			RMSE_lst = [RMSE_lst, RMSE];
			rt_lst = [rt_lst, mean(key_tt_lst(:,3))];
			stop_cr = RMSE <= 5.5; % the latest RMSE is less than 5.5
			counter = counter+1;
		end%end while

		res_lst = [RMSE_lst; rt_lst]';
	
	else % stop after doing 10 rounds
	
		round_nr = 10;
		res_lst = zeros(round_nr, 2); %first col - RMSE; second col - RT

		for i_round = 1:round_nr

			%initiate a matrix to store all keys and the repnse keys
			key_tt_lst = zeros(numel(P.key_lst_AV), 3); % frst row - real key; second row - response key, Third - response time
			key_tt_lst(:,1) = randperm(numel(P.key_lst_AV));% the given key rder is randomized
			
			for idx = 1:numel(P.key_lst_AV) 
				% draw fixation cross and quest
				Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x, P.winCenter_y], 1);
				DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
				Screen('DrawingFinished', P.win);
				Screen('Flip', P.win);

				key_idx = key_tt_lst(idx,1);% the input key
				%prepare the sound 
				Sound_test= MakeSound2(P, Stimuli, Stimuli.aud_pool_train(key_idx), 0.8, 1)';
				%Sound_test = squeeze(WavDat(key_idx,:,:))';%samples * two channels
				% Buffer the Sound 
				PsychPortAudio('FillBuffer',P.AudioHandle, Sound_test);
				PsychPortAudio('Start', P.AudioHandle, [], []);
				% Stop sound playback
				PsychPortAudio('Stop', P.AudioHandle, 1);  
				Sound_test=[];%reset the sound

				%check input from the keyboard and give feedback
				[~, key_tt_lst(idx,2), key_tt_lst(idx,3)] = checkKeyInput(P, D, qtxt, key_idx, disp_color, 0);
				WaitSecs(1);
			end%end for
            WaitSecs(0.5);
			SquareDiffResp2Target = ((key_tt_lst(:,1) - key_tt_lst(:,2))*8).^2;
			res_lst(i_round, 1) = sqrt(mean(SquareDiffResp2Target)); % if RMSE larger than 5.5 then rej
			res_lst(i_round, 2) = mean(key_tt_lst(:,3));

		end % end for

	end%end if condition (to toggle between cr)
	
	plot(res_lst);
	legend('RMSE','rt');
	%print the average RMSE
	disp(['The average RMSE in this session is ' num2str(mean(res_lst(:, 1)))]);
	
end % EOF - train_p2
	
	
function train_p3(P, D, Stimuli, block_ann, disp_color, qtxt)	
	
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%% PART III: map blob to fingers %%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%	
	
	DrawFormattedText(P.win, block_ann, 'center', 'center', disp_color, 80);
	Screen('Flip', P.win);
    KbStrokeWait;
    
	vis_loc = sort(Stimuli.aud_pool_train);
	dur = 0.0167 * 8;
	% draw fixation cross 
	Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x,P.winCenter_y], 1);
	boundsText = Screen(P.win,'TextBounds',qtxt); %[L,T,R,B] from [L=0,T=0]
	DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
	Screen('DrawingFinished', P.win);                                                                                                 
	Screen('Flip', P.win);
	WaitSecs(0.5);
	% each answer and key were iterated from left to right and right to left once
	rep_order = repmat(1:numel(P.key_lst_AV), 1, 1);
	rep_order = [rep_order, flip(rep_order)];
	
	for key_idx = rep_order
		vis_test_pxl = vis_loc(key_idx) * P.pxl_per_deg;
		blob_dstRect_test = CenterRectOnPoint(Stimuli.blob.texrect, vis_test_pxl+P.winCenter_x, P.winCenter_y); 
		% draw the blob and wait for dur
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x,P.winCenter_y], 1);
        DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
		Screen('DrawTextures', P.win, Stimuli.blob.blobtex, [], blob_dstRect_test, [], [], [], [], [], kPsychDontDoRotation, Stimuli.blob.myblobpars);
		Screen('DrawingFinished', P.win);
		Screen('Flip', P.win); 
		WaitSecs(dur);
		
		% the blob disappear
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x,P.winCenter_y], 1);
		DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
		Screen('DrawingFinished', P.win);
		Screen('Flip', P.win); 
		
		%check input from the keyboard and give feedback
		checkKeyInput(P, D, qtxt, key_idx, disp_color, 0);
		WaitSecs(0.5);
	end % end for
	
	%random order without the hints - stop only when 100% accuracy two times in a row
	acc_rt = zeros(1,2); % store two consecetive terms
	stop_cr=0;
	while ~ismembertol(stop_cr,2.00) % to avoid issue with precision

		%for one test run
		% draw fixation cross and quest
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x, P.winCenter_y], 1);
		DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
		Screen('DrawingFinished', P.win);
		Screen('Flip', P.win);

		acc_acum = 0;
		for key_idx = randperm(numel(P.key_lst_AV)) % iterate a random list
		
			vis_test_pxl = vis_loc(key_idx) * P.pxl_per_deg;
			blob_dstRect_test = CenterRectOnPoint(Stimuli.blob.texrect, vis_test_pxl+P.winCenter_x, P.winCenter_y); 

			Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x,P.winCenter_y], 1);
			DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
			Screen('DrawTextures', P.win, Stimuli.blob.blobtex, [], blob_dstRect_test, [], [], [], [], [], kPsychDontDoRotation, Stimuli.blob.myblobpars);
			Screen('DrawingFinished', P.win);
			Screen('Flip', P.win); 
			WaitSecs(dur);

			Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, disp_color , [P.winCenter_x,P.winCenter_y], 1);
			DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
			Screen('DrawingFinished', P.win);
			Screen('Flip', P.win); 
			
			%check input from the keyboard and give feedback
			[acc, ~, ~] = checkKeyInput(P, D, qtxt, key_idx, disp_color, 0);
			WaitSecs(0.5);
			acc_acum = acc + acc_acum;
		end

		% the accuracy rate
		acc_rt=flip(acc_rt);%flip, so that the previous acc rate whipped to the second index
		acc_rt(1) = acc_acum / numel(P.key_lst_AV);% the first element is the current acc rate, the second one is from previous term.
		f_txt = sprintf('The overall accuracy is %.2f%%', acc_rt(1)*100);
		DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
		%% Draw iverall feedback 
		DrawFormattedText(P.win, f_txt, 'center', 'center', disp_color);
		Screen('DrawingFinished', P.win);                                                                                                 
		Screen('Flip', P.win);
		WaitSecs(1);
		
		stop_cr = sum(acc_rt);
	end

end  % EOF - train_p3


%helper function
%check input from the keyboard and give feedback
function  [acc, key_idx_resp, RT] = checkKeyInput(P, D, qtxt, key_idx, disp_color, p1)

	%Set start time
	startTime = GetSecs;
	RespBool = 0;
	
	while ~RespBool % no time limit
		[KBpressed, ~, keyCode] = KbCheck;
		
		if KBpressed && (keyCode(P.answerKey1) || keyCode(P.answerKey2) || keyCode(P.answerKey3) || keyCode(P.answerKey4) || keyCode(P.answerKey5) || keyCode(P.answerKey6))
			% for p1 and p2/p3, we use different set of keys. 
			% p1 use 6 keys system while p2/3 only use four
			if p1 & keyCode(P.answerKey1)
				key_idx_resp = 1; RespBool=1;
			elseif p1 & keyCode(P.answerKey2)
				key_idx_resp = 2; RespBool=1;
			elseif p1 & keyCode(P.answerKey3)
				key_idx_resp = 3; RespBool=1;
			elseif p1 & keyCode(P.answerKey4)
				key_idx_resp = 4; RespBool=1;
			elseif p1 & keyCode(P.answerKey5)
				key_idx_resp = 5; RespBool=1;
			elseif p1 & keyCode(P.answerKey6)
				key_idx_resp = 6; RespBool=1;

			elseif (~p1) & keyCode(P.answerKey2)
				key_idx_resp = 1; RespBool=1;
			elseif (~p1) & keyCode(P.answerKey3)
				key_idx_resp = 2; RespBool=1;
			elseif (~p1) & keyCode(P.answerKey4)
				key_idx_resp = 3; RespBool=1;
			elseif (~p1) & keyCode(P.answerKey5)
				key_idx_resp = 4; RespBool=1;

			end % end if
		end % end if
		
	end % end while
	
	RT = GetSecs - startTime; % RESPONSE TIME
	
	%feedback
	if key_idx_resp == key_idx
		feedback_color = [71,189,82];%green 
		acc = 1;
	else 
		feedback_color = [189,55,81];% pink red
		acc = 0;
	end

	if ~p1
		boundsText = Screen(P.win,'TextBounds',qtxt); %[L,T,R,B] from [L=0,T=0]
		DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), disp_color);
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, feedback_color , [P.winCenter_x, P.winCenter_y], 1);
		Screen('DrawingFinished', P.win);
		Screen('Flip', P.win);
		%WaitSecs(0.5);
	end


end %EOF - checkKeyInput