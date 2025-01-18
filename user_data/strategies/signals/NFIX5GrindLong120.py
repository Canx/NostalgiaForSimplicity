from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd

# Grind mode long 120 entry signal
class NFIX5GrindLong120(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def get_plugin_tag(self) -> str:
        return "gl_120"

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["STOCHRSIk_14_14_3_3"] < 20.0) &
            (df["WILLR_14"] < -80.0) &
            (df["AROONU_14"] < 25.0) &
            (df["close"] < (df["EMA_20"] * 0.978))
        )

        return condition
