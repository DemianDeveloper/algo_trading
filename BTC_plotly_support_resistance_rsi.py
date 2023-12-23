# вывел график BTC за прошлый год 
# обозначил линию поддержки на 16к и сопротивления на 18к разными цветами 
# отключил навигационный график снизу
# добавил RSI под графиком. у графика цены и индикатора одна ось Х


import yfinance as yf
import plotly.graph_objects as go
import talib as ta
from plotly.subplots import make_subplots

# Загрузка данных по BTC-USD
btc_data = yf.download('BTC-USD', start='2022-01-01', end='2023-01-01')

# Создание свечного графика
candlestick = go.Candlestick(x=btc_data.index,
                             open=btc_data['Open'],
                             high=btc_data['High'],
                             low=btc_data['Low'],
                             close=btc_data['Close'], name='Price')

# Создание линии поддержки (красная)
support_line = go.Scatter(x=[btc_data.index[0], btc_data.index[-1]],
                          y=[16000, 16000],
                          mode='lines',
                          line=dict(color='red'),
                          name='Support Line')

# Создание линии сопротивления (зелёная)
resistance_line = go.Scatter(x=[btc_data.index[0], btc_data.index[-1]],
                             y=[18000, 18000],
                             mode='lines',
                             line=dict(color='green'),
                             name='Resistance Line')

# Создание индикатора RSI
rsi_values = ta.RSI(btc_data['Close'], timeperiod=14)
rsi_trace = go.Scatter(x=btc_data.index, y=rsi_values, name='RSI', yaxis='y2')

# Создание макета
layout = go.Layout(title='BTC-USD Candlestick Chart with Support, Resistance Lines, and RSI',
                   xaxis=dict(title='Date', title_standoff=2, showticklabels=False),  # Устанавливаем расстояние между названием оси X и графиками
                   yaxis=dict(title='Price', showticklabels=False),
                   yaxis2=dict(title='RSI', overlaying='y', side='right'),  # Вторая ось Y для RSI
                   xaxis_rangeslider_visible=False,  # Отключение навигационного графика
                   yaxis_title_standoff=2)  # Устанавливаем расстояние между названием оси Y и графиками

# Создание фигуры и добавление свечного графика, линий и RSI
fig = make_subplots(rows=3, cols=1, shared_xaxes=True, subplot_titles=('Price', 'Support and Resistance Lines', 'RSI'),
                    row_heights=[0.7, 0.15, 0.1], vertical_spacing=0.02)  # Устанавливаем высоту рядов и расстояние между ними

fig.add_trace(candlestick, row=1, col=1)
fig.add_trace(support_line, row=1, col=1)
fig.add_trace(resistance_line, row=1, col=1)
fig.add_trace(rsi_trace, row=3, col=1)

# Установка макета
fig.update_layout(layout)

# Сохранение графика в HTML файл
fig.write_html('btc_candlestick_chart_with_lines_and_rsi.html')
