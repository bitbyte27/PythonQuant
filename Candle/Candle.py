
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_finance as mplf
import matplotlib.dates as mdates
import Risk_Ratio_Functions


# In[2]:

def Candle_plot(Stock_data, stadate, enddate):
    # 输入Stock_data，并处理索引、日期格式、按索引日期排序
    Stock_data = Stock_data.set_index('date')
    Stock_data.index = pd.to_datetime(Stock_data.index)
    Stock_data = Stock_data.sort_index(axis=0, ascending=True)
    
    # 风险决策指标
    Risk_Ratio = Risk_Ratio_Functions.Risk_Ratio(Stock_data)
    Risk_Ratio = Risk_Ratio[['Decision','MAJCQX']]
    Stock_data_Risk_Ratio = pd.concat([Stock_data,Risk_Ratio], axis=1)
    
    # 设置目标时间区间
    Stock_data_Risk_Ratio = Stock_data_Risk_Ratio[Stock_data_Risk_Ratio.index >= pd.to_datetime(stadate)]
    Stock_data_Risk_Ratio = Stock_data_Risk_Ratio[Stock_data_Risk_Ratio.index <= pd.to_datetime(enddate)]
    k = len(Stock_data_Risk_Ratio)
    
    # 设置id，作为坐标系的x轴数据，最后用date来标注
    Stock_data_Risk_Ratio['date'] = Stock_data_Risk_Ratio.index
    Stock_data_Risk_Ratio = Stock_data_Risk_Ratio.reset_index(drop=True)
    Stock_data_Risk_Ratio['id'] = Stock_data_Risk_Ratio.index+1
    
    # ochl数据设置，date数据设置
    Stock_data_Risk_Ratio_ochl = Stock_data_Risk_Ratio[['id','open','close','high','low']]
    Stock_data_Risk_Ratio_date = Stock_data_Risk_Ratio.set_index('date')
    
    # 设置画出K线图的数据datarray，画出风险决策曲线的数据（Id，De），（ID，JCQX）
    # 设置替代x轴的日期数据（idx，date）
    datarray = Stock_data_Risk_Ratio_ochl.values
    De = Stock_data_Risk_Ratio['Decision'].values
    JCQX = Stock_data_Risk_Ratio['MAJCQX'].values
    Id = Stock_data_Risk_Ratio['id'].values
    idx = np.arange(0, k, 1)
    date = Stock_data_Risk_Ratio_date.index[idx].date
    
    # 画图
    plt.figure(2,figsize=(14,6), dpi=80)
    ax1 = plt.subplot(111)
    
    # 设置candlestick_ochl
    mplf.candlestick_ochl(ax1, datarray, width=0.8, colorup='red', colordown='green', alpha=0.7)
    plt.grid(linestyle=':', alpha=0.5)
    
    # 设置x轴
    plt.xticks(Id-0.5, date)
    plt.xticks(rotation=45)
    
    # 设置风险决策曲线
    ax2 = ax1.twinx()
    plt.plot(Id, De, color ='Orange', linewidth=2.0, alpha=1)
    plt.plot(Id, JCQX, color ='Brown', linewidth=2.0, alpha=1)
    plt.xlim(0,k+1,1)
    plt.ylim(0,100,10)
    
    return plt.show()

