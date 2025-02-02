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

        df['price_drop'] = (df['close'] - df['close'].shift(30)) / df['close'].shift(30)
        df['significant_drop'] = df['price_drop'].shift(1) < -0.02
        df['significant_high'] = df['price_drop'].shift(1) > 0.02


        return df