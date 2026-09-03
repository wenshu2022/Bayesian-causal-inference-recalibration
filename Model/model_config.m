function [config, stiPar, par, param_names] = model_config(path, box_sel, M_Nr, defaul_par)
    % this function sparse two excel files
    % 1) m_config.xlsx 
    % 2) default_param.xlsx - not used
    % and generate two structs
    
    % read in 
    model_config_tbl = readtable(fullfile(path, "m_config.xlsx"));
    model_lst = model_config_tbl{:,1}';
    %model_lst
    
    %% choose a model
    if box_sel %% 1. choose by box selection - only for demonstration purpose 
        [M_Nr,continueBool] = taskDialog([{'select'}, model_lst],1,'Model List','Select a Model');
        M_Nr = M_Nr-1;
        
        if ~continueBool
            errordlg('Program is aborted');                             %dialog window was closed
            error('Program is aborted');
        end
        
        if M_Nr == 0
            errordlg('No Model was Selected');                   %Default option 'Select' was not changed
            error('No Model was Selected');
        else
            config.model_name                   = model_lst{M_Nr};
            config.shift_update                 = model_config_tbl{M_Nr, 2}{:};
            config.dec_noise_flag               = model_config_tbl{M_Nr, 3};
            config.lapse_flag                   = model_config_tbl{M_Nr, 4};
            config.conf_b_nr                    = model_config_tbl{M_Nr, 5};
            config.C_readout                    = model_config_tbl{M_Nr, 6}{:};
            config.AV_readout                   = model_config_tbl{M_Nr, 7}{:};
            config.past_influ                   = model_config_tbl{M_Nr, 8};
            config.same_var_2phase              = model_config_tbl{M_Nr, 9};      
            config.long_term_ef                 = model_config_tbl{M_Nr, 10}; 
            config.NLL_ty                       = model_config_tbl{M_Nr, 11}; 
            config.free_alp_V                   = model_config_tbl{M_Nr, 12}; 
            config.m_id                         = M_Nr;
            config.Conf_readout                 = model_config_tbl{M_Nr, 14}{:}; 
            config.step                         = model_config_tbl{M_Nr, 15}; 
            config.vs                           = model_config_tbl{M_Nr, 16}{:}; 
            config.ec                         = model_config_tbl{M_Nr, 17};
            
        end

    else % 2. text input - for fitting

        row_idx = find(ismember(model_config_tbl.m_id, M_Nr));
        if M_Nr==model_config_tbl{row_idx, 13}
            config.model_name                   = model_lst{row_idx};
            config.shift_update                 = model_config_tbl{row_idx, 2}{:};
            config.dec_noise_flag               = model_config_tbl{row_idx, 3};
            config.lapse_flag                   = model_config_tbl{row_idx, 4};
            config.conf_b_nr                    = model_config_tbl{row_idx, 5};
            config.C_readout                    = model_config_tbl{row_idx, 6}{:};
            config.AV_readout                   = model_config_tbl{row_idx, 7}{:};
            config.past_influ                   = model_config_tbl{row_idx, 8};
            config.same_var_2phase              = model_config_tbl{row_idx, 9};     
            config.long_term_ef                 = model_config_tbl{row_idx, 10}; 
            config.NLL_ty                       = model_config_tbl{row_idx, 11}; 
            config.free_alp_V                   = model_config_tbl{row_idx, 12}; 
            config.m_id                         = M_Nr;
            config.Conf_readout                 = model_config_tbl{row_idx, 14}{:}; 
            config.step                         = model_config_tbl{row_idx, 15}; 
            config.vs                           = model_config_tbl{row_idx, 16}; 
            %config.ec                         = model_config_tbl{row_idx, 17};
            %config.sato                         = model_config_tbl{row_idx, 18};
        else
            error('Error. \n input the model number when calling model_config function.')
        end
    end % end if box_sel

    if defaul_par
        param_tbl = readtable(fullfile(path, "default_param.xlsx"));
        param_names = param_tbl{:,1};
        par = param_tbl{:,M_Nr+1};
    else 
        par = [];
        param_names = {};
    end

    stiPar.resp_loc = [-12, -4, 4, 12];
    stiPar.resp_loc_len = length(stiPar.resp_loc);

end %EOF

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
end % end helper function