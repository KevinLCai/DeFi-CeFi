import ccxt
import os
from dotenv import load_dotenv
import websocket
import json

# load_dotenv()

# API_KEY = os.getenv("BINANCE_API_KEY")
# API_SECRET = os.getenv("BINANCE_API_SECRET")

# exchange = ccxt.binance(
#     # {
#     # 'apiKey': API_KEY,
#     # 'secret': API_SECRET
#     # }
# )

# # Define your trading strategy
# def trading_strategy(ticker):
#     pass

# # Define the WebSocket message handler
# def handle_message(message):
#     if message['e'] == 'ticker':
#         print(message)
#         # Update moving average
#         # symbol = message['s']
#         # price = float(message['c'])
#         # exchange.fetch_ohlcv(symbol, timeframe='1d') # fetch historical data
#         # ticker = exchange.fetch_ticker(symbol) # fetch current ticker
#         # ma50 = sum([ohlcv[4] for ohlcv in exchange.ohlcv[symbol]]) / 50 # calculate moving average
#         # ticker['ma50'] = ma50
        
#         # # Implement trading strategy
#         # action = trading_strategy(ticker)
#         # if action == 'buy':
#         #     order = exchange.create_order(symbol, 'market', 'buy', 0.1)
#         #     print('Bought 0.1', symbol, 'at', ticker['c'])
#         # elif action == 'sell':
#         #     order = exchange.create_order(symbol, 'market', 'sell', 0.1)
#         #     print('Sold 0.1', symbol, 'at', ticker['c'])
#         # else:
#         #     print('Hold', symbol)

# Connect to the WebSocket and start listening for messages

socket = 'wss://stream.binance.com:9443/ws/btcusd/@kline_1m'

def on_message(ws, message):
    print(message)

def on_close(ws):
    print("CLOSED")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(socket, 
                                # on_open=on_open,
                                on_message=on_message,
                                # on_error=on_error,
                                on_close=on_close)
    
    ws.run_forever()