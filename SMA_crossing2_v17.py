
import pandas as pd
import numpy as np
import datetime
import requests
import time
# from integration.trading_lists import moex_list
from persistence.candles_repository import get_sql_history_price, create_heartbeating_table, upload_indicators_history, \
    connect_to_sql_database, get_futures_from_sql
# from integration.alor_client import get_moex_sql_history_price
# from moex_futures.requests_to_database import check_futures
from indicator.pivot_point_supertrend import pivot_point_supertrend

import sqlalchemy as sql
from sqlalchemy import or_, bindparam, create_engine, text, update
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from dateutil.relativedelta import relativedelta
from integration.binance_client import get_binance_historical_klines
from integration.trading_lists import tf_5m, tf_5m_str
from binance.client import Client
from pybit.unified_trading import HTTP
import re


mysqluser = "demian"
mysqlpassword = "_17Demian17"

import datetime
from pathlib import Path
import pandas as pd
import numpy as np

# Функция для тестирования стратегии на всех фьючерсах
def single_strategy_testing_crypto(start_time, end_time, exchange='Binance'):
    begining_time = datetime.datetime.now()
    print(f'Расчет начат: {begining_time}')    
    all_futures = get_all_futures()    
    
    all_futures = get_futures_from_sql(symbol, start_time, end_time, exchange)
    trades_df = pd.DataFrame(columns=[
        'timestamp', 'symbol', 'type', 'amount', 'price', 'cost',
        'open_time', 'open_price', 'cls_time', 'cls_price', 'cls_reason',
        'result_per', 'cumulat_per', 'drawdown', 'coin', 'strategy'
    ])
   
    for index, row in all_futures.iterrows():
        future = row["coin"]  
        from_time = start_time if start_time > (row["listed"] / 1000) else (row["listed"] / 1000)
        to_time = end_time if end_time < (row["delisted"] / 1000) else (row["delisted"] / 1000)
        
        print(f'Тестируем монету {future}')
        
        df = strategy_SMA_crossing(future, from_time, to_time, short_window, long_window)  
        
        if len(df) > 0:
            df['coin'] = future  
            trades_df = pd.concat([trades_df, df], ignore_index=True)
    
    trades_df.sort_values(by='cls_time', ascending=True, inplace=True, ignore_index=True)
    trades_df['cumulat_per'] = round(trades_df['result_per'].cumsum(), 2)    
    trades_df['cum_max_per'] = round(trades_df['cumulat_per'].cummax(), 2)
    trades_df['drawdown'] = trades_df['cumulat_per'] - trades_df['cum_max_per']
    trades_df = normalize_dataframe_columns(trades_df)
    
    filename2 = f"t2_strategy_trades.xlsx"
    filepath2 = Path("testing", filename2)
    trades_df.to_excel(filepath2, index=False)
    
    finishing_time = datetime.datetime.now()
    it_takes = finishing_time - begining_time
    print(f'Расчет окончен: {finishing_time}.\n Всего на расчет ушло: {it_takes}')

    return trades_df