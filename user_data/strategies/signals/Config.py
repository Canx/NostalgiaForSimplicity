from Signal import Signal
from freqtrade.strategy import IStrategy
import logging


class Config(Signal):
    """
    Dynamic config
    """

    def __init__(self, priority: int = 0):
        super().__init__(priority, enabled=True)


    def config_strategy(self, strat: IStrategy):
        strat.protections = [
        {
            "method": "LowProfitPairs",
            "lookback_period_candles": 60,
            "trade_limit": 1,
            "stop_duration": 60,
            "required_profit": -0.01
        },
        {
            "method": "CooldownPeriod",
            "stop_duration_candles": 2
        }
        ]

        strat.order_types = {
            'buy': 'market',
            'sell': 'limit',
            'force_entry': 'market',
            'force_exit': 'market',
            'trailing_stop_loss': 'limit',
            'stoploss': 'limit',
            'stoploss_on_exchange': False
        }

        #strat.stoploss = -0.0189
        strat.stoploss = -0.01

        # Trailing stoploss
        strat.trailing_stop = True
        strat.trailing_only_offset_is_reached = False
        #strat.trailing_stop_positive = 0.001
        #strat.trailing_stop_positive_offset = 0.015
        strat.use_custom_stoploss = False
        
        strat.timeframe = "5m"
        strat.startup_candle_count = 300

        strat.process_only_new_candles = True