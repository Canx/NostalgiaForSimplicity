from Signal import Signal
from freqtrade.strategy import IStrategy
from freqtrade.persistence import Trade
from datetime import datetime, timedelta
import pandas as pd
import pandas_ta as pta


# Exit borrowed from KamaFama_2
class Exit_Stochastic(Signal):

    WAIT_TIME = timedelta(minutes=9, seconds=55)

    def __init__(self, priority: int = 100):
        self.cc = {}
        super().__init__(priority, enabled=False)


    def compute_fastk(self, df: 'pd.DataFrame') -> float:
        """
        Calcula el valor 'fastk' del estocástico rápido usando el DataFrame proporcionado.
        
        Parámetros:
        - df: DataFrame con los datos históricos y la vela actual.
        
        Retorna:
        - El valor 'fastk' de la última vela.
        """
        stoch_fast = pta.STOCHF(df, 5, 3, 0, 3, 0)
        df = df.copy()  # Evitamos modificar el DataFrame original
        df['fastk'] = stoch_fast['fastk']
        return df.iloc[-1]['fastk']
    
    def update_live_candle(self, trade_id: str, current_candle: 'pd.Series', current_rate: float) -> dict:
        """
        Actualiza el estado de la vela en tiempo real para un trade específico.

        Parámetros:
        - trade_id: Identificador único del trade.
        - current_candle: La vela actual proveniente del DataFrame analizado.
        - current_rate: Precio actual.
        
        Retorna:
        - Un diccionario con el estado actualizado de la vela.
        """
        state = self.cc
        default_candle_state = {
            'date': current_candle['date'],
            'open': current_candle['close'],
            'high': current_candle['close'],
            'low': current_candle['close'],
            'close': current_rate,
            'volume': 0,
        }
        # Recuperamos o inicializamos la vela
        candle_state = state.get(trade_id, default_candle_state.copy())

        # Si la fecha de la vela actual es distinta, se trata de una nueva vela
        if current_candle['date'] != candle_state['date']:
            candle_state.update({
                'date': current_candle['date'],
                'open': current_candle['close'],
                'high': current_candle['close'],
                'low': current_candle['close'],
                'close': current_rate,
            })
        else:
            # Actualizamos la vela existente
            candle_state['high'] = max(candle_state['high'], current_rate)
            candle_state['low'] = min(candle_state['low'], current_rate)
            candle_state['close'] = current_rate

        # Guardamos el estado actualizado y lo retornamos
        state[trade_id] = candle_state
        return candle_state



    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                current_profit: float, **kwargs):
        """
        Determina cuándo salir de una operación basándose en el indicador estocástico rápido (fastk)
        y en el estado de la vela en tiempo real.
        
        Parámetros:
        - pair: par de trading.
        - trade: objeto de la operación actual.
        - current_time: tiempo actual.
        - current_rate: precio actual.
        - current_profit: beneficio actual del trade.
        - kwargs: parámetros adicionales.
        
        Retorna:
        - Una cadena que indica la señal de salida o None si no se cumple la condición.
        """
        # 1. Obtener el DataFrame analizado y la vela actual.
        dataframe, _ = self.strat.dp.get_analyzed_dataframe(pair=pair, timeframe=self.strat.timeframe)
        current_candle = dataframe.iloc[-1].squeeze()

        # (min_profit se ha eliminado ya que no se utiliza)
        runmode = self.strat.config['runmode'].value

        # 2. Actualizar el estado de la vela en modo 'live' o 'dry_run'
        if runmode in ('live', 'dry_run'):
            live_candle = self.update_live_candle(trade.id, current_candle, current_rate)
        else:
            live_candle = current_candle

        # 3. Evaluar la condición de salida si la operación está en ganancia
        if current_profit > 0:
            if runmode in ('live', 'dry_run'):
                # Verificar que la vela tenga al menos WAIT_TIME de formación
                if current_time > live_candle['date'] + WAIT_TIME:
                    # Crear un DataFrame temporal añadiendo la vela actual actualizada
                    candle_df = pd.DataFrame([live_candle])
                    temp_df = pd.concat([dataframe, candle_df], ignore_index=True)
                    fastk_value = self.compute_fastk(temp_df)
                    if fastk_value > self.sell_fastx.value:
                        return "fastk_profit_sell_2"
            else:
                # Para otros modos (por ejemplo, backtesting) usamos directamente el valor 'fastk' de la vela actual
                if current_candle.get("fastk", 0) > self.sell_fastx.value:
                    return "fastk_profit_sell"

        return None