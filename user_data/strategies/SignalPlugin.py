from pandas import DataFrame
import pandas as pd
import logging


class SignalPlugin:
    """
    Base class for all signal plugins. Allows plugins to implement only the required methods.
    """

    def __init__(self, priority: int = 0, enabled: bool = True):
        """
        Initialize the plugin with a priority value and enabled state.
        :param priority: Lower values indicate higher priority. Default is 0.
        :param enabled: Whether the plugin is enabled or not. Default is True.
        """
        self.priority = priority
        self.enabled = enabled  # Estado de activación/desactivación del plugin
        self.log = logging.getLogger(__name__)

    def get_priority(self) -> int:
        """
        Returns the priority of the plugin.
        """
        return self.priority

    def is_enabled(self) -> bool:
        """
        Returns whether the plugin is enabled.
        """
        return self.enabled

    def set_enabled(self, enabled: bool):
        """
        Enable or disable the plugin.
        """
        self.enabled = enabled
        state = "enabled" if enabled else "disabled"
        self.log.info(f"Plugin {self.get_plugin_tag()} has been {state}.")

    def get_plugin_tag(self) -> str:
        """
        Returns the unique tag for the plugin.
        """
        return self.__class__.__name__

    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signals based on plugin-specific logic. Default returns False for all rows.
        """
        self.log.debug(f"Plugin {self.get_plugin_tag()} does not implement entry_signal.")
        return pd.Series(False, index=dataframe.index)

    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate exit signals based on plugin-specific logic. Default returns False for all rows.
        """
        self.log.debug(f"Plugin {self.get_plugin_tag()} does not implement exit_signal.")
        return pd.Series(False, index=dataframe.index)

