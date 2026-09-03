clc;clear;
outputpath = 'M:\MATLAB\Model\Recovery\output';
wkdir = 'M:\MATLAB\Model\Recovery'; 
cd(wkdir)

m_lst = [70, 71, 73, 74, 87:94];
CM= zeros(12);
% first step - for one simulated model (data model), get all the fitted
% results
for i = 1:numel(m_lst)
    sim_mid = m_lst(i);
    fitFiles = dir(fullfile(outputpath, ['*_dat_m_' num2str(sim_mid) '_*'])); 
    fitFileNames = {fitFiles.name}';
    %init
    BIC = zeros(numel(fitFileNames), 4);
    BIC(:,1) = sim_mid;
    for iFile = 1:numel(fitFileNames)
        fit_res = load(fullfile(outputpath, fitFileNames{iFile}));
        BIC(iFile, 2) = fit_res.fit_m_id;
        BIC(iFile, 3) = min(fit_res.ev.BIC);
        BIC(iFile, 4) = fit_res.dat_id;
    end

    BIC_T = array2table(BIC, 'VariableNames', {'sim_mid', 'fit_mid', 'BIC', 'DID'});
    [G, DID_groups] = findgroups(BIC_T.DID);
    [minBIC, idx] = splitapply(@min, BIC_T.BIC, G);
    fit_mid_min = splitapply(@(x, y) y(x == min(x)), BIC_T.BIC, BIC_T.fit_mid, G);
    CM(i, :) = histcounts(fit_mid_min, [m_lst, max(m_lst)+1]);
end

confMat = round(CM / 20, 2);

m_labels = {'BayMS-Bay-Bay', 'BayMS-Bay-xDiff', 'BayMS-xDiff-Bay', 'BayMS-xDiff-xDiff', 'xDiff-Bay-Bay','xDiff-xDiff-Bay', ...
            'xDiff-Bay-xDiff', 'xDiff-xDiff-xDiff', 'BayMA-Bay-Bay', 'BayMA-Bay-xDiff', 'BayMA-xDiff-Bay','BayMA-xDiff-xDiff'};


% Plot Confusion Matrix as Colored Rectangles
figure;
imagesc(confMat); % Display the matrix with color mapping
colormap(gray); % Choose a colormap (e.g., 'parula', 'hot', 'jet', 'gray')
colorbar; % Show color scale
caxis([0 max(confMat(:))]); % Normalize color range based on max value

% Add labels
xlabel('Fit Model', 'FontSize', 16);
ylabel('Simulated Model', 'FontSize', 16);
t = title('Confusion matrix: p(fit model | simulated model)', 'FontSize', 24, 'FontWeight', 'bold');
t.Position(2) = t.Position(2) - 0.5; % Moves title higher
% Customize Axes
numClasses = size(confMat, 1);
xticks(1:numClasses);
yticks(1:numClasses);
xticklabels(m_labels);
yticklabels(m_labels);
xtickangle(45); % Rotate x-axis labels for better readability
ytickangle(0);  % Keep y-axis labels horizontal
set(gca, 'FontSize', 14, 'FontWeight', 'bold');
axis square;

for i = 1:numClasses
    for j = 1:numClasses
        value = confMat(i, j); % Get matrix value
        
        % Determine text color based on position
        if j == i  % Upper triangular (including diagonal)
            textColor = 'black'; 
        else  % Lower triangular
            textColor = 'white'; 
        end

        text(j, i, num2str(value), 'HorizontalAlignment', 'center', ...
             'FontSize', 12, 'Color', textColor, 'FontWeight', 'bold');
    end
end

saveas(gcf, 'ConfusionMatrix.png');