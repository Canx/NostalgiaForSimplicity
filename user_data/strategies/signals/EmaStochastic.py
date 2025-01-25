from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


class EmaStochastic(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        condition = (
            #(df["STOCHRSIk_14_14_3_3_slope"] > 0)
            #& (df["STOCHRSIk_14_14_3_3_slope"].shift(1) < 0)
            (df["falling_knife"] == False)
            #& (df["is_downtrend"] == False)
            #& (df["is_downtrend"].shift(1) == False)
            & (df["EMA_9_acceleration"] > 0)
            & (df["EMA_5_slope"] > 0)
            & (df["STOCHRSIk_14_14_3_3"] < 50)
            #& (df["OBV"] > df["OBV_SMA"])
            #& (df["EMA_50_slope"] > 0)
            #& (df["EMA_12_slope"].shift(1) < 0)
            #& (df["EMA_5_slope"] > df["EMA_200_slope"])
            
            #& (df["falling_knife"].shift(1) == True)
            #
            
            #& (df["close"] < df["EMA_200"]) &
            
        )

        return condition
    
    def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        condition = (
            (df["falling_knife"] == True)
        )

        return condition
        
