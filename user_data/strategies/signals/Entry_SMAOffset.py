from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class Entry_SMAOffset(Signal):
    def __init__(self, priority: int = 105):
        super().__init__(priority, enabled=False)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['close'] < df['EMA_16'] * 0.973) &
            (df['EWO'] > 5.672) &
            (df['RSI_14'] < 59)
        )