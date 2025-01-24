from signals.Signal import Signal
from pandas import DataFrame


class FallingKnifeIndicator(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        df["falling_knife_start"] = (df["EMA_5_acceleration"] < -0.0005)

        # Verificar si el falling_knife_start ocurrió en las últimas 10 velas
        X = 10
        df["falling_knife_recent"] = (df["falling_knife_start"].rolling(window=X).apply(lambda x: x.any(), raw=True))

        df["falling_knife"] = (df["EMA_5_slope"] < 0) & df["falling_knife_recent"]
        return df