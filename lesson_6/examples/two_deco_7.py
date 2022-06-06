"""
Два декоратора

(<ext_tag> [<int_tag> <Какой-то текст> </int_tag>] </ext_tag>)
"""


def make_ext(func):
    """Первый декоратор"""
    return lambda: "(<ext_tag> " + func() + " </ext_tag>)"


def make_int(func):
    """Второй декоратор"""
    return lambda: "[<int_tag> " + func() + " </int_tag>]"


@make_ext
@make_int
def my_func():
    """Какая-то логика"""
    return "Какой-то текст"


# порядок выполнения декораторов
# сначала make_ext, потом make_int
# func = make_ext(make_int(my_func))

print(my_func())


# def make_ext(func):
#     """Первый декоратор"""
#     def wrap(*args, **kwargs):
#         return "(<ext_tag> " + func() + " </ext_tag>)"
#     return wrap

