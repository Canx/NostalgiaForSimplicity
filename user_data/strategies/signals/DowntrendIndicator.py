from signals.Signal import Signal
from pandas import DataFrame
import pandas_ta as ta


class DowntrendIndicator(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        # slope (1st derivative)
        df['EMA_5_slope'] = df['EMA_5'].diff() / df["EMA_5"].shift()
        df['EMA_9_slope'] = df['EMA_9'].diff() / df["EMA_9"].shift()
        df['EMA_12_slope'] = df['EMA_12'].diff() / df["EMA_12"].shift()
        df['EMA_26_slope'] = df['EMA_26'].diff() / df["EMA_26"].shift()
        df['EMA_50_slope'] = df['EMA_50'].diff() / df["EMA_50"].shift()
        df['EMA_200_slope'] = df['EMA_200'].diff() / df["EMA_200"].shift()

        # acceleration (2nd derivative)
        df['EMA_5_acceleration'] = df['EMA_5_slope'].diff()
        df['EMA_9_acceleration'] = df['EMA_9_slope'].diff()
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
        
        # StockRSI low
        df['downtrend_signals'] += (df["STOCHRSIk_14_14_3_3"] < 30).astype(int)

        
        # Need to have a minimum ADX to show downtrend
        #df['downtrend_signals'] = df['downtrend_signals'] * (df['ADX'] > 25).astype(int)

        

        # Set is_downtrend to True if downtrend_signals reaches the threshold
        df['is_downtrend'] = df['downtrend_signals'] >= threshold

        # Identificar la longitud de los períodos consecutivos de "is_downtrend"
        df["downtrend_length"] = (
            df["is_downtrend"].astype(int).groupby((df["is_downtrend"] != df["is_downtrend"].shift()).cumsum()).cumsum()
        )
        
        # Reseteamos la longitud a 0 si el período no es un "downtrend"
        df["downtrend_length"] = df["downtrend_length"].where(df["is_downtrend"], 0)

        # Identificar dónde termina un downtrend de al menos X velas
        df["end_of_downtrend"] = (
            (df["is_downtrend"] == False)  # No estamos en un downtrend
            & (df["is_downtrend"].shift(1) == True)  # En la vela anterior estábamos en un downtrend
            #& (df["downtrend_length"].shift(1) >= 20)  # El downtrend anterior tuvo al menos 5 velas
        )

        return df