from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class Entry_KamaFama2(Signal):
    def init(self):
        self.priority = 105
        self.enabled = True
    
    def plot_config(self):
        plot_config = {}
        plot_config['main_plot'] = {
            'kama': {'color': 'red'},
            'mama': {'color': 'blue'},
            'fama': {'color': 'green'},
            'mama_offset_0981': { 'color': 'orange'}
        }
        plot_config['subplots'] = {
            "entry_KF": {
                'entry_KF': {'color': 'white'},
            },
            "kama_over_fama": {
                'kama_over_fama': {'color': 'red'},
            },
            "fama_over_mama": {
                'fama_over_mama': { 'color': 'blue'},
            },
            "WILLR_KF": {
                'WILLR_KF': { 'color': 'green'},
            },
            "mamadiff_KF": {
                "mamadiff_KF": { 'color': 'orange'}
            },
            "cti_KF": {
                "cti_KF": { 'color': 'purple'}
            },
            "close288_KF": {
                "close48_KF": { 'color': 'yellow'}
            },
            "close < close288 * 0.96": {
                "close288_KF": { 'color': 'white'}
            },
            "RSI84_KF": {
                "RSI84_KF": { 'color': 'maroon'}
            },
            "RSI112_KF": {
                "RSI112_KF": { 'color': 'pink'}
            }
        }

        return plot_config


    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['kama_over_fama'])
            & (df['fama_over_mama'])
            & (df['WILLR_KF'])
            & (df['mamadiff_KF'])
            & (df['cti_KF'])
            & (df['close48_KF'])
            & (df['close288_KF'])
            & (df['RSI84_KF'])
            & (df['RSI112_KF'])
        )