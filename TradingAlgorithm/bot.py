import websocket
import json

SOCKET = "wss://stream.binance.com:443/ws/btcusdt@kline_1m"

def on_message(ws, message):
    data = json.loads(message)
    print(data)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("WebSocket closed")

def on_open(ws):
    print("WebSocket opened")


ws = websocket.WebSocketApp(SOCKET,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close,
                            )

ws.run_forever()
