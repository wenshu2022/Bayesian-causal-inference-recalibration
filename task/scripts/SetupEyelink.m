function el = SetupEyelink(eye_par, P)


el                          = EyelinkInitDefaults(P.win);

el.backgroundcolour         = P.vis_intensity_background;
el.calibrationtargetcolour  = P.yellow; % Same as the stimuli color in AV phase
%probably more features than can be used
el.msgfontcolour           = P.yellow;
el.imgtitlecolour          = P.yellow;

el.calibrationtargetsize  = 1;
el.calibrationtargetwidth = 0.5;
el.displayCalResults = 1;
el.targetbeep             = 0;
el.feedbackbeep           = 0;

% Update the changes to Eyelink
EyelinkUpdateDefaults(el);


% Check if eyelink has been initiated
if ~EyelinkInit(eye_par.dummymode)
	Eyelink('Shutdown'); sca;
	% Restore keyboard output to Matlab:
	ListenChar(0);
	error('Eyelink initialization aborted!\n');
end

% Check the version
[~, vs] = Eyelink('GetTrackerVersion');
fprintf('Running experiment on a ''%s'' tracker.\n', vs );

% Setup eyelink file name 
fprintf('EDFFile: %s\n', eye_par.edfFile);

% Open edf file to record data to 
%{
status = Eyelink('OpenFile', edfFile);
if status ~=0 
	fprintf('Cannot creat EDF files ''%s'' ', edfFile);
	Eyelink('shutdown');
	sca;
	return;
end
%}

% Open file on host computer
if Eyelink('Openfile', eye_par.edfFile)                               
	Eyelink('Shutdown'); sca; %shutdown Eyelink
	% Restore keyboard output to Matlab:
	ListenChar(0); 
	error('Cannot create EDF file');
end

Eyelink('Command','add_file_preamble_text = "%s"', eye_par.header_msg);  

% Make sure we're still connected.
if Eyelink('IsConnected')~=1 && ~eye_par.dummymode
	Eyelink('Shutdown'); sca; %shutdown Eyelink
	% Restore keyboard output to Matlab:
	ListenChar(0); 
	error('No Eyelink connection exiting');
end

[width, height] = Screen('WindowSize', P.screenNumber);


% Setup tracker configuration, setting the proper recording resolution,
% proper calibration type, as well as the data file content;
Eyelink('command','screen_pixel_coords = %ld %ld %ld %ld', 0, 0, width-1, height-1);
Eyelink('message', 'DISPLAY_COORDS %ld %ld %ld %ld', 0, 0, width-1, height-1);

% set parser (conservative saccade thresholds)
%Cognitive Configuration:
%Eyelink('Command','select_parser_configuration = 0');  %standard saccade
%either select_parser_configuration or the next two??
Eyelink('command', 'saccade_velocity_threshold = 35');
Eyelink('command', 'saccade_acceleration_threshold = 9500');

% set edf data 
% Sets which types of events will be written to EDF file.
%Eyelink('command', 'file_event_filter = LEFT,RIGHT,FIXATION,FIXUPDATE,MESSAGE,INPUT'); 
%Eyelink('command', 'file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS,INPUT');
Eyelink('command', 'file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT,FIXUPDATE');
Eyelink('command', 'file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS,INPUT');
Eyelink('command', 'link_event_data = GAZE,GAZERES,HREF,AREA,VELOCITY');

% set link data (can be used to react to events online)
% Sets data in events sent through link. - need??????
%Eyelink('command', 'link_event_data = GAZE,GAZERES,HREF,AREA,VELOCITY'); 
% Sets which types of events will be sent through link.
%Eyelink('command', 'link_event_filter = LEFT,RIGHT,FIXATION,MESSAGE,BUTTON');

%allow to use the big button on the eyelink gamepad to accept the
% calibration/drift correction target
%Eyelink('command', 'button_function 5 "accept_target_fixation"');

% change camera setup options
% set pupil Tracking model in camera setup screen
% no = centroid. yes = ellipse
Eyelink('command', 'use_ellipse_fitter = no');
% set sample rate in camera setup screen
Eyelink('command', 'sample_rate = %d',1000); % could be lower 

% Set calibration type.
Eyelink('command', 'calibration_type = HV9');
%Eyelink('Command','binocular_enabled = Yes');
% you must send this command with value NO for custom calibration
% you must also reset it to YES for subsequent experiments
Eyelink('command', 'generate_default_targets = YES');

%set a smaller area for calibration/validation 
% could be useful in calibration takes forever to complete
Eyelink('command','calibration_area_proportion = 0.5 0.5');
Eyelink('command','validation_area_proportion = 0.5 0.5');

%enable automatic calibration
[result, reply]=Eyelink('ReadFromTracker','enable_automatic_calibration');

if reply % reply = 1
    fprintf('Automatic sequencing ON');
else
    fprintf('Automatic sequencing OFF');
end

% enter Eyetracker camera setup mode, calibration and validation
EyelinkDoTrackerSetup(el);

end