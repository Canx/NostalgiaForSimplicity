from Signal import Signal
from pandas import DataFrame
import pandas_ta as ta
import numpy as np


class StochRSI(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    
    def _calculate_stochrsi(self, df: DataFrame) -> DataFrame:

        stochrsi = ta.stochrsi(df["close"])
        if isinstance(stochrsi, DataFrame):
            df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]
            df["STOCHRSId_14_14_3_3"] = stochrsi["STOCHRSId_14_14_3_3"]
        else:
            df["STOCHRSIk_14_14_3_3"] = np.nan
            df["STOCHRSId_14_14_3_3"] = np.nan

        # Calculate slopes
        df["STOCHRSIk_14_14_3_3_slope"] = df["STOCHRSIk_14_14_3_3"].diff() / df["STOCHRSIk_14_14_3_3"].shift()

        return df

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        df = self._calculate_stochrsi(df)

        return df
