import pandas as pd

df = pd.read_csv(
    "TradingAlgorithm/data/daily_BTC.csv")

print(df.tail())
