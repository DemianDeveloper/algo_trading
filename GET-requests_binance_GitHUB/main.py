#файл main.py
import api

client = api.Binance_api(futures=True)#инициилизируем client как Binance_api класс 
#и передаём ему свойство futures=True в качестве аргумента

# info = client.get_exchange_info()
# print(info)
# info.keys()


custom_symbol = "ADAUSDT"
# переменная custom_symbol снаружи функции имеет значение "ADAUSDT". 
tickers = client.get_price_ticker(symbol=custom_symbol)['price']
# При вызове функции get_price_ticker(symbol=custom_symbol), это значение передается внутрь функции. 
tickers = float(tickers)
# print(tickers)

interval_Binance = '5m'

# распечатать 5 свейчей 
klines = client.get_klines(symbol=custom_symbol, interval=interval_Binance, limit=5)
# print(klines)

# open_int = client.get_open_interes(symbol=symbol)
# print(open_int)

period_Binance = '5m'
LongShortAccountRatio = client.get_long_short_ratio(symbol=custom_symbol, period=period_Binance)
print(LongShortAccountRatio)