"""
Простейший декоратор-функция
Работаем с параметрами исходной функции
"""


def log(func):
    """Декоратор"""
    def decorated(*args, **kwargs):
        """Обертка"""
        res = func(*args, **kwargs)
        print(f'log: {func.__name__}({args}, {kwargs}) = {res}')
        return res
    return decorated


@log
def my_func(val_1, val_2):
    """Простое вычисление"""
    return val_1 * val_2


print('-- Функции с декораторами --')
my_func(14, 15)

# другой подход применения декоратора к функции func = log(func)

# func = log(func)
# func(14, 15)
