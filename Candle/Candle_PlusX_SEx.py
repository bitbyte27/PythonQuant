
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import mpl_finance as mplf
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
import Risk_Ratio_Functions


# In[2]:

def Candle_plot(Stock_data, stadate, enddate, trade_dates, trade_prices, buy_dates, buy_prices, sell_dates, sell_prices):
    
    # 输入Stock_data，并处理索引、日期格式、按索引日期排序
    Stock_data = Stock_data.set_index('date')
    Stock_data.index = pd.to_datetime(Stock_data.index)
    Stock_data = Stock_data.sort_index(axis=0, ascending=True)
    
    # 风险决策指标
    Risk_Ratio = Risk_Ratio_Functions.Risk_Ratio(Stock_data)
    Risk_Ratio = Risk_Ratio[['Decision','MAJCQX']]
    
    # 运筹帷幄指标，指标构建
    DA = 6
    ZFXF_YCWW = pd.DataFrame()
    ZFXF_YCWW['LLV_min'] = Stock_data['close'].rolling(window=DA).min()
    ZFXF_YCWW['HHV_max'] = Stock_data['close'].rolling(window=DA).max()
    ZFXF_YCWW['ABS'] = np.abs(ZFXF_YCWW['HHV_max']/ZFXF_YCWW['LLV_min']-1)
    ZFXF_YCWW['MAX'] = ZFXF_YCWW['ABS'].rolling(window=DA).max()
    ZFXF_YCWW['DA'] = DA
    ZFXF_YCWW.loc[ZFXF_YCWW['MAX']>0.1,'DA'] = 3
    ZFXF_YCWW['Tomorrow'] = Stock_data['close'].rolling(window=DA).mean()
    ZFXF_YCWW.loc[ZFXF_YCWW['DA'] == 3,'Tomorrow'] = Stock_data['close'].rolling(window=3).mean()
    ZFXF_YCWW['YCWW'] = ZFXF_YCWW['Tomorrow'].shift(1)
    
    # 运筹帷幄指标，买卖信号点构建
    ZFXF_YCWW['Buy_point'] = 0
    ZFXF_YCWW.loc[Stock_data['close'] > ZFXF_YCWW['YCWW'],'Buy_point'] = 1
    ZFXF_YCWW['Sell_point'] = 0
    ZFXF_YCWW.loc[Stock_data['close'] < ZFXF_YCWW['YCWW'],'Sell_point'] = -1
    ZFXF_YCWW['Points'] = ZFXF_YCWW['Buy_point']+ZFXF_YCWW['Sell_point']
    
    # 运筹帷幄指标，形成【成住坏空（2，1，-2，-1）】信号点
    g = len(ZFXF_YCWW)
    ZFXF_YCWW['order'] = np.arange(0,g,1)
    ZFXF_YCWW.loc[g-1:g,'Points'] = -1
    ZFXF_YCWW['BS_point'] = ZFXF_YCWW['Points'].shift(1)
    ZFXF_YCWW['BS_point'] = ZFXF_YCWW['BS_point'].fillna(-1)
    ZFXF_YCWW['BS_point'] = (ZFXF_YCWW['Points'] - ZFXF_YCWW['BS_point'])/2+ZFXF_YCWW['Points']
    
    # 合并两大指标
    Stock_Risk_Ratio_ZFXF_YCWW = pd.concat([Stock_data,Risk_Ratio,ZFXF_YCWW[['YCWW','Tomorrow','BS_point']]], axis=1)
    
    # 设置目标时间区间
    Stock_Risk_Ratio_ZFXF_YCWW = Stock_Risk_Ratio_ZFXF_YCWW[Stock_Risk_Ratio_ZFXF_YCWW.index >= pd.to_datetime(stadate)]
    Stock_Risk_Ratio_ZFXF_YCWW = Stock_Risk_Ratio_ZFXF_YCWW[Stock_Risk_Ratio_ZFXF_YCWW.index <= pd.to_datetime(enddate)]
    k = len(Stock_Risk_Ratio_ZFXF_YCWW)
    
    # 设置id，作为坐标系的x轴数据，最后用date来标注
    Stock_Risk_Ratio_ZFXF_YCWW['date'] = Stock_Risk_Ratio_ZFXF_YCWW.index
    Stock_Risk_Ratio_ZFXF_YCWW = Stock_Risk_Ratio_ZFXF_YCWW.reset_index(drop=True)
    Stock_Risk_Ratio_ZFXF_YCWW['id'] = Stock_Risk_Ratio_ZFXF_YCWW.index+1
    
    # ochl数据设置，date数据设置
    Stock_Risk_Ratio_ZFXF_YCWW_ochl = Stock_Risk_Ratio_ZFXF_YCWW[['id','open','close','high','low']]
    Stock_Risk_Ratio_ZFXF_YCWW_date = Stock_Risk_Ratio_ZFXF_YCWW.set_index('date')
    
    # 设置交易点的时间和价格
    Trades = pd.DataFrame()
    Trades['price'] = trade_prices
    Trades['date'] = 0
    Trades['id'] = 0
    
    for t in range(0,len(trade_dates)):
        T_date = Stock_Risk_Ratio_ZFXF_YCWW.loc[Stock_Risk_Ratio_ZFXF_YCWW['date'] == pd.to_datetime(trade_dates[t]),'date'].values
        T_id = Stock_Risk_Ratio_ZFXF_YCWW.loc[Stock_Risk_Ratio_ZFXF_YCWW['date'] == pd.to_datetime(trade_dates[t]),'id'].values
        Trades.loc[t:t+1,'date'] = T_date
        Trades.loc[t:t+1,'id'] = T_id
    
    Trades = Trades.set_index('id')
    tp = trade_prices
    idt = Trades.index.values
    
    # 设置买卖连线的时间和价格
    Buys = pd.DataFrame()
    Buys['price'] = buy_prices
    Buys['date'] = 0
    Buys['id'] = 0
    
    Sells = pd.DataFrame()
    Sells['price'] = sell_prices
    Sells['date'] = 0
    Sells['id'] = 0
    
    for p in range(0,len(buy_dates)):
        Buys_date = Stock_Risk_Ratio_ZFXF_YCWW.loc[Stock_Risk_Ratio_ZFXF_YCWW['date'] == pd.to_datetime(buy_dates[p]),'date'].values
        Buys_id = Stock_Risk_Ratio_ZFXF_YCWW.loc[Stock_Risk_Ratio_ZFXF_YCWW['date'] == pd.to_datetime(buy_dates[p]),'id'].values
        Buys.loc[p:p+1,'date'] = Buys_date
        Buys.loc[p:p+1,'id'] = Buys_id
    
    Buys = Buys.set_index('id')
    by = buy_prices
    idby = Buys.index.values
    
    for q in range(0,len(sell_dates)):
        Sells_date = Stock_Risk_Ratio_ZFXF_YCWW.loc[Stock_Risk_Ratio_ZFXF_YCWW['date'] == pd.to_datetime(sell_dates[q]),'date'].values
        Sells_id = Stock_Risk_Ratio_ZFXF_YCWW.loc[Stock_Risk_Ratio_ZFXF_YCWW['date'] == pd.to_datetime(sell_dates[q]),'id'].values
        Sells.loc[q:q+1,'date'] = Sells_date
        Sells.loc[q:q+1,'id'] = Sells_id
    
    Sells = Sells.set_index('id')
    sl = sell_prices
    idsl = Sells.index.values
    
    # 交易收益率
    prf = pd.DataFrame()
    prf['sl'] = sell_prices
    prf['by'] = buy_prices
    # 每次交易收益率
    prf['prf'] = (prf['sl']-prf['by'])/prf['by']
    # 格式化卖出日期为可计算的date2num值
    prf['sd'] = sell_dates
    prf['sd'] = pd.to_datetime(prf['sd']).astype(np.object)
    prf['sd'] = mdates.date2num(prf['sd'])
    # 格式化买入日期为可计算的date2num值
    prf['bd'] = buy_dates
    prf['bd'] = pd.to_datetime(prf['bd']).astype(np.object)
    prf['bd'] = mdates.date2num(prf['bd'])
    # 持仓时间
    prf['ri'] = prf['sd'] - prf['bd']
    # 每次年化收益
    prf['Yprf'] = prf['prf']/prf['ri']*365
    # 格式化百分比
    prf['prf'] = prf['prf'].apply(lambda x: format(x, '.2%'))
    prf['Yprf'] = prf['Yprf'].apply(lambda x: format(x, '.2%'))
    prfs = prf['prf'].values
    Yprfs = prf['Yprf'].values
    
    # 设置画出K线图的数据datarray
    # 画出风险决策曲线的数据（Id，De），（ID，JCQX）
    # 设置替代x轴的日期数据（idx，date）
    datarray = Stock_Risk_Ratio_ZFXF_YCWW_ochl.values
    De = Stock_Risk_Ratio_ZFXF_YCWW['Decision'].values
    JCQX = Stock_Risk_Ratio_ZFXF_YCWW['MAJCQX'].values
    Id = Stock_Risk_Ratio_ZFXF_YCWW['id'].values
    idx = np.arange(0, k, 2)
    date = Stock_Risk_Ratio_ZFXF_YCWW_date.index[idx].date
    
    # 画出运筹帷幄买卖信号点的数据（idb，buy），（ids，sell）
    buy_point = Stock_Risk_Ratio_ZFXF_YCWW.loc[Stock_Risk_Ratio_ZFXF_YCWW['BS_point']==2.0,['YCWW','BS_point']]
    sell_point = Stock_Risk_Ratio_ZFXF_YCWW.loc[Stock_Risk_Ratio_ZFXF_YCWW['BS_point']==-2.0,['YCWW','BS_point']]
    buy = buy_point['YCWW'].values.round(3)
    idb = buy_point.index+1
    sell = sell_point['YCWW'].values.round(3)
    ids = sell_point.index+1
    
    # 判断起始画线点应当为买点，如果为卖点，则删除sell_point的第一个点，使得buy_point的第一个点为画线点
    if buy_point.index[0] > sell_point.index[0]:
        sell_point = sell_point.iloc[1:,:]
    
    sell2 = sell_point['YCWW'].values.round(3)
    ids2 = sell_point.index+1
    
    # 运筹帷幄指标预测值
    idp = Stock_Risk_Ratio_ZFXF_YCWW.index[-1]
    # Today's YCWW
    ptd = Stock_Risk_Ratio_ZFXF_YCWW['YCWW'].tail(1).values.round(4)
    ptd = float(ptd[0])
    # Tomorrow's YCWW
    ptmr = Stock_Risk_Ratio_ZFXF_YCWW['Tomorrow'].tail(1).values.round(4)
    ptmr = float(ptmr[0])
        
    # 画图
    plt.figure(2,figsize=(14,6), dpi=300)
    ax1 = plt.subplot(111)
    
    # 先画风险决策曲线，在最底层；并画网格
    plt.plot(Id, De, color ='Orange', linewidth=2.0, alpha=0.8)
    plt.plot(Id, JCQX, color ='Brown', linewidth=2.0, alpha=0.8)
    plt.axhline(y=20, color='cyan', linewidth=1.0, alpha=1.0)
    plt.axhline(y=60, color='yellow', linewidth=1.0, alpha=1.0)
    plt.axhline(y=70, color='gold', linewidth=1.0, alpha=1.0)
    plt.axvline(x=Id[0], color='LightPink', linestyle='--', linewidth=1.0, alpha=1.0)
    plt.axvline(x=Id[-1], color='MediumOrchid', linestyle='--', linewidth=1.0, alpha=1.0)
    plt.axvline(x=Id[-1]+1, color='RosyBrown', linestyle='--', linewidth=1.0, alpha=1.0)
    plt.grid(linestyle=':', alpha=0.5)
    
    # 设置x轴，风险决策曲线的y轴
    plt.xticks(idx, date)
    plt.xticks(rotation=45)
    plt.ylim(10,80,10)
    
    # 设置candlestick_ochl
    ax2 = ax1.twinx()
    mplf.candlestick_ochl(ax2, datarray, width=0.8, colorup='red', colordown='green', alpha=0.6)
    
    # 设置买卖信号点
    plt.scatter(idb, buy, color ='blue', s=50, alpha=1.0, zorder=2)
    plt.scatter(ids, sell, color ='brown', s=50, alpha=1.0, zorder=3)
    
    # 设置交易价格点
    plt.scatter(idt, tp, color ='black', s=80, alpha=1.0, zorder=4)
    plt.scatter(idt, tp, color ='yellow', s=30, alpha=1.0, zorder=5)
    
    # 设置预测点
    plt.scatter(idp+1, ptd, color ='black', s=80, alpha=1.0, zorder=6)
    plt.scatter(idp+1, ptd, color ='cyan', s=30, alpha=1.0, zorder=7)
    plt.scatter(idp+2, ptmr, color ='black', s=80, alpha=1.0, zorder=6)
    plt.scatter(idp+2, ptmr, color ='Lime', s=30, alpha=1.0, zorder=7)
    
    # 标注卖点的价格和标签样式
    for a,b in zip(ids,sell):
        ax2.text(a, b*1.01, b, ha='center', va= 'center', bbox = dict(facecolor = "blue", alpha = 0.2))
    
    # 标注买点的价格和标签样式
    for c,d in zip(idb,buy):
        ax2.text(c, d*0.995, d, ha='center', va= 'center', bbox = dict(facecolor = "magenta", alpha = 0.2))
        
    # 标注交易点的价格和标签样式
    for e,f in zip(idt,tp):
        ax2.text(e, f*1.01, f, ha='center', va= 'center', bbox = dict(facecolor = "yellow", alpha = 0.5))
    
    # 标注预测值的价格和标签样式
    ax2.text(idp+1, ptd*1.004, ptd, ha='center', va= 'center', bbox = dict(facecolor = "cyan", alpha = 0.2))
    ax2.text(idp+2, ptmr*1.004, ptmr, ha='center', va= 'center', bbox = dict(facecolor = "Lime", alpha = 0.2))
    
    # 预测买卖点的连线
    for m,n,p,q in zip(idb,ids2,buy,sell2):
        ax2.add_line(Line2D((m,n), (p,q), linewidth=3, color='magenta', zorder=1))
        
    # 成交买卖点的连线
    for u,v,h,g in zip(idby,idsl,by,sl):
        ax2.add_line(Line2D((u,v), (h,g), linewidth=3, color='blue', zorder=1))
        
    # 交易收益率，年化收益率
    for r,s,t in zip(idsl,sl,prfs):
        ax2.text(r, s*1.024, t, ha='center', va= 'center', bbox = dict(facecolor = "magenta", alpha = 0.5))
    for x,y,z in zip(idsl,sl,Yprfs):
        ax2.text(x, y*1.037, z, ha='center', va= 'center', bbox = dict(facecolor = "cyan", alpha = 0.5))
    
    return plt.show()

