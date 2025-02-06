from Signal import Signal
from pandas import DataFrame
import talib.abstract as ta


class KamaFama(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        df['hl2'] = (df['high'] + df['low']) / 2
        df['mama'], df['fama'] = ta.MAMA(df['hl2'], 0.25, 0.025)
        df['mama_diff'] = ( ( df['mama'] - df['fama'] ) / df['hl2'] )
        df['kama'] = ta.KAMA(df['close'], 84)
        df["kama_slope"] = df["kama"].diff()
        df['mama_over_fama'] = df['mama'] > df['fama']
        df["mama_crossup_fama"] = (df["mama"].shift(1) < df["fama"].shift(1)) & (df["mama"] >= df["fama"])
        df["kama_slope3_pct"] = (df["kama"] / df["kama"].shift(3) - 1) * 100
        df["kama_accel_pct"] = df["kama_slope3_pct"].diff()

        df["kama_bottom"] = (df["kama_accel_pct"] > 0.1) #(df["kama_slope3_pct"] < 0) & 



        return df