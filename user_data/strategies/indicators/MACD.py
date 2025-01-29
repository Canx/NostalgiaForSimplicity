from Signal import Signal
import numpy as np
from pandas import DataFrame
import pandas_ta as ta


class MACD(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        # MACD_12_26_9 → Línea MACD (Diferencia entre EMA rápida y EMA lenta).
        # MACDh_12_26_9 → Histograma (Diferencia entre MACD y la Señal).
        # MACDs_12_26_9 → Línea de Señal (EMA del MACD).
        
        df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)

        return df
