from Signal import Signal
from pandas import DataFrame
import pandas as pd
import numpy as np


class WaddarAttar(Signal):
    def __init__(self, strat, priority: int = 10):
        super().__init__(strat, priority, enabled=False)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        # Explosión y tendencia
        df['explosion'] = df['BBU_20_2.0'] - df['BBL_20_2.0']
        df['waddah_bull'] = np.where(df['MACD_12_26_9'] > 0, df['BBU_20_2.0'] - df['BBL_20_2.0'], 0)
        df['waddah_bear'] = np.where(df['MACD_12_26_9'] < 0, df['BBU_20_2.0'] - df['BBL_20_2.0'], 0)

        return df