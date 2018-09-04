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




class object_checker():
    '''

    Class for compare lists of objects

    '''
    def __init__(self):

        # init some objects for test
        self.obj = ObjectA(id=1, name='name1', value='value1')
        self.obj1 = ObjectA(id=2, name='name2', value='value2')
        self.obj2 = ObjectA(id=3, name='name3', value='value3')
        self.obj3_1 = ObjectA(id=3, name='name3', value='value35')
        self.obj3_2 = ObjectA(id=3, name='name3', value='value36')
        self.obj3_3 = ObjectA(id=3, name='name35', value='value3')
        self.obj4 = ObjectA(id=4, name='name4', value='value4')

    def create_lists(self):

        # create source list of objects
        src_list = list()
        src_list.append(self.obj)
        src_list.append(self.obj1)
        src_list.append(self.obj2)
        src_list.append(self.obj3_1)

        # create check list of objects
        check_list = list()
        check_list.append(self.obj1)
        check_list.append(self.obj2)
        check_list.append(self.obj3_2)
        check_list.append(self.obj3_3)
        check_list.append(self.obj4)

        self.src_list = self.create_object_list(src_list)
        self.check_list = self.create_object_list(check_list)

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

    def compare_lists(self):
        '''

        function for compare lists of objects

        :return: string Comparing result
        '''

        compare_result = True

        # loop for source list
        for src_item in self.src_list:
            # if object exist in source list and not exist in check list
            if (src_item.id not in self.check_list):
                logger.error('ObjectA ' + str(src_item) + ' NOT EXIST IN CHECK LIST')
                compare_result = False
            else:
                # loop for check list
                for check_item in self.check_list:
                    # first check for id field
                    if (src_item.id == check_item.id):
                        # call equals founction to compare objects
                        res = src_item.__eq__(check_item)
                        if (res == False):
                            compare_result = res

        for check_item in self.check_list:
            # if object exist in checks list and not exist in source list
            if (check_item.id not in self.src_list):
                logger.error('ObjectA ' + str(check_item) + ' NOT EXIST IN SRC LIST')
                compare_result = False

        return compare_result

if __name__ == "__main__":

    # init checker object
    checker = object_checker()

    # create test lists
    checker.create_lists()

    # call function to compare lists
    result = checker.compare_lists()

    logger.debug('compare result: ' + str(result))
