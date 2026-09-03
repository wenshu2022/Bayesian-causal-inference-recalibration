function R = AskQuestKey(P, D, R, iTrial, odd_flag)

qtxt = 'Common source?' ;
boundsText = Screen(P.win,'TextBounds',qtxt); %[L,T,R,B] from [L=0,T=0]
DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/3*2+boundsText(4)/2),  P.yellow);
offset = 20;

Screen('FrameOval', P.win, P.yellow, D.Button_Coords_conf');
DrawFormattedText(P.win, 'High', D.Button_Coords_conf(3,1)+offset , (D.Button_Coords_conf(3,2)+D.Button_Coords_conf(3,4))/2+boundsText(4)/2,  P.yellow);%left side yes	
DrawFormattedText(P.win, 'High', D.Button_Coords_conf(4,1)+offset, (D.Button_Coords_conf(4,2)+D.Button_Coords_conf(4,4))/2+boundsText(4)/2,  P.yellow);%left side yes	
DrawFormattedText(P.win, 'Med.', D.Button_Coords_conf(5,1)+offset, (D.Button_Coords_conf(5,2)+D.Button_Coords_conf(5,4))/2+boundsText(4)/2,  P.yellow);	%right side no
DrawFormattedText(P.win, 'Med.', D.Button_Coords_conf(2,1)+offset, (D.Button_Coords_conf(2,2)+D.Button_Coords_conf(2,4))/2+boundsText(4)/2,  P.yellow);	%right side no
DrawFormattedText(P.win, 'Low', D.Button_Coords_conf(1,1)+offset, (D.Button_Coords_conf(1,2)+D.Button_Coords_conf(1,4))/2+boundsText(4)/2,  P.yellow);	%right side no
DrawFormattedText(P.win, 'Low', D.Button_Coords_conf(6,1)+offset, (D.Button_Coords_conf(6,2)+D.Button_Coords_conf(6,4))/2+boundsText(4)/2,  P.yellow);	%right side no
if ~odd_flag
	%Three buttons on the left (YES), three on the right (NO)
	DrawFormattedText(P.win, 'Yes', D.Button_Coords_conf(1,1), 'center',  P.yellow);	%left side yes
	DrawFormattedText(P.win, 'No', D.Button_Coords_conf(6,1)+2*offset, 'center',  P.yellow);	%right side no
else
	%Three buttons on the left (NO), three on the right (YES)
	DrawFormattedText(P.win, 'No', D.Button_Coords_conf(1,1), 'center',  P.yellow);	%left side yes
	DrawFormattedText(P.win, 'Yes', D.Button_Coords_conf(6,1)+2*offset, 'center',  P.yellow);	%right side no
end
Screen('DrawingFinished', P.win);                                                                                                  % No further drawing commands before Screen('Flip')
Screen('Flip', P.win);


%Wait for mouse selection response
LocQuestionAnsweredBool = 0;

while ~LocQuestionAnsweredBool 

	[KBpressed, ~, keyCode] = KbCheck;

	if KBpressed && (keyCode(P.answerKey1) || keyCode(P.answerKey2) || keyCode(P.answerKey3) || keyCode(P.answerKey4) || keyCode(P.answerKey5)|| keyCode(P.answerKey6))
        
		if keyCode(P.answerKey1) & ~odd_flag %yes, low
			R.QuestResp{iTrial}(1) = 1;
			R.QuestResp{iTrial}(2) = 1;
            Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(1,:)');

		elseif keyCode(P.answerKey2) & ~odd_flag %yes, med
			R.QuestResp{iTrial}(1) = 1;
			R.QuestResp{iTrial}(2) = 2;
            Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(2,:)');    
            
		elseif keyCode(P.answerKey3) & ~odd_flag %yes, high
			R.QuestResp{iTrial}(1) = 1;
			R.QuestResp{iTrial}(2) = 3;
            Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(3,:)'); 

		elseif keyCode(P.answerKey4) & ~odd_flag %no, high
			R.QuestResp{iTrial}(1) = 0;
			R.QuestResp{iTrial}(2) = 3; 
            Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(4,:)');      
            
        elseif keyCode(P.answerKey5) & ~odd_flag %no, med
			R.QuestResp{iTrial}(1) = 0;
			R.QuestResp{iTrial}(2) = 2;
            Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(5,:)');  
            
        elseif keyCode(P.answerKey6) & ~odd_flag %no, low
			R.QuestResp{iTrial}(1) = 0;
			R.QuestResp{iTrial}(2) = 1;
            Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(6,:)');

		%odd number is oppsite
		elseif keyCode(P.answerKey1) & odd_flag %no, low
			R.QuestResp{iTrial}(1) = 0;
			R.QuestResp{iTrial}(2) = 1;
			Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(1,:)');
			
		elseif keyCode(P.answerKey2) & odd_flag %no, med
			R.QuestResp{iTrial}(1) = 0;
			R.QuestResp{iTrial}(2) = 2;
			Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(2,:)');
			
		elseif keyCode(P.answerKey3) & odd_flag %no, high
			R.QuestResp{iTrial}(1) = 0;
			R.QuestResp{iTrial}(2) = 3;
			Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(3,:)');
			
		elseif keyCode(P.answerKey4) & odd_flag %yes, high
			R.QuestResp{iTrial}(1) = 1;
			R.QuestResp{iTrial}(2) = 3;   
			Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(4,:)');
			
		elseif keyCode(P.answerKey5) & odd_flag %yes, med
			R.QuestResp{iTrial}(1) = 1;
			R.QuestResp{iTrial}(2) = 2;
			Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(5,:)');
			
		elseif keyCode(P.answerKey6) & odd_flag %yes, low
			R.QuestResp{iTrial}(1) = 1;
			R.QuestResp{iTrial}(2) = 1;
			Screen('FillOval', P.win, P.drawColor, D.Button_Coords_conf(6,:)');

        end
		
		DrawFormattedText(P.win, qtxt, 'center', round(P.winCenter_y/3*2+boundsText(4)/2),  P.yellow, 40);

		Screen('FrameOval', P.win, P.yellow, D.Button_Coords_conf');
		DrawFormattedText(P.win, 'High', D.Button_Coords_conf(3,1)+offset , (D.Button_Coords_conf(3,2)+D.Button_Coords_conf(3,4))/2+boundsText(4)/2,  P.yellow);%left side yes	
		DrawFormattedText(P.win, 'High', D.Button_Coords_conf(4,1)+offset, (D.Button_Coords_conf(4,2)+D.Button_Coords_conf(4,4))/2+boundsText(4)/2, P.yellow);%left side yes	
		DrawFormattedText(P.win, 'Med.', D.Button_Coords_conf(5,1)+offset, (D.Button_Coords_conf(5,2)+D.Button_Coords_conf(5,4))/2+boundsText(4)/2, P.yellow);	%right side no
		DrawFormattedText(P.win, 'Med.', D.Button_Coords_conf(2,1)+offset, (D.Button_Coords_conf(2,2)+D.Button_Coords_conf(2,4))/2+boundsText(4)/2, P.yellow);	%right side no
		DrawFormattedText(P.win, 'Low', D.Button_Coords_conf(1,1)+offset, (D.Button_Coords_conf(1,2)+D.Button_Coords_conf(1,4))/2+boundsText(4)/2, P.yellow);	%right side no
		DrawFormattedText(P.win, 'Low', D.Button_Coords_conf(6,1)+offset, (D.Button_Coords_conf(6,2)+D.Button_Coords_conf(6,4))/2+boundsText(4)/2, P.yellow);	%right side no
		
		if ~odd_flag
			%Three buttons on the left (YES), three on the right (NO)
			DrawFormattedText(P.win, 'Yes', D.Button_Coords_conf(1,1), 'center',  P.yellow);	%left side yes
			DrawFormattedText(P.win, 'No', D.Button_Coords_conf(6,1)+2*offset, 'center',  P.yellow);	%right side no
		else
			%Three buttons on the left (NO), three on the right (YES)
			DrawFormattedText(P.win, 'No', D.Button_Coords_conf(1,1), 'center',  P.yellow);	%left side yes
			DrawFormattedText(P.win, 'Yes', D.Button_Coords_conf(6,1)+2*offset, 'center',  P.yellow);	%right side no
		end
		Screen('DrawingFinished', P.win);                                                                                                  % No further drawing commands before Screen('Flip')
		Screen('Flip', P.win);
			
		LocQuestionAnsweredBool = 1;
        WaitSecs (0.05);	
	end

end


end