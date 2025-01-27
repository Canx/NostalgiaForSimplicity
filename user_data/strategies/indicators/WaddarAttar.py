from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd
import numpy as np


class WaddarAttar(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=False)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        ema_fast_period = 12
        ema_slow_period = 26
        channel_period = 20
        sensitivity = 2.0

        df['ema_fast'] = df['close'].ewm(span=ema_fast_period).mean()
        df['ema_slow'] = df['close'].ewm(span=ema_slow_period).mean()

        # MACD como diferencia entre EMA rápida y EMA lenta
        df['macd'] = df['ema_fast'] - df['ema_slow']

        # Bandas de Bollinger (explosión de volatilidad)
        df['bollinger_mid'] = df['close'].rolling(window=channel_period).mean()
        df['bollinger_std'] = df['close'].rolling(window=channel_period).std()
        df['bollinger_upper'] = df['bollinger_mid'] + (sensitivity * df['bollinger_std'])
        df['bollinger_lower'] = df['bollinger_mid'] - (sensitivity * df['bollinger_std'])

        # Explosión y tendencia
        df['explosion'] = df['bollinger_upper'] - df['bollinger_lower']
        df['waddah_bull'] = np.where(df['macd'] > 0, df['explosion'], 0)
        df['waddah_bear'] = np.where(df['macd'] < 0, df['explosion'], 0)

        return df