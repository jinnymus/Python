from selenium.webdriver.common.by import By

class CurrencyPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    TOP_LIST = (By.XPATH, "//li[contains(@class,'converter-popularItem')]")
    TOP_SELECTED_ITEM = (By.XPATH,
                         "//li[@class='converter-popularItem converter-popularItem__selected']")

    ALL_LIST = (By.XPATH, "//li[contains(@class,'converter-currenciesItem')]/span[@class='converter-currenciesSymbol']")
    ALL_SELECTED_ITEM = (By.XPATH,
                         "//li[@class='converter-currenciesItem converter-currenciesItem__selected']/span[@class='converter-currenciesSymbol']")

    AMOUNT = (By.XPATH, "//div[contains(@class,'converter-tabItem')]/input")
    CURRENCY_SELECTED = (By.XPATH, "//div[@class='converter-tabItem converter-tabItem__selected']/span")

    SEARCH = (By.XPATH, "//input[@id='find-currencies']")
    BUTTON_CLEAR = (By.XPATH, "//div[@class='converter-tabBtns']")

    TABS = (By.XPATH, "//div[contains(@class,'converter-tabItem')]")
    SELECTED_TAB = (By.XPATH, "//div[@class='converter-tabItem converter-tabItem__selected']")

    #BUTTON_CLOSE_WIDGET = (By.XPATH, "//button[@title='Close widget']")
