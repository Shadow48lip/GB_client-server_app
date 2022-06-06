"""
Задача:
ПЕРЕД выполнением и ПОСЛЕ выполнения определёных функций
печатать заданный текст (одинаковый для всех функций)
-------------------------------------------------------
Передача параметров через функцию обёртки
"""


def decorator(func):
    """Сам декоратор"""
    def wrap(*args, **kwargs):
        """Обертка"""
        print('Операция ДО выполнения функции some_func()')
        print(f'Переданные аргументы: {args}, {kwargs}')
        print('-' * 50)
        func(*args, **kwargs)
        print('-' * 50)
        print('Операция ПОСЛЕ выполнения функции some_func()')
    return wrap


@decorator  # == decorator(some_func) !!!
def some_func(*args, **kwargs):
    """Какая-то логика"""
    print('Выполнение самой функции some_func()')
    print(f'Переданные аргументы: {args}, {kwargs}')


some_func(1, 2, a=3, b=4)

# ==========================================
# Возможность передачи данных в декоратор - это здорово!
# Но как всё-таки вернуть имя и док-стринг для функции some_func() ?