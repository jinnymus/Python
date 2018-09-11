#!/bin/bash
py.test -s -vvv --alluredir site/reports site/test_one/test_url.py
#allure-2.6.0/bin/allure generate --clean /home/ub/PycharmProjects/tests/site/reports
#allure-2.6.0/bin/allure serve /home/ub/PycharmProjects/tests/site/reports


