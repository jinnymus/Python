import pytest
import allure
import selenium
from selenium import webdriver
import os
import sys
import seleniumwrapper as selwrap
import logging

log = logging.getLogger('tests')

@pytest.yield_fixture(scope='module')
def get_driver(request):

    browser = request.config.getoption('--browser')

    if browser == 'firefox':
        # driver = webdriver.Firefox(executable_path=driver_path, log_path=log_path)
        driver = webdriver.Firefox()
    elif browser == 'chrome':
        driver = webdriver.Chrome()
        # driver = webdriver.Chrome(executable_path=driver_path, service_log_path=log_path)

    request.cls.CurrencyPage.driver = driver

    # driver.page_config = config['page_config']
    # driver.locators = config['locators']
    driver.maximize_window()
    #yield driver

    def close_driver():
        print('[close_driver]')
        #driver.quit()

    request.addfinalizer(close_driver)
    return driver

@pytest.yield_fixture(scope='class')
def firefox_driver_setup(request):
    driver = selwrap.create("firefox")
    request.cls.driver = driver
    yield driver
    driver.close()

@pytest.fixture(scope='class')
def d(request):
    from selenium import webdriver

    driver = webdriver.Firefox()
    #request.cls.driver = driver
    yield driver

    def fin():
        driver.quit()
    #request.cls.driver = driver
