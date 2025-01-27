from signals.Signal import Signal
from pandas import DataFrame
import pandas as pd


class TrendSignal(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df["uptrend_start"])
            & (df["range_pct"] - 0.15 > df["avg_range_pct"])
            & (df["downtrend_start"].shift(1) == False)  # La vela anterior
            & (df["downtrend_start"].shift(2) == False)  # 2 velas atrás
            & (df["downtrend_start"].shift(3) == False)  # 3 velas atrás
            & (df["downtrend_start"].shift(4) == False)  # 4 velas atrás
            & (df["downtrend_start"].shift(5) == False)  # 5 velas atrás
            & (df["downtrend_start"].shift(6) == False)  # 6 velas atrás
        )   
    
    #def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
    #    return df["downtrend_start"]