from Signal import Signal
import pandas as pd
import talib as ta


# Exit borrowed from KamaFama_2
class Exit_Stochastic(Signal):

    

    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=False)

    def exit_signal(self, df: pd.DataFrame, metadata: dict) -> pd.Series:
        import talib as ta

        fastk, fastd = ta.STOCHF(
            df['high'].values,
            df['low'].values,
            df['close'].values,
            5, 3, 0
        )
        df['fastk'] = fastk

        return ((df['fastk'] > 90) & (df['RSI_14'] > 70))