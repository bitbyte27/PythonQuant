
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd


# In[2]:

def YCWW(stock_data,DA):
    LLV_min = stock_data['close'].rolling(window=DA).min()
    HHV_max = stock_data['close'].rolling(window=DA).max()
    
    HHV_LLV = pd.concat([stock_data['close'], LLV_min, HHV_max], axis=1)
    HHV_LLV.columns = ['close','LLV','HHV']
    
    HHV_LLV['ABS'] = np.abs(HHV_LLV['HHV']/HHV_LLV['LLV']-1)
    HHV_LLV['MAX'] = HHV_LLV['ABS'].rolling(window=DA).max()
    
    HHV_LLV['DA'] = DA
    HHV_LLV.loc[HHV_LLV['MAX']>0.1,'DA'] = 3
    
    HHV_LLV['MM'] = HHV_LLV['close'].rolling(window=DA).mean()
    HHV_LLV.loc[HHV_LLV['DA'] == 3,'MM'] = HHV_LLV['close'].rolling(window=3).mean()
    HHV_LLV['M1'] = HHV_LLV['MM'].shift(1)
    
    return HHV_LLV

