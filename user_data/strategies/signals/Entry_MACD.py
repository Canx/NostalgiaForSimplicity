from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class Entry_MACD(Signal):
    def __init__(self, priority: int = 105):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df["macd_buy"].rolling(window=5).sum() > 0)
            & (df['volume_filter'])
            & (df['trend_filter'])
            #& (df['trend_filter'].shift(1) == False)
            & (df["RSI_14"] < 70)
            & df['not_too_green']
        )