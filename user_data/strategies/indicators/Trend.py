from Signal import Signal
from pandas import DataFrame
import pandas_ta as ta
import numpy as np


class Trend(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        df['trending'] = (
            (df['close'] > df['EMA_55_1h']) &      # Precio en 1h por encima de EMA_55_1h
            #(df['EMA_9_angle'] > 10) &             # Ángulo de EMA_9 en 5m mayor a 10 grados
            #(df['EMA_12_angle'] > 10) &            # Ángulo de EMA_12 en 5m mayor a 10 grados
            #(df['EMA_5'] > df['EMA_9']) &          # Orden ascendente en el corto plazo
            (df['EMA_9_acceleration'] > 0)         # Aceleración positiva en EMA_9
            
        )

        return df

        # required_columns = ["EMA_200_acceleration", "EMA_50_acceleration", "EMA_26_acceleration", "EMA_12_acceleration", "EMA_9_acceleration"]
    
        # # Verificar columnas requeridas
        # for col in required_columns:
        #     if col not in df.columns:
        #         raise KeyError(f"La columna requerida '{col}' no está presente en el DataFrame. Asegúrate de que los indicadores se generen correctamente.")

        # # Initialize the 'downtrend_signals' column with zeros
        # df['trend'] = 0

        # # Increase downtrend signals based on conditions (ordered from more to less reactive)
        # df['trend'] += (df["EMA_200_acceleration"])
        # df['trend'] += (df["EMA_50_acceleration"])
        # df['trend'] += (df["EMA_26_acceleration"]) * 3
        # df['trend'] += (df["EMA_12_acceleration"]) * 2
        # df['trend'] += (df["EMA_9_acceleration"]) 

        # alpha = 0.1  # Coeficiente de suavizado (más pequeño = más suavizado)
        # df['trend_smoothed'] = df['trend'].ewm(alpha=alpha, adjust=False).mean()

        # df['uptrend_start'] = (
        #     (df["trend_smoothed"] > 0)
        #      & (df["trend_smoothed"].shift(1) < 0)
        # )

        # df['downtrend_start'] = (

        #     (df["trend_smoothed"] < 0)
        #      & (df["trend_smoothed"].shift(1) > 0)
        # )