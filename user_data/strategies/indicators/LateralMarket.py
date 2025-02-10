from Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta


class LateralMarket(Signal):
    def init(self):
        self.priority = 10
        self.enabled = False
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        
        df["lateral"] = (
            (abs(df["SMA_50"].diff()) < 0.1) &  # Pendiente del SMA baja
            (df["ADX_14"] < 20) &  # ADX indica mercado sin tendencia
            ((df["BBU_20_2.0"] - df["BBL_20_2.0"]) < 0.2)  # Bandas de Bollinger estrechas
        )

        return df
