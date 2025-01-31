from Signal import Signal
from pandas import DataFrame
import pandas as pd


# Long 4 entry signal
class NFIX5Long4(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=False)


    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["AROONU_14"] < 25.0) &
            (df["AROONU_14_15m"] < 25.0) &
            (df["close"] < (df["EMA_9"] * 0.942)) &
            (df["close"] < (df["EMA_20"] * 0.960))
        )

        return condition
