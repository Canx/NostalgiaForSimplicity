from Signal import Signal
from pandas import DataFrame
import pandas as pd
from freqtrade.strategy import IntParameter
from freqtrade.strategy import IStrategy


class Entry_SMAOffset(Signal):

    def __init__(self, strat: IStrategy, priority: int = 105):
        super().__init__(strat, priority, enabled=True)

        strat.buy_rsi = IntParameter(50, 70, default=59, space="buy")
  

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['close'] < df['EMA_16'] * 0.973) &
            (df['EWO'] > 5.672) &
            (df['RSI_14'] < self.strat.buy_rsi.value)
        )