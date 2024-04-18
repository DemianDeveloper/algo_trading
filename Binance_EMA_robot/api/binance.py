import hashlib
import hmac
import time
import requests


class Binance_api:
    spot_link = "https://api.binance.com"
    futures_link = "https://fapi.binance.com"
    futures = False

    def __init__(self, api_key=None, secret_key=None, futures=False,
                 proxy_ip=None, proxy_port=None,
                 proxy_username=None, proxy_password=None):
        self.api_key = api_key
        self.secret_key = secret_key
        self.futures = futures
        self.proxy_ip = proxy_ip
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.base_link = self.futures_link if self.futures else self.spot_link
        self.header = {'X-MBX-APIKEY': self.api_key}
        if self.proxy_ip:
            self.proxies = {
                "http": f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_ip}:{self.proxy_port}",
                "https": f"http://{self.proxy_username}:{self.proxy_password}@{self.proxy_ip}:{self.proxy_port}",
            }
        else:
            self.proxies = None

    def gen_signature(self, params):
        param_str = '&'.join([f'{k}={v}' for k, v in params.items()])
        sign = hmac.new(bytes(self.secret_key, "utf-8"), param_str.encode("utf-8"), hashlib.sha256).hexdigest()
        return sign

    def http_request(self, method, endpoint, params=None, sign_need=False):
        """
        Отправляет http запрос на сервер торговой площадки

        :param endpoint: url адрес запроса
        :param method: тип запроса (GET, POST, DELETE)
        :param params: тело запроса (params)
        :param sign_need: проверка если нужно подставить подпись

        :return: :class:Response (requests.models.Response)
        """

        if params is None:
            params = {}

        # Добавляем в словарь, если необходимо, параметры для подписи - отпечаток времени и саму подпись.
        if sign_need:
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self.gen_signature(params)

        url = self.base_link + endpoint
        if method == "GET":
            response = requests.get(url=url, params=params, headers=self.header, proxies=self.proxies)
        elif method == "POST":
            response = requests.post(url=url, params=params, headers=self.header, proxies=self.proxies)
        elif method == "DELETE":
            response = requests.delete(url=url, params=params, headers=self.header, proxies=self.proxies)
        else:
            return print("Метод не известен!")
        if response:  # Проверяем если ответ не пустой - чтоб не получить ошибки форматирования пустого ответа.
            response = response.json()
        else:
            print(response.text)
        return response

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

    def get_open_interes(self, symbol: str):
        if self.futures:
            endpoint = "/fapi/v1/openInterest"
        else:
            print("Not for Spot!")
            return
        method = "GET"
        params = {
            'symbol': symbol
        }

        return self.http_request(method=method, endpoint=endpoint, params=params)

    def post_limit_order(self, symbol: str, side: str, quantity: float, price: float, newClientOrderId: str = None,
                         reduceOnly=False):
        if self.futures:
            endpoint = "/fapi/v1/order"
        else:
            endpoint = "/api/v3/order"
        method = "POST"
        params = {
            "symbol": symbol,
            "side": side,
            "type": "LIMIT",
            "quantity": quantity,
            "price": price,
            "timeInForce": "GTC"
        }

        if reduceOnly:
            params['reduceOnly'] = reduceOnly

        if newClientOrderId:
            params['newClientOrderId'] = newClientOrderId

        return self.http_request(method=method, endpoint=endpoint, params=params, sign_need=True)

    def post_market_order(self, symbol: str, side: str, quantity: float, newClientOrderId: str = None,
                          reduceOnly=False):
        if self.futures:
            endpoint = "/fapi/v1/order"
        else:
            endpoint = "/api/v3/order"
        method = "POST"
        params = {
            "symbol": symbol,
            "side": side,
            "type": "MARKET",
            "quantity": quantity,
        }

        if newClientOrderId:
            params['newClientOrderId'] = newClientOrderId

        if reduceOnly:
            params['reduceOnly'] = reduceOnly

        return self.http_request(method=method, endpoint=endpoint, params=params, sign_need=True)

    def delete_cancel_order(self, symbol: str, orderId: int = None, origClientOrderId: str = None):
        if self.futures:
            endpoint = "/fapi/v1/order"
        else:
            endpoint = "/api/v3/order"
        method = "DELETE"
        params = {
            "symbol": symbol,
        }

        if orderId:
            params['orderId'] = orderId
        elif origClientOrderId:
            params['origClientOrderId'] = origClientOrderId

        else:
            print("Не указан параметр orderId")
            return

        return self.http_request(method=method, endpoint=endpoint, params=params, sign_need=True)

    def post_futures_trailing_stop_market_order(self, symbol, side, callbackRate, qnt, activationPrice: float = None,
                                                reduceOnly=True, workingType='CONTRACT_PRICE'):
        if self.futures:
            endpoint = "/fapi/v1/order"
            method = "POST"
            params = {
                "symbol": symbol,
                "side": side,
                "type": "TRAILING_STOP_MARKET",
                "callbackRate": callbackRate,  # The activation price as a percentage
                "quantity": qnt,
                "reduceOnly": reduceOnly,
                "workingType": workingType  # You can also use "MARK_PRICE"
            }

            if activationPrice:
                params['activationPrice'] = activationPrice
        else:
            print("Only for Futures market!")
            return

        return self.http_request(endpoint=endpoint, method=method, params=params, sign_need=True)

    def get_exchange_info(self, symbol: str = None, symbols=None):
        method = "GET"
        if self.futures:
            endpoint = '/fapi/v1/exchangeInfo'
            params = {}
        else:
            endpoint = '/api/v3/exchangeInfo'
            params = {'symbol': symbol} if symbol else {'symbols': symbols} if symbols else {}

        return self.http_request(endpoint=endpoint, method=method, params=params)

    def get_filter_details(self, our_symbol=None):
        result = {}
        raw_result = self.get_exchange_info()

        for symbol in raw_result['symbols']:
            look_symbol = symbol['symbol']
            if our_symbol and look_symbol != our_symbol:
                continue

            price_digit = lot_digit = min_notional = None
            for filter in symbol['filters']:
                if filter['filterType'] == 'PRICE_FILTER':
                    price_digit = int(filter['tickSize'].index('1') - 1)
                elif filter['filterType'] == 'LOT_SIZE':
                    lot_digit = int(filter['stepSize'].index('1') - 1) if float(filter['stepSize']) < 1 else 0
                elif filter['filterType'] == 'MIN_NOTIONAL' or (
                        not self.futures and filter['filterType'] == 'NOTIONAL'):
                    min_notional_key = 'notional' if filter['filterType'] == 'MIN_NOTIONAL' else 'minNotional'
                    min_notional = float(filter[min_notional_key])

            result[look_symbol] = {
                'min_notional': min_notional,
                'price_digit': price_digit,
                'lot_digit': lot_digit
            }

        return result.get(our_symbol, result)

