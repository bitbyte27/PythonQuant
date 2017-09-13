
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd


# In[2]:

def Risk_Ratio(stock_data):
    # 01
    # MA1赋值:收盘价的5日简单移动平均
    # MA2赋值:收盘价的10日简单移动平均
    MA1 = stock_data['close'].rolling(window=5).mean()
    MA2 = stock_data['close'].rolling(window=10).mean()
    MA12 = pd.concat([stock_data['close'], MA1, MA2], axis=1)
    MA12.columns = ['close','MA1','MA2']
    # P01赋值:如果MA1>MA2,返回1,否则返回如果MA2>MA1,返回-1,否则返回0
    MA12['P01'] = 0
    MA12.loc[MA12['MA1'] > MA12['MA2'],'P01'] = 1
    MA12.loc[MA12['MA1'] < MA12['MA2'],'P01'] = -1

    # 02
    # MA3赋值:收盘价的3日简单移动平均
    # MA4赋值:收盘价的5日简单移动平均
    MA3 = stock_data['close'].rolling(window=3).mean()
    MA4 = stock_data['close'].rolling(window=5).mean()
    MA1234 = pd.concat([MA12, MA3, MA4], axis=1)
    MA1234.columns = ['close','MA1','MA2','P01','MA3','MA4']
    # P02赋值:如果MA3>MA4,返回1,否则返回如果MA4>MA3,返回-1,否则返回0
    MA1234['P02'] = 0
    MA1234.loc[MA1234['MA3'] > MA1234['MA4'],'P02'] = 1
    MA1234.loc[MA1234['MA3'] < MA1234['MA4'],'P02'] = -1

    # 03
    # MA5赋值:收盘价的12日简单移动平均
    # MA6赋值:收盘价的50日简单移动平均
    MA5 = stock_data['close'].rolling(window=12).mean()
    MA6 = stock_data['close'].rolling(window=50).mean()
    MA123456 = pd.concat([MA1234, MA5, MA6], axis=1)
    MA123456.columns = ['close','MA1','MA2','P01','MA3','MA4','P02','MA5','MA6']
    # P03赋值:如果MA5>MA6,返回1,否则返回如果MA6>MA5,返回-1,否则返回0
    MA123456['P03'] = 0
    MA123456.loc[MA123456['MA5'] > MA123456['MA6'],'P03'] = 1
    MA123456.loc[MA123456['MA5'] < MA123456['MA6'],'P03'] = -1

    # 04
    # 5日内最低价的最低值
    # 5日内最高价的最高值
    LOW5 = stock_data['low'].rolling(window=5).min()
    HIGH5 = stock_data['high'].rolling(window=5).max()
    MAPO_RSV = pd.concat([MA123456, HIGH5, LOW5], axis=1)
    MAPO_RSV.columns = ['close','MA1','MA2','P01','MA3','MA4','P02','MA5','MA6','P03','HIGH5','LOW5']
    # RSV赋值:(收盘价-5日内最低价的最低值)/(5日内最高价的最高值-5日内最低价的最低值)*100
    MAPO_RSV['RSV'] = (MAPO_RSV['close']-MAPO_RSV['LOW5'])/(MAPO_RSV['HIGH5']-MAPO_RSV['LOW5'])*100
    # K赋值:RSemaV的3日指数移动平均
    # D赋值:K的3日指数移动平均
    K = MAPO_RSV['RSV'].ewm(span=3).mean()
    D = K.ewm(span=3).mean()
    MAPO_RSV_KD = pd.concat([MAPO_RSV, K, D], axis=1)
    MAPO_RSV_KD.columns = ['close','MA1','MA2','P01','MA3','MA4','P02','MA5','MA6','P03','HIGH5','LOW5','RSV','RSV_K','RSV_D']
    # P04赋值:如果K>D,返回1,否则返回如果D>K,返回-1,否则返回0
    MAPO_RSV_KD['P04'] =0
    MAPO_RSV_KD.loc[MAPO_RSV_KD['RSV_K'] > MAPO_RSV_KD['RSV_D'],'P04'] = 1
    MAPO_RSV_KD.loc[MAPO_RSV_KD['RSV_K'] < MAPO_RSV_KD['RSV_D'],'P04'] = -1

    # 05
    # 收盘价的12日指数移动平均
    # 收盘价的26日指数移动平均
    EMA12 = stock_data['close'].ewm(span=12).mean()
    EMA26 = stock_data['close'].ewm(span=26).mean()

    EMA1226 = pd.concat([EMA12, EMA26], axis=1)
    EMA1226.columns = ['EMA12','EMA26']
    # DIF赋值:收盘价的12日指数移动平均-收盘价的26日指数移动平均
    EMA1226['DIF'] = EMA1226['EMA12']-EMA1226['EMA26']
    # DEA赋值:DIF的9日指数移动平均
    DEA = EMA1226['DIF'].ewm(span=9).mean()
    EMA_DEA = pd.concat([EMA1226, DEA], axis=1)
    EMA_DEA.columns = ['EMA12','EMA26','DIF','DEA']
    # MACD赋值:(DIF-DEA)*2
    EMA_DEA['MACD'] = (EMA_DEA['DIF']-EMA_DEA['DEA'])*2
    # P05赋值:如果DIF>DEA,返回1,否则返回如果DEA>DIF,返回-1,否则返回0
    EMA_DEA['P05'] = 'NaN'
    EMA_DEA.loc[EMA_DEA['DIF'] > EMA_DEA['DEA'],'P05'] = 1
    EMA_DEA.loc[EMA_DEA['DIF'] < EMA_DEA['DEA'],'P05'] = -1
    EMA_DEA.loc[EMA_DEA['DIF'] == EMA_DEA['DEA'],'P05'] = 0
    
    # 06
    # 波幅（true range，TR）与真实波幅（average true range，ATR）的计算
    TR = stock_data[['close']].shift(1)
    TR.columns = ['Yesterday_Close']
    TR = pd.concat([stock_data[['high','low','close']], TR], axis=1)
    # TR=∣最高价-最低价∣和∣最高价-昨收∣和∣昨收-最低价∣的最大值
    TR['TR1'] = np.abs(TR['high']-TR['low'])
    TR['TR2'] = np.abs(TR['high']-TR['Yesterday_Close'])
    TR['TR3'] = np.abs(TR['Yesterday_Close']-TR['low'])
    # 求三者（'TR1','TR2','TR3'）或多者中的最大值、最小值的更好的方法
    TR_max = TR.loc[:,['TR1','TR2','TR3']]
    TR_max['TRmax'] = TR_max.apply(lambda x: x.max(), axis=1)
    # TRIX赋值:(真实波幅-1日前的真实波幅)/1日前的真实波幅*100
    TR['Yesterday_TR'] = TR_max['TRmax'].shift(1)
    TR['TRIX'] = (TR_max['TRmax'] - TR['Yesterday_TR'])/TR['Yesterday_TR']*100
    TR.loc[0:2,'TRIX'] = 0
    # MATRIX赋值:TRIX的9日简单移动平均 
    MATRIX = TR['TRIX'].rolling(window=9).mean()
    TRIX = pd.concat([TR_max['TRmax'], TR['TRIX'], MATRIX], axis=1)
    TRIX.columns = ['TR','TRIX','MATRIX']
    # P06赋值:如果TRIX>MATRIX,返回1,否则返回如果MATRIX>TRIX,返回-1,否则返回0
    TRIX['P06'] = 0
    TRIX.loc[TRIX['TRIX'] > TRIX['MATRIX'],'P06'] = 1
    TRIX.loc[TRIX['TRIX'] < TRIX['MATRIX'],'P06'] = -1

    # 07
    # HD赋值:最高价-1日前的最高价
    # LD赋值:1日前的最低价-最低价
    HDLD = stock_data[['high','low']].shift(1)
    HDLD.columns = ['Yesterday_high','Yesterday_low']
    HDLD = pd.concat([stock_data[['high','low','close']], HDLD], axis=1)
    HDLD['HD'] = HDLD['high'] - HDLD['Yesterday_high']
    HDLD['LD'] = HDLD['Yesterday_low'] - HDLD['low']
    # DMP赋值:如果HD>0 AND HD>LD,返回HD,否则返回0，的7日指数移动平均
    HDLD['DMP'] = 0
    HDLD.loc[HDLD['HD'] > HDLD['LD'], 'DMP'] = HDLD['HD']
    HDLD.loc[HDLD['HD'] <= 0, 'DMP'] = 0
    HDLD['DMP7'] = HDLD['DMP'].ewm(span=7).mean()
    # DMM赋值:如果LD>0 AND LD>HD,返回LD,否则返回0，的7日指数移动平均
    HDLD['DMM'] = 0
    HDLD.loc[HDLD['HD'] < HDLD['LD'], 'DMM'] = HDLD['LD']
    HDLD.loc[HDLD['LD'] <= 0, 'DMM'] = 0
    HDLD['DMM7'] = HDLD['DMM'].ewm(span=7).mean()
    # PDI赋值: DMP*100/真实波幅
    # MDI赋值: DMM*100/真实波幅
    HDLD = pd.concat([HDLD,TRIX['TR']], axis=1)
    HDLD['PDI'] = HDLD['DMP7']*100/HDLD['TR']
    HDLD['MDI'] = HDLD['DMM7']*100/HDLD['TR']
    # ADX赋值: MDI-PDI的绝对值/(MDI+PDI)*100，的7日指数移动平均
    HDLD['ADX'] = np.abs(HDLD['MDI'] - HDLD['PDI'])/(HDLD['MDI'] + HDLD['PDI'])*100
    HDLD['ADX7'] = HDLD['ADX'].ewm(span=7).mean()
    # P07赋值:如果PDI>MDI AND ADX>PDI AND ADX>50,返回3,否则返回如果PDI<MDI AND ADX>MDI AND ADX>50,返回-3,否则返回0
    HDLD['P07'] = 0
    HDLD.loc[HDLD['PDI'] > HDLD['MDI'], 'P07'] = 3
    HDLD.loc[HDLD['PDI'] < HDLD['MDI'], 'P07'] = -3
    HDLD.loc[HDLD['PDI'] == HDLD['MDI'], 'P07'] = 0
    HDLD.loc[HDLD['ADX7'] <= HDLD['PDI'], 'P07'] = 0
    HDLD.loc[HDLD['ADX7'] <= HDLD['MDI'], 'P07'] = 0
    HDLD.loc[HDLD['ADX7'] <= 50, 'P07'] = 0

    # 08
    # LC赋值:1日前的收盘价
    LC = stock_data[['close']].shift(1)
    LC.columns = ['Yesterday_close']
    # RSI赋值:收盘价-LC和0的较大值的5日指数移动平均/收盘价-LC的绝对值的5日指数移动平均*100
    LC['LC5'] = 0
    LC.loc[stock_data['close'] - LC['Yesterday_close']>0, 'LC5'] = (stock_data['close'] - LC['Yesterday_close'])
    LC['RSI5'] = LC['LC5'].ewm(span=5).mean()
    LC['ABS'] = np.abs(stock_data['close'] - LC['Yesterday_close'])
    LC['ABS5'] = LC['ABS'].ewm(span=5).mean()
    RSI = pd.concat([stock_data['close'], LC], axis=1)
    RSI['RSI'] = RSI['RSI5']/RSI['ABS5']*100
    # P08赋值:如果RSI1>80,返回1,否则返回如果RSI1<20,返回-1,否则返回0
    RSI['P08'] = 0
    RSI.loc[RSI['RSI'] > 80, 'P08'] = 1
    RSI.loc[RSI['RSI'] < 20, 'P08'] = -1
    
    # 09
    # TYP赋值:(最高价+最低价+收盘价)/3
    TYP = (stock_data['high']+stock_data['low']+stock_data['close'])/3
    # CCI赋值:(TYP-TYP的8日简单移动平均)/(0.015*TYP的8日平均绝对偏差)
    TYP8 = TYP.rolling(window=8).mean()
    # 平均绝对偏差的计算方法
    mad = lambda x: np.fabs(x-x.mean()).mean()
    AVEDEV = TYP.rolling(window=8).apply(mad)
    CCI = pd.concat([TYP, TYP8, AVEDEV], axis=1)
    CCI.columns = ['TYP','TYP8','AVEDEV']
    CCI['CCI'] = (CCI['TYP']-CCI['TYP8'])/(0.015*CCI['AVEDEV'])
    # P09赋值:如果CCI>180,返回2,否则返回如果CCI<-180,返回-2,否则返回0
    CCI['P09'] = 0
    CCI.loc[CCI['CCI'] > 180, 'P09'] = 2
    CCI.loc[CCI['CCI'] < -180, 'P09'] = -2

    # 10
    # WR赋值:(收盘价-6日内最低价的最低值)/(6日内最高价的最高值-6日内最低价的最低值)*100
    LOW6 = stock_data['low'].rolling(window=6).min()
    HIGH6 = stock_data['high'].rolling(window=6).max()
    WR = pd.concat([stock_data['close'], HIGH6, LOW6], axis=1)
    WR.columns = ['close','HIGH6','LOW6']
    WR['WR'] = (WR['close']-WR['LOW6'])/(WR['HIGH6']-WR['LOW6'])*100
    # P10赋值: 如果WR>80,返回1,否则返回如果WR<20,返回-1,否则返回0
    WR['P10'] = 0
    WR.loc[WR['WR'] > 80, 'P10'] = 1
    WR.loc[WR['WR'] < 20, 'P10'] = -1

    # 11
    # OSC赋值:100*(收盘价-收盘价的20日简单移动平均)
    MA20 = stock_data['close'].rolling(window=20).mean()
    OSC = pd.concat([stock_data['close'], MA20], axis=1)
    OSC.columns = ['close','MA20']
    OSC['OSC'] = 100*(OSC['close']-OSC['MA20'])
    # P11赋值:如果OSC>0,返回1,否则返回如果OSC<0,返回-1,否则返回0
    OSC['P11'] = 0
    OSC.loc[OSC['OSC'] > 0, 'P11'] = 1
    OSC.loc[OSC['OSC'] < 0, 'P11'] = -1

    # 12
    # MOM赋值:收盘价-7日前的收盘价
    MOM = stock_data.loc[:,['close']]
    MOM['Day7'] = MOM['close'].shift(7)
    MOM['MOM'] = MOM['close']-MOM['Day7']
    # P12赋值:如果MOM>0,返回1,否则返回如果MOM<0,返回-1,否则返回0
    MOM['P12'] = 0
    MOM.loc[MOM['MOM'] > 0, 'P12'] = 1
    MOM.loc[MOM['MOM'] < 0, 'P12'] = -1

    # 13
    # DPO赋值:收盘价-6日前的收盘价的11日简单移动平均
    MA11 = stock_data['close'].rolling(window=11).mean()
    DPO = pd.concat([stock_data['close'], MA11], axis=1)
    DPO.columns = ['close','MA11']
    DPO['MA11_Day6'] = DPO['MA11'].shift(6)
    DPO['DPO'] = DPO['close']-DPO['MA11_Day6']
    # P13赋值:如果DPO>0,返回1,否则返回如果DPO<0,返回-1,否则返回0
    DPO['P13'] = 0
    DPO.loc[DPO['DPO'] > 0, 'P13'] = 1
    DPO.loc[DPO['DPO'] < 0, 'P13'] = -1

    # 14
    # MB赋值:收盘价的12日简单移动平均
    # R赋值:(收盘价-MB)*(收盘价-MB)
    MB = stock_data['close'].rolling(window=12).mean()
    R = (stock_data['close']-MB)*(stock_data['close']-MB)
    # X1赋值:R的12日简单移动平均
    # X2赋值:X1的开方
    # D1赋值:1
    X1 = R.rolling(window=12).mean()
    X2 = X1**0.5
    D1 = 1
    # UPPER赋值:MB+(D1*X2)
    # LOWER赋值:MB-(D1*X2)
    UPPER = MB+(D1*X2)
    LOWER = MB-(D1*X2)
    BOLL = pd.concat([stock_data['close'], MB, R, X1, X2, UPPER, LOWER], axis=1)
    BOLL.columns = ['close','MB','R','X1','X2','UPPER','LOWER']
    # P14赋值:如果收盘价>UPPER,返回2,否则返回如果收盘价<LOWER,返回-2,否则返回0
    BOLL['P14'] = 0
    BOLL.loc[BOLL['close'] > BOLL['UPPER'], 'P14'] = 2
    BOLL.loc[BOLL['close'] < BOLL['LOWER'], 'P14'] = -2
    
    # 15
    # BR赋值:0和最高价-1日前的收盘价的较大值的14日累和/0和1日前的收盘价-最低价的较大值的14日累和*100
    Day1 = stock_data[['close']].shift(1)
    Day1.columns = ['Day1']
    BR = pd.concat([stock_data[['high','low']], Day1], axis=1)
    BR['high_Day1'] = BR['high']-BR['Day1']
    BR['max1'] = 0
    BR.loc[BR['high_Day1'] > 0, 'max1'] = BR['high_Day1']
    BR['sum14_1'] = BR['max1'].rolling(window=14).sum()
    BR['Day1_low'] = BR['Day1']-BR['low']
    BR['max2'] = 0
    BR.loc[BR['Day1_low'] > 0, 'max2'] = BR['Day1_low']
    BR['sum14_2'] = BR['max2'].rolling(window=14).sum()
    BR['BR'] = BR['sum14_1']/BR['sum14_2']*100
    # AR赋值:最高价-开盘价的14日累和/开盘价-最低价的14日累和*100
    AR = stock_data.loc[:,['open','high','low']]
    AR['high_open'] = AR['high']-AR['open']
    AR['sum14_3'] = AR['high_open'].rolling(window=14).sum()
    AR['open_loe'] = AR['open']-AR['low']
    AR['sum14_4'] = AR['open_loe'].rolling(window=14).sum()
    AR['AR'] = AR['sum14_3']/AR['sum14_4']*100
    BRAR = pd.concat([stock_data[['open','high','low','close']], BR['BR'], AR['AR']], axis=1)
    # P15赋值:如果BR>350 OR AR>180,返回3,否则返回如果BR<45 OR AR<45,返回-3,否则返回0
    BRAR['P15'] = 0
    BRAR.loc[BRAR['BR'] > 350, 'P15'] = 3
    BRAR.loc[BRAR['AR'] > 180, 'P15'] = 3
    BRAR.loc[BRAR['BR'] < 45, 'P15'] = -3
    BRAR.loc[BRAR['AR'] < 45, 'P15'] = -3

    # 16
    # TH赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回0的14日累和
    # TL赋值:如果收盘价<1日前的收盘价,返回成交量(手),否则返回0的14日累和
    # TQ赋值:如果收盘价=1日前的收盘价,返回成交量(手),否则返回0的14日累和
    THLQ = stock_data.loc[:,['close','volume']]
    THLQ['Day1'] = THLQ['close'].shift(1)
    THLQ['TH'] = 0
    THLQ.loc[THLQ['close'] > THLQ['Day1'],'TH'] = THLQ['volume']/100
    THLQ['TH14'] = THLQ['TH'].rolling(window=14).sum()
    THLQ['TL'] = 0
    THLQ.loc[THLQ['close'] < THLQ['Day1'],'TL'] = THLQ['volume']/100
    THLQ['TL14'] = THLQ['TL'].rolling(window=14).sum()
    THLQ['TQ'] = 0
    THLQ.loc[THLQ['close'] == THLQ['Day1'],'TQ'] = THLQ['volume']/100
    THLQ['TQ14'] = THLQ['TQ'].rolling(window=14).sum()
    # VR赋值:100*(TH*2+TQ)/(TL*2+TQ)
    THLQ['VR'] = 100*(THLQ['TH14']*2+THLQ['TQ14'])/(THLQ['TL14']*2+THLQ['TQ14'])
    # P16赋值:如果VR>350,返回3,否则返回如果VR<45,返回-3,否则返回0
    THLQ['P16'] = 0
    THLQ.loc[THLQ['VR'] > 350, 'P16'] = 3
    THLQ.loc[THLQ['VR'] < 45, 'P16'] = -3

    # 17
    # WVAD赋值:(收盘价-开盘价)/(最高价-最低价)*成交量(手)的6日累和/10000
    WVAD = (stock_data['close'] - stock_data['open'])/(stock_data['high'] - stock_data['low'])*(stock_data['volume']/100)
    WVAD = pd.concat([stock_data['volume'], WVAD], axis=1)
    WVAD.columns = ['volume','WVAD']
    WVAD['WVAD6'] = WVAD['WVAD'].rolling(window=6).sum()/10000
    # P17赋值:如果WVAD>0,返回1,否则返回如果WVAD<0,返回-1,否则返回0
    WVAD['P17'] = 0
    WVAD.loc[WVAD['WVAD6'] > 0, 'P17'] = 1
    WVAD.loc[WVAD['WVAD6'] < 0, 'P17'] = -1

    # 18
    # VOLUME赋值:成交量(手)的4日简单移动平均/成交量(手)
    VOLUME = stock_data[['volume']].rolling(window=4).mean()
    VOLUME['VOL'] = VOLUME['volume']/stock_data['volume']
    # MID赋值:100*(最高价+最低价-1日前的最高价+最低价)/(最高价+最低价)
    MID = stock_data[['high','low']].shift(1)
    MID['MID'] = 100*(stock_data['high']+stock_data['low']-MID['high']-MID['low'])/(stock_data['high']+stock_data['low'])
    # EMV赋值:MID*VOLUME*(最高价-最低价)/最高价-最低价的4日简单移动平均的4日简单移动平均
    EMV = pd.concat([VOLUME['VOL'], MID['MID']], axis=1)
    EMV['high_low'] = stock_data['high']-stock_data['low']
    EMV['high_low_4'] = EMV['high_low'].rolling(window=4).mean()
    EMV['MID_VOLUME'] = EMV['MID']*EMV['VOL']*EMV['high_low']/EMV['high_low_4']
    EMV['MID_VOLUME_4'] = EMV['MID_VOLUME'].rolling(window=4).mean()
    # P18赋值:如果EMV>0,返回1,否则返回如果EMV<0,返回-1,否则返回0
    EMV['P18'] = 0
    EMV.loc[EMV['MID_VOLUME_4'] > 0, 'P18'] = 1
    EMV.loc[EMV['MID_VOLUME_4'] < 0, 'P18'] = -1

    # 19
    # VA赋值:如果收盘价>1日前的收盘价,返回成交量(手),否则返回-成交量(手)
    OBV = stock_data[['close']].shift(1)
    va = stock_data['close'][0]
    OBV.loc[0:1,'close'] = va
    OBV['VA'] = stock_data['volume']/100
    OBV.loc[stock_data['close'] <= OBV['close'],'VA'] = -1*stock_data['volume']/100
    # OBV赋值:如果收盘价=1日前的收盘价,返回0,否则返回VA的历史累和
    OBV['OBV_VA'] = OBV['VA']
    OBV.loc[stock_data['close'] == OBV['close'],'OBV_VA'] = 0
    OBV['OBV'] = OBV['OBV_VA'].cumsum()
    # MAOBV赋值:OBV的24日指数移动平均
    OBV['MAOBV'] = OBV['OBV'].ewm(span=24).mean()
    # P19赋值:如果OBV>MAOBV,返回1,否则返回如果OBV<MAOBV,返回-1,否则返回0
    OBV['P19'] = 0
    OBV.loc[OBV['OBV'] > OBV['MAOBV'], 'P19'] = 1
    OBV.loc[OBV['OBV'] < OBV['MAOBV'], 'P19'] = -1
    
    # 20
    # PVI赋值:PVI
    PVI = stock_data[['close','volume']].shift(1)
    PVI['CLS'] = (stock_data['close']-PVI['close'])/PVI['close']
    PVI['vol'] = stock_data['volume']-PVI['volume']
    PVI['PV'] = 1
    PVI.loc[stock_data['volume']-PVI['volume'] > 0,'PV'] = (PVI['CLS']+1)
    PVI['PVI'] = PVI['PV'].cumprod()*100
    # MPVI赋值:PVI的24日指数移动平均
    PVI['MPVI'] = PVI['PVI'].ewm(span=24).mean()
    # P20赋值:如果PVI>MPVI,返回1,否则返回如果PVI<MPVI,返回-1,否则返回0
    PVI['P20'] = 0
    PVI.loc[PVI['PVI'] > PVI['MPVI'], 'P20'] = 1
    PVI.loc[PVI['PVI'] < PVI['MPVI'], 'P20'] = -1

    # 21
    # NVI赋值:NVI
    NVI = PVI.loc[:,['close','volume','CLS','vol']]
    NVI['NV'] = 1
    NVI.loc[stock_data['volume']-NVI['volume'] < 0,'NV'] = (NVI['CLS']+1)
    NVI['NVI'] = NVI['NV'].cumprod()*100
    # MNVI赋值:NVI的24日指数移动平均
    NVI['MNVI'] = NVI['NVI'].ewm(span=24).mean()
    # P21赋值:如果NVI>MNVI,返回2,否则返回如果NVI<MNVI,返回-2,否则返回0
    NVI['P21'] = 0
    NVI.loc[NVI['NVI'] > NVI['MNVI'], 'P21'] = 2
    NVI.loc[NVI['NVI'] < NVI['MNVI'], 'P21'] = -2

    # 22
    # MASS赋值:最高价-最低价的9日简单移动平均/最高价-最低价的9日简单移动平均的9日简单移动平均的25日累和
    MASS = stock_data.loc[:,['high','low']]
    MASS['high_low'] = MASS['high']-MASS['low']
    MASS['high_low_9'] = MASS['high_low'].rolling(window=9).mean()
    MASS['high_low_99'] = MASS['high_low_9'].rolling(window=9).mean()
    MASS['high_low_sum'] = MASS['high_low_9']/MASS['high_low_99']
    MASS['sum25'] = MASS['high_low_sum'].rolling(window=25).sum()
    # MA9赋值:收盘价的9日简单移动平均
    MASS['MA9'] = stock_data['close'].rolling(window=9).mean()
    MASS['MA9_day1'] = MASS['MA9'].shift(1)
    # P22赋值:如果MA9>1日前的MA9 AND MASS>26.5,返回2,否则返回如果MA9<1日前的MA9 AND MASS<26.5,返回-2,否则返回0
    MASS['P221'] = 0
    MASS['P222'] = 0
    MASS.loc[MASS['MA9'] > MASS['MA9_day1'], 'P221'] = 2
    MASS.loc[MASS['sum25'] <= 26.5, 'P221'] = 0
    MASS.loc[MASS['MA9'] <= MASS['MA9_day1'], 'P222'] = -2
    MASS.loc[MASS['sum25'] > 26.5, 'P222'] = 0
    MASS['P22'] = MASS['P221']+MASS['P222']

    # 23
    # NUM赋值:15日内最高价的最高值-15日内最低价的最低值的绝对值
    NUM = stock_data.loc[:,['high','low']]
    NUM['high15'] = NUM['high'].rolling(window=15).max()
    NUM['low15'] = NUM['low'].rolling(window=15).min()
    NUM['NUM'] = np.abs(NUM['high15']-NUM['low15'])
    # DEN赋值:收盘价-1日前的收盘价的绝对值的15日累和
    DEN = stock_data[['close']].shift(1)
    DEN['DEN_abs'] = np.abs(stock_data['close'] - DEN['close'])
    DEN['DEN'] = DEN['DEN_abs'].rolling(window=15).sum()
    # VHF赋值:如果DEN=0,返回0,否则返回NUM/DEN
    # VHF1赋值:VHF的240日指数移动平均
    VHF = pd.concat([NUM['NUM'], DEN['DEN']], axis=1)
    VHF['VHF'] = 0
    VHF.loc[VHF['DEN'] <> 0,'VHF'] = VHF['NUM']/VHF['DEN']
    VHF['VHF1'] = VHF['VHF'].ewm(span=240).mean()
    # P23赋值:如果VHF>VHF1,返回1,否则返回如果VHF<VHF1,返回-1,否则返回0
    VHF['P23'] = 0
    VHF.loc[VHF['VHF'] > VHF['VHF1'], 'P23'] = 1
    VHF.loc[VHF['VHF'] < VHF['VHF1'], 'P23'] = -1

    # 24
    # PU赋值:收盘价的13日简单移动平均
    # CU赋值:成交量(手)的13日简单移动平均
    # PU1赋值:(PU-1日前的PU)/1日前的PU*100
    # CU1赋值:(CU-1日前的CU)/1日前的CU*100
    PU = stock_data['close'].rolling(window=13).mean()
    CU = (stock_data['volume']/100).rolling(window=13).mean()
    PU1 = (PU-PU.shift(1))/PU.shift(1)*100
    CU1 = (CU-CU.shift(1))/CU.shift(1)*100
    PUCU = pd.concat([PU, CU, PU1, CU1], axis=1)
    PUCU.columns = ['PU','CU','PU1','CU1']
    # 逆时针曲线赋值:PU1+CU1
    PUCU['NSZ'] = PUCU['PU1']+PUCU['CU1']
    PUCU['NSZ1'] = PUCU['NSZ'].shift(1)
    # P24赋值:如果逆时针曲线>1日前的逆时针曲线,返回1,否则返回如果逆时针曲线<1日前的逆时针曲线,返回-1,否则返回0
    PUCU['P24'] = 0
    PUCU.loc[PUCU['NSZ'] > PUCU['NSZ1'], 'P24'] = 1
    PUCU.loc[PUCU['NSZ'] < PUCU['NSZ1'], 'P24'] = -1

    # 25
    # LC2赋值:1日前的收盘价
    # AA赋值:最高价-LC2的绝对值
    # BB赋值:最低价-LC2的绝对值
    # CC赋值:最高价-1日前的最低价的绝对值
    # DD赋值:LC2-1日前的开盘价的绝对值
    MASI = stock_data[['close']].shift(1)
    MASI.columns = ['LC2']
    c1 = stock_data['close'][0]
    l1 = stock_data['low'][0]
    o1 = stock_data['open'][0]
    MASI = MASI[['LC2']].fillna(c1)
    MASI['AA'] = np.abs(stock_data['high']-MASI['LC2'])
    MASI['BB'] = np.abs(stock_data['low']-MASI['LC2'])
    MASI['CC'] = np.abs(stock_data['high']-stock_data['low'].shift(1).fillna(l1))
    MASI['DD'] = np.abs(MASI['LC2']-stock_data['open'].shift(1).fillna(o1))
    # R2赋值:如果AA>BB AND AA>CC,返回AA+BB/2+DD/4,否则返回如果BB>CC AND BB>AA,返回BB+AA/2+DD/4,否则返回CC+DD/4
    MASI['R2'] = MASI['CC']+MASI['DD']/4
    MASI.loc[(MASI['AA']>MASI['BB']) & (MASI['AA']>MASI['CC']),'R2'] = MASI['AA']+MASI['BB']/2+MASI['DD']/4
    MASI.loc[(MASI['R2'] == MASI['CC']+MASI['DD']/4) & (MASI['BB']>MASI['CC']) & (MASI['BB']>MASI['AA']),'R2'] =     MASI['BB']+MASI['AA']/2+MASI['DD']/4
    # X01赋值:(收盘价-LC2+(收盘价-开盘价)/2+LC2-1日前的开盘价)
    MASI['X01'] = (stock_data['close']-MASI['LC2']+(stock_data['close']-stock_data['open'])/2+MASI['LC2']-stock_data['open'].shift(1).fillna(o1))
    # SI赋值:16*X01/R2*AA和BB的较大值
    MASI['AABB'] = MASI[['AA','BB']].apply(lambda x: x.max(), axis=1)
    MASI['SI'] = 16*MASI['X01']/MASI['R2']*MASI['AABB']
    # ASI赋值:SI的历史累和
    MASI['ASI'] = MASI['SI'].cumsum()
    # MASI赋值:ASI的6日简单移动平均
    MASI['MASI'] = MASI['ASI'].rolling(window=6).mean()
    # P25赋值:如果收盘价<13日内收盘价的最高值 AND ASI=13日内ASI的最高值,返回1,
    # 否则返回如果收盘价>13日内收盘价的最低值 AND ASI=13日内ASI的最低值,返回-1,否则返回0
    MASI['P25'] = 0
    MASI['close13_max'] = stock_data['close'].rolling(window=13).max()
    MASI['close13_min'] = stock_data['close'].rolling(window=13).min()
    MASI['ASI_max'] = MASI['ASI'].rolling(window=13).max()
    MASI['ASI_min'] = MASI['ASI'].rolling(window=13).min()
    MASI.loc[(stock_data['close']<MASI['close13_max']) & (MASI['ASI'] == MASI['ASI_max']),'P25'] = 1
    MASI.loc[(stock_data['close']>MASI['close13_min']) & (MASI['ASI'] == MASI['ASI_min']),'P25'] = -1

    # 26
    # BIAS赋值:(收盘价-收盘价的12日简单移动平均)/收盘价的12日简单移动平均*100
    BIAS = stock_data[['close']].rolling(window=12).mean()
    BIAS.columns = ['MA12']
    BIAS['BIAS'] = (stock_data['close']-BIAS['MA12'])/BIAS['MA12']*100
    # P26赋值:如果BIAS>10,返回1,否则返回如果BIAS<-10,返回-1,否则返回0
    BIAS['P26'] = 0
    BIAS.loc[BIAS['BIAS'] > 10, 'P26'] = 1
    BIAS.loc[BIAS['BIAS'] < -10, 'P26'] = -1
    
    # 输出决策曲线: (36+P01+P02+P03+P04+P05+P06+P07+P08+P09+P10+P11+P12+P13+P14+P15+P16+P17+P18+P19+P20+P21+P22+P23+P24+P25+P26)*1.36
    Decision = (MAPO_RSV_KD['P01']+MAPO_RSV_KD['P02']+MAPO_RSV_KD['P03']+MAPO_RSV_KD['P04']
                +EMA_DEA['P05']+TRIX['P06']+HDLD['P07']+RSI['P08']+CCI['P09']+WR['P10']
                +OSC['P11']+MOM['P12']+DPO['P13']+BOLL['P14']+BRAR['P15']+THLQ['P16']+WVAD['P17']+EMV['P18']
                +OBV['P19']+PVI['P20']+NVI['P21']+MASS['P22']+VHF['P23']+PUCU['P24']+MASI['P25']+BIAS['P26']+36)*1.36
    
    # 输出MAJCQX:决策曲线的3日简单移动平均
    MAJCQX = Decision.rolling(window=3).mean()
    Risk_Ratio = pd.concat([stock_data['close'],Decision, MAJCQX], axis=1)
    Risk_Ratio.columns = ['close','Decision','MAJCQX']
    
    Risk_Ratio.index = pd.to_datetime(Risk_Ratio.index)
    Risk_Ratio = Risk_Ratio.sort_index(axis=0, ascending=True)

    return Risk_Ratio

