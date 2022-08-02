"""Простейший декоратор-функция"""

import time


def timer(func):
    """Сам декоратор"""
    def wrapper(*args, **kwargs):
        """Обертка"""
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print(f'Расчёт для функции {func.__name__}. '
              f'Время выполнения: {end-start} секунд')
        return return_value
    return wrapper


@timer
def get_list_loop(x):
    ll = []
    for idx in range(x):
        ll.append(idx)
    return ll


@timer
def get_list_comp(x):
    return [idx for idx in range(x)]


value = 10 ** 6
get_list_loop(value)
get_list_comp(value)
