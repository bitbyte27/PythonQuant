# CDLADVANCEBLOCK

* Proceed with the calculation for the requested range.
* Must have:
* - three white candlesticks with consecutively higher closes
* - each candle opens within or near the previous white real body 
* - first candle: long white with no or very short upper shadow (a short shadow is accepted too for more flexibility)
* - second and third candles, or only third candle, show signs of weakening: progressively smaller white real bodies 
* and/or relatively long upper shadows; see below for specific conditions;
* The meanings of "long body", "short shadow", "far" and "near" are specified with TA_SetCandleSettings;
* outInteger is negative (-1 to -100): advance block is always bearish;
* the user should consider that advance block is significant when it appears in uptrend, while this function;
* does not consider it.
