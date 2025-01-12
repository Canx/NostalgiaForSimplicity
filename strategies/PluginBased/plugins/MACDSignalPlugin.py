from SignalPlugin import SignalPlugin


class MACDSignalPlugin(SignalPlugin):
    """
    MACD-based signal plugin.
    """

    def get_plugin_tag(self) -> str:
        """
        Returns the unique tag for this plugin.
        """
        return "MACD"

    def get_priority(self) -> int:
        """
        Returns the priority of this plugin.
        """
        return 2

    def required_indicators(self) -> set:
        """
        Returns the MACD indicator name.
        """
        return {"macd"}

    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate entry signal based on MACD crossover.
        """
        return dataframe["macd"] > dataframe["macd_signal"]

    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate exit signal based on MACD divergence.
        """
        return dataframe["macd"] < dataframe["macd_signal"]
