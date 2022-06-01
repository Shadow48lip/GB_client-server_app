"""
Задача:
ПЕРЕД выполнением и ПОСЛЕ выполнения определёных функций
печатать заданный текст (одинаковый для всех функций)
-------------------------------------------------------
Постановка задачи
(A decorator in Python is any callable object
that modifies existing functions or classes.)
"""


def decorator(func):
    print('Операция ДО выполнения функции some_func()')
    print('-' * 50)
    func()
    print('-' * 50)
    print('Операция ПОСЛЕ выполнения функции some_func()')


def some_func():
    """Какая-то логика"""
    print('Выполнение самой функции some_func()')


decorator(some_func)

# ==========================================
# func_with_decorator = decorator(some_func)
# print('Тип функции func_with_decorator : ', type(func_with_decorator))
# func_with_decorator()

# Однако попытка создать новую функцию func_with_decorator(), где совмещается
# функции decorator() и some_func() оказалась неудачной
