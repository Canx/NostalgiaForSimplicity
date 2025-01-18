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

def calculate_willr(df: pd.DataFrame, length: int) -> pd.DataFrame:
    """
    Calcula el indicador Williams %R (WILLR).
    """
    df[f"WILLR_{length}"] = ta.willr(df["high"], df["low"], df["close"], length=length)
    return df

def calculate_rsi(df: pd.DataFrame, length: int) -> pd.DataFrame:
    """
    Calcula el indicador RSI.
    """
    df[f"RSI_{length}"] = ta.rsi(df["close"], length=length)
    return df

def calculate_sma(df: pd.DataFrame, length: int) -> pd.DataFrame:
    """
    Calcula la media móvil simple (SMA).
    """
    df[f"SMA_{length}"] = ta.sma(df["close"], length=length)
    return df

def calculate_mfi(df: pd.DataFrame, length: int) -> pd.DataFrame:
    """
    Calcula el indicador Money Flow Index (MFI).
    """
    df[f"MFI_{length}"] = ta.mfi(df["high"], df["low"], df["close"], df["volume"], length=length)
    return df

def calculate_ema(df: pd.DataFrame, length: int) -> pd.DataFrame:
    """
    Calcula la media móvil exponencial (EMA).
    """
    df[f"EMA_{length}"] = ta.ema(df["close"], length=length)
    return df

def calculate_rolling_max(df: pd.DataFrame, length: int, column: str = "close") -> pd.DataFrame:
    """
    Calcula el valor máximo rodante.
    """
    df[f"{column}_max_{length}"] = df[column].rolling(length).max()
    return df

def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega todos los indicadores necesarios al DataFrame.
    """
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

    df = calculate_willr(df, length=14)
    df = calculate_rolling_max(df, length=48, column="close")

    df = calculate_aroon(df, length=14)
    df = calculate_stochrsi(df)
    df = calculate_bbands(df)
    df = calculate_is_downtrend(df)

    return df


def calculate_ema_slope(df: pd.DataFrame, length: int) -> pd.Series:
    """
    Calcula la pendiente de una EMA determinada.
    """
    ema = ta.ema(df['close'], length=length)
    return ema.diff()


def calculate_is_downtrend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula una columna `is_downtrend` en el DataFrame basada en:
    - Pendiente de EMA12 negativa
    - Pendiente de EMA26 negativa
    - Pendiente de EMA12 más pronunciada que EMA26
    """
    # Calcular las EMAs y sus pendientes
    df['EMA_12_slope'] = df['EMA_12'].diff()
    df['EMA_26_slope'] = df['EMA_26'].diff()

    # Calcular la condición de downtrend
    df['is_downtrend'] = (
        (df['EMA_12_slope'] < 0) &
        (df['EMA_26_slope'] < 0) &
        (df['EMA_12_slope'] < df['EMA_26_slope'])
    )

    return df
