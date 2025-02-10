from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class Entry_MACD(Signal):
    def init(self):
        self.priority = 105
        self.enabled = False
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df["macd_buy"].rolling(window=20).sum() > 0)
            & (df['volume'] > df['volume'].shift() * 3)
            & (df['trend_filter'])
            & (df["RSI_14"] < 60)
            & df['not_too_green']
            & (df['close'] > df['open'])
        )