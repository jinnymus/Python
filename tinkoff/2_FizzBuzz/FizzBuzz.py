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

# loop for numbers
for num in range(1, 101):
    # if num multiple of 15
    if (num % 15 == 0):
        '''
        Checking multiple of 15
        '''
        logger.debug('num: ' + str(num) + ' --> FizzBuzz')
        logger.info('FizzBuzz')
    # if num multiple of 3
    elif (num % 3 == 0):
        '''
        Checking multiple of 3
        '''
        logger.debug('num: ' + str(num) + ' --> Fizz')
        logger.info('Fizz')
    # if num multiple of 5
    elif (num % 5 == 0):
        '''
        Checking multiple of 5
        '''
        logger.debug('num: ' + str(num) + ' --> Buzz')
        logger.info('Buzz')
    # else happening
    else:
        '''
        Other numbers
        '''
        logger.debug('num: ' + str(num))
        logger.info(str(num))