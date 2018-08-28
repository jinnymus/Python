#!/usr/bin/python3

'''
Задание:

Даны две коллекции ObjectA (исходные/справочные данные и проверяемые данные), который содержит поля: int id, String name, String value.
Ваша задача проверить эквивалентность всех полей попарно и в случае не совпадения вывести в отчет, а в конце проверки выкинуть ошибку проверки

'''

import logging
import sys

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')


class ObjectA(object):
    '''

    Class for build ObjectA

    '''

    def __init__(self, id, name , value):
        # init objectA
        '''

        :param int id: id field for object
        :param string name: name field for object
        :param string value: value field for object
        '''
        self.id = int(id)
        self.name = str(name)
        self.value = str(value)

    def __eq__(self, other):
        '''

        :param ObjectA other: object to compare with
        :return:
        '''
        # method to compare two objects
        if (type(other) == int):
            # block for compare num with id field in list of objects
            if (self.id == other):
                return True
            else:
                return False
        else:
            # block for compare whole objects
            if (self.id == other.id):
                if (self.name == other.name):
                    if (self.value == other.value):
                        logger.info('ObjectA[' + str(self.id) + ', ' + str(self.name) + ', ' + str(self.value) + '] PASS')
                        return True
                    else:
                        logger.error('ObjectA check value SRC ' + str(self) + ' != CHECK ' + str(other) + ' FAIL')
                        return False
                else:
                    logger.error('ObjectA check name SRC ' + str(self) + ' != CHECK ' + str(other) + ' FAIL')
                    return False
            else:
                logger.error('ObjectA check id SRC ' + str(self) + ' != CHECK ' + str(other) + ' FAIL')
                return False

    def __str__(self):
        return str([self.id, self.name, self.value])

# init some objects for test
obj = ObjectA(id=1, name='name1', value='value1')
obj1 = ObjectA(id=2, name='name2', value='value2')
obj2 = ObjectA(id=3, name='name3', value='value3')
obj3_1 = ObjectA(id=3, name='name3', value='value35')
obj3_2 = ObjectA(id=3, name='name3', value='value36')
obj3_3 = ObjectA(id=3, name='name35', value='value3')
obj4 = ObjectA(id=4, name='name4', value='value4')

# create source list of objects
src_list = list()
src_list.append(obj)
src_list.append(obj1)
src_list.append(obj2)
src_list.append(obj3_1)

# create check list of objects
check_list = list()
check_list.append(obj1)
check_list.append(obj2)
check_list.append(obj3_2)
check_list.append(obj3_3)
check_list.append(obj4)

class create_object_list():
    '''

    class for create object with iterator and list

    '''
    def __init__(self, list):
        self.list = list

    def __iter__(self):
        self.n = 0
        return self

    def __next__(self):
        if self.n < len(self.list):
            result = self.list[self.n]
            self.n += 1
            return result
        else:
            raise StopIteration

def compare_lists():
    '''

    function for compare lists of objects

    '''
    compare_result = True

    # create objects with list and iterator
    src_list_obj = create_object_list(src_list)
    check_list_obj = create_object_list(check_list)

    # loop for source list
    for src_item in src_list_obj:
        # if object exist in source list and not exist in check list
        if (src_item.id not in check_list_obj):
            logger.error('ObjectA ' + str(src_item) + ' NOT EXIST IN CHECK LIST')
        else:
            # loop for check list
            for check_item in check_list_obj:
                # first check for id field
                if (src_item.id == check_item.id):
                    # call equals founction to compare objects
                    res = src_item.__eq__(check_item)
                    if (res == False):
                        compare_result = res

    for check_item in check_list_obj:
        # if object exist in checks list and not exist in source list
        if (check_item.id not in src_list_obj):
            logger.error('ObjectA ' + str(check_item) + ' NOT EXIST IN SRC LIST')

    return compare_result

if __name__ == "__main__":
    # call function to compare lists
    result = compare_lists()
    logger.debug('compare result: ' + str(result))
