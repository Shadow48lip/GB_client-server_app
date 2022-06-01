"""
The <dec_for_class> function decorates all methods of a class with a <decorator> function.
"""


def decorator(func):
    def wrap(*args, **kwargs):
        print(f"{'=' * 25} {func.__name__} {'=' * 25}")
        res = func(*args, **kwargs)
        print(f'Была вызвана функция {func.__name__} c параметрами {args}, {kwargs}.')
        return res
    return wrap


def dec_for_class(func_decor):
    """
    This decorator function takes a method from the class instance,
    modifies it, and returns the instance with the modified method.
    """
    def wrapper(cls):
        """
        Dunder method __getattribute__(self, name) is called to implement attribute accesses
        for instances of the class.
        https://docs.python.org/3/reference/datamodel.html#object.__getattribute__
        """
        get_method = cls.__getattribute__

        def modified_method(cls, name):
            method = get_method(cls, name)
            return func_decor(method)
        cls.__getattribute__ = modified_method
        return cls
    return wrapper


# @dec_for_class(decorator)
class Example:

    @staticmethod
    def method_1(*args, **kwargs):
        print(f'Method 1 for {args} {kwargs}')

    @staticmethod
    def method_2(*args, **kwargs):
        print(f'Method 2 for {args} {kwargs}')


ex = Example()
ex.method_1(10, 20, name='new_name')
ex.method_2(10, 20, name='new_name')
