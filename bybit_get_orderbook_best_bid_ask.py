# Найти в документации Bybit ендпоинт Get Orderbook с глубиной 1, 
# получить для списка торговых пар лучший бид и лучший аск.  
# Найти пару с самый большим спредом между бидом и аском.

import hashlib
import hmac
import time
import requests


base_url = 'https://api.bybit.com/'
endpoint = 'v5/market/orderbook'


symbols = ['BTCUSDT', 'ETHUSDT', 'BNDUSDT', 'LINKUSDT', 'ARKUSDT']


params = {
    'symbol': '',
    'category': 'linear', 
    'limit': 1
}

# создаю переменные для хранения максимального спреда и соответствующей торговой пары. 
# Оба эти значения устанавливаются до того, как начнется цикл по торговым парам, 
# чтобы предоставить переменным начальные значения перед тем, как они будут использованы в цикле.

MaxSpread = 0 # используется для хранения максимального значения спреда между лучшим бидом и аском. 
# Начальное значение устанавливается в 0, 
# так как еще не было найдено ни одного спреда, 
# и 0 является хорошим начальным значением для сравнения.

MasSpreadSymbol = '' # используется для хранения торговой пары с самым большим спредом. 
# Начальное значение устанавливается в пустую строку (''), 
# так как на момент начала выполнения кода еще нет торговой пары с максимальным спредом. 
# Позже, при обнаружении пары с большим спредом, это значение будет обновлено на символ этой пары.

# Проходим по каждой торговой паре
for symbol in symbols: 
    params['symbol'] = symbol
    response = requests.get(url=base_url + endpoint, params=params)

    try:
        result = response.json()
    except requests.exceptions.JSONDecodeError:
        print(f"Failed to decode JSON response for symbol {symbol}")
        continue

    # Проверяем, что запрос успешен
    if 'retMsg' in result and result['retMsg'] == 'OK':
        # Получаем лучший бид
        bid = float(result['result']['b'][0][0])

        # Проверяем, что лучший бид не равен 0 (чтобы избежать деления на 0)
        if bid != 0:
            # Вычисляем спред и сравниваем с текущим максимальным спредом
            spread = (float(result['result']['a'][0][0]) - bid) / bid

            # Если текущий спред больше максимального, обновляем значения
            if spread > MaxSpread:
                MaxSpread = spread
                MasSpreadSymbol = symbol

# Выводим результат
print('Среди пар', ', '.join(symbols))
print('Самый большой спред у', MasSpreadSymbol)



