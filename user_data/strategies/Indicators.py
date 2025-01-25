import pandas_ta as ta
import pandas as pd
from pandas import DataFrame
import numpy as np

def calculate_aroon(df: DataFrame, length: int) -> DataFrame:

    aroon = ta.aroon(df["high"], df["low"], length=length)
    if isinstance(aroon, pd.DataFrame):
        df[f"AROONU_{length}"] = aroon[f"AROONU_{length}"]
        df[f"AROOND_{length}"] = aroon[f"AROOND_{length}"]
    else:
        df[f"AROONU_{length}"] = np.nan
        df[f"AROOND_{length}"] = np.nan

    return df

def calculate_stochrsi(df: DataFrame) -> DataFrame:

    stochrsi = ta.stochrsi(df["close"])
    if isinstance(stochrsi, DataFrame):
        df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]
        df["STOCHRSId_14_14_3_3"] = stochrsi["STOCHRSId_14_14_3_3"]
    else:
        df["STOCHRSIk_14_14_3_3"] = np.nan
        df["STOCHRSId_14_14_3_3"] = np.nan

    # Calculate slopes
    df["STOCHRSIk_14_14_3_3_slope"] = df["STOCHRSIk_14_14_3_3"].diff() / df["STOCHRSIk_14_14_3_3"].shift()

    return df


def detect_divergences(dataframe: DataFrame) -> DataFrame:
    # Initialize divergence columns
    dataframe['hidden_bullish_div'] = 0
    dataframe['hidden_bearish_div'] = 0

    # Ensure the required columns exist
    if 'STOCHRSIk_14_14_3_3' not in dataframe.columns:
        raise ValueError("STOCHRSIk_14_14_3_3 column is missing. Make sure to calculate StochRSI before calling this function.")

    # Look for divergences in the last N candles
    for i in range(2, len(dataframe)):
        # Hidden Bullish Divergence
        if (dataframe['low'].iloc[i] < dataframe['low'].iloc[i-1] and  # Lower Low in price
            dataframe['STOCHRSIk_14_14_3_3'].iloc[i] > dataframe['STOCHRSIk_14_14_3_3'].iloc[i-1]):  # Higher Low in StochRSI
            dataframe.loc[i, 'hidden_bullish_div'] = 1

        # Hidden Bearish Divergence
        if (dataframe['high'].iloc[i] > dataframe['high'].iloc[i-1] and  # Higher High in price
            dataframe['STOCHRSIk_14_14_3_3'].iloc[i] < dataframe['STOCHRSIk_14_14_3_3'].iloc[i-1]):  # Lower High in StochRSI
            dataframe.loc[i, 'hidden_bearish_div'] = 1

    return dataframe


def calculate_bbands(df: DataFrame) -> DataFrame:

    bbands_20_2 = ta.bbands(df["close"], length=20, std=2)
    df["BBL_20_2.0"] = bbands_20_2["BBL_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBM_20_2.0"] = bbands_20_2["BBM_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBU_20_2.0"] = bbands_20_2["BBU_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBB_20_2.0"] = bbands_20_2["BBB_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBP_20_2.0"] = bbands_20_2["BBP_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan

    return df

def calculate_willr(df: DataFrame, length: int) -> DataFrame:

    df[f"WILLR_{length}"] = ta.willr(df["high"], df["low"], df["close"], length=length)
    return df

def calculate_rsi(df: DataFrame, length: int) -> DataFrame:

    df[f"RSI_{length}"] = ta.rsi(df["close"], length=length)
    return df

def calculate_sma(df: DataFrame, length: int) -> DataFrame:

    df[f"SMA_{length}"] = ta.sma(df["close"], length=length)
    return df

def calculate_mfi(df: DataFrame, length: int) -> DataFrame:

    df[f"MFI_{length}"] = ta.mfi(df["high"], df["low"], df["close"], df["volume"], length=length)
    return df

def calculate_ema(df: DataFrame, length: int) -> DataFrame:

    df[f"EMA_{length}"] = ta.ema(df["close"], length=length)
    return df

def calculate_rolling_max(df: DataFrame, length: int, column: str = "close") -> DataFrame:

    df[f"{column}_max_{length}"] = df[column].rolling(length).max()
    return df

def calculate_adx(df: DataFrame, length: int = 14) -> DataFrame:

    adx = ta.adx(df["high"], df["low"], df["close"], length=length)
    df[f"ADX_{length}"] = adx[f"ADX_{length}"]
    return df


def add_indicators(df: DataFrame) -> DataFrame:

    df = calculate_rsi(df, length=3)
    df = calculate_rsi(df, length=4)
    df = calculate_rsi(df, length=20)
    df = calculate_sma(df, length=16)
    df = calculate_rsi(df, length=14)
    df = calculate_mfi(df, length=14)
    df = calculate_ema(df, length=5)
    df = calculate_ema(df, length=9)
    df = calculate_ema(df, length=12)
    df = calculate_ema(df, length=20)
    df = calculate_ema(df, length=26)
    df = calculate_ema(df, length=50)
    df = calculate_ema(df, length=200)

    df = calculate_willr(df, length=14)
    df = calculate_rolling_max(df, length=48, column="close")

    df = calculate_aroon(df, length=14)

    df = calculate_stochrsi(df)

    #df = calculate_bbands(df)
    #df = calculate_adx(df, length=14)

    return df
