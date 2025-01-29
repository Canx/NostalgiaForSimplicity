from Signal import Signal
from pandas import DataFrame
import pandas as pd


class NewtonSignal(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def get_plugin_tag(self) -> str:
        return "newton"

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        """
        Generate entry signal based on EMA, RSI and (not) downtrend signals
        """
        condition = (
            (df["close"] < df["EMA_200"]) &
            (df["close"] < df["EMA_12"]) &
            (df["close"] > df["open"]) &
            (df["close"].shift(1) < df["open"].shift(1)) & # Vela anterior era roja
            
            # Cuerpo de la vela anterior era más pequeña que la actual
            (abs(df["close"].shift(1) - df["open"].shift(1)) < abs(df["close"] - df["open"])) &
            (df["EMA_12_acceleration"] > 0) &
            (df["EMA_26_acceleration"] > 0) &
            (df["EMA_12"] < df["EMA_26"])

            

            # TODO: Comprobar que la EMA_12 y la EMA_26 están separandose


            #(df["RSI_14"] < 60)
            #(df["is_downtrend"] == True)
            #(df["close"] > df["EMA_12"]) &
            #(df["high"] > df["EMA_26"]) &
            #(df["EMA_50_slope"] > 0) &
            
            
            #(df["downtrend_signals"] >= 1)
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
