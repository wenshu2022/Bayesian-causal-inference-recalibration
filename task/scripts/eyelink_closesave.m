function eyelink_closesave(sv,saveFile,edfName)

%% from Claire Pleche 
   
    
    % Receive file from host computer and move to the experimental data folder
    if sv==1
        Eyelink('CloseFile');
        try
            status = Eyelink('ReceiveFile');
            if status > 0
                fprintf('ReceiveFile status %d\n',status);
            end
        catch
            warning('Problem receiving eye data file');
        end
        
        if exist(edfName,'file')
            
            movefile(edfName,[saveFile,'.edf']); % rename and move file to destination
            fprintf('Data file moved to subject folder.\n');
        else 
            error('Can not find eye data file.\')
        end
    end
    
    Eyelink('Shutdown');


end
%     % Converting edf file to asc
%     if exist(S.eyelink.edfFileName,'file')
%         try
%             fprintf('Converting file %s\n',[name,ext]);
%             [status,~] = system(sprintf('edf2asc %s',S.eyelink.edfFileName));
%             
% %             if status
% %                 warning('Can not convert file %s ',[name,ext]);
% %             end
%         catch
%             warning('Can not convert file %s ',[name,ext]);
%         end
%     end
%     
    % Shut down the eyetracker