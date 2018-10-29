#from pages.element import BasePageElement
from pages.element import BaseHTMLPageElement
from pages.locators import CalcPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import logging, sys
from pages.basecase import BaseCase
from selenium.webdriver.common.keys import Keys
import logging
import sys
from selenium.common.exceptions import TimeoutException
import time

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('calc_page')


class ObjectCostElement(BaseHTMLPageElement):
     locator = CalcPageLocators.OBJECT_COST

class InitialFeeElement(BaseHTMLPageElement):
     locator = CalcPageLocators.INITIAL_FEE

class CreditPeriodElement(BaseHTMLPageElement):
     locator = CalcPageLocators.CREDIT_PERIOD

class MonthlyPaymentElement(BaseHTMLPageElement):
    locator = CalcPageLocators.MONTHLY_PAYMENT

class BasePage(object):

    def __init__(self, driver):
        self.driver = driver


class CalcPage(BasePage):

    monthly_payment = None
    URI = 'https://ipoteka.domclick.ru'


    def navigate(self):
        self.driver.get(self.URI)

    def set_object_target(self, target):
        element = WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*CalcPageLocators.OBJECT_TARGET))
        element.click()
        element.send_keys(target)

        
    def set_object_cost(self, cost):
        element = WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*CalcPageLocators.OBJECT_COST))
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.DELETE)
        element.send_keys(cost)
        element.send_keys(Keys.ENTER)
        # time.sleep(2)
        # element.send_keys(Keys.CONTROL, 'a')
        # element.send_keys(Keys.DELETE)
        # element.send_keys(cost)
        # element.send_keys(Keys.ENTER)

        #element.click()

    def set_initial_fee(self, fee):
        element = WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*CalcPageLocators.INITIAL_FEE))
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.DELETE)
        element.send_keys(fee)
        element.send_keys(Keys.ENTER)
        # time.sleep(2)
        # element.send_keys(Keys.CONTROL, 'a')
        # element.send_keys(Keys.DELETE)
        # element.send_keys(fee)
        # element.send_keys(Keys.ENTER)

    def set_credit_period(self, period):
        element = WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*CalcPageLocators.CREDIT_PERIOD))
        element.send_keys(Keys.CONTROL, 'a')
        element.send_keys(Keys.DELETE)
        element.send_keys(period)
        element.send_keys(Keys.ENTER)
        # time.sleep(2)
        # element.send_keys(Keys.CONTROL, 'a')
        # element.send_keys(Keys.DELETE)
        # element.send_keys(period)
        # element.send_keys(Keys.ENTER)

    def pay_card(self):
        element = self.driver.find_element(*CalcPageLocators.PAY_CARD_BOX)
        element.click()

    def life_insurance(self):
        element = self.driver.find_element(*CalcPageLocators.LIFE_INSURANCE_BOX)
        element.click()

    def electronic_registration(self):
        element = self.driver.find_element(*CalcPageLocators.ELECTRONIC_REGISTRATION_BOX)
        element.click()

    def developer_discount(self):
        element = self.driver.find_element(*CalcPageLocators.DEVELOPER_DISCOUNT_BOX)
        element.click()

    def close_chat(self):
        element = self.driver.find_element(*CalcPageLocators.CHAT)
        element.click()

    def get_monthly_payment(self):
        element = WebDriverWait(self.driver, 100).until(
            lambda driver: driver.find_element(*CalcPageLocators.MONTHLY_PAYMENT))
        self.monthly_payment = element.text
        logger.debug('get payment: ' + str(element.text))

