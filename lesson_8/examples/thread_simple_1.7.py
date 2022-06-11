"""
Сравнение производительности потоков при вычислениях
Все вычисления происходят ТОЛЬКО в главном потоке
"""

import time
from threading import Thread


def calculate_amount(min_index, max_index):
    """Функция, которая может быть запущена в потоке"""

    amount = 0
    for x in range(min_index, max_index):
        amount += (x * x) ** x


# THR1 = Thread(target=calculate_amount, args=(0, 5000))
# THR2 = Thread(target=calculate_amount, args=(5000, 10000))
# THR1.daemon = True
# THR2.daemon = True


print(f"Время запуска основной программы: {time.ctime()}")
time1 = time.time()
calculate_amount(0, 5000)
calculate_amount(5000, 10000)
time2 = time.time()
print(f'total = {time2 - time1:.2f}')

