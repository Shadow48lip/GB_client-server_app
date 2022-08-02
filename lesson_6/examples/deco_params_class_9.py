"""
Простейший декоратор-класс с параметром
"""

import time


class Sleep:
    """Класс-декоратор"""
    def __init__(self, timeout):
        self.timeout = timeout

    def __call__(self, func):
        def decorated(*args, **kwargs):
            """Обертка"""
            time.sleep(self.timeout)
            res = func(*args, **kwargs)
            print('Function {} was sleeping in class'.format(func.__name__))
            return res
        return decorated


@Sleep(3)
def factorial(param):
    """Вычисляем факториал"""
    if param <= 1:
        return 1
    else:
        return param * factorial(param - 1)


print(' -- Использован декоратор, реализованный через класс --')
print('!!! Обратите внимание на то, сколько раз будет вызван декоратор (рекурсия) !!!')
print(factorial(5))
