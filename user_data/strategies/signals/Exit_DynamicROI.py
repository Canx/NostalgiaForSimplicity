from Signal import Signal

class Exit_DynamicROI(Signal):
    def init(self):
        self.priority = 100
        self.enabled = False

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        """
        Define condiciones personalizadas de salida para cada trade, 
        ajustando el ROI base y el factor de decaimiento en función de la volatilidad.
        """

        dataframe, _ = self.strat.dp.get_analyzed_dataframe(pair, self.strat.timeframe)
        if dataframe is None or dataframe.empty:
            return None

        last_candle = dataframe.iloc[-1]  # Última vela disponible

        # Evaluamos la tendencia del mercado
        is_bullish = last_candle['close'] > last_candle['EMA_50'] > last_candle['EMA_200']
        rsi_high = last_candle['RSI_14'] > 60
        strong_trend = last_candle['ADX_14'] > 25  # ADX alto = fuerte tendencia

        # Definir ROI dinámico y factor de decaimiento según la tendencia
        if is_bullish and rsi_high and strong_trend:
            base_dynamic_roi = 0.08  # Tendencia fuerte, ROI alto
            decay_factor = 0.995     # Decrecimiento lento
        elif is_bullish:
            base_dynamic_roi = 0.04  # Tendencia moderada
            decay_factor = 0.99      # Decrecimiento estándar
        else:
            base_dynamic_roi = 0.02  # Tendencia bajista, ROI bajo
            decay_factor = 0.98      # Decrecimiento rápido para salir antes

        # --- Ajuste por volatilidad ---
        # Calcular la volatilidad relativa usando ATR (por ejemplo, ATR_14)
        try:
            atr_value = last_candle['ATR_14']
        except KeyError:
            self.log.warning("ATR_14 no se encontró en el DataFrame. No se aplicarán ajustes por volatilidad.")
            atr_value = None

        if atr_value is not None:
            volatility_percent = atr_value / last_candle['close']

            # Establecemos ajustes según rangos arbitrarios de volatilidad
            # Estos umbrales y multiplicadores pueden ajustarse según el activo y el comportamiento histórico.
            if volatility_percent > 0.05:  # Alta volatilidad
                volatility_roi_adjustment = 0.9    # Reducir el ROI base en un 10%
                volatility_decay_adjustment = 1.002  # Hacer el decaimiento un poco más lento (factor más cercano a 1)
            elif volatility_percent < 0.02:  # Baja volatilidad
                volatility_roi_adjustment = 1.1    # Aumentar el ROI base en un 10%
                volatility_decay_adjustment = 0.998  # Hacer el decaimiento un poco más rápido
            else:  # Volatilidad media
                volatility_roi_adjustment = 1.0
                volatility_decay_adjustment = 1.0

            # Ajustamos el ROI base y el factor de decaimiento
            base_dynamic_roi *= volatility_roi_adjustment
            decay_factor *= volatility_decay_adjustment

            self.log.info(f"[custom_exit] {pair} - Volatilidad: {volatility_percent:.4f} | "
                        f"Ajuste ROI: {volatility_roi_adjustment} | Ajuste decay: {volatility_decay_adjustment}")
        # --- Fin del ajuste por volatilidad ---

        # Duración del trade en minutos
        trade_dur = int((current_time.timestamp() - trade.open_date_utc.timestamp()) // 60)

        # Aplicar el decaimiento del ROI con el tiempo
        min_roi_time_decay = base_dynamic_roi * (decay_factor ** trade_dur)
        # Establecer un mínimo absoluto de -1%
        min_roi_time_decay = max(min_roi_time_decay, -0.01)

        self.log.info(f"[custom_exit] {pair} - Duración: {trade_dur} min - ROI requerido: {min_roi_time_decay:.4f}")

        # Si el profit actual es mayor que el ROI requerido (incluso en territorio negativo), salimos del trade
        if current_profit > min_roi_time_decay:
            return "dynamic_roi_exit"  # Etiqueta personalizada para el exit

        return None  # No salir si no se cumple la condición


            
