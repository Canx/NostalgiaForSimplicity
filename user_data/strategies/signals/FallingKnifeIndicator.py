from signals.Signal import Signal
import pandas as pd
from pandas import DataFrame


class FallingKnifeIndicator(Signal):
    def __init__(self, priority: int = 10):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        df["falling_knife_start"] = ((df["EMA_5_acceleration"] < -0.0005) & (df["EMA_12_slope"] > 0))

        candles = 50
        df["falling_knife_recent"] = (df["falling_knife_start"].rolling(window=candles).apply(lambda x: x.any(), raw=True))

        df["falling_knife"] = (
            (df["EMA_9_slope"] < 0) 
            & (df["EMA_9_slope"].shift(1) < 0)
            & (df["falling_knife_recent"])
        )

        df["falling_knife_length"] = (
            df["falling_knife"].astype(int).groupby((df["falling_knife"] != df["falling_knife"].shift()).cumsum()).cumsum()
        )

        # Reseteamos la longitud a 0 si el período no es un "falling_knife"
        df["falling_knife_length"] = df["falling_knife_length"].where(df["falling_knife"], 0)

        # Identificar dónde termina un falling knife de al menos 2 velas
        df["end_of_falling_knife"] = (
            (df["falling_knife"] == False)  # No estamos en un falling_knife
            & (df["falling_knife"].shift(1) == True)  # En la vela anterior estábamos en un downtrend
            & (df["falling_knife_length"].shift(1) >= 2)  # El falling_knife anterior tuvo al menos 5 velas
        )

        # Inicializamos la columna para el precio de la vela anterior
        df["prev_close_before_falling_knife"] = pd.NA
        last_close = None  # Variable para almacenar el precio de cierre previo al último falling_knife_start

        for i in range(len(df)):  # Iteramos hacia adelante (de menos reciente a más reciente)
            if df.loc[i, "falling_knife_start"]:  # Si encontramos un nuevo falling_knife_start
                last_close = df.loc[i - 1, "close"] if i > 0 else None  # Capturamos el cierre de la vela anterior
            df.loc[i, "prev_close_before_falling_knife"] = last_close  # Rellenamos hasta el siguiente falling_knife_start

        return df