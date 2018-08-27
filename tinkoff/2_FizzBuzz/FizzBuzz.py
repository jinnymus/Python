#!/usr/bin/python3

'''
Задание:

Напишите программу, которая выводит на экран числа от 1 до 100. При этом вместо чисел,
кратных 3, программа должна выводить слово Fizz, а вместо чисел, кратных 5 — слово Buzz.
Если число кратно 15, то программа должна выводить слово FizzBuzz.
Для 15 выводим FizzBuzz, а не FizzBuzzFizzBuzz.

'''

import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger('test')

for num in range(1, 101):
    if (num % 15 == 0):
        '''
        Проверка кратности 15
        '''
        logger.debug('num: ' + str(num) + ' --> FizzBuzz')
        logger.info('FizzBuzz')
    elif (num % 3 == 0):
        '''
        Проверка кратности 3
        '''
        logger.debug('num: ' + str(num) + ' --> Fizz')
        logger.info('Fizz')
    elif (num % 5 == 0):
        '''
        Проверка кратности 5
        '''
        logger.debug('num: ' + str(num) + ' --> Buzz')
        logger.info('Buzz')
    else:
        '''
        Остальные числа
        '''
        logger.debug('num: ' + str(num))
        logger.info(str(num))