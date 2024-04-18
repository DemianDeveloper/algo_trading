import json
import traceback
import websocket
import threading
import time

class Socket_conn_Binance(websocket.WebSocketApp):
    def __init__(self, url):
        super().__init__(
            url=url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        # self.run_forever()
        self.close_price = None

    def on_open(self, ws):
        print(ws, 'Websocket was opened')

    def on_error(self, ws, error):
        print('on_error', ws, error)
        print(traceback.format_exc())

    def on_close(self, ws, status, msg):
        print('on_close', ws, status, msg)
        exit()

    def on_message(self, ws, msg):
        data = json.loads(msg)
        # print(data)
        if 'data' in data and data['data']['k']['x']:
            self.close_price = float(data['data']['k']['c'])
            print("Print from Ws_connection>>", self.close_price)

    def get_close_price(self):
        return self.close_price

symbol = 'ETHUSDT'
interval = '1m'
limit = 20

socket = f'wss://fstream.binance.com/stream?streams={symbol.lower()}@kline_{interval}'
ws_binance = Socket_conn_Binance(socket)
threading.Thread(target=ws_binance.run_forever).start()

