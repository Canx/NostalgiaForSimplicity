from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


class NewtonSignal(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def get_plugin_tag(self) -> str:
        return "newton"

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on Bollinger Bands and RSI.
        """
        condition = (
            (df["close"] < df["EMA_200"]) &
            (df["RSI_14"] < 50) &
            (df["is_downtrend"] == False) &
            ((df["is_downtrend"]).shift(1) == False)
        )

        #(df["close"] > df["EMA_12"]) &
            #(df["EMA_12_acceleration"] > 0) &
            #(df["EMA_12_slope"] > 0) &
            #(df["close"] < df["EMA_50_slope"])
            #(df["EMA_26_slope"] > 0) &
            #             (df["EMA_50_slope"] < 0) &
            #(df["close"] > df["open"]) &
            #(df["is_downtrend"] == False) &
            #(df["RSI_14"] < 40) &
            #(df["EMA_12"] > df["EMA_26"]) &
            
            #(df["OBV"] > df["OBV_SMA"]*2) &
            #(df["close"] > df["EMA_200"]) &
        return condition
    
    def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate exit signal based on Bollinger Bands and additional indicators.
        """
        # Condition for scalping exit signal
        condition = (
            (df["RSI_14"] > 60) &
            #(df["close"] < df["EMA_9"]) &
            (df["close"] > df["EMA_200"]) &
            (df["downtrend_signals"] > 0)
            #(df["close"] < df["open"]) &
            
            #(df["ADX_14"] > 30)
            #(df["is_downtrend"] == True)
            
        )

        return condition
