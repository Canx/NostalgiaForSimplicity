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
            "required_profit": -0.05
        },
        {
            "method": "CooldownPeriod",
            "stop_duration_candles": 2
        }
        ]

        strat.order_types = {
            'buy': 'limit',
            'sell': 'limit',
            'trailing_stop_loss': 'limit',
            'stoploss': 'limit',
            'stoploss_on_exchange': False
        }

        strat.minimal_roi = {
            "0": 0.15,
            "5": 0.10,
            "10": 0.08,
            "15": 0.07,
            "20": 0.06,
            "30": 0.05,
            "60": 0.04,
            "120": 0.03,
            "180": 0.02,
            "210": 0.01,
            "240": 0.005
        }

        #strat.stoploss = -0.0189
        strat.stoploss = -0.05

        # Trailing stoploss
        strat.trailing_stop = True
        strat.trailing_only_offset_is_reached = False
        #strat.trailing_stop_positive = 0.001
        #strat.trailing_stop_positive_offset = 0.015
        strat.use_custom_stoploss = False
        
        strat.timeframe = "5m"
        strat.startup_candle_count = 300

        strat.process_only_new_candles = True