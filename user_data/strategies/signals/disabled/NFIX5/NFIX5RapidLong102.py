from Signal import Signal
from pandas import DataFrame
import pandas as pd

# Rapid mode long 102 entry signal
class NFIX5RapidLong102(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["WILLR_14"] < -95.0)
            & (df["STOCHRSIk_14_14_3_3"] < 10.0)
            & (df["close"] < (df["BBL_20_2.0"] * 0.999))
            & (df["close"] < (df["EMA_20"] * 0.960))
        )

        return condition
