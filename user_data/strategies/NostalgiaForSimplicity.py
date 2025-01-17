import os
import importlib.util
import logging
from SignalPlugin import SignalPlugin
from pandas import DataFrame
import pandas as pd
import pandas_ta as ta
import numpy as np
from freqtrade.strategy import IStrategy, informative


class NostalgiaForSimplicity(IStrategy):
    """
    Strategy managing multiple plugins with priority-based entry and exit signals.
    """

    INTERFACE_VERSION = 3
    minimal_roi = {"40": 0.0, "30": 0.01, "20": 0.02, "0": 0.04}
    stoploss = -0.1
    timeframe = "5m"
    startup_candle_count = 100 # TODO: definida por los plugins

    def __init__(self, config: dict) -> None:
        self.log = logging.getLogger(__name__)
        super().__init__(config)
        self.plugins = self.load_plugins()


    def load_plugins(self):
        """
        Dynamically load and sort plugins by priority.
        """
        plugins = []
        plugin_dir = os.path.join(os.path.dirname(__file__), "plugins")

        for file in os.listdir(plugin_dir):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                file_path = os.path.join(plugin_dir, file)

                # Dynamically import the module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Search for subclasses of SignalPlugin
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, SignalPlugin) and attr is not SignalPlugin:
                        plugins.append(attr())

        # Sort plugins by priority
        return sorted(plugins, key=lambda plugin: plugin.get_priority())


    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        Add necessary indicators to the DataFrame.
        """

        # Indicadores de 5 minutos
        df["RSI_20"] = ta.rsi(df["close"], length=20)
        df["RSI_3"] = ta.rsi(df["close"], length=3)

        stochrsi = ta.stochrsi(df["close"])
        if isinstance(stochrsi, pd.DataFrame):
            df["STOCHRSIk_14_14_3_3"] = stochrsi["STOCHRSIk_14_14_3_3"]
            df["STOCHRSId_14_14_3_3"] = stochrsi["STOCHRSId_14_14_3_3"]
        else:
            df["STOCHRSIk_14_14_3_3"] = np.nan
            df["STOCHRSId_14_14_3_3"] = np.nan

        df["SMA_16"] = ta.sma(df["close"], length=16)
        df["RSI_14"] = ta.rsi(df["close"], length=14)

        df = self.calculate_aroon(df, length=14)

        return df
    

    @informative('15m')
    def populate_indicators_15m(self, df: DataFrame, metadata: dict) -> DataFrame:
        """
        Calcula los indicadores para el timeframe de 15m.
        """
        # Llamada a la función genérica para calcular Aroon
        df = self.calculate_aroon(df, length=14)

        return df


    def calculate_aroon(self, df: DataFrame, length: int) -> DataFrame:
        """
        Función genérica para calcular el indicador Aroon.
        """
        aroon = ta.aroon(df["high"], df["low"], length=length)
        if isinstance(aroon, pd.DataFrame):
            df[f"AROONU_{length}"] = aroon[f"AROONU_{length}"]
            df[f"AROOND_{length}"] = aroon[f"AROOND_{length}"]
        else:
            df[f"AROONU_{length}"] = np.nan
            df[f"AROOND_{length}"] = np.nan

        return df


    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate entry signals based on plugin logic, with custom tags for each signal.
        """
        # Asegurar columnas necesarias
        if "enter_long" not in dataframe.columns:
            dataframe["enter_long"] = 0
        if "enter_tag" not in dataframe.columns:
            dataframe["enter_tag"] = ""

        pair = metadata.get("pair", "Unknown")  # Obtener el par desde metadata

        for plugin in self.plugins:
            if not plugin.enabled:
                #self.log.info(f"Plugin {plugin.get_plugin_tag()} is disabled, skipping entry signal.")
                continue
            
            self.log.debug(f"Checking entry signals from plugin {plugin.get_plugin_tag()}.")
            entry_signal = plugin.entry_signal(dataframe, metadata)

            # Verificar que entry_signal sea una Series booleana
            if not isinstance(entry_signal, pd.Series) or entry_signal.dtype != bool:
                raise TypeError(f"Plugin {plugin.get_plugin_tag()} returned an invalid entry signal type.")

            # Aplicar señales de entrada al DataFrame
            dataframe.loc[entry_signal, "enter_long"] = 1

            # Asignar etiquetas (enter_tag) para las señales activas
            dataframe.loc[entry_signal, "enter_tag"] = plugin.get_plugin_tag()

            # Registrar el par y las señales generadas
            signal_count = entry_signal.sum()
            if signal_count > 0:
                self.log.info(f"Plugin {plugin.get_plugin_tag()} generated {signal_count} entry signal(s) for pair {pair}.")

        return dataframe


    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate exit signals based on plugin logic, with custom tags for each signal.
        """
        # Asegurar columnas necesarias
        if "exit_long" not in dataframe.columns:
            dataframe["exit_long"] = 0
        if "exit_tag" not in dataframe.columns:
            dataframe["exit_tag"] = ""

        pair = metadata.get("pair", "Unknown")  # Obtener el par desde metadata

        for plugin in self.plugins:
            if not plugin.enabled:
                #self.log.info(f"Plugin {plugin.get_plugin_tag()} is disabled, skipping exit signal.")
                continue

            self.log.debug(f"Checking exit signals from plugin {plugin.get_plugin_tag()}.")
            exit_signal = plugin.exit_signal(dataframe, metadata)

            # Verificar que exit_signal sea una Series booleana
            if not isinstance(exit_signal, pd.Series) or exit_signal.dtype != bool:
                raise TypeError(f"Plugin {plugin.get_plugin_tag()} returned an invalid exit signal type.")

            # Aplicar señales de salida al DataFrame
            dataframe.loc[exit_signal, "exit_long"] = 1

            # Asignar etiquetas (exit_tag) para las señales activas
            dataframe.loc[exit_signal, "exit_tag"] = plugin.get_plugin_tag()

            # Registrar el par y las señales generadas
            signal_count = exit_signal.sum()
            if signal_count > 0:
                self.log.info(f"Plugin {plugin.get_plugin_tag()} generated {signal_count} exit signal(s) for pair {pair}.")

        return dataframe


