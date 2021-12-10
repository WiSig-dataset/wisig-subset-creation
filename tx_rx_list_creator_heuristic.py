import pickle
import numpy as np





def solve_for_lists_heurstic(num_tx = None, min_sig = None, min_sig_low = None, satisfaction=1.0, verbose=False):
    with open('data_summary.pkl', 'rb') as f:
        d=pickle.load(f)
    capture_date_list=d['capture_date_list']
    tx_list= d['tx_list']
    rx_list= d['rx_list']
    mat_date=np.array(d['mat_date'])
    mat_date_eq=np.array(d['mat_date_eq'])

    mat = np.minimum(np.min(mat_date,0),np.min(mat_date_eq,0))

    n_tx = len(tx_list)
    n_rx = len(rx_list)
    num_days = 4;
    
    if(num_tx is None):
        raise ValueError("num_tx must be specified. Exiting...")
        return
    
    if(min_sig is None):
        raise ValueError("min_sig must be specified. Exiting...")
        return
    
    if( not (min_sig_low is None)): 
        raise ValueError("min_sig_low is not supported. Exiting...")
        return

    min_sig = min_sig
    n_req_tx= num_tx
    rx_ratio = satisfaction

    cur_mat = mat>=min_sig

    tx_sel = np.zeros(n_tx,dtype=np.bool)
    rx_sel = np.zeros(n_rx,dtype=np.bool)

    cnt = np.sum(cur_mat,0)

    
    srt= np.argsort(-cnt)

    if cnt[srt[0]]>0:
        

        cur_mat = np.copy(cur_mat)
        tx_sel[srt[:n_req_tx]] = True

        cur_mat = cur_mat[:,tx_sel] 
        rx_sel = np.sum(cur_mat,1)>=rx_ratio*n_req_tx
        cur_mat = cur_mat[rx_sel,:]

    op_tx_list = apply_list(tx_list,tx_sel)
    op_rx_list = apply_list(rx_list,rx_sel)

    return op_tx_list,op_rx_list



def apply_list(lst, bool_list):
    return [lst[ii] for ii in range(bool_list.size) if bool_list[ii]]


def apply_list(lst, bool_list):
    return [lst[ii] for ii in range(bool_list.size) if bool_list[ii]]