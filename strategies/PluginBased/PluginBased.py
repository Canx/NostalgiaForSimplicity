class PluginBasedStrategy(IStrategy):
    """
    Strategy managing multiple plugins with priority-based entry and exit signals.
    """

    INTERFACE_VERSION = 3
    minimal_roi = {"0": 0.1}
    stoploss = -0.1
    timeframe = "5m"

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.plugins = self.load_plugins()

    def load_plugins(self):
        """
        Dynamically load and sort plugins by priority.
        """
        # Load plugins
        plugins = [RSISignalPlugin(), MACDSignalPlugin()]
        # Sort plugins by priority (lower is higher priority)
        return sorted(plugins, key=lambda plugin: plugin.get_priority())

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populate indicators for all plugins.
        """
        for plugin in self.plugins:
            dataframe = plugin.populate_indicators(dataframe, metadata)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate a single entry signal based on plugin priority.
        """
        dataframe["enter_long"] = 0
        dataframe["enter_tag"] = ""
        for plugin in self.plugins:
            dataframe = plugin.generate_entry_signals(dataframe, metadata)
            if dataframe["enter_long"].any():
                break  # Stop after the first valid entry signal
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Filter exit signals based on the enter_tag.
        """
        for plugin in self.plugins:
            dataframe = plugin.generate_exit_signals(dataframe, metadata)
        return dataframe
