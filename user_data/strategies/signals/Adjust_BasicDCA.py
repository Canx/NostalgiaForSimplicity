from Signal import Signal
from freqtrade.persistence import Trade
from freqtrade.exchange import date_minus_candles
from datetime import datetime
# Asegúrate de tener importada o definida la función date_minus_candles
# from utils import date_minus_candles

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
        se marcó una señal de entrada (columna 'enter_long' o 'enter_short'), se calcula el DCA como
        la cantidad del trade actual, siempre que se cumplan ciertas condiciones.

        :param trade: Objeto Trade del par.
        :param current_time: Tiempo actual.
        :param current_rate: Precio actual.
        :param current_profit: Beneficio actual.
        :param min_stake: Inversión mínima permitida.
        :param max_stake: Inversión máxima disponible.
        :param current_entry_rate: Precio de entrada actual.
        :param current_exit_rate: Precio de salida actual.
        :param current_entry_profit: Beneficio calculado con precio de entrada.
        :param current_exit_profit: Beneficio calculado con precio de salida.
        :param kwargs: Parámetros adicionales.
        :return: La cantidad para ajustar la posición (DCA) o None si no se cumple ninguna condición.
        """
        pair = trade.pair

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

        self.log.info(f"Calculando DCA para {pair}")

        # Verificar que existan al menos dos candles para hacer la comparación
        if len(dataframe) > 2:
            last_candle = dataframe.iloc[-1].squeeze()
            previous_candle = dataframe.iloc[-2].squeeze()
            # Determinar el nombre de la columna de señal en función de la dirección del trade
            signal_name = 'enter_long' if not trade.is_short else 'enter_short'
            prior_date = date_minus_candles(self.strat.timeframe, 1, current_time)

            # Solo se agranda la posición en un nuevo señal:
            if (
                last_candle.get(signal_name) == 1
                and previous_candle.get(signal_name) != 1
                and trade.nr_of_successful_entries < 2
                and trade.orders[-1].order_date_utc < prior_date
                and current_rate < current_entry_rate * 0.99  # El precio actual debe ser al menos 1% inferior
            ):
                return trade.stake_amount

        return None




