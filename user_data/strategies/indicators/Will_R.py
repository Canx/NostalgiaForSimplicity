from Signal import Signal
from pandas import DataFrame
import pandas_ta as pta


class Will_R(Signal):
    def init(self):
        self.priority = 1
        self.enabled = True
    
    def _calculate_willr(self, df: DataFrame, length: int) -> DataFrame:

        df[f"WILLR_{length}"] = pta.willr(df["high"], df["low"], df["close"], length=length)
        
        return df

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        df = self._calculate_willr(df, length=14)

        return df