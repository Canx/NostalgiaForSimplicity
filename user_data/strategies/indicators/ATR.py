from Signal import Signal
from pandas import DataFrame
import pandas_ta as pta



class ATR(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        
        df['ATR_14'] = pta.atr(high=df['high'], low=df['low'], close=df['close'], length=14)

        return df