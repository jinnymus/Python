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
from datetime import datetime

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
    'service_host_info': 'info',
    'service_port_info': '8082',
}

@pytest.fixture(scope="class")
def KAFKAjson():
    testlib = TestLib.KAFKALib(topic=config.get('kafka_topic_raw'), lang='json', server=config.get('kafka_server'),
                                 schema_registry = config.get('kafka_schema'), server_zoo = config.get('kafka_schema'))
    testlib.service.delete_topic()
    yield testlib

@pytest.fixture(scope="class")
def KAFKAavro():
    testlib = TestLib.KAFKALib(topic=config.get('kafka_topic_valid'), lang='avro', server=config.get('kafka_server'),
                                 schema_registry = config.get('kafka_schema'), server_zoo = config.get('kafka_schema'))
    testlib.service.delete_topic()
    yield testlib

@pytest.fixture(scope="class")
def KAFKAchanged():
    testlib = TestLib.KAFKALib(topic=config.get('kafka_topic_changed'), lang='json', server=config.get('kafka_server'),
                                 schema_registry = config.get('kafka_schema'), server_zoo = config.get('kafka_schema'))
    testlib.service.delete_topic()
    yield testlib

@pytest.fixture(scope="class")
def DRS():
    authorise = nistest.basic.auth(user='tester', pwd='12345678', use=True)
    testlib = TestLib.DRSLib(host=config.get('service_host_drs'), port=config.get('service_port_drs'), authorise=authorise)
    yield testlib

@pytest.fixture(scope="class")
def HDS():
    authorise = nistest.basic.auth(user='tester', pwd='12345678', use=True)
    testlib = TestLib.HDSLib(host=config.get('service_host_hds'), port=config.get('service_port_hds'), authorise=authorise)
    yield testlib

@pytest.fixture(scope="class")
def INFO():
    authorise = nistest.basic.auth(user='userIS', pwd='test123', use=True)
    testlib = TestLib.INFOLib(host=config.get('service_host_info'), port=config.get('service_port_info'), authorise=authorise)
    yield testlib

@pytest.fixture(scope="class")
def DB():
    testlib = TestLib.DBLib(db_host=config.get('db_host'), db_port=config.get('db_port'),
                            db_user=config.get('db_user'), db_pwd=config.get('db_pwd'), db_database=config.get('db_database'),
                            db_table=config.get('db_table'))
    yield testlib

@pytest.fixture(scope="class")
def DBHistory():
    testlib = TestLib.DBLib(db_host=config.get('db_host'), db_port=config.get('db_port'),
                            db_user=config.get('db_user'), db_pwd=config.get('db_pwd'), db_database=config.get('db_database_history'),
                            db_table=config.get('db_table_history'))
    yield testlib


@allure.feature('E2E operation feature')
@allure.feature('e2e')
@allure.label('e2e operations')
class Test_E2E_Basic():

    @allure.testcase('Testcase-1 Test create device by drs read history')
    # @pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create device by drs and read history')
    def test_create_device_by_drs_read_history(self, KAFKAavro, KAFKAchanged, KAFKAjson,
                                              DRS, HDS, INFO, DB,
                                              DBHistory):
        '''

        Create device test

        Send http request to create device

        '''

        allure.description('Testing e2e creating device and read history')

        '''
        -----------------------------------------------------------------------------
        prepare kafka
        -----------------------------------------------------------------------------        
        '''

        KAFKAjson.service.delete_topic()

        '''
        -----------------------------------------------------------------------------
        create device
        -----------------------------------------------------------------------------

        '''
        device_v_device_type = 'hub'
        device_v_model = 'OVI-BOVI'
        hubId = 0
        device_sensorId = random.randint(1, 100000)
        device = DRS.create_device(deviceType=device_v_device_type, model=device_v_model, hubId=hubId, sensorId=device_sensorId)

        device_v_term_id = device.response.json().get('termId')
        device_v_protocol_family_id = 100
        device_v_status_id = device.response.json().get('statusId')
        device_activity_info = 1



        '''
        -----------------------------------------------------------------------------
        check device in db
        -----------------------------------------------------------------------------
        '''
        expected = {'v_status_id': '2'}
        response = DB.get_device(expected=expected, p_term_id=device_v_term_id)

        '''
        -----------------------------------------------------------------------------
        check chanded device in kafka
        -----------------------------------------------------------------------------
        '''

        response = KAFKAchanged.read_changed(term_id=device_v_term_id, deviceType=device_v_device_type, uid=str(device_sensorId))

        '''
        -----------------------------------------------------------------------------
        change status
        -----------------------------------------------------------------------------
        '''
        response = DRS.change_device(device=device, statusId=3)


        '''
        -----------------------------------------------------------------------------
        send raw
        -----------------------------------------------------------------------------
        '''
        device_time_device = 1530523171000
        device_time_device_utc = datetime.fromtimestamp(int(device_time_device / 1000)).strftime('%Y-%m-%dT%H:%M:%SZ')

        KAFKAjson.send_raw(termId=device_v_term_id, protocolId=device_v_protocol_family_id, deviceTypeId=100,
                                     timePlatformFrom1970=device_time_device, timeDeviceFrom1970=device_time_device,
                                     activityInfo=device_activity_info)

        '''
        -----------------------------------------------------------------------------
        check raw
        -----------------------------------------------------------------------------
        '''
        time.sleep(10)
        #KAFKAjson.read_raw(termId=device_v_term_id, protocolId=device_v_protocol_family_id, deviceTypeId=100,
        #                             timePlatformFrom1970=device_time_device, timeDeviceFrom1970=device_time_device,
        #                             activityInfo=device_activity_info)

        '''
        -----------------------------------------------------------------------------
        check valid
        -----------------------------------------------------------------------------
        '''

        log.debug('sleep')
        time.sleep(10)

        #KAFKAavro.read_valid(term_id=device_v_term_id, time_platform=device_time_device,
        #                               time_device=device_time_device, activity_info=device_activity_info)

        '''
        -----------------------------------------------------------------------------
        check history db
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-06-27T09:08:28+03:00'
        dateTo = '2018-06-27T09:08:28+03:00'

        response = DBHistory.get_history(in_term_id=device_v_term_id, in_time_start=startTime,
                                                   in_time_end=endTime)

        '''
        -----------------------------------------------------------------------------
        get history
        -----------------------------------------------------------------------------
        '''

        response = HDS.get_history(termId=device_v_term_id, limit=None, sort='asc', filter=None,
                                             startTime=startTime, endTime=endTime, dateFrom=dateFrom, dateTo=dateTo,
                                             activityInfo=device_activity_info, timeDevice=device_time_device_utc)


    @allure.testcase('Testcase-1 Test create device by db read history')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create device by db and read history')
    def test_create_device_by_db_read_history(self, KAFKAavro, KAFKAchanged, KAFKAjson, DRS, HDS, INFO, DB, DBHistory):

        '''

        Create device test

        Send http request to create device

        '''

        allure.description('Testing e2e creating device and read history')


        '''
        -----------------------------------------------------------------------------
        prepare kafka
        -----------------------------------------------------------------------------        
        '''

        KAFKAjson.service.delete_topic()

        '''
        -----------------------------------------------------------------------------
        create device
        -----------------------------------------------------------------------------
        
        '''
        device_v_device_type = 'hub'
        device_v_model = 'OVI-BOVI'
        hubId = 0
        device_sensorId = random.randint(1, 100000)

        response = DB.create_device(p_device_type=device_v_device_type, p_model=device_v_model, p_hub_id=hubId,
                                         p_sensor_id=device_sensorId)

        device_v_term_id = response.get('v_term_id')
        device_v_protocol_family_id = response.get('v_protocol_family_id')
        device_v_status_id = response.get('v_status_id')
        device_activity_info = 1

        '''
        -----------------------------------------------------------------------------
        check device in db
        -----------------------------------------------------------------------------
        '''
        expected = {'v_status_id': '2'}
        response = DB.get_device(expected=expected, p_term_id=device_v_term_id)


        '''
        -----------------------------------------------------------------------------
        change status
        -----------------------------------------------------------------------------
        '''

        response = DB.set_status(p_term_id=device_v_term_id, p_status_id = 3)

        '''
        -----------------------------------------------------------------------------
        send raw
        -----------------------------------------------------------------------------
        '''
        device_time_device = 1530523171000
        device_time_device_utc = datetime.fromtimestamp(int(device_time_device/1000)).strftime('%Y-%m-%dT%H:%M:%SZ')

        KAFKAjson.send_raw(termId=device_v_term_id, protocolId=device_v_protocol_family_id, deviceTypeId=100,
                                 timePlatformFrom1970=device_time_device, timeDeviceFrom1970=device_time_device, activityInfo=device_activity_info)


        '''
        -----------------------------------------------------------------------------
        check raw
        -----------------------------------------------------------------------------
        '''

        KAFKAjson.read_raw(termId=device_v_term_id, protocolId=device_v_protocol_family_id, deviceTypeId=100,
                                 timePlatformFrom1970=device_time_device, timeDeviceFrom1970=device_time_device, activityInfo=device_activity_info)

        '''
        -----------------------------------------------------------------------------
        check valid
        -----------------------------------------------------------------------------
        '''

        log.debug('sleep')
        time.sleep(20)
        log.debug('sleep')
        KAFKAavro.read_valid(term_id=device_v_term_id, time_platform=device_time_device, time_device=device_time_device, activity_info=device_activity_info )


        '''
        -----------------------------------------------------------------------------
        check history db
        -----------------------------------------------------------------------------
        '''

        startTime = '2018-06-20T09:08:28+03:00'
        endTime = '2018-07-29T09:08:28+03:00'
        dateFrom = '2018-06-27T09:08:28+03:00'
        dateTo = '2018-06-27T09:08:28+03:00'

        response = DBHistory.get_history(in_term_id=device_v_term_id, in_time_start=startTime, in_time_end=endTime)

        '''
        -----------------------------------------------------------------------------
        get history
        -----------------------------------------------------------------------------
        '''

        response = HDS.get_history(termId=device_v_term_id, limit=None, sort='asc', filter=None,
                                          startTime=startTime, endTime=endTime, dateFrom=dateFrom, dateTo=dateTo, activityInfo=device_activity_info, timeDevice=device_time_device_utc)



