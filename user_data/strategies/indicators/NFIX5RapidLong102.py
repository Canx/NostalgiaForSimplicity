from Signal import Signal
from pandas import DataFrame
import pandas_ta as ta
import numpy as np


class NFIX5RapidLong102(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=False)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        df["NFIX5_102"] = (
            (df["WILLR_14"] < -95.0)
            & (df["STOCHRSIk_14_14_3_3"] < 10.0)
            & (df["close"] < (df["BBL_20_2.0"] * 0.999))
            & (df["close"] < (df["EMA_20"] * 0.960))
        )

        return df