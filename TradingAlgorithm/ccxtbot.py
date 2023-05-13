from CCXT import CCXT
import os
from strategies.DummyStrategy import DummyStrategy
from strategies.MMR import MMR

# Example usage:
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

TIMEFRAME = "4HOUR"
TOKEN = "ETH/USDT"
params = {'momentum_window': 10, 'mean_reversion_threshold': 0.1}

# Instantiate the TradingAlgorithm object
trading_algorithm = CCXT(API_KEY, API_SECRET, TIMEFRAME, TOKEN, MMR, params)

# Run the trading algorithm
trading_algorithm.run()
