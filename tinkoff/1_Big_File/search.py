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

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

arr = dict()

# Открываем файл и работаем с ним, используя буферизованное управление вводами и памятью
with open("bigfile") as myfile:
    # для всех строк
    for line in myfile:
        # удаляем перенос строки
        line = line.rstrip()
        if line in arr:
            # если текущее число в строке есть в результируещем словаре - инкрементим
            arr[line]=int(arr.get(line)) + 1
        else:
            # если нет - пишем 1
            arr[line] = 1
# посмотрим что посчитали
logger.debug('result arr: ' + str(arr))
# пробежимся по результируещему массиву
for number, count in arr.items():
    # если нечетное количество чисел - выводим
    if (count % 2 != 0):
        logger.debug('found number: ' + str(number))

