# Робот позволяет: 
# 1. Посмотреть баланс своего кошелька на binance
# 2. Посмотреть открытые позиции по параметру: объём и результат
# 3. Посмотреть текущие лимитные позиции в шорт и лонг 
# 4. Закрыть все открытые позции



from binance.um_futures import UMFutures
from config import api_key, secret_key, TELEGRAM_TOKEN
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

import requests
import time
from datetime import datetime
import aiogram

bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot)
client = UMFutures(api_key, secret_key)

b1 = KeyboardButton('/balance')
b2 = KeyboardButton('/limits')
b3 = KeyboardButton('/positions')
b4 = KeyboardButton('/close_positions')

# расположение клавиатуры
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)  
# делаю маленькую клавиатура + чтобы не исчезала клавиатура
kb_client.add(b1).insert(b2).add(b3).insert(b4)


# Отправка клавиатуры пользователю
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await bot.send_messagesage(message.from_user.id, "бот запущен", reply_markup=kb_client)



@dp.message_handler(commands=['balance'])
async def balance(message: types.Message):
    balance = round(float(client.account()['availableBalance']), 1)
    await message.answer(f'Ваш баланс: {balance}')

# @dp.message_handler()
# async def echo(message: types.Message):
#     if message.text == 'Привет!':
#         await message.answer("И тебе привет!")


@dp.message_handler(commands=['limits'])
async def limits(message: types.Message):
        positions = client.account()['positions']
        for position in positions:
            if float(position['askNotional']) > 0:
                result = f"{position['symbol']} шорт {round(float(position['askNotional']))}"
                await message.answer(result)     

            if float(position['bidNotional']) > 0:
                result = f"{position['symbol']} лонг {round(float(position['bidNotional']))}"
                await message.answer(result)


@dp.message_handler(commands=['positions'])
async def position(message: types.Message):
    positions = client.account()['positions']
    for position in positions:
        if float(position['initialMargin']) > 0 and not float(position['positionAmt']) == 0:
            result = f"{position['symbol']} объем {position['positionAmt']} результат {position['unrealizedProfit']}"
            await message.answer(result)


@dp.message_handler(commands=['close_positions'])
async def close_position(message: types.Message):
    positions = client.account()['positions']
    for position in positions:
        if float(position['initialMargin']) > 0 and float(position['positionAmt']) < 0:
                order = client.new_order(position['symbol'], side='BUY',type='MARKET', quantity=abs(float(position['positionAmt'])), reduceOnly=True)
                await message.answer(f"Позиции по {position['symbol']} закрыты")

        elif float(position['initialMargin']) > 0 and float(position['positionAmt']) > 0:
                order = client.new_order(position['symbol'], side='SELL',type='MARKET', quantity=abs(float(position['positionAmt'])), reduceOnly=True)
                await message.answer(f"Позиции по {position['symbol']} закрыты")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)