function set_path
[pathstr,~,~] = fileparts(mfilename('fullpath'));
cd(fullfile(pathstr,'.'))
rootPath = pwd;

%rootdir = 'C:\Users\wenlou\Documents\MATLAB';
%outdir = fullfile(rootdir, 'output');
%taskdir = fullfile(rootdir, 'task');
%sofadir = fullfile(rootdir, 'SOFA');

%Add the relevant paths
addpath(genpath([rootPath filesep 'scripts']));                             %add the Scripts-folder and all subfolders to the matlab path

%% load in the pregenerated move sound files and trajectorys




end

