from CCXT import CCXT
import os
from strategies.DummyStrategy import DummyStrategy

# Example usage:
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

TIMEFRAME = "4HOUR"
TOKEN = "ETH/BTC"

# Instantiate the TradingAlgorithm object
trading_algorithm = CCXT(API_KEY, API_SECRET, TIMEFRAME, TOKEN, DummyStrategy)

# Run the trading algorithm
trading_algorithm.run()

