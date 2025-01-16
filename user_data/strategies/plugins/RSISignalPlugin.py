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
        super().__init__(priority, enabled=False)

    def get_plugin_tag(self) -> str:
        return "RSI"

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Add RSI indicators to the DataFrame if not already present, only if valid.
        """
        # # Verificar si hay suficientes datos
        # if len(dataframe) < 14:
        #     self.log.warning("Not enough data to calculate RSI. Skipping.")
        #     return dataframe

        # # Verificar si hay valores NaN en la columna "close"
        # if dataframe["close"].isna().any():
        #     self.log.warning("NaN values detected in 'close'. Skipping RSI calculation.")
        #     return dataframe

        # Calcular RSI
        dataframe["rsi"] = pta.rsi(dataframe["close"], length=14)

        # # Contar valores NaN en la columna "rsi"
        # nan_count = dataframe["rsi"].isna().sum()
        # if nan_count > 0:
        #     self.log.warning(f"{nan_count} NaN values detected in 'rsi' after calculation.")
        # else:
        #     self.log.info(f"RSI calculated successfully with no NaN values. Example values: {dataframe['rsi'].head()}")

        return dataframe




    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on RSI. Returns a boolean Series aligned with the DataFrame index.
        """
        # Verificar si existe la columna 'rsi'
        if "rsi" not in dataframe.columns:
            self.log.warning("RSI column is missing in DataFrame. Returning false signals for all rows.")
            return pd.Series(False, index=dataframe.index)

        # Generar señales booleanas (RSI < 30)
        return (dataframe["rsi"] < 30).fillna(False)



    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate exit signal based on RSI. Returns a boolean Series aligned with the DataFrame index.
        """
        # Verificar si existe la columna 'rsi'
        if "rsi" not in dataframe.columns:
            self.log.warning("RSI column is missing in DataFrame. Returning false signals for all rows.")
            return pd.Series(False, index=dataframe.index)

        # Generar señales booleanas (RSI > 70)
        return (dataframe["rsi"] > 70).fillna(False)






