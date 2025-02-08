from Signal import Signal
from pandas import DataFrame
import talib.abstract as ta
from technical import qtpylib


class KamaFama(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        df['mama'], df['fama'] = ta.MAMA(df['close'], 0.5, 0.05)
        #df['mama_diff'] = (df['mama'] - df['fama'])
        df['kama'] = ta.KAMA(df['close'], 84)
        df["kama_slope"] = df["kama"].diff()
        df['mama_over_fama'] = df['mama'] > df['fama']
        #df["mama_crossup_fama"] = (df["mama"].shift(1) < df["fama"].shift(1)) & (df["mama"] >= df["fama"])
        df["kama_slope3_pct"] = (df["kama"] / df["kama"].shift(3) - 1) * 100
        df["kama_accel_pct"] = (df["kama_slope3_pct"] / df["kama_slope3_pct"].shift(4) - 1) * 100
        df["kama_min_prev_accel"] = df["kama_accel_pct"].shift(1).rolling(window=5, min_periods=1).min()

        #df["kama_buy"] = (df["kama_min_prev_accel"] < -0.015) & (df["kama_accel_pct"] > 0)
        df["mama_crossup_fama"] = qtpylib.crossed_above(df['mama'], df['fama'])
        df['mama_diff'] = 100 / df['mama'].shift(1) * df['mama'] - 100
        df['kama_increase'] = df['kama'] > df['kama'].shift(1)
        df['mama_diff_over'] = df['mama_diff'] > 0.1
        df["kama_buy"] = (
                (df["mama_crossup_fama"]) &
                (df['mama_diff_over']) &
                (df['kama_increase']) &
                (df['volume'] > 0)
        )



        return df