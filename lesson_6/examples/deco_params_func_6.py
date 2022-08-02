"""Простейший декоратор-функция с параметром"""

import time
import requests


def decorator(iters):
    print('Этот декоратор!!!!')
    """Внешняя функция (формально - декоратор)"""
    def real_decorator(func):
        """Сам декоратор"""
        def wrapper(*args, **kwargs):
            """Обертка"""
            total_time = 0
            for i in range(iters):
                start = time.time()
                func(*args, **kwargs)
                end = time.time()
                delta = end - start
                total_time += delta
                print(f'#{i + 1}: {delta:.2f} sec')
            print(f'Среднее время выполнения: {total_time / iters:.2f} секунд')
        return wrapper
    return real_decorator


@decorator(10)
def get_wp(url):
    """Запрос"""
    res = requests.get(url)
    return res


get_wp('https://google.com')
# x = decorator(10)(get_wp)('https://google.com')
# print(x.__name__)
# print(x)
