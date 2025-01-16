import pandas_ta as ta
from SignalPlugin import SignalPlugin
from pandas import DataFrame
import pandas as pd


class MACDSignalPlugin(SignalPlugin):
    """
    MACD-based signal plugin.
    """

    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=False)

    def get_plugin_tag(self) -> str:
        return "MACD"

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add MACD indicators to the DataFrame if not already present.
        """
        if "macd" not in dataframe.columns or "macd_signal" not in dataframe.columns:
            # Calcular MACD
            macd = ta.macd(dataframe["close"], fast=12, slow=26, signal=9)
            dataframe["macd"] = macd["MACD_12_26_9"]
            dataframe["macd_signal"] = macd["MACDs_12_26_9"]
            dataframe["macd_histogram"] = macd["MACDh_12_26_9"]

        return dataframe


    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on MACD.
        """
        # Verificar si las columnas necesarias existen
        if "macd" not in dataframe.columns or "macd_signal" not in dataframe.columns:
            self.log.warning("MACD or MACD Signal column is missing. Returning false signals.")
            return pd.Series(False, index=dataframe.index)

        # Generar señales booleanas
        return dataframe["macd"] > dataframe["macd_signal"]


    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate exit signal based on MACD.
        """
        # Verificar si las columnas necesarias existen
        if "macd" not in dataframe.columns or "macd_signal" not in dataframe.columns:
            self.log.warning("MACD or MACD Signal column is missing. Returning false signals.")
            return pd.Series(False, index=dataframe.index)

        # Generar señales booleanas
        return dataframe["macd"] < dataframe["macd_signal"]




