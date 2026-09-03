function [SubjectData, F] = SetSubjIDandTask(rootPath)

%Initialize output
t_datetimeObject = datetime('now');    
SubjectData.CreatedSes = datestr(t_datetimeObject);
F.rootPath = rootPath;


expriments = {'select', 'exp1', 'exp2', 'practice', 'training'};
[expNr,continueBool] = taskDialog(expriments,1,'Expriment','Select a Expriment');

if ~continueBool
    errordlg('Program is aborted');                             %dialog window was closed
    error('Program is aborted');
end

if expNr == 1 
    errordlg('No Expriment was Selected');                   %Default option 'Select' was not changed
    error('No Expriment was Selected');

elseif expNr == 4 %%%test the stimuli or the practice session

    SubjectData.exp_type = 'prac';
	SubjectData.ses_nr = 0;
	SubjectData.exp_nr = 0;
	
elseif  expNr == 2

	SubjectData.exp_type = 'main';
	SubjectData.exp_nr = 1; 
	
	%for the first experiment, we have three sessions
	sessions = {'select', 'session1', 'session2', 'session3'};
	[sesNr,continueBool] = taskDialog(sessions,1,'Session','Select a Session');

	if ~continueBool
		errordlg('Program is aborted');                             %dialog window was closed
		error('Program is aborted');
	end
	
	if sesNr == 1 
		errordlg('No Session was Selected');                   %Default option 'Select' was not changed
		error('No Session was Selected');
		
	else
		SubjectData.ses_nr = sesNr-1;

	end
	
elseif  expNr == 3
	%for the second experiment, we have two sessions
	SubjectData.exp_type = 'main';
	SubjectData.exp_nr = 2; 
	
	sessions = {'select', 'session1', 'session2'};
	[sesNr,continueBool] = taskDialog(sessions,1,'Session','Select a Session');

	if ~continueBool
		errordlg('Program is aborted');                             %dialog window was closed
		error('Program is aborted');
	end
	
	if sesNr == 1 
		errordlg('No Session was Selected');                   %Default option 'Select' was not changed
		error('No Session was Selected');
		
	else
		SubjectData.ses_nr = sesNr-1;

	end
	
elseif  expNr == 5 % the training session 
    SubjectData.exp_type = 'train';
	
	train_parts = {'select', '1-keyQuest', '2-Sound', '3-Visual'};
	[trNr,continueBool] = taskDialog(train_parts,1,'training','Select a Training part');

	if ~continueBool
		errordlg('Program is aborted');                             %dialog window was closed
		error('Program is aborted');
	end
	
	if trNr == 1 
		errordlg('No Training was Selected');                   %Default option 'Select' was not changed
		error('No Training was Selected');
		
	else
		SubjectData.tr_nr = trNr-1;
	end
end


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Initialize Subject Settings %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Ask for SONA ID
answers = inputdlg({'Subject ID:'},'Input subject ID',1,{''});
if sum(size(answers) == [0,0]) == 2
    errordlg('ERROR: No answer was given');        %cancel was pressed or dialog window was closed
    error('ERROR: No answer was given');
elseif isempty(answers{1})
    errordlg('ERROR: No answer was given');        %OK was pressed but no input was given
    error('ERROR: No answer was given');
end

SubjectData.sub_id = answers{1};

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Set subject's path and create directories
F.SubjPath = [rootPath filesep 'Data' filesep 'Subj_' num2str(SubjectData.sub_id)];

% the subject folder should already be generated when creating the design matrix
if not(isfolder(F.SubjPath )) 
    %mkdir(F.SubjPath )
	errordlg('ERROR: Sub data folder not exist. Sub id might be wrong.');        %cancel was pressed or dialog window was closed
    error('ERROR: Sub data folder not exist. Sub id might be wrong.');
end

    
end %[EOF]


% Helper function: Dialog box with tasks in drop-down menu
function [choice,continueBool] = taskDialog(TaskOptions,default_nr,titleString,promptString)
    
    %Open the dialog box
    Pix_SS = get(0,'screensize');
    middle = [Pix_SS(3)/2 Pix_SS(4)/2];
    boxSize = [Pix_SS(3)/5 Pix_SS(4)/5];
    d = dialog('Position',[middle(1)-Pix_SS(3)/10 middle(2)-Pix_SS(4)/10 boxSize],'Name',titleString);
    
    %Text
    txt = uicontrol('Parent',d,...
           'Style','text',...
           'Position',[boxSize(1)/7 boxSize(2)*5/7 boxSize(1)*5/7 boxSize(2)/7],...
           'String',promptString);
    
    %Drop-down menu   
    popup = uicontrol('Parent',d,...
           'Style','popup',...
           'Position',[boxSize(1)/7 boxSize(2)*3/7 boxSize(1)*5/7 boxSize(2)/7],...
           'String',TaskOptions,...
           'Callback',@popup_callback);
    
    %Continue Button   
    btn = uicontrol('Parent',d,...
           'Position',[boxSize(1)/7 boxSize(2)*1/7 boxSize(1)*5/7 boxSize(2)/7],...
           'String','Continue',...
           'Callback',@btn_callback);
    
    %Set the default value   
    set(popup,'Value',default_nr);   
    choice = default_nr;
    continueBool = 0;
       
    %Wait for the dialog box to close before running to completion
    uiwait(d);
   
    %Callback function of the drop-down menu
    function popup_callback(popup,callbackdata)
       choice = get(popup,'Value');
    end

    %Callback function of the continue button
    function btn_callback(btn,callbackdata)
        continueBool = 1;
        delete(gcf);
    end
end