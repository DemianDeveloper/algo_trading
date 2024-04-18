import numpy as np

def ema(data, period):
    # Создаем копию массива data с нулевыми значениями
    ema_values = np.zeros_like(data)
    # Считаем стандартный sma для первого периода, переменная mean используется для вычисления среднего значения (среднего арифметического) 
    sma = np.mean(data[:period])
    # Указыаем первое значение в последнем элементе первого перебора
    ema_values[period - 1] = sma
    # Создаем условный множитель для округления (сглаживания) значения к более свежим данным (важность)
    multiplier = 2 / (period + 1)
    # Применяем цыкл для перебора оставшегося массива и вычисления Экспоненциальной средней сколзящей.
    for i in range(period, len(data)):
        ema_values[i] = (data[i] - ema_values[i - 1]) * multiplier + ema_values[i - 1]

    return ema_values

