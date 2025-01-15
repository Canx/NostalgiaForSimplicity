from abc import ABC, abstractmethod
from pandas import DataFrame


class SignalPlugin(ABC):
    """
    Abstract base class for all signal plugins.
    """

    def __init__(self, priority: int = 0):
        """
        Initialize the plugin with a priority value.
        :param priority: Lower values indicate higher priority. Default is 0.
        """
        self.priority = priority

    def get_priority(self) -> int:
        """
        Returns the priority of the plugin.
        """
        return self.priority

    @abstractmethod
    def get_plugin_tag(self) -> str:
        """
        Returns the unique tag for the plugin.
        """
        pass

    @abstractmethod
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate and add required indicators to the DataFrame.
        """
        pass

    @abstractmethod
    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate entry signals based on plugin-specific logic.
        """
        pass

    @abstractmethod
    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate exit signals based on plugin-specific logic.
        """
        pass


