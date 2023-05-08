import math
import pandas as pd
import random
import numpy as np
import scipy.stats as stats
# from ta.trend import MACD

class PairsTrading():
    def __init__(self, btc_df, eth_df, in_position):
        self.btc_df = btc_df
        self.eth_df = eth_df
        self.in_position = in_position
        self.spread_ratio = self.btc_df['Close'].mean() / self.eth_df['Close'].mean()
        self.p_threshodl = 0.05
        self.slow_period = 26
        self.fast_period = 12
        self.spread = self.btc_df['Close'] - (self.spread_ratio * self.eth_df['Close'])

    def calc_spread_std_deviation(self):
        std = np.std(self.spread)
        return std

    def calc_p_score(self):
        z_score = self.spread.iloc[-1] / self.calc_spread_std_deviation()
        p_value = 1 - stats.norm.cdf(z_score)
        return p_value
    
    def signal(self, p):
        # check if p value meets threshodl
        if p > self.p_threshodl:
            return None
        
        # check which token to long and short
        btc_value = self.btc_df.iloc[-1]['Close']
        eth_value = self.eth_df.iloc[-1]['Close'] * self.spread_ratio
        
        if btc_value > eth_value:
            # btc overvalued - short btc, long eth
            ratio_overvalued = True
        else:
            # eth overvalued - short eth, long btc
            ratio_overvalued = False

        # verify signal
        # macd = MACD(self.spread, window_fast=self.fast_period, window_slow=self.slow_period).macd().iloc[-1]

        # if not macd:
        #     return None

        if ratio_overvalued:
            # return {'BTC': 'short', 'ETH': 'long'}
            return {'BTC': 'sell', 'ETH': 'buy', 'position_type': 'open'}
        else:
            # return {'BTC': 'long', 'ETH': 'short'}
            return {'BTC': 'buy', 'ETH': 'sell', 'position_type': 'open'}
        
    def close(self):
        # condition - check p-value
        p = self.calc_p_score()
        # closes position

        # return trade data - checks which token to buy and sell
        pass

    def next(self):
        if self.in_position:
            # decide whether or not to close position
            decision = self.close()
            return decision
        else:
            # calculations
            p = self.calc_p_score()
            decision = self.signal(p)
            return decision

# btc_path = '/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/separate/4HOUR_BTC.csv'
# eth_path = '/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/separate/4HOUR_ETH.csv'
# pairs_trading = PairsTrading(pd.read_csv(btc_path), pd.read_csv(eth_path))

# print(pairs_trading.next())
