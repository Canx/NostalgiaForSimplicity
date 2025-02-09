from Signal import Signal
import numpy as np
from pandas import DataFrame
import pandas_ta as ta


class WMA(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=False)
    
    def tv_wma(df, length = 9) -> DataFrame:
        """
        Source: Tradingview "Moving Average Weighted"
        Pinescript Author: Unknown
        Args :
            dataframe : Pandas Dataframe
            length : WMA length
            field : Field to use for the calculation
        Returns :
            dataframe : Pandas DataFrame with new columns 'tv_wma'
        """

        norm = 0
        sum = 0

        for i in range(1, length - 1):
            weight = (length - i) * length
            norm = norm + weight
            sum = sum + df.shift(i) * weight

        tv_wma = (sum / norm) if norm > 0 else 0
        return tv_wma

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        return df
