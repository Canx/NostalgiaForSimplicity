#!/bin/bash
# Test Momemtum Breakout
rm -rf user_data/backtest_results/*
freqtrade backtesting --timeframe 5m --config user_data/config.json --strategy MomentumBreakout --export trades
freqtrade plot-dataframe --timeframe 5m --config user_data/config.json --strategy MomentumBreakout --export trades --indicators2 macd_signal
google-chrome-stable user_data/plot/freqtrade-plot-1MBABYDOGE_USDT-5m.html
