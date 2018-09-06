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
from allure_commons._allure import epic, feature, story
#from pytest_testrail.plugin import pytestrail

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


@pytest.fixture(scope="function")
def DRS():
    authorise = nistest.basic.auth(user='tester', pwd='12345678', use=True)
    testlib = TestLib.DRSLib(host=config.get('service_host_drs'), port=config.get('service_port_drs'), authorise=authorise)
    yield testlib

@pytest.fixture(scope="function")
def DB():
    testlib = TestLib.DBLib(db_host=config.get('db_host'), db_port=config.get('db_port'),
                            db_user=config.get('db_user'), db_pwd=config.get('db_pwd'), db_database=config.get('db_database'),
                            db_table=config.get('db_table'))
    yield testlib


@allure.feature('DRS operation feature')
@allure.label('drs operations')
class Test_DRS_Basic():

    @allure.testcase('Testcase-1 Test create device')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.feature('drs')
    @allure.issue('http://jira.lan/browse/ISSUE-3')
    @allure.testcase('http://localhost/TC-001')
    @allure.story('Create device story')
    @epic('Epic1')
    #@pytestrail.case('C1')
    def test_create_device(self, DRS):

        '''

        Create device test

        Send http request to create device

        '''

        allure.description('Testing drs creating device')

        devicetype = 'ovibovi'
        model = 'OVI-BOVI'
        hubId = 0

        device2 = DRS.create_device(deviceType=devicetype, model=model, hubId=hubId, sensorId=random.randint(1, 100000))

    @allure.testcase('Testcase-2 Test create and delete device')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create and delete device story')
    def test_create_and_delete_device(self, DRS):
        '''

        Create and delete device test

        Send http request to create and then delete device

        '''

        allure.description('Testing drs creating and delete device')

        deviceType = 'ovibovi'
        model = 'OVI-BOVI'
        hubId = 0

        device = DRS.create_device(deviceType=deviceType, model=model, hubId=hubId, sensorId=random.randint(1, 100000))
        DRS.delete_device(device=device)
        device = DRS.get_device(termId=device.termId)



    @allure.testcase('Testcase-3 Test create device raw')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create device raw')
    def test_create_device_raw(self, DRS):
        '''

        Create device test

        Send http request to create device

        '''

        allure.description('Testing drs creating device from raw')

        json_data = {
            "deviceType": 'ovibovi',
            "model": 'OVI-BOVI',
            "hubId": 0,
            "sensorId": random.randint(1, 100000)
        }

        DRS.create_device_raw( payload=json_data)

    @allure.testcase('Testcase-4 Test create device if exist')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create device if exist')
    def test_create_device_if_exist(self, DRS):

        '''

        Create device test

        Send http request to create device if exist

        '''

        allure.description('Testing drs creating device if exist')

        deviceType = 'ovibovi'
        model = 'OVI-BOVI'
        hubId = 0
        sensorId = random.randint(1, 100000000)

        device = DRS.create_device(deviceType=deviceType, model=model, hubId=hubId, sensorId=sensorId)

        device2 = DRS.create_device(deviceType=deviceType, model=model, hubId=hubId, sensorId=sensorId, no_check=True)
        assert device2.response.status_code == 400, 'response: ' + str(device2.response.text)

        expected_response = {"developerMessage":"Can't registrate terminal","errorCode":1,"errorMessage":"Can't registrate terminal"}
        assert device2.response.json() == expected_response, 'response: ' + str(device2.resp.text)


    @allure.testcase('Testcase-5 Test change device')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create and change device')
    def test_create_and_change_device(self, DRS):
        '''

        Create device test

        Send http request to create device

        '''

        allure.description('Testing drs change device')

        deviceType = 'ovibovi'
        model = 'OVI-BOVI'
        hubId = 0

        device = DRS.create_device(deviceType=deviceType, model=model, hubId=hubId, sensorId=random.randint(1, 100000))
        device = DRS.change_device(device=device, statusId=5)


    @allure.testcase('Testcase-6 Test get device')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Get device')
    def test_get_device(self, DRS):

        '''

        Create device test

        Send http request to create device

        '''

        allure.description('Testing drs creating device')

        devicetype = 'ovibovi'
        model = 'OVI-BOVI'
        hubId = 0

        device = DRS.create_device(deviceType=devicetype, model=model, hubId=hubId, sensorId=random.randint(1, 100000))
        device = DRS.get_device(termId=device.id)

