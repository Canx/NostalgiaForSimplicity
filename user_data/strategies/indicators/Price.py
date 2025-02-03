from Signal import Signal
import pandas as pd
from pandas import DataFrame


class Price(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        window = 200

        df['pct_change'] = 100 / df['open'] * df['close'] - 100

        df["range_pct"] = ((df["high"] - df["low"]) / df["low"]) * 100

        df["avg_range_pct"] = df["range_pct"].rolling(window=200).mean()

        df['retorno_20'] = df['close'].pct_change(periods=30).shift(1)

        # Señal de caída significativa y alza significativa
        umbral = 0.01
        df['significant_drop'] = df['retorno_20'] < -umbral
        df['significant_high'] = df['retorno_20'] > umbral

        return df