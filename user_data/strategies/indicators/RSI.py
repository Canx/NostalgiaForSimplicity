from Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta


class RSI(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    
    def _calculate_rsi(self, df: DataFrame, length: int) -> DataFrame:

        df[f"RSI_{length}"] = ta.rsi(df["close"], length=length)
        return df

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        df = self._calculate_rsi(df, length=3)
        df = self._calculate_rsi(df, length=4)
        df = self._calculate_rsi(df, length=20)
        df = self._calculate_rsi(df, length=14)
        df = self._calculate_rsi(df, length=84)
        df = self._calculate_rsi(df, length=112)

        return df
