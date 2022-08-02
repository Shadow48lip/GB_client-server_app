"""
Пример логера-декоратора, созданного с помощью класса, в котором
настроен дополнительный фильтр, а именно:
пишем только те логи, где в сообщении есть слово "фУнкция"
Более подробно: 
добавление фильтра: https://stackoverflow.com/questions/879732/logging-with-filters
удаление фильтра: https://stackoverflow.com/questions/59314525/how-to-remove-a-log-filter-formatter

Для исследования действия фильтра необходимо запустить не server.py, а
server_where_log_is_class.py
"""


import inspect
import logging
import sys

sys.path.append('../../')
import logs.config_client_log
import logs.config_server_log
from functools import wraps


class MyFilter(logging.Filter):
    """
    Фильтр позволяет записывать только те логи, которые удовлетворяют
    какому-либо дополнительному условию.
    В нашем случае - это наличие слова <ФУнкция>, где две первых буквы заглавные.
    """

    def filter(self, record):
        return "фУнкция" in record.getMessage()


class Log:
    def __init__(self, logger=None):
        """
        Это декоратор с параметром - именем логера. В client.py и server.py
        это будет:

        LOGGER = logging.getLogger('client')

        @Log(LOGGER)
        def function():
            pass

        Но в модуле utils.py параметр LOGGER мы указать не можем, поэтому
        по умолчанию, при вызове функции из utils.py, logger будет == None.
        """
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            parent_func_name = inspect.currentframe().f_back.f_code.co_name
            module_name = inspect.currentframe().f_back.f_code.co_filename.split("/")[-1]
            if self.logger is None:
                """
                Если декоратор вызван из utils.py, то параметр logger не задан.
                Значит, определяем (и связываем) наш логер по имени модуля module_name
                """
                logger_name = module_name.replace('.py', '')
                self.logger = logging.getLogger(logger_name)

            # создаём экземпляр класса нового фильтра и добавляем его в текущий логер
            new_filter = MyFilter()
            self.logger.addFilter(new_filter)
            print('List of filters after adding new_filter: ', self.logger.filters)

            # -- Сообщение, где <функция> написана как "фУнкция" (пройдёт фильтарцию) --
            self.logger.debug(f'фУнкция {func.__name__} вызвана из функции {parent_func_name} '
                              f'в модуле {module_name} с аргументами: {args}; {kwargs}')

            # -- Сообщение, где <функция> написана как "Функция" (НЕ пройдёт фильтарцию) --
            self.logger.debug(f'Функция {func.__name__} вызвана из функции {parent_func_name} '
                              f'в модуле {module_name} с аргументами: {args}; {kwargs}')

            # удаляем фильтр, иначе больше не запишется ни одно сообщение, где нет слова "фУнкция"
            self.logger.filters.remove(new_filter)
            print('List of filters after removing new_filter: ', self.logger.filters)

            result = func(*args, **kwargs)
            return result
        return wrapper
