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
from concurrent import futures
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
# THREAD_COUNT = os.cpu_count()
THREAD_COUNT = 2


a_list = [i * math.floor(NUMBER_OF_FILES / THREAD_COUNT) for i in range(THREAD_COUNT)]
b_list = a_list[1:]
b_list.append(NUMBER_OF_FILES)
a_b = list(zip(a_list, b_list))
assert len(a_list) == len(b_list)


def count_time(function):
    def wrapper():
        time_start = datetime.datetime.now()
        function()
        time_finish = datetime.datetime.now()
        print(f'{time_finish - time_start} - {function.__name__} time')

        print(len(os.listdir(FILES_DIR)))
        for file in os.listdir(FILES_DIR):
            os.remove(os.path.join(FILES_DIR, file))

    return wrapper


def create_file(i):
    with open(f'./files/{i}-file.txt', 'w') as new_file:
        for line_number in range(NUMBER_OF_LINES):
            new_file.write(str(random.randint(1, 1000000)))


@count_time
def without_threads():
    for j in range(NUMBER_OF_FILES):
        create_file(j)


class MyThread(Thread):
    def __init__(self, a, b):
        super(MyThread, self).__init__()
        self.a = a
        self.b = b

    def run(self) -> None:
        for i in range(self.a, self.b):
            create_file(i)


@count_time
def with_threads_manual_start():
    threads = list()
    for a, b in list(zip(a_list, b_list)):
        thread = MyThread(a, b)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def create_files(ab):
    a, b = ab
    for i in range(a, b):
        create_file(i)

@count_time
def with_thread_pool():
    with futures.ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        executor.map(create_files, a_b)


without_threads()
with_threads_manual_start()
with_thread_pool()
