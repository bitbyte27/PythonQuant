

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```


```python
def Strategy_Point_MA(FirstDF,buy_compare1,buy_compare2,sell_compare1,sell_compare2):
    
    # MA类策略中，即“buy_compare1”>“buy_compare2”；并将这些收盘价设置为买点（1）。
    Buy_Point = FirstDF.loc[buy_compare1 > buy_compare2, FirstDF.columns]
    Buy_Point.loc[0:,'buy_point'] = 1
    
    # MA类策略中，即“sell_compare1”>“sell_compare2”；并将这些收盘价设置为卖点（-1）。
    Sell_Point = FirstDF.loc[sell_compare1 < sell_compare2, FirstDF.columns]
    Sell_Point.loc[0:,'sell_point'] = -1
    
    # 将买表、卖表合并；形成一个买卖（1，-1）的信号点Point，但这并不够表示实际交易，缺少买点、卖点、持仓、空仓的区分。
    Strategy_data = pd.concat([Buy_Point['buy_point'], Sell_Point['sell_point']], axis=1)
    Strategy_data = Strategy_data.fillna(0)
    Strategy_data['Points'] = Strategy_data.apply(lambda x: x.sum(), axis=1)
    Strategy_point_data = pd.concat([FirstDF, Strategy_data['Points']], axis=1)
    
    # 设置一个排序序列，用于对照、显示调用。
    k = len(Strategy_point_data)
    Strategy_point_data['order'] = np.arange(0,k,1)
    
    # 将最后一个交易日的买卖信号点设置为卖点（-1），因此规定最后一个交易日为卖出，才能形成买卖闭环。
    Strategy_point_data.loc[k-1:k,'Points'] = -1
    
    # 通过错位.shift(1)函数，形成一个买卖持空（2，-2，1，-1）的信号点BS_point，有买点、卖点、持仓、空仓。
    Strategy_point_data['BS_point'] = Strategy_point_data['Points'].shift(1)
    # 将首个错位信号设置为（-1），可以使得第一个交易日要么是空仓、要么是买点，而不会出现持仓或卖点的情况。
    Strategy_point_data['BS_point'] = Strategy_point_data['BS_point'].fillna(-1)
    Strategy_point_data['BS_point'] = (Strategy_point_data['Points'] - Strategy_point_data['BS_point'])/2+Strategy_point_data['Points']
    
    return Strategy_point_data
```


```python
def Strategy_Point_risk(FirstDF,buy_compare1,buy_compare2,sell_compare1,sell_compare2):
    
    # risk类策略中，即“buy_compare1”>“buy_compare2”；并将这些收盘价设置为买点（1）。
    Buy_Point = FirstDF.loc[buy_compare1 > buy_compare2, FirstDF.columns]
    Buy_Point.loc[0:,'buy_point'] = 1
    
    # risk类策略中，即“sell_compare1”>“sell_compare2”；并将这些收盘价设置为卖点（-1）。
    Sell_Point = FirstDF.loc[sell_compare1 < sell_compare2, FirstDF.columns]
    Sell_Point.loc[0:,'sell_point'] = -1
    
    # 将买表、卖表合并；形成一个买卖、持空仓（1，-1, 0）的信号点Point，但这并不够表示实际交易，缺少买点、卖点、持仓、空仓的区分。
    Strategy_data = pd.concat([Buy_Point['buy_point'], Sell_Point['sell_point']], axis=1)
    Strategy_data = Strategy_data.fillna(0)
    Strategy_data['Points'] = Strategy_data.apply(lambda x: x.sum(), axis=1)
    
    # 设置一个BS_point的买卖点，用于实现买点、卖点、持仓、空仓的区分。
    Strategy_data['BS_point'] = Strategy_data.loc[:,'Points']
    
    # 设置一个排序序列，用于对照、显示调用。
    p = len(Strategy_data)
    Strategy_data['order'] = np.arange(0,p,1)
    
    # 设置第一个信号为（-1或2），可以使得第一个交易日要么是空仓、要么是买点，而不会出现持仓或卖点的情况。
    if Strategy_data['Points'][0] == -1 or Strategy_data['Points'][0] == 0:
        Strategy_data.loc[0:1,'BS_point'] = -1
    else:
        Strategy_data.loc[0:1,'BS_point'] = 2
    
    # 实现一个买卖持空（2，-2，1，-1）的信号点BS_point，有买点、卖点、持仓、空仓。
    for i in range(1,p):
        if Strategy_data['Points'][i] == 0 and (Strategy_data['BS_point'][i-1] == -2 or Strategy_data['BS_point'][i-1] == -1):
            Strategy_data.loc[i:i+1,'BS_point'] = -1
        elif Strategy_data['Points'][i] == 1 and (Strategy_data['BS_point'][i-1] == -2 or Strategy_data['BS_point'][i-1] == -1):
            Strategy_data.loc[i:i+1,'BS_point'] = 2
        elif Strategy_data['Points'][i] == -1 and (Strategy_data['BS_point'][i-1] == 2 or Strategy_data['BS_point'][i-1] == 1):
            Strategy_data.loc[i:i+1,'BS_point'] = -2
        elif Strategy_data['Points'][i] == 0 and (Strategy_data['BS_point'][i-1] == 2 or Strategy_data['BS_point'][i-1] == 1):
            Strategy_data.loc[i:i+1,'BS_point'] = 1
    
    # 所最后一个交易日是买入或持仓信号，则将最后一个交易日的买卖信号点设置为卖点（-2），因此规定最后一个交易日为卖出，才能形成买卖闭环。
    if Strategy_data['BS_point'][-1] == 1 or Strategy_data['BS_point'][-1] == 2:
        Strategy_data.loc[p-1:p,'BS_point'] = -2
    
    # 合并一个交易信息信号表。
    Strategy_point_data = pd.concat([FirstDF, Strategy_data[['Points','order','BS_point']]], axis=1)
    
    return Strategy_point_data
```


```python
def Strategy_Profit(SPD,Buy,Sell,cash,brokerage):
    
    # 再将买点和卖点单独成表。
    BP_price = SPD.loc[SPD['BS_point'] == 2, SPD.columns]
    SP_price = SPD.loc[SPD['BS_point'] == -2, SPD.columns]
    
    # 买点表设置一个startdate，为开仓时间，开仓信号点（BS_point = 2）。
    BP_price['startdate'] = BP_price.index
    BP_Profit = BP_price[['startdate',Buy]]
    BP_Profit.columns = ['Start_date','Buy_price']
    BP_Profit = BP_Profit.reset_index(drop=True)
        
    # 卖点表设置一个enddate，为平仓时间，开仓信号点（BS_point = -2）。
    SP_price['enddate'] = SP_price.index
    SP_Profit = SP_price[['enddate',Sell]]
    SP_Profit.columns = ['End_date','Sell_price']
    SP_Profit = SP_Profit.reset_index(drop=True)
    
    # 将两个表合并，形成一个有开仓时间、平仓时间、开仓价格、平仓价格的交易表。
    Strategy_Profit = pd.concat([BP_Profit, SP_Profit], axis=1, join_axes=[BP_Profit.index])
    Strategy_Profit = Strategy_Profit[['Start_date','End_date','Buy_price','Sell_price']]

    # 设置资金cash，第一行Startcash列为初始资金cash；
    # batch：1手=100股；
    # 佣金比例brokerage：万分之2.5。
    p = len(Strategy_Profit)
    Strategy_Profit.loc[0:0,'Startcash'] = cash
    Startcash = Strategy_Profit['Startcash'][0]
    batch = 100
    
    # 建仓股数Shares =（资金/100股）整除建仓价*100股。
    Strategy_Profit.loc[0:0,'Shares'] = (Startcash/batch)//Strategy_Profit['Buy_price']*batch
    
    # 建仓总价Price = 建仓价格 * 建仓股数Shares。
    Strategy_Profit.loc[0:0,'Price'] = Strategy_Profit['Buy_price']*Strategy_Profit['Shares']
    
    # 佣金bb，最低5元，建仓时的佣金Buy_Brokerage（Price）。
    bb = Strategy_Profit['Price'][0]*brokerage/10000
    if bb > 5:
        Strategy_Profit.loc[0:0,'Buy_Brokerage'] = bb
    else:
        Strategy_Profit.loc[0:0,'Buy_Brokerage'] = 5
    
    # 剩余未交易资金Surplus = 初始资金（剩余总资金）- 建仓总价 - 佣金。
    Strategy_Profit.loc[0:0,'Surplus'] = Strategy_Profit['Startcash'] - Strategy_Profit['Price'] - Strategy_Profit['Buy_Brokerage']
    
    # 平仓总价AlphaCat = 平仓价格 * 建仓股数Shares。
    Strategy_Profit.loc[0:0,'AlphaCat'] = Strategy_Profit['Sell_price']*Strategy_Profit['Shares']
    
    # 佣金sb，最低5元，平仓时的佣金Sell_Brokerage（AlphaCat）。
    sb = Strategy_Profit['AlphaCat'][0]*brokerage/10000
    if sb > 5:
        Strategy_Profit.loc[0:0,'Sell_Brokerage'] = sb
    else:
        Strategy_Profit.loc[0:0,'Sell_Brokerage'] = 5
    
    # 印花税Tax = 平仓总价AlphaCat的千分之一。
    Strategy_Profit.loc[0:0,'Tax'] = Strategy_Profit['AlphaCat']*1.0/1000
    
    # 剩余总资金Endcash = 平仓总价 + 未交易资金 - 平仓佣金 - 印花税。
    Strategy_Profit.loc[0:0,'Endcash'] = Strategy_Profit['AlphaCat'] + Strategy_Profit['Surplus'] - Strategy_Profit['Sell_Brokerage'] - Strategy_Profit['Tax']
    
    # 第二次建仓的资金Startcash为第一次的平仓剩余总资金Endcash。
    Strategy_Profit.loc[1:1,'Startcash'] = Strategy_Profit['Endcash'][0]
    
    # 以上是设置了收益表的第一行，下面将用For循环，设置剩余整表。
    
    for i in range(1,p):
        Strategy_Profit.loc[i:i,'Shares'] = (Strategy_Profit['Startcash']/batch)//Strategy_Profit['Buy_price']*batch
        Strategy_Profit.loc[i:i,'Price'] = Strategy_Profit['Buy_price']*Strategy_Profit['Shares']
        bbr = Strategy_Profit['Price']*brokerage/10000
        if bbr[i-1] > 5:
            Strategy_Profit.loc[i:i,'Buy_Brokerage'] = bbr[i-1]
        else:
            Strategy_Profit.loc[i:i,'Buy_Brokerage'] = 5
        Strategy_Profit.loc[i:i,'Surplus'] = Strategy_Profit['Startcash'] - Strategy_Profit['Price'] - Strategy_Profit['Buy_Brokerage']
        Strategy_Profit.loc[i:i,'AlphaCat'] = Strategy_Profit['Sell_price']*Strategy_Profit['Shares']
        sbr = Strategy_Profit['AlphaCat']*brokerage/10000
        if sbr[i-1] > 5:
            Strategy_Profit.loc[i:i,'Sell_Brokerage'] = sbr[i-1]
        else:
            Strategy_Profit.loc[i:i,'Sell_Brokerage'] = 5
        Strategy_Profit.loc[i:i,'Tax'] = Strategy_Profit['AlphaCat']*1.0/1000
        Strategy_Profit.loc[i:i,'Endcash'] = Strategy_Profit['AlphaCat'] + Strategy_Profit['Surplus'] - Strategy_Profit['Sell_Brokerage'] - Strategy_Profit['Tax']
        Strategy_Profit.loc[i+1:i+1,'Startcash'] = Strategy_Profit['Endcash'][i]
    
    # 相对原始资金的收益率Profit_real
    Strategy_Profit['Profit_real'] = Strategy_Profit['Endcash']/cash
    
    return  Strategy_Profit    
```


```python
def Strategy_Profit_plt(SPf,plt_W,plt_H,plt_C):
    
    # 将第一天建仓时的收益率设置为（1）。
    ONE = SPf.loc[0:0,['Start_date','Profit_real']]
    ONE = ONE.set_index('Start_date')
    ONE.loc[0:1,'Profit_real'] = 1
    
    # 其他接下来的收益率设为平仓时间的收益率。
    Next = SPf[['End_date','Profit_real']]
    Next = Next.set_index('End_date')
    
    # 合并第一天和其他接下来的平仓收益率。
    SPP = pd.concat([ONE, Next], axis=1)
    SPP = SPP.fillna(0)
    SPP['Profit'] = SPP.apply(lambda x: x.sum(), axis=1)
    
    # 画图。
    plt.figure(2,figsize=(plt_W,plt_H), dpi=80)
    ax1 = plt.subplot(111)
    SPP['Profit'].plot(color=plt_C, alpha=1)
    
    return plt.show()
```
