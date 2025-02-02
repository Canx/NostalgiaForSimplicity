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

        return df