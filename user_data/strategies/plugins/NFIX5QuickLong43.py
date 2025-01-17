from SignalPlugin import SignalPlugin
from pandas import DataFrame
import pandas as pd

# Rapid mode long 101 entry signal
class NFIX5QuickLong43(SignalPlugin):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def get_plugin_tag(self) -> str:
        return "ql_101"

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        condition = (
            (df["RSI_14"] < 40.0) &
            (df["MFI_14"] < 40.0) &
            (df["AROONU_14"] < 25.0) &
            (df["EMA_26"] > df["EMA_12"]) &
            ((df["EMA_26"] - df["EMA_12"]) > (df["open"] * 0.024)) &
            ((df["EMA_26"].shift() - df["EMA_12"].shift()) > (df["open"] / 100.0)) &
            (df["close"] < (df["EMA_20"] * 0.958)) &
            (df["close"] < (df["BBL_20_2.0"] * 0.992))
        )

        return condition
