from Signal import Signal
from pandas import DataFrame
import pandas as pd


class Momemtum(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=False)
    

    # TODO: Buys too much in peaks
    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (df['macd_buy'])
    
    # def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
    #     pass