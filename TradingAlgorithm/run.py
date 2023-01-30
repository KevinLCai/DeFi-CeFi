import os
import sys
import argparse
import pandas as pd
import backtrader as bt
# from strategies.GoldenCross import GoldenCross
from SimpleStrategy import SimpleStrategy

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)

spy_prices = pd.read_csv('TradingAlgorithm/data/daily_BTC.csv',
                         index_col='Date', parse_dates=True)

feed = bt.feeds.PandasData(dataname=spy_prices)
cerebro.adddata(feed)

cerebro.addstrategy(SimpleStrategy)

cerebro.run()
cerebro.plot()
