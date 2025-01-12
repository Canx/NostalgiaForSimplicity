from SignalPlugin import SignalPlugin


class RSISignalPlugin(SignalPlugin):
    """
    RSI-based signal plugin.
    """

    def get_plugin_tag(self) -> str:
        """
        Returns the unique tag for this plugin.
        """
        return "RSI"

    def get_priority(self) -> int:
        """
        Returns the priority of this plugin.
        """
        return 1

    def required_indicators(self) -> set:
        """
        Returns the RSI indicator name.
        """
        return {"rsi"}

    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate entry signal based on RSI < 30.
        """
        return dataframe["rsi"] < 30

    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate exit signal based on RSI > 70.
        """
        return dataframe["rsi"] > 70




