"""
Мультипроцессинг с функцией
subprocess vs multiprocessing:
https://stackoverflow.com/questions/13606867/what-is-the-difference-between-multiprocessing-and-subprocess
"""

import time
import multiprocessing


def clock(interval):
    """Простая функция"""
    while True:
        time.sleep(interval)
        print(interval)
        print(f"The time is {time.ctime()}")
        break


if __name__ == "__main__":
    PROC = multiprocessing.Process(target=clock, args=(3, ))
    PROC.daemon = True
    PROC.start()
    # PROC.join()
    print(f"The time of main process is {time.ctime()}")
    # time.sleep(4)
    # print(f"The time of main process is {time.ctime()}")

# Основной и дополнительный процесс запускаются вместе
# Сначала завершается основной процесс, и тут же - дополнительный (не успев завершиться!)
