import os
import datetime
import importlib.util
import logging
from Signal import Signal
from pandas import DataFrame
import pandas as pd
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from datetime import datetime
import Indicators as ind


class NostalgiaForSimplicity(IStrategy):
    """
    Strategy managing multiple signals with priority
    """

    INTERFACE_VERSION = 3

    def __init__(self, config: dict) -> None:
        self.log = logging.getLogger(__name__)
        self.log.info("INICIANDO...")
        self.indicators = self.load("indicators", Signal)
        self.log.info(f"Indicadores cargados: {[type(ind).__name__ for ind in self.indicators]}")
        self.signals = self.load("signals", Signal)
        self.config_strategy()
        super().__init__(config)
        


    def bot_loop_start(self, current_time: datetime, **kwargs) -> None:
        """
        Called once before the bot starts. Checks for modified signals and indicators and reloads if needed.
        """
        # Verificar si es la primera vez que se ejecuta
        if not hasattr(self, '_has_run_once'):
            self._has_run_once = False

        # Inicializar almacenamiento para archivos monitoreados
        if not hasattr(self, "_last_loaded_files"):
            self._last_loaded_files = {}

        # Verificar cambios en archivos
        files_modified = self._check_for_file_changes()

        # En la primera iteración, simplemente marcar como completada y salir
        if not self._has_run_once:
            self.log.info("Primera ejecución completada: las marcas de tiempo han sido registradas.")
            self._has_run_once = True
            return

        # Recargar señales e indicadores solo si se detectaron cambios
        if files_modified.get("signals"):
            self.log.info("Cambios detectados en 'signals'. Recargando...")
            self._reload_component("signals", Signal)
            self._refresh_signals()

        if files_modified.get("indicators"):
            self.log.info("Cambios detectados en 'indicators'. Recargando...")
            self._reload_component("indicators", Signal)
            self._reload_component("signals", Signal)
            self._refresh_signals()

            

    def _check_for_file_changes(self) -> dict:
        """
        Verifica los cambios en los archivos de las carpetas "signals" y "indicators".
        """
        directories = [
            ("indicators", "indicators"),
            ("signals", "signals"),
        ]
        files_modified = {"signals": False, "indicators": False}

        for dir_name, attr_name in directories:
            dir_path = os.path.join(os.path.dirname(__file__), dir_name)

            for file in os.listdir(dir_path):
                if file.endswith(".py") and file != "__init__.py":
                    file_path = os.path.join(dir_path, file)

                    # Obtener el tiempo de modificación del archivo
                    last_modified_time = os.path.getmtime(file_path)
                    self.log.debug(f"Archivo: {file}, Marca de tiempo actual: {last_modified_time}")

                    # Si es la primera iteración, solo registrar las fechas
                    if not self._has_run_once:
                        self._last_loaded_files[file_path] = last_modified_time
                        self.log.debug(f"Primera ejecución: registrada marca de tiempo para {file}.")
                    else:
                        # Detectar cambios en iteraciones posteriores
                        prev_time = self._last_loaded_files.get(file_path)
                        if prev_time != last_modified_time:
                            self.log.debug(f"Cambio detectado en {file}: {prev_time} -> {last_modified_time}")
                            self._last_loaded_files[file_path] = last_modified_time
                            files_modified[attr_name] = True

        return files_modified

    def _reload_component(self, component_name: str, loader) -> None:
        """
        Recarga un componente especificado (signals o indicators).
        """
        self.log.debug(f"Recargando {component_name}...")
        setattr(self, component_name, self.load(component_name, loader))
        self.log.debug(f"{component_name.capitalize()} recargados.")

    def _refresh_signals(self) -> None:
        """
        Fuerza la actualización de los pares para regenerar señales de entrada y salida.
        """
        current_pairs = self.dp.current_whitelist() if callable(self.dp.current_whitelist) else self.dp.current_whitelist
        self.process_only_new_candles = False
        self.analyze(current_pairs)
        self.process_only_new_candles = True


    def load(self, signal_dir="signals", base_class=Signal):
        """
        Carga dinámicamente clases desde la carpeta dada y las retorna en una lista ordenada por prioridad.
        """
        components = []
        signal_dir = os.path.join(os.path.dirname(__file__), signal_dir)

        if not os.path.exists(signal_dir):
            self.log.warning(f"El directorio {signal_dir} no existe.")
            return components

        for file in os.listdir(signal_dir):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]
                file_path = os.path.join(signal_dir, file)

                # Dinámicamente importar el módulo
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # Buscar subclases del tipo base_class
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, base_class) and attr is not base_class:
                        components.append(attr())
                        self.log.debug(f"Clase cargada: {attr.__name__} desde {file_path}")

        # Ordenar las clases por prioridad si aplicable
        return sorted(components, key=lambda component: component.get_priority())



    @property
    def plot_config(self):
        plot_config = {}
        plot_config['main_plot'] = {
            'EMA_12': {'color': 'red'},
            'EMA_26': {'color': 'blue'},
            'EMA_50': {'color': 'green'},
            'EMA_200': {'color': 'yellow'},
        }
        plot_config['subplots'] = {
            # Create subplot MACD
            "downtrend": {
                'is_downtrend': {'color': 'red'},
            },
            "downtrend_signals": {
                'downtrend_signals': { 'color': 'blue'},
            },
            "ADX": {
                'ADX': { 'color': 'green'},
            }
        }

        return plot_config

    def config_strategy(self):
        
        for signal in self.signals:
            if signal.enabled:
                self.log.info(f"Configuring strategy... {signal.get_signal_tag()}.")
                signal.config_strategy(self)  # Llamar al método de cada señal



    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df = ind.add_indicators(df)  # Indicadores globales (quitar cuando no sea necesario)
        
        for indicator in self.indicators:
            if indicator.enabled:
                self.log.debug(f"Populating indicators for {indicator.get_signal_tag()}.")
                df = indicator.populate_indicators(df)  # Llamar al método de cada señal
        return df
    

    @informative('15m')
    def populate_indicators_15m(self, df: DataFrame, metadata: dict) -> DataFrame:
        #df = ind.calculate_aroon(df, length=14)
        for indicator in self.indicators:
            if indicator.enabled:
                self.log.debug(f"Populating indicators 15m for {indicator.get_signal_tag()}.")
                df = indicator.populate_indicators_15m(df)  # Llamar al método de cada señal
        return df


    @informative('1h')
    def populate_indicators_1h(self, df: DataFrame, metadata: dict) -> DataFrame:
        #df = ind.calculate_willr(df, length=84)
        #df = ind.calculate_stochrsi(df)
        #df = ind.calculate_bbands(df)

        return df


    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate entry signals based on plugin logic, with custom tags for each signal,
        while avoiding entries during a downtrend.
        """
        # Verificar que la vela actual tiene datos válidos
        if dataframe.empty or dataframe.iloc[-1].isna().any():
            self.log.warning(f"Skipping populate_entry_trend for {metadata.get('pair')} due to missing candle data.")
            return dataframe

        # Ensure required columns exist
        if "enter_long" not in dataframe.columns:
            dataframe["enter_long"] = 0
        if "enter_tag" not in dataframe.columns:
            dataframe["enter_tag"] = None  # Initialize with None

        pair = metadata.get("pair", "Unknown")  # Retrieve the trading pair from metadata

        for signal in self.signals:
            if not signal.enabled:
                continue

            self.log.debug(f"Checking entry signals from plugin {signal.get_signal_tag()}.")

            # Create a lazy evaluation function for the signal
            def lazy_evaluation():
                entry_signal = signal.entry_signal(dataframe, metadata)

                # Ensure entry_signal is a boolean Series
                if not isinstance(entry_signal, pd.Series) or entry_signal.dtype != bool:
                    raise TypeError(f"Signal {signal.get_signal_tag()} returned an invalid entry signal type.")

                return entry_signal

            # Generate an initial mask to evaluate signals
            new_signals = (dataframe["enter_long"] == 0)

            # Apply signals lazily
            if new_signals.any():
                entry_signal = lazy_evaluation()  # Evaluate the signal only if necessary
                final_signals = new_signals & entry_signal

                # Assign 1 to 'enter_long' for active signals
                dataframe.loc[final_signals, "enter_long"] = 1

                # Assign tags with the prefix 'enter_' to 'enter_tag'
                dataframe.loc[final_signals, "enter_tag"] = f"enter_{signal.get_signal_tag()}"

                # Log the pair and the generated signals
                signal_count = final_signals.sum()
                if signal_count > 0:
                    self.log.info(f"Signal {signal.get_signal_tag()} generated {signal_count} entry signal(s) for pair {pair}.")

        return dataframe



    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Generate exit signals based on plugin logic, with custom tags for each signal.
        """
        # Verificar que la vela actual tiene datos válidos
        if dataframe.empty or dataframe.iloc[-1].isna().any():
            self.log.warning(f"Skipping populate_exit_trend for {metadata.get('pair')} due to missing candle data.")
            return dataframe

        # Asegurar columnas necesarias
        if "exit_long" not in dataframe.columns:
            dataframe["exit_long"] = 0
        if "exit_tag" not in dataframe.columns:
            dataframe["exit_tag"] = ""

        pair = metadata.get("pair", "Unknown")  # Obtener el par desde metadata

        for signal in self.signals:
            if not signal.enabled:
                #self.log.info(f"Plugin {plugin.get_plugin_tag()} is disabled, skipping exit signal.")
                continue

            self.log.debug(f"Checking exit signals from plugin {signal.get_signal_tag()}.")
            exit_signal = signal.exit_signal(dataframe, metadata)

            # Verificar que exit_signal sea una Series booleana
            if not isinstance(exit_signal, pd.Series) or exit_signal.dtype != bool:
                raise TypeError(f"Signal {signal.get_signal_tag()} returned an invalid exit signal type.")

            # Aplicar señales de salida al DataFrame
            dataframe.loc[exit_signal, "exit_long"] = 1

            # Asignar etiquetas (exit_tag) para las señales activas
            dataframe.loc[exit_signal, "exit_tag"] = f"exit_{signal.get_signal_tag()}"


            # Registrar el par y las señales generadas
            signal_count = exit_signal.sum()
            if signal_count > 0:
                self.log.info(f"Signal {signal.get_signal_tag()} generated {signal_count} exit signal(s) for pair {pair}.")

        return dataframe


    def custom_exit(self, pair: str, trade: Trade, current_time: datetime, current_rate: float,
                    current_profit: float, **kwargs):

        params = {
            "pair": pair,
            "trade": trade,
            "current_time": current_time,
            "current_rate": current_rate,
            "current_profit": current_profit,
            **kwargs,
        }

        exit_signal = False  # Valor por defecto si ninguna señal se activa

        for signal in self.signals:
            if signal.enabled:
                signal_triggered = signal.custom_exit(**params)  # Llamada al método de la señal

                if isinstance(signal_triggered, bool) and signal_triggered:
                    return True  # Prioridad: si alguna señal devuelve True, se retorna inmediatamente
                elif isinstance(signal_triggered, str) and signal_triggered.strip():
                    exit_signal = signal_triggered  # Guardar la cadena no vacía, pero seguir buscando True

        return exit_signal  # Devuelve la última cadena no vacía encontrada o False si no hubo ninguna

