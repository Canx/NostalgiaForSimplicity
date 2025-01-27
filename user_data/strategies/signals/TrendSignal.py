from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


class TrendSignal(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df["uptrend_start"])
        )
    
    
    #def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
    #    return df["downtrend_start"]