#!/bin/bash

# Assign command line arguments to variables
sub_id=$1
m_id=$2
#nrun=$3

# Define MATLAB binary path
MATLAB_BIN="/opt/matlab/R2023b/bin/matlab"

# Define paths
m_path="/home/mpla/wenlou/MATLAB/Model"
toolbox="/home/mpla/wenlou/MATLAB/Model/bads-master"

# Set base and output directories
base_path="/home/mpla/wenlou/MATLAB/Model/Fitting"
output_dir="$base_path/output/"

# Check if the output directory exists, if not, create it
if [ ! -d "$output_dir" ]; then
    mkdir -p "$output_dir"
fi

# Define the output file path
data_out="${output_dir}m_${m_id}_sub_${sub_id}.mat"

# Construct MATLAB command
command="$MATLAB_BIN -singleCompThread -nodisplay -nosplash -nodesktop -r \"addpath('$base_path');addpath('$m_path'); addpath('$toolbox'); try; [sub_id, m_id, estimatedP, minNLL,ev] = fit_for_individual($sub_id, $m_id); save('$data_out', 'm_id', 'sub_id', 'minNLL', 'estimatedP','ev'); catch ME; fprintf(2, 'Error: %s\n', ME.message); exit(1); end; exit;\""

# Execute MATLAB command
eval "$command"
