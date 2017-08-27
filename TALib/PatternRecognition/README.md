## 模式识别相关函数的翻译与校验

|序号|函数名|翻译者|进度|校对者|进度|
|:---:|-----|----|:----:|----|:----:|
|1|[CDLADVANCEBLOCK](CDLADVANCEBLOCK.md) |灵峤|0|灵峤|0| 
|2|[CDLBELTHOLD](CDLBELTHOLD.md) |灵峤|0|灵峤|0| 
|3|[CDLBREAKAWAY](CDLBREAKAWAY.md) |灵峤|0|灵峤|0| 
|4|[CDLCLOSINGMARUBOZU](CDLCLOSINGMARUBOZU.md) |灵峤|0|灵峤|0| 
|5|[CDLCONCEALBABYSWALL](CDLCONCEALBABYSWALL.md) |灵峤|0|灵峤|0| 
|6|[CDLCOUNTERATTACK](CDLCOUNTERATTACK.md) |灵峤|0|灵峤|0| 
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
* The meaning of "long" and "very short" is specified with TA_SetCandleSettings;
* outInteger is positive (1 to 100) when white (bullish), negative (-1 to -100) when black (bearish).

### CDLBREAKAWAY
* Proceed with the calculation for the requested range.
* Must have:
* 1. first candle: long black (white)
* 2. second candle: black (white) day whose body gaps down (up)
* 3. third candle: black or white day with lower (higher) high and lower (higher) low than prior candle's
* 4. fourth candle: black (white) day with lower (higher) high and lower (higher) low than prior candle's
* 5. fifth candle: white (black) day that closes inside the gap, erasing the prior 3 days
* The meaning of "long" is specified with TA_SetCandleSettings;
* outInteger is positive (1 to 100) when bullish or negative (-1 to -100) when bearish;
* the user should consider that breakaway is significant in a trend opposite to the last candle, while this function does not consider it.

### CDLCLOSINGMARUBOZU
* Proceed with the calculation for the requested range.
* Must have:
* 1. long white (black) real body
* 2. no or very short upper (lower) shadow
* The meaning of "long" and "very short" is specified with TA_SetCandleSettings;
* outInteger is positive (1 to 100) when white (bullish), negative (-1 to -100) when black (bearish).

### CDLCONCEALBABYSWALL
Proceed with the calculation for the requested range.
* Must have:
* 1. first candle: black marubozu (very short shadows)
* 2. second candle: black marubozu (very short shadows)
* 3. third candle: black candle that opens gapping down but has an upper shadow that extends into the prior body
* 4. fourth candle: black candle that completely engulfs the third candle, including the shadows
* The meanings of "very short shadow" are specified with TA_SetCandleSettings;
* outInteger is positive (1 to 100): concealing baby swallow is always bullish;
* the user should consider that concealing baby swallow is significant when it appears in downtrend, while this function does not consider it.

### CDLCOUNTERATTACK
* Proceed with the calculation for the requested range.
* Must have:
* 1. first candle: long black (white)
* 2. second candle: long white (black) with close equal to the prior close
* The meaning of "equal" and "long" is specified with TA_SetCandleSettings;
* outInteger is positive (1 to 100) when bullish or negative (-1 to -100) when bearish;
* the user should consider that counterattack is significant in a trend, while this function does not consider it

### CDLCOUNTERATTACK
* Proceed with the calculation for the requested range.
* Must have:
* 1. first candle: long white candle
* 2. second candle: black candle that opens above previous day high and closes within previous day real body; 
* Greg Morris wants the close to be below the midpoint of the previous real body
* The meaning of "long" is specified with TA_SetCandleSettings, the penetration of the first real body is specified with optInPenetration;
* outInteger is negative (-1 to -100): dark cloud cover is always bearish;
* the user should consider that a dark cloud cover is significant when it appears in an uptrend, while this function does not consider it.
