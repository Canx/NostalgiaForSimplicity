from Signal import Signal
from pandas import DataFrame
import pandas as pd


# Long 1 entry signal
class NFIX5Long1(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=False)


    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["EMA_26"] > df["EMA_12"]) &
            ((df["EMA_26"] - df["EMA_12"]) > (df["open"] * 0.030)) &
            ((df["EMA_26"].shift() - df["EMA_12"].shift()) > (df["open"] / 100.0)) &
            (df["close"] < (df["BBL_20_2.0"] * 0.999))
        )

        return condition
