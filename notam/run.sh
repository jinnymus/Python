#!/usr/bin/env bash

pytest -vvrxXs tests/test_notam.py -s #| grep -v 'charsetgroupprober.py' #> test.log
#allure-2.6.0/bin/allure generate -o tests/allure -- tests/report
#allure-2.6.0/bin/allure serve tests/report/
