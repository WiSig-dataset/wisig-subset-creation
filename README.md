Examples scripts on creating new subsets of Full WiSig



Note that the MILP solver requires a GUROBI Licence
License can be obtained for free for academic users
https://www.gurobi.com/downloads/end-user-license-agreement-academic/

## Jupyter Notebooks:

001_create_tx_rx_list.ipynb: Shows an example of how to generate the Tx Rx list given a  required number of  Tx, a minimum number of signals, and a satisfiaction rate

002_FullWiSig_create_compact_datasets.ipynb: Files

## Python Files

tx_rx_list_creator_heuristic.py: Contains heuristic function

tx_rx_list_creator_milp.py: Contain MILP solver

data_utilities.py: Functions to create a new dataset. Also it can be used load the dataset and prepare it for classification


## PKL Files

data_summary.pkl: Contains number of signal per Tx-Rx for the entire datset


IdSig_info.pkl: Contains the google drive links of all files of Full WiSig