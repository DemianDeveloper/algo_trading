# Краткое описание робота: 
# 1. робот ищет наиболее растущую монету на binance 
# 2. проверяет продолжает ли она движение 
# 3. заходит соблюдая TP/SL


from binance.um_futures import UMFutures
from keys import key, secret
import pprint
import requests
import time
from datetime import datetime

TELEGRAM_TOKEN = '***'
TELEGRAM_CHANNEL = '@***'
TF = '15m'
TP = 0.03
SL = 0.01
DEPOSIT = 10

client = UMFutures(key=key, secret=secret)

def send_message(text): #эта фукнция отправляет запрос в tg
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN) #Создается переменная url, 
    # содержащая URL-адрес API Telegram для отправки сообщения. 
    # В этот URL вставляется значение TELEGRAM_TOKEN с помощью форматирования строк.

    data = {
        'chat_id': TELEGRAM_CHANNEL,
        'text': text
    } #Создается словарь data, содержащий два ключа: 
    # 'chat_id', который указывает идентификатор чата или канала Telegram, на который нужно отправить сообщение, 
    # и 'text', который содержит текст сообщения.


    response = requests.post(url, data=data) #функция закончиться тут
#  Выполняется POST-запрос к адресу url с использованием библиотеки requests. 
# В теле запроса отправляются данные из словаря data.
# - Результат запроса сохраняется в переменной response

change ={}
data = client.ticker_24hr_price_change()
# pprint.pprint(data)

for i in data:#этим циклом вытаскиваем символ и изменение, на выходе получая словарь где будут все монеты с изменением цены
    change[i['symbol']] = float(i['priceChangePercent'])

# print(change)#на выходе вывели словарь ключ:значение 

def get_top_coin():# 1)получает все монеты за сутки
    data = client.ticker_24hr_price_change()
    change = {}
    for i in data:
        change[i['symbol']] = float(i['priceChangePercent'])

    coin = max(change, key=change.get)# 2)определяем монету по которой прошло макимальное изменения цены, 
    # перебрали и вернули макс.значение ключа 
    print(f"Top coin is: {coin}: {change[coin]}")# coin - это тикер, 
    send_message(f"Top coin is: {coin}: {change[coin]}")
    return coin

# get_top_coin()


def get_symbol_price(symbol): #получаем цену символа и переводим в USDT 
    price = round(float(client.ticker_price(symbol)['price']), 5) #округлил до 5 знака после запятой
    print(f"Price: {price}")
    send_message(f"Price: {price}")
    return price


def get_close_data(symbol): #4)получить информацию по закрытым свечам  
    klines = client.klines(symbol, TF, limit=1500)
    close = []
    for i in klines:
        close.append(float(i[4]))
    return close


# klines = client.klines(symbol, TF, limit=1500) #этим проверял как достаю свечи c binance 
# print(klines)


def get_trade_volume():
    volume = round(DEPOSIT/get_symbol_price(symbol), 1)
    # print(type(volume))
    print(f"Trade volume: {volume}")
    return volume


def open_market_order(symbol, volume): #открываем по рынку ордер 
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': volume,
    }

    response = client.new_order(**params)
    print(response)


def open_stop_order(symbol, price, volume):
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'STOP_MARKET',
        # 'timeInForce': 'GTC',
        'stopPrice': price,
        'quantity': volume,
    }

    response = client.new_order(**params)
    print(response)


def open_take_profit_order(symbol, price, volume):
    params = {
        'symbol': symbol,
        'side': 'SELL',
        'type': 'TAKE_PROFIT_MARKET',
        # 'timeInForce': 'GTC',
        'stopPrice': price,
        'quantity': volume,
    }

    response = client.new_order(**params)
    print(response)


def get_stop_loss_price():
    stop_loss_price = round(price - (price * SL), 4)
    print(f"Stop Loss: {stop_loss_price}")
    return stop_loss_price   


def get_take_profit_price():
    take_profit_price = round((price * TP + price), 4)
    print(f"Take Profit: {take_profit_price}")
    return take_profit_price


symbol = get_top_coin()
# price = get_symbol_price(symbol)
# volume = get_trade_volume() перенё в функцию if 
close = get_close_data(symbol)
open_position = False

# print(close)

while True: 
    if close[-2] > close[-3] and open_position == False:
        print("The coin is growing")
        send_message("The coin is growing")
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

    else:
        print('the coin is NOT growing')
        send_message('the coin is NOT growing')
        time.sleep(2)