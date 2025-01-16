import pandas_ta as ta
from SignalPlugin import SignalPlugin
from pandas import DataFrame
import pandas as pd
import numpy as np

# Long 6 entry signal
class NFIX5Long6(SignalPlugin):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def get_plugin_tag(self) -> str:
        return "6"

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        Add necessary indicators to the DataFrame.
        """
        df["RSI_20"] = ta.rsi(df["close"], length=20)
        df["RSI_3"] = ta.rsi(df["close"], length=3)

        stochrsi = ta.stochrsi(df["close"])
        if isinstance(stochrsi, pd.DataFrame):
            df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]
            df["STOCHRSId_14_14_3_3"] = stochrsi["STOCHRSId_14_14_3_3"]
        else:
            df["STOCHRSIk_14_14_3_3"] = np.nan
            df["STOCHRSId_14_14_3_3"] = np.nan

        df["SMA_16"] = ta.sma(df["close"], length=16)
        
        # Asegurarse de devolver el DataFrame modificado
        return df

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on conditions.
        """
        condition = (
            (df["RSI_20"] < df["RSI_20"].shift(1)) &
            (df["RSI_3"] < 46.0) &
            (df["STOCHRSIk_14_14_3_3"] < 20.0) &
            (df["close"] < df["SMA_16"] * 0.956)
        )

        return condition
