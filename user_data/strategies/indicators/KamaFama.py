from Signal import Signal
from pandas import DataFrame
import talib.abstract as ta
from technical import qtpylib


class KamaFama(Signal):
    def init(self):
        self.priority = 5
        self.enabled = True
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        df['hl2'] = (df['high'] + df['low']) / 2
        df['mama'], df['fama'] = ta.MAMA(df['hl2'], 0.25, 0.025)
        df['mama_diff'] = ( ( df['mama'] - df['fama'] ) / df['hl2'] )
        df['kama'] = ta.KAMA(df['close'], 84)
        df["kama_slope"] = df["kama"].diff()
        df['mama_over_fama'] = df['mama'] > df['fama']
        df['kama_over_fama'] = df['kama'] > df['fama']
        df['mama_offset_0981'] = (df['mama'] * 0.981)
        df['fama_over_mama'] = (df['fama'] > df['mama_offset_0981'])
        df['WILLR_KF'] = (df['WILLR_14'] < -61.3)
        df['mamadiff_KF'] = (df['mama_diff'] < -0.025)
        df['cti_KF'] = (df['cti'] < -0.715)
        df['close48_KF'] = (df['close'].rolling(48).max() >= df['close'] * 1.05)
        df['close288_KF'] = (df['close'].rolling(288).max() >= df['close'] * 1.125)
        df['RSI84_KF'] = (df['RSI_84'] < 60)
        df['RSI112_KF'] = (df['RSI_112'] < 60)

        return df