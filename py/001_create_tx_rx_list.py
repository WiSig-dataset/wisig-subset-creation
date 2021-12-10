#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tqdm.notebook import trange, tqdm
import matplotlib.pyplot as plt
import numpy as np
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import timeit


# In[2]:


min_sig = 50
num_tx = 125
min_sig_low = 0

satisfaction = 0.9


# In[3]:


from tx_rx_list_creator_heuristic import solve_for_lists_heurstic

start = timeit.default_timer()

op_tx_list, op_rx_list = solve_for_lists_heurstic(num_tx=num_tx, min_sig=min_sig, min_sig_low = None, satisfaction=satisfaction)

stop = timeit.default_timer()
print('Time: ', stop - start)  
    
print(len(op_rx_list))
print(op_tx_list)
print(op_rx_list)


# In[4]:


from tx_rx_list_creator_milp import solve_for_lists_milp


# Requires a GUROBI Licence
# License can be obtained for free for academic users
# https://www.gurobi.com/downloads/end-user-license-agreement-academic/
start = timeit.default_timer()

op_tx_list, op_rx_list = solve_for_lists_milp(num_tx=num_tx, min_sig=min_sig, min_sig_low = min_sig_low, satisfaction=satisfaction)

stop = timeit.default_timer()
print('Time: ', stop - start) 
    
print(len(op_rx_list))
print(op_tx_list)
print(op_rx_list)


# In[ ]:




