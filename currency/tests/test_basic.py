import pytest
import allure
import selenium
from selenium.webdriver.common.keys import Keys
import logging
from selenium.common.exceptions import TimeoutException
import sys
import itertools
from selenium import webdriver
import pages
from pages.basecase import BaseCase
from pages.locators import CurrencyPageLocators
from pages.currency_page import CurrencyPage
from django.conf import settings
from unittest import TestCase


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

site = 'https://www.exness.com/tools/converter/'
settings.configure()


@allure.feature('Функциональное тестирование')
@allure.story('Базовый функционал')
class Test_basic(BaseCase):

    @allure.testcase('Проверка названия страницы')
    def test_title_page(self):
        """

        Проверка названия страницы

        """
        currency_page = CurrencyPage(self.driver)
        currency_page.navigate()
        self.list = currency_page.tab_from.get_all_list()
        assert currency_page.is_title_matches(), "title doesn't match. Title: " + str(self.driver.title)

    # @allure.testcase('Проверка кнопки очистики полей')
    # def test_check_clear_form(self):
    #     """
    #
    #     Проверка кнопки очистики полей
    #
    #     """
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     currency_page.tab_to.set_amount(100)
    #     currency_page.click_clear_button()
    #     assert currency_page.tab_to.get_amount() == '0', 'amount_element: ' + str(currency_page.tab_to.get_amount())
    #     currency_page.tab_from.set_amount(100)
    #     currency_page.click_clear_button()
    #     assert currency_page.tab_from.get_amount() == '0', 'amount_element: ' + str(currency_page.tab_from.get_amount())
    #
    # @allure.testcase('Проверка валют из всего списка')
    # def test_all_currency(self):
    #     """
    #
    #     Проверка валют из всего списка
    #
    #     """
    #
    #     currency_from = 'ARS'
    #     currency_to = 'RUB'
    #
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     #currency_page.search_text_element = "RUB"
    #
    #     currency_page.tab_to.set_amount(100)
    #     currency_page.tab_to.select_all_currency(currency_to)
    #     currency_page.tab_from.select_all_currency(currency_from)
    #
    #     currency_page.tab_from.check_selected_currency(currency_from)
    #     currency_page.tab_to.check_selected_currency(currency_to)
    #     assert currency_page.tab_from.get_amount() != '', 'amount_element: ' + str(currency_page.tab_from.get_amount())
    #
    #
    # @allure.testcase('Проверка популярных валют, ввод суммы в поле "из"')
    # def test_top_currency(self):
    #     """
    #
    #     Проверка популярных валют, ввод суммы в поле "из"
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
    #     currency_page.tab_to.set_amount(100)
    #     currency_page.tab_to.select_top_currency(currency_to)
    #     currency_page.tab_from.select_top_currency(currency_from)
    #
    #     assert currency_page.tab_from.get_amount() != '', 'amount_element: ' + str(currency_page.tab_from.get_amount())
    #
    # @allure.testcase('Проверка популярных валют, ввод суммы в поле "в"')
    # def test_top_currency_reverse(self):
    #     """
    #
    #     Проверка популярных валют, ввод суммы в поле "в"
    #
    #     """
    #
    #     #currency_from = 'AUD'
    #     currency_to = 'CAD'
    #     currency_from = 'USD'
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
    #     assert currency_page.tab_from.get_amount() != '', 'amount_element: ' + str(currency_page.tab_from.get_amount())
    #
    # @allure.testcase('Проверка поиска валюты, результат не содержит искомую валюту')
    # def test_search_fail(self):
    #     """
    #
    #     Проверка поиска валюты, результат не содержит искомую валюту
    #
    #     """
    #     currency_from = 'CHF'
    #     currency_to = 'RUB'
    #
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     currency_page.search_text_element = currency_from
    #     if (currency_to in currency_page.tab_from.get_all_list_names()):
    #         assert False, 'listnames:' + str(currency_page.tab_from.get_all_list_names())
    #
    # @allure.testcase('Проверка поиска валюты, результат содержит искомую валюту')
    # def test_search_ok(self):
    #     """
    #
    #     Проверка поиска валюты, результат содержит искомую валюту
    #
    #     """
    #     currency_from = 'CHF'
    #
    #     currency_page = CurrencyPage(self.driver)
    #     currency_page.navigate()
    #     currency_page.search_text_element = currency_from
    #     if (currency_from not in currency_page.tab_from.get_all_list_names()):
    #         assert False, 'listnames:' + str(currency_page.tab_from.get_all_list_names())
