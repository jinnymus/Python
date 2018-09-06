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
import sqlalchemy
#import psycopg2
log = logging.getLogger('drs_operations')

config = {
    'kafka_topic1': 'ru.nis.idg.terminal.rawData.smartFarm',
    'kafka_topic2': 'ru.nis.idg.terminal.validData.smartFarm',
    'db_host': 'sql',
    'db_port': 5432,
    'db_database': 'terminal',
    'db_user': 'postgres',
}

testlib = TestLib.DBLib()
testlib.set_config(config=config)

@pytest.fixture(scope="class")
def DB():
    smartFarmingObj = nistest.DB(db_host=config.get('db_host'), db_port=config.get('db_port'), db_user=config.get('db_user'), db_pwd=config.get('db_pwd'), db_database=config.get('db_database'))
    yield smartFarmingObj
    smartFarmingObj.close()

@allure.feature('DB operation feature')
@allure.feature('db')
@allure.label('db operations')
class Test_DB_Basic():

    @allure.testcase('Testcase-1 Test get info device')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create device')
    def test_create_device(self, DB):
        '''

        Create device test

        Send http request to create device

        '''

        allure.description('Testing info get device')
        expected_list = {'v_device_type':'hub'}
        response = DB.create_device(p_device_type='hub', p_model='OVI-BOVI', p_hub_id=0, p_sensor_id=101 )
        ids = response.get('v_term_id')
        log.debug('ids: ' + str(ids))


    @allure.testcase('Testcase-2 Test get info device')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create device if exist')
    def test_create_device_if_exist(self, DB):
        '''

        Create device test

        Send http request to create device

        '''

        allure.description('Testing info get device')
        expected_list = {'v_device_type':'hub'}
        response = DB.create_device(p_device_type='hub', p_model='OVI-BOVI', p_hub_id=0,
                                         p_sensor_id=102)
        ids = response.get('v_term_id')
        log.debug('ids: ' + str(ids))
        with pytest.raises(sqlalchemy.exc.InternalError) as excinfo:
            response = DB.create_device(p_device_type='hub', p_model='OVI-BOVI', p_hub_id=0,
                                             p_sensor_id=102)
            log.debug('response: ' + str(response))
            log.debug('excinfo: ' + str(excinfo))

    @allure.testcase('Testcase-3 Test create device, set and check status')
    @allure.story('Create device set and check status')
    def test_create_device_set_and_check_status(self, DB):
        '''

        Create device test

        Send http request to create device, set and check status

        '''

        allure.description('Testing info set status')
        expected_list = {'v_device_type':'hub'}
        response = DB.create_device(p_device_type='hub', p_model='OVI-BOVI', p_hub_id=0,
                                         p_sensor_id=1010)
        ids = response.get('v_term_id')
        DB.set_status(p_term_id=ids, p_status_id = 3)
        expected_list = {'v_status_id': '3'}
        response = DB.get_device(expected_list=expected_list, p_term_id=ids)
