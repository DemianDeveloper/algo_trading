# Краткое описание робота:
# 1. Робот ищет наиболее падающую монету на Binance (цена на которую упала больше).
# 2. Проверяет, продолжается ли движение цены вниз.
# 3. Заходит с соблюдением TP/SL (3/1)

from binance.um_futures import UMFutures
from keys import key, secret
import requests
import time

TELEGRAM_TOKEN = '***'
TELEGRAM_CHANNEL = '@***'
TF = '15m'
TP = 0.03
SL = 0.01
DEPOSIT = 10

client = UMFutures(key=key, secret=secret)

def send_message(text):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
    data = {'chat_id': TELEGRAM_CHANNEL, 'text': text}
    requests.post(url, data=data)

def get_top_coin():
    data = client.ticker_24hr_price_change()
    change = {}
    for i in data:
        change[i['symbol']] = float(i['priceChangePercent'])

    coin = min(change, key=change.get)
    print(f"Top falling coin is: {coin}: {change[coin]}")
    send_message(f"Top falling coin is: {coin}: {change[coin]}")
    return coin

def get_symbol_price(symbol):
    price = round(float(client.ticker_price(symbol)['price']), 5)
    print(f"Price: {price}")
    send_message(f"Price: {price}")
    return price

def get_close_data(symbol):
    klines = client.klines(symbol, TF, limit=1500)
    close = [float(i[4]) for i in klines]
    return close

def get_trade_volume():
    volume = round(DEPOSIT / get_symbol_price(symbol), 1)
    print(f"Trade volume: {volume}")
    return volume

def open_market_order(symbol, volume):
    params = {'symbol': symbol, 'side': 'SELL', 'type': 'MARKET', 'quantity': volume}
    response = client.new_order(**params)
    print(response)

def open_stop_order(symbol, price, volume):
    params = {'symbol': symbol, 'side': 'BUY', 'type': 'STOP_MARKET', 'stopPrice': price, 'quantity': volume}
    response = client.new_order(**params)
    print(response)

def open_take_profit_order(symbol, price, volume):
    params = {'symbol': symbol, 'side': 'BUY', 'type': 'TAKE_PROFIT_MARKET', 'stopPrice': price, 'quantity': volume}
    response = client.new_order(**params)
    print(response)

def get_stop_loss_price():
    stop_loss_price = round(price + (price * SL), 4)
    print(f"Stop Loss: {stop_loss_price}")
    return stop_loss_price

def get_take_profit_price():
    take_profit_price = round((price * (1 - TP)), 4)
    print(f"Take Profit: {take_profit_price}")
    return take_profit_price

symbol = get_top_coin()
close = get_close_data(symbol)
open_position = False

while True:
    if close[-2] < close[-3] and not open_position:
        print("The coin is falling")
        send_message("The coin is falling")
        volume = get_trade_volume()
        price = get_symbol_price(symbol)
        open_market_order(symbol, volume)
        send_message("The order was open")
        time.sleep(2)
        take_profit_price = get_take_profit_price()
        stop_loss_price = get_stop_loss_price()
        open_stop_order(symbol, stop_loss_price, volume)
        send_message("The was open Stop order")
        time.sleep(2)
        open_take_profit_order(symbol, take_profit_price, volume)
        send_message("The was open Take Profit order")
        open_position = True

    elif close[-2] > close[-3] and open_position:
        print('The coin is not falling')
        send_message('The coin is not falling')
        time.sleep(2)
        open_position = False

    else:
        print('The coin is not moving')
        send_message('The coin is not moving')
        time.sleep(2)
