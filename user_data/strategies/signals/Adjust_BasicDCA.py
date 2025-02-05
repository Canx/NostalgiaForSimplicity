from Signal import Signal
from freqtrade.persistence import Trade
from datetime import datetime


# TODO: Generar vela actual para hacer cálculos
# TODO: Comprobar si tenemos que vender, no solo comprar.
class Adjust_BasicDCA(Signal):
    def __init__(self, priority: int = 100):
        super().__init__(priority, enabled=False)


    def adjust_trade_position(
        self,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        min_stake: float | None,
        max_stake: float,
        current_entry_rate: float,
        current_exit_rate: float,
        current_entry_profit: float,
        current_exit_profit: float,
        **kwargs,
    ) -> float | None | tuple[float | None, str | None]:
        """
        DCA básico basado en la cantidad inicial del trade, verificando fondos suficientes.
        
        Se verifica inicialmente que se disponga de fondos (max_stake) al menos iguales a min_stake.
        Luego, si el beneficio actual es inferior a un umbral (por ejemplo, -3%) y en el último candle
        se marcó una señal de entrada (columna 'entry_signal'), se calcula el DCA como la mitad del costo
        de la primera orden de compra, garantizando que no sea inferior a min_stake.
        """
        pair = trade.pair

        self.log.info(f"Calculando DCA para {pair}")

        # Comprobación inicial de fondos: si no se tienen fondos al menos iguales a min_stake, no se realiza DCA.
        if min_stake is not None and max_stake < min_stake:
            self.log.info(
                f"No se dispone de fondos suficientes para DCA en {pair}: "
                f"max_stake ({max_stake}) es menor que min_stake ({min_stake})."
            )
            return None

        # Obtener el DataFrame analizado para el par y timeframe de la estrategia.
        dataframe, _ = self.strat.dp.get_analyzed_dataframe(pair, self.strat.timeframe)
        if dataframe is None or dataframe.empty:
            self.log.warning(f"No se pudo obtener el DataFrame analizado para {pair}")
            return None

        # Se obtiene el último candle.
        last_candle = dataframe.iloc[-1]

        # Verificar si en el último candle se marcó una señal de entrada (se asume que 'entry_signal' es booleana).
        if not last_candle.get("entry_signal", False):
            return None

        # Definir umbral de DCA, por ejemplo, -3%
        dca_threshold = -0.03
        if current_profit < dca_threshold:
            try:
                # Obtener las órdenes de compra llenadas para el trade.
                filled_buys = trade.select_filled_orders('buy')
                if not filled_buys:
                    self.log.warning(f"No se encontraron órdenes de compra para {pair}")
                    return None

                # Tomamos como referencia la primera orden de compra.
                initial_order_cost = filled_buys[0].cost

                # Calculamos la mitad del costo de la orden inicial.
                calculated_dca = initial_order_cost * 0.5

                # Nos aseguramos de que el DCA sea, al menos, min_stake.
                if min_stake is not None and calculated_dca < min_stake:
                    dca_amount = min_stake
                else:
                    dca_amount = calculated_dca

                # Comprobar si tenemos fondos suficientes para ejecutar el DCA.
                # Se requiere que max_stake (fondos disponibles) sea mayor o igual a dca_amount.
                if max_stake < dca_amount:
                    self.log.info(
                        f"No hay fondos suficientes para DCA en {pair}: "
                        f"max_stake ({max_stake}) < dca_amount ({dca_amount})."
                    )
                    return None

                self.log.info(
                    f"DCA activado para {pair}: beneficio actual {current_profit:.2%} inferior a {dca_threshold:.2%}, "
                    f"calculado DCA = {calculated_dca}, usando stake {dca_amount}"
                )
                return dca_amount

            except Exception as e:
                self.log.error(f"Error al calcular DCA para {pair}: {str(e)}")
                return None

        return None

