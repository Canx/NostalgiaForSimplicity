import pandas_ta as ta
from SignalPlugin import SignalPlugin
from pandas import DataFrame


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
        if "macd" not in dataframe.columns or "macd_signal" not in dataframe.columns:
            macd = ta.macd(dataframe["close"], fast=12, slow=26, signal=9)
            dataframe["macd"] = macd["MACD_12_26_9"]
            dataframe["macd_signal"] = macd["MACDs_12_26_9"]
            dataframe["macd_histogram"] = macd["MACDh_12_26_9"]
        return dataframe

    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe["macd"] > dataframe["macd_signal"]

    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe["macd"] < dataframe["macd_signal"]


