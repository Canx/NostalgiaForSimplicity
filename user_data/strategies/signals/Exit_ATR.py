from Signal import Signal

class Exit_ATR(Signal):
    def __init__(self, priority: int = 100, atr_multiplier: float = 1.5, atr_sl_multiplier: float = 1.0):
        """
        atr_multiplier se establece en 1.5 por defecto para el target (take profit) en operaciones intradía o de pocas horas.
        atr_sl_multiplier se establece en 1.0 por defecto para el stop loss basado en ATR.
        """
        super().__init__(priority, enabled=True)
        self.atr_multiplier = atr_multiplier
        self.atr_sl_multiplier = atr_sl_multiplier

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

        if direction == "long":
            target = trade.open_rate + atr * self.atr_multiplier
            stoploss = trade.open_rate - atr * self.atr_sl_multiplier
            diff_target = target - current_rate
            diff_stoploss = current_rate - stoploss
            self.log.info(
                f"[{pair}] Trade LONG: open_rate={trade.open_rate:.4f}, ATR={atr:.4f}, "
                f"target={target:.4f} (dif={diff_target:.4f}), stoploss={stoploss:.4f} (dif={diff_stoploss:.4f}), "
                f"current_rate={current_rate:.4f}"
            )
            if current_rate >= target:
                return "exit_ATR_take_profit"
            elif current_rate <= stoploss:
                return "exit_ATR_stop_loss"

        elif direction == "short":
            target = trade.open_rate - atr * self.atr_multiplier
            stoploss = trade.open_rate + atr * self.atr_sl_multiplier
            diff_target = current_rate - target
            diff_stoploss = stoploss - current_rate
            self.log.info(
                f"[{pair}] Trade SHORT: open_rate={trade.open_rate:.4f}, ATR={atr:.4f}, "
                f"target={target:.4f} (dif={diff_target:.4f}), stoploss={stoploss:.4f} (dif={diff_stoploss:.4f}), "
                f"current_rate={current_rate:.4f}"
            )
            if current_rate <= target:
                return "exit_ATR_take_profit"
            elif current_rate >= stoploss:
                return "exit_ATR_stop_loss"

        # Si ninguna condición se cumple, logueamos el estado actual
        self.log.info(f"[{pair}] No se alcanzó ni target ni stoploss. current_rate={current_rate:.4f}")
        return None

