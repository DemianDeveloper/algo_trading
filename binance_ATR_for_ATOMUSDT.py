# поиск значения ATR (20 SMA на обычной шкале в пунктах) на 15 мин ТФ. 
# за 15 ноября 2023 года по инструменту
# монета ATOMUSDT (бинанс)

'''
у нас есть данные за 15-минутные бары с максимальной (high), минимальной (low) и закрывающей (close) ценами. 
Для каждого бара мы сначала рассчитываем True Range (TR) согласно первой формуле, 
а затем используем эти значения для расчета ATR по второй формуле.

Рассчитываем ATR(20) на 15 ноября 2023 года, используя 20 предыдущих баров. 
Формула ATR будет применяться последовательно для каждого бара, 
усредняя True Range с учетом предыдущих значений ATR.

Расчёт далее: 
Формула для расчета среднего истинного диапазона (ATR) 
с использованием простого скользящего среднего (SMA):

1.	Считаю True Range (TR) для каждого бара:
•	TR = max(high - low, abs(high - close_prev), abs(low - close_prev))

2.	ATR:
•	Сначала рассчитать первый ATR как простое скользящее среднее из первых 20 True Range (TR) значений.
•	Затем используйте следующую формулу для последующих значений ATR (i):
•	ATR(i) = [(ATR(i-1) * (n-1)) + TR(i)] / n, где n - количество периодов (20 в данном случае).
'''

import ccxt
import pandas as pd

# Устанавливаем символ, временной интервал и даты
symbol = 'ATOMUSDT'  # Binance формат
interval = '15m'
start_date = '2023-11-15T00:00:00Z'
end_date = '2023-11-16T00:00:00Z'

# Инициализируем Binance API
binance = ccxt.binance()

# Получаем данные с использованием Binance API
ohlcv = binance.fetch_ohlcv(symbol, interval, binance.parse8601(start_date), binance.parse8601(end_date))

# Строим DataFrame из полученных данных
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
df = pd.DataFrame(ohlcv, columns=columns)
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')  # Преобразуем timestamp в datetime

# Рассчитываем True Range (TR)
df['tr'] = df.apply(lambda row: max(row['high'] - row['low'], abs(row['high'] - row['close']), abs(row['low'] - row['close'])), axis=1)

# Рассчитываем ATR(20) с использованием простого скользящего среднего
n = 20
df['atr'] = df['tr'].rolling(window=n).mean()

# Выводим последнее значение ATR (20 SMA) на обычной шкале в пунктах
last_atr_value = df['atr'].iloc[-1]
print(f'Последнее значение ATR (20 SMA) на обычной шкале в пунктах: {last_atr_value}')





