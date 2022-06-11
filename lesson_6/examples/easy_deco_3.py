"""Простейший декоратор-функция"""

import time
import requests


def timer(func):
    """Сам декоратор"""
    def wrapper(*args, **kwargs):
        """Обертка"""
        start = time.time()
        return_value = func(*args, **kwargs)
        end = time.time()
        print(f'Отправлен запрос на адрес {args[0]}. '
              f'Время выполнения: {round(end-start, 2)} секунд')
        return return_value
    return wrapper


@timer
def get_wp(url):
    """Делаем запрос"""
    res = requests.get(url)
    return res


get_wp('https://google.com')
