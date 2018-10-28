from selenium.webdriver.common.by import By

class CalcPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    OBJECT_COST = (By.XPATH, "//input[@id='estateCost']")
    INITIAL_FEE = (By.XPATH, "//input[@id='initialFee']")
    CREDIT_PERIOD = (By.XPATH, "//input[@id='creditTerm']")
    PAY_CARD_BOX = (By.XPATH, "//input[@data-test-id='paidToCard']")
    LIFE_INSURANCE_BOX = (By.XPATH, "//input[@data-test-id='lifeInsurance']")
    ELECTRONIC_REGISTRATION_BOX = (By.XPATH, "//input[@data-test-id='onRegDiscount']")
    DEVELOPER_DISCOUNT_BOX = (By.XPATH, "//input[@v='realtyDiscount']")
    MONTHLY_PAYMENT = (By.XPATH, "//span[@data-test-id='monthlyPayment']")

