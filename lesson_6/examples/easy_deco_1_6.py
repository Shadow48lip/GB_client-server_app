"""
Задача:
ПЕРЕД выполнением и ПОСЛЕ выполнения определёных функций
печатать заданный текст (одинаковый для всех функций)
-------------------------------------------------------
Возврат (получение) информации из функции some_func()
"""
from functools import wraps


def decorator(func):
    """Сам декоратор"""
    @wraps(func)
    def wrap(*args, **kwargs):
        """Обертка"""
        print('Операция ДО выполнения функции some_func()')
        print(f'Переданные аргументы: {args}, {kwargs}')
        print('-' * 50)
        f = func(*args, **kwargs)
        print('-' * 50)
        print('Операция ПОСЛЕ выполнения функции some_func()')
        return f
    return wrap


@decorator  # == decorator(some_func) !!!
def some_func(*args, **kwargs):
    """Какая-то логика"""
    print('Выполнение самой функции some_func()')
    print(f'Переданные аргументы: {args}, {kwargs}')
    main_info = "Важная информация!"
    return main_info


# ==========================================
print('=' * 50)
print('main_info из функции some_func() ==', some_func())
