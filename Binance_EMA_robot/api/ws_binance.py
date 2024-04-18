#ws_binance.py 
# Этот код определяет класс Socket_conn_Binance, предназначенный для подключения к Binance WebSocket API. 
# Вот пояснения к основным частям кода:

# on_message: Метод обратного вызова, который вызывается при получении сообщения по WebSocket. 
# Он обрабатывает сообщения и извлекает информацию о цене и свече (Kline).
# return_data: Метод, который возвращает текущую цену и цену закрытия свечи.
# stop_ws: Метод для закрытия WebSocket соединения.


# pip install websocket-client
import json
import traceback
import websocket
import threading
import time


class Socket_conn_Binance(websocket.WebSocketApp):
    def __init__(self, url, on_message):
        super().__init__(
            url=url,
            on_open=self.on_open,
            on_message=on_message,  # Измененно на передачу хэндлера в майн
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.price = None
        self.kline = None
        self.closed_kline = None

        # self.run_forever()

    def on_open(self, ws):
        print(ws, 'Websocket was opened')
        # time.sleep(15)
        # ws.close()

    def on_error(self, ws, error):
        print('on_error', ws, error)
        print(traceback.format_exc())
        exit()

    def on_close(self, ws, status, msg):
        print('on_close', ws, status, msg)
        exit()


# on_message: Метод обратного вызова, который вызывается при получении сообщения по WebSocket. 
# Он обрабатывает сообщения и извлекает информацию о цене и свече (Kline).
    def on_message(self, ws,  msg):
        # при обработке этого хэндлера в майн, тут не будет выполняться дальнейшая логика... Каждый выбирает что ему удобно
        data = json.loads(msg)#Преобразует строку msg в объект Python с помощью метода json.loads()

        # Проверяет, содержит ли объект data ключ 'data', и равен ли ключ 'stream' значению 'ethusdt@kline_1m'. Это условие 
        # используется для фильтрации сообщений только для определенного потока данных (свечи ETH/USDT с интервалом 1 минута).
        if 'data' in data and data['stream'] == 'ethusdt@kline_1m':
            # print(data)


            # Присваивает переменной self.kline данные о свече из полученного сообщения.
            self.kline = data['data']['k']
            # print(self.)

            # Присваивает переменной self.price значение закрытой цены свечи 
            # (поле 'c' в данных о свече), преобразуя его в число с плавающей точкой.
            self.price = float(self.kline['c'])
            # print(self.price)

            # Проверяет, есть ли в данных о свече поле 'x', которое, указывает на то, что свеча закрыта.
            if self.kline['x']:
                # print(self.kline)

                # Если свеча закрыта (поле 'x' равно истине), 
                # присваивает переменной self.closed_kline значение закрытой цены свечи и выводит это значение на экран.
                self.closed_kline = float(self.kline['c'])
                print(self.closed_kline)

            # if self.closed_kline and self.closed_kline < self.price:
            #     print("Мы перебили прошлый Хай...")
            #     print("Prices >", self.price, self.closed_kline)


# 'k' и ['c'] - это ключи, используемые для доступа к данным о свече (Kline)

# 'k': Этот ключ  используется для доступа к данным о свече внутри объекта данных. 
# содержит информацию о времени открытия, закрытия, минимальной, максимальной ценах за период свечи и другие связанные события.

# ['c']: Это обращение к значению закрытой цены свечи. В контексте данного кода данные о свече содержат поле 'c', 
# которое обозначает цену закрытия свечи.

# ключи взяты из библиотеки binance
# https://binance-docs.github.io/apidocs/spot/en/#trade-streams
#                 {
#   "e": "kline",     // Event type
#   "E": 1672515782136,   // Event time
#   "s": "BNBBTC",    // Symbol
#   "k": {
#     "t": 123400000, // Kline start time
#     "T": 123460000, // Kline close time
#     "s": "BNBBTC",  // Symbol
#     "i": "1m",      // Interval
#     "f": 100,       // First trade ID
#     "L": 200,       // Last trade ID
#     "o": "0.0010",  // Open price
#     "c": "0.0020",  // Close price
#     "h": "0.0025",  // High price
#     "l": "0.0015",  // Low price
#     "v": "1000",    // Base asset volume
#     "n": 100,       // Number of trades
#     "x": false,     // Is this kline closed?
#     "q": "1.0000",  // Quote asset volume
#     "V": "500",     // Taker buy base asset volume
#     "Q": "0.500",   // Taker buy quote asset volume
#     "B": "123456"   // Ignore
#   }
# }


# В коде self.kline = data['data']['k'] и self.price = float(self.kline['c']) мы обращаемся к данным о свече, 
# используя ключ 'k' для доступа к самой свече, а затем используем ключ ['c'] для получения значения закрытой цены этой свечи.


    def return_data(self):
        return self.price, self.closed_kline

    def stop_ws(self):
        self.close()

