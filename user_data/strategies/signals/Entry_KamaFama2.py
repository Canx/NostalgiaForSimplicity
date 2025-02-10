from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class Entry_KamaFama2(Signal):
    def __init__(self, strat, priority: int = 105):
        super().__init__(strat, priority, enabled=False)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['kama_over_fama']) &
            (df['fama_over_mama']) &
            (df['WILLR_KF']) &
            (df['mamadiff_KF']) &
            (df['cti'] < -0.715) &
            (df['close48_KF']) &
            #(df['close288_KF']) &
            (df['RSI84_KF']) &
            (df['RSI112_KF'])
        )