from selenium.webdriver.common.by import By

class CalcPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    OBJECT_TARGET = (By.XPATH, "//div[@class='dcCalc_input-row-desktop__label' and text()='Цель кредита']/../following-sibling::div/.//input[@class='dcCalc_textfield__input']")
    OBJECT_COST = (By.XPATH, "//input[@id='estateCost']")
    INITIAL_FEE = (By.XPATH, "//input[@id='initialFee']")
    CREDIT_PERIOD = (By.XPATH, "//input[@id='creditTerm']")
    PAY_CARD_BOX = (By.XPATH, "//input[@data-test-id='paidToCard']")
    LIFE_INSURANCE_BOX = (By.XPATH, "//input[@data-test-id='lifeInsurance']")
    ELECTRONIC_REGISTRATION_BOX = (By.XPATH, "//input[@data-test-id='onRegDiscount']")
    DEVELOPER_DISCOUNT_BOX = (By.XPATH, "//input[@v='developerDiscount']")
    MONTHLY_PAYMENT = (By.XPATH, "//span[@data-test-id='monthlyPayment']")
    

