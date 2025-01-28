from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


class ReverseMean(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            # Nos aseguramos de que estemos en mercado lateral.
            df["lateral"]
            & (df["uptrend_start"])
        )   
    
    # def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
    #    return df["downtrend_start"]
