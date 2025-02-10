from Signal import Signal
from pandas import DataFrame
import pandas as pd
import numpy as np


class WaddarAttar(Signal):
    def init(self):
        self.priority = 10
        self.enabled = False
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:

        # Explosión y tendencia
        df['explosion'] = df['BBU_20_2.0'] - df['BBL_20_2.0']
        df['waddah_bull'] = np.where(df['MACD_12_26_9'] > 0, df['BBU_20_2.0'] - df['BBL_20_2.0'], 0)
        df['waddah_bear'] = np.where(df['MACD_12_26_9'] < 0, df['BBU_20_2.0'] - df['BBL_20_2.0'], 0)

        return df