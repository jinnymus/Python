import pytest
import allure
import selenium
from selenium.webdriver.common.keys import Keys
import logging
from selenium.common.exceptions import TimeoutException
import sys
import itertools
from selenium import webdriver
from libs.webdriver import WebDriver
from libs.auth import auth
from django.conf import settings
from unittest import TestCase
from django.conf import settings

config = {'host': 'notamdev.qantor.ru'
          }

auth = auth('test','1234', False)
#logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

settings.configure()
logger = logging.getLogger(__name__)

class Test_de():
    def test_one(self):
        logger.debug('test')

def test_auth():
    uri = '/api/auth/login'
    response = request(uri)
    get_value(response=response, value='key')
    assert response == '', response.text

def get_value(response, value):
    logger.debug('[get_value] value: ' + str(value))


def request(uri, data=None):
    uri = '/api/auth/login'
    logger.debug('[request] data: ' + str(data))
    driver = WebDriver(host=config.get('host'), port=80, authorise=auth, methods='POST', content='application/json', paths=uri )
    response=driver.request(path=uri, method='POST')
    logger.debug('[request] response code: ' + str(response.status_code))
    logger.debug('[request] response text: ' + str(response.text))
    return response



