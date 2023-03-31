from api import Historical
# from api import Deal

# Send historical data to API Gateway
# historical = Historical("/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/combined/1DAY_BTCUSDT_ETHUSDT_ETCUSDT_LTCUSDT__combined.csv")
# historical.send_data()

# Send Deal data to API Gateway
# deal = Deal('CeFi', 1, 'BTC', 1679787060.0, 1800, 0.1, 0.001)
# deal.send_data()

import requests

class Deal:
    def __init__(self, strategy, tokenID, timestamp, orderType, price, size, fees):
        # Might need to include which tokens are being traded - more data
        self.api_url = "http://localhost:3000/deal"
        self.data_to_send = {"strategy": strategy, "tokenID": tokenID,
                             "timestamp": timestamp, "orderType": orderType, "price": price, "size": size, "fees": fees}

    def send_data(self):
        response = requests.post(self.api_url, json=self.data_to_send)
        return response

deal = Deal("CeFi", "BTC", 
1679786302, "buy", 1600, 1, 0.001)
deal.send_data()