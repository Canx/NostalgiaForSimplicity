from abc import ABC, abstractmethod
from pandas import DataFrame
import pandas_ta as ta


class SignalPlugin(ABC):
    """
    Abstract base class for all signal plugins, with built-in priority and indicator management.
    """

    # Predefined mapping of indicator names to their calculation functions
    indicator_functions = {
        "rsi": lambda df: ta.rsi(df["close"], length=14),
        "macd": lambda df: ta.macd(df["close"], fast=12, slow=26, signal=9),
    }

    @abstractmethod
    def get_plugin_tag(self) -> str:
        """
        Returns the unique tag for the plugin.
        """
        pass

    @abstractmethod
    def get_priority(self) -> int:
        """
        Returns the priority of the plugin.
        Lower numbers indicate higher priority.
        """
        pass

    @abstractmethod
    def required_indicators(self) -> set:
        """
        Returns a set of required indicator names for the plugin.
        Example: {"rsi", "macd"}
        """
        pass

    @abstractmethod
    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Plugin-specific logic for generating entry signals.
        """
        pass

    @abstractmethod
    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Plugin-specific logic for generating exit signals.
        """
        pass

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds required indicators to the DataFrame if not already present.
        """
        for indicator_name in self.required_indicators():
            if indicator_name not in dataframe.columns:
                calc_function = self.indicator_functions.get(indicator_name)
                if not calc_function:
                    raise ValueError(f"Unknown indicator: {indicator_name}")
                indicator_data = calc_function(dataframe)
                if isinstance(indicator_data, DataFrame):
                    # Add multiple columns (e.g., MACD with multiple outputs)
                    for col in indicator_data.columns:
                        dataframe[col] = indicator_data[col]
                else:
                    # Add single column indicator
                    dataframe[indicator_name] = indicator_data
        return dataframe

    def generate_entry_signals(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate entry signals and add the plugin's tag to the 'enter_tag' column.
        """
        signal = self.entry_signal(dataframe, metadata)
        dataframe["enter_long"] |= signal
        dataframe.loc[signal, "enter_tag"] = (
            dataframe.loc[signal, "enter_tag"].astype(str) + f",{self.get_plugin_tag()}"
        ).str.strip(",")
        return dataframe

    def generate_exit_signals(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate exit signals and filter them based on the enter_tag.
        """
        signal = self.exit_signal(dataframe, metadata)
        dataframe["exit_long"] = dataframe["enter_tag"] == self.get_plugin_tag()
        dataframe["exit_long"] &= signal
        return dataframe

