from Signal import Signal
from pandas import DataFrame
import pandas as pd


class ReverseMean(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=False)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        pass
    
    def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        pass