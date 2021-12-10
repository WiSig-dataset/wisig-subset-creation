#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('load_ext', 'autoreload')

get_ipython().run_line_magic('autoreload', '2')
import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
import scipy.optimize


# In[2]:


import os
GPU = ""
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"   
os.environ["CUDA_VISIBLE_DEVICES"]=GPU


# In[3]:


src='../orbit_rf_dataset/data/'
dst='../orbit_rf_dataset/data/compact_datasets/'


# In[4]:


from data_utilities import create_dataset_impl


# In[5]:


full_dataset_path = '../../orbit_rf_dataset/data/'
dst='../../orbit_rf_dataset/data/compact_pkl_datasets/'


# In[6]:


tx_list = ['14-10', '14-7', '20-15', '20-19', '6-15', '8-20']
rx_list = ['1-1', '1-19', '14-7', '18-2', '19-2', '2-1', '2-19', '20-1', '3-19', '7-14', '7-7', '8-8']
capture_date_list = ['2021_03_01','2021_03_08','2021_03_15','2021_03_23']
dataset_name = 'ManySig'
max_n = 1000
print(len(tx_list),len(rx_list))

dataset = create_dataset_impl(tx_list,rx_list,capture_date_list,max_sig=max_n,equalized_list=[0,1],full_dataset_path=full_dataset_path,op_dataset_file=dst+dataset_name+'.pkl')


# In[7]:


tx_list = ['1-1', '1-10', '1-11', '1-12', '1-14', '1-15', '1-16', '1-18', '1-19', '1-2', '1-8', '10-1', '10-10', '10-11', '10-17', '10-4', '10-7', '11-1', '11-10', '11-17', '11-19', '11-20', '11-4', '11-7', '12-1', '12-19', '12-20', '12-7', '13-14', '13-18', '13-19', '13-20', '13-3', '13-7', '14-10', '14-11', '14-12', '14-13', '14-14', '14-20', '14-7', '14-8', '14-9', '15-1', '15-19', '15-6', '16-1', '16-16', '16-19', '16-20', '16-5', '17-10', '17-11', '18-1', '18-10', '18-11', '18-12', '18-13', '18-14', '18-15', '18-16', '18-17', '18-2', '18-20', '18-4', '18-5', '18-7', '18-8', '18-9', '19-1', '19-10', '19-11', '19-12', '19-13', '19-14', '19-19', '19-2', '19-20', '19-3', '19-4', '19-6', '19-7', '19-8', '19-9', '2-1', '2-12', '2-13', '2-14', '2-15', '2-16', '2-17', '2-19', '2-20', '2-3', '2-4', '2-5', '2-6', '2-7', '2-8', '20-1', '20-12', '20-14', '20-15', '20-16', '20-18', '20-19', '20-20', '20-3', '20-4', '20-5', '20-7', '20-8', '3-1', '3-13', '3-18', '3-19', '3-2', '3-20', '3-8', '4-1', '4-10', '4-11', '5-1', '5-16', '5-20', '5-5', '6-1', '6-15', '6-6', '7-10', '7-11', '7-12', '7-13', '7-14', '7-20', '7-7', '7-8', '7-9', '8-1', '8-13', '8-14', '8-18', '8-20', '8-3', '8-7', '8-8', '9-1', '9-14', '9-20', '9-7']
rx_list = ['1-1', '1-19', '1-20', '13-7', '14-7', '18-19', '18-2', '19-1', '19-2', '2-1', '20-1', '20-19', '3-19', '7-14', '7-7', '8-14', '8-7', '8-8']
capture_date_list = ['2021_03_01','2021_03_08','2021_03_15','2021_03_23']
dataset_name = 'ManyTx'
max_n = 50

print(len(tx_list),len(rx_list))
dataset = create_dataset_impl(tx_list,rx_list,capture_date_list,max_sig=max_n,equalized_list=[0,1],full_dataset_path=full_dataset_path,op_dataset_file=dst+dataset_name+'.pkl')


# In[8]:


tx_list = ['1-10', '11-1', '14-10', '14-7', '17-11', '20-15', '20-19', '7-11', '7-14', '8-20']
rx_list = ['1-1', '1-19', '1-20', '13-14', '13-7', '14-7', '18-19', '18-2', '19-1', '19-19', '19-2', '19-20', '2-1', '2-19', '20-1', '20-19', '20-20', '23-1', '23-3', '23-5', '23-6', '23-7', '24-13', '24-16', '24-5', '24-6', '3-19', '7-14', '7-7', '8-14', '8-7', '8-8']
capture_date_list = ['2021_03_01','2021_03_08','2021_03_15','2021_03_23']
dataset_name = 'ManyRx'
max_n = 200

print(len(tx_list),len(rx_list))
dataset = create_dataset_impl(tx_list,rx_list,capture_date_list,max_sig=max_n,equalized_list=[0,1],full_dataset_path=full_dataset_path,op_dataset_file=dst+dataset_name+'.pkl')


# In[9]:


tx_list = ['1-11', '10-11', '10-7', '11-1', '11-17', '11-4', '11-7', '13-3', '14-10', '14-7', '15-1', '16-16', '2-19', '20-12', '20-15', '20-19', '20-7', '3-13', '3-18', '4-11', '5-5', '6-1', '6-15', '7-10', '7-11', '8-18', '8-20', '8-3']
rx_list = ['1-1', '13-13', '14-7', '2-1', '2-20', '20-1', '7-14', '7-7', '8-13', '8-8']
capture_date_list = ['2021_03_23']
dataset_name = 'SingleDay'
max_n = 800

print(len(tx_list),len(rx_list))

dataset = create_dataset_impl(tx_list,rx_list,capture_date_list,max_sig=max_n,equalized_list=[0,1],full_dataset_path=full_dataset_path,op_dataset_file=dst+dataset_name+'.pkl')


# In[7]:


with open('datasets_info.pkl','rb') as f:
    t=pickle.load(f)
t


# In[ ]:




