#!/usr/bin/env bash

pytest -vvrxXs tests/test_notam.py -s --alluredir report #| grep -v 'charsetgroupprober.py' #> test.log
allure-2.6.0/bin/allure generate -o tests/allure -- report --clean
allure-2.6.0/bin/allure serve report

