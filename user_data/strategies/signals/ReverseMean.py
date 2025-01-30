from Signal import Signal
from pandas import DataFrame
import pandas as pd


class ReverseMean(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df["bb_buy"] == False) 
            & (df["bb_buy"].rolling(window=2, min_periods=1).max() == True)
            & (df["close"] > df["open"]) 
        )
    
    def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['price_over_bbu'].shift(1))
            & (df['close'] < df['BBU_20_2.0'])
            & (df['close'] < df['open'])
        )
            
