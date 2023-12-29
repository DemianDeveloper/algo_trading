# применяю 24hr Ticker Price Change Statistics от сюда: 
# https://binance-docs.github.io/apidocs/futures/en/#24hr-ticker-price-change-statistics
# для вывода фьючерсных пар

# вывожу пару которая наиболее росла
# вывожу пару которая больше всего упала за период 

import requests

url = 'https://fapi.binance.com/fapi/v1/ticker/24hr'

# Создаю список словарей, чтобы хранить информацию о нескольких монетах
symbols = ['BNBUSDT', 'SOLUSDT', 'BTCUSDT', 'ETHUSDT', 'DOTUSDT']

# Создаю список data_list, в котором каждый элемент представляет данные для одной монеты
data_list = []

for symbol in symbols:
    response = requests.get(url=url, params={'symbol': symbol})
    result = response.json()
    data_list.append(result)

# Вывод данных о каждой монете
for data in data_list:
    # Преобразование значения priceChange и priceChangePercent в проценты
    price_change_percent = float(data["priceChangePercent"])
    data["priceChangePercent"] = f"{price_change_percent:.2f}%"

    print({
        "symbol": data["symbol"],
        "priceChange": data["priceChange"],
        "priceChangePercent": data["priceChangePercent"],
        "weightedAvgPrice": data["weightedAvgPrice"],
        "lastPrice": data["lastPrice"],
        "lastQty": data["lastQty"],
        "openPrice": data["openPrice"],
        "highPrice": data["highPrice"],
        "lowPrice": data["lowPrice"],
        "volume": data["volume"],
        "quoteVolume": data["quoteVolume"],
        "openTime": data["openTime"],
        "closeTime": data["closeTime"],
        "firstId": data["firstId"],
        "lastId": data["lastId"],
        "count": data["count"]
    })

# Определение монеты, которая наиболее выросла в цене
# использую функцию max и лямбда-функцию для сравнения значений priceChangePercent.
max_price_change_coin = max(data_list, key=lambda x: float(x["priceChangePercent"][:-1]))
print("\nМонета, наиболее выросшая в цене:")
print({
    "symbol": max_price_change_coin["symbol"],
    "priceChange": max_price_change_coin["priceChange"],
    "priceChangePercent": max_price_change_coin["priceChangePercent"]
})

# Определение монеты, которая больше всего упала в цене
min_price_change_coin = min(data_list, key=lambda x: float(x["priceChangePercent"][:-1]))
print("\nМонета, наиболее упавшая в цене:")
print({
    "symbol": min_price_change_coin["symbol"],
    "priceChange": min_price_change_coin["priceChange"],
    "priceChangePercent": min_price_change_coin["priceChangePercent"]
})



