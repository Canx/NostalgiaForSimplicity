from signals.Signal import Signal
import numpy as np
from pandas import DataFrame
import pandas_ta as ta


class EMA(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        # EMA
        df["EMA_5"] = ta.ema(df["close"], length=5)
        df["EMA_9"] = ta.ema(df["close"], length=9)
        df["EMA_12"] = ta.ema(df["close"], length=12)
        df["EMA_26"] = ta.ema(df["close"], length=26)
        df["EMA_50"] = ta.ema(df["close"], length=50)
        df["EMA_200"] = ta.ema(df["close"], length=200)

        # slope (1st derivative)
        df['EMA_5_slope'] = df['EMA_5'].diff()
        df['EMA_9_slope'] = df['EMA_9'].diff()
        df['EMA_12_slope'] = df['EMA_12'].diff()
        df['EMA_26_slope'] = df['EMA_26'].diff()
        df['EMA_50_slope'] = df['EMA_50'].diff()
        df['EMA_200_slope'] = df['EMA_200'].diff()

        # degrees
        df['EMA_9_angle'] = np.degrees(np.arctan(df['EMA_9_slope']))
        df['EMA_12_angle'] = np.degrees(np.arctan(df['EMA_12_slope']))
        df['EMA_26_angle'] = np.degrees(np.arctan(df['EMA_26_slope']))
        df['EMA_50_angle'] = np.degrees(np.arctan(df['EMA_50_slope']))
        df['EMA_200_angle'] = np.degrees(np.arctan(df['EMA_200_slope']))

        # acceleration (2nd derivative)
        df['EMA_5_acceleration'] = df['EMA_5_slope'].diff()
        df['EMA_9_acceleration'] = df['EMA_9_slope'].diff()
        df['EMA_12_acceleration'] = df['EMA_12_slope'].diff()
        df['EMA_26_acceleration'] = df['EMA_26_slope'].diff()
        df['EMA_50_acceleration'] = df['EMA_50_slope'].diff()
        df['EMA_200_acceleration'] = df['EMA_200_slope'].diff()

        return df
