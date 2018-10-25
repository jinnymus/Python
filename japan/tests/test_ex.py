import pytest
from pages.currency_page_f import CurrencyPage_func
from django.conf import settings
from unittest import TestCase
import logging
import sys
import glob
import globals as gbl

site = 'https://www.exness.com/tools/converter/'

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

settings.configure()


#all_list = [1,3]
#def pytest_namespace():
#    return {'all_list': 0}


def get_all_list():
    #t = TestCase()
    #return globals()[
    # "all_list"]
    #return getattr(thismodule,'all_list')
    return gbl.all_list

    #return [1,3]

@pytest.fixture
def data():
    pytest.all_list = 100

#def test_get_all_list_args(CurrencyPage_func, d):
def test_get_all_list():
    #global cp
    #global all_list
    #cp = CurrencyPage_func(d)
    #cp.navigate()
    #logging.debug('all_list: ' + str(cp.tab_from.get_all_list_names()))
    #self.all_list = tuple(cp.tab_from.get_all_list_names())
    #self.all_list = cp.tab_from.get_all_list_names()
    #assert False, str(self.all_list)
    #all_list = [1,5]
    #all_list = [1, 5]
    def CurrencyPage_func():

    #globals()['all_list'] = [1, 5]
    #setattr(thismodule, 'all_list', [1,5])
    gbl.all_list = [1,5]

    #return all_list
    #logging.debug('TestSuite.all_list: ' + str(TestSuite.all_list))
    #logging.debug('self.all_list: ' + str(self.all_list))

@pytest.mark.parametrize('currency', get_all_list())
#def test_currency(self, currency, CurrencyPage_func, d):
#def test_currency(self, currency):
#@pytest.fixture(scope="function", params=globals()["all_list"])
#def test_currency(currency, CurrencyPage_func, d):
#@pytest.fixture(scope="function", params=[1,3])
def test_currency(currency, request):
    #logging.debug('currency start')
    #cp = CurrencyPage_func(d)
    #cp.navigate()
    #cp.tab_from.set_amount(100)
    #logging.debug('currency: ' + str(request.param))
    logging.debug('currency: ' + str(currency))
    #cp.tab_to.select_top_currency(currency)
    #cp.tab_from.select_top_currency('USD')
    #cp.click_clear_button()

# def test_currency2(test_currency):
#     #cp = CurrencyPage_func(d)
#     #cp.navigate()
#     #cp.tab_from.set_amount(100)
#     #logging.debug('currency: ' + str(request.param))
#     logging.debug('currency: ' + str(test_currency))
#     #cp.tab_to.select_top_currency(currency)
#     #cp.tab_from.select_top_currency('USD')
#     #cp.click_clear_button()