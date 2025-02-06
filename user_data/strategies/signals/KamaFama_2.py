from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class KamaFama_2(Signal):
    def __init__(self, priority: int = 105):
        super().__init__(priority, enabled=False)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['kama'] > df['fama']) &
            (df['fama'] > df['mama'] * 0.981) &
            (df['WILLR_14'] < -61.3) &
            (df['mama_diff'] < -0.025) &
            (df['cti'] < -0.715) &
            (df['close'].rolling(48).max() >= df['close'] * 1.05) &
            (df['close'].rolling(288).max() >= df['close'] * 1.125) &
            (df['RSI_84'] < 60) &
            (df['RSI_112'] < 60)
        )