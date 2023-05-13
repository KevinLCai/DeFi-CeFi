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
from strategies.PairsTrading import PairsTrading
from api.api import Deal

TIMEFRAME = "4HOUR"
PAIRS = ["BTC/USDT", "ETH/USDT"]
FILE_TYPE = "combined"
POSITION_SIZE = 50 # USD
PRODUCTION = False

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

btc_candle_received = False
eth_candle_received = False
in_position = False

def get_filename(symbol):
    return f"/Users/kevincai/Library/Mobile Documents/com~apple~CloudDocs/Career/CV/DeFi_Trading/DeFi-CeFi/TradingAlgorithm/data/separate/4HOUR_{symbol}.csv"

async def handle_message(message, symbol):
    global btc_candle_received, eth_candle_received, in_position
    if symbol == "BTC":
        btc_candle_received = True
    elif symbol == "ETH":
        eth_candle_received = True
    else:
        raise Exception(f"Invalid Token: {symbol}")
    
    try:
        data = json.loads(message)
    except json.JSONDecodeError:
        print('Invalid JSON message received.')
        return
    
    print(f"{symbol} data received:")
    print(data)

    candlestick = data['k']
    if not candlestick:
        print('No candlestick data found in message.')
        return

    # format new row data
    new_row = {'Date':candlestick['t']/1000.0, 'Open': candlestick['o'], 'High': candlestick['h'], 'Low': candlestick['l'], 'Close': candlestick['c'], 'Volume': candlestick['v'], 'OpenInterest': candlestick['B']}

    # write to csv
    with open(get_filename(symbol), 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(new_row.values())
    print("Written candlestick to CSV")

    if not (btc_candle_received and eth_candle_received):
        return
    btc_candle_received = False
    eth_candle_received = False

    print("New tick data...")

    # read data in
    eth_df = pd.read_csv(get_filename("ETH"))
    btc_df = pd.read_csv(get_filename("BTC"))

    # # put through strategy
    strategy = PairsTrading(btc_df, eth_df, in_position)
    decision = strategy.next()

    print(f"{decision}")

    if decision:
        # create order
        btc_row = btc_df.iloc[-1]
        eth_row = eth_df.iloc[-1]

        btc_price = btc_row['Close'] # current market price
        eth_price = eth_row['Close']

        btc_order_amount = POSITION_SIZE / float(btc_price) # fixed value / market price
        eth_order_amount = POSITION_SIZE / float(eth_price) # fixed value / market price
        
        # execute trade in prod
        if PRODUCTION:
            # create ETH order
            eth_order = exchange.create_order("ETH", 'limit', decision["ETH"], eth_order_amount, eth_price)
            # create BTC order
            btc_order = exchange.create_order("BTC", 'limit', decision["BTC"], btc_order_amount, btc_price)
        
        # update global variable
        in_position = True

        # if buy or sell send deal data to api gateway
        fees = 0.00001
        btc_deal = Deal("CeFi", "BTC", candlestick['t']/1000.0, decision["BTC"], btc_price, btc_order_amount, fees)
        btc_deal_sent = btc_deal.send_data()

        eth_deal = Deal("CeFi", "ETH", candlestick['t']/1000.0, decision["ETH"], eth_price, eth_order_amount, fees)
        eth_deal_sent = eth_deal.send_data()
        if btc_deal_sent and eth_deal_sent:
            print("SUCCESS: Deal sent to API")
        else:
            print("ERROR: Deal data not sent to API")    


async def connect_to_websocket(symbol):
    async with websockets.connect(SOCKETS[symbol]) as ws:
        while True:
            message = await ws.recv()
            await handle_message(message, symbol)

async def main():
    tasks = [connect_to_websocket(symbol) for symbol in SOCKETS.keys()]

    await asyncio.gather(*tasks)

asyncio.run(main())
