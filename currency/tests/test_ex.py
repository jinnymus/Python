import pytest
from pages.currency_page_f import CurrencyPage_func
from django.conf import settings
from unittest import TestCase
import logging
import sys

site = 'https://www.exness.com/tools/converter/'

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger('test')

settings.configure()
all_list = tuple()

def test_get_all_list(CurrencyPage_func, d):
    global cp
    global all_list
    cp = CurrencyPage_func(d)
    cp.navigate()
    all_list = tuple(cp.tab_from.get_all_list_names())
    logging.info(all_list)

@pytest.mark.parametrize('currency', all_list)
def test_currency(currency, CurrencyPage_func, d):
    #cp = CurrencyPage_func(d)
    #cp.navigate()
    #cp.tab_from.set_amount(100)
    logging.debug(currency)
    #cp.tab_to.select_top_currency(currency)
    #cp.tab_from.select_top_currency('USD')
    #cp.click_clear_button()

