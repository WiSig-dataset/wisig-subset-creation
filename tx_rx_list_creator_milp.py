import pickle
import numpy as np
import gurobipy as gp
from gurobipy import GRB
from tqdm.notebook import trange, tqdm


def solve_for_lists_milp(num_tx = None, min_sig = None, min_sig_low = None, satisfaction=1.0, verbose=False):
    with open('data_summary.pkl', 'rb') as f:
        d=pickle.load(f)
    capture_date_list=d['capture_date_list']
    tx_list= d['tx_list']
    rx_list= d['rx_list']
    mat_date=np.array(d['mat_date'])
    mat_date_eq=np.array(d['mat_date_eq'])

    n_tx = len(tx_list)
    n_rx = len(rx_list)
    num_days = 4;
    
    if(num_tx is None):
        raise ValueError("num_tx must be specified. Exiting...")
        return
    
    if(min_sig is None):
        raise ValueError("min_sig must be specified. Exiting...")
        return
    
    if(min_sig_low is None): min_sig_low = 0;
    
    M=3000 # Upper-bound to num_signals for any rx-tx pair
    mat_date_thresh = np.double(mat_date > min_sig);
    mat_date_eq_thresh = np.double(mat_date_eq > min_sig);
    
    m = gp.Model("mip_dual_tol")
    
    if(verbose): m.params.outputflag = 1
    else: m.params.outputflag = 0

    T = m.addMVar(shape=n_tx, vtype=GRB.BINARY, name="T")
    R = m.addMVar(shape=(n_rx, 1), vtype=GRB.BINARY, name="R")
    Y = m.addMVar(shape=(n_rx, n_tx), vtype=GRB.BINARY, name="Y")
    min_sig_var = m.addMVar(shape = 1, vtype=GRB.INTEGER, name="min_sig_var")
    Z = m.addMVar(shape=(n_rx, n_tx), vtype=GRB.INTEGER, name="Z")

    Q = m.addMVar(shape=(num_days, n_rx, n_tx), vtype=GRB.BINARY, name="Q")
    Q_eq = m.addMVar(shape=(num_days, n_rx, n_tx), vtype=GRB.BINARY, name="Q_eq")

    for rxid in range(n_rx):
        for txid in range(n_tx):
            
            # Y[rxid][txid] = R[rxid] AND T[txid]
            m.addConstr(Y[rxid][txid] <= T[txid])
            m.addConstr(Y[rxid][txid] <= R[rxid, 0])
            m.addConstr(Y[rxid][txid] >= T[txid] + R[rxid, 0] - 1)

            # Z[rxid][txid] = 0 if Y[rxid][txid] == False. Z[rxid][txid] = min_sig if Y[rxid][txid] == True.
            m.addConstr(Z[rxid][txid] <= Y[rxid][txid] * M)
            m.addConstr(Z[rxid][txid] >= 0)
            m.addConstr(Z[rxid][txid] <= min_sig_var[0])
            m.addConstr(Z[rxid][txid] >= min_sig_var[0] - (1-Y[rxid][txid]) * M)

            for day_id in range(num_days):

                # Q[rxid][txid] = Y[rxid][txid] AND (mat_date[rxid][txid] > min_sig)
                m.addConstr(Q[day_id][rxid][txid] <= Y[rxid][txid])
                m.addConstr(Q[day_id][rxid][txid] <= mat_date_thresh[day_id][rxid][txid])
                m.addConstr(Q[day_id][rxid][txid] >= Y[rxid][txid] + mat_date_thresh[day_id][rxid][txid] - 1)

                # Q_eq[rxid][txid] = Y[rxid][txid] AND (mat_date_eq[rxid][txid] > min_sig)
                m.addConstr(Q_eq[day_id][rxid][txid] <= Y[rxid][txid])
                m.addConstr(Q_eq[day_id][rxid][txid] <= mat_date_eq_thresh[day_id][rxid][txid])
                m.addConstr(Q_eq[day_id][rxid][txid] >= Y[rxid][txid] + mat_date_eq_thresh[day_id][rxid][txid] - 1)

                # mat_date[day_id][rxid][txid] >= min_sig, if R[rxid] == True AND T[txid] == True
                m.addConstr(mat_date[day_id][rxid][txid] * Y[rxid][txid] - Z[rxid][txid] >= 0)
                # mat_date_eq[day_id][rxid][txid] >= min_sig, if R[rxid] == True AND T[txid] == True
                m.addConstr(mat_date_eq[day_id][rxid][txid] * Y[rxid][txid] - Z[rxid][txid] >= 0)
 
    m.addConstr(T.sum() == num_tx) # This can be made m.addConstr(T.sum() >= num_tx) at the expense of larger solve times, but larger dataset
    m.addConstr(min_sig_var >= min_sig_low) 

    for i in range(n_rx):
        for day_id in range(num_days):
            m.addConstr(Q[day_id, i, :].sum() >= R[i] * num_tx * satisfaction)
            m.addConstr(Q_eq[day_id, i, :].sum() >= R[i] * num_tx * satisfaction)

    # dual-objective optimization. maximixing n_rx has higher priority over maximizing min_sig
    m.setObjectiveN(R.sum(), 0, 10)
    m.setObjectiveN(min_sig_var - min_sig_low, 1, 0)
    m.ModelSense = GRB.MAXIMIZE

    m.optimize()
    
    if m.status == GRB.OPTIMAL:
        min_sig_value = min_sig_var.X;
        R_V, T_V = np.array(R.X, dtype=bool).squeeze(), np.array(T.X, dtype=bool)
#         min_satisfaction = min(np.min((mat_date[:,:,T_V][:,R_V,:]>satisfaction).sum(axis=2) / np.sum(T_V)),
#                                np.min((mat_date_eq[:,:,T_V][:,R_V,:]>satisfaction).sum(axis=2) / np.sum(T_V)));
        print(f"Found optimal solution with {np.sum(R_V)} Rx")
    else:
        print("Could not find optimal solution.")
      
    T_V = np.array(T.X, dtype=bool)
    R_V = np.array(R.X, dtype=bool).squeeze()
    op_tx_list = apply_list(tx_list,T_V)
    op_rx_list = apply_list(rx_list,R_V)
    
    return op_tx_list,op_rx_list



def apply_list(lst, bool_list):
    return [lst[ii] for ii in range(bool_list.size) if bool_list[ii]]


