#!/usr/bin/python3

'''
Задание:

Написать функцию, которая будет возвращать цифру от 0 до 9, которая будет уникальна для любого треда, обратившегося к этой функции в единицу времени.
После выполнения работы тред должен вернуть в массив цифр свою цифру.
Пример: число тредов <= 10 => каждый тред получит любую свободную цифру из массива [0-9].
При количестве тредов > 10 => первые 10 получат любую свободную цифру из массива [0-9], остальные N - 10 тредов должны получить первую свободную цифру


'''

import logging
import sys
import time
import random
from threading import Thread

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

# Configuration on task

config = {
    'threads_count' : 12, # number of threads
    'threads_search_time' : 1, # search time, seconds
    'threads_work_time_min' : 10, # thread work time, minumum, seconds
    'threads_work_time_max' : 14, # thread work time, maximum, seconds
}

class Singleton(type):
    '''

    Singleton class

    '''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MyClass(metaclass=Singleton):
    '''

    Use metaclass

    '''

    def __init__(self, host = 'none'):
        '''

        Init list on constructor

        '''
        self.numbers = list(range(1, 11))

    def get_number(self):
        '''
        Function for get free number from list
        '''
        try:
            num = self.numbers.pop()
        except IndexError:
            # if list if empty, intercept exception, assign None
            num = None
        return num

    def return_number(self, num):
        '''
        Function for return number to free status
        '''
        return self.numbers.append(num)
    pass

class MyThread(Thread):
    """

    Class for thread

    """

    def __init__(self, name):
        """

        init thread

        """
        Thread.__init__(self)
        self.name = name

    def run(self):
        """

        run a thread

        """
        msg = "%s is running" % self.name
        print('[' + str(self.name) + '] ' + str(msg))
        self.process(self.name)

    def process(self, thread_name):
        '''
        function to task for thread
        :param sring thread_name: thread name for log
        :return:
        '''

        print('[' + str(thread_name) + '] start thread')
        # Create class object to work with list numbers
        a = MyClass()
        # get free number
        num = a.get_number()
        # While there are no free
        while (num is None):
            print('[' + str(thread_name) + '] Wait for free numbers..')
            # will wait
            time.sleep(config.get('threads_search_time'))
            # try get free number again
            num = a.get_number()
        print('[' + str(thread_name) + '] Yeap, i got num: ' + str(num))
        sleep_time = random.randint(config.get('threads_work_time_min'),config.get('threads_work_time_max'))
        # emulation of work
        time.sleep(sleep_time)
        # return number to free stasus
        num = a.return_number(num)
        print('[' + str(thread_name) + '] end thread')


def create_threads():
    """
    create group of threads
    """
    for i in range(config.get('threads_count')):
        name = "Thread #%s" % (i+1)
        # sleep between creating threads
        time.sleep(0.1)
        # call threads constructor
        my_thread = MyThread(name)
        # run a thread
        my_thread.start()

if __name__ == "__main__":
    # call function to create threads
    create_threads()

