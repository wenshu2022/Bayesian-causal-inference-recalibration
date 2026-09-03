function [Stimuli, R] = PresentAV(Stimuli, P, D, R, trialpar, eye_par, add_flag)

		% THIS IS THE MAGICAL PARAMETER FOR THE SYNCHRONIZATION:
		Delay_emprical = 0.0005-0.000; % This number consists of 2 parts: the first part is
		% based on an AV-sync measurement with the photodiode attached to the
		% left upper corner of the screen, and testing this function, after
		% uncommenting the Screen('FillRect',...) line (approx line 393). The
		% second part is to be obtained by computing the difference between the
		% Fliptimestamp and VBLtimestamp when the particular Screen is flipped.
		% The number should correspond to half this difference.


        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        %%%%%%%%%%% the AV phase%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
		% draw fixation cross
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.yellow , [P.winCenter_x,P.winCenter_y], 1);
		Screen('DrawingFinished', P.win);
		[fixVBL,fix_onset] = Screen('Flip', P.win);  
		
		%prepare for the visual presentation
		%load in and translate trajectory
		vis_traj_pxl = trialpar.vis_trajectory * P.pxl_per_deg;
		%generate a rect for each positions; the size is exactly as the textrect the locations is along the moving trajectories in pixels
		centerCoordinate = {vis_traj_pxl+P.winCenter_x, zeros(length(vis_traj_pxl), 1)+P.winCenter_y};%in pixels, only horizontal
		blob_dstRects = cell2mat(cellfun(@CenterRectOnPoint, {Stimuli.blob.texrect}, centerCoordinate(1), centerCoordinate(2), 'UniformOutput',false));
		
		if add_flag.testAVsynchrony
			mynoise = 1 * MakeBeep(1000,0.0167,Stimuli.aud_fsample_play);
			Sound_temp = repmat(mynoise,[P.nAudioChannels 1]);
		else
			%for now, we had one sound each generation
			Sound_temp = MakeSound2(P, Stimuli, trialpar.aud_loc , 0.8, 1)';
		end

		R.stimGenTime{trialpar.iTrial} = GetSecs - R.stimGenTime{trialpar.iTrial};
		
		wait_fix_dur = Stimuli.fixation(1)+rand*(Stimuli.fixation(2)-Stimuli.fixation(1));
		% initial flip
		[vbl1, vis_onset1]= Screen('Flip', P.win, fix_onset + wait_fix_dur);
		
		% Buffer the Sound 
		PsychPortAudio('FillBuffer',P.AudioHandle, Sound_temp);

		PsychPortAudio('Start', P.AudioHandle, [], vis_onset1 + Delay_emprical);

		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' AV stimulus Onset'])
		end
		% draw the first blob
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.yellow , [P.winCenter_x,P.winCenter_y], 1);
		Screen('DrawTextures', P.win, Stimuli.blob.blobtex, [], blob_dstRects(1,:), [], [], [], [], [], kPsychDontDoRotation, Stimuli.blob.myblobpars);
		if add_flag.testAVsynchrony
			Screen('FillRect', P.win, P.white, [0 0 200 200]);
		end
		Screen('DrawingFinished', P.win);
		[BlobVBL, Blob0]=Screen('Flip', P.win, vis_onset1  + 0.5 * P.ifi) ;

		R.AVTrialOnset{trialpar.iTrial} = BlobVBL;
		R.AVStimOnset{trialpar.iTrial} = Blob0;
		
		
		if add_flag.testAVsynchrony % if test AV sync only present for 16.7mm
			PsychPortAudio('Stop', P.AudioHandle, 1); % this function will hold the whole scripts until the sound is stopped.
        
		else % real experiment 
		
			%%%% animation of the visual 
			for idx=2:length(vis_traj_pxl)
				% draw fixation cross
				Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.yellow , [P.winCenter_x,P.winCenter_y], 1);
				%draw gaussian blob
				Screen('DrawTextures', P.win, Stimuli.blob.blobtex, [], blob_dstRects(idx,:), [], [], [], [], [], kPsychDontDoRotation, Stimuli.blob.myblobpars);
				Screen('DrawingFinished', P.win);
				BlobVBL = Screen('Flip', P.win, BlobVBL  + 0.5 * P.ifi);
				%BlobVBL = Screen('Flip', P.win, BlobVBL  - 0.5 * P.ifi);
			end	%end for animation
        
			% Stop sound playback
			PsychPortAudio('Stop', P.AudioHandle, 1);  
		end
		
		%recover the visual display
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.yellow , [P.winCenter_x,P.winCenter_y], 1);
		Screen('DrawingFinished', P.win);
		Blob_offset = Screen('Flip', P.win, BlobVBL + 0.5 * P.ifi);
		
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' AV stimulus Offset'])
		end
		
        R.AVStimOffset{trialpar.iTrial} = Blob_offset; 
		
		%for test, save one sound 
		if add_flag.test_exp
			Stimuli.AVwavdat = Sound_temp;
		end
		Sound_temp=[];%reset the sound


	if ~add_flag.testAVsynchrony
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
		%please check the time variables, here, it is fishy
        % theretically, after sound display, 
		WaitSecs(Stimuli.TI_post_stim(1)+rand*(Stimuli.TI_post_stim(2)-Stimuli.TI_post_stim(1)));
        
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' AV task Onset'])
		end
		
        %%%%%%%%%%%%%%%%%%%%%%
        %%%%%ask question%%%%%
        %%%%%%%%%%%%%%%%%%%%%%
        
		%resp: 0 - mouse; 1 - keyboard; 2 - bitsi
		respTimeStart1 = GetSecs;
		%put the two questions in one go
        % 1) do AV come from the same location? 2) confidence level
        if add_flag.resp == 0 % mouse
			% if use mouse again, need to incorporate the 
	        %R = AskQuestMouse(Stimuli, R, P, trialpar.iTrial, D);
            
        elseif add_flag.resp == 1 && (~add_flag.test_exp) % keyboard in the main session
        
            %R = AskQuestKey(P, D, R, Stimuli, trialpar.iTrial);
            qtxt = 'Common source?' ;
			boundsText = Screen(P.win,'TextBounds',qtxt); %[L,T,R,B] from [L=0,T=0]
			DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), P.yellow);
            Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.yellow , [P.winCenter_x,P.winCenter_y], 1);
			Screen('DrawingFinished', P.win);   % No further drawing commands before Screen('Flip')
			[AVtaskVBL, AVtaskOnset] = Screen('Flip', P.win);

			%Wait for selection response
			LocQuestionAnsweredBool = 0;
			
			while ~LocQuestionAnsweredBool

				[KBpressed, ~, keyCode] = KbCheck;

				if KBpressed && (keyCode(P.answerKey1) || keyCode(P.answerKey2) || keyCode(P.answerKey3) || keyCode(P.answerKey4) || keyCode(P.answerKey5)|| keyCode(P.answerKey6))

					if keyCode(P.answerKey1) & ~add_flag.odd_flag %yes, low
						R.QuestResp{trialpar.iTrial}(1) = 1;
						R.QuestResp{trialpar.iTrial}(2) = 1;
					elseif keyCode(P.answerKey2) & ~add_flag.odd_flag %yes, med
						R.QuestResp{trialpar.iTrial}(1) = 1;
						R.QuestResp{trialpar.iTrial}(2) = 2;
					elseif keyCode(P.answerKey3) & ~add_flag.odd_flag %yes, high
						R.QuestResp{trialpar.iTrial}(1) = 1;
						R.QuestResp{trialpar.iTrial}(2) = 3;
					elseif keyCode(P.answerKey4) & ~add_flag.odd_flag %no, high
						R.QuestResp{trialpar.iTrial}(1) = 0;
						R.QuestResp{trialpar.iTrial}(2) = 3;   
					elseif keyCode(P.answerKey5) & ~add_flag.odd_flag %no, med
						R.QuestResp{trialpar.iTrial}(1) = 0;
						R.QuestResp{trialpar.iTrial}(2) = 2;
					elseif keyCode(P.answerKey6) & ~add_flag.odd_flag %no, low
						R.QuestResp{trialpar.iTrial}(1) = 0;
						R.QuestResp{trialpar.iTrial}(2) = 1;

					%odd number is oppsite
					elseif keyCode(P.answerKey1) & add_flag.odd_flag %no, low
						R.QuestResp{trialpar.iTrial}(1) = 0;
						R.QuestResp{trialpar.iTrial}(2) = 1;
					elseif keyCode(P.answerKey2) & add_flag.odd_flag %no, med
						R.QuestResp{trialpar.iTrial}(1) = 0;
						R.QuestResp{trialpar.iTrial}(2) = 2;
					elseif keyCode(P.answerKey3) & add_flag.odd_flag %no, high
						R.QuestResp{trialpar.iTrial}(1) = 0;
						R.QuestResp{trialpar.iTrial}(2) = 3;
					elseif keyCode(P.answerKey4) & add_flag.odd_flag %yes, high
						R.QuestResp{trialpar.iTrial}(1) = 1;
						R.QuestResp{trialpar.iTrial}(2) = 3;   
					elseif keyCode(P.answerKey5) & add_flag.odd_flag %yes, med
						R.QuestResp{trialpar.iTrial}(1) = 1;
						R.QuestResp{trialpar.iTrial}(2) = 2;
					elseif keyCode(P.answerKey6) & add_flag.odd_flag %yes, low
						R.QuestResp{trialpar.iTrial}(1) = 1;
						R.QuestResp{trialpar.iTrial}(2) = 1;
					end

					LocQuestionAnsweredBool = 1;
				end

			end
            
            
        elseif add_flag.resp == 1 && add_flag.test_exp % keyboard in the practice session
		
			R = AskQuestKey(P, D, R, trialpar.iTrial, add_flag.odd_flag);
		
		
        elseif add_flag.resp ==2 % bitsi
        
		
        end

        R.RespTime{trialpar.iTrial}(1) = GetSecs - respTimeStart1;

		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' AV task Offset'])
		end
		
	end % end if not add_flag.testAVsynchrony

end
