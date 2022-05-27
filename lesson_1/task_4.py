"""
Преобразовать слова «разработка», «администрирование», «protocol», «standard» из
строкового представления в байтовое и выполнить обратное преобразование (используя
методы encode и decode).
"""


def word_wrap(word):
    print('{:*^30}'.format(word))
    word_b = word.encode('utf-8')
    print(word_b)
    word_str = word_b.decode('utf-8')
    print(word_str)


words = ['разработка', 'администрирование', 'protocol', 'standard']

[word_wrap(word) for word in words]