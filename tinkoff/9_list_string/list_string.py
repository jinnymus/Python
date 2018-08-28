#!/usr/bin/python3

'''
Задание:

 Есть два List<String>. Первый это эталонные ключи, второй это ключи, которые содержатся в БД.
 Задача: а) проверить, что в БД нет лишних ключей и вывести все лишние ключи б) проверить,
 что эталонные ключи содержатся в БД и вывести ключи, которых нет в БД

'''

import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')
