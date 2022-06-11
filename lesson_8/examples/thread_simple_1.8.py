"""
Сравнение производительности потоков при вычислениях
Объём вычислений делится на 2 потока
"""

import time
from threading import Thread


def calculate_amount(min_index, max_index):
    """Функция, которая может быть запущена в потоке"""

    amount = 0
    for x in range(min_index, max_index):
        amount += (x * x) ** x


THR1 = Thread(target=calculate_amount, args=(0, 5000))
THR2 = Thread(target=calculate_amount, args=(5000, 10000))
THR1.daemon = True
THR2.daemon = True


print(f"Время запуска основной программы: {time.ctime()}")
time1 = time.time()

THR1.start()
THR2.start()
THR1.join()
THR2.join()
time2 = time.time()
print(f'total = {time2 - time1:.2f}')


