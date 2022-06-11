"""
Поток с объектами-событиями (с комментариями)
"""

import threading

marks = {
    'Я-первый поток': ['EVENT_2', 'EVENT_1'],
    'Я-второй поток': ['EVENT_1', 'EVENT_2'],
}


def writer(mes, event_for_wait, event_for_set):
    """
    функция принимает на вход некий параметр, событие, которое ожидают
    и еще одно событие, для которого необходимо установить True
    :param mes:
    :param event_for_wait:
    :param event_for_set:
    :return:
    """
    for i in range(10):
        print('=' * 50)
        print(f'1={i}-mes={mes}, event_for_wait={marks[mes][0]}, event_for_set={marks[mes][1]}')
        print(f'EVENT_1={EVENT_1.is_set()}, EVENT_2={EVENT_2.is_set()}')

        # ожидать установки флага события в True
        # (т.е. потоки, чьи события == False, здесь останавливаются и ждут)
        event_for_wait.wait()

        print(f'2-mes={mes}, event_for_wait={marks[mes][0]}, event_for_set={marks[mes][1]}')
        print(f'EVENT_1={EVENT_1.is_set()}, EVENT_2={EVENT_2.is_set()}')

        # сбросить флаг события c True на False
        event_for_wait.clear()

        print(f'3-mes={mes}, event_for_wait={marks[mes][0]}, event_for_set={marks[mes][1]}')
        print(f'EVENT_1={EVENT_1.is_set()}, EVENT_2={EVENT_2.is_set()}')

        # выводим параметр
        print(f'{i} - {mes}')

        # устанавливаем флага события в True
        # потоки, которые его ожидают, активизируются
        event_for_set.set()

        print(f'4-mes={mes}, event_for_wait={marks[mes][0]}, event_for_set={marks[mes][1]}')
        print(f'EVENT_1={EVENT_1.is_set()}, EVENT_2={EVENT_2.is_set()}')


# определяем объекты-события
# это объекты-наблюдатели
EVENT_1 = threading.Event()
EVENT_2 = threading.Event()

# определяем потоки
# в каждом потоке запускаем на выполнение ф-цию writer
# args - позиционные аргументы для ф-ции writer
# 0 или 1, как выодимое значение
# EVENT_1, EVENT_2 - объекты событий
THR_1 = threading.Thread(target=writer, args=('Я-первый поток', EVENT_2, EVENT_1))
THR_2 = threading.Thread(target=writer, args=('Я-второй поток', EVENT_1, EVENT_2))

# устанавливаем значение True
# потоки, которые этого ждут - пробуждаются
print('========== установка собития #1 в True ==========')
print(f'before set: EVENT_1={EVENT_1.is_set()}, EVENT_2={EVENT_2.is_set()}')
EVENT_1.set()
print(f'after set: EVENT_1={EVENT_1.is_set()}, EVENT_2={EVENT_2.is_set()}')

# запускаем потоки
THR_1.start()
THR_2.start()

# ждем, пока завершатся запущенные потоки
# Ждем, пока поток не закончится. Это блокирует вызывающий поток до тех пор,
# пока поток, чей метод join() вызывается, не завершится
THR_1.join()
THR_2.join()
