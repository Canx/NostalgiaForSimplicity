from Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta


class ADX(Signal):
    def init(self):
        self.priority = 1
        self.enabled = True
    
    def _calculate_adx(self, df: DataFrame, length: int = 14) -> DataFrame:

        adx = ta.adx(df["high"], df["low"], df["close"], length=length)
        df[f"ADX_{length}"] = adx[f"ADX_{length}"]
        return df

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        df = self._calculate_adx(df, 14)

        return df
