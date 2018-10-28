from pages.element import BasePageElement
from pages.element import BaseHTMLPageElement
from pages.locators import CalcPageLocators
from selenium.webdriver.common.by import By
import logging, sys
from pages.basecase import BaseCase
#logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
#logger = logging.getLogger('test')

# class ObjectCostElement(BaseHTMLPageElement):
#     """This class gets the search text from the specified locator"""
#
#     locator = CalcPageLocators.OBJECT_COST
#
# class InitialFeeElement(BaseHTMLPageElement):
#     """This class gets the search text from the specified locator"""
#
#     locator = CalcPageLocators.INITIAL_FEE
#
# class CreditPeriodElement(BasePageElement):
#     """This class gets the search text from the specified locator"""
#
#     locator = CalcPageLocators.CREDIT_PERIOD
#
# class PayCardBoxElement(BasePageElement):
#     """This class gets the search text from the specified locator"""
#
#     locator = CalcPageLocators.PAY_CARD_BOX
#
# class LifeInsuranceBoxElement(BasePageElement):
#     """This class gets the search text from the specified locator"""
#
#     locator = CalcPageLocators.LIFE_INSURANCE_BOX
#
# class ElecronicRegistrationBoxElement(BasePageElement):
#     """This class gets the search text from the specified locator"""
#
#     locator = CalcPageLocators.ELECTRONIC_REGISTRATION_BOX
#
# class DeveloperDiscountBoxElement(BasePageElement):
#     """This class gets the search text from the specified locator"""
#
#     locator = CalcPageLocators.DEVELOPER_DISCOUNT_BOX
#
#
class MonthlyPaymentElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    locator = CalcPageLocators.MONTHLY_PAYMENT

class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver


class CalcPage(BasePage):

    monthly_payment = MonthlyPaymentElement()
    URI = 'https://ipoteka.domclick.ru'


    def navigate(self):
        self.driver.get(self.URI)

    def set_object_cost(self, cost):
        element = self.driver.find_element(*CalcPageLocators.OBJECT_COST)
        element.clear()
        element.send_keys(cost)

    def set_initial_fee(self, fee):
        element = self.driver.find_element(*CalcPageLocators.INITIAL_FEE)
        element.clear()
        element.send_keys(fee)

    def set_credit_period(self, period):
        element = self.driver.find_element(*CalcPageLocators.CREDIT_PERIOD)
        element.clear()
        element.send_keys(period)

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

    def get_monthly_payment(self):
        element = self.driver.find_element(*CalcPageLocators.MONTHLY_PAYMENT)
        self.monthly_payment = element.get_attribute('value')

#
# class CurrencyPageTab(CurrencyPage):
#
#     currency_element = CurrencyElement()
#
#     def init(self, num):
#         self.num = num
#
#     def select(self):
#         tab = self.driver.find_elements(*CurrencyPageLocators.TABS)[self.num]
#         tab.click()
#
#     def select_top_currency(self, currency):
#         self.select()
#         self.select_currency(*CurrencyPageLocators.TOP_LIST, currency=currency)
#         self.check_selected_currency(currency)
#
#     def select_all_currency(self, currency):
#         self.select()
#         self.select_currency(*CurrencyPageLocators.ALL_LIST, currency=currency)
#         self.check_selected_currency(currency)
#
#     def get_all_list(self):
#         self.select()
#         elements = self.driver.find_elements(*CurrencyPageLocators.ALL_LIST)
#         return elements
#
#     def get_all_list_names(self):
#         all_list = list()
#         elements = self.driver.find_elements(*CurrencyPageLocators.ALL_LIST)
#         for cur in elements:
#             cur_str = cur.get_attribute('innerHTML')
#             all_list.append(cur_str)
#         return all_list
#
#     def get_top_list_names(self):
#         top_list = list()
#         elements = self.driver.find_elements(*CurrencyPageLocators.TOP_LIST)
#         for cur in elements:
#             cur_str = cur.get_attribute('innerHTML')
#             top_list.append(cur_str)
#         return top_list
#
#     def check_selected_currency(self, currency):
#         self.select()
#         assert self.get_item(*CurrencyPageLocators.CURRENCY_SELECTED) == currency, self.get_item(*CurrencyPageLocators.CURRENCY_SELECTED)
#         assert self.get_item(*CurrencyPageLocators.ALL_SELECTED_ITEM) == currency, self.get_item(*CurrencyPageLocators.ALL_SELECTED_ITEM)
#         top_list = list()
#         elements = self.driver.find_elements(*CurrencyPageLocators.TOP_LIST)
#         for cur in elements:
#             cur_str = cur.get_attribute('innerHTML')
#             top_list.append(cur_str)
#         if (currency in top_list):
#             assert self.get_item(*CurrencyPageLocators.TOP_SELECTED_ITEM) == currency, self.get_item(*CurrencyPageLocators.TOP_SELECTED_ITEM)
#
#     def select_currency(self, *currencyListLocator, currency):
#         self.select()
#         elements = self.driver.find_elements(*currencyListLocator)
#         for cur in elements:
#             cur_str = cur.get_attribute('innerHTML')
#             if (currency in cur_str):
#                 cur.click()
#
#     def get_item(self, *currencyLocator):
#         self.select()
#         element = self.driver.find_element(*currencyLocator)
#         selected_item = element.get_attribute('innerHTML')
#         return selected_item
#
#     def set_amount(self, value):
#         self.select()
#         element = self.driver.find_elements(*CurrencyPageLocators.AMOUNT)[self.num]
#         element.clear()
#         element.send_keys(value)
#
#     def get_amount(self):
#         self.select()
#         element = self.driver.find_elements(*CurrencyPageLocators.AMOUNT)[self.num]
#         amount = element.get_attribute('value')
#         return amount



