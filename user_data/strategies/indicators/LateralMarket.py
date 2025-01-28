from signals.Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta


class LateralMarket(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        
        df["lateral"] = (
            (abs(df["SMA_50"].diff()) < 0.1) &  # Pendiente del SMA baja
            (df["ADX_14"] < 20) &  # ADX indica mercado sin tendencia
            ((df["BBU_20_2.0"] - df["BBL_20_2.0"]) < 0.2)  # Bandas de Bollinger estrechas
        )

        return df
