import pytest
import allure
import selenium
from selenium import webdriver
import os
import sys
import seleniumwrapper as selwrap
#import getcwd
#import popen
#
# @pytest.fixture(scope="class")
# def driver_init(request):
#     from selenium import webdriver
#     web_driver = webdriver.Firefox()
#     request.cls.driver = web_driver
#     yield
#     #web_driver.close()

# @pytest.yield_fixture(params=browsers.keys())
# def driver(request):
#     browser = browsers[request.param]()
#     # Тут я создаю ексзепляр класса и передаю ему драйвер.
#     login_page = LoginPage(browser)
#     login_page.open_page('https://client.triggmine.com.ua/login')
#     yield login_page
#     browser.quit()

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox", help="Type of browser: ie, chrome, firefox")

#@pytest.fixture(scope="class")
#@pytest.fixture()
@pytest.yield_fixture(scope='module')
def get_driver(request):

    browser = request.config.getoption('--browser')
    # results_dir = os.path.join(os.getcwd(), 'results')
    #
    # if not os.path.exists(results_dir):
    #     os.makedirs(results_dir)

    # log_path = os.path.join(results_dir, 'driver.log')
    # drivers_dir = os.path.join(os.getcwd(), 'drivers')

    # driver = None
    # driver_name = dict(
    #     firefox='geckodriver',
    #     chrome='chromedriver'
    # )[browser]
    # driver_path = os.path.join(drivers_dir, driver_name)

    if browser == 'firefox':
        # driver = webdriver.Firefox(executable_path=driver_path, log_path=log_path)
        driver = webdriver.Firefox()
    elif browser == 'chrome':
        driver = webdriver.Chrome()
        # driver = webdriver.Chrome(executable_path=driver_path, service_log_path=log_path)

    request.cls.CurrencyPage.driver = driver

    # driver.page_config = config['page_config']
    # driver.locators = config['locators']
    driver.maximize_window()
    #yield driver

    def close_driver():
        print('[close_driver]')
        #driver.quit()

    request.addfinalizer(close_driver)
    return driver

@pytest.fixture()
def currency_page(get_driver):
    from pages.currency_page import CurrencyPage
    page = CurrencyPage(get_driver)
    page.navigate()
    return page


@pytest.yield_fixture(scope='class')
def firefox_driver_setup(request):
    driver = selwrap.create("firefox")
    request.cls.driver = driver
    #request.cls.CurrencyPage = CurrencyPage(driver)
    yield driver
    driver.close()

@pytest.fixture(scope='class')
def d(request):
    from selenium import webdriver

    driver = webdriver.Firefox()
    request.cls.driver = driver

    def fin():
        driver.quit()

    #request.addfinalizer(fin)

# @pytest.fixture()
# def get_driver(request):
#     browser = request.config.getoption('--browser')
#     results_dir = os.path.join(os.getcwd(), 'results')
#
#     if not os.path.exists(results_dir):
#         os.makedirs(results_dir)
#
#     log_path = os.path.join(results_dir, 'driver.log')
#     drivers_dir = os.path.join(os.getcwd(), 'drivers')
#
#     os_name = os.system().lower()
#     os_arch = ''.join([s for s in os.architecture()[0] if s.isdigit()])
#     os_type = os_name + os_arch
#     driver = None
#     driver_name = dict(
#         firefox='geckodriver',
#         chrome='chromedriver'
#     )[browser]
#     driver_path = path.join(drivers_dir, driver_name, os_type, driver_name)
#     if os_name == 'windows':
#         driver_path += '.exe'
#
#     if browser == 'firefox':
#         cap = webdriver.DesiredCapabilities().FIREFOX
#         cap['marionette'] = False
#         driver = webdriver.Firefox(executable_path=driver_path,
#                                    log_path=log_path,
#                                    capabilities=cap)
#     elif browser == 'chrome':
#         driver = webdriver.Chrome(executable_path=driver_path, service_log_path=log_path)
#
#     print(os.popen(driver_path + ' --version').read())
#     driver.maximize_window()
#
#     def close_driver():
#         driver.quit()
#
#     request.addfinalizer(close_driver)
#     return driver


# @pytest.fixture(scope="function")
# def screenshot_on_failure(request):
#     def fin():
#         driver = SeleniumWrapper().driver
#         attach = driver.get_screenshot_as_png()
#         if request.node.rep_setup.failed:
#             allure.attach(request.function.__name__, attach, allure.attach_type.PNG)
#         elif request.node.rep_setup.passed:
#             if request.node.rep_call.failed:
#                 allure.attach(request.function.__name__, attach, allure.attach_type.PNG)
#     request.addfinalizer(fin)

# def pytest_exception_interact(node, call, report):
#     driver = node.instance.driver
#     allure.attach(
#         name='Скриншот',
#         contents=driver.get_screenshot_as_png(),
#         type=allure.constants.AttachmentType.PNG,
#     )