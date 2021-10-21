"""
CPython implementation detail: In CPython, due to the Global Interpreter Lock,
only one thread can execute Python code at once (even though certain performance-oriented
libraries might overcome this limitation). If you want your application to make better
use of the computational resources of multi-core machines, you are advised to use
multiprocessing or concurrent.futures.ProcessPoolExecutor. However, threading is still
an appropriate model if you want to run multiple I/O-bound tasks simultaneously.
"""
import threading
from threading import Thread


def print_something(arg):
    print(threading.current_thread())
    print(f'{arg} - your arg')


for i in range(5):
    thread = Thread(target=print_something, args=(i,))
    thread.start()




