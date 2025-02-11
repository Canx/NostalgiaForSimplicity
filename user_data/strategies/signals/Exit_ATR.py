from Signal import Signal
import pandas as pd

class Exit_ATR(Signal):
    def init(self):
        self.priority = 100
        self.enabled = True

        self.atr_multiplier = 1.5
        self.atr_sl_multiplier = 1.0

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        # Obtener el dataframe analizado
        dataframe, _ = self.strat.dp.get_analyzed_dataframe(pair, self.strat.timeframe)
        if dataframe is None or dataframe.empty:
            self.log.warning(f"[{pair}] Dataframe vacío o None al obtener datos analizados.")
            return None

        # Intentar obtener ATR desde la columna "ATR_14" de la última vela válida.
        try:
            atr = None
            # Recorrer el dataframe desde el final hacia el principio
            for idx in range(len(dataframe) - 1, -1, -1):
                atr_candidate = dataframe["ATR_14"].iloc[idx]
                if pd.notnull(atr_candidate):
                    atr = atr_candidate
                    break
            if atr is None:
                self.log.error(f"[{pair}] No se encontró un valor ATR válido en el dataframe.")
                # Fallback: usar ATR almacenado en el trade, si existe.
                atr = trade.get_custom_data(key='fallback_atr', default=None)
                if atr is None:
                    self.log.error(f"[{pair}] No se encontró ATR fallback en los datos del trade.")
                    return None
                else:
                    self.log.info(f"[{pair}] Se utiliza ATR fallback obtenido del trade: {atr:.4f}")
            else:
                # Guardar el ATR obtenido como fallback para usos futuros
                trade.set_custom_data(key='fallback_atr', value=atr)
        except Exception as e:
            self.log.exception(f"[{pair}] Error al obtener ATR: {e}")
            # Fallback en caso de excepción
            atr = trade.get_custom_data(key='fallback_atr', default=None)
            if atr is None:
                self.log.error(f"[{pair}] No se encontró ATR fallback en los datos del trade tras excepción.")
                return None
            else:
                self.log.info(f"[{pair}] Se utiliza ATR fallback obtenido del trade: {atr:.4f}")

        # Determinar la dirección del trade (por defecto "long")
        try:
            direction = trade.direction.lower()
        except AttributeError:
            direction = "long"

        # Lógica de salida con ATR, incluyendo take profit y stop loss
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

        return None


