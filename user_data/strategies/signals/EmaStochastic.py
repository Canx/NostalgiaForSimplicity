from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


class EmaStochastic(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        buy_after_knive = (
            #(df["STOCHRSIk_14_14_3_3_slope"] > 0)
            #& (df["STOCHRSIk_14_14_3_3_slope"].shift(1) < 0)
            (df["falling_knife"] == False)
            #& (df["falling_knife"].shift(1) == True)
            #& (df["is_downtrend"] == False)
            #& (df["is_downtrend"].shift(1) == True)
            & (df["EMA_9_acceleration"] > 0)
            & (df["EMA_5_slope"] > 0)
            & ((df["prev_close_before_falling_knife"] - df["close"]) / df["prev_close_before_falling_knife"] > 0.019  # Baja > 1.9%
        )
            #& (df["STOCHRSIk_14_14_3_3"] < 50)
            #& (df["OBV"] > df["OBV_SMA"])
            #& (df["EMA_50_slope"] > 0)
            #& (df["EMA_12_slope"].shift(1) < 0)
            #& (df["EMA_5_slope"] > df["EMA_200_slope"])
            
            #& (df["falling_knife"].shift(1) == True)
            #
            
            #& (df["close"] < df["EMA_200"]) &
            
        )

        buy_after_downtrend = (
            (df["end_of_downtrend"] == True)
        )

        return buy_after_downtrend #| buy_after_knife
    
    # def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
    #     condition = (
    #         (df["falling_knife"] == True)
    #     )

    #     return condition
        
