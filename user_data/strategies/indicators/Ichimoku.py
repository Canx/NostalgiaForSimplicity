
from Signal import Signal
from pandas import DataFrame
import pandas_ta as ta
from freqtrade.strategy import IntParameter

class Ichimoku(Signal):
    def init(self):
        self.priority = 1
        self.enabled = False


    def populate_indicators(self, df: DataFrame) -> DataFrame:

        ichimoku_short = IntParameter(7, 10, default=9, space="buy")
        ichimoku_medium = IntParameter(20, 30, default=26, space="buy")
        ichimoku_long = IntParameter(45, 60, default=52, space="buy")
        
        # Calcular Ichimoku Cloud
        ichimoku = pta.ichimoku(
            dataframe['high'],
            dataframe['low'],
            dataframe['close']
        )
        
        # Concatenar los resultados en el DataFrame original
        dataframe = pd.concat([dataframe, ichimoku[0], ichimoku[1]], axis=1)
        
        # Ajustar nombres de columnas según pandas_ta
        dataframe.rename(columns={
            'ITS_9': 'tenkan_sen',
            'IKS_26': 'kijun_sen',
            'ISA_9': 'senkou_span_a',
            'ISB_26': 'senkou_span_b',
            'ICS_26': 'chikou_span'
        }, inplace=True)

        return df



