from Signal import Signal
from pandas import DataFrame
import pandas_ta as pta



class CTI(Signal):
    def __init__(self, strat, priority: int = 1):
        super().__init__(strat, priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        
        df['cti'] = pta.cti(df["close"], length=20)

        return df