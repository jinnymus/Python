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

@allure.feature('HDS operation feature')
@allure.feature('hds')
@allure.label('hds operations')
class Test_HDS_Basic():

    @allure.testcase('Testcase-1 Test get history')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.feature('hds')
    @allure.feature('kafka')
    @allure.feature('avro')
    @allure.feature('db')
    @allure.story('Get history')
    def test_get_history(self, HDS, KAFKAavro):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Testing hds get history')


        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-06-27T09:08:28+03:00'
        dateTo = '2018-06-27T09:08:28+03:00'

        log.debug('[test_get_history] dateFrom: ' + str(dateFrom))
        device_v_term_id = random.randint(1, 100000)

        filter = 'null'
        limit = 1
        sort = 'asc'
        device_activity_info = random.randint(1, 100000)

        expected = []

        for tim in range(2):

            device_time_device = 1530523171000 + 1000 * tim
            device_time_device_utc = datetime.fromtimestamp(int(device_time_device / 1000)).strftime(
                '%Y-%m-%dT%H:%M:%SZ')

            expected_dict = {}
            expected_dict['activityInfo'] = device_activity_info
            expected_dict['termId'] = device_v_term_id
            expected_dict['timeDevice'] = device_time_device_utc
            expected.append(expected_dict)
            KAFKAavro.send_valid(termId=device_v_term_id, time_platform=device_time_device, time_device=device_time_device,
                                       activity_info=device_activity_info)

        '''
        -----------------------------------------------------------------------------
        get history
        -----------------------------------------------------------------------------
        '''

        response = HDS.get_history(expected=expected, termId=device_v_term_id, limit=None, sort='asc', filter=None,
                                             startTime=startTime, endTime=endTime, dateFrom=dateFrom, dateTo=dateTo)



    @allure.testcase('Testcase-1 Test get history with empty term_id')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.feature('hds')
    @allure.feature('kafka')
    @allure.feature('avro')
    @allure.feature('db')
    @allure.story('Get history')
    @allure.story('HTTP Errors')
    def test_get_history_empty_term_id(self, HDS, KAFKAavro):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Testing hds get history')


        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-06-27T09:08:28+03:00'
        dateTo = '2018-06-27T09:08:28+03:00'

        '''
        -----------------------------------------------------------------------------
        get history
        -----------------------------------------------------------------------------
        '''

        response = HDS.get_history(expected=None, termId=None, limit=None, sort='asc', filter=None,
                                             startTime=startTime, endTime=endTime, dateFrom=dateFrom, dateTo=dateTo, no_check=True)
        assert response.status_code == 400
        expected = {"developerMessage": "Required query parameter in URI 'termId'", "errorCode": 1,
         "errorMessage": "Required query parameter in URI 'termId'"}
        assert nistest.basic.CompareDriver(data_result=response.json(), data_expected=expected, lang='json', dump=False)


    @allure.testcase('Testcase-3 Test get history hide')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Get history hide')
    def test_get_history_hide(self, HDS, KAFKAavro, DBHistory):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Testing hds get history hide equal time')


        '''
        -----------------------------------------------------------------------------
        prepare infra
        -----------------------------------------------------------------------------
        '''

        KAFKAavro.service.delete_topic()

        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-07-02T09:19:32+03:00'
        dateTo = '2018-07-02T09:19:32+03:00'


        log.debug('[test_get_history] dateFrom: ' + str(dateFrom))
        device_v_term_id = random.randint(1, 100000)
        filter = 'null'
        limit = 1
        sort = 'asc'

        expected = []
        device_activity_info = random.randint(1, 100000)

        for tim in range(2):

            device_activity = device_activity_info + tim
            device_time_device = 1530523171000 + 1000 * tim
            device_time_device_utc = datetime.fromtimestamp(int(device_time_device / 1000)).strftime(
                '%Y-%m-%dT%H:%M:%SZ')

            KAFKAavro.send_valid(termId=device_v_term_id, time_platform=device_time_device, time_device=device_time_device,
                                       activity_info=device_activity)

        '''
        -----------------------------------------------------------------------------
        get history
        -----------------------------------------------------------------------------
        '''
        device_time_device_utc = datetime.fromtimestamp(int(1530523171000 / 1000)).strftime(
                '%Y-%m-%dT%H:%M:%SZ')
        expected = [{
                        "activityInfo": device_activity_info,
                        "termId": device_v_term_id,
                        "timeDevice": device_time_device_utc
                    }]

        response = HDS.get_history(expected=expected, termId=device_v_term_id, limit=None, sort='asc', filter=None,
                                             startTime=startTime, endTime=endTime, dateFrom=dateFrom, dateTo=dateTo)


    @allure.testcase('Testcase-3 Test send to validator')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Send to validator')
    def test_send_to_validator(self, KAFKAavro, HDS):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Testing hds send to validator')


        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-07-02T09:19:32+03:00'
        dateTo = '2018-07-02T09:19:32+03:00'

        log.debug('[test_get_history] dateFrom: ' + str(dateFrom))
        device_v_term_id = random.randint(1, 100000)
        filter = 'null'
        limit = 1
        sort = 'asc'

        expected = []

        for tim in range(2):

            device_activity_info = random.randint(1, 100000)
            device_time_device = 1530523171000 + 1000 * tim
            device_time_device_utc = datetime.fromtimestamp(int(device_time_device / 1000)).strftime(
                '%Y-%m-%dT%H:%M:%SZ')

            KAFKAavro.send_valid(termId=device_v_term_id, time_platform=device_time_device, time_device=device_time_device,
                                       activity_info=device_activity_info)

    @allure.testcase('https://jira.nis-glonass.ru/jira/browse/DEV-555')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Get history hide intervale equals')
    @pytestrail.case('C2')
    def test_get_history_hide_interval_empty_response(self, HDS, KAFKAavro, DBHistory):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Test get history hide interval equals and response empty')


        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''


        device_v_term_id = random.randint(1, 100000)
        filter = 'null'
        limit = 1
        sort = 'asc'
        device_activity_info = random.randint(1, 100)
        expected = []

        for t in range(2):

            device_time_device = datetime.strptime('2018-07-02 09:19:3' + str(t), "%Y-%m-%d %H:%M:%S").strftime('%s000')
            KAFKAavro.send_valid(termId=device_v_term_id, time_platform=int(device_time_device), time_device=int(device_time_device),
                                       activity_info=device_activity_info)

        '''
        -----------------------------------------------------------------------------
        get history
        -----------------------------------------------------------------------------
        '''


        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-07-02T09:19:30+03:00'
        dateTo = '2018-07-02T09:19:33+03:00'
        device_time_device_utc = '2018-07-02T09:19:30Z'

        expected = [{
                        "activityInfo": device_activity_info,
                        "termId": device_v_term_id,
                        "timeDevice": device_time_device_utc
        }]

        response = HDS.get_history(expected=expected, termId=device_v_term_id, limit=None, sort='asc', filter=None,
                                             startTime=startTime, endTime=endTime, dateFrom=dateFrom, dateTo=dateTo, no_check=True)

        assert response.status_code == 200
        expected = [ "Data not found" ]
        assert nistest.basic.CompareDriver(data_result=response.json(), data_expected=expected, lang='json', dump=False)

    @allure.testcase('Testcase-5 Test get history hide interval')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Get history hide interval')
    def test_get_history_hide_interval(self, HDS, KAFKAavro, DBHistory):
        '''

        Create device test

        Send http request to read history

        '''
        allure.description('Test get history hide interval')


        '''
        -----------------------------------------------------------------------------
        send message
        -----------------------------------------------------------------------------
        '''


        device_v_term_id = random.randint(1, 100000)
        filter = 'null'
        limit = 1
        sort = 'asc'
        device_activity_info = random.randint(1, 100)


        for t in range(5):

            device_activity_info += 1
            device_time_device = datetime.strptime('2018-07-02 09:19:3' + str(t), "%Y-%m-%d %H:%M:%S").strftime('%s000')
            KAFKAavro.send_valid(termId=device_v_term_id, time_platform=int(device_time_device), time_device=int(device_time_device),
                                       activity_info=device_activity_info)

        '''
        -----------------------------------------------------------------------------
        get history
        -----------------------------------------------------------------------------
        '''


        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-07-02T09:19:30+03:00'
        dateTo = '2018-07-02T09:19:33+03:00'
        device_time_device_utc = '2018-07-02T09:19:34Z'

        expected = [{
                        "activityInfo": device_activity_info,
                        "termId": device_v_term_id,
                        "timeDevice": device_time_device_utc
        }]

        response = HDS.get_history(expected=expected, termId=device_v_term_id, limit=None, sort='asc', filter=None,
                                             startTime=startTime, endTime=endTime, dateFrom=dateFrom, dateTo=dateTo)
