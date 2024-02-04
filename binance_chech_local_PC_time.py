
# проверка, что мой timestamp корректен и соответствует текущему времени Binance. 
# Если timestamp сильно отличается, запрос может быть отклонен.

import hashlib
import hmac
import time
import requests 

from config import api_key, secret_key

url_server_time = 'https://api.binance.com/api/v3/time'

# Получаем текущее время на сервере Binance
server_time_response = requests.get(url_server_time)
server_time = server_time_response.json()['serverTime']

# Мой текущий timestamp
your_timestamp = int(time.time() * 1000)

# Выводим оба времени для сравнения
print(f"Server Time: {server_time}")
print(f"Your Timestamp: {your_timestamp}")

# Сравниваем разницу во времени
time_difference = abs(server_time - your_timestamp)
print(f"Time Difference: {time_difference} milliseconds")


'''
пришёл ответ: 
Server Time: 1706800930700
Your Timestamp: 1706800930836
Time Difference: 136 milliseconds

Разница должна находится в пределах нескольких секунд. 
Если разница слишком велика, это может быть причиной отклонения запроса.
'''
