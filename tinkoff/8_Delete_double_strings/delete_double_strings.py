#!/usr/bin/python3

'''
Задание:

Напишите функцию, которая будет из входной строки удалять парные, идущие друг за другом буквы в одну и на выходе вернуть строку,
которая не будет иметь парных, идущих друг за другом букв.
Пример: aaabccddd => abd, baab => пусто

'''

import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')


#source_string='baab'
#source_string='aaabccddd'
source_string='aaaabccdddggggg'

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
    dict_letters_new = dict(dict_letters)

    for key,value in dict_letters.items():
        logger.debug('dict_letters key: ' + str(key) + ' value: ' + str(value))
        if (value % 2 == 0):
            dict_letters_new.pop(key, None)

    dict_letters_new2 = dict(dict_letters_new)

    for key,value in dict_letters_new.items():
        logger.debug('dict_letters_new key: ' + str(key) + ' value: ' + str(value))
        if (value % 2 != 0) :
            dict_letters_new2.pop(key, None)
            dict_letters_new2[key] = 1

    for key,value in dict_letters_new2.items():
        logger.debug('dict_letters_new2 key: ' + str(key) + ' value: ' + str(value))
        result += str(key) + str(value)
    return result

if __name__ == "__main__":
    # call function to calculate lists
    dict_letters = calculate_letters(source_string)
    result = print_result(dict_letters)
    logger.debug('calculate result: ' + str(result))
