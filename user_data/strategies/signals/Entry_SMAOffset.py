from Signal import Signal
from pandas import DataFrame
import pandas as pd
from freqtrade.strategy import IntParameter
from freqtrade.strategy import IStrategy


class Entry_SMAOffset(Signal):

    def __init__(self, priority: int = 105):
        super().__init__(priority, enabled=True)

    def config_strategy(self, strat: IStrategy):
        strat.buy_rsi = IntParameter(50, 70, default=59, space="buy")
        super().config_strategy(strat)
  

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['close'] < df['EMA_16'] * 0.973) &
            (df['EWO'] > 5.672) &
            (df['RSI_14'] < self.strat.buy_rsi.value)
        )