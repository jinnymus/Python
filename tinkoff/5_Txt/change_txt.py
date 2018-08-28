#!/usr/bin/python3

'''
Задание:

Есть файл формата txt в котором две строки => первая строка колонки, вторая значения.
Задача – на вход функции подается название колонки и новое значение, напишите функцию, которая будет менять у указанной колонки значение на новое.

'''

import logging
import sys
import re
from tempfile import mkstemp
from shutil import move
from os import fdopen, remove

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

# Config for task

config = {
    'file_name' : 'file.txt', # file name for work
    'column_name' : 'column4', # column name for search
    'new_value' : 'newvalue27', # new valuu for column
}



def update_column_value(column_name, column_value):
    '''

    Function for change value by column name
    :param string column_name: Column name
    :param string column_value: New value
    '''
    # open source file
    f = open(config.get('file_name'))
    # file to list
    lines = f.read().splitlines()
    column_count = len(re.split('(\W+)', lines[0]))
    new_value_row = ""
    old_column_value = ""
    # loop for columns
    for column_num in range(column_count):
        # columns to list with separators
        columns = re.split('(\W+)', lines[0])
        # values to list with separators
        values = re.split('(\W+)', lines[1])
        # get current column name by cloumn num
        column = columns[column_num]
        # get current value for column by column num
        value = values[column_num]
        if (column == column_name):
            # if found target column name, update value
            old_column_value = value
            value = column_value
        # build new row for file
        new_value_row = str(new_value_row) + str(value)
        # update new row in file
        replace_all_line(file_path='file.txt', value_row_id=1, new_value_row=new_value_row)
    logger.debug('Search column: ' + str(column_name))
    logger.debug('Old column value: ' + str(old_column_value))
    logger.debug('New column value: ' + str(column_value))

def replace_all_line(file_path, value_row_id, new_value_row):
    '''

    Function for replace whole string in file

    :param string file_path: Path to source file
    :param int value_row_id: Row number
    :param string new_value_row: New string to replace
    '''
    # Create temporary file
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            # File to list
            lines = old_file.readlines()
            # Loop for whole file
            for row_id in range(len(lines)):
                if (row_id == value_row_id):
                    # If row id equals seached id, write new string to new file
                    new_file.write(new_value_row)
                else:
                    # Else no, copy old srting to new string
                    new_file.write(lines[row_id])
    # Remove temprorary file
    remove(file_path)
    # Move new file
    move(abs_path, file_path)



if __name__ == "__main__":
    # Call function for replace value by column name
    update_column_value(config.get('column_name'),config.get('new_value'))

