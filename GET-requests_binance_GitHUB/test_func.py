
# файл test_func.py
import requests

futures = True  
#когда у нас установлен флаг False мы запрашиваем спот, 
#если поставим True то это будте обращение к фьючерсам
if futures:
    base_link = "https://fapi.binance.com"
else:
    base_link = "https://api.binance.com"

# Задача - разобрать способ получения публичных данных с биржи Бинанс
symbol = "AXSUSDT"
limit = 5
base_url = "https://fapi.binance.com"
endpoint = "/fapi/v1/depth"

params = {
    "symbol": symbol,
    "limit": limit,

}

url = base_url + endpoint
# response = requests.get(url=url, params=params)
# result = response.json()
#
# print(result)

# Функция для выполнения запроса и получения результата в формате JSON
def get_result(url, params=None):
    response = requests.get(url, params=params)#это аналог такоже запроса
    # только через функцию # response = requests.get(url=url, params=params)
    result = response.json()
    return result

# Функция для получения текущей цены торгового символа
def get_price_ticker(symbol: str = None): #функция get_price_ticker вызывается с символом в качестве аргумента, 
# и она вернет текущую цену этого символа. Если символ не передан, то используется значение по умолчанию None.
#  (symbol: str = None) это список параметров функции, в нашем случае один параметр symbol который имеет тип str (строка). 
    # str = None указывает на то, что у параметра есть значение по умолчанию, и это значение равно None.

    if futures:
        endpoint = "/fapi/v1/ticker/price" #для фьючерсов
    else:
        endpoint = "/api/v3/ticker/price" #для спота
    method = "GET" #эта переменная будет отправлять в наш класс метод обращения
    # когда к публичным данным обращаемся, только метод GET  
    params = {}
    if symbol:
        params['symbol'] = symbol

    return get_result(url=base_link+endpoint, params=params)


response = get_price_ticker(symbol=symbol)
print(response)

"""""
ответ на споте без time
[Running] python -u "c:\Work\Blockchain\GitHub\test_func.py"
{'symbol': 'AXSUSDT', 'price': '7.20000000'}

[Done] exited with code=0 in 1.626 seconds

[Running] python -u "c:\Work\Blockchain\GitHub\test_func.py"
{'symbol': 'AXSUSDT', 'price': '7.20300', 'time': 1704710938109}

[Done] exited with code=0 in 2.176 seconds

"""
