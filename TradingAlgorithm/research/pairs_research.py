import pandas as pd

df = pd.read_csv(
    "TradingAlgorithm/data/combined/4HOUR_BTCUSDT_ETHUSDT__combined.csv")

print(df.corr())
