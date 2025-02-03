from Signal import Signal
import pandas as pd
from pandas import DataFrame
import pandas_ta as ta


class BollingerBands(Signal):
    def __init__(self, priority: int = 2):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        
        bbands_20_2 = ta.bbands(df["close"], length=20, std=2)
        
        df["BBL_20_2.0"] = bbands_20_2["BBL_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
        df["BBM_20_2.0"] = bbands_20_2["BBM_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
        df["BBU_20_2.0"] = bbands_20_2["BBU_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
        df["BBB_20_2.0"] = bbands_20_2["BBB_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
        df["BBP_20_2.0"] = bbands_20_2["BBP_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan

        df["BB_WIDTH_20_2.0"] = ((df["BBU_20_2.0"] - df["BBL_20_2.0"]) / df["BBM_20_2.0"]) * 10

        df["price_over_bbu"] = (
            (df['close'] >= df['BBU_20_2.0'])
            # & (df['close'].shift(1) < df['BBU_20_2.0'])
            )
        
        df["bb_buy"] = (
            (df['low'] < df['BBL_20_2.0']) &
            (df['high'].shift(1) > df['BBL_20_2.0'])  # La vela anterior estaba dentro
            & (df['RSI_3'] < 25)
            & (df["BB_WIDTH_20_2.0"] > 0.10)  # Confirmación de sobreventa
        )

        return df