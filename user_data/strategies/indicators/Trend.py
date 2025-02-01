from Signal import Signal
from pandas import DataFrame
import pandas_ta as ta
import numpy as np


class Trend(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        df['is_trending'] = (
            (df['close'] > df['EMA_55_1h']) #&      # Precio en 1h por encima de EMA_55_1h
            #(df['EMA_9_angle'] > 10) &             # Ángulo de EMA_9 en 5m mayor a 10 grados
            #(df['EMA_12_angle'] > 10) &            # Ángulo de EMA_12 en 5m mayor a 10 grados
            #(df['EMA_5'] > df['EMA_9']) &          # Orden ascendente en el corto plazo
            #(df['EMA_9_acceleration'] > 0)         # Aceleración positiva en EMA_9
            
        )

        return df