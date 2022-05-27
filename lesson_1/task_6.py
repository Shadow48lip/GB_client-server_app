"""
Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование»,
«сокет», «декоратор». Далее забыть о том, что мы сами только что создали этот файл и исходить из
того, что перед нами файл в неизвестной кодировке. Задача: открыть этот файл БЕЗ ОШИБОК вне
зависимости от того, в какой кодировке он был создан.
"""

import chardet

f_name = 'test_file.txt'
data_to_file = 'сетевое программирование\nсокет\nдекоратор'

with open(f_name, 'w', encoding='koi8-r') as f:
    f.write(data_to_file)

with open(f_name, 'rb') as fb:
    data_bytes = fb.read()
    charset = chardet.detect(data_bytes)['encoding']
    print('file codetable:', charset)

    data_str = data_bytes.decode(encoding=charset).encode('utf-8')
    print(data_str.decode('utf-8'))
