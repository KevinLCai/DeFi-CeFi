import ccxt
import os
from dotenv import load_dotenv
import websocket
import json
import pandas as pd
from getData import GetData
import datetime
import csv

from api.api import Deal


class CCXT:
    def __init__(self, api_key, api_secret, timeframe, token_pair, strategy, strategy_params):
        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.TIMEFRAME = timeframe
        self.TOKEN_PAIR = token_pair
        self.FILENAME = f"/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/separate/{timeframe}_{token_pair.replace('/', '')}.csv"
        self.SOCKET = f"wss://stream.binance.com:443/ws/{token_pair.replace('/', '').lower()}@kline_{CCXT.timeframe_to_code(timeframe)}"
        print(self.SOCKET)
        self.Strategy = strategy
        self.strategy_params = strategy_params

        load_dotenv()

        self.exchange = ccxt.binance({
            'apiKey': self.API_KEY,
            'secret': self.API_SECRET
        })

        self.ws = websocket.WebSocketApp(self.SOCKET,
                                         on_open=self.on_open,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)

    @classmethod
    def timeframe_to_code(cls, timeframe):
        tftc = {"1MINUTE": '1m', "3MINUTE": "3m", "15MINUTE": "15m", "30MINUTE": "30m", "1HOUR": "1h", "2HOUR": "2h",
                                                "4HOUR": "4h", "12HOUR": "12h", "1DAY": "1d", "3DAY": "3d", "1WEEK": "1w"}
        return tftc[timeframe]

    def run(self):
        self.ws.run_forever()

    def on_open(self, ws):
        print("WebSocket opened...")
        pairs = [self.TOKEN_PAIR.replace('/', '')]

        if os.path.exists(self.FILENAME):
            # TODO: Implement getting data using the latest timestamp
            pass
        else:
            get_data = GetData(self.TIMEFRAME, pairs, 'separate', None)
            get_data.collect_data()
        print("Data collected...")

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            print('Invalid JSON message received.')
            return

        candlestick = data['k']
        if not candlestick:
            print('No candlestick data found in message.')
            return

        # Read data
        df = pd.read_csv(self.FILENAME)
        new_row = {'Date': candlestick['t'] / 1000.0, 'Open': candlestick['o'], 'High': candlestick['h'],
                   'Low': candlestick['l'], 'Close': candlestick['c'], 'Volume': candlestick['v'],
                   'OpenInterest': candlestick['B']}
        df = pd.concat([df, pd.DataFrame(new_row, index=[1])], ignore_index=True)

        # Apply strategy
        if not self.strategy_params:
            strategy = self.Strategy(df)
        else:
            strategy = self.Strategy(df, **self.strategy_params)
        decision = strategy.next()
        print(decision)

        if decision != 'hold':
            # Create order
            symbol = self.TOKEN_PAIR.split('/')[0]
            amount = 0.0001
            price = None  # current market price

            # Execute trade
            # order = self.exchange.create_order(symbol, 'limit', decision, amount, price)
            # if order:
            #     print("ORDER")
            # else:
            #     print("No Order")

            # If buy or sell, send deal data to API gateway
            print("Token traded:")
            print(symbol)

            fees = 0.00001
            deal = Deal("CeFi", symbol, candlestick['t'] / 1000.0, decision, price, amount, fees)
            deal.send_data()
            print("Deal sent to API:")
            deal.print_deal()

        # Write to CSV
        with open(self.FILENAME, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(new_row.values())

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("WebSocket closed.")