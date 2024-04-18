# main_method2.py второй метод 

import threading
import time
import numpy as np
import api
from config import api_key, secret_key

symbol = "ETHUSDT"
interval = "1m"
limit = 50
socket = f'wss://fstream.binance.com/stream?streams={symbol.lower()}@kline_{interval}'
client = api.Binance_api(api_key=api_key, secret_key=secret_key, futures=True)


def condition(client, indicator_values):
    # Покупка:
    if indicator_values['previous_value'] <= 0 and indicator_values['last_value'] > 0:
        print("Buy!")
        market_order = client.post_market_order(symbol=symbol, side="BUY", qnt=5)
        print(market_order)

    # Продажа:
    elif indicator_values['previous_value'] >= 0 and indicator_values['last_value'] < 0:
        print("Sell!")
        market_order = client.post_market_order(symbol=symbol, side="SELL", qnt=5)
        print(market_order)

    else:
        print("Нет сигнала!")



def get_klines_closes(client, symbol, interval, limit):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    # print(klines)
    last_kline = klines[-1]
    if (time.time() * 1000) < last_kline[6]:
        klines.pop()
    nupay_klines = np.array(klines)
    close_prices = nupay_klines[:, 4].astype(float)
    return close_prices


def indicator_output(close_prices):
    ema_short = api.ema(data=close_prices, period=6)
    ema_long = api.ema(data=close_prices, period=12)
    # print(ema_short)
    # print(ema_long)
    new_values = ema_short - ema_long
    indicator_values = {
        'last_value': new_values[-1],
        'previous_value': new_values[-2]
    }
    return indicator_values


def execute_main(historical_closes):
    print(historical_closes)
    indicator_values = indicator_output(close_prices=historical_closes)
    condition(client=client, indicator_values=indicator_values)
    # print(self.close_price)


if __name__ == '__main__':
    ws_binance = api.Socket_conn_Binance2(socket)
    threading.Thread(target=ws_binance.run_forever).start()


