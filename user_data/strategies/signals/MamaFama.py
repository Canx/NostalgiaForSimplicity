from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class MamaFama(Signal):
    def __init__(self, priority: int = 105):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df["mama_crossup_fama"]) 
            & (df["ADX_14"] > 15)
            & (df["vwma_diff"] > 0.0013)
        )