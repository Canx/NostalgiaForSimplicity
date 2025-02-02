from freqtrade.strategy import IStrategy
from freqtrade.persistence import Trade
from datetime import datetime
from pandas import DataFrame
import pandas as pd
import logging


class Signal:
    """
    Base class for all signals.
    """

    def __init__(self, priority: int = 0, enabled: bool = True):
        """
        Initialize the signal with a priority value and enabled state.
        :param priority: Lower values indicate higher priority. Default is 0.
        :param enabled: Whether the plugin is enabled or not. Default is True.
        """
        self.priority = priority
        self.enabled = enabled  # Estado de activación/desactivación del plugin
        self.log = logging.getLogger(__name__)

    def config_strategy(self, strat: IStrategy):
        pass
    
    def get_priority(self) -> int:
        """
        Returns the priority of the signal.
        """
        return self.priority

    def is_enabled(self) -> bool:
        """
        Returns whether the signal is enabled.
        """
        return self.enabled

    def set_enabled(self, enabled: bool):
        """
        Enable or disable the signal.
        """
        self.enabled = enabled
        state = "enabled" if enabled else "disabled"
        self.log.info(f"Signal {self.get_signal_tag()} has been {state}.")

    def get_signal_tag(self) -> str:
        """
        Returns the unique tag for the signal.
        """
        return self.__class__.__name__

    def populate_indicators(self, dataframe):
        return dataframe

    def populate_indicators_15m(self, dataframe):
        return dataframe
    
    def populate_indicators_1h(self, dataframe):
        return dataframe
    
    def populate_indicators_4h(self, dataframe):
        return dataframe
    

    def entry_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        self.log.debug(f"Plugin {self.get_signal_tag()} does not implement entry_signal.")
        return pd.Series(False, index=dataframe.index)

    def exit_signal(self, dataframe: DataFrame, metadata: dict) -> pd.Series:
        self.log.debug(f"Plugin {self.get_signal_tag()} does not implement exit_signal.")
        return pd.Series(False, index=dataframe.index)
    

    def custom_exit(self, strategy: IStrategy, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                    current_profit: float, **kwargs):
        """
        Called for open trade every throttling iteration (roughly every 5 seconds).
        """
        self.log.debug(f"Plugin {self.get_signal_tag()} does not implement custom_exit..")
        return False
    

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime, current_rate: float, 
                        current_profit: float, **kwargs) -> float:
        self.log.debug(f"Plugin {self.get_signal_tag()} does not implement custom_stoploss..")
        return None

