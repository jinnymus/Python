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
from pages.locators import CalcPageLocators
from pages.calc_page import CalcPage
from django.conf import settings
from unittest import TestCase


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

site = 'https://ipoteka.domclick.ru'
settings.configure()


@allure.story('Hypotek calculator')
class Test_basic(BaseCase):

    @allure.testcase('Checking monthly payment')
    def test_monthly_payment(self):
        """

        Checking monthly paid

        """
        calc_page = CalcPage(self.driver)
        calc_page.navigate()
        #calc_page.set_object_target("Покупка квартиры в новостройке")
        calc_page.set_object_cost("4800000")
        #calc_page.set_initial_fee("1000000")
        #calc_page.set_credit_period("7")
        #calc_page.pay_card()
        #calc_page.life_insurance()
        #calc_page.electronic_registration()
        #calc_page.developer_discount()
        #calc_page.get_monthly_payment()
        assert calc_page.monthly_payment == 57539, "Payment doesn't match. Paid: " + str(self.driver.title)

