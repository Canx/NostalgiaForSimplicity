from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class Entry_MACD(Signal):
    def __init__(self, priority: int = 105):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df["macd_buy"])
            & (df["RSI_14"] < 50)
            & (df["RSI_3"] < 80)
        )