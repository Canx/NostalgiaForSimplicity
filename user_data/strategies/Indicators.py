import pandas_ta as ta
import pandas as pd
import numpy as np

def calculate_aroon(df: pd.DataFrame, length: int) -> pd.DataFrame:

    aroon = ta.aroon(df["high"], df["low"], length=length)
    if isinstance(aroon, pd.DataFrame):
        df[f"AROONU_{length}"] = aroon[f"AROONU_{length}"]
        df[f"AROOND_{length}"] = aroon[f"AROOND_{length}"]
    else:
        df[f"AROONU_{length}"] = np.nan
        df[f"AROOND_{length}"] = np.nan

    return df

def calculate_stochrsi(df: pd.DataFrame) -> pd.DataFrame:

    stochrsi = ta.stochrsi(df["close"])
    if isinstance(stochrsi, pd.DataFrame):
        df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]
        df["STOCHRSId_14_14_3_3"] = stochrsi["STOCHRSId_14_14_3_3"]
    else:
        df["STOCHRSIk_14_14_3_3"] = np.nan
        df["STOCHRSId_14_14_3_3"] = np.nan

    return df

def calculate_bbands(df: pd.DataFrame) -> pd.DataFrame:

    bbands_20_2 = ta.bbands(df["close"], length=20, std=2)
    df["BBL_20_2.0"] = bbands_20_2["BBL_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBM_20_2.0"] = bbands_20_2["BBM_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBU_20_2.0"] = bbands_20_2["BBU_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBB_20_2.0"] = bbands_20_2["BBB_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan
    df["BBP_20_2.0"] = bbands_20_2["BBP_20_2.0"] if isinstance(bbands_20_2, pd.DataFrame) else np.nan

    return df

def calculate_willr(df: pd.DataFrame, length: int) -> pd.DataFrame:

    df[f"WILLR_{length}"] = ta.willr(df["high"], df["low"], df["close"], length=length)
    return df

def calculate_rsi(df: pd.DataFrame, length: int) -> pd.DataFrame:

    df[f"RSI_{length}"] = ta.rsi(df["close"], length=length)
    return df

def calculate_sma(df: pd.DataFrame, length: int) -> pd.DataFrame:

    df[f"SMA_{length}"] = ta.sma(df["close"], length=length)
    return df

def calculate_mfi(df: pd.DataFrame, length: int) -> pd.DataFrame:

    df[f"MFI_{length}"] = ta.mfi(df["high"], df["low"], df["close"], df["volume"], length=length)
    return df

def calculate_ema(df: pd.DataFrame, length: int) -> pd.DataFrame:

    df[f"EMA_{length}"] = ta.ema(df["close"], length=length)
    return df

def calculate_rolling_max(df: pd.DataFrame, length: int, column: str = "close") -> pd.DataFrame:

    df[f"{column}_max_{length}"] = df[column].rolling(length).max()
    return df

def calculate_adx(df: pd.DataFrame, length: int = 14) -> pd.DataFrame:

    adx = ta.adx(df["high"], df["low"], df["close"], length=length)
    df[f"ADX_{length}"] = adx[f"ADX_{length}"]
    return df


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:

    df = calculate_rsi(df, length=3)
    df = calculate_rsi(df, length=4)
    df = calculate_rsi(df, length=20)
    df = calculate_sma(df, length=16)
    df = calculate_rsi(df, length=14)
    df = calculate_mfi(df, length=14)
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
    df = calculate_bbands(df)
    df = calculate_adx(df, length=14)
    df = calculate_is_downtrend(df)

    return df


def calculate_ema_slope(df: pd.DataFrame, length: int) -> pd.Series:

    ema = ta.ema(df['close'], length=length)
    return ema.diff()


def calculate_is_downtrend(df: pd.DataFrame) -> pd.DataFrame:

    # slope (1st derivative)
    df['EMA_12_slope'] = df['EMA_12'].diff() / df["EMA_12"].shift()
    df['EMA_26_slope'] = df['EMA_26'].diff() / df["EMA_26"].shift()
    df['EMA_50_slope'] = df['EMA_50'].diff() / df["EMA_50"].shift()
    df['EMA_200_slope'] = df['EMA_200'].diff() / df["EMA_200"].shift()

    # acceleration (2nd derivative)
    df['EMA_12_acceleration'] = df['EMA_12_slope'].diff()
    df['EMA_26_acceleration'] = df['EMA_26_slope'].diff()
    df['EMA_50_acceleration'] = df['EMA_50_slope'].diff()
    df['EMA_200_acceleration'] = df['EMA_200_slope'].diff()

    # Volume average
    df['OBV'] = ta.obv(df['close'], df['volume'])
    df['OBV_SMA'] = df['OBV'].rolling(10).mean()

    # Initialize the 'downtrend_signals' column with zeros
    df['downtrend_signals'] = 0

    # Defines a threshold to consider a downtrend
    threshold = 7

    # Increase downtrend signals based on conditions (ordered from more to less reactive)
    df['downtrend_signals'] += (df["close"] < df['EMA_12']).astype(int)
    df['downtrend_signals'] += (df["close"] < df['EMA_26']).astype(int)
    df['downtrend_signals'] += (df["close"] < df['EMA_50']).astype(int)
    df['downtrend_signals'] += (df["close"] < df['EMA_200']).astype(int)
    df['downtrend_signals'] += (df['OBV'] < df['OBV_SMA']).astype(int)
    df['downtrend_signals'] += (df['EMA_12_slope'] < 0).astype(int)
    #df['downtrend_signals'] += (df["BBB_20_2.0"] > 0.25).astype(int)
    df['downtrend_signals'] += (df["EMA_26_slope"] < 0).astype(int)
    df['downtrend_signals'] += (df["EMA_50_slope"] < 0).astype(int)
    df['downtrend_signals'] += (df["EMA_200_slope"] < 0).astype(int)
    df['downtrend_signals'] += ((df["EMA_200_slope"] < 0) & (df["EMA_200_acceleration"] < 0)).astype(int) * 2
    df['downtrend_signals'] += (df['EMA_12_acceleration'] < 0).astype(int)
    df['downtrend_signals'] += (df['EMA_26_acceleration'] < 0).astype(int)
    df['downtrend_signals'] += (df['EMA_200_acceleration'] < 0).astype(int)
    df['downtrend_signals'] += (df['EMA_50_acceleration'] < 0).astype(int)

    # Las cortas por debajo de las largas
    df['downtrend_signals'] += (df['EMA_50'] < df['EMA_200']).astype(int)
    df['downtrend_signals'] += (df['EMA_12'] < df['EMA_26']).astype(int)
    #df['downtrend_signals'] += (df['EMA_12_slope'] < df['EMA_26_slope']).astype(int)
    #df['downtrend_signals'] += (df['close'] < df['EMA_50']).astype(int)
    #df['downtrend_signals'] += (df['close'] < df['EMA_200']).astype(int)
    

    
    # Need to have a minimum ADX to show downtrend
    #df['downtrend_signals'] = df['downtrend_signals'] * (df['ADX'] > 25).astype(int)

    

    # Set is_downtrend to True if downtrend_signals reaches the threshold
    df['is_downtrend'] = df['downtrend_signals'] >= threshold

    return df
