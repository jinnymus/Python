import pytest
import allure
import selenium
from selenium.webdriver.common.keys import Keys
import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import itertools


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

class Currency(object):

    def __init__(self):
        logger.debug('[TopCurrency] start')

    def getList(self):
        logger.debug('[TopCurrency][getList] start')
        return list

    def selected(self):
        logger.debug('[TopCurrency][checkPressed] start')
        return True

    def selectCurrency(self, currency):
        logger.debug('[TopCurrency][selectCurrency] start')