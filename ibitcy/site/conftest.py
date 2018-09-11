import pytest
import allure
import selenium

@pytest.fixture(scope="class")
def driver_init(request):
    from selenium import webdriver
    web_driver = webdriver.Firefox()
    request.cls.driver = web_driver
    yield
    #web_driver.close()

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