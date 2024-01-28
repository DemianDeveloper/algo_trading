# файл bybit_bid_ask.py

from api.bybit import Bybit_api  # Используем правильный путь

def main():
    # Создание объекта класса Bybit_api
    trader = Bybit_api()

    # Получение лучшего бида, лучшего аска и пары с максимальным спредом
    best_bid, best_ask, selected_pair = trader.get_best_bid_ask_pair()

    # Вывод результатов
    print(f"For the pair {selected_pair}, the best bid is {best_bid} and the best ask is {best_ask}")
    print(f"The maximum spread for any pair is {best_ask - best_bid}")

if __name__ == "__main__":
    main()
