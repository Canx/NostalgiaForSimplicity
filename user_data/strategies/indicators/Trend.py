from Signal import Signal
from pandas import DataFrame
import pandas_ta as ta
import numpy as np


class Trend(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        # TODO: Remove segments where price dropped significantly
        df['trend_filter'] = df["close"] > df["close"].rolling(window=50).mean()
        df['is_trend'] = (
            (df['low'] > df['EMA_55_1h'])           # Precio en 1h por encima de EMA_55_1h
            #(df['EMA_9_angle'] > 10) &             # Ángulo de EMA_9 en 5m mayor a 10 grados
            #(df['EMA_12_angle'] > 10) &            # Ángulo de EMA_12 en 5m mayor a 10 grados
            #(df['EMA_5'] > df['EMA_9']) &          # Orden ascendente en el corto plazo
            #(df['EMA_9_acceleration'] > 0)         # Aceleración positiva en EMA_9
            
        )

        # TODO: Create trend_level with this levels to use in dynamic ROI and custom_stoploss
        # 2: strong uptrend
        # 1: uptrend
        # 0: sideways
        # -1: downtrend
        # 2: strong downtrend

        return df