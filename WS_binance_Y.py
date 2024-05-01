'''коннектор для запросов по webscoket на бирже binance
разобраны основные команды для SPOT и FUTURES'''


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

'''SPOT'''
# url = f'wss://stream.binance.com:443/ws/ethusdt@aggTrade={"/".join(str(e) for e in list)}'
# threading.Thread(target=SocketConn, args=('wss://stream.binance.com:443/ws/ethusdt@aggTrade',)).start()

# threading.Thread(target=SocketConn, args=('wss://stream.binance.com:443/ws/ethusdt@kline_1m',)).start()

# threading.Thread(target=SocketConn, args=('wss://stream.binance.com:443/ws/ethusdt@miniTicker',)).start()

# threading.Thread(target=SocketConn, args=('wss://stream.binance.com:443/ws/!miniTicker@arr',)).start()

# threading.Thread(target=SocketConn, args=('wss://stream.binance.com:443/ws/ethusdt@trade/ethusdt@kline_1m/!ticker@arr',)).start()

'''FUTURES'''
# threading.Thread(target=SocketConn, args=('wss://fstream.binance.com:443/ws/ethusdt@aggTrade',)).start()
threading.Thread(target=SocketConn, args=('wss://fstream.binance.com:443/ws/ethusdt@markPrice@1s',)).start()

