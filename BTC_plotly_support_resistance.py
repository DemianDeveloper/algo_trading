# вывел график BTC за прошлый год 
# обозначил линию поддержки на 16к и сопротивления на 18к разными цветами 


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

# Создание макета
layout = go.Layout(title='BTC-USD Candlestick Chart with Support and Resistance Lines',
                   xaxis=dict(title='Date'),
                   yaxis=dict(title='Price'))

# Создание фигуры и добавление свечного графика и линий
fig = go.Figure(data=[candlestick, support_line, resistance_line], layout=layout)

# Сохранение графика в HTML файл
fig.write_html('btc_candlestick_chart_with_lines.html')
