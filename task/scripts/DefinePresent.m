function Stimuli = DefinePresent

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%  LOCATIONS  %%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%

%% set the test pool - exp 1

Stimuli.loc_pool = [ -12, -4, 4, 12]; % MUST be from left to right order !!!!!!!
Stimuli.aud_pool_train = [ -12, -4, 4, 12];% MUST be from left to right order !!!!!!!
%Stimuli.aud_pool_train = [-20, -12, -4, 4, 12, 20];% MUST be from left to right order !!!!!!!

Stimuli.aud_duration = 0.0167 * 8 /2;% in sec. NOTE! THIS IS ONLY HALF OF THE REAL DURATION
% 0.0167 is the duration of one flip
% % in this scrip, we create auditory stimuli half the target length and play
% % it with double sampling frequency (bc I think it sound better)
Stimuli.aud_ramp_duration = Stimuli.aud_duration * 0.1 /2;% ramp-on or ramp-off
%% set the test pool - exp 2 
Stimuli.min_dis = 8;
Stimuli.max_dis = 24;
	
% if new_par % new par for testing - pilot subject 
	% Stimuli.min_dis = 8;
	% Stimuli.max_dis = 24;

% else % old par
	% %% set the test pool - exp 2 
	% Stimuli.min_dis = 16;
	% Stimuli.max_dis = 32;
% end

%% Auditory
Stimuli.aud_volume          = 0.5;%0.05                                     %0.05 (and system vol = 50%) with Sennheiser HD 280 Pro headphones leads to +/- 70 dB sounds --> 1 is maximum, 0 minimum. The scale is logarithmic.
Stimuli.aud_fsample         = 192000;                              %%% Stimuli.aud_fsample_play is the sampling rate for playing the sound
Stimuli.aud_fsample_play         = 96000; 

% Stimuli.aud_duration = 0.0167 * (Stimuli.abs_inc+1)/2; % 0.0167 is the duration of one flip
% % in this scrip, we create auditory stimuli half the target length and play
% % it with double sampling frequency (bc I think it sound better)
% Stimuli.aud_ramp_duration = Stimuli.aud_duration * 0.1/2;% ramp-on or ramp-off

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%  VISUAL STIM  %%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
                                    
Stimuli.vis_intensity_background = 0.5; %or 0.5                       %the background is grey (30=15 cd/m2) --> N.b. The luminance has been recalibrated to be linearly correlated with intensity levels
Stimuli.vis_intensity            = [45 45 45];                               %intensity value is integer in between 0 and 255 (45=20 cd/m2)  
Stimuli.vis_intensity_drawText   = 150;                                      %intensity value for drawing items and text (previously P.grey)     

%% Visual gaussian blob
% define the rectangula pocket of the blob
Stimuli.blob.width = 1; %1.5  %in visual degree, radius (diameter/2)
% Spatial constant of the exponential "hull" (sigma in the expotential formula)
Stimuli.blob.sc = 0.5;  % in visual angle
% Contrast of grating:
Stimuli.blob.contrast = 30; % 'contrast' is the amplitude of your blob in intensity units - A factor
							% that is multiplied to the evaluated blob equation before converting the
							% value into a color value. 'contrast' may be a bit of a misleading term here... (from comments in github)


%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%% SCREEN  %%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%                                   %Note that this leads to a minimum step size of ~0.5° (the time-difference of 1 sample at 192000 Hz = ~5 microseconds)    
% Computer specific distances (in meters)                                   

%Stimuli.cpu.fixx_height_from_bottom   = 0.20;                                     %Height of the fixation cross relative to the bottom of the screen (middle) - set relative to chin-rest
%Stimuli.cpu.usable_height_from_bottom = 0.40;                                     %We only use the bottom part of the projected area for presenting (anything). 
%Stimuli.cpu.usable_width              = 0.48;                                     %We only use the middle (width) of the projected area for presenting text etc. (but stimuli run over this hypothetical border)


Stimuli.cpu.width_cm   = 53;   % horizontal dimension of viewable screen (cm)
Stimuli.cpu.height_cm   = 30;   % vertical dimension of viewable screen (cm)
Stimuli.cpu.view_dist_cm = 50;   % viewing distance (cm)


%screen.pxl_per_deg = pi * screen.width_pxl / atan(S.cpu.width_cm/S.cpu.view_dist_cm/2) / 360;    % pixels per degree
%screen.half_deg_h = screen.width_pxl /screen.pxl_per_deg / 2; %horizontal; maximum viewing range: -screen.half_deg_h ~ screen.half_deg_h

%%%set restriction to response time

%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%% TIMING  %%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%% 
Stimuli.fixation = [0.75, 1]; % in s
Stimuli.TI_post_stim = [0.4, 0.6] ; 
Stimuli.ITI = [1, 1.2];
Stimuli.ITI_AV = [0.4, 0.6] ; 

end %[EOF]