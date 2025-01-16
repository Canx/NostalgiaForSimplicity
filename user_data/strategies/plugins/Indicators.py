import pandas_ta as ta
from SignalPlugin import SignalPlugin
from pandas import DataFrame
import pandas as pd
import numpy as np

# Long 6 entry signal
class Indicators(SignalPlugin):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

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