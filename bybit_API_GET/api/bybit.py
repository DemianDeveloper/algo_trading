# файл bybit.py

# создаю класс Bybit_api который предоставляет методы для взаимодействия с API биржи Binance.

# код предназначен для взаимодействия с API Binance для получения различной информации  
# текущие цены, история котировок, стакан заказов, открытый интерес и другие.


# внутри этого класса создаю функции, к которым далее буду обращаться из main.py
# Метод http_request отправляет HTTP-запрос на сервер торговой площадки и возвращает объект Response из библиотеки requests.
# Методы get_price_ticker, get_klines, get_order_book и get_open_interest используют метод http_request для выполнения конкретных 
# запросов к API Binance, таких как получение текущей цены, свечей, стакана и открытого интереса.

import hashlib
import hmac
import time
import requests


class Bybit_api:
    BASE_LINK = "https://api.bybit.com"

    # (True, если используется, False для рынка спот)
    futures = False

    # Инициализатор класса, вызывается при создании нового объекта
    def __init__(self, api_key=None, secret_key=None, futures=False):
        self.api_key = api_key
        self.secret_key = secret_key

        # Переменная, определяющая рынок (фьючерсы или спот) на основе переданного параметра
        self.futures = futures

        # Условие проверки переменной futures
        if self.futures:

            self.category = "linear"
        else:

            self.category = "spot"

        # Создаем словарь с хедерами, которые будут использоваться в запросах
        self.header = {
            # Здесь обычно содержатся параметры аутентификации, такие как таймстамп, подпись (sign),
            # и ключ API, 
            # "X-BAPI-TIMESTAMP": timestamp,
            # "X-BAPI-SIGN": sign,
            # "X-BAPI-API-KEY": self.api_key,

            # Окно приема (receive) для ограничения времени ожидания ответа от сервера, по умолчанию взято с bybit 5 сек = 5000мсек
            "X-BAPI-RECV-WINDOW": "5000",
        }
    '''
        Комментарии по использованию self:

        self.api_key и self.secret_key - переменные для хранения ключей API, принадлежащих экземпляру объекта класса.

        self.futures - переменная, представляющая рынок (фьючерсы или спот) для данного экземпляра класса. 
                self используется для обращения к этой переменной в методах класса.

        self.category - переменная, определяющая категорию рынка (линейные или спотовые) 
                на основе значения self.futures.

        self.header - словарь, содержащий хедеры для использования в запросах. 
                self используется для обращения к переменным и методам класса внутри инициализатора.
    '''

    def http_request(self, method, endpoint, params):
        """
        Отправляет http запрос на сервер торговой площадки

        :param endpoint: url адрес запроса
        :param method: тип запроса (GET, POST, DELETE)
        :param params: тело запроса (params)

        :return: :class:Response (requests.models.Response)
        """

        if method == "GET":
            response = requests.get(url=self.BASE_LINK + endpoint, params=params, headers=self.header)
        else:
            print("Метод не известен!")
            return None
        if response:
            response = response.json()
        return response


    def get_klines(self, symbol: str, interval: str, start: int = None, end: int = None, limit=200):
        endpoint = "/v5/market/kline"
        method = "GET"
        params = {
            'category': self.category,
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        if start:
            params['start'] = start
        if end:
            params['end'] = end
        return self.http_request(method=method, endpoint=endpoint, params=params)


    def get_server_time(self):
        endpoint = "/v5/market/time"
        method = "GET"
        params = {}

        return self.http_request(method=method, endpoint=endpoint, params=params)


    def get_tickers(self, symbol: str = None):
        endpoint = "/v5/market/tickers"
        method = "GET"

        # в параметрах функции вышу уже прописан symbol поэтому в этой функции мы не прописываем 
        params = {
            'category': self.category,
        }
        if symbol:
            params['symbol'] = symbol

        return self.http_request(method=method, endpoint=endpoint, params=params)


    # def get_tickers(self, symbol: str = None):
    #     endpoint = "/v5/market/tickers"
    #     method = "GET"
    #     params = {
    #         'category': self.category,
    #     }
    #     if symbol:
    #         params['symbol'] = symbol

    #     return self.http_request(method=method, endpoint=endpoint, params=params)

    def get_best_bid_ask_pair(self):
        tickers_data = self.get_tickers()  # Используем новый метод
        if 'result' in tickers_data and isinstance(tickers_data['result'], list):
            tickers = [entry['symbol'] for entry in tickers_data['result']]
        else:
            print("Ошибка при получении данных тикеров")
            return None

        max_spread = 0
        best_bid = 0
        best_ask = 0
        selected_pair = None

        for symbol in tickers:
            orderbook_data = self.http_request("GET", "/v5/market/orderbook", params={'symbol': symbol, 'depth': 1})

            if 'result' in orderbook_data and isinstance(orderbook_data['result'], list) and orderbook_data['result']:
                current_bid = orderbook_data['result'][0]['bids'][0]['price']
                current_ask = orderbook_data['result'][0]['asks'][0]['price']
            else:
                print(f"Ошибка при получении данных стакана для {symbol}")
                continue

            spread = current_ask - current_bid

            if spread > max_spread:
                max_spread = spread
                best_bid = current_bid
                best_ask = current_ask
                selected_pair = symbol

        return best_bid, best_ask, selected_pair
