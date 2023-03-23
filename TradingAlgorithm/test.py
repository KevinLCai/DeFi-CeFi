import websocket, json

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

# import websocket
# import json

# def on_message(ws, message):
#     print(message)

# def on_close(ws):
#     print("WebSocket connection closed")

# def main():
#     cc='btcusd'
#     interval='1m'
#     socket = f'wss://stream.binance.com:9443/ws/{cc}t@kline_{interval}'

#     try:
#         ws = websocket.WebSocketApp(socket, on_message=on_message, on_close=on_close)
#         ws.run_forever()
#     except Exception as e:
#         print("Exception raised:", e)

# if __name__ == "__main__":
#     main()
