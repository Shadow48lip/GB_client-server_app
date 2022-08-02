"""
Decorator for Class
Function as Decorator
"""


def my_decorator(person):
    # define a new display method
    def new_display(self):
        print('Name: ', self.name)
        print('Function Decorator')

    # replace the display with new_display
    person.display = new_display

    # return the modified student
    return person


@my_decorator
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
Name:  Ivanov
'''
# ============================
# after decorating
'''
Name:  Ivanov
Function Decorator
'''
