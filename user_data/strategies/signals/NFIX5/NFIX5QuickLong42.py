from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd

# Quick mode long 42 entry signal
class NFIX5QuickLong42(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def get_plugin_tag(self) -> str:
        return "ql_42"

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        condition = (
            (df["WILLR_14"] < -50.0) &
            (df["STOCHRSIk_14_14_3_3"] < 20.0) &
            (df["WILLR_84_1h"] < -70.0) &
            (df["STOCHRSIk_14_14_3_3_1h"] < 20.0) &
            (df["BBB_20_2.0_1h"] > 16.0) &
            (df["close_max_48"] >= (df["close"] * 1.10))
        )

        return condition
