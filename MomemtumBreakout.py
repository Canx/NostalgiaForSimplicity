import pandas as pd
import talib as ta
from freqtrade.strategy.interface import IStrategy

class MomentumBreakout(IStrategy):
    # Configuración básica
    timeframe = '5m'
    minimal_roi = {
        "0": 0.05,  # Espera un 5% de ROI mínimo en los primeros minutos
        "60": 0.03,  # Reduce a 3% después de 1 hora
        "120": 0.01  # Acepta 1% si se mantiene más de 2 horas
    }

    # Desactivar trailing_stop y stop_loss
    trailing_stop = False  # Desactiva trailing stop
    stoploss = -0.99  # Desactiva el stoploss (ningún stop loss)

    # Parámetros de indicadores
    rsi_length = 14
    rsi_overbought = 70
    rsi_oversold = 30
    macd_fast = 12
    macd_slow = 26
    macd_signal = 9
    atr_length = 14  # ATR para volatilidad

    def populate_indicators(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # RSI
        df['rsi'] = ta.RSI(df['close'], timeperiod=self.rsi_length)

        # MACD
        df['macd'], df['macd_signal'], df['macd_hist'] = ta.MACD(df['close'], fastperiod=self.macd_fast, slowperiod=self.macd_slow, signalperiod=self.macd_signal)

        # ATR (para volatilidad)
        df['atr'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=self.atr_length)

        return df

    def populate_buy_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Calcula la media móvil de la señal MACD
        signal_mean = df['macd_signal'].rolling(window=9, min_periods=1).mean()
        
        # Disparidad: Cuánto se ha alejado la señal del promedio
        signal_disparity = df['macd_signal'] - signal_mean
        
        # Umbral relativo basado en el tamaño promedio de macd_signal
        avg_signal = df['macd_signal'].abs().mean()
        relative_threshold = avg_signal * 0.7  # Por ejemplo, 10% del promedio absoluto

        avg_volume = df['volume'].rolling(window=20, min_periods=1).mean()

        # Umbral de volumen: 150% del promedio
        volume_threshold = avg_volume * 1.5  # Cambiar el 1.5 según el porcentaje deseado

        # Condición de compra: La disparidad supera el umbral relativo
        df.loc[
            (signal_disparity > relative_threshold) &  # Señal disparada relativa a su tamaño
            (df['volume'] > volume_threshold),
            'buy'
        ] = 1
        
        return df





    def populate_sell_trend(self, df: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        # Condición de venta: El RSI está por encima de 70 (sobrecompra) y el MACD está cruzando a la baja
        # Además, el precio ha subido más de un 5% desde la compra
        df.loc[
            (
                (df['rsi'] > self.rsi_overbought) &  # RSI por encima de 70 (sobrecompra)
                (df['macd'] < df['macd_signal']) &  # MACD cruzando hacia abajo
                (df['close'] > df['close'].shift(1) * 1.05)  # El precio ha subido más de un 5%
            ),
            'sell'] = 1
        return df
