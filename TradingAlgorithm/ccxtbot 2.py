import ccxt
import os
from dotenv import load_dotenv
import websocket
import json
import pandas as pd
from getData import GetData
import datetime
import csv
from strategies.DummyStrategy import DummyStrategy
from api.api import Deal

TIMEFRAME = "1HOUR"
PAIRS = ["BTC/USDT"]
FILE_TYPE = "combined"


FILENAME="/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/daily_BTC.csv"

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

exchange = ccxt.binance(
    {
    'apiKey': API_KEY,
    'secret': API_SECRET
    }
)


# Connect to the WebSocket and start listening for messages

SOCKET = "wss://stream.binance.com:443/ws/btcusdt@kline_1m"

def on_message(ws, message):
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print('Invalid JSON message received.')
        return
    
    candlestick = data['k']
    if not candlestick:
        print('No candlestick data found in message.')
        return
    
    # read data in
    df = pd.read_csv(FILENAME)
    new_row = {'Date':candlestick['t']/1000.0, 'Open': candlestick['o'], 'High': candlestick['h'], 'Low': candlestick['l'], 'Close': candlestick['c'], 'Volume': candlestick['v'], 'OpenInterest': candlestick['B']}
    
    df = pd.concat([df, pd.DataFrame(new_row, index=[1])], ignore_index=True)

    # # put through strategy
    strategy = DummyStrategy(df)
    decision = strategy.next()
    print(decision)

    if decision != 'hold':
        # create order
        symbol = PAIRS[0].split('/')[0]
        amount = 0.0001
        price = None # current market price

        # execute trade

        # order = exchange.create_order(symbol, 'limit', decision, amount, price)

        # if order:
        #     print("ORDER")
        # else:
        #     print("No Order")

        # if buy or sell send deal data to api gateway
        print("SYMBOL======")
        print(symbol)

        fees = 0.00001
        deal = Deal("CeFi", symbol, candlestick['t']/1000.0, decision, price, amount, fees)
        deal.send_data()
        print("DEAL SENT")

    # write to csv
    with open(FILENAME, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row.values())


def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")
    # Gets Market Data and writes to a csv
    data = collect_market_data()

    

def collect_market_data():
    # try find historical data
    try:
        df = pd.read_csv(
            '/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/daily_BTC.csv')
        # set the latest data point
        last_date = df["Date"].iloc[-1]
    except:
        last_date = None

    # get data from last date, if there is any data - append to csv

    # get_data = GetData(TIMEFRAME, PAIRS, FILE_TYPE, datetime.datetime.strptime(last_date, '%d%m%y'))
    # get_data.collect_data()

    data = pd.read_csv('/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/daily_BTC.csv')
    
    return data


ws = websocket.WebSocketApp(SOCKET,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            )

ws.run_forever()
