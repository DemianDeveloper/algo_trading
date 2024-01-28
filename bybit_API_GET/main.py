import time
from datetime import datetime, timedelta
import api

def to_timestamp(data_string=None, format="%Y-%m-%d %H:%M:%S", delta=None):
    if data_string:
        date_time_obj = datetime.strptime(data_string, format)
        timestamp = int(date_time_obj.timestamp() * 1000)
    else:
        if delta:
            now = datetime.now()
            target_time = now + delta
            timestamp = int(target_time.timestamp() * 1000)

        else:
            return "Wrong paramethers!"

    return timestamp


# current_time = int(time.time() * 1000)
# print(current_time)
# # get the current date and time
# current_DateTime = datetime.now()
# # convert the current date and time into timestamp
# currentTimestamp = datetime.timestamp(current_DateTime)
#
# print("The current date and time is:", current_DateTime)
# print("The current TimeStamp is:", currentTimestamp)

data_string = "2023-11-05 17:15:00"
delta = -timedelta(minutes=10) # минус ставим, чтобы на 10 минут назад. если минус убрать то на +10минут вперёд 

client = api.Bybit_api()
futures_client = api.Bybit_api(futures=True)

symbol = "BTCUSDT"
interval = "1" # время в минутах 

# klines = client.get_klines(symbol=symbol, interval=interval, limit=5) # выводим для 5ти свечей 
# print(klines)

# target_time = to_timestamp(delta=delta)
# f_klines = futures_client.get_klines(symbol=symbol, interval=interval, start=target_time, limit=4)
# print(f_klines)


# server_time = futures_client.get_server_time()
# print(server_time)

tickers = client.get_tickers(symbol="FILUSDT")
print(tickers)
