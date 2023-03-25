import ccxt
import os
from dotenv import load_dotenv
import websocket
import json
import pandas as pd
from getData import GetData
import datetime

TIMEFRAME = "1HOUR"
PAIRS = ["ETHUSDT"],
FILE_TYPE = "combined",


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
    data = json.loads(message)
    print(data)
    # write to csv

    # put through strategy

    # buy/sell/hold

    # if buy or sell send deal data to api gateway

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
