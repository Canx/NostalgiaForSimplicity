from Signal import Signal
from pandas import DataFrame
import pandas as pd
import talib as ta


class Entry_KamaFama2(Signal):
    def init(self):
        self.priority = 105
        self.enabled = False
    
    def plot_config(self):
        plot_config = {}
        plot_config['main_plot'] = {
            'kama': {'color': 'red'},
            'mama': {'color': 'blue'},
            'fama': {'color': 'green'},
            'mama_offset_0981': { 'color': 'orange'}
        }
        plot_config['subplots'] = {
            "kama > fama": {
                'kama_over_fama': {'color': 'red'},
            },
            "fama > mama*0.981": {
                'fama_over_mama': { 'color': 'blue'},
            },
            "WILLR < -61.3": {
                'WILLR_KF': { 'color': 'green'},
            },
            "mama_diff < -0.025": {
                "mamadiff_KF": { 'color': 'orange'}
            },
            "cti < -0.715": {
                "cti_KF": { 'color': 'purple'}
            },
            "close < close48 * 0.98": {
                "close48_KF": { 'color': 'yellow'}
            },
            "close < close288 * 0.96": {
                "close288_KF": { 'color': 'white'}
            },
            "RSI84 < 60": {
                "RSI84_KF": { 'color': 'maroon'}
            },
            "RSI112 < 60": {
                "RSI112_KF": { 'color': 'pink'}
            }
        }

        return plot_config


    def entry_signal(self, df: DataFrame, metadata: dict) -> pd.Series:
        return (
            (df['kama_over_fama']) &
            (df['fama_over_mama']) &
            (df['WILLR_KF']) &
            (df['mamadiff_KF']) &
            (df['cti_KF']) &
            (df['close48_KF']) &
            (df['close288_KF']) &
            (df['RSI84_KF']) &
            (df['RSI112_KF'])
        )