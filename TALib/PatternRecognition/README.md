## 模式识别相关函数的翻译与校验

|序号|函数名|翻译者|进度|校对者|进度|
|:---:|-----|----|:----:|----|:----:|
|1|[CDLADVANCEBLOCK](CDLADVANCEBLOCK.md) |小猪哥|0|灵峤|0| 
|2|[CDLBELTHOLD](CDLBELTHOLD.md) |小猪哥|0|灵峤|0| 
|3|[CDLBREAKAWAY](CDLBREAKAWAY.md) |Roggggggi.|0|灵峤|0| 
|4|[CDLCLOSINGMARUBOZU](CDLCLOSINGMARUBOZU.md) |Roggggggi.|0|灵峤|0| 
|5|[CDLCONCEALBABYSWALL](CDLCONCEALBABYSWALL.md) |Roggggggi.|0|灵峤|0| 
|6|[CDLCOUNTERATTACK](CDLCOUNTERATTACK.md) |Roggggggi.|0|灵峤|0| 
|7|[CDLDARKCLOUDCOVER](CDLDARKCLOUDCOVER.md) |Roggggggi.|0|灵峤|0| 
|8|[CDLDOJI](CDLDOJI.md) |刘晶晶|0|灵峤|0| 
<br>

## 英文原文

### CDLADVANCEBLOCK
* Proceed with the calculation for the requested range.
* Must have:
* 1. three white candlesticks with consecutively higher closes
* 2. each candle opens within or near the previous white real body 
* 3. first candle: long white with no or very short upper shadow (a short shadow is accepted too for more flexibility)
* 4. second and third candles, or only third candle, show signs of weakening: progressively smaller white real bodies 
* and/or relatively long upper shadows; see below for specific conditions:
* The meanings of "long body", "short shadow", "far" and "near" are specified with TA_SetCandleSettings;
* outInteger is negative (-1 to -100): advance block is always bearish;
* the user should consider that advance block is significant when it appears in uptrend, while this function does not consider it.

### CDLBELTHOLD
* Proceed with the calculation for the requested range.
* Must have:
* 1. long white (black) real body
* 2. no or very short lower (upper) shadow
* The meaning of "long" and "very short" is specified with TA_SetCandleSettings
* outInteger is positive (1 to 100) when white (bullish), negative (-1 to -100) when black (bearish)
