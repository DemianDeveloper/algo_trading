# запрос на binance через вебсокет
# получение данных в реальном времени по ETHUSDT 



import websocket
import traceback
import threading
import json

class SocketConn(websocket.WebSocketApp):
    def __init__(self, url):
        super().__init__(
        url=url,
        on_open=self.on_open, # открываем соединение 
        on_message = self.message,
        on_error = self.on_error,
        on_close = self.on_close #закрываем соединение 
        )

        self.run_forever()   


    def on_open(self, ws,):
        print(ws, 'Websocket was opened')
        

    def message(self, ws, msg):
        data = json.loads(msg)
        print(data)

    def on_error(self, ws, error):
        print('on_error', ws, error)
        print(traceback.format_exc())

    def on_close(self, ws, status, msg):
        print('on_close', ws, status, msg)
        exit()

list = [
    "ethusdt@kline_1m",
    "ethusdt@trade",
    "ethusdt@bookTicker"
]


# url = 'wss://fstream.binance.com/ws/!markPrice@arr'
# threading.Thread(target=SocketConn, args=(url,)).start()


url = f'wss://stream.binance.com:443/stream?streams={"/".join(str(e) for e in list)}'
threading.Thread(target=SocketConn, args=(url,)).start()