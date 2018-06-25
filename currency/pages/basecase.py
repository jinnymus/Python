from unittest import TestCase
import pytest
import logging
import sys

#logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
#logger = logging.getLogger('test')

@pytest.mark.usefixtures('d')
class BaseCase(TestCase):

    pass