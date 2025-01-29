from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


# Long 2 entry signal
class NFIX5Long2(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)


    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["AROONU_14"] < 25.0) &
            (df["STOCHRSIk_14_14_3_3"] < 20.0) &
            (df["close"] < (df["EMA_20"] * 0.944))
        )

        return condition
