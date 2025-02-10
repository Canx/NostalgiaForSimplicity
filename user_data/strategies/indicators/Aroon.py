from Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta


class Aroon(Signal):
    def __init__(self, strat, priority: int = 1):
        super().__init__(strat, priority, enabled=True)
    
    def aroon(self, df: DataFrame, length):
        
        aroon = ta.aroon(df["high"], df["low"], length=length)

        if isinstance(aroon, pd.DataFrame):
            df[f"AROONU_{length}"] = aroon[f"AROONU_{length}"]
            df[f"AROOND_{length}"] = aroon[f"AROOND_{length}"]
        else:
            df[f"AROONU_{length}"] = np.nan
            df[f"AROOND_{length}"] = np.nan
    
        return df

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        df = self.aroon(df, 14)

        return df

    def populate_indicators_15m(self, df: DataFrame) -> DataFrame:

        df = self.aroon(df, 14)

        return df


