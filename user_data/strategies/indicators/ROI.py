from Signal import Signal
from pandas import DataFrame
import numpy as np


class ROI(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)
    

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        """
        Calcula el ROI máximo esperado en un periodo de 2h basado en los movimientos históricos del par,
        asegurando que la entrada (mínimo) sea antes de la salida (máximo).
        """

        window = 24  # 24 velas de 5 minutos = 2 horas
        expected_roi = [np.nan] * len(df)

        for i in range(window, len(df)):
            df_window = df.iloc[i - window:i].reset_index(drop=True)

            # Buscar la vela con el precio mínimo (punto de entrada ideal)
            min_index = df_window['low'].idxmin()
            min_price = df_window['low'].iloc[min_index]

            # Buscar la vela con el precio máximo *después* del mínimo (punto de salida ideal)
            df_after_min = df_window.iloc[min_index + 1:]  # Solo consideramos después del mínimo
            if not df_after_min.empty:
                max_price = df_after_min['high'].max()
            else:
                max_price = min_price  # Si no hay valores después, asumimos que no hay ganancia

            # Calcular ROI solo si la entrada ocurre antes que la salida
            if min_price > 0:
                max_roi = (max_price - min_price) / min_price
            else:
                max_roi = 0  # Evitar divisiones por 0

            expected_roi[i] = max_roi  # Guardamos el resultado en la lista

        df['expected_ROI_2h'] = expected_roi

        # Calcular SMA (Media Móvil Simple) de 1 hora (~12 velas)
        df['expected_ROI_2h_SMA'] = df['expected_ROI_2h'].rolling(window=12).mean()

        # Calcular EMA (Media Móvil Exponencial) de 1 hora (~12 velas)
        df['expected_ROI_2h_EMA'] = df['expected_ROI_2h'].ewm(span=12, adjust=False).mean()

        return df