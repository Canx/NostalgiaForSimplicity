from Signal import Signal

class Exit_ExpectedROI(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=True)

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        """
        Salida optimizada basada en el ROI esperado en 2 horas, ajustando el ROI si la operación se alarga.
        """

        df, _ = self.strat.dp.get_analyzed_dataframe(pair, self.strat.timeframe)
        if df is None or df.empty:
            return None

        last_candle = df.iloc[-1]

        # ROI esperado basado en la media exponencial de 2h
        expected_roi_ema = last_candle.get("max_profit_2h_EMA", 0.05)  # 5% por defecto si no hay datos

        # Tiempo en la operación (en minutos)
        trade_dur = int((current_time.timestamp() - trade.open_date_utc.timestamp()) // 60)

        # Stop-loss: salir rápido si la pérdida supera cierto umbral
        stop_loss_threshold = -0.02  # -2% de pérdida

        # Parámetros de reducción del ROI esperado
        decay_start_time = 60  # Comenzamos a reducir ROI después de 1 hora
        decay_factor = 0.98  # Factor de reducción por cada minuto extra

        # Si llevamos más de 1 hora, empezamos a reducir el ROI esperado
        if trade_dur > decay_start_time:
            decay_minutes = trade_dur - decay_start_time
            expected_roi_ema *= (decay_factor ** decay_minutes)  # Reducción progresiva

        # No permitir que el ROI esperado caiga por debajo de un umbral mínimo
        min_expected_roi = 0.001  # Mínimo ROI requerido
        expected_roi_ema = max(expected_roi_ema, min_expected_roi)

        # Log de información para monitorear la estrategia
        self.log.info(
            f"[Exit_ExpectedROI] {pair} | Duración: {trade_dur} min | "
            f"ROI Esperado (ajustado): {expected_roi_ema:.4f} | Beneficio Actual: {current_profit:.4f}"
        )

        # Salida estándar: si alcanzamos el ROI esperado, salimos
        if current_profit >= expected_roi_ema:
            self.log.info(f"[Exit_ExpectedROI] {pair} | 🚀 Salida por ROI alcanzado: {current_profit:.4f}")
            return "exp_roi_exit_profit"

        # Si llevamos más de 2 horas y estamos cerca del ROI esperado, salir
        max_trade_time = 120  # 120 minutos (2 horas)
        if trade_dur >= max_trade_time and current_profit >= expected_roi_ema * 0.8:
            self.log.info(f"[Exit_ExpectedROI] {pair} | ⏳ Salida por tiempo máximo alcanzado")
            return "exp_roi_exit_time"

        # Stop-loss: salir si la pérdida es demasiado alta
        if current_profit < stop_loss_threshold:
            self.log.info(f"[Exit_ExpectedROI] {pair} | ❌ Stop-loss activado: {current_profit:.4f}")
            return "exp_roi_exit_stoploss"

        return None




            
