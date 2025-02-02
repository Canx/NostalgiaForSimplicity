from Signal import Signal
from freqtrade.strategy import IStrategy
from datetime import datetime



class Exit_DynamicTrailing(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)

    def custom_stoploss(self, strategy: IStrategy, pair: str, trade, current_time: datetime, current_rate: float, 
                          current_profit: float, **kwargs) -> float:
        """
        Calcula un stoploss dinámico que comienza en -5% y se va reduciendo (endureciendo) con el tiempo hasta acercarse a 0,
        combinándolo con un trailing stop basado en el máximo alcanzado.
        
        Parámetros:
          - Se asume que cada vela dura 5 minutos.
          - initial_stoploss: -0.05 (es decir, -5%) al inicio.
          - max_hold_bars: 60 barras (equivalentes a 5 horas en un timeframe de 5 minutos).
          - trailing_stop_pct: 0.98, es decir, se activaría si el precio cae un 2% respecto al máximo alcanzado.
        
        Se devuelve un float negativo que representa el stoploss (por ejemplo, -0.10 equivale a -10%).
        """
        # Parámetros ajustables
        initial_stoploss = -0.05      # Stoploss inicial del -5%
        max_hold_bars = 60            # Umbral de tiempo: 60 barras (5 minutos cada una => 5 horas)
        trailing_stop_pct = 0.98      # Factor para el trailing stop (permite un retroceso del 2%)

        # Obtener el DataFrame analizado para el par en el timeframe de la estrategia
        dataframe, _ = strategy.dp.get_analyzed_dataframe(pair, strategy.timeframe)
        if dataframe is None or dataframe.empty:
            return initial_stoploss  # Si no hay datos, se devuelve el stoploss inicial

        # --- Cálculo del Trailing Stop Dinámico ---
        # Calcular el máximo acumulado de la columna "close"
        trailing_max = dataframe["close"].cummax()
        # Precio de trailing stop basado en el máximo acumulado
        current_trailing_stop = trailing_max.iloc[-1] * trailing_stop_pct
        # Cálculo del stoploss dinámico en porcentaje
        dynamic_stoploss = (current_trailing_stop / current_rate) - 1

        # --- Cálculo del Stoploss Basado en el Tiempo ---
        # Calcular la duración del trade en minutos
        trade_dur_minutes = int((current_time.timestamp() - trade.open_date_utc.timestamp()) // 60)
        # Calcular el número de barras transcurridas (suponiendo 5 minutos por vela)
        bars_since_entry = trade_dur_minutes / 5.0
        # Relación de tiempo (máximo 1.0 cuando se alcanza o supera max_hold_bars)
        time_ratio = min(1.0, bars_since_entry / max_hold_bars)
        # El stoploss basado en el tiempo se interpola linealmente:
        # Al inicio: -5% (time_ratio = 0) y a los 60 bares: 0% (time_ratio = 1)
        time_based_stoploss = initial_stoploss * (1 - time_ratio)

        # --- Combinación de Ambos Componentes ---
        # Se toma el máximo (es decir, el menos negativo) entre el trailing stop y el stop basado en el tiempo.
        # Esto significa que, a medida que pasa el tiempo y el stop basado en el tiempo se eleva, se forzará la salida si es más alto.
        final_stoploss = max(dynamic_stoploss, time_based_stoploss)

        strategy.log.info(
            f"[custom_stoploss] {pair} - Current rate: {current_rate:.4f}, Trailing stop price: {current_trailing_stop:.4f}, "
            f"Dynamic stoploss: {dynamic_stoploss:.4f}, Time-based stoploss: {time_based_stoploss:.4f}, "
            f"Bars since entry: {bars_since_entry:.1f}"
        )

        return final_stoploss

            
