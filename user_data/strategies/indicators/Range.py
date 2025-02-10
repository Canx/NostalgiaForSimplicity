from Signal import Signal
from pandas import DataFrame
import pandas_ta as ta
import numpy as np


class Range(Signal):
    def __init__(self, strat, priority: int = 10):
        super().__init__(strat, priority, enabled=False)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        df['EMA_55_1h_pricecross'] = np.where(
            ((df['close'].shift(1) < df['EMA_55_1h']) & (df['close'] > df['EMA_55_1h'])) |
            ((df['close'].shift(1) > df['EMA_55_1h']) & (df['close'] < df['EMA_55_1h'])),
            1, 0)

        df['cross_count'] = df['EMA_55_1h_pricecross'].rolling(window=55, min_periods=1).sum()  

        umbral = 2
        df['is_range'] = df['cross_count'] > umbral

        return df