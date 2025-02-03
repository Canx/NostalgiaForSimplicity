from Signal import Signal
from freqtrade.strategy import IStrategy


class Exit_DynamicROI(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)

    def custom_exit(self, strategy: IStrategy, pair, trade, current_time, current_rate, current_profit, **kwargs):
        """
        Define condiciones personalizadas de salida para cada trade.
        """
        # No salir si no hay beneficios
        if current_profit < 0:
            return None

        dataframe, _ = strategy.dp.get_analyzed_dataframe(pair, strategy.timeframe)

        if dataframe is None or dataframe.empty:
            return None

        last_candle = dataframe.iloc[-1]  # Última vela disponible

        # Evaluamos la tendencia del mercado
        is_bullish = last_candle['close'] > last_candle['EMA_50'] > last_candle['EMA_200']
        rsi_high = last_candle['RSI_14'] > 60
        strong_trend = last_candle['ADX_14'] > 25  # ADX alto = fuerte tendencia

        # Definir ROI dinámico y factor de decaimiento según la tendencia
        if is_bullish and rsi_high and strong_trend:
            base_dynamic_roi = 0.07  # Tendencia fuerte, ROI alto
            decay_factor = 0.995  # Decrecimiento lento
        elif is_bullish:
            base_dynamic_roi = 0.05  # Tendencia moderada
            decay_factor = 0.99  # Decrecimiento estándar
        else:
            base_dynamic_roi = 0.02  # Tendencia bajista, ROI bajo
            decay_factor = 0.98  # Decrecimiento rápido para salir antes

        # Duración del trade en minutos
        trade_dur = int((current_time.timestamp() - trade.open_date_utc.timestamp()) // 60)

        # Aplicar el decaimiento del ROI con el tiempo
        min_roi_time_decay = base_dynamic_roi * (decay_factor ** trade_dur)

        self.log.info(f"[custom_exit] {pair} - Duración: {trade_dur} min - ROI requerido: {min_roi_time_decay:.4f}")

        # Si el profit actual es mayor que el ROI decreciente, salimos del trade
        if current_profit > min_roi_time_decay:
            return "dynamic_roi_exit"  # Etiqueta personalizada para el exit

        return None  # No salir si no se cumple la condición
            
