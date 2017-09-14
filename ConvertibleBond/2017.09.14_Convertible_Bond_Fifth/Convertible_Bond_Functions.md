

```python
import numpy as np
import pandas as pd
```


```python
def CB_data(CB):
    
    # 分别取最大值、最小值、最后收盘价、最初开盘价。
    CB_max = CB['close'].max()
    CB_max_data = CB.loc[CB['close'] == CB_max,'close']
    CB_min = CB['close'].min()
    CB_min_data = CB.loc[CB['close'] == CB_min,'close']
    CB_last_data = CB['close'].tail(1)
    CB_begin = CB['close'].head(1)
    CB_begin_data = CB['open'].head(1)
    
    # 设置一个最大值和最小值的日期与数值为0的一行记录；
    # 其目的是为了把相同时间的价格设置为0。
    CB_min_data_0 = CB.loc[CB['close'] == CB_min,'close']
    CB_min_data_0[0] = 0
    CB_max_data_0 = CB.loc[CB['close'] == CB_max,'close']
    CB_max_data_0[0] = 0
    
    # 如果最后收盘价就是最高价或者最低价，那么将最高价或最低价设置为0；
    # 因为最后收盘价是可以做得了卖出价的，而最高价或最低价是可遇不可求的。
    if CB_last_data[0] == CB_max:
        CB_max_data = CB_max_data_0
    if CB_last_data[0] == CB_min:
        CB_min_data = CB_min_data_0
    if CB_begin[0] == CB_min:
        CB_min_data = CB_min_data_0
    
    # ====================
    if CB_min < 107:
        CB_call_price = CB.loc[CB['close'] <= 107,'close'].head(1)
        if CB_begin_data[0] < 107:
            CB_call_price = CB_min_data_0
        elif CB_call_price[0] < 103:
            CB_call_price = CB_min_data_0
        elif CB_call_price[0] == CB_min:
            CB_min_data = CB_min_data_0
    else:
        CB_call_price = CB_min_data_0
    # 最小收盘价小于赎回价107元时，令买入价格为低于107的第一个收盘价
    # 如果这个收盘价还小于回售价103元，那么设置这个收盘价为0，其时间用最小收盘价时间
    # 就是使用了上述的“设置一个最大值和最小值的日期与数值为0”
    # 赎回价等于最小收盘价时，将最小收盘价设置为0，因为我们可能在达到赎回价线时进行建仓，
    # 但非常难用最低价建仓，所以这里将最低价设置为0，而保留赎回价，以下的回售价、面值价亦如此
    # 如果最小收盘价大于赎回价107元时，同样设置为0，其时间用最小收盘价时间
    # 以下同理
    # ====================
    if CB_min < 103:
        CB_sell_back = CB.loc[CB['close'] <= 103,'close'].head(1)
        if CB_begin_data[0] < 103:
            CB_sell_back = CB_min_data_0
        elif CB_sell_back[0] < 100:
            CB_sell_back = CB_min_data_0
        elif CB_sell_back[0] == CB_min:
            CB_min_data = CB_min_data_0
    else:
        CB_sell_back = CB_min_data_0
    # ====================
    if CB_min < 100:
        CB_par_value = CB.loc[CB['close'] <= 100,'close'].head(1)
        if CB_begin_data[0] < 100:
            CB_par_value = CB_min_data_0
        elif CB_par_value[0] == CB_begin[0]:
            CB_par_value = CB_min_data_0
        elif CB_par_value[0] == CB_min:
            CB_min_data = CB_min_data_0
    else:
        CB_par_value = CB_min_data_0
    # ====================
    if CB_min < 95:
        CB_95Sell = CB.loc[CB['close'] <= 95,'close'].head(1)
    else:
        CB_95Sell = CB_min_data_0
    # ====================
    if CB_min < 90:
        CB_90Sell = CB.loc[CB['close'] <= 90,'close'].head(1)
    else:
        CB_90Sell = CB_min_data_0
    # ====================
    if CB_min < 85:
        CB_85Sell = CB.loc[CB['close'] <= 85,'close'].head(1)
    else:
        CB_85Sell = CB_min_data_0
    # ====================
    if CB_min < 80:
        CB_80Sell = CB.loc[CB['close'] <= 80,'close'].head(1)
    else:
        CB_80Sell = CB_min_data_0
    # ====================
    # 以上为建仓买入价格的阶梯价
    
    # ====================
    if CB_max > 140:
        CB_140Sell = CB.loc[CB['close'] > 140,'close'].head(1)
        if CB_140Sell[0] == CB_max:
            CB_140Sell = CB_max_data_0
    else:
        CB_140Sell = CB_max_data_0
    # ====================
    CB['Stock_Transfer_Profit'] = (CB['TargetStock'] - CB['ShareTransfer'])/CB['ShareTransfer']*100
    Stock_Transfer_Profit = CB['Stock_Transfer_Profit'].max()
    # ====================
    if Stock_Transfer_Profit > 30:
        CB_30Sell = CB.loc[CB['Stock_Transfer_Profit'] > 30,'close'].head(1)
        if CB_30Sell[0] == CB_max:
            CB_30Sell = CB_max_data_0
    else:
        CB_30Sell = CB_max_data_0
    # ====================
    if Stock_Transfer_Profit > 50:
        CB_50Sell = CB.loc[CB['Stock_Transfer_Profit'] > 50,'close'].head(1)
        if CB_50Sell[0] == CB_max:
            CB_50Sell = CB_max_data_0
    else:
        CB_50Sell = CB_max_data_0
    # ====================
    # 以上为平仓卖出价格的阶梯价
    
    CB_data = pd.concat([CB_begin_data,CB_max_data, CB_min_data, CB_last_data,CB_call_price,CB_sell_back,CB_par_value,CB_95Sell,CB_90Sell,CB_85Sell,CB_80Sell,CB_140Sell,CB_30Sell,CB_50Sell], axis=1)
    CB_data.columns = ['close_begin','close_max','close_min','close_last','close_call_price','close_sell_back','close_par_value','close_95','close_90','close_85','close_80','close_140','close_30','close_50']
    # 将以上各表合成一个总表，并重命名各个字段。
    
    CB_data['BS_close'] = CB_data.apply(lambda x: x.sum(), axis=1)
    # 将每一行的所有列累加，得到一列合计数。
    
    CB_data.loc[CB_data['close_begin'] > 0,'Name'] = 'Begin Price [1]'
    CB_data.loc[CB_data['close_max'] > 0,'Name'] = 'Max Price'
    CB_data.loc[CB_data['close_min'] > 0,'Name'] = 'Min Price'
    CB_data.loc[CB_data['close_last'] > 0,'Name'] = 'Last Price'
    CB_data.loc[CB_data['close_call_price'] > 0,'Name'] = 'Call Price [2]'
    CB_data.loc[CB_data['close_sell_back'] > 0,'Name'] = 'SellBack Price [3]'
    CB_data.loc[CB_data['close_par_value'] > 0,'Name'] = 'Par Value [4]'
    CB_data.loc[CB_data['close_95'] > 0,'Name'] = '￥95 [5]'
    CB_data.loc[CB_data['close_90'] > 0,'Name'] = '￥90 [6]'
    CB_data.loc[CB_data['close_85'] > 0,'Name'] = '￥85 [7]'
    CB_data.loc[CB_data['close_80'] > 0,'Name'] = '￥80 [8]'
    CB_data.loc[CB_data['close_140'] > 0,'Name'] = '￥140 [A]'
    CB_data.loc[CB_data['close_30'] > 0,'Name'] = '30％ [B]'
    CB_data.loc[CB_data['close_50'] > 0,'Name'] = '50％ [C]'
    
    CB_data.index = pd.to_datetime(CB_data.index)
    CB_data = CB_data.sort_index(axis=0, ascending=True)
    CB_data = CB_data[['Name','BS_close']]
    
    return CB_data
```
