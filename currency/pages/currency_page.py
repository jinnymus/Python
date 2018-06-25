from pages.element import BasePageElement
from pages.element import BaseHTMLPageElement
from pages.locators import CurrencyPageLocators
from selenium.webdriver.common.by import By
import logging, sys
from pages.basecase import BaseCase
#logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
#logger = logging.getLogger('test')

class SearchTextElement(BaseHTMLPageElement):
    """This class gets the search text from the specified locator"""

    #The locator for search box where search string is entered
    #locator = (By.XPATH, "//input[@id='find-currencies']")
    locator = CurrencyPageLocators.SEARCH

class CurrencyElement(BaseHTMLPageElement):
    """This class gets the search text from the specified locator"""

    #The locator for search box where search string is entered
    #locator = (By.XPATH, "//div[@class='converter-tab']/div[contains(@class,'converter-tabItem')][0]/span")
    locator = CurrencyPageLocators.CURRENCY_SELECTED

class AmountElement(BasePageElement):
    """This class gets the search text from the specified locator"""

    #The locator for search box where search string is entered
    locator = CurrencyPageLocators.AMOUNT


class BasePage(object):
    """Base class to initialize the base page that will be called from all pages"""

    def __init__(self, driver):
        self.driver = driver


class CurrencyPage(BasePage):

    search_text_element = SearchTextElement()
    URI = 'https://www.exness.com/tools/converter/'

    def is_title_matches(self):
        """Verifies that the appears in page title"""
        return "EXNESS - Trader Calculator and Currency Converter" in self.driver.title

    def click_clear_button(self):
        element = self.driver.find_element(*CurrencyPageLocators.BUTTON_CLEAR)
        element.click()

    def navigate(self):
        self.driver.get(self.URI)
        self.tab_from = CurrencyPageTab(self.driver)
        self.tab_from.init(0)
        self.tab_to = CurrencyPageTab(self.driver)
        self.tab_to.init(1)
        self.close_widget()
        self.init_top_list()

    def init_top_list(self):
        top_list = list()
        elements = self.driver.find_elements(*CurrencyPageLocators.TOP_LIST)
        for cur in elements:
            cur_str = cur.get_attribute('innerHTML')
            top_list.append(cur_str)
        self.top_list_currency = top_list

    def is_top_currency(self, currency):
        if (currency in self.top_list_currency):
            return True
        else:
            return False

    def close_widget(self):
        element = self.driver.find_element(*CurrencyPageLocators.BUTTON_CLOSE_WIDGET)
        element.click()


class CurrencyPageTab(CurrencyPage):

    #amount_element = AmountElement()
    currency_element = CurrencyElement()

    def init(self, num):
        self.num = num
        #self.amount_element = AmountElement(num)
        #self.currency_element = CurrencyElement()

    def select(self):
        tab = self.driver.find_elements(*CurrencyPageLocators.TABS)[self.num]
        tab.click()

    def select_top_currency(self, currency):
        self.select()
        self.select_currency(*CurrencyPageLocators.TOP_LIST, currency=currency)
        self.check_selected_currency(currency)

    def select_all_currency(self, currency):
        self.select()
        self.select_currency(*CurrencyPageLocators.ALL_LIST, currency=currency)
        self.check_selected_currency(currency)

    def get_all_list(self):
        self.select()
        elements = self.driver.find_elements(*CurrencyPageLocators.ALL_LIST)
        return elements

    def get_all_list_names(self):
        all_list = list()
        elements = self.driver.find_elements(*CurrencyPageLocators.ALL_LIST)
        for cur in elements:
            cur_str = cur.get_attribute('innerHTML')
            all_list.append(cur_str)
        return all_list

    def get_top_list_names(self):
        top_list = list()
        elements = self.driver.find_elements(*CurrencyPageLocators.TOP_LIST)
        for cur in elements:
            cur_str = cur.get_attribute('innerHTML')
            top_list.append(cur_str)
        return top_list

    def check_selected_currency(self, currency):
        self.select()
        assert self.get_item(*CurrencyPageLocators.CURRENCY_SELECTED) == currency, self.get_item(*CurrencyPageLocators.CURRENCY_SELECTED)
        assert self.get_item(*CurrencyPageLocators.ALL_SELECTED_ITEM) == currency, self.get_item(*CurrencyPageLocators.ALL_SELECTED_ITEM)
        top_list = list()
        elements = self.driver.find_elements(*CurrencyPageLocators.TOP_LIST)
        for cur in elements:
            cur_str = cur.get_attribute('innerHTML')
            top_list.append(cur_str)
        if (currency in top_list):
            assert self.get_item(*CurrencyPageLocators.TOP_SELECTED_ITEM) == currency, self.get_item(*CurrencyPageLocators.TOP_SELECTED_ITEM)

    def select_currency(self, *currencyListLocator, currency):
        self.select()
        #elements = self.driver.find_elements(*CurrencyPageLocators.TOP_LIST)
        elements = self.driver.find_elements(*currencyListLocator)
        for cur in elements:
            cur_str = cur.get_attribute('innerHTML')
            #logger.debug('[cur_str] cur_str: ' + str(cur_str))
            if (currency in cur_str):
                cur.click()

    def get_item(self, *currencyLocator):
        self.select()
        element = self.driver.find_element(*currencyLocator)
        selected_item = element.get_attribute('innerHTML')
        return selected_item

    def set_amount(self, value):
        self.select()
        element = self.driver.find_elements(*CurrencyPageLocators.AMOUNT)[self.num]
        element.clear()
        element.send_keys(value)

    def get_amount(self):
        self.select()
        element = self.driver.find_elements(*CurrencyPageLocators.AMOUNT)[self.num]
        amount = element.get_attribute('value')
        return amount



