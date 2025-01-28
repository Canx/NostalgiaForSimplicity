from signals.Signal import Signal
import numpy as np
from pandas import DataFrame
import pandas_ta as ta


class SMA(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        # SMA
        df["SMA_5"] = ta.sma(df["close"], length=5)
        df["SMA_9"] = ta.sma(df["close"], length=9)
        df["SMA_12"] = ta.sma(df["close"], length=12)
        df["SMA_26"] = ta.sma(df["close"], length=26)
        df["SMA_50"] = ta.sma(df["close"], length=50)
        df["SMA_200"] = ta.sma(df["close"], length=200)

        return df
