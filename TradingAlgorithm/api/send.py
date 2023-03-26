from api import Historical
from api import Deal

# Send historical data to API Gateway
# historical = Historical("/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/combined/1DAY_BTCUSDT_ETHUSDT_ETCUSDT_LTCUSDT__combined.csv")
# historical.send_data()

# Send Deal data to API Gateway
deal = Deal('CeFi', 1, 'ETH', 1679787060.0, 1800, 0.1, 0.001)
deal.send_data()