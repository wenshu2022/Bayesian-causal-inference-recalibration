function D = SetDrawingParameters(P, Stimuli, resp)

% resp - 0 : mouse response; resp - 1 : keyboard response; resp - 2 : bitsi
% has rebundant field, but ok for now.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Prepare fixation cross %%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

D.fixx_LineWidth = 2;                                                           %in pixels (integers only) for the cursor line-width
fixx_diameter = 1;                                                              %in visual angle (in degrees)
fixxWidth_pix = round(tand(fixx_diameter/2)*P.dist2Screen_nPixWidth);           %half the size in pixels
fixxHeight_pix = round(tand(fixx_diameter/2)*P.dist2Screen_nPixHeight);
% Coords for DrawLines always in order: 1st row = x_coords, 2nd row = y_coords: 1st column pair is start_coord, 2nd column is stop_coord).     
D.fixx_Coords = [ [-fixxWidth_pix fixxWidth_pix; 0 0] [0 0; -fixxHeight_pix fixxHeight_pix] ];
% All coords are relative to some centre point (x,y). Use as:     
% Screen('DrawLines', P.win, D.fixx_Coords, D.fixx_LineWidth, P.grey, [P.centerX_cor,P.centerY_cor], 2);  %(the last '2' is for high quality smoothing)    

%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%----Common---%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
D.responseButton_LineWidth = 2;     %in pixels
responseButton_diameter_width = 3;        %in degrees visual angle      

responseButton_offset = 3;          %in degrees visual angle 
responseButton_Xoffset_pix = round(tand(responseButton_offset)*P.dist2Screen_nPixWidth);          %in pixels
responseButton_Yoffset_pix = round(tand(responseButton_offset)*P.dist2Screen_nPixHeight);         %in pixels

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%% Prepare a horizontal line%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
D.horLineWidth = 2;                    %in visual angle (in degrees)
horLine_pix = P.winCenter_x;
D.horlines_Coords = [ [ -horLine_pix horLine_pix ; 0 0]  [ 0  0 ; 0 0] ];


%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%----MOUSE----%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%

if resp == 0   
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%% Prepare Response button %%%%%%%%%
    %%% for the causal inference task %%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    responseButton_diameter_height = 6;        %in degrees visual angle  
    responseButton_height_pix = round(tand(responseButton_diameter_height)*P.dist2Screen_nPixHeight);        %in pixels
    responseButton_width_pix = round(tand(responseButton_diameter_width)*P.dist2Screen_nPixWidth);          %in pixels
    xLoc_L = P.winCenter_x-round(responseButton_width_pix/2);
    xLoc_R = P.winCenter_x+round(responseButton_width_pix/2);
    yLoc_T = P.winCenter_y-round(responseButton_height_pix/2);
    yLoc_B = P.winCenter_y+round(responseButton_height_pix/2);

    %D.MiddleResponseButton_Coords = [xLoc_L, yLoc_T, xLoc_R, yLoc_B];                                                                     %[L,T,R,B]
    D.LeftResponseButton_Coords   = [xLoc_L, yLoc_T, xLoc_R, yLoc_B] - [responseButton_Xoffset_pix 0 responseButton_Xoffset_pix 0];       %[L,T,R,B]
    D.RightResponseButton_Coords  = [xLoc_L, yLoc_T, xLoc_R, yLoc_B] + [responseButton_Xoffset_pix 0 responseButton_Xoffset_pix 0];       %[L,T,R,B]  
    %D.UpResponseButton_Coords     = [xLoc_L, yLoc_T, xLoc_R, yLoc_B] - [0 responseButton_Yoffset_pix 0 responseButton_Yoffset_pix];       %[L,T,R,B]
    %D.DownResponseButton_Coords   = [xLoc_L, yLoc_T, xLoc_R, yLoc_B] + [0 responseButton_Yoffset_pix 0 responseButton_Yoffset_pix];       %[L,T,R,B]
    % Use as:
    % Screen('FrameRect', P.win, P.grey, D.MiddleResponseButton_Coords, D.responseButton_LineWidth);
end


%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%-----key-----%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%

if resp ==1
    
    if 1
        % this is to generated 6 buttons on the screen for keyboard
        % response
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        %%% Prepare six reponse circle %%%
        %%% for confidence level %%%%%%%%%
        %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        Button_Radius = responseButton_diameter_width/2;                 %radius = diameter/2. Diameter in visual angles
        ButtonWidth_pix_conf = round(tand(Button_Radius)*P.dist2Screen_nPixWidth);               
        ButtonHeight_pix_conf = round(tand(Button_Radius)*P.dist2Screen_nPixHeight);   
        % Coords for FrameOval always in order [Left, Top, Right, Bottom]

        % generate a oval for each positions; the size is exactly as the textrect the locations is along the moving trajectories in pixels
        % button_loc_deg_h_conf = [-responseButton_offset*3, -responseButton_offset*2, -responseButton_offset, ...
        %     responseButton_offset, responseButton_offset*2, responseButton_offset*3]' * P.pxl_per_deg;
        % button_loc_deg_v_conf = [responseButton_offset, 0, -responseButton_offset, -responseButton_offset, 0, responseButton_offset]' * P.pxl_per_deg;
        button_loc_deg_h_conf = [-responseButton_Xoffset_pix*3, -responseButton_Xoffset_pix*2, -responseButton_Xoffset_pix, ...
            responseButton_Xoffset_pix, responseButton_Xoffset_pix*2, responseButton_Xoffset_pix*3]';
        button_loc_deg_v_conf = [responseButton_Yoffset_pix, 0, -responseButton_Yoffset_pix, -responseButton_Yoffset_pix, 0, responseButton_Yoffset_pix]';

        centerCoordinate_conf = {button_loc_deg_h_conf+P.winCenter_x, button_loc_deg_v_conf+P.winCenter_y};%in pixels, only horizontal
        D.Button_Coords_conf = cell2mat(cellfun(@CenterRectOnPoint, {[0 0 ButtonWidth_pix_conf*2  ButtonHeight_pix_conf*2]}, centerCoordinate_conf(1), centerCoordinate_conf(2), 'UniformOutput',false));
        % Use as: Screen('FrameOval', P.win, P.grey, D.Button_Coords, D.responseButton_LineWidth);

    else
        
        
        
    end
    
    
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%% Prepare six reponse circle %%%
    %%% for localization task  %%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %this part is discrarded, because we do not want to use visual aids for
    %auditory localizations
    if 0
        ButtonWidth_pix = round(tand(Stimuli.blob.width)*P.dist2Screen_nPixWidth); 

        % generate a oval for each positions; the size is exactly as the textrect the locations is along the moving trajectories in pixels
        button_loc_deg_h = Stimuli.aud_pool_train' * P.pxl_per_deg;
        centerCoordinate = {button_loc_deg_h+P.winCenter_x, zeros(length(button_loc_deg_h), 1)+P.winCenter_y};%in pixels, only horizontal
        D.Button_Coords = cell2mat(cellfun(@CenterRectOnPoint, {[0 0 ButtonWidth_pix  ButtonWidth_pix]}, centerCoordinate(1), centerCoordinate(2), 'UniformOutput',false));
    end
end


end %[EOF]

