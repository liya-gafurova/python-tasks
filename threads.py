"""
CPython implementation detail: In CPython, due to the Global Interpreter Lock,
only one thread can execute Python code at once (even though certain performance-oriented
libraries might overcome this limitation). If you want your application to make better
use of the computational resources of multi-core machines, you are advised to use
multiprocessing or concurrent.futures.ProcessPoolExecutor. However, threading is still
an appropriate model if you want to run multiple I/O-bound tasks simultaneously.

Стоит ли преодолевать связанные c GIL сложности и тратить время на реализацию многопоточности?
Вот примеры ситуаций, когда многопоточность несёт с собой больше плюсов, чем минусов.

-Для длительных и несвязанных друг с другом операций ввода-вывода.
    Например, нужно обрабатывать ворох разрозненных запросов с большой задержкой на ожидание.
    В режиме «живой очереди» это долго  — лучше распараллелить задачу.
- Вычисления занимают более миллисекунды и вы хотите сэкономить время за счёт их параллельного выполнения.
    Если операции укладываются в 1 мс, многопоточность не оправдает себя из-за высоких накладных расходов.
- Число потоков не превышает количество ядер.
    В противном случае параллельной работы всех потоков не получается и мы больше теряем, чем выигрываем.
"""
import math
import os
import random
import threading
import time
import datetime
from threading import Thread

FILES_DIR = './files/'
NUMBER_OF_FILES = 1000
NUMBER_OF_LINES = 1000
THREAD_COUNT = os.cpu_count()


def create_file(i):
    with open(f'./files/{i}-file.txt', 'w') as new_file:
        for line_number in range(NUMBER_OF_LINES):
            new_file.write(str(random.randint(1, 1000000)))


for file in os.listdir(FILES_DIR):
    os.remove(os.path.join(FILES_DIR, file))


# # 0:00:00.763496 - time
# time_start = datetime.datetime.now()
# for j in range(NUMBER_OF_FILES):
#     create_file(j)
#
# time_finish = datetime.datetime.now()
# print(f'{time_finish - time_start} - time')


class MyThread(Thread):
    def __init__(self, a, b):
        super(MyThread, self).__init__()
        self.a = a
        self.b = b

    def run(self) -> None:
        print(f'current thread - {self.name}')
        for i in range(self.a, self.b):
            create_file(i)
        print(f'finished thread - {self.name}')


a_list = [i * math.floor(NUMBER_OF_FILES / THREAD_COUNT) for i in range(THREAD_COUNT)]
b_list = a_list[1:]
b_list.append(NUMBER_OF_FILES)
assert len(a_list) == len(b_list)


# 0:00:00.084930 - time --- не чистое время, так как считается время, как потоки запустились, но не доджилается заверщения
time_start = datetime.datetime.now()
for a, b in list(zip(a_list, b_list)):
    thread = MyThread(a, b)
    thread.start()
time_finish = datetime.datetime.now()
print(f'{time_finish - time_start} - time')

