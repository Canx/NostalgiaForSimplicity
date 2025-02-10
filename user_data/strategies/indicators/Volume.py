from Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as pta


class Volume(Signal):
    def init(self):
        self.priority = 1
        self.enabled = True

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        df['mfi'] = pta.mfi(df['high'], df['low'], df['close'], df['volume'], length=14)
        df['vwma'] = (df['close'] * df['volume']).rolling(window=20).sum() / df['volume'].rolling(window=20).sum()
        df['vwma_diff'] = df['vwma'].diff()
        df['volume_filter'] = df["volume"] > df["volume"].rolling(window=20).mean()

        return df
