"""
Каждое из слов «class», «function», «method» записать в байтовом типе. Сделать это необходимо
в автоматическом, а не ручном режиме, с помощью добавления литеры b к текстовому значению,
(т.е. ни в коем случае не используя методы encode, decode или функцию bytes) и определить тип,
содержимое и длину соответствующих переменных
"""


def word_wrap(word):
    word_b = eval(f'b\'{word}\'')

    print('{:*^30}'.format(word))
    print(word_b)
    print(type(word_b))
    print(len(word_b))


words = ['class', 'function', 'method']

[word_wrap(word) for word in words]
