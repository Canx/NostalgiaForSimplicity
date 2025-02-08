from Signal import Signal
from pandas import DataFrame
import pandas as pd


class ReverseMean(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=False)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        # -1 candle RSI very low
        # 0 candle RSI increasing
        # green candle
        # significant drop in price in last 20 candles (>3%)
        # At least 1 bb_buy signal in the last 5 candles
        return (
            #(df["is_trend"]) &
            #(df['kama'] > df['fama'])
            (df["ema_momemtum_signal"])
            #& (df["RSI_3"] > 35)
            #& (df["RSI_3"] < 91)
            #& (df["close"] > df["close"].shift(1))
            #& (df["close"] > df["EMA_50"]*0.985)
            #& (df["close"].shift(1) > df["open"].shift(1))
            #& (df["significant_drop"])
            & (df['bb_buy'].rolling(window=6, min_periods=1).sum() >= 2)
        )
    
    # TODO: Improve exits, to early sometimes
    # def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
    #     return (
    #         (df["close"] > df["EMA_50"])
    #         & (df["close"].shift(1) < df["EMA_50"])
    #         # (df['price_over_bbu'].shift(1))
    #         # & (df['close'] < df['BBU_20_2.0'])
    #         # & (df['RSI_3'].shift(1) > 90)

    #     )
            
