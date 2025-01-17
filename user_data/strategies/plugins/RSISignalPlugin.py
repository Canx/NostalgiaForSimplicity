from SignalPlugin import SignalPlugin
import pandas as pd
from pandas import DataFrame


class RSISignalPlugin(SignalPlugin):
    """
    RSI-based signal plugin.
    """

    def __init__(self, priority: int = 2):
        super().__init__(priority, enabled=False)

    def get_plugin_tag(self) -> str:
        return "RSI"

    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on RSI. Returns a boolean Series aligned with the DataFrame index.
        """
        return (dataframe["rsi"] < 30)

    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate exit signal based on RSI. Returns a boolean Series aligned with the DataFrame index.
        """
        return (dataframe["rsi"] > 70)






