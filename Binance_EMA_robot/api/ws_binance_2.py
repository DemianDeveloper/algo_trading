# ws_binance2.py второй вариант 


import _thread
import json
import os
import traceback
import websocket
import threading
import time
from main_method2 import *

class Socket_conn_Binance2(websocket.WebSocketApp):
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
        self.historical_closes = get_klines_closes(client=client, symbol=symbol, interval=interval, limit=limit)


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
            threading.Thread(target=self.execute).start()
            # self.historical_closes = np.append(self.historical_closes, self.close_price)
            # self.historical_closes = self.historical_closes[-limit:]
            # threading.Thread(target=execute_main(historical_closes=self.historical_closes)).start()
            # print(self.historical_closes)
            # indicator_values = indicator_output(close_prices=self.historical_closes)
            # condition(client=client, indicator_values=indicator_values)

    # вся логика выполняется в этой функции не нагружая on_message
    def execute(self):
        self.historical_closes = np.append(self.historical_closes, self.close_price)
        self.historical_closes = self.historical_closes[-limit:]
        print(self.historical_closes)
        indicator_values = indicator_output(close_prices=self.historical_closes)
        condition(client=client, indicator_values=indicator_values)
        # print(self.close_price)



# symbol = 'ETHUSDT'
# interval = '1m'
# limit = 20
#
# socket = f'wss://fstream.binance.com/stream?streams={symbol.lower()}@kline_{interval}'
# ws_binance = Socket_conn_Binance(socket)
# threading.Thread(target=ws_binance.run_forever).start()
