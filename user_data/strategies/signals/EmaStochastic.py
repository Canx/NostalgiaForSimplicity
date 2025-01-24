from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


class EmaStochastic(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        condition = (
            (df["STOCHRSIk_14_14_3_3_slope"] > 0)
            #& (df["STOCHRSIk_14_14_3_3_slope"].shift(1) < 0)
            #& (df["EMA_12_slope"] > 0)
            #& (df["close"] < df["EMA_200"]) &
            #& (df["EMA_200_slope"] > 0)
        )

        return condition
        