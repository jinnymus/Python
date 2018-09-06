import logging
import os
import pytest
import allure
import logging
import time

log = logging.getLogger('conftest')

def pytest_exception_interact(node, call, report):

    logging.debug("[pytest_exception_interact] node: " + str(node.__dict__))

    testlib = node.__getattribute__('funcargs')

    for key, cls in testlib.items():
        logging.debug("[pytest_exception_interact] node: " + str(node.__dict__))
        logging.debug("[pytest_exception_interact] key: " + str(key))
        logging.debug("[pytest_exception_interact] cls: " + str(cls))
        log_path = cls.service.log_path
        log_name = str(key) + '.log'
        logging.debug("[pytest_exception_interact] log_name: " + str(log_name))
        logging.debug("[pytest_exception_interact] log_path: " + str(log_path))
        if (log_path is not None):
            logfile = open(log_path, 'r')
            lines = logfile.read()
            allure.attach(
               name=log_name,
               contents=lines,
               type=allure.constants.AttachmentType.TEXT)


