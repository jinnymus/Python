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

# Открываем файл и работаем с ним, используя буферизованное управление вводами и памятью
with open("bigfile") as myfile:
    # Используем класс Counter из коробки Python
    counter = Counter(myfile)

# посмотрим что посчитали
logger.debug('result counter: ' + str(counter))
# пробежимся по результируещему массиву
for number, count in counter.items():
    # если нечетное количество чисел - выводим
    if (count % 2 != 0):
        logger.debug('found number: ' + str(number))

