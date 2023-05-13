from MMR import MMR
import pandas as pd

params = {'momentum_window': 10, 'mean_reversion_threshold': 0.1}

df = pd.read_csv('/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/daily_BTC.csv')

strategy = MMR(df, **params)
# print(strategy.next())
print(type(df['Close'].mean()))