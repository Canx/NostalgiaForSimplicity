from Signal import Signal
from pandas import DataFrame
import pandas_ta as pta



class CTI(Signal):
    def init(self):
        self.priority = 1
        self.enabled = True
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        
        df['cti'] = pta.cti(df["close"], length=20)

        return df