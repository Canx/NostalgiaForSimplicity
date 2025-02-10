from Signal import Signal
from pandas import DataFrame
import numpy as np

class TrendSlope(Signal):
    def __init__(self, strat, priority: int = 10, window: int = 10):
        """
        :param priority: Prioridad del indicador.
        :param window: Número de velas a considerar para el cálculo (N).
        """
        super().__init__(strat, priority, enabled=False)
        self.N = window
        self.min_distance = window / 2  # Distancia mínima en número de velas dentro de la ventana

    def calc_line_angle_array(self, arr: np.ndarray) -> float:
        """
        Calcula el ángulo (en grados) de la línea definida por los dos highs más elevados
        dentro del arreglo 'arr' (que representa los valores 'high' de una ventana de self.N velas),
        usando índices relativos (0, 1, …, self.N-1). Se exige que los dos highs estén separados al menos
        self.min_distance posiciones.
        
        :param arr: np.ndarray de longitud self.N con los valores de 'high'
        :return: Ángulo en grados o np.nan si no se cumple la condición.
        """
        N = len(arr)
        if N < self.N:
            return np.nan

        # Seleccionar el high máximo (punto 1) y su posición relativa
        pos1 = int(np.argmax(arr))

        # Filtrar candidatos: posiciones cuya diferencia con pos1 sea al menos self.min_distance
        candidates = [i for i in range(N) if abs(i - pos1) >= self.min_distance]
        if not candidates:
            return np.nan

        # De entre los candidatos, seleccionar la posición con el mayor valor high (punto 2)
        candidate_values = arr[candidates]
        pos2 = candidates[int(np.argmax(candidate_values))]

        # Evitar división por cero
        if (pos2 - pos1) == 0:
            return np.nan

        # Calcular la pendiente y convertir a ángulo en grados
        slope = (arr[pos2] - arr[pos1]) / (pos2 - pos1)
        angle = np.degrees(np.arctan(slope))
        return angle

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        """
        Calcula el indicador 'trend_slope', que es el ángulo (en grados) de la línea
        definida por los dos highs más elevados (separados al menos self.N/2 velas)
        en una ventana de self.N velas. Se añade la columna 'trend_slope' al DataFrame.
        """
        # Si no hay suficientes datos, asignar np.nan
        if len(df) < self.N:
            df['trend_slope'] = np.nan
            return df

        # Se aplica la función rolling sobre la columna 'high'.
        # Usamos raw=True para que la función reciba un np.ndarray.
        df['trend_slope'] = df['high'].rolling(window=self.N, min_periods=self.N)\
            .apply(self.calc_line_angle_array, raw=True)

        return df

