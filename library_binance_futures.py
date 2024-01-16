# Содержание
# Binance API
# Индикаторы: RSI, HA, ATR, supertrend, halftrend, WMA, HMA


from datetime import datetime
import time

import requests
from pandas import DataFrame
import pandas as pd
import numpy as np
import json

# BINANCE API
from binance.um_futures import UMFutures

pd.options.mode.chained_assignment = None

js_f = open('settings/settings.json')
SETTINGS = json.load(js_f)
js_f.close()

client = UMFutures(key=SETTINGS['API_KEY'], secret=SETTINGS['SECRET_KEY'])


def send_to_admin_a(text):
    apiToken = SETTINGS['BOT_TOKEN']
    chatID = SETTINGS['ADMIN_ID']
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': text})
        print(response.text)
    except Exception as e:
        print(e)

def get_json_data(path):
    json_data = open(path)
    data = json.load(json_data)
    json_data.close()

    return data

def init_file_log():
    f = open("log/log.txt", "a")
    f.write('\n')
    f.write('Start robot time: ' + datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    f.write('\n')
    f.close()


init_file_log()


def write_to_logs(string, symbol=''):
    string = str(string)
    if symbol:
        f = open('log/' + str(symbol) + ".txt", "a")
    else:
        f = open("log/log.txt", "a")
    f.write('\n' + datetime.now().strftime("%d.%m.%Y %H:%M:%S") + '\n')
    f.write(string)
    f.write(
        '\n----------------------------------------------------------')
    f.close()


def round_down(x, n):
    return float(str(x)[:int(n)+2])

def is_int(n):
    return int(n) == float(n)


def has_opened_position(SYMBOL):
    positions = client.account()['positions']
    for position in positions:
        if position['symbol'] == SYMBOL and float(position['initialMargin']) > 0 and not float(position['positionAmt']) == 0:
            return True
    return False


def get_opened_positions(SYMBOL):
    opened_positions = []

    positions = client.account()['positions']

    for position in positions:
        if position['symbol'] == SYMBOL and float(position['initialMargin']) > 0 and not float(
                position['positionAmt']) == 0:
            opened_positions.append(position)
    if opened_positions:
        df = DataFrame(opened_positions).iloc[:, :17]
        df.columns = ['symbol', 'initialMargin', 'maintMargin', 'unrealizedProfit', 'positionInitialMargin',
                      'openOrderInitialMargin', 'leverage', 'isolated', 'entryPrice', 'maxNotional', 'positionSide',
                      'positionAmt', 'notional', 'isolatedWallet', 'updateTime', 'bidNotional', 'askNotional']
    else:
        df = DataFrame(opened_positions)
    return df

def get_opened_position_direction(SYMBOL):
    opened_positions = []

    positions = client.account()['positions']

    for position in positions:
        if (position['symbol'] == SYMBOL) and (float(position['initialMargin']) > 0) and not float(position['positionAmt']) == 0:
            opened_positions.append(position)
    try:
        if float(opened_positions[0]['positionAmt']):
            if float(opened_positions[0]['positionAmt']) > 0:
                return 'BUY'
            else:
                return 'SELL'
    except:
        return False

    return False

def get_position_entry_price(symbol):
    if has_opened_position(symbol):
        position = get_opened_positions(symbol).tail(1)
        return float(position['entryPrice'].iloc[0])
    return False

def get_symbol_price(SYMBOL):
    return float(client.ticker_price(symbol=SYMBOL)['price'])

def close_opened_positions_by_market(SYMBOL):
    opened_positions = []
    positions = client.account()['positions']

    for position in positions:
        if position['symbol'] == SYMBOL and float(position['initialMargin']) > 0 and not float(position['positionAmt']) == 0:
            opened_positions.append(position)

    for position in opened_positions:
        if float(position['positionAmt']) > 0:
            write_to_logs(SYMBOL + ' LONG Закрытие текущей сделки по рынку qnt: ' + str(abs(float(position['positionAmt']))), 'close_opened_positions_by_market')
            create_market_order(SYMBOL, 'SELL', abs(float(position['positionAmt'])), True)
        elif float(position['positionAmt']) < 0:
            write_to_logs(SYMBOL + ' SHORT Закрытие текущей сделки по рынку qnt: ' + str(abs(float(position['positionAmt']))), 'close_opened_positions_by_market')
            create_market_order(SYMBOL, 'BUY', abs(float(position['positionAmt'])), True)

    client.cancel_open_orders(symbol=SYMBOL)


def create_market_order(symbol, side, qnt, reduce_only=False):
    if not(qnt == 0):
        if side == 'BUY':
            print(str(symbol) + ' Рыночный ордер BUY ' + str(abs(qnt)))
            write_to_logs(symbol + ' Рыночный ордер BUY ' + str(abs(qnt)), 'create_market_order')
        else:
            print(str(symbol) + ' Рыночный ордер SHORT ' + str(abs(qnt)))
            write_to_logs(symbol + ' Рыночный ордер SHORT ' + str(abs(qnt)), 'create_market_order')

        if reduce_only:
            client.new_order(symbol=symbol, side=side, type='MARKET', quantity=abs(qnt), reduceOnly=True)
            send_to_admin_a(symbol + ' Закрытие позиции ' + side + ' ' + str(qnt))
        else:
            client.new_order(symbol=symbol, side=side, type='MARKET', quantity=abs(qnt))
            send_to_admin_a(symbol + ' Открытие новой позиции ' + side + ' ' + str(qnt))




def create_limit_order(symbol, side, price, qnt):
    if side == 'BUY':
        print(str(symbol) + ' созданна лимитка LONG: ' + str(price) + ' => ' + str(qnt))
        write_to_logs('созданна лимитка LONG: ' + str(price) + ' => ' + str(qnt), symbol)
        try:
            client.new_order(symbol=symbol, side='SELL', type='LIMIT', price=price, quantity=abs(qnt), timeInForce='GTC', reduceOnly=True)
            send_to_admin_a(symbol + ' Установка лимитки ' + side + str(price) + ' => ' + str(qnt))
        except Exception as err:
            print(symbol + f" Ошибка: Unexpected " + err.error_message)
            write_to_logs(symbol + f" Ошибка: Unexpected " + err.error_message, 'create_limit_order')
            send_to_admin_a(symbol + f" Ошибка:\n" + err.error_message)
            close_opened_positions_by_market(symbol)
    else:
        print(str(symbol) + ' созданна лимитка SHORT: ' + str(price) + ' => ' + str(qnt))
        write_to_logs('созданна лимитка SHORT: ' + str(price) + ' => ' + str(qnt), symbol)
        try:
            client.new_order(symbol=symbol, side='BUY', type='LIMIT', price=price, quantity=abs(qnt), timeInForce='GTC', reduceOnly=True)
            send_to_admin_a(symbol + ' Установка лимитки ' + side + str(price) + ' => ' + str(qnt))
        except Exception as err:
            print(symbol + f" Ошибка: Unexpected " + err.error_message)
            write_to_logs(symbol + f" Ошибка: Unexpected " + err.error_message, 'create_limit_order')
            send_to_admin_a(symbol + f" Ошибка:\n" + err.error_message)
            close_opened_positions_by_market(symbol)


def set_take_profit_market_order(symbol, side, price):
    print(str(symbol) + ' Установка TakeProfit: ' + str(price))
    write_to_logs('Установка TakeProfit: ' + str(price), symbol)

    try:
        client.new_order(symbol=symbol, side=side, type='TAKE_PROFIT_MARKET', stopPrice=price, closePosition=True)
    except Exception as err:
        print(symbol + f" Ошибка: Unexpected " + err.error_message)
        write_to_logs(symbol + f" Ошибка: Unexpected " + err.error_message, 'set_take_profit_market_order')
        send_to_admin_a(symbol + f" Ошибка:\n" + err.error_message)
        close_opened_positions_by_market(symbol)

def set_stop_loss_market_order(symbol, side, price):
    print(str(symbol) + ' Установка StopLoss: ' + str(price))
    write_to_logs('Установка StopLoss: ' + str(price), symbol)

    try:
        client.new_order(symbol=symbol, side=side, type='STOP_MARKET', stopPrice=price, closePosition=True)
        send_to_admin_a(symbol + " Установка StopLoss: " + str(price))
    except Exception as err:
        print(symbol + f" Ошибка: Unexpected " + err.error_message)
        write_to_logs(symbol + f" Ошибка: Unexpected " + err.error_message, 'set_stop_loss_market_order')
        send_to_admin_a(symbol + f" Ошибка:\n" + err.error_message)
        close_opened_positions_by_market(symbol)


def get_symbol_quantity(symbol, leverage, volume_percent, symbol_price, lot_precision):
    for s in client.exchange_info()['symbols']:
        if s['symbol'] == symbol:
            if s['marginAsset']:
                for i in client.balance():
                    if i['asset'] == s['marginAsset']:
                        return round(float(leverage) * (float(i['balance']) / 100 * float(volume_percent)) / symbol_price, lot_precision)

def get_user_balance():
    user_account = client.account()

    return float(user_account['totalWalletBalance']) - float(user_account['totalUnrealizedProfit'])

def close_long_positions(positions):
    for position in positions:
        if float(position['initialMargin']) > 0 and not float(position['positionAmt']) == 0:
            if float(position['positionAmt']) > 0:
                close_opened_positions_by_market(position['symbol'])

def close_short_positions(positions):
    for position in positions:
        if float(position['initialMargin']) > 0 and not float(position['positionAmt']) == 0:
            if float(position['positionAmt']) < 0:
                close_opened_positions_by_market(position['symbol'])
def get_candels(symbol, TM, limit=1500, slice=False):
    klines = client.klines(symbol, TM, limit=limit)
    if slice:
        if klines[-1][6] - time.time() * 1000 > 0:
            klines.pop()
    for i, val in enumerate(klines):
        klines[i][0] = float(klines[i][0])
        klines[i][1] = float(klines[i][1])
        klines[i][2] = float(klines[i][2])
        klines[i][3] = float(klines[i][3])
        klines[i][4] = float(klines[i][4])
    df = DataFrame(klines).iloc[:, :5]
    df.columns = ['Time', 'Open', 'High', 'Low', 'Close']
    return df

#ИНДИКАТОРЫ
def RSI(df, periods=14, ema=True):
    close_delta = df['Close'].diff()

    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)

    if ema == True:
        # Use exponential moving average
        ma_up = up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        ma_down = down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window=periods, adjust=False).mean()
        ma_down = down.rolling(window=periods, adjust=False).mean()

    rsi = ma_up / ma_down
    rsi = 100 - (100 / (1 + rsi))
    return rsi


def HA(df):
    df_close = df._get_value(0, 'Close')
    df_open = df._get_value(0, 'Open')
    df['Close'] = (df['Open'] + df['High'] + df['Low'] + df['Close']) / 4

    for i in range(0, len(df)):
        if i == 0:
            df._set_value(i, 'Open', ((df_open + df_close) / 2))
        else:
            df._set_value(i, 'Open', ((df._get_value(i - 1, 'Open') + df._get_value(i - 1, 'Close')) / 2))

    df['High'] = df[['Open', 'Close', 'High']].max(axis=1)
    df['Low'] = df[['Open', 'Close', 'Low']].min(axis=1)
    return df


def ATR(df, length=14):
    high_low = df['High'] - df['Low']
    high_cp = np.abs(df['High'] - df['Close'].shift())
    low_cp = np.abs(df['Low'] - df['Close'].shift())
    df_n = pd.concat([high_low, high_cp, low_cp], axis=1)
    true_range = np.max(df_n, axis=1)

    return true_range.ewm(alpha=1 / length, min_periods=length, adjust=False).mean()


    # print(amplitude)
    # print(deviation)


def WMA(df, period):
    return df.rolling(period).apply(lambda x: ((np.arange(period) + 1) * x).sum() / (np.arange(period) + 1).sum(), raw=True)

def HMA(df, period):
    
    return WMA(WMA(df, period // 2).multiply(2).sub(WMA(df, period)), int(np.sqrt(period)))

def get_symbol_data(symbol):
    min_lot_size = 0
    lot_precision = 0
    price_precision = 0
    min_notional = 0
    symbol_price = get_symbol_price(symbol)
    for s in client.exchange_info()['symbols']:
        if s['symbol'] == symbol:
            rs = str(float(s['filters'][0]['tickSize']))
            if '1e' in rs:
                price_precision = int(rs[-1])
            else:
                price_precision = int(len(str(float(s['filters'][0]['tickSize'])).split(".")[1]))

            min_lot_size = float(s['filters'][1]['minQty'])
            if is_int(min_lot_size):
                # lot_precision = int(min_lot_size)
                lot_precision = 0
            else:
                try:
                    if '1e' in str(min_lot_size):
                        lot_precision = int(str(min_lot_size)[-1])
                    else:
                        lot_precision = len(str(min_lot_size).split(".")[1])
                except:
                    lot_precision = 0
            min_notional = float(s['filters'][5]['notional'])

            while min_lot_size * symbol_price < min_notional:
                min_lot_size = min_lot_size + float(s['filters'][1]['minQty'])

            min_lot_size = round(min_lot_size, lot_precision)

    return {
        'min_lot_size': min_lot_size,
        'lot_precision': lot_precision,
        'min_notional': min_notional,
        'symbol_price': symbol_price,
        'price_precision': price_precision
    }
