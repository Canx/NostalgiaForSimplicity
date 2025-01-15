import pandas_ta as ta
from SignalPlugin import SignalPlugin
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
        Add RSI indicators to the DataFrame if not already present.
        """
        if "rsi" not in dataframe.columns:
            dataframe["rsi"] = ta.rsi(dataframe["close"], length=14)
        return dataframe

    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe["rsi"] < 30

    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        return dataframe["rsi"] > 70

