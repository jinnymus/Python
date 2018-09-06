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
import time
from datetime import datetime, timedelta
from pytest_testrail.plugin import pytestrail

log = logging.getLogger('hds_operations')

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
    'service_host_info': 'info',
    'service_port_info': '8082',
}


@pytest.fixture(scope="function")
def KAFKAjson():
    testlib = TestLib.KAFKALib(topic=config.get('kafka_topic_raw'), lang='json', server=config.get('kafka_server'),
                                 schema_registry = config.get('kafka_schema'), server_zoo = config.get('kafka_schema'))
    testlib.service.delete_topic()
    yield testlib

@pytest.fixture(scope="function")
def KAFKAavro():
    testlib = TestLib.KAFKALib(topic=config.get('kafka_topic_valid'), lang='avro', server=config.get('kafka_server'),
                                 schema_registry = config.get('kafka_schema'), server_zoo = config.get('kafka_schema'))
    testlib.service.delete_topic()
    yield testlib

@pytest.fixture(scope="function")
def HDS():
    authorise = nistest.basic.auth(user='tester', pwd='12345678', use=True)
    testlib = TestLib.HDSLib(host=config.get('service_host_hds'), port=config.get('service_port_hds'), authorise=authorise)
    yield testlib

@pytest.fixture(scope="function")
def HDS():
    authorise = nistest.basic.auth(user='tester', pwd='12345678', use=True)
    testlib = TestLib.HDSLib(host=config.get('service_host_hds'), port=config.get('service_port_hds'), authorise=authorise)
    yield testlib


@pytest.fixture(scope="function")
def DBHistory():
    testlib = TestLib.DBLib(db_host=config.get('db_host'), db_port=config.get('db_port'),
                            db_user=config.get('db_user'), db_pwd=config.get('db_pwd'), db_database=config.get('db_database_history'),
                            db_table=config.get('db_table_history'))
    yield testlib

@allure.feature('rest')
@allure.label('rest checker')
class Test_HDS_Basic():

    @allure.testcase('Testcase Test invalid json')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.feature('hds')
    @allure.story('HTTP Errors')
    def test_invalid_json(self, HDS):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Testing hds http 400 invalid json')


        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-06-27T09:08:28+03:00'
        dateTo = '2018-06-27T09:08:28+03:00'

        termId = '1'
        filter = '1'
        limit = 1
        sort = 'asc'
        device_activity_info = random.randint(1, 100000)

        params = 'termId={0}&filter={1}&limit={2}&sort={3}'.format(str(termId), str(filter), str(limit), str(sort))

        payload = '''{
          "startTime": ''' + str(startTime) + ''',
          "endTime": ''' + str(endTime) + ''',
          "hideTimes": [
             { "from": ''' + str(dateFrom) + ''', "to": ''' + str(dateTo) + '''}
          ]
        '''

        headers = {
            'Authorization': str(HDS.service.authorise.get_basic_auth()),
            'Content-Type': 'application/json',
             'X-Sender': 'nistest2'
        }

        response = HDS.service.request(method='get_history', path=HDS.service.paths.get('get_history') + str(params), payload=payload, headers=headers)
        assert response.status_code == 400
        assert response.text == 'invalid json'

    @allure.testcase('Testcase Test absent header')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('HTTP Errors')
    def test_absent_header(self, HDS):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Testing hds http 400 invalid json')


        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-06-27T09:08:28+03:00'
        dateTo = '2018-06-27T09:08:28+03:00'

        termId = '1'
        filter = '1'
        limit = 1
        sort = 'asc'
        device_activity_info = random.randint(1, 100000)

        params = 'termId={0}&filter={1}&limit={2}&sort={3}'.format(str(termId), str(filter), str(limit), str(sort))

        payload = '''{
          "startTime": ''' + str(startTime) + ''',
          "endTime": ''' + str(endTime) + ''',
          "hideTimes": [
             { "from": ''' + str(dateFrom) + ''', "to": ''' + str(dateTo) + '''}
          ]
        '''

        headers = {
            'Authorization': str(HDS.service.authorise.get_basic_auth()),
            'Content-Type': 'application/json'
        }

        response = HDS.service.request(method='get_history', path=HDS.service.paths.get('get_history') + str(params), payload=payload, headers=headers)
        assert response.status_code == 400
        assert response.text == 'absent header x-sender'


    @allure.testcase('Testcase Test invalid auth')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('HTTP Errors')
    def test_invalid_auth(self, HDS):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Testing hds http 400 invalid json')


        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-06-27T09:08:28+03:00'
        dateTo = '2018-06-27T09:08:28+03:00'

        termId = '1'
        filter = '1'
        limit = 1
        sort = 'asc'
        device_activity_info = random.randint(1, 100000)

        params = 'termId={0}&filter={1}&limit={2}&sort={3}'.format(str(termId), str(filter), str(limit), str(sort))

        payload = '''{
          "startTime": ''' + str(startTime) + ''',
          "endTime": ''' + str(endTime) + ''',
          "hideTimes": [
             { "from": ''' + str(dateFrom) + ''', "to": ''' + str(dateTo) + '''}
          ]
        '''

        HDS.service.authorise.set('pwd', '123')

        headers = {
            'Authorization': str(HDS.service.authorise.get_basic_auth()),
            'Content-Type': 'application/json'
        }

        response = HDS.service.request(method='get_history', path=HDS.service.paths.get('get_history') + str(params), payload=payload, headers=headers)
        assert response.status_code == 400
        assert response.text == 'absent header x-sender'