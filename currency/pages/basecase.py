from unittest import TestCase
import pytest
import logging
import sys

@pytest.mark.usefixtures('d')
class BaseCase(TestCase):

    pass