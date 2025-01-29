from Signal import Signal
from pandas import DataFrame
import pandas as pd


# Long 5 entry signal
class NFIX5Long5(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["RSI_3"] < 50.0) &
            (df["AROONU_14"] < 25.0) &
            (df["AROOND_14"] > 75.0) &
            (df["STOCHRSIk_14_14_3_3"] < 30.0) &
            (df["EMA_26"] > df["EMA_12"]) &
            ((df["EMA_26"] - df["EMA_12"]) > (df["open"] * 0.020)) &
            ((df["EMA_26"].shift() - df["EMA_12"].shift()) > (df["open"] / 100.0))
        )

        return condition
