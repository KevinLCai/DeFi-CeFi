import ccxt
import os
from dotenv import load_dotenv
import asyncio
import websockets
import json
import pandas as pd
from getData import GetData
import datetime
import csv
from strategies.DummyStrategy import DummyStrategy
from api.api import Deal

TIMEFRAME = "4HOUR"
PAIRS = ["BTC/USDT", "ETH/USDT"]
FILE_TYPE = "combined"


load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

exchange = ccxt.binance(
    {
    'apiKey': API_KEY,
    'secret': API_SECRET
    }
)

# create a dictionary to map symbols to websockets
SOCKETS = {
    "BTC": "wss://stream.binance.com:9443/ws/btcusdt@kline_1m",
    "ETH": "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
}

def get_filename(symbol):
    return f"/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/daily_{symbol}.csv"

async def handle_message(message, symbol):
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print('Invalid JSON message received.')
        return

    print(symbol + "=============")
    print(message)

    candlestick = data['k']
    if not candlestick:
        print('No candlestick data found in message.')
        return
    
    # read data in
    # df = pd.read_csv(get_filename(symbol))
    df = pd.read_csv(get_filename("BTC"))
    new_row = {'Date':candlestick['t']/1000.0, 'Open': candlestick['o'], 'High': candlestick['h'], 'Low': candlestick['l'], 'Close': candlestick['c'], 'Volume': candlestick['v'], 'OpenInterest': candlestick['B']}
    # df = pd.DataFrame(new_row)
    # df = pd.concat([df, pd.DataFrame(new_row, index=[1])], ignore_index=True)

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
    # with open(get_filename(symbol), 'a', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(new_row.values)


async def connect_to_websocket(symbol):
    async with websockets.connect(SOCKETS[symbol]) as ws:
        while True:
            message = await ws.recv()
            await handle_message(message, symbol)

async def main():
    tasks = [connect_to_websocket(symbol) for symbol in SOCKETS.keys()]

    await asyncio.gather(*tasks)

asyncio.run(main())
