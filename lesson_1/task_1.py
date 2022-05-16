"""
Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и
проверить тип и содержание соответствующих переменных. Затем с помощью
онлайн-конвертера преобразовать строковые представление в формат Unicode и также
проверить тип и содержимое переменных.
Конвертер: https://calcsbox.com/post/konverter-teksta-v-unikod.html
"""


def check_string(w_str, w_unicode):
    print(w_str)
    print(type(w_str))
    print('-------------------')
    print(w_unicode)
    print(type(w_unicode))
    print('-------------------\n')


check_string('разработка', '\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430')

check_string('сокет', '\u0441\u043e\u043a\u0435\u0442')

check_string('декоратор', '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440')

