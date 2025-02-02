from Signal import Signal
from pandas import DataFrame
import pandas as pd


class Momemtum(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)
    

    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        # 0. Solo entramos si el precio está por encima de la EMA_200
        price_over_ema = (df["close"] > df["EMA_200"])

        # 1. Cruce de EMAs: detecta el cruce de EMA_12 sobre EMA_26 en esta vela.
        ema_cross = (df["EMA_12"].shift(1) <= df["EMA_26"].shift(1)) & (df["EMA_12"] > df["EMA_26"])
        
        # 2. Aceleración del momentum: el incremento actual (últimos 12 períodos) debe ser mayor que el anterior.
        momentum_current = df["close"] - df["close"].shift(12)
        momentum_prev = df["close"].shift(12) - df["close"].shift(24)
        momentum_rising = momentum_current > momentum_prev
        
        # 3. Condición de volumen: el volumen actual es mayor que la media móvil de 20 períodos.
        volume_cond = df["volume"] > df["volume"].rolling(window=20).mean()
        
        # 4. Condición de RSI: el RSI a 14 períodos debe estar por encima de 50.
        rsi_cond = df["RSI_14"] > 50
        
        # 5. (Opcional) Evitar comprar cuando el precio ya está muy alto: 
        # Se requiere que el cierre actual esté relativamente cerca del mínimo de los últimos 20 períodos.
        local_min_cond = df["close"] <= df["close"].rolling(window=20).min() * 1.1  # Ajusta el factor (1.1) según convenga
        
        return price_over_ema & ema_cross & momentum_rising & volume_cond & rsi_cond & local_min_cond


    # TODO: IMPROVE!
    # def exit_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
    #     # 1. Evaluar rally significativo en una ventana larga (por ejemplo, 60 velas ~5 horas en 5m)
    #     long_window = 60
    #     local_max_long = df["close"].rolling(window=long_window, min_periods=1).max()
    #     local_min_long = df["close"].rolling(window=long_window, min_periods=1).min()
    #     # Se considera rally si el pico es, por ejemplo, al menos 3% superior al mínimo de ese período
    #     significant_rally = (local_max_long / local_min_long) >= 1.03

    #     # 2. Detectar pico en el corto plazo (por ejemplo, 10 velas)
    #     short_window = 10
    #     local_max_short = df["close"].rolling(window=short_window, min_periods=1).max()
    #     # Se detecta pico si la vela anterior cerró al menos al 99% del máximo en la ventana corta
    #     peak_detected = df["close"].shift(1) >= local_max_short.shift(1) * 0.99

    #     # 3. Condición de reversión: la vela actual cierra por debajo de la vela anterior
    #     drop_condition = df["close"] < df["close"].shift(1)

    #     # 4. Filtro de downtrend: por ejemplo, que EMA_12 esté por debajo de EMA_26
    #     ema_downtrend = df["EMA_12"] < df["EMA_26"]

    #     # 5. Condición adicional para no salir si venimos de una montaña anterior mayor:
    #     # Se calcula un máximo global en una ventana muy amplia (por ejemplo, 300 velas)
    #     very_long_window = 300
    #     global_max = df["close"].rolling(window=very_long_window, min_periods=1).max()
    #     # Se exige que el pico detectado en la ventana corta sea al menos el 95% del máximo global reciente.
    #     peak_is_new = local_max_short.shift(1) >= global_max.shift(1) * 0.95

    #     # 6. Combinar todas las condiciones:
    #     raw_exit = peak_detected & drop_condition & ema_downtrend & significant_rally & peak_is_new

    #     # Emitir la señal solo en la transición de False a True (evitando señales repetitivas)
    #     raw_exit_bool = raw_exit.astype(bool)
    #     exit_condition = raw_exit_bool & (~raw_exit_bool.shift(1).fillna(False).astype(bool))

    #     return exit_condition










