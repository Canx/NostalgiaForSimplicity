from Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta


class Price(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        window = 200

        df["range_pct"] = ((df["high"] - df["low"]) / df["low"]) * 100

        df["avg_range_pct"] = df["range_pct"].rolling(window=200).mean()

        df['price_drop'] = (df['close'] - df['close'].shift(20)) / df['close'].shift(20)
        df['significant_drop'] = df['price_drop'] < -0.03


        return df