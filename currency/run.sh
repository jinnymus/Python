#!/usr/bin/env bash

pytest -vv tests/test_basic.py
allure-2.6.0/bin/allure generate -o tests/allure -- tests/report
allure-2.6.0/bin/allure serve tests/report/
