from Signal import Signal
from pandas import DataFrame
import pandas_ta as pta



class EWO(Signal):
    def __init__(self, strat, priority: int = 5):
        super().__init__(strat, priority, enabled=True)

    def EWO(self, df, ema_fast, ema_long):
        return (ema_fast - ema_long) / df['close'] * 100


    def populate_indicators(self, df: DataFrame) -> DataFrame:
        
        df['EWO'] = self.EWO(df, df["EMA_50"], df["EMA_200"])

        return df