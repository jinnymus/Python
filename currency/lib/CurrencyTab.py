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

class CurrencyTab(object):

    def __init__(self, target):
        logger.debug('[CurrencyTab] start')
        self.target = target

    def clearField(self):
        logger.debug('[CurrencyTab][clearField] start')

    def getValue(self):
        logger.debug('[CurrencyTab][getValue] start')
        self.value = 'test'
        return self.value

    def setValue(self, value):
        logger.debug('[CurrencyTab][setValue] start')
        self.value = value

    def selectCurrency(self, currency):
        logger.debug('[CurrencyTab][setValue] start')
        self.currency = currency

    def selectTopCurrency(self, currency):
        logger.debug('[CurrencyTab][setValue] start')
        self.currency = currency

    def activate(self):
        logger.debug('[CurrencyTab][activate] start')

    def searchCurrency(self, string):
        logger.debug('[CurrencyTab][activate] start')
