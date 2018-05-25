
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time


# In[2]:

def CB_Transaction_Data(CB_name):
    
    # 选择数据中的某个转债数据
    CB_Transaction_Data = pd.read_csv('cbcsv/CB_Transaction_Data.csv', encoding='gbk')
    CB_TD = CB_Transaction_Data.loc[CB_Transaction_Data[u'证券名称'] == CB_name]
    CB_TD = CB_TD.reset_index(drop=True)
    
    # 计算转债的持仓成本
    CB_TD[u'成本'] = CB_TD[u'发生金额'].cumsum()
    CB_TD[u'成本'] = CB_TD[u'成本']/CB_TD[u'股份余额']*-1
    
    return CB_TD


# In[3]:

def CB_TD_cost(CB_name,CB_TD,Startdate):
    
    # 设置时间
    Now_Date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    Now_Date = pd.to_datetime(Now_Date)
    Now_Date = mdates.date2num(Now_Date)
    
    # 计算持仓金额、持仓数量
    CB_TD_cost_O = CB_TD[[u'发生金额',u'成交数量']]
    CB_TD_cost_P = CB_TD_cost_O.T
    CB_TD_cost_P[CB_name] = CB_TD_cost_P.apply(lambda x: x.sum(), axis=1)
    CB_TD_cost_Q = CB_TD_cost_P[[CB_name]]
    CB_TD_cost = CB_TD_cost_Q.T
    CB_TD_cost[u'持仓金额'] = 0 - CB_TD_cost[u'发生金额']
    CB_TD_cost = CB_TD_cost[[u'持仓金额',u'成交数量']]
    
    # 计算持仓成本
    if CB_TD_cost[u'成交数量'].values == 0:
        CB_TD_cost[u'持仓成本'] = 0
    else:
        CB_TD_cost[u'持仓成本'] =CB_TD_cost[u'持仓金额']/CB_TD_cost[u'成交数量']
        
    # 计算转债到期剩余时间
    CB_TD_cost[u'起息日'] = Startdate
    CB_TD_Date = pd.to_datetime(CB_TD_cost[u'起息日']).astype(np.object)
    CB_TD_Date = mdates.date2num(CB_TD_Date)
    CB_TD_Year = int(6-(Now_Date-CB_TD_Date)/365)
    CB_TD_Day = ((6-(Now_Date-CB_TD_Date)/365)-CB_TD_Year)*365
    CB_TD_cost[u'剩余年限'] = u'%d年%d天'%(CB_TD_Year,CB_TD_Day)
    
    return CB_TD_cost


# In[4]:

def CB_TD_plt(CB_TD,y1,y2,y3,y4):
    
    CB_TD_B = CB_TD.loc[CB_TD[u'成交数量'] > 0,[u'发生日期',u'成交均价',u'成交数量']]
    CB_TD_B = CB_TD_B.set_index(u'发生日期')
    CB_TD_B.index = pd.to_datetime(CB_TD_B.index)
    CB_TD_S = CB_TD.loc[CB_TD[u'成交数量'] < 0,[u'发生日期',u'成交均价',u'成交数量']]
    CB_TD_S = CB_TD_S.set_index(u'发生日期')
    CB_TD_S.index = pd.to_datetime(CB_TD_S.index)
    
    CB_TD_BS = CB_TD.loc[CB_TD[u'成交数量'] <> 0,[u'发生日期',u'成本']]
    CB_TD_BS = CB_TD_BS.drop_duplicates([u'发生日期'])
    CB_TD_BS = CB_TD_BS.set_index(u'发生日期')
    CB_TD_BS.index = pd.to_datetime(CB_TD_BS.index)
    Day1 = CB_TD_BS.index[0]
    Day1 = mdates.date2num(Day1)-2
    Day2 = CB_TD_BS.index[-1]
    Day2 = mdates.date2num(Day2)+2
    
    plt.figure(1,figsize=(16,4), dpi=80)
    ax1 = plt.subplot(111)
    
    CB_TD_B[u'成交均价'].plot(color='red', marker='.', alpha=0.5)
    CB_TD_S[u'成交均价'].plot(color='blue', marker='.', alpha=0.5)
    CB_TD_BS[u'成本'].plot(color='purple', marker='.', alpha=0.5)
    plt.grid(linestyle=':', alpha=0.5)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.xticks(CB_TD_BS.index, rotation=45)
    plt.xlim(Day1,Day2)
    plt.xlabel('Date') 
    
    plt.axhline(y=y1, color='Magenta', linewidth='1.0')
    plt.axhline(y=y2, color='Green', linewidth='1.0')
    plt.ylim(y3,y4,1)
    
    return plt.show()

