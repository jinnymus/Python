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
from collections import Counter
import time
import random
from threading import Thread

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

# Конфигурация запуска

config = {
    'threads_count' : 12, # количество потоков
    'threads_search_time' : 1, # время поиска свободного номера в секундах
    'threads_work_time_min' : 10, # время работы потока, минимум в секундах
    'threads_work_time_max' : 14, # время работы потока, максимум в секундах
}

class Singleton(type):
    '''

    Синглтон

    '''
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MyClass(metaclass=Singleton):
    '''

    Используем метакласс

    '''

    def __init__(self, host = 'none'):
        '''

        Инициализирование списка чисел в конструкторе

        '''
        self.numbers = list(range(1, 11))

    def get_number(self):
        '''
        Функция получения свободного числа из списка
        '''
        try:
            num = self.numbers.pop()
        except IndexError:
            # Если список пустой, перехватим исключение, присвоим None
            num = None
        return num

    def return_number(self, num):
        '''
        Функция возврата числа в список свободных
        '''
        return self.numbers.append(num)
    pass

class MyThread(Thread):
    """

    Класс для потока

    """

    def __init__(self, name):
        """

        Инициализация потока

        """
        Thread.__init__(self)
        self.name = name

    def run(self):
        """

        Запуск потока

        """
        msg = "%s is running" % self.name
        print('[' + str(self.name) + '] ' + str(msg))
        self.process(self.name)

    def process(self, thread_name):
        """

        Задача для потока

        """
        print('[' + str(thread_name) + '] start thread')
        # Создаем объект класса для работы с списком чисел
        a = MyClass()
        # Получим свободное число
        num = a.get_number()
        # Пока нет свободных
        while (num is None):
            print('[' + str(thread_name) + '] Wait for free numbers..')
            # Будем ждать
            time.sleep(config.get('threads_search_time'))
            # И снова пытаться получить свободное число
            num = a.get_number()
        print('[' + str(thread_name) + '] Yeap, i got num: ' + str(num))
        sleep_time = random.randint(config.get('threads_work_time_min'),config.get('threads_work_time_max'))
        # Эмуляция полезной работы
        time.sleep(sleep_time)
        # Возврат числа в список свободных
        num = a.return_number(num)
        print('[' + str(thread_name) + '] end thread')


def create_threads():
    """
    Создаем группу потоков
    """
    for i in range(config.get('threads_count')):
        name = "Thread #%s" % (i+1)
        # Задержка создания между потоками
        time.sleep(0.1)
        # Вызов конструктора для потока
        my_thread = MyThread(name)
        # Запуск потока
        my_thread.start()

if __name__ == "__main__":
    # Вызов функции для создания потоков
    create_threads()

