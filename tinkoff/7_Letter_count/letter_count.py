#!/usr/bin/python3

'''
Задание:

Есть строка вида “aaabbcccd”. Задача посчитать количество каждой буквы и вывести. Например: “3a2b3c1d”.

'''

import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')


source_string='aaabbcccd'

def calculate_letters(source_string):
    '''

    function to calculate letters in string

    :param string source_string:
    :return: list letters: dict of { letter : count_of_letters }
    '''
    letters = dict()
    for letter in source_string:
        if letter not in letters:
            letters[letter] = 1
        else:
            letters[letter] += 1
    return letters

def print_result(dict_letters):
    '''

    :param dict dict_letters: dict of { letter : count_of_letters }
    :return: string result: string example 'a3b2c3d1'
    '''
    result = ""
    for key,value in dict_letters.items():
        result += str(key) + str(value)
    return result

if __name__ == "__main__":
    # call function to calculate lists
    dict_letters = calculate_letters(source_string)
    result = print_result(dict_letters)
    logger.debug('calculate result: ' + str(result))
