from Signal import Signal

class Exit_ATR(Signal):
    def __init__(self, priority: int = 100, atr_multiplier: float = 1.5):
        """
        atr_multiplier se establece en 1.5 por defecto, adecuado para operaciones intradía o de pocas horas.
        """
        super().__init__(priority, enabled=True)
        self.atr_multiplier = atr_multiplier

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        # Obtener el dataframe analizado
        dataframe, _ = self.strat.dp.get_analyzed_dataframe(pair, self.strat.timeframe)
        if dataframe is None or dataframe.empty:
            self.log.warning(f"[{pair}] Dataframe vacío o None al obtener datos analizados.")
            return None

        # Utilizamos directamente la columna ATR_14
        atr = dataframe["ATR_14"].iloc[-1]

        # Determinar la dirección del trade (por defecto "long")
        try:
            direction = trade.direction.lower()
        except AttributeError:
            direction = "long"

        # Calcular el nivel de Take Profit basado en ATR y la dirección del trade
        if direction == "long":
            target = trade.open_rate + atr * self.atr_multiplier
            difference = target - current_rate
            self.log.info(
                f"[{pair}] Trade LONG: open_rate={trade.open_rate:.4f}, ATR={atr:.4f}, "
                f"target={target:.4f}, current_rate={current_rate:.4f}, diferencia={difference:.4f}"
            )
            if current_rate >= target:
                return f"exit_ATR"
        elif direction == "short":
            target = trade.open_rate - atr * self.atr_multiplier
            difference = current_rate - target
            self.log.info(
                f"[{pair}] Trade SHORT: open_rate={trade.open_rate:.4f}, ATR={atr:.4f}, "
                f"target={target:.4f}, current_rate={current_rate:.4f}, diferencia={difference:.4f}"
            )
            if current_rate <= target:
                return f"exit_ATR"

        # Logueamos la diferencia restante si el target no se ha alcanzado
        self.log.info(f"[{pair}] Target no alcanzado. Diferencia restante: {difference:.4f}")
        return None
