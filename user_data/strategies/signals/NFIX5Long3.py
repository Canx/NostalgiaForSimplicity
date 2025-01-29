from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


# Long 3 entry signal
class NFIX5Long3(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=False)

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["RSI_20"] < df["RSI_20"].shift(1)) &
            (df["RSI_4"] < 46.0) &
            (df["AROONU_14"] < 25.0) &
            (df["close"] < df["SMA_16"] * 0.942)
        )

        return condition
