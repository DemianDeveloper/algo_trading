# торговый робот для пары BTCUSDT
# 1. реализован с помощью индикатор bolinger bands 
# 2. согласно стратегии робот должен открывать позицию в short у верхней границы BB, а открывать long у нижней границы
# 3. стратегию на минутных свечах любой ликвидной монеты с бинанс


# исправлено: 
# 1. сделка открывается, при пересечении полосы BB
# 2. на графике показаны только сделки, а не сигналы

# не могу построить точки закрытия



import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Загрузка данных по BTC-USD с минутной частотой
btc_data = yf.download('BTC-USD', start='2023-12-17', end='2023-12-23', interval='1m')


# SMA по свечам закрытиям (Close), с помощью rolling взяли период 20 и посчитали среднее
btc_data['SMA'] = btc_data['Close'].rolling(window=20).mean()

# полосы Болллинджера (строим с помощью стандартного отклонения).
btc_data['stddev'] = btc_data['Close'].rolling(window=20).std()

# границами BB принимаем отклонения от среднего
btc_data['Upper'] = btc_data['SMA'] + 2 * btc_data.stddev
btc_data['Lower'] = btc_data['SMA'] - 2 * btc_data.stddev


# СТРАТЕГИЯ
# сигнал на покупку, если уровень цены пересекает верхнюю линию
btc_data['buy_signal'] = (btc_data.Upper > btc_data.Close) & (btc_data.Upper.shift(1) <= btc_data.Close.shift(1))

# сигнал на продажу, если уровень цены пересекает нижнюю линию
btc_data['sell_signal'] = (btc_data.Lower < btc_data.Close) & (btc_data.Lower.shift(1) >= btc_data.Close.shift(1))

# Добавление столбца для отслеживания открытых сделок
btc_data['deal_open'] = False

# Закрытие сделок при пересечении средней линии
btc_data.loc[(btc_data.deal_open) & (btc_data.Close > btc_data.SMA), 'sell_signal'] = True
btc_data.loc[(btc_data.deal_open) & (btc_data.Close < btc_data.SMA), 'buy_signal'] = True

# Определение цветов точек в соответствии с условиями
btc_data['buy_color'] = np.where(btc_data['buy_signal'], 'green', 'rgba(0,0,0,0)')
btc_data['sell_color'] = np.where(btc_data['sell_signal'], 'red', 'rgba(0,0,0,0)')
btc_data['close_color'] = np.where(btc_data['deal_open'] & (btc_data.Close.shift(1) > btc_data.SMA.shift(1)),
                                   'black', 'rgba(0,0,0,0)')




# СОЗДАНИЕ ГРАФИКА
fig = go.Figure()
fig.show(config=dict({'scrollZoom': True}))

# Добавление полос Боллинджера
fig.add_trace(go.Scatter(x=btc_data.index, y=btc_data['Upper'], mode='lines', line=dict(color='red'), name='Upper Band'))
fig.add_trace(go.Scatter(x=btc_data.index, y=btc_data['Lower'], fill='tonexty', mode='lines', line=dict(color='green'), fillcolor='gray', name='Lower Band'))

# Добавление цены закрытия и SMA
fig.add_trace(go.Scatter(x=btc_data.index, y=btc_data['Close'], mode='lines', line=dict(color='blue'), name='Close'))
fig.add_trace(go.Scatter(x=btc_data.index, y=btc_data['SMA'], mode='lines', line=dict(color='black'), name='SMA'))

# Добавление точек
fig.add_trace(go.Scatter(x=btc_data[btc_data['buy_signal']].index, y=btc_data[btc_data['buy_signal']]['Close'],
                         mode='markers', marker=dict(color=btc_data['buy_color'], size=8), name='Buy Deal'))
fig.add_trace(go.Scatter(x=btc_data[btc_data['sell_signal']].index, y=btc_data[btc_data['sell_signal']]['Close'],
                         mode='markers', marker=dict(color=btc_data['sell_color'], size=8), name='Sell Deal'))
# fig.add_trace(go.Scatter(x=btc_data[btc_data.deal_open].index, y=btc_data[btc_data.deal_open]['Close'],
#                          mode='markers', marker=dict(color=btc_data['close_color'], size=8), name='Close Deal'))


# Добавление точек закрытия сделок
fig.add_trace(go.Scatter(x=btc_data[btc_data['deal_open'] & (btc_data.Close.shift(1) > btc_data.SMA.shift(1))].index,
                         y=btc_data[btc_data['deal_open'] & (btc_data.Close.shift(1) > btc_data.SMA.shift(1))]['Close'],
                         mode='markers', marker=dict(color='black', size=8), name='Close Deal'))


# Настройка макета и легенды с установкой масштабов для осей X и Y
fig.update_layout(title='Bollinger Bands, Deals, Price, and SMA',
                  xaxis=dict(title='Data', range=[btc_data.index.min(), btc_data.index.max()]),
                  yaxis=dict(title='Price', range=[btc_data['Close'].min(), btc_data['Close'].max()]),
                  showlegend=True)


# Отображение графика
fig.show()

# Сохранение графика в HTML файл
fig.write_html('your_graph.html')









