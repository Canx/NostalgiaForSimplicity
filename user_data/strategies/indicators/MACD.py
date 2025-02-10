from Signal import Signal
import numpy as np
from pandas import DataFrame
import pandas_ta as ta


class MACD(Signal):
    def init(self):
        self.priority = 1
        self.enabled = True
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        # MACD_12_26_9 → Línea MACD (Diferencia entre EMA rápida y EMA lenta).
        # MACDh_12_26_9 → Histograma (Diferencia entre MACD y la Señal).
        # MACDs_12_26_9 → Línea de Señal (EMA del MACD).
        
        df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

        df['macd_crossover'] = (df['MACD_12_26_9'] > df['MACDs_12_26_9']) & (df['MACD_12_26_9'].shift(1) <= df['MACDs_12_26_9'].shift(1))
        df['macd_positive'] = df['MACDh_12_26_9'] > 0
        df['macd_buy'] = df['macd_crossover'] & df['macd_positive']

        return df
