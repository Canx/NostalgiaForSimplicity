from Signal import Signal
from pandas import DataFrame
import numpy as np

class ProfitLoss(Signal):
    def __init__(self, priority: int = 1):
        super().__init__(priority, enabled=True)

    def populate_indicators(self, df: DataFrame) -> DataFrame:
        """
        Calcula el beneficio máximo (max_profit) y la pérdida máxima (max_loss) en un periodo de 2h 
        (24 velas de 5 minutos).

        Para max_profit:
          - Se busca el precio mínimo en 'low' dentro de la ventana y, a partir de ese punto, 
            se busca el máximo en 'high' posterior.
            
        Para max_loss (máximo drawdown):
          - Se calcula, para cada vela de la ventana, el drawdown = (low / acumulado_max(high) - 1)
            y se toma el valor mínimo (más negativo).

        Se utiliza un enfoque vectorizado con sliding_window_view para minimizar el coste en CPU.
        """
        # Verificar que existan las columnas requeridas
        required_columns = {'low', 'high'}
        if not required_columns.issubset(df.columns):
            self.log.warning("El DataFrame no contiene las columnas requeridas ('low','high'). Se omite el cálculo de indicadores.")
            return df

        window = 24  # 24 velas de 5 minutos = 2 horas
        values = df[['low', 'high']].to_numpy()
        n = len(values)
        max_profit = np.full(n, np.nan)
        max_loss = np.full(n, np.nan)

        if n < window:
            df['max_profit_2h'] = max_profit
            df['max_loss_2h'] = max_loss
        else:
            from numpy.lib.stride_tricks import sliding_window_view
            # Crear la vista de ventanas: forma (n - window + 1, window, 2)
            win_view = sliding_window_view(values, window_shape=window, axis=0)

            # Función para calcular el beneficio máximo (max_profit) en una ventana
            def calc_max_profit(win):
                # win es un array de forma (window, 2)
                low_vals = win[:, 0]
                high_vals = win[:, 1]
                min_idx = np.argmin(low_vals)
                min_price = low_vals[min_idx]
                if min_price <= 0:
                    return 0
                # Se consideran solo las velas posteriores al mínimo para hallar el máximo
                if min_idx < len(win) - 1:
                    max_price = np.max(high_vals[min_idx + 1:])
                else:
                    max_price = min_price
                return (max_price - min_price) / min_price

            # Función para calcular la pérdida máxima (máximo drawdown) en una ventana
            def calc_max_loss(win):
                # Para cada vela se calcula el máximo acumulado en high hasta ese punto
                # y el drawdown relativo con respecto a ese acumulado: (low / cum_max - 1).
                high_vals = win[:, 1]
                cum_max = np.maximum.accumulate(high_vals)
                # drawdown para cada vela
                drawdowns = win[:, 0] / cum_max - 1
                return np.min(drawdowns)

            # Calcular los indicadores para cada ventana usando list comprehensions
            profit_values = np.array([calc_max_profit(win) for win in win_view])
            loss_values = np.array([calc_max_loss(win) for win in win_view])

            # Asignar los resultados a los índices correspondientes (los primeros window-1 quedan como NaN)
            max_profit[window - 1:] = profit_values
            max_loss[window - 1:] = loss_values

            df['max_profit_2h'] = max_profit
            df['max_loss_2h'] = max_loss

        # Calcular medias móviles para suavizar los indicadores (ventana ~1h = 12 velas)
        df['max_profit_2h_SMA'] = df['max_profit_2h'].rolling(window=12, min_periods=1).mean()
        df['max_profit_2h_EMA'] = df['max_profit_2h'].ewm(span=12, adjust=False).mean()
        df['max_loss_2h_SMA'] = df['max_loss_2h'].rolling(window=12, min_periods=1).mean()
        df['max_loss_2h_EMA'] = df['max_loss_2h'].ewm(span=12, adjust=False).mean()

        return df
