function [R, Stimuli,trialpar] = PresentStim(Stimuli, trial_design, eye_par, add_flag)
   
%try
    %%%%%%%%%%%%%%%%%%
    %%% Initialize %%%
    %%%%%%%%%%%%%%%%%%
    
    % Defining keys for input 
    KbName('UnifyKeyNames');
    
    % Defining keys for input 
    P.quitKey   = KbName('ESCAPE');                                         % To exit the program
    P.calibrateKey = KbName('C');                                           % Calibrate the eyetracker
    P.validateKey = KbName('V');                                            % Validate the eyetracker
    P.returnKey = KbName('Return');                                         % To accept the eyeLink prompts
	P.leftArrowKey = KbName('LeftArrow');                             % eyelink shortcut key
	P.rightArrowKey = KbName('RightArrow');                           % eyelink shortcut key
	P.upArrowKey = KbName('UpArrow');                             % eyelink shortcut key
	P.downArrowKey = KbName('DownArrow');                           % eyelink shortcut key
	P.AltKey = KbName('Alt');                           % eyelink shortcut key
	P.plusKey = KbName('+'); P.minusKey = KbName('-'); % eyelink shortcut key
	P.driftCorrctKey = KbName('D'); % initiate drift correction
	P.autoThrestKey = KbName('A'); 
	
	%%%%eyelink search limit shortcut key
	P.SR_shortcut1 = KbName('M');                                      %M = toggle on/off Mouse Simulation
	P.SR_shortcut2 = KbName('F4');										%F4 = toggle Search Limit on/off
	P.SR_shortcut3 = KbName('F5');										%F5 = toggle dynamic updating of the Search Limit area around the pupil
	
	P.spaceKey = KbName('Space'); 
	
	if add_flag.resp == 0 % mouse response
	
		P.leftMouseKey = KbName('left_mouse');                                  % To answer with Left Mouse button
		P.rightMouseKey = KbName('right_mouse');                                  % To answer with Right Mouse button
		
		% not updated to the latest version. Commented to throw a mistake when trying resp method 0
		% P.regularKeys = [P.quitKey, P.calibrateKey,P.validateKey,P.returnKey, P.spaceKey, ...
			% P.leftMouseKey, P.rightMouseKey, P.leftArrowKey, P.rightArrowKey, P.SR_shortcut1, P.SR_shortcut2, P.SR_shortcut3];
			
	elseif add_flag.resp == 1 % keyboard response

		P.answerKey1 = KbName('Q');  P.answerKey2 = KbName('W'); P.answerKey3 = KbName('E');
		P.answerKey4 = KbName('I'); P.answerKey5 = KbName('O'); P.answerKey6 = KbName('P'); 
%         P.answerKey1 = KbName('Z');  P.answerKey2 = KbName('X'); P.answerKey3 = KbName('C');
% 		P.answerKey4 = KbName('B'); P.answerKey5 = KbName('N'); P.answerKey6 = KbName('M'); 

		P.regularKeys = [P.quitKey, P.calibrateKey,P.validateKey,P.returnKey, P.spaceKey, ...
            P.answerKey1, P.answerKey2, P.answerKey3, P.answerKey4, P.answerKey5, P.answerKey6,  ...
			P.leftArrowKey, P.rightArrowKey, P.SR_shortcut1, P.SR_shortcut2, P.SR_shortcut3, ...
			P.upArrowKey, P.downArrowKey, P.AltKey, P.plusKey, P.minusKey, P.driftCorrctKey, P.autoThrestKey];
	
	elseif add_flag.resp == 2 % bitsi response

	
	end

    RestrictKeysForKbCheck(P.regularKeys);   
    
    % Initialize Screen
    [P, Stimuli] = SetupScreen(Stimuli,P, add_flag.testAVsynchrony);
    
	% Set up Eyelink
    if ~eye_par.dummymode
        el = SetupEyelink(eye_par, P);
    end
	% Set Drawing paramaters
    D = SetDrawingParameters(P, Stimuli, add_flag.resp); 
	
    % Prepare Audio Device
    P = SetupAudio(Stimuli,P);
    
    % Dummy call to GetSecs (because the first call may take some time and we'll use it later)
    dummy = GetSecs;

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%% Experiment Round%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    iTrial = 1; 
    %iBlock=1;
    blockstartTime = GetSecs;
    quit_n_save_flag = 0;
    
    % if ~add_flag.testAVsynchrony && add_flag.test_exp
        % nperblock = 4; % number per block
    % elseif ~add_flag.testAVsynchrony &&  ~add_flag.test_exp
        % nperblock = 64; % number per block
	% elseif add_flag.testAVsynchrony % test AV sync
		% nperblock = trial_design.total_trial_nr; % number per block
    % end

	% Before recording, we place reference graphics on the host display
	if ~eye_par.dummymode      
	%     EyelinkDoDriftCorrect(el); 
	%     WaitSecs(0.05);
		Eyelink('StartRecording');
	end
	%     record a few samples before we actually start displaying
	%     otherwise you may lose a few msec of data
	WaitSecs(0.1);
	

    while iTrial <= trial_design.total_trial_nr
	
		% are we testing the new parameters??
		% if ~add_flag.new_par
			% %define the trial parameters
			% trialpar = DefineTrial(trial_design, iTrial, Stimuli, 2); %trialpar = defineTrial(trial_design, iTrial, Stimuli, speed), default speed : 2
		% else 
			% trialpar = DefineTrial2(trial_design, iTrial, Stimuli);
		% end
		trialpar = DefineTrial2(trial_design, iTrial, Stimuli);

	    % For the first trial in each block , Ask participant to fixate
		if iTrial == 1 || trialpar.iBlock~=trial_design.trial_order(6, iTrial-1)

			%new block annoucement
			if  trialpar.trial_type == 1 % AV - A
			
				block_ann = 'Please put your fingers on the keyboard. Key Q/W/E for the left fingers, and key I/O/P for the right fingers. \n\n This block is a SOUND task block. You would first see a circular blob and hear a sound, then response to the common source questions. Next, a NEW SOUND is played. You would locate the SOUND using the keyboard. Please Press the SPACE key to continue.';
				
			elseif trialpar.trial_type == 2 % AV - V
			
				block_ann = 'Please put your fingers on the keyboard. Key Q/W/E for the left fingers, and key I/O/P for the right fingers. \n\n This block is a VISUAL task block. You would first see a circular blob and hear a sound, then response to the common source questions. Next, a NEW BLOB is showed on the screen. You would locate the BLOB using the keyboard. Please Press the SPACE key to continue.';
					
			else 
				%warning
			
			end
			
			DrawFormattedText(P.win, block_ann, 'center', 'center', P.drawColor, 80);
			Screen('Flip', P.win);
			
			%add quit function the whole experiment will quit and saving the data 
			
            while 1
                [KBpressed, ~, keyCode] = KbCheck;

                if KBpressed && keyCode(P.spaceKey) % if press space, continue
                    break
                end

                if KBpressed && keyCode(P.quitKey) % if the quit key is pressed
                    quit_n_save_flag = 1;
					if ~eye_par.dummymode
						Eyelink('Message', ['Quit Main Exp at Block ',num2str(trialpar.iBlock),' Trial ',num2str(iTrial)])
					end
					
                    break
                end
                
            end
			
			if ~eye_par.dummymode
				Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(iTrial),' Block Onset'])
			end
			
			%fixation msg
			myText = 'Please fixate your eyes on the cross';
			boundsText = Screen(P.win,'TextBounds',myText); %[L,T,R,B] from [L=0,T=0]
			DrawFormattedText(P.win, myText, round(P.winCenter_x-boundsText(3)/2), round(P.winCenter_y+boundsText(4)/2), P.drawColor);
			Screen('Flip', P.win);
			WaitSecs(1);
			
			% for the first trial in every block, add extra 750ms for fixations
			% draw fixation cross
            Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.yellow , [P.winCenter_x,P.winCenter_y], 1);
            Screen('DrawingFinished', P.win);    
            Screen('Flip', P.win);
			if ~eye_par.dummymode
				Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(iTrial),' first Fix Onset'])
			end
			WaitSecs(0.75);
			
		end
		
		%trialpar.iBlock = iBlock;
		
		if ~quit_n_save_flag % run a normal trial
			
			trialstartTime = GetSecs;

            % draw fixation cross
            Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.yellow , [P.winCenter_x,P.winCenter_y], 1);
            Screen('DrawingFinished', P.win);                          % No further drawing commands before Screen('Flip')
            Screen('Flip', P.win);

			if ~eye_par.dummymode
				Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(iTrial),' FixAV Onset'])
			end

            R.stimGenTime{iTrial} =  GetSecs;%mark the start of stimuli gen - will update later in PresentAV.m
            %initial response cell
            R.RespTime{iTrial}(1) = -99;% response time for the question. if no response, time will be -99
            R.RespTime{iTrial}(2) = -99;% response time for the localization task. if no response, time will be -99
            R.QuestResp{iTrial}(1) = -99;% question for common or seperate source judegement
            R.QuestResp{iTrial}(2) = -99;% confidence level for the common source judgement
            R.Resp_deg{iTrial} = -99; % locale response in degree for either A or V
			R.Resp_mispres{iTrial} = 0; % BOOL  misspressed for each participants in A/V phase


            %%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%GENERATE STIMULI%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%
            % the visual blob is generated once. visual movement is updated per
            % trial;
            % the auditory stimuli is generated every trial seperatedly for AV and A even for the same
            % location - this is to avoid subjects remembering the signature of
            % a specific white noise. 
            %
            %%%%%%%%%%%%%%%
            %%% visual %%%%
            %%%%%%%%%%%%%%%
            %for the first trial only, make the gaussian blob texture
            if iTrial == 1

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

            end
        
            %%%%%%%%%%%%%
            %%% sound %%%
            %%%%%%%%%%%%%

            %%%% every trial generate a new sound sequence, so that
            %%%% subjects won't remeber the signature of white noise

			%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%present one compound trial%%%%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			
			%%%%%%%%%%%%%%%%%%%
			%%%%%%AV phase%%%%%
			%%%%%%%%%%%%%%%%%%%
			
			[Stimuli, R] = PresentAV(Stimuli, P, D, R, trialpar, eye_par, add_flag);
			
			if ~add_flag.testAVsynchrony 
			
				WaitSecs(Stimuli.ITI_AV(1)+rand*(Stimuli.ITI_AV(2)-Stimuli.ITI_AV(1)));
			
				if  trialpar.trial_type == 1 % AV - A
				
					%%%%%%%%%%%%%%%%%%%
					%%%%%%A phase%%%%%%
					%%%%%%%%%%%%%%%%%%%
					%resp: 0 - mouse; 1-keyboard; 2-bitsi
					[Stimuli, R] = PresentA(Stimuli, P, D, R, trialpar, add_flag, eye_par);
					
				elseif trialpar.trial_type == 2 % AV - V
				
					%%%%%%%%%%%%%%%%%%%
					%%%%%%V phase%%%%%%
					%%%%%%%%%%%%%%%%%%%
					[Stimuli, R] = PresentV(Stimuli, P, D, R, trialpar, add_flag.resp, eye_par);

				else
					%warning
				end
            
				R.trialDur{iTrial} = GetSecs - trialstartTime;
				
			
			end % end if
			
			%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %%%%END one compound trial%%%%
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
			
            %%%%%%%%%%%%%%%%%
            %%% Pauze? %%%%%%
            %%%%%%%%%%%%%%%%%

            %compulsory break at the end of each block. can be changed to self-pace mode
            if iTrial == trial_design.total_trial_nr % the last trial
			    WaitSecs(0.5);
			    DrawFormattedText(P.win, 'This is the end of this session. Thank you very much for your participation.', 'center', 'center', P.drawColor, 80);
                Screen('DrawingFinished', P.win);
                Screen('Flip', P.win); 
                WaitSecs(1);
				
				if ~eye_par.dummymode
					Eyelink('Message', 'End of Main Task')
				end
				
			elseif trialpar.iBlock~=trial_design.trial_order(6, iTrial+1)  % the end of each block, except for the last block
                WaitSecs(0.5);
				if ~eye_par.dummymode
					Eyelink('Message', ['End of Main Block ',num2str(trialpar.iBlock)])
				end
				
				if ~add_flag.test_exp % for real exp , take a one min compulsory break
				
					brk_msg = ' Now Please take a compulsory break for one minute.';
					DrawFormattedText(P.win, brk_msg, 'center', 'center', P.drawColor, 80);
					Screen('DrawingFinished', P.win);      
					Screen('Flip', P.win); 
					
					startbrkTime = GetSecs;
					while 1
						if GetSecs - startbrkTime > 60
							break 
						end
					end
				
					brk_msg = ' Now is after 1 miniute. When you are ready, Please press the SPACE key to continue. If you wish to take a longer break, please kindly let me know. ';
					DrawFormattedText(P.win, brk_msg, 'center', 'center', P.drawColor, 80);
					Screen('DrawingFinished', P.win);      
					Screen('Flip', P.win); 
				
					while 1
						[KBpressed, ~, keyCode] = KbCheck;
						if KBpressed && keyCode(P.spaceKey) 
							break;
						elseif  KBpressed && ~eye_par.dummymode && keyCode(P.calibrateKey) 
							cal_msg = 'Now we do calibrate. Please fixate the dots on the following screens.';
							DrawFormattedText(P.win, cal_msg, 'center', 'center', P.drawColor, 80);
							Screen('DrawingFinished', P.win);      
							Screen('Flip', P.win); 
							WaitSecs(1);
							
							EyelinkDoTrackerSetup(el);
							Eyelink('Command', 'set_idle_mode');
							WaitSecs(0.05);
							Eyelink('StartRecording');
							break
						elseif KBpressed && ~eye_par.dummymode && keyCode(P.driftCorrctKey) 
							cal_msg = 'Now we do drift correction. Please fixate the dots on the following screens.';
							DrawFormattedText(P.win, cal_msg, 'center', 'center', P.drawColor, 80);
							Screen('DrawingFinished', P.win);      
							Screen('Flip', P.win); 
							WaitSecs(1);
							
							EyelinkDoDriftCorrection(el);
							Eyelink('Command', 'set_idle_mode');
							WaitSecs(0.05);
							Eyelink('StartRecording');
							break
						end%end if
					end%end while
				
				else % for practice self-paced breaks

					brk_msg = ' Now Please take a break. When you are ready, press ANY key to continue.';
					DrawFormattedText(P.win, brk_msg, 'center', 'center', P.drawColor, 80);
					Screen('DrawingFinished', P.win);      
					Screen('Flip', P.win); 
					KbStrokeWait;
					
				end % end if add_flad.test_exp
				
               %record the block duration 
               R.blockDur{trialpar.iBlock} = GetSecs - blockstartTime;
               blockstartTime = GetSecs;
               WaitSecs(1);

            else % the trials within a block
                % wait for the inter-trial interval
                WaitSecs(Stimuli.ITI(1)+rand*(Stimuli.ITI(2)-Stimuli.ITI(1)));
				if ~eye_par.dummymode
					Eyelink('Message', ['Main Exp Block ',num2str(trialpar.iBlock),' Trial ',num2str(iTrial),' Compound Offset'])
				end
            end

            iTrial = iTrial+1;

            %reset trial parameter
			trialpar=[];
			%Stimuli.WavDat = [];
			%Stimuli.TestWavDat=[];

		else %quite and save
			
			break % will the prev data be saved?? - yes
		
        end


    end %end all trials

        
        
    % Clean up
    Priority(0);                        % Shutdown realtime scheduling:
    ListenChar;                         % Reenable all keys output to Matlab
    RestrictKeysForKbCheck([]);         % Reenable all keys for KbCheck

    ShowCursor;                         % Show Cursor
    Screen('CloseAll');                 % Close display(s)
    
    if isfield(P,'AudioHandle')
        Snd('Close');
        PsychPortAudio('Close');        % Shutdown sound driver
    end
    
% catch
%     % Clean up
%     Priority(0);                        % Shutdown realtime scheduling:
%     ListenChar;                         % Reenable all keys output to Matlab
%     RestrictKeysForKbCheck([]);         % Reenable all keys for KbCheck

%     ShowCursor;                         % Show Cursor
%     Screen('CloseAll');                 % Close display(s)
% 
%     if isfield(P,'AudioHandle')
%         PsychPortAudio('Close');        % Shutdown sound driver
%     end
% end
	
end