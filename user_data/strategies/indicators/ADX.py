from signals.Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta


class ADX(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        
        df['ADX_14'] = ta.adx(high=df['high'], low=df['low'], close=df['close'], length=14)['ADX_14']

        return df
