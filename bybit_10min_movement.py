#  алгоритм по следующей торговой логике: 
# 1.  На 5min монета сделала движение 10% (абсолютного значения)
# 2.  На 1min монета ушла во флэт 0.2 – 1% (абсолютного значения)
# 3.  Алгоритм улавливает движение BTC на 3min 0.2 – 1%  (абсолютного значения)
# 4.  Выставляется лимитный ордер на расстояние +0.8% от текущей цены. 
# 5.  Если пункты 1 – 3 не соблюдаются – ордер не выставляется. 


import ccxt
import pandas as pd
import time


api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

bybit = ccxt.bybit({
    'apiKey': api_key,
    'secret': api_secret,
})

# Функции для получения данных и проверки условий

def get_ohlcv(symbol, timeframe, limit=100):
    return bybit.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)

def check_movement_5min(data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['change'] = (df['close'] - df['open']) / df['open'] * 100
    if df['change'].abs().max() >= 10:
        return True
    return False

def check_flat_1min(data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['change'] = (df['close'] - df['open']) / df['open'] * 100
    if 0.2 <= df['change'].abs().max() <= 1:
        return True
    return False

def check_btc_movement_3min(data):
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['change'] = (df['close'] - df['open']) / df['open'] * 100
    if 0.2 <= df['change'].abs().max() <= 1:
        return True
    return False

def place_limit_order(symbol, price, amount):
    order = bybit.create_limit_buy_order(symbol, amount, price)
    return order

# Основной цикл алгоритма

def main():
    symbol = 'BTC/USDT'
    order_amount = 0.01  # это можем менять
    while True:
        try:
            # Получение данных
            data_5min = get_ohlcv(symbol, '5m', limit=12)  # последние 1 час данных
            data_1min = get_ohlcv(symbol, '1m', limit=15)  # последние 15 минут данных
            btc_data_3min = get_ohlcv('BTC/USDT', '3m', limit=20)  # последние 1 час данных

            # Проверка условий
            if check_movement_5min(data_5min) and check_flat_1min(data_1min) and check_btc_movement_3min(btc_data_3min):
                current_price = bybit.fetch_ticker(symbol)['last']
                limit_price = current_price * 1.008  # +0.8% от текущей цены

                # Выставление лимитного ордера
                order = place_limit_order(symbol, limit_price, order_amount)
                print(f'Order placed: {order}')
            else:
                print('Conditions not met, order not placed')

            time.sleep(60)  # Проверка каждую минуту

        except Exception as e:
            print(f'Error: {e}')
            time.sleep(60)

if __name__ == '__main__':
    main()
