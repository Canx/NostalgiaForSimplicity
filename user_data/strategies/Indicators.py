import pandas_ta as ta
import pandas as pd
import numpy as np

def calculate_aroon(df: pd.DataFrame, length: int) -> pd.DataFrame:
    """
    Calcula el indicador Aroon.
    """
    aroon = ta.aroon(df["high"], df["low"], length=length)
    if isinstance(aroon, pd.DataFrame):
        df[f"AROONU_{length}"] = aroon[f"AROONU_{length}"]
        df[f"AROOND_{length}"] = aroon[f"AROOND_{length}"]
    else:
        df[f"AROONU_{length}"] = np.nan
        df[f"AROOND_{length}"] = np.nan

    return df

def calculate_stochrsi(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el indicador Stochastic RSI.
    """
    stochrsi = ta.stochrsi(df["close"])
    if isinstance(stochrsi, pd.DataFrame):
        df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]
        df["STOCHRSId_14_14_3_3"] = stochrsi["STOCHRSId_14_14_3_3"]
    else:
        df["STOCHRSIk_14_14_3_3"] = np.nan
        df["STOCHRSId_14_14_3_3"] = np.nan

    return df

def calculate_bbands(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula las Bandas de Bollinger (BBands).
    """
    bbands_20_2 = ta.bbands(df["close"], length=20, std=2)
    df["BBL_20_2.0"] = bbands_20_2["BBL_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBM_20_2.0"] = bbands_20_2["BBM_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBU_20_2.0"] = bbands_20_2["BBU_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBB_20_2.0"] = bbands_20_2["BBB_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBP_20_2.0"] = bbands_20_2["BBP_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan

    return df

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega todos los indicadores necesarios al DataFrame.
    """
    df["RSI_3"] = ta.rsi(df["close"], length=3)
    df["RSI_4"] = ta.rsi(df["close"], length=4)
    df["RSI_20"] = ta.rsi(df["close"], length=20)
    df["SMA_16"] = ta.sma(df["close"], length=16)
    df["RSI_14"] = ta.rsi(df["close"], length=14)
    df["MFI_14"] = ta.mfi(df["high"], df["low"], df["close"], df["volume"], length=14)
    df["EMA_9"] = ta.ema(df["close"], length=9)
    df["EMA_12"] = ta.ema(df["close"], length=12)
    df["EMA_20"] = ta.ema(df["close"], length=20)
    df["EMA_26"] = ta.ema(df["close"], length=26)
    df["WILLR_14"] = ta.willr(df["high"], df["low"], df["close"], length=14)
    df["close_max_48"] = df["close"].rolling(48).max()

    df = calculate_aroon(df, length=14)
    df = calculate_stochrsi(df)
    df = calculate_bbands(df)

    return df
