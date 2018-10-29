from selenium.webdriver.common.by import By

class CalcPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    OBJECT_TARGET = (By.XPATH, "//div[@class='dcCalc_input-row-desktop__label' and text()='Цель кредита']/../following-sibling::div/.//input[@class='dcCalc_textfield__input']")
    OBJECT_COST = (By.XPATH, "//input[@id='estateCost']")
    OBJECT_COST_CSS = (By.CSS_SELECTOR, "#estateCost")
    INITIAL_FEE = (By.XPATH, "//input[@id='initialFee']")
    INITIAL_FEE_CSS = (By.CSS_SELECTOR, "# initialFee")
    CREDIT_PERIOD = (By.XPATH, "//input[@id='creditTerm']")
    CREDIT_PERIOD_CSS = (By.CSS_SELECTOR, "#creditTerm")
    PAY_CARD_BOX = (By.XPATH, "//input[@data-test-id='paidToCard']")
    LIFE_INSURANCE_BOX = (By.XPATH, "//*[@data-test-id='lifeInsurance']")
    LIFE_INSURANCE_BOX_CSS = (By.CSS_SELECTOR, "div.dcCalc_switch - desktop: nth - child(3) > div:nth - child(2) > label: nth - child(2) > input:nth - child(1)")
    ELECTRONIC_REGISTRATION_BOX = (By.XPATH, "//input[@data-test-id='onRegDiscount']")
    DEVELOPER_DISCOUNT_BOX = (By.XPATH, "//input[@data-test-id='developerDiscount']")
    MONTHLY_PAYMENT = (By.XPATH, "//span[@data-test-id='monthlyPayment']")
    CHAT = (By.XPATH, "//div[@class='_5nk8qq5zvxzyzz35ju7j6kmcm78ee63v8dkz3udkdfykg6ggy4c6c26uq3qyrq4rr61b4ns9jmdpxcvrf4yqxczs6xa77qdmsxvmrk-ChatButton-module-ChatButton _3u2x63smmnq3128jrpqcaz1hcx2r95musy4rfj27h1vhh2whpycf1kd3j791z9crhppvgb8ju6w3q6qrprdr5exkq7je6t1bytutfe6-ChatButton-module-open m219pqh9s68z9x2gw8t8rct3hxbjamshfdeh2c3vepdt999re9qbvd37wt7nqfye81tpgu3fvqregk8xn1xaywn5wxvn5vvqk2wwcz-ChatButton-module-alone']")

