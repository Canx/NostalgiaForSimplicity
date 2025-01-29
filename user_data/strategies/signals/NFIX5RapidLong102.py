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
            (df["NFIX5_102"].rolling(window=5, min_periods=1).max().astype(bool))
            & (df["close"] > df["open"])
            & (df["close"].shift() < df["open"].shift())
        )

        return condition
