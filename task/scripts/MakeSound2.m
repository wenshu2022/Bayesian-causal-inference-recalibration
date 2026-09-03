function wavDat = MakeSound2(P, Stimuli, aud_loc, volumn, norm)

	% generate the sound with 0.5*flip duration under 192000 sampling rate and plays it in 96000.
	% the result would be one sound per flip
	samplesPerPosition = round(Stimuli.aud_duration* Stimuli.aud_fsample);
	white_noise = dsp.ColoredNoise('white',samplesPerPosition, 1);
	noiseSignal = volumn * white_noise();
	
	%Create a hanning ramp (onset and offset)
	nramp   = round((Stimuli.aud_ramp_duration) * Stimuli.aud_fsample); % ramp Duration in samples
	ramps           = hanningWindow(nramp*2);
	ramp_on         = ramps(1:nramp)';
	ramp_off        = ramps(nramp+1:end)';
	taper           = [ramp_on ones(1,samplesPerPosition-nramp*2) ramp_off]';
    
    
    %For a given auditory trajectory, translate into the SOFA standards.
    if aud_loc <=0
		new_aud_loc = -aud_loc;
	else
		new_aud_loc = 360-aud_loc;
	end

    %for the left degrees in the aud_traj (negative value) - should be postive and smaller than 90 degrees 
    %(since we are experimenting on the front)
    %for the right degrees in the aud_traj (positive value) - should be 360 - value and greater than 270 degrees.

    %also get the corresponding index of the desirable positions in the original positions
    [~,aud_loc_idx] = ismember(new_aud_loc,P.azimuth_int);

    %%create two filters for later use
    leftFilter = dsp.FIRFilter('NumeratorSource','Input port');
    rightFilter = dsp.FIRFilter('NumeratorSource','Input port');

    %convolve the white noise through HRTF for a sequence of positions
	leftChannel = taper.*leftFilter(noiseSignal,P.hrirL(:, aud_loc_idx)');
	rightChannel = taper.*rightFilter(noiseSignal,P.hrirR(:, aud_loc_idx)');
	%save two channels of soundwaves
	wavDat= [leftChannel,rightChannel];%samples*two_channels

    %normalization
    if norm
        %parameter for sound normalization
        maxvalue = 20; % might be adjusted if you run into an endless while loop below, but do not use too high values, otherwise it squeezes the amplitude of the sound
        clipping= true;
        wavDat = norm_sound(wavDat, maxvalue, clipping);
    end
    
end

%helper function sound normalization
function Sound = norm_sound(Sound_temp, maxvalue, clipping)
		
	if clipping
		% Normalize to get the sound between -1 and 1 (otherwise PTB clips the values outside)
		if (max(max(max(abs(Sound_temp)))) <= maxvalue)
			Sound = Sound_temp / maxvalue;
		end
		
	else
		%If no clipping, no normalization
		Sound = Sound_temp;
	end%end if clipping

end%end helper function