# -*- coding: utf-8 -*-
import allure
import pytest
import logging
import sys, os
import nistest
import io
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import collections
import json
import random
from hamcrest import *
import TestLib

log = logging.getLogger('drs_operations')

config = {
    'kafka_topic_raw': 'ru.nis.idg.terminal.rawData.smartFarm',
    'kafka_topic_valid': 'ru.nis.idg.terminal.validData.smartFarm',
    'kafka_topic_changed': 'ru.nis.drs.terminal.changedData',
    'kafka_server': 'kafka1',
    'kafka_schema': 'kafka-schema-registry',
    'kafka_zoo': 'zoo1',
    'db_host': 'sql',
    'db_port': 5432,
    'db_database': 'terminal',
    'db_database_history': 'sodmtd',
    'db_table': 'tbl_terminal',
    'db_table_history': 'tbl_smart_farm',
    'db_user': 'postgres',
    'service_name': 'drs',
    'service_host_drs': 'drs',
    'service_port_drs': '9080',
    'service_host_hds': 'hds',
    'service_port_hds': '9080',
    'service_host_info': 'info-serviced',
    'service_port_info': '8082',
}


testlib = TestLib.INFOLib()
testlib.set_config(config=config)

@pytest.fixture(scope="class")
def INFO():
    authorise = nistest.basic.auth(user='userIS', pwd='test123', use=True)
    testlib = TestLib.INFOLib(host=config.get('service_host_info'), port=config.get('service_port_info'), authorise=authorise)
    yield testlib

@allure.feature('INFO operation feature')
@allure.feature('info')
@allure.label('info operations')
class Test_HDS_Basic():

    @allure.testcase('Testcase-1 Test get device type')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Get device')
    def test_get_device(self, INFO):
        '''

        Create device test

        Send http request to get device type info

        '''

        allure.description('Testing info get device')

        response = INFO.get_device()
        #assert response.status_code == 200
        # assert response.text == {}

    @allure.testcase('Testcase-2 Test get model device')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Get model')
    def test_get_model(self, INFO):
        '''

        Create device test

        Send http request to get device model

        '''

        allure.description('Testing info get protocol')

        response = INFO.get_model()
        #assert response.status_code == 200
        #assert response.text == {}


    @allure.testcase('Testcase-3 Test get protocol device')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Get protocol')
    def test_get_protocol(self, INFO):
        '''

        Create device test

        Send http request to get device protocol

        '''

        allure.description('Testing info get protocol')

        response = INFO.get_protocol()
        #assert response.status_code == 200
        # assert response.text == {}