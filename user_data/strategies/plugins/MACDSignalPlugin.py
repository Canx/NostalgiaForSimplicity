import pandas_ta as ta
from SignalPlugin import SignalPlugin
from pandas import DataFrame
import pandas as pd


class MACDSignalPlugin(SignalPlugin):
    """
    MACD-based signal plugin.
    """

    def __init__(self, priority: int = 1):
        super().__init__(priority)

    def get_plugin_tag(self) -> str:
        return "MACD"

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add MACD indicators to the DataFrame if not already present.
        """
        # Verificar si hay suficientes datos
        if len(dataframe) < 26:  # 26 es el valor de 'slow'
            self.log.warning("Not enough data to calculate MACD. Skipping.")
            return dataframe

        # Manejar valores NaN en "close"
        if dataframe["close"].isna().any():
            self.log.warning("NaN values detected in 'close'. Filling NaN values.")
            dataframe["close"] = dataframe["close"].fillna(method="ffill").fillna(method="bfill")

        # Calcular MACD
        macd = ta.macd(dataframe["close"], fast=12, slow=26, signal=9)
        dataframe["macd"] = macd["MACD_12_26_9"]
        dataframe["macd_signal"] = macd["MACDs_12_26_9"]
        dataframe["macd_histogram"] = macd["MACDh_12_26_9"]

        # Verificar si MACD contiene valores NaN después del cálculo
        if dataframe["macd"].isna().any() or dataframe["macd_signal"].isna().any():
            self.log.warning("MACD or MACD Signal contains NaN values after calculation.")

        return dataframe

    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on MACD.
        """
        if "macd" not in dataframe.columns or "macd_signal" not in dataframe.columns:
            self.log.warning("MACD or MACD Signal column is missing. Returning false signals.")
            return pd.Series([False] * len(dataframe), index=dataframe.index)

        if dataframe["macd"].isna().any() or dataframe["macd_signal"].isna().any():
            self.log.warning("NaN values detected in MACD or MACD Signal. Returning false signals.")
            return pd.Series([False] * len(dataframe), index=dataframe.index)

        return dataframe["macd"] > dataframe["macd_signal"]

    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate exit signal based on MACD.
        """
        if "macd" not in dataframe.columns or "macd_signal" not in dataframe.columns:
            self.log.warning("MACD or MACD Signal column is missing. Returning false signals.")
            return pd.Series([False] * len(dataframe), index=dataframe.index)

        if dataframe["macd"].isna().any() or dataframe["macd_signal"].isna().any():
            self.log.warning("NaN values detected in MACD or MACD Signal. Returning false signals.")
            return pd.Series([False] * len(dataframe), index=dataframe.index)

        return dataframe["macd"] < dataframe["macd_signal"]



