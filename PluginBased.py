import os
import importlib.util
from SignalPlugin import SignalPlugin
from pandas import DataFrame
from freqtrade.strategy.interface import IStrategy


class PluginBased(IStrategy):
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
        plugins = []
        plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")

        for file in os.listdir(plugin_dir):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                file_path = os.path.join(plugin_dir, file)

                # Dynamically import the module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Search for subclasses of SignalPlugin
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, SignalPlugin) and attr is not SignalPlugin:
                        plugins.append(attr())

        # Sort plugins by priority
        return sorted(plugins, key=lambda plugin: plugin.get_priority())



    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Callback to populate indicators for the strategy.
        """
        if dataframe.empty:
            self.log.warning("Received an empty DataFrame in populate_indicators. Skipping.")
            return dataframe

        # Lógica para indicadores, si el DataFrame no está vacío
        for plugin in self.plugins:
            dataframe = plugin.populate_indicators(dataframe, metadata)

        return dataframe



    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate entry signals based on plugin priority.
        """
        # Ensure the required columns exist
        if "enter_long" not in dataframe.columns:
            dataframe["enter_long"] = 0
        if "enter_tag" not in dataframe.columns:
            dataframe["enter_tag"] = ""

        # Iterate through plugins and apply entry signals
        for plugin in self.plugins:
            dataframe = plugin.populate_indicators(dataframe, metadata)
            entry_signal = plugin.entry_signal(dataframe, metadata)

            # Apply the entry signal if found
            if entry_signal.any():
                dataframe.loc[entry_signal, "enter_long"] = 1
                dataframe.loc[entry_signal, "enter_tag"] = plugin.get_plugin_tag()
                break  # Stop after the first plugin generates a signal

        return dataframe



    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Filter exit signals based on the enter_tag.
        """
        for plugin in self.plugins:
            dataframe = plugin.exit_signal(dataframe, metadata)
        return dataframe
