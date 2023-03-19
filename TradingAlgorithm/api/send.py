from api import Historical
from api import Deal

# Send historical data to API Gateway
# historical = Historical("/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/combined/1DAY_BTCUSDT_ETHUSDT_ETCUSDT_LTCUSDT__combined.csv")
# historical.send_data()

# Send Deal data to API Gateway
deal = Deal()
deal.send_data()