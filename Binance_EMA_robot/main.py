# main.py 

import threading
import time
import numpy as np
import api
from config import api_key, secret_key

# Инициализируем клиент класса для дальнейшей работы
client = api.Binance_api(api_key=api_key, secret_key=secret_key, futures=True)

symbol = 'ETHUSDT'
interval = '1m'
limit = 50

socket = f'wss://fstream.binance.com/stream?streams={symbol.lower()}@kline_{interval}'

# Функция ожидающая 1-ю секунду новой минуты.
def sleep_to_next_min():
    time_to_sleep = 60 - time.time() % 60 + 1
    print('sleep', time_to_sleep)
    time.sleep(time_to_sleep)

# ПОЛУЧАЕМ ЗАКРЫТЫЕ СВЕЧИ 
def get_klines_closed(client, symbol, interval, limit):
    # Получаем свечи с помощью метода get_klines объекта client
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    # ОБРАБОТКА ДАННЫХ
    last_kline = klines[-1]  # Получаем последнюю свечу из списка
    # Проверяем, если время закрытия последней свечи меньше текущего времени
    if (time.time() * 1000) < last_kline[6]:  # last_kline[6] содержит время закрытия свечи в миллисекундах
        klines.pop()  # Если условие выполняется, удаляем последнюю незакрытую свечу из списка

    numpy_klines = np.array(klines)  # Преобразуем список свечей в массив NumPy для удобства работы с данными
    close_prices = numpy_klines[:, 4]  # Получаем только цены закрытия из массива свечей
    close_prices = close_prices.astype(float)  # Преобразуем цены закрытия в тип данных float
    return close_prices  # Возвращаем массив цен закрытия

# ВЫЧИСЛЕНИЯ ИНДИКАТОРОМ
def indicator_output(close_prices):
    ema_short = api.ema(data=close_prices, period=6)
    ema_long = api.ema(data=close_prices, period=12)
    # print(ema_short)
    # print(ema_long)

    # вычисляются последние два значения разницы между коротким и длинным экспоненциальными скользящими средними. 
    # Это сделано для того, чтобы понять, в каком направлении движется разница между двумя скользящими средними.
    new_values = ema_short[-2:] - ema_long[-2:]

    # Два последних значения этой разницы сохраняются в словаре indicator_values под ключами 'last_value' и 'previous_value'. 
    # 'last_value' содержит последнее значение разницы, а 'previous_value' содержит предыдущее значение разницы.
    indicator_values = {
        'last_value': new_values[-1],
        'previous_value': new_values[-2]
    }
    return indicator_values

# ЛОГИКА ВХОДА: стратегия входа в позицию
def condition(indicator_values):
    # Покупка

    # эта строка означает, что мы ищем момент, когда значение индикатора было отрицательным или нулевым на предыдущем временном шаге, 
    # а на последнем временном шаге стало положительным.
    if indicator_values['previous_value'] <= 0 and indicator_values['last_value'] > 0:
        print("Buy!")  # Выводим сообщение о покупке
        # Здесь может быть код для выполнения реальной покупки на рынке, например:
        # market_order = client.post_market_order(symbol=symbol, side="BUY", qnt=5)
        # print(market_order)
        signal = "BUY"  # Возвращаем сигнал "BUY", чтобы указать на покупку

    # Продажа:
    elif indicator_values['previous_value'] >= 0 and indicator_values['last_value'] < 0:
        print("Sell!")  # Выводим сообщение о продаже
        # Здесь может быть код для выполнения реальной продажи на рынке, например:
        # market_order = client.post_market_order(symbol=symbol, side="SELL", qnt=5)
        # print(market_order)
        signal = "SELL"  # Возвращаем сигнал "SELL", чтобы указать на продажу

    else:
        print("No signal")  # Выводим сообщение о том, что нет сигнала
        return  # Возвращаем None, если нет сигнала

    return signal  # Возвращаем сигнал, который указывает на действие по стратегии (покупку, продажу)



def main():
    historical_closes = get_klines_closed(client=client, symbol=symbol, interval=interval, limit=limit)
    while True:
        # 1 Получение данных
        sleep_to_next_min()		# Ждем начало новой минуты
        if ws_binance.get_close_price(): #Получает текущую цену закрытия с помощью метода get_close_price объекта ws_binance

            #Обновляет исторические цены закрытия путем 
            # добавления последней цены в массив historical_closes и обрезки его до ограниченного лимита.
            historical_closes = np.append(historical_closes, ws_binance.get_close_price()) 
            historical_closes = historical_closes[-limit:]

            # 3 Отправка данных в индикатор
            indicator_values = indicator_output(historical_closes)
            print(indicator_values)
            # 5 Стратегия
            condition(indicator_values)


if __name__ == '__main__': #роверяет, запущен ли текущий скрипт напрямую, и если это так, выполняет слудеющие действия. если нет, не запускается 
    ws_binance = api.Socket_conn_Binance(url=socket) #Создается экземпляр объекта Socket_conn_Binance из модуля api, используя URL socket.
    
    # Создается новый поток с помощью модуля threading. Этот поток запускает метод run_forever объекта ws_binance, 
    # который, обрабатывает подключение к WebSocket и ожидает событий.
    threading.Thread(target=ws_binance.run_forever).start()
    main()



