#!/usr/bin/env bash

sudo chown -R kir:kir *
sudo find . -name '.pytest_cache' -exec rm -rf {} \;
sudo find . -name '__pycache__' -exec rm -rf {} \;
sudo find . -name '*.pyc' -exec rm -rf {} \;
sudo find . -name '*.log' -exec rm -rf {} \;
sudo find . -name 'nistest.egg-info' -exec rm -rf {} \;
rm -rf ./tests/report/*
rm -rf ./tests/allure/*
rm -rf ./allure/*
rm -rf ./tests/pytests/lib/dist/*
