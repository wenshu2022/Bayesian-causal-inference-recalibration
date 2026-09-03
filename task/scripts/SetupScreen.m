function [P, Stimuli]= SetupScreen(Stimuli,P, testAVsynchrony)

%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Initialize Screen %%%
%%%%%%%%%%%%%%%%%%%%%%%%%

% Get the list of Screens and choose the one with the highest screen number. Choosing the display with the highest dislay number is a best guess about where you want the stimulus displayed.
% Screen 0 is, by definition, the display with the menu bar. Often when two monitors are connected the one without the menu bar is used as the stimulus display.  
P.screenNumber = max(Screen('Screens'));                                                        %Projector Screen

% Prepare setup of imaging pipeline for onscreen window.
% This is the first step in the sequence of configuration steps
PsychImaging('PrepareConfiguration'); 
% Open a fullscreen, onscreen window with gray background. Enable 32bpc
% floating point framebuffer via imaging pipeline on it, if this is possible
% on your hardware while alpha-blending is enabled. Otherwise use a 16bpc
% precision framebuffer together with alpha-blending. We need alpha-blending
% here to implement the nice superposition of overlapping gabors. The demo will
% abort if your graphics hardware is not capable of any of this.
PsychImaging('AddTask', 'General', 'FloatingPoint32BitIfPossible');
  
% Open window. 
if ~testAVsynchrony
	[P.win,P.winRect]=PsychImaging('OpenWindow',P.screenNumber,Stimuli.vis_intensity_background);    %Projector Screen
else
	[P.win,P.winRect]=PsychImaging('OpenWindow',P.screenNumber, 0);    %Projector Screen - black
end
% Hide the cursor
HideCursor;
% Switch to realtime-priority to reduce timing jitter and interruptions caused by other applications and the operating system itself:
Priority(MaxPriority(P.win));
% Prevent keyboard presses to be executed within MATLAB (we don't want to edit the scripts!). This cannot be used if KbQueue commands are required.            
ListenChar(2);   
% Enable antialiasing blending function (so we can use line smoothing in the DrawLines command)
Screen('BlendFunction', P.win, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

% Colours
P.white = WhiteIndex(P.screenNumber);
P.black = BlackIndex(P.screenNumber);
P.grey = round((P.white + P.black) / 2);
P.red = [128 0 0];
%P.green = [0 128 0];
%P.darkgreen = [0 64 0];
%P.blue = [0 0 192];
%P.yellow = [192 96 0];
P.yellow = [234, 164, 20]; % AV phase, yellowish
P.green = [170, 198, 39]; % A phase, greenish
P.pink = [237, 96, 119]; % V phase, pinkish

P.drawColor = Stimuli.vis_intensity_drawText;
P.vis_intensity_background = Stimuli.vis_intensity_background;

% Text Specifics
Screen('TextFont',P.win,'Arial');
Screen('TextSize',P.win,24);
Screen('TextStyle',P.win,0);                %0=normal, 1=bold, 2=italic, 4=underline
Screen('TextColor',P.win,P.drawColor);

% Measure monitor refresh interval.
% Flip three times (bug). Otherwise screen will start flickering
Screen('Flip',P.win);    Screen('Flip',P.win);     Screen('Flip',P.win);
% This will trigger a calibration loop of minimum 100 valid samples and return the estimated inter-flip-interval in 'P.ifi': interflip interval (in seconds).
% We require an accuracy of 0.5 ms == 0.0005 secs. If this level of accuracy can't be reached, we time out after 5 seconds.  
[P.ifi,~,~] = Screen('GetFlipInterval',P.win,100,0.0005,5);
% Correct the stimulus duration (to ifi's)
Stimuli.stim_dur_in_flips = round((Stimuli.aud_duration*2)/P.ifi); 

disp(['stim duration in flips is ' num2str(Stimuli.stim_dur_in_flips)]);
%Stimuli.aud_duration = P.stim_dur_in_flips * P.ifi;

% Define window center, width and height (in pixels).     
[P.winCenter_x,P.winCenter_y] = RectCenter(P.winRect);                   

% Calculate the size of one pixel (in cm).
P.width_of_1pix = Stimuli.cpu.width_cm/P.winRect(3);                    %in cm
P.height_of_1pix = Stimuli.cpu.height_cm/P.winRect(4);                  %in cm

% translate visual degree to pixels
P.pxl_per_deg = P.winRect(3) / (2*atand(Stimuli.cpu.width_cm/Stimuli.cpu.view_dist_cm/2)) ;    % pixels per degree
P.half_deg_h = P.winRect(4) /P.pxl_per_deg / 2; %horizontal; maximum viewing range: -screen.half_deg_h ~ screen.half_deg_h

% Express the distance to the screen in number of pixels (separate for width and height) 
P.dist2Screen_nPixWidth = Stimuli.cpu.view_dist_cm/P.width_of_1pix;
P.dist2Screen_nPixHeight = Stimuli.cpu.view_dist_cm/P.height_of_1pix;
% We can now calculate the number of pixels from the screen_centre by: Nr_pixels = round(tand(visual_angle)*P.dist2Screen_nPixWidth);    (or use P.dist2Screen_nPixHeight instead)

end %[EOF]
