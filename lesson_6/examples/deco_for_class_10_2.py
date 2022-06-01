"""
Decorator for Class
Class as Decorator
"""


class MyDecorator:
    # accept the class as argument
    def __init__(self, name):
        self.person = name

    # accept the class's __init__ method arguments
    def __call__(self, name):
        # define a new display method
        def new_display(self):
            print('Name: ', self.name)
            print('Class Decorator')

        # replace display with new_display
        self.person.display = new_display

        # return the instance of the class
        obj = self.person(name)
        return obj


@MyDecorator
class Person:
    def __init__(self, name):
        self.name = name

    def display(self):
        print('Name:', self.name)


obj = Person('Ivanov')
obj.display()


# ============================
# before decorating
'''
Name: Ivanov
'''
# ============================
# after decorating
'''
Name: Ivanov
Class Decorator
'''
