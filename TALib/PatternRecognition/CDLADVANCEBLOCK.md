## CDLADVANCEBLOCK

## 指标概述
### 英文原文
* Proceed with the calculation for the requested range.
* Must have:
* 1. three white candlesticks with consecutively higher closes
* 2. each candle opens within or near the previous white real body 
* 3. first candle: long white with no or very short upper shadow (a short shadow is accepted too for more flexibility)
* 4. second and third candles, or only third candle, show signs of weakening: progressively smaller white real bodies 
* and/or relatively long upper shadows; see below for specific conditions;
* The meanings of "long body", "short shadow", "far" and "near" are specified with TA_SetCandleSettings;
* outInteger is negative (-1 to -100): advance block is always bearish;
* the user should consider that advance block is significant when it appears in uptrend, while this function;
* does not consider it.
<br>

#### 中文名称：
Advance Block 推进块（意译：大敌当前）

#### 形态判断：
* 1、三根收盘价连续抬升的红色实心阳线；
* 2、后一根阳线的开盘价在前一根阳线的实体里或接近实体，而非明显的跳空高开；
* 3、第一根K线，没有上影线（光头阳）或者只有短短的上影线；
* 4、第二根、第三根K线，或者仅第三根K先，显示出无力上攻的信号，红色实心阳线变小

#### 调用方法：
talib.CDLADVANCEBLOCK(open, high, low, close)

#### 输出：
-1代表不符合k线形态，-100表示符合形态。
