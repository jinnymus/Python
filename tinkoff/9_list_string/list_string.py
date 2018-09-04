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

class db_checker():
    '''

    Class for compare lists

    '''

    def __init__(self):

        # create source list of objects
        src_list = list()
        src_list.append('test1')
        src_list.append('test2')
        src_list.append('test3')
        src_list.append('test4')
        src_list.append('test6')
        self.src_list = src_list

    def get_db_list(self):

        # get some list from db
        db_list = list()
        db_list.append('test1')
        db_list.append('test3')
        db_list.append('test4')
        db_list.append('test5')

        self.db_list = db_list

    def compare_lists(self):
        '''

        function for compare lists of objects

        :return: string Comparing result
        '''

        compare_result = True

        # loop for source list
        for src_item in self.src_list:
            # if object exist in source list and not exist in check list
            if (src_item not in self.db_list):
                logger.error(str(src_item) + ' NOT EXIST IN DB LIST')
                compare_result = False
            else:
                # loop for check list
                for check_item in self.db_list:
                    # first check for id field
                    if (src_item == check_item):
                        logger.debug(str(src_item) + ' found equals string')

        for check_item in self.db_list:
            # if object exist in checks list and not exist in source list
            if (check_item not in self.src_list):
                logger.error(str(check_item) + ' NOT EXIST IN SRC LIST')
                compare_result = False

        return compare_result


if __name__ == "__main__":

    # init compare object
    db = db_checker()
    # get list from db
    db.get_db_list()
    # call function to compare lists
    result = db.compare_lists()
    logger.debug('compare result: ' + str(result))