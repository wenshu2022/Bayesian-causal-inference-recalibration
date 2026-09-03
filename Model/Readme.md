## Prerequisite
- [Bayesian Adaptive Direct Search (BADS)](https://github.com/acerbilab/bads) - Download BADS and put under the 'Model' folder.
- MATLAB

## Folder structure
- m_config.xlsx - the list of tested models with the model configuration 
- model_config.m - function to read model configuration from m_config.xlsx
- fitting_config.m - function to define free parameters and parameters search ranges
- simAllConds.m - function to generate model simultion
- NLLsimAllConds.m - function to compute joint NLL based on behavior and simulation data
- Fitting/
  - fit_for_individual.m - function to run model fitting
  - output/ - the fitting results for each participant and each model
- check_performance/
  - gen_pred.m - to generate model prediction based on the best-fitted parameters for each participant and each model
  - factor_compare.m - perform factorial comparison
- Recovery/ 
  - confusion_mat.m - perform model recovery

## Usage
1. download data and change the workpath and datapath in the scripts according to your folder names.
2. Run Fitting/run_model.sh with a sub_id and m_id as input

## Reference
1. Acerbi, L. & Ma, W. J. (2017). Practical Bayesian Optimization for Model Fitting with Bayesian Adaptive Direct Search. In Advances in Neural Information Processing Systems 30, pages 1834-1844. (link, arXiv preprint)