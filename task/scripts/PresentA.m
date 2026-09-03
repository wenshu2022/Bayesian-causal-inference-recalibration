function [Stimuli, R] = PresentA(Stimuli, P, D, R, trialpar, add_flag, eye_par)
		
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        %%%%%%%%%%% the A phase%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        % draw fixation cross 
        Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.green , [P.winCenter_x,P.winCenter_y], 1);
        Screen('DrawingFinished', P.win); 
        Screen('Flip', P.win); 
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' FixA Onset'])
		end
			
		WaitSecs(Stimuli.fixation(1)+rand*(Stimuli.fixation(2)-Stimuli.fixation(1)));
		
		%for now, we had one sound each generation
		%Sound_test = Stimuli.TestWavDat'; %samples * two channels
		Sound_test = MakeSound2(P, Stimuli, trialpar.aud_test_loc, 0.8, 1)';

        % Buffer the Sound 
        PsychPortAudio('FillBuffer',P.AudioHandle, Sound_test);
        
        ATrialStartTime = GetSecs;
		
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' A stimulus Onset'])
		end
		
        PsychPortAudio('Start', P.AudioHandle, [], []);		

        % Stop sound playback
        PsychPortAudio('Stop', P.AudioHandle, 1);  
		
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' A stimulus Offset'])
		end
		
        R.Atrialdur{trialpar.iTrial} = GetSecs - ATrialStartTime; 
		
		%for test, save one sound 
		if add_flag.test_exp
			Stimuli.AVwavdatTest = Sound_test;
		end
		
		Sound_test=[];%reset the sound
		

        WaitSecs(Stimuli.TI_post_stim(1)+rand*(Stimuli.TI_post_stim(2)-Stimuli.TI_post_stim(1)));


        %%%%%%%%%%%%%%%%%%%%%%%
        %%%%%ask question1%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%

		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' A task Onset'])
		end
		
		%resp: 0 - mouse; 1 - keyboard; 2 - bitsi
		respTimeStart2 = GetSecs;
		% indicate the A location
		if add_flag.resp == 0 % mouse
		
			%R = CollectAlocMouse(R, P, Stimuli, D, trialpar.iTrial); % NEED TO UPDATE FUNCTION IF WANT TO USE MOUSE

		elseif add_flag.resp == 1 % keyboard

			% draw fixation cross 
			Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.green , [P.winCenter_x,P.winCenter_y], 1);
			qtxt = 'Locate A' ;
			boundsText = Screen(P.win,'TextBounds',qtxt); %[L,T,R,B] from [L=0,T=0]
			DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), P.green);
			Screen('DrawingFinished', P.win);                                            % No further drawing commands before Screen('Flip')
			Screen('Flip', P.win); 
		
			LocQuestionAnsweredBool = 0;
			while ~LocQuestionAnsweredBool 

				[KBpressed, ~, keyCode] = KbCheck;
				
				if KBpressed && (keyCode(P.answerKey1) || keyCode(P.answerKey2) || keyCode(P.answerKey3) || keyCode(P.answerKey4) || keyCode(P.answerKey5)|| keyCode(P.answerKey6))
					
					if keyCode(P.answerKey2)
						R.Resp_deg{trialpar.iTrial} = Stimuli.loc_pool(1);
						LocQuestionAnsweredBool = 1;
						
					elseif keyCode(P.answerKey3)
						R.Resp_deg{trialpar.iTrial} = Stimuli.loc_pool(2);
						LocQuestionAnsweredBool = 1;
						
					elseif keyCode(P.answerKey4)
						R.Resp_deg{trialpar.iTrial} = Stimuli.loc_pool(3);
						LocQuestionAnsweredBool = 1;
						
					elseif keyCode(P.answerKey5)
						R.Resp_deg{trialpar.iTrial} = Stimuli.loc_pool(4);
						LocQuestionAnsweredBool = 1;

					else % if press answerKey1 and answerKey6
						R.Resp_mispres{trialpar.iTrial} = 1;
					end

				end

			end %End of question's while-loop 


		elseif add_flag.resp ==2 % bitsi
		
		end
		
        R.RespTime{trialpar.iTrial}(2) = GetSecs - respTimeStart2;
		
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' A task Offset'])
		end

end
