# торговый робот для пары BTCUSDT
# 1. реализован с помощью индикатор bolinger bands 
# 2. согласно стратегии робот должен открывать позицию в short у верхней границы BB, а открывать long у нижней границы
# 3. стратегию на минутных свечах любой ликвидной монеты с бинанс


import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Загрузка данных по BTC-USD
# btc_data = yf.download('BTC-USD', start='2022-01-01', end='2023-01-01')

# Загрузка данных по BTC-USD с минутной частотой
btc_data = yf.download('BTC-USD', start='2023-12-18', end='2023-12-22', interval='1m')


# SMA по свечам закрытиям(Close), с помощью rolling взяли период 20 и посчитали среднее
btc_data['SMA'] = btc_data['Close'].rolling(window=20).mean()

# полосы Болллинджера (строим с помощью стандартного отклонения).
btc_data['stddev'] = btc_data['Close'].rolling(window=20).std()

# границами BB принимаем отклонения от среднего
btc_data['Upper'] = btc_data['SMA'] + 2 * btc_data.stddev
btc_data['Lower'] = btc_data['SMA'] - 2 * btc_data.stddev

# СТРАТЕГИЯ
# сигнал на покупку, если уровень цены пересекает нижнюю линию
btc_data['buy_signal'] = np.where(btc_data.Lower > btc_data.Close, True, False)
# сигнал на продажу, если уровень цены пересекает верхнюю линию
btc_data['sell_signal'] = np.where(btc_data.Upper < btc_data.Close, True, False)

# СОЗДАНИЕ ГРАФИКА
fig = go.Figure()

# Добавление полос Боллинджера
fig.add_trace(go.Scatter(x=btc_data.index, y=btc_data['Upper'], mode='lines', line=dict(color='red'), name='Upper Band'))
fig.add_trace(go.Scatter(x=btc_data.index, y=btc_data['Lower'], fill='tonexty', mode='lines', line=dict(color='green'), fillcolor='gray', name='Lower Band'))

# Добавление цены закрытия и SMA
fig.add_trace(go.Scatter(x=btc_data.index, y=btc_data['Close'], mode='lines', line=dict(color='blue'), name='Close'))
fig.add_trace(go.Scatter(x=btc_data.index, y=btc_data['SMA'], mode='lines', line=dict(color='black'), name='SMA'))

# Добавление сигналов на покупку и продажу
fig.add_trace(go.Scatter(x=btc_data[btc_data['buy_signal']].index, y=btc_data[btc_data['buy_signal']]['Close'],
                         mode='markers', marker=dict(color='green', size=8), name='Buy Signal'))
fig.add_trace(go.Scatter(x=btc_data[btc_data['sell_signal']].index, y=btc_data[btc_data['sell_signal']]['Close'],
                         mode='markers', marker=dict(color='red', size=8), name='Sell Signal'))

# Настройка макета и легенды
fig.update_layout(title='Bollinger Bands, Signals, Price, and SMA',
                  xaxis=dict(title='Data'),
                  yaxis=dict(title='Price'),
                  showlegend=True)

# Отображение графика
fig.show()

# ЗАДАНИЕ РОБОТУ. ПОКУПАТЬ ВНИЗУ, ПРОДАВАТЬ ВВЕРХУ
buys = []
sells = []
open_pos = False

for i in range(len(btc_data)):
    if btc_data['Lower'].iloc[i] > btc_data['Close'].iloc[i]:
        if open_pos == False: 
            buys.append(i)
            open_pos = True
    elif btc_data['Upper'].iloc[i] < btc_data['Close'].iloc[i]:
        if open_pos:
            sells.append(i)
            open_pos = False

print(buys)
print(sells)

# ОБРАБОТАЕМ ДАННЫЕ, ЧТОБЫ ПОНЯТЬ ПРИБЫЛЬ / УБЫТОК 
merged = pd.concat([btc_data.iloc[buys].Close, btc_data.iloc[sells].Close], axis=1)
merged.columns = ['Buys', 'Sells']
print(merged)

# профит по сделкам
totalprofit = merged.shift(-1).Sells - merged.Buys
print(totalprofit)

# доходность сделки в %
relprofits = (merged.shift(-1).Sells - merged.Buys)/merged.Buys 
print(relprofits)

# средний % по сделкам 
relprofits.mean()
