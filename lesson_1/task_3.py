"""
Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в
байтовом типе.
"""


words = ['attribute', 'класс', 'функция', 'type']

for word in words:
    try:
        # print(eval(f'b\'{word}\''), end='')
        word_b = word.encode('ascii')
    except UnicodeEncodeError:
        print(f'"{word}" невозможно записать в байтовом типе')
    else:
        print(f'{word_b} байтовый вид строки "{word}"')