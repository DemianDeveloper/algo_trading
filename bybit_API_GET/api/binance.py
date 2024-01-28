# файл binance.py

# создаю класс Binance_api который предоставляет методы для взаимодействия с API биржи Binance.

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

class Binance_api:
    spot_link = "https://api.binance.com"
    futures_link = "https://fapi.binance.com"
    
    # Инициализация класса с передачей ключей API и опций фьючерсов
    def __init__(self, api_key=None, secret_key=None, futures=False):
        self.api_key = api_key
        self.secret_key = secret_key
        self.futures = futures
        
        # Выбор базовой ссылки в зависимости от использования фьючерсов
        if self.futures:
            self.base_link = self.futures_link
        else:
            self.base_link = self.spot_link
        
        # Формирование заголовка с использованием API ключа
        self.header = {
            'X-MBX-APIKEY': self.api_key
        }

    # Метод для отправки HTTP-запросов к серверу биржи
    def http_request(self, method, endpoint, params):
        """
        Отправляет http запрос на сервер торговой площадки

        :param endpoint: url адрес запроса
        :param method: тип запроса (GET, POST, DELETE)
        :param params: тело запроса (params)

        :return: :class:Response (requests.models.Response)
        """
        # Проверка типа запроса и формирование запроса
        if method == "GET":
            response = requests.get(url=self.base_link + endpoint, params=params, headers=self.header)
        else:
            print("Метод не известен!")
            return None

        # Если получен ответ, преобразуем его в формат JSON
        if response: 
            response = response.json() 
        # если нет (если пустой словарь), то применяем к нему ответ где будет пустой словарь   
        return response

    # Метод для получения текущей цены торгового символа
    def get_price_ticker(self, symbol: str = None):
        if self.futures:
            endpoint = "/fapi/v1/ticker/price"
        else:
            endpoint = "/api/v3/ticker/price"
        method = "GET"
        params = {}
        if symbol:
            params['symbol'] = symbol

        return self.http_request(method=method, endpoint=endpoint, params=params)

    # Метод для получения свечей (Klines) для заданного символа и интервала времени
    def get_klines(self, symbol: str, interval: str, startTime: int = None, endTime: int = None, limit=500):
        if self.futures:
            endpoint = "/fapi/v1/klines"
        else:
            endpoint = "/api/v3/klines"
        method = "GET"
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        # эти два параметра startTime и endTime добавим если их значения отличное от None(startTime: int = None, endTime: int = None)
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        return self.http_request(method=method, endpoint=endpoint, params=params)


    def get_order_book(self, symbol: str, limit=100):
        if self.futures:
            endpoint = "/fapi/v1/depth"
        else:
            endpoint = "/api/v3/depth"
        method = "GET"
        params = {
            'symbol': symbol,
            'limit': limit
        }

        return self.http_request(method=method, endpoint=endpoint, params=params)


    def get_open_interest(self, symbol: str):
        if self.futures:
            endpoint = "/fapi/v1/openInterest"
        method = "GET"
        params = {
            'symbol': symbol
        }



        return self.http_request(method=method, endpoint=endpoint, params=params)
    

    # пишу для Ratio 
    def get_long_short_ratio(self, symbol: str, period: int):
        if self.futures: 
            endpoint = '/futures/data/globalLongShortAccountRatio'
        method = 'GET'
        params = {
            'symbol': symbol,
            'period': period
        }

        return self.http_request(method=method, endpoint=endpoint, params=params)
