import pandas_ta as ta
from SignalPlugin import SignalPlugin
import pandas as pd
import pandas_ta as pta
from pandas import DataFrame


class RSISignalPlugin(SignalPlugin):
    """
    RSI-based signal plugin.
    """

    def __init__(self, priority: int = 2):
        super().__init__(priority)

    def get_plugin_tag(self) -> str:
        return "RSI"

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add RSI indicators to the DataFrame if not already present, only if valid.
        """
        # Verificar si hay suficientes datos
        if len(dataframe) < 14:
            self.log.warning("Not enough data to calculate RSI. Skipping.")
            return dataframe

        # Verificar si hay valores NaN en la columna "close"
        if dataframe["close"].isna().any():
            self.log.warning("NaN values detected in 'close'. Skipping RSI calculation.")
            return dataframe

        dataframe["rsi"] = pta.rsi(dataframe["close"], length=14)
        self.log.info(f"RSI calculated and added to DataFrame: {dataframe['rsi'].head()}")

        return dataframe



    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate entry signal based on RSI. If an issue is detected, return a Series of False values.
        """
        if "rsi" not in dataframe.columns:
            self.log.warning("RSI column is missing in DataFrame. Returning false signals for all rows.")
            return pd.Series([False] * len(dataframe), index=dataframe.index)

        if dataframe["rsi"].isna().any():
            self.log.warning("NaN values detected in RSI. Returning false signals for all rows.")
            return pd.Series([False] * len(dataframe), index=dataframe.index)

        # Generar señal válida
        return dataframe["rsi"] < 30


    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate exit signal based on RSI. If an issue is detected, return a Series of False values.
        """
        if "rsi" not in dataframe.columns:
            self.log.warning("RSI column is missing in DataFrame. Returning false signals for all rows.")
            return pd.Series([False] * len(dataframe), index=dataframe.index)

        if dataframe["rsi"].isna().any():
            self.log.warning("NaN values detected in RSI. Returning false signals for all rows.")
            return pd.Series([False] * len(dataframe), index=dataframe.index)

        # Generar señal válida
        return dataframe["rsi"] > 70




