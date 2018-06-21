import pytest
import allure
import selenium
from selenium.webdriver.common.keys import Keys
import logging
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sys
import itertools


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

site = 'ibitcy.com/interview/qa/mobile-deposit/'
site_user = 'qa'
site_pass = 'Af4shrewyirlyuds'
users = {'username1@name.ru':'pass1',
'username2@name.ru':'pass2',
'username3@name.ru':'pass3',
'username4@name.ru':'pass4'}
site_auth = 'https://' + site_user + ':' + site_pass + '@' + site

#@pytest.mark.usefixtures("driver_init","screenshot_on_failure")
@pytest.mark.usefixtures("driver_init")
@allure.feature('Функциональное тестирование')
@allure.story('Авторизация')
class Test_authorization():

    @allure.step('Открытие страницы в браузере')
    def test_open_link_in_browser(self):

        """

        Открытие браузера

        """

        assert True

    @allure.step('Ввод данных в поля')
    def test_enter_values_in_form(self):

        """

        Ввод данных в полня формы

        """

        assert True

    def test_invalid_pass_auth(self):

        """

        Проверка авторизации при неверном пароле

        """

        assert True

    def test_invalid_user_auth(self):

        """

        Проверка авторизации при неверном пользователе

        """

        assert True

    def test_empty_form(self):
        """

        Проверка авторизации при пустых полях формы

        """
        assert True

    def test_restore_form_valid(self):
        """

        Проверка формы восттановления пароля

        """

        assert True

    def test_restore_form_invalid_pass(self):
        """

        Проверка формы восттановления пароля при несоответствии паролей

        """

        assert True


    def test_restore_form_empty_valued(self):
        """

        Проверка формы восттановления пароля при пустых значениях в полях

        """

        assert True

    def test_valid_auth(self):

        """
        Проверка успешной авторизации
        """



@pytest.mark.usefixtures("driver_init")
@allure.feature('Функциональное тестирование')
@allure.story('Авторизация')
class Test_refill_balance():

    @allure.step('Открытие страницы в браузере')
    def auth_open_link_in_browser(self):
        """

        Авторизация и открытие браузера

        """

        logger.debug('[test_example_uri] start')
        self.driver.get(site_auth)

        try:
            element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "login-form"))
            WebDriverWait(self.driver, 10).until(element_present)

            btn_en = self.driver.find_element_by_xpath("//div[@class='languages-buttons']/div[@class='lang en']/a")
            btn_en.click()

            WebDriverWait(self.driver, 10).until(element_present)

            username = self.driver.find_element_by_xpath(
                "//login-form/form/div[@class='amount-inputs']/input[@name='username']")
            password = self.driver.find_element_by_xpath(
                "//login-form/form/div[@class='amount-inputs']/textarea[@name='password']")
            submit = self.driver.find_element_by_xpath(
                "//login-form/form/div[@class='submit gold']/a/span[@class='text']")

            username.send_keys('username1@name.ru')
            password.send_keys('pass1')
            submit.click()


        except TimeoutException:
            print("Timed out waiting for page to load")

        assert True

    @allure.step('Отправка запроса на пополнение')
    def submit_pay(self):

        """

        Пополнение баланса
        Отправка формы

        """
        element_bonus = EC.presence_of_element_located((By.CSS_SELECTOR, "total"))
        WebDriverWait(self.driver, 10).until(element_bonus)
        submit = self.driver.find_element_by_xpath("//submit/div/a/span[@class='text']")
        submit.click()

        assert True

    @allure.step('Назад к форме запроса на пополнение')
    def back_to_pay(self):

        """

        Пополнение баланса
        Назад к форме пополнения

        """
        element_bonus = EC.presence_of_element_located((By.XPATH, "//div[@class='deposit-result result']"))
        WebDriverWait(self.driver, 10).until(element_bonus)
        back = self.driver.find_element_by_xpath("//a[@class='dashed-link']")
        back.click()

        assert True

    @allure.step('Установка чекбокса на бонусы')
    def set_bonus_checkbox(self, chk):

        """

        Пополнение баланса
        Установка чекбокса на бонусы

        """

        element_bonus = EC.presence_of_element_located((By.CSS_SELECTOR, "total"))
        WebDriverWait(self.driver, 10).until(element_bonus)


        bonus = self.driver.find_element_by_xpath("//label[@for='bonus-activator']")
        if (chk):
            bonus.click()

        assert True

    @allure.step('Выбор платежной системы')
    def select_payment_system(self, system):

        """

        Пополнение баланса
        Выбор платежной системы

        """
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "amount-inputs"))
        WebDriverWait(self.driver, 10).until(element_present)
        payment_items = self.driver.find_element_by_xpath("//payment-system-selector")
        select_pay = payment_items.find_element_by_xpath(".//rg-select/div[@name='selectfield']")
        select_pay.click()
        select_pays = payment_items.find_elements_by_xpath(".//rg-select/ul/li")
        for pay in select_pays:
            #pa = pay.find_element_by_xpath(".//li")
            pay_str = pay.find_element_by_xpath(".//span[@class='title']").get_attribute('innerHTML')
            logger.debug('pay: ' + str(pay_str))
            if (system in pay_str):
                pay.click()


        assert True

    @allure.step('Выбор валюты')
    def select_currency(self, curen):

        """

        Пополнение баланса
        Выбор валюты

        """
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "amount-inputs"))
        WebDriverWait(self.driver, 10).until(element_present)

        amount_items = self.driver.find_element_by_xpath("//amount-inputs")
        amount = amount_items.find_element_by_xpath(".//div[@class='amount']/input[@name='amount']")
        amount.clear()
        amount.send_keys('10002')

        select_cur = amount_items.find_element_by_xpath(".//rg-select/div[@name='selectfield']")
        select_cur.click()
        select_curs = amount_items.find_elements_by_xpath(".//rg-select/ul/li")
        for cur in select_curs:
            cur_str = cur.find_element_by_xpath(".//span").get_attribute('innerHTML')
            logger.debug('cur: ' + str(cur_str))
            if (curen in cur_str):
                cur.click()


        assert True

    @allure.step('Ввод суммы')
    def enter_amount(self, amo):

        """

        Пополнение баланса
        Ввод суммы

        """
        element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "amount-inputs"))
        WebDriverWait(self.driver, 10).until(element_present)

        amount_items = self.driver.find_element_by_xpath("//amount-inputs")
        amount = amount_items.find_element_by_xpath(".//div[@class='amount']/input[@name='amount']")
        amount.clear()
        amount.send_keys(amo)


        assert True
    #
    # amo = ['10003']
    # curr = ['CNH']
    # paysystem = ['Payweb']
    # chk = [True]
    #
    # @pytest.mark.parametrize('number,vowel,consonant',
    #                          itertools.product(amou, curr, paysystem, chk)
    #                          )

    def test_refill_balanse(self):
        """

        Пополнение баланса
        используется бонус, валюта, сумма, платежная система
            password.send_keys('pass1')

        """
        self.auth_open_link_in_browser()
        self.enter_amount('1004')
        self.select_currency('CNH')
        self.select_payment_system('Payweb')
        self.set_bonus_checkbox(True)
        self.submit_pay()
        self.back_to_pay()

    def test_user_status(self):
        """

        Проверка статуса пользователя после пополнения
        Mini, Silver, Gold, VIP

        """

        assert True

    def test_user_privelege(self):
        """

        Проверка привилегий статусов

        """

        assert True

    def test_terms_of_the_bonus_program(self):
        """

        Проверка условий бонусной программы

        """

        assert True