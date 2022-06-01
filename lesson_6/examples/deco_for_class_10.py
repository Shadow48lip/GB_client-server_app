"""Декорируем класс"""


def mod_bar(cls):
    """декоратор в виде функции"""
    # возвращает модифицированный класс
    def decorate(func):
        """возвращает декорированную функцию"""
        def new_func(self):
            """
            здесь вызываем исходную функцию
            и дополняем ее поведение
            """
            print(self.start_str)
            print("Логика декоратора")
            print(func())
            print(self.end_str)

        return new_func

    cls.show = decorate(cls.show)
    return cls


@mod_bar
class Test:
    """Простой класс"""
    def __init__(self):
        self.start_str = "Запуск декоратора"
        self.end_str = "Завершение декоратора"

    @classmethod
    def show(cls):
        """Метод класса"""
        return "Какая-то функциональность метода класса"


TEST_OBJ = Test()
TEST_OBJ.show()
