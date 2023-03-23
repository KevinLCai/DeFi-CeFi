import json
import requests
import os
from websocket import WebSocketApp
from dotenv import load_dotenv

SOCKET = "wss://stream.binance.com:9443/ws"
SYMBOL = "btcusdt"
INTERVAL = "1m"

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

ws_data = {
    "method": "SUBSCRIBE",
    "params":
    [
        f"{SYMBOL}@kline_{INTERVAL}"
    ],
    "id": 1,
    "key": API_KEY,
    "secret": API_SECRET
}

def getSocket(TOKEN):
    print(f'Retreiving {TOKEN} socket from: wss://stream.binance.com:9443/ws/{TOKEN.lower()}gbp@kline_1d')
    return f"wss://stream.binance.com:9443/ws/{TOKEN.lower()}usdt@kline_1d"

def on_message(ws, message):
    json_message = json.loads(message)
    candle = json_message['k']
    print(f"Candle open time: {candle['t']}, close price: {candle['c']}")
    
    # Make an authenticated API call
    headers = {
        'X-MBX-APIKEY': API_KEY
    }
    params = {
        'symbol': SYMBOL,
        'interval': INTERVAL,
        'limit': 1
    }
    response = requests.get('https://api.binance.com/api/v3/klines', headers=headers, params=params)
    print(response.json())


socket = WebSocketApp(getSocket("ETH"), on_message=on_message)

socket.on_open = lambda: socket.send(json.dumps(ws_data))

socket.run_forever()
