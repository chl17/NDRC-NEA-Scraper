import func_timeout
from func_timeout import func_set_timeout
import time


@func_set_timeout(2.5)
def task():
    while True:
        print('a')
        time.sleep(3)


task()
