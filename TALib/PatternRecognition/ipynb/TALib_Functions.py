
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


# In[2]:

def import_stock_data(stock_code,stadate,enddate):
    stock_data = pd.read_csv('../datacsv/' + stock_code + '.csv')
    stock_data = stock_data[pd.to_datetime(stock_data['date']) >= pd.to_datetime(stadate)]
    stock_data = stock_data[pd.to_datetime(stock_data['date']) <= pd.to_datetime(enddate)]
    stock_data = stock_data.reset_index(drop=True)
    return stock_data


# In[3]:

def plot_signal(df):
    plt.figure(1,figsize=(16,4), dpi=80)
    ax1 = plt.subplot(111)
    df.plot(color='red', marker='.', alpha=0.4)
    return plt.show()

