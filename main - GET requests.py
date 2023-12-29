# GET - обычные запросы, которые можно выполнить даже в браузере.
# POST - продвинутые запросы, требующие отправки определенным способом с передачей необходимых параметров.
# в этом коде только про запросы GET


import requests

url = 'https://api2.binance.com/api/v3/ticker/price'
# response = requests.get(url)
# result = response.json()


# print(response)
# print(response.text)
# print(result[3])
# print(result)


url2 = 'https://api2.binance.com/api/v3/klines'
# url2 = 'https://api2.binance.com/api/v3/klines?symbol=BNBUSDT&interval=5m'
dictionary = {
    'symbol': 'BNBUSDT', 
    'interval': '5m'
    # 'limit': 900

}


response = requests.get(url=url2, params=dictionary)
result = response.json()

# запрашиваю последнюю и предпоследнюю свечи 
kline_last = result[-1]
kline_previous = result[-2]


print(len(result))
print(result)
print(kline_previous)
print(kline_last)


# ОТВЕТ ВОЗВРАЩАЕТСЯ В ФОРМАТЕ
# [
#   [
#     1499040000000,      // Kline open time
#     "0.01634790",       // Open price
#     "0.80000000",       // High price
#     "0.01575800",       // Low price
#     "0.01577100",       // Close price
#     "148976.11427815",  // Volume
#     1499644799999,      // Kline Close time
#     "2434.19055334",    // Quote asset volume
#     308,                // Number of trades
#     "1756.87402397",    // Taker buy base asset volume
#     "28.46694368",      // Taker buy quote asset volume
#     "0"                 // Unused field, ignore.
#   ]
# ]

# вывожу цены закрытия последней и предыдущей 
print(kline_previous[4])
print(kline_last[4])