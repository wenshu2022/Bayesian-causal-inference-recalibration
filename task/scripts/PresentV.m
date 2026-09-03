function [Stimuli, R] = PresentV(Stimuli, P, D, R, trialpar, resp, eye_par)

        %%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%        
        %%%%%%%%%%% the V phase%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%% 
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        % draw fixation cross - change the color as inidication for response expectation
        Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.pink , [P.winCenter_x,P.winCenter_y], 1);
        Screen('DrawingFinished', P.win);
        Screen('Flip', P.win); 
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' FixV Onset'])
		end

		WaitSecs(Stimuli.fixation(1)+rand*(Stimuli.fixation(2)-Stimuli.fixation(1)));
		
		vis_test_pxl = trialpar.vis_test_loc * P.pxl_per_deg;
		blob_dstRect_test = CenterRectOnPoint(Stimuli.blob.texrect, vis_test_pxl+P.winCenter_x, P.winCenter_y); 
		
		%draw gaussian blob
		%draw fixation cross 
        Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.pink , [P.winCenter_x,P.winCenter_y], 1);
		Screen('DrawTextures', P.win, Stimuli.blob.blobtex, [], blob_dstRect_test, [], [], [], [], [], kPsychDontDoRotation, Stimuli.blob.myblobpars);
		Screen('DrawingFinished', P.win);
		[stimVBL, stim_onset] = Screen('Flip', P.win); 
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' V stimulus Onset'])
		end
		% alternatively
		%WaitSecs(Stimuli.aud_duration*2);% wait time is the same as in auditory stimuli
		%%%% replace with the real auditory duration
		
		Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.pink , [P.winCenter_x,P.winCenter_y], 1);
		Screen('DrawingFinished', P.win);
		[fixVBL, stim_offset] = Screen('Flip', P.win, stim_onset + Stimuli.aud_duration*2 -0.5*P.ifi); 
		
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' V stimulus Offset'])
		end
		
        WaitSecs(Stimuli.TI_post_stim(1)+rand*(Stimuli.TI_post_stim(2)-Stimuli.TI_post_stim(1)));


        %%%%%%%%%%%%%%%%%%%%%%%
        %%%%%ask question1%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%

		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' V task Onset'])
		end
		
		% draw fixation cross - change the color as inidication for response expectation
		qtxt = 'Locate V' ;
		boundsText = Screen(P.win,'TextBounds',qtxt); %[L,T,R,B] from [L=0,T=0]
		DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/4*3+boundsText(4)/2), P.pink);
        Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.pink , [P.winCenter_x,P.winCenter_y], 1);
		Screen('DrawingFinished', P.win);
		Screen('Flip', P.win); 

		%resp: 0 - mouse; 1 - keyboard; 2 - bitsi
		respTimeStart2 = GetSecs;
		% indicate the A location
		if resp == 0 % mouse
		
			R = CollectAlocMouse(R, P, Stimuli, D, trialpar.iTrial);

		elseif resp == 1 % keyboard

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

		elseif resp ==2 % bitsi
		
		end
		
        R.RespTime{trialpar.iTrial}(2) = GetSecs - respTimeStart2;
		
		if ~eye_par.dummymode
			Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(trialpar.iTrial),' V task Offset'])
		end

end
