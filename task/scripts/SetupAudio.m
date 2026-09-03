function P = SetupAudio(Stimuli,P)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Prepare Audio Device %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%    

% Open sound driver for high timing precision, stereo playback with a certain given sampling frequency: 
% This has to be called with input argument 1 in order to achieve really low latency!
InitializePsychSound(1);

%Set the reqLatencyClass level to 2; this means: Take full control over the audio device, even if this causes other sound applications to fail or shutdown.
reqLatencyClass = 2;
%Set the number of channels that we will be using (2: one for left, and one for right)     
P.nAudioChannels = 2;
buffersize           = 0;     % Pointless to set this. Auto-selected to be optimal.
suggestedLatencySecs = [];

%Open the audioDevice with the selected settings and the sampling frequency as was defined earlier    
P.AudioHandle = PsychPortAudio('Open', [], [], reqLatencyClass, Stimuli.aud_fsample_play, 2, buffersize, suggestedLatencySecs);


% The visuo-audio delay (visual onset minus auditory onset) of the system depends on the setup we use. Therefore we need to measure this manually!   
% It is important to do so since this introduces temporal asynchronies that will decrease the probability of multisensory integration.     
% On setup 'PSYCHL-120046' it is around -9 ms, This means that the auditory onset is 9 ms later than the visual onset. Therefore we set the auditory onset 9 ms earlier to compensate for the delay  
%%%%%%%%%%%%%%%%
latBias = 0;%%%% to-be update
PsychPortAudio('LatencyBias',P.AudioHandle,latBias);

% Generate some beep sound: 1000 Hz, 0.1 secs, 50% amplitude and fill it in the buffer for preheating playback (this avoids deformations of the first sound). 
mynoise = 0.5 * MakeBeep(1000,0.1,Stimuli.aud_fsample_play);
mynoise = repmat(mynoise,[P.nAudioChannels 1]);
PsychPortAudio('FillBuffer',P.AudioHandle,mynoise);
% Preheat: run audio device once silently, with volume set to zero.
PsychPortAudio('Volume',P.AudioHandle,0);
PsychPortAudio('Start',P.AudioHandle,1,0);                  %repetitions = 1 , when = 0 delay   
PsychPortAudio('Stop',P.AudioHandle,1);                     %waitForEndOfPlayback = 1
% Set Volume to prescribed level
PsychPortAudio('Volume',P.AudioHandle,Stimuli.aud_volume);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Prepare Generation of Sounds %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%load IR data
load('.\IRdata_192000_pm40deg.mat' );

P.azimuth_int = IRdata.az;
P.hrirL = IRdata.hrirL;
P.hrirR = IRdata.hrirR;

%check the sampling rate 
if Stimuli.aud_fsample ~= IRdata.SamplingRate
	error("sampling rate is not the same!!!");
end

% for using PsychPortAudio and Snd() simultaneously in EyelinkDoDriftCorrection
Snd('Open', P.AudioHandle);


end %[EOF]