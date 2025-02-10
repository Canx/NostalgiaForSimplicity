from Signal import Signal
from pandas import DataFrame
import pandas as pd
from freqtrade.strategy import IntParameter


class Entry_SMAOffset(Signal):

    def init(self):
        self.priority = 105
        self.enabled = True
        self.strat.buy_rsi = IntParameter(50, 70, default=59, space="buy")
  

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['close'] < df['EMA_16'] * 0.973) &
            (df['EWO'] > 5.672) &
            (df['RSI_14'] < self.strat.buy_rsi.value)
        )