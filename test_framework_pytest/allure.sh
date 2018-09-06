#!/usr/bin/env bash

tests/bin/allure-2.6.0/bin/allure generate -o allure -- tests/report
tests/bin/allure-2.6.0/bin/allure serve tests/report
