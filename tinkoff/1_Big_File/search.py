#!/usr/bin/python3

'''
Задание:

Есть огромный файл в несколько гигабайт, в котором записаны целые числа. Известно, что
каждое число встречается два раза, но есть единственное число, которое встречается один раз.
Предложите эффективный алгоритм для поиска этого числа. Как изменится алгоритм, если
каждое число будет встречаться в файле чётное число раз, а единственное из них нечётное
число раз?

'''

import logging
import sys
from collections import Counter

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

# open file
with open("bigfile") as myfile:
    # User Counter class for better perfomance
    counter = Counter(myfile)

# посмотрим что посчитали
logger.debug('result counter: ' + str(counter))
# loop for result dict
for number, count in counter.items():
    # if count is odd print it
    if (count % 2 != 0):
        logger.debug('found number: ' + str(number))

