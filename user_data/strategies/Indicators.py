import pandas_ta as ta
import pandas as pd
from pandas import DataFrame
import numpy as np



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

def calculate_willr(df: DataFrame, length: int) -> DataFrame:

    df[f"WILLR_{length}"] = ta.willr(df["high"], df["low"], df["close"], length=length)
    return df

def calculate_sma(df: DataFrame, length: int) -> DataFrame:

    df[f"SMA_{length}"] = ta.sma(df["close"], length=length)
    return df

def calculate_mfi(df: DataFrame, length: int) -> DataFrame:

    df[f"MFI_{length}"] = ta.mfi(df["high"], df["low"], df["close"], df["volume"], length=length)
    return df


def calculate_rolling_max(df: DataFrame, length: int, column: str = "close") -> DataFrame:

    df[f"{column}_max_{length}"] = df[column].rolling(length).max()
    return df

def calculate_adx(df: DataFrame, length: int = 14) -> DataFrame:

    adx = ta.adx(df["high"], df["low"], df["close"], length=length)
    df[f"ADX_{length}"] = adx[f"ADX_{length}"]
    return df


def add_indicators(df: DataFrame) -> DataFrame:

    #df = calculate_mfi(df, length=14)

    #df = calculate_willr(df, length=14)
    #df = calculate_rolling_max(df, length=48, column="close")


    return df
