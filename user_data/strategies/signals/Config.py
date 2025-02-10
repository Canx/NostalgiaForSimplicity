from Signal import Signal
from freqtrade.strategy import IStrategy
import logging


class Config(Signal):
    """
    Dynamic config
    """

    def init(self):
        self.priority = 0
        self.enabled = True

        self.strat.protections = [
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

        self.strat.order_types = {
            'entry': 'limit',
            'exit': 'limit',
            'force_entry': 'market',
            'force_exit': 'market',
            'trailing_stop_loss': 'limit',
            'stoploss': 'market',
            'stoploss_on_exchange': False
        }

        self.strat.stoploss = -0.25  # Stop-loss en -25%
    
        # Trailing stoploss
        self.strat.trailing_stop = False  
        #strat.trailing_stop_positive = 0.01  # Activa trailing stop al +1%
        #strat.trailing_stop_positive_offset = 0.015  # Se activa cuando el precio sube al 1.5%
        #strat.trailing_only_offset_is_reached = True  # Solo activa trailing si alcanza offset
        self.strat.use_custom_stoploss = True

        # Adjust trade position
        self.strat.position_adjustment_enable = True
        
        self.strat.timeframe = "5m"
        self.strat.startup_candle_count = 300

        self.strat.process_only_new_candles = True