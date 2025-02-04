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
            "stop_duration_candles": 5
        }
        ]

        strat.order_types = {
            'entry': 'limit',
            'exit': 'limit',
            'force_entry': 'market',
            'force_exit': 'market',
            'trailing_stop_loss': 'limit',
            'stoploss': 'market',
            'stoploss_on_exchange': False
        }

        strat.stoploss = -0.02  # Stop-loss en -1%
    
        # Trailing stoploss
        strat.trailing_stop = True  
        strat.trailing_stop_positive = 0.01  # Activa trailing stop al +1%
        strat.trailing_stop_positive_offset = 0.015  # Se activa cuando el precio sube al 1.5%
        strat.trailing_only_offset_is_reached = True  # Solo activa trailing si alcanza offset
        strat.use_custom_stoploss = True

        
        strat.timeframe = "5m"
        strat.startup_candle_count = 300

        strat.process_only_new_candles = True

        # call parent Signal
        super().config_strategy(strat)