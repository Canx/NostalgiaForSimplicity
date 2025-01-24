from signals.Signal import Signal
from pandas import DataFrame


class FallingKnifeIndicator(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        condition = ()


        df["falling_knife"] = condition
        
        return df