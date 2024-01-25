#робот позволяет выводить график по выбранной паре 

import yfinance as yf
import plotly.graph_objects as go

# Загрузка данных по BTC-USD
btc_data = yf.download('BTC-USD', start='2022-01-01', end='2023-01-01')

# Создание свечного графика
candlestick = go.Candlestick(x=btc_data.index,
                              open=btc_data['Open'],
                              high=btc_data['High'],
                              low=btc_data['Low'],
                              close=btc_data['Close'])

# Создание макета
layout = go.Layout(title='BTC-USD Candlestick Chart',
                   xaxis=dict(title='Date'),
                   yaxis=dict(title='Price'))

# Создание фигуры и добавление свечного графика
fig = go.Figure(data=[candlestick], layout=layout)

# Сохранение графика в HTML файл
fig.write_html('btc_candlestick_chart.html')
