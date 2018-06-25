import pytest
import allure
import selenium
from selenium.webdriver.common.keys import Keys
import logging
from selenium.common.exceptions import TimeoutException
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
import sys
import itertools
from selenium import webdriver
import pages
from pages.basecase import BaseCase
from pages.locators import CurrencyPageLocators
from pages.currency_page import CurrencyPage

#logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
#logger = logging.getLogger('test')

site = 'https://www.exness.com/tools/converter/'


def pytest_generate_tests(d, metafunc):
    if 'top_list' in metafunc.fixturenames:
        currency_page = CurrencyPage(d)
        currency_page.navigate()
        list = currency_page.get_all_list_names()
        metafunc.parametrize('top_list', [i for i in list])

@allure.feature('Функциональное тестирование')
@allure.story('Базовый функционал')
class Test_basic(BaseCase):

    # def test_title_page(self):
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     assert currency_page.is_title_matches(), "title doesn't match. Title: " + str(self.driver.title)

    # def test_check_clear_form(self):
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     currency_page.tab_to.amount_element = 100
    #     currency_page.click_clear_button()
    #     assert currency_page.tab_to.amount_element == '', 'amount_element: ' + str(currency_page.tab_to.amount_element)
    #     currency_page.tab_from.amount_element = 100
    #     currency_page.click_clear_button()
    #     assert currency_page.tab_from.amount_element == '', 'amount_element: ' + str(currency_page.tab_from.amount_element)
    #
    # def test_all_currency(self):
    #     """
    #
    #     Пополнение баланса
    #     используется бонус, валюта, сумма, платежная система
    #         password.send_keys('pass1')
    #
    #     """
    #
    #     currency_from = 'BKK'
    #     currency_to = 'RUB'
    #
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     #currency_page.search_text_element = "RUB"
    #
    #     currency_page.tab_to.amount_element = 100
    #     currency_page.tab_to.select_all_currency(currency_to)
    #     currency_page.tab_from.select_all_currency(currency_from)
    #
    #     currency_page.tab_from.check_selected_currency(currency_from)
    #     currency_page.tab_to.check_selected_currency(currency_to)
    #     assert currency_page.tab_from.amount_element > 0, 'amount_element: ' + str(currency_page.tab_from.amount_element)

    def test_top_currency(self):
        """

        Пополнение баланса
        используется бонус, валюта, сумма, платежная система
            password.send_keys('pass1')

        """

        currency_from = 'AUD'
        currency_to = 'CAD'

        currency_page = CurrencyPage(self.driver)
        currency_page.navigate()
        # currency_page.search_text_element = "RUB"

        currency_page.tab_to.set_amount(100)
        currency_page.tab_to.select_top_currency(currency_to)
        currency_page.tab_from.select_top_currency(currency_from)

        #currency_page.tab_from.check_selected_currency(currency_from)
        #currency_page.tab_to.check_selected_currency(currency_to)
        assert currency_page.tab_from.get_amount() != '', 'amount_element: ' + str(currency_page.tab_from.get_amount())


    def test_toplist_currency(self, top_list):
        for i in top_list:
            print('i: ' + str(i))


    #
    # def test_top_currency_reverse(self):
    #     """
    #
    #     Пополнение баланса
    #     используется бонус, валюта, сумма, платежная система
    #         password.send_keys('pass1')
    #
    #     """
    #
    #     currency_from = 'AUD'
    #     currency_to = 'CAD'
    #
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     # currency_page.search_text_element = "RUB"
    #
    #     currency_page.tab_from.set_amount(100)
    #     currency_page.tab_to.select_top_currency(currency_to)
    #     currency_page.tab_from.select_top_currency(currency_from)
    #
    #     currency_page.tab_from.check_selected_currency(currency_from)
    #     currency_page.tab_to.check_selected_currency(currency_to)
    #     assert currency_page.tab_from.amount_element != '', 'amount_element: ' + str(currency_page.tab_from.amount_element)
    #
    # def test_search_fail(self):
    #
    #     currency_from = 'CHF'
    #     currency_to = 'RUB'
    #
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     currency_page.search_text_element = currency_from
    #     if (currency_to in currency_page.tab_from.get_all_list_names()):
    #         assert False, 'listnames:' + str(currency_page.tab_from.get_all_list_names())
    #
    # def test_search_ok(self):
    #
    #     currency_from = 'CHF'
    #
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     currency_page.search_text_element = currency_from
    #     if (currency_from not in currency_page.tab_from.get_all_list_names()):
    #         assert False, 'listnames:' + str(currency_page.tab_from.get_all_list_names())

