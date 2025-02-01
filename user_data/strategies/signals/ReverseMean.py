from Signal import Signal
from pandas import DataFrame
import pandas as pd


class ReverseMean(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        # price over EMA_55 1h
        # -1 candle RSI very low
        # 0 candle RSI increasing
        # green candle
        # significant drop in price in last 20 candles (>3%)
        # At least 1 bb_buy signal in the last 5 candles
        return (
            (df["close"] > df["EMA_55_1h"])
            & (df["RSI_3"].shift(1) < 15)
            & (df["RSI_3"] > 20)
            & (df["close"] > df["open"]) 
            & (df["significant_drop"])
            & (df["bb_buy"].rolling(window=5, min_periods=1).max() == True)
        )
    
    # TODO: Improve exits, to early sometimes
    # def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
    #     return (
    #         (df['price_over_bbu'].shift(1))
    #         & (df['close'] < df['BBU_20_2.0'])
    #         & (df['RSI_3'].shift(1) > 90)

    #     )
            
