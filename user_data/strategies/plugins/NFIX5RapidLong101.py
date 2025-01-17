from SignalPlugin import SignalPlugin
from pandas import DataFrame
import pandas as pd

# Rapid mode long 101 entry signal
class NFIX5RapidLong101(SignalPlugin):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def get_plugin_tag(self) -> str:
        return "rl_101"

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["RSI_14"] < 36.0) &
            (df["AROONU_14"] < 25.0) &
            (df["STOCHRSIk_14_14_3_3"] < 20.0) &
            (df["close"] < (df["SMA_16"] * 0.946)) &
            (df["AROONU_14_15m"] < 50.0)
        )

        return condition
