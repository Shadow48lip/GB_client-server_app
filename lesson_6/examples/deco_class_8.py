"""Простейший декоратор-класс"""


class Log:
    """Класс-декоратор"""
    def __call__(self, func):
        def decorated(*args, **kwargs):
            """Обертка"""
            res = func(*args, **kwargs)
            print(f'log: {func.__name__}({args}, {kwargs}) = {res}')
            return res
        return decorated


@Log()
def my_func(val_1, val_2):
    """Вычисление"""
    return val_1 ** val_2


print('-- Функции с декораторами --')
my_func(4, 5)

# другой подход применения декоратора к функции func2 = Log()(func2)
# func2 = Log()(my_func)
# func2(4, 5)
