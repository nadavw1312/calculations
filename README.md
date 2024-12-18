﻿# calculations
- class: Atr
  description: Measures the average true range of price movement over a defined period
    to assess volatility.
  returns_structure:
    columns:
    - dtype: Float32
      name: ATR_<timeframe>_<period>
    type: pl.DataFrame
  usage_example: 'Atr.calc(df, {''timeframe'': ''1d'', ''period'': 14})'
- class: Ema
  description: Calculates the exponentially weighted average price over a specified
    number of periods.
  returns_structure:
    columns:
    - dtype: pl.Float64
      name: EMA_{timeframe}_{window}
    type: pl.DataFrame
  usage_example: 'Ema.calc(df, params={''window'': 20, ''timeframe'': ''1d''})'
- class: Macd
  description: The MACD is a trend-following momentum indicator that shows the relationship
    between two moving averages of prices.
  returns_structure:
    columns:
    - dtype: pl.Float64
      name: MACD_1d_<fast_ema_period>_<slow_ema_period>
    - dtype: pl.Float64
      name: MACD_SIGNAL_1d_<fast_ema_period>_<slow_ema_period>_<signal_ema_period>
    - dtype: pl.Float64
      name: MACD_HIST_1d_<fast_ema_period>_<slow_ema_period>_<signal_ema_period>
    type: pl.DataFrame
  usage_example: 'Macd.calc(df, params={''timeframe'': ''1d'', ''fast_ema_period'':
    12, ''slow_ema_period'': 26, ''signal_ema_period'': 9})'
- class: Sma
  description: Calculates the average price over a specified number of periods.
  returns_structure:
    columns:
    - dtype: pl.Float64
      name: SMA_{timeframe}_{window}
    type: pl.DataFrame
  usage_example: 'Sma.calc(df, params={''window'': 20, ''timeframe'': ''1d''})'
