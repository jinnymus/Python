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
import sqlalchemy

log = logging.getLogger('testlib')


class DRSLib():

    def __init__(self, **kwargs):
        self.service = nistest.smartFarming.DRS(host=kwargs.get('host'), port=kwargs.get('port'),
                                      authorise=kwargs.get('authorise'))

        nistest.basic.alluredriver.AllureTools.set_allure_env(service='DRS', **kwargs)

    def set_config(self, config):
        self.config = config

    @allure.feature('Create device')
    def create_device(self, deviceType, model, hubId, sensorId, expected={}, no_check=False):

        '''

        Create device function

        Send http request to create info device

       '''

        device = self.service.create_device(no_check=no_check, deviceType=deviceType, model=model, hubId=hubId, sensorId=sensorId)

        if (no_check == False):
            expected = {"termId": 90, "deviceType": deviceType, "model": model,
                                     "sensorId": sensorId, "statusId": 2}

            assert device.response.status_code == 200, 'status_code: ' + str(device.response.status_code) + ' response: ' + str(device.response.text)

            ignore_data = {"termId": 90}
            #assert device.response.json() == expected_response, 'response: ' + str(device.response.text)
            assert nistest.basic.CompareDriver(data_result=device.response.json(), data_expected=expected, lang='json', dump=False, ignore_data=ignore_data)

        return device



    @allure.feature('Change device')
    def change_device(self, device, expected={}, no_check=False, **kwargs):
        '''

        Change device function

        Send http request to change info device

       '''
        for k in kwargs.items():
            logging.debug('[TestLib][changeDevice] kwargs k : ' + str(k))

        device = self.service.change_device(device, **kwargs)
        logging.debug('[TestLib][changeDevice] kwargs: ' + str(kwargs.items()))

        if (no_check == False):
            expected = {"termId": device.get_key_value('termId'), "deviceType": device.get_key_value('deviceType'),
                        "model": device.get_key_value('model'),
                        "sensorId": device.get_key_value('sensorId'), "statusId": kwargs.get('statusId')}

            assert device.response.status_code == 200, 'status_code: ' + str(device.response.status_code) + ' response: ' + str(device.response.text)
            ignore_data = {"termId": 90}
            #assert device.response.json() == expected_response, 'response: ' + str(device.response.text)
            assert nistest.basic.CompareDriver(data_result=device.response.json(), data_expected=expected, lang='json', dump=False, ignore_data=ignore_data)

        return device


    @allure.feature('Create device raw')
    def create_device_raw(self, payload, expected={},no_check=False):

        '''

        Create device from raw function

        Send http request to create info device

       '''

        device = self.service.create_device_raw(payload=payload)
        if (no_check == False):
            assert device.response.status_code == 200, 'response: ' + str(device.response.status_code) + ' response: ' + str(device.response.text)
        #expected_response = { "termId": 90,"deviceType": deviceType, "model": model, "hubId": hubId, "sensorId": sensorId, "statusId": 2 }
        #ignore_data = {"termId": 90}
        #assert device.response.json() == expected_response, 'response: ' + str(device.response.text)
        #assert nistest.basic.CompareDriver(data_result=device.response.json(), data_expected=expected_response, lang='json', dump=False, ignore_data=ignore_data)
        return device

    @allure.feature('Delete device')
    def delete_device(self, device, expected={}, no_check=False):

        '''

        Delete device function

        Send http request to delete info device

       '''

        self.service.delete_device(device)
        if (no_check == False):
            assert device.response.status_code == 204, 'status_code: ' + str(device.response.status_code) + ' response: ' + str(device.response.text)
            assert device.response.text == "", 'response: ' + str(device.response.text)

    @allure.feature('Get device')
    def get_device(self, termId=None, expected={}, no_check=False, **kwargs):

        '''

        Delete device function

        Send http request to delete info device

       '''

        device = self.service.get_device(id=termId)
        if (no_check == False):
            assert device.response.status_code == 200, 'status_code: ' + str(device.response.status_code) + ' response: ' + str(device.response.text)
            expected = {"termId": device.get_key_value('termId'), "deviceType": device.get_key_value('deviceType'),
                        "model": device.get_key_value('model'),
                        "sensorId": device.get_key_value('sensorId'), "statusId": device.get_key_value('statusId')}
            assert nistest.basic.CompareDriver(data_result=device.response.json(), data_expected=expected, lang='json', dump=False)


class HDSLib():

    def __init__(self, **kwargs):
        logging.debug('[TestLib][HDSLib] init')
        self.service = nistest.smartFarming.HDS(host=kwargs.get('host'), port=kwargs.get('port'),
                                      authorise=kwargs.get('authorise'))
        nistest.basic.alluredriver.AllureTools.set_allure_env(service='HDS', **kwargs)
        logging.debug('[TestLib][HDSLib] init end')


    def set_config(self, config):
        self.config = config


    @allure.feature('Get history')
    def get_history(self, expected=None, no_check=False, **kwargs):

        '''

        Get history function

        Send request for get history

       '''
        logging.debug('[TestLib][get_history] kwargs : ' + str(kwargs.items()))
        logging.debug('[TestLib][get_history] expected : ' + str(expected))
        response = self.service.get_history(**kwargs)
        if (no_check == False):
            if (expected is None):
                expected = [{
                    "termId": kwargs.get('termId'),
                    "timeDevice": kwargs.get('timeDevice'),
                    "activityInfo": kwargs.get('activityInfo')
                }]

            assert response.status_code == 200, 'status_code: ' + str(response.status_code) + ' response: ' + str(response.text)
            #assert response.json()[0] == expected, 'response: ' + str(response.json()[0]) + ' expected: ' + str(expected)
            if (response.text == ""):
                assert False, 'response empty'
            assert nistest.basic.CompareDriver(data_result=response.json(), data_expected=expected, lang='json', dump=False)
        return response



class INFOLib():

    def __init__(self, **kwargs):
        self.service = nistest.smartFarming.INFO(host=kwargs.get('host'), port=kwargs.get('port'),
                                      authorise=kwargs.get('authorise'))

        nistest.basic.alluredriver.AllureTools.set_allure_env(service='INFO', **kwargs)

    def set_config(self, config):
        self.config = config


    @allure.feature('Get device')
    def get_device(self, expected={}, no_check=False):

        '''

        Get device

        Send request for get info

       '''
        response = self.service.get_device()
        if (no_check == False):
            assert response.status_code == 200, 'status_code: ' + str(response.status_code) + ' response: ' + str(response.response.text)
            assert response.json()[0] == expected, 'response: ' + str(response.json()) + ' expected: ' + str(expected)
        return response

    @allure.feature('Get model')
    def get_model(self, expected={}, no_check=False):

        '''

        Get model device

        Send request for get model

       '''
        response = self.service.get_model()
        if (no_check == False):
            assert response.status_code == 200, 'status_code: ' + str(response.status_code) + ' response: ' + str(response.response.text)
            assert response.json()[0] == expected, 'response: ' + str(response.json()) + ' expected: ' + str(expected)
        return response

    @allure.feature('Get protocol')
    def get_protocol(self, expected={}, no_check=False):

        '''

        Get protocol device

        Send request for get protocol

       '''
        response = self.service.get_protocol()
        if (no_check == False):
            assert response.status_code == 200, 'status_code: ' + str(response.status_code) + ' response: ' + str(response.response.text)
            assert response.json()[0] == expected, 'response: ' + str(response.json()) + ' expected: ' + str(expected)
        return response


class DBLib():

    def __init__(self, **kwargs):
        self.service = nistest.smartFarming.DB(db_host=kwargs.get('db_host'), db_port=kwargs.get('db_port'),
                                     db_user=kwargs.get('db_user'), db_pwd=kwargs.get('db_pwd'),
                                     db_database=kwargs.get('db_database'))
        nistest.basic.alluredriver.AllureTools.set_allure_env(service='DB', **kwargs)
        #self.service.truncate(kwargs.get('db_table'))


    def set_config(self, config):
        self.config = config

    @allure.feature('create device')
    def create_device(self, expected={}, no_check=False, **kwargs):
        '''

        Create device function

        Send psql request to create device

        '''
        try:
            response = self.service.create_device(**kwargs)
            log.debug('[create_device] no_check: ' + str(no_check))
            log.debug('[create_device] response: ' + str(response))
            for row in response:
                log.debug('[create_device] response row: ' + str(row))
                row_as_dict = dict(row)
                log.debug('[create_device] response row_as_dict: ' + str(row_as_dict))
            if (no_check == False):
                expected = {'v_device_type': 'hub'}
                for key, assert_value in expected.items():
                    log.debug('[create_device] expected_list->key: ' + str(key))
                    log.debug('[create_device] expected_list->assert_value: ' + str(expected[key]))
                    log.debug('[create_device] row_as_dict[key]: ' + str(row_as_dict[key]))
                    assert row_as_dict[key] == expected[key], 'assert_value: ' + str(assert_value)
            return row_as_dict
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise

    @allure.feature('get device')
    def get_device(self, expected={}, no_check=False, **kwargs ):
        '''

        Get device function

        Send psql request to get device

        '''
        response = self.service.get_device(**kwargs)
        for row in response:
            log.debug('[get_device] response row: ' + str(row))
            row_as_dict = dict(row)
        if (no_check == False):
            for key, assert_value in expected.items():
                log.debug('[create_device] expected_list->key: ' + str(key))
                log.debug('[create_device] expected_list->assert_value: ' + str(expected[key]))
                log.debug('[create_device] row_as_dict[key]: ' + str(row_as_dict[key]))
                assert str(row_as_dict[key]) == str(expected[key]), 'response[key]: "' + str(row_as_dict[key]) + '" expected[key]: "' + str(expected[key]) + '"'
        return row_as_dict

    @allure.feature('get history')
    def get_history(self, expected={}, no_check=False, **kwargs ):
        '''

        Get history

        Send psql request to get history

        '''
        row_as_dict = {}
        response = self.service.get_history(in_tem_id=kwargs.get('in_term_id'),in_time_start=kwargs.get('in_time_start'),in_time_end=kwargs.get('in_time_end'))
        for row in response:
            log.debug('[get_history] response row: ' + str(row))
            row_as_dict = dict(row)
            log.debug('[get_history] response row_as_dict: ' + str(row_as_dict))
        #expected = (kwargs.get('term'), datetime.datetime(2018, 7, 2, 9, 19, 31), datetime.datetime(2018, 7, 2, 9, 19, 31), 1)
        if (no_check == False):
            for key, assert_value in expected.items():
                log.debug('[create_device] expected_list->key: ' + str(key))
                log.debug('[create_device] expected_list->assert_value: ' + str(expected[key]))
                log.debug('[create_device] row_as_dict[key]: ' + str(row_as_dict[key]))
                assert str(row_as_dict[key]) == str(expected[key]), 'response[key]: "' + str(row_as_dict[key]) + '" expected[key]: "' + str(expected[key]) + '"'
        return row_as_dict

    @allure.feature('set status')
    def set_status(self, expected={}, no_check=False, **kwargs ):
        '''

        Create device function

        Send psql request to set status device

        '''
        response = self.service.set_status(**kwargs)
        log.debug('[set_status] response: ' + str(response))
        for row in response:
            log.debug('[set_status] response row: ' + str(row))
            row_as_dict = dict(row)
            log.debug('[set_status] response row_as_dict: ' + str(row_as_dict))
        if (no_check == False):
            expected = {'v_status_id' : kwargs.get('p_status_id') }
            for key, assert_value in expected.items():
                log.debug('[set_status] expected_list->key: ' + str(key))
                log.debug('[set_status] expected_list->assert_value: ' + str(expected[key]))
                log.debug('[set_status] row_as_dict[key]: ' + str(row_as_dict[key]))
                assert str(row_as_dict[key]) == str(expected[key]), 'response[key]: "' + str(row_as_dict[key]) + '" expected[key]: "' + str(expected[key]) + '"'
        return row_as_dict

    @allure.feature('get dict device')
    def get_dict_device(self, expected={}, no_check=False):
        '''

        Create device function

        Send psql request to get dict device

        '''
        response = self.service.get_dict_device()
        log.debug('[set_status] response: ' + str(response))
        for row in response:
            log.debug('[set_status] response row: ' + str(row))
            row_as_dict = dict(row)
        if (no_check == False):
            for key, assert_value in expected.items():
                log.debug('[create_device] expected_list->key: ' + str(key))
                log.debug('[create_device] expected_list->assert_value: ' + str(expected[key]))
                log.debug('[create_device] row_as_dict[key]: ' + str(row_as_dict[key]))
                assert str(row_as_dict[key]) == str(expected[key]), 'response[key]: "' + str(row_as_dict[key]) + '" expected[key]: "' + str(expected[key]) + '"'
        return row_as_dict

    @allure.feature('get dict protocol')
    def get_dict_protocol(self, expected={}, no_check=False):
        '''

        Create device function

        Send psql request to get dict protocol

        '''
        response = self.service.get_dict_protocol()
        log.debug('[set_status] response: ' + str(response))
        for row in response:
            log.debug('[set_status] response row: ' + str(row))
            row_as_dict = dict(row)
        if (no_check == False):
            for key, assert_value in expected.items():
                log.debug('[create_device] expected_list->key: ' + str(key))
                log.debug('[create_device] expected_list->assert_value: ' + str(expected[key]))
                log.debug('[create_device] row_as_dict[key]: ' + str(row_as_dict[key]))
                assert str(row_as_dict[key]) == str(expected[key]), 'response[key]: "' + str(row_as_dict[key]) + '" expected[key]: "' + str(expected[key]) + '"'
        return row_as_dict

    @allure.feature('get dict device type')
    def get_dict_device_type(self, expected={}, no_check=False):
        '''

        Create device function

        Send psql request to get dict device type

        '''
        response = self.service.get_dict_device_type()
        log.debug('[set_status] response: ' + str(response))
        for row in response:
            log.debug('[set_status] response row: ' + str(row))
            row_as_dict = dict(row)
        if (no_check == False):
            for key, assert_value in expected.items():
                log.debug('[create_device] expected_list->key: ' + str(key))
                log.debug('[create_device] expected_list->assert_value: ' + str(expected[key]))
                log.debug('[create_device] row_as_dict[key]: ' + str(row_as_dict[key]))
                assert str(row_as_dict[key]) == str(expected[key]), 'response[key]: "' + str(row_as_dict[key]) + '" expected[key]: "' + str(expected[key]) + '"'
        return row_as_dict

class KAFKALib():

    def __init__(self, **kwargs):
        self.service = nistest.smartFarming.KAFKA(topic=kwargs.get('topic'), lang=kwargs.get('lang'),
                                    server=kwargs.get('server'),
                                    schema_registry=kwargs.get('schema_registry'), server_zoo=kwargs.get('server_zoo'))

        nistest.basic.alluredriver.AllureTools.set_allure_env(service='KAFKA', **kwargs)

    def set_config(self, config):
        self.config = config

    @allure.feature('read')
    def read(self, expected={}, no_check=False, ignore=None):
        '''

        Read from kafka

        '''

        response = None
        log.debug('[read] self.service.lang: ' + str(self.service.lang))
        log.debug('[read] expected: ' + str(expected))

        if (self.service.lang == 'json'):
            expected = json.dumps(expected, sort_keys=True).encode('utf-8')
            log.debug('[read] expected: ' + str(expected))
            response = self.service.read()
        elif (self.service.lang == 'avro'):
            expected = json.dumps(expected, indent=4, sort_keys=True, default=str)
            log.debug('[read] expected: ' + str(expected))
            response = self.service.read()

        #log.debug('[read] response: ' + str(response))
        #response = json.dumps(response, indent=4, sort_keys=True, default=str)
        if (no_check == False):
            response = json.loads(response)
            expected = json.loads(expected)
            log.debug('[read] response: ' + str(response))
            log.debug('[read] expected: ' + str(expected))
            #assert response == expected, 'response: ' + str(response) + ' expected: ' + str(expected)
            assert nistest.basic.CompareDriver(data_result=response, data_expected=expected, lang='json', dump=False, ignore_data=ignore)
        return response

    @allure.feature('send')
    def send(self, message, expected=None, no_check=False):
        '''

        Send to kafka

        '''
        #if (self.service.lang == 'json'):
        #    message = json.dumps(message, sort_keys=True).encode('utf-8')<
        response = self.service.send(data=message)
        if (expected is not None) or (no_check == False):
            assert response == expected, 'response: ' + str(response) + ' expected: ' + str(expected)

    @allure.feature('send raw')
    def send_raw(self, **kwargs):
        rawData = {
              "producer": "test",
              "sessionKey": "123e4567-e89b-12d3-a456-426655440002",
              "termId": kwargs.get('termId'),
              "protocolId": kwargs.get('protocolId'),
              "deviceTypeId": kwargs.get('deviceTypeId'),
              "timePlatformFrom1970": kwargs.get('timePlatformFrom1970'),
              "timeDeviceFrom1970": kwargs.get('timeDeviceFrom1970'),
              "activityInfo": kwargs.get('activityInfo')
            }
        self.send(message=rawData, expected=None)

    @allure.feature('send valid')
    def send_valid(self, **kwargs):
        validData =  {"term_id": kwargs.get('termId'), "time_platform": kwargs.get('time_platform'), "time_device": kwargs.get('time_device'), "activity_info": kwargs.get('activity_info') }
        self.send(message=validData, expected=None)

    @allure.feature('read raw')
    def read_raw(self, **kwargs):
        expected = {
              "producer": "test",
              "sessionKey": "123e4567-e89b-12d3-a456-426655440002",
              "termId": kwargs.get('termId'),
              "protocolId": kwargs.get('protocolId'),
              "deviceTypeId": kwargs.get('deviceTypeId'),
              "timePlatformFrom1970": kwargs.get('timePlatformFrom1970'),
              "timeDeviceFrom1970": kwargs.get('timeDeviceFrom1970'),
              "activityInfo": kwargs.get('activityInfo')
            }
        self.read(expected=expected)

    @allure.feature('read valid')
    def read_valid(self, **kwargs):
        expected = {"term_id": kwargs.get('term_id'), "time_platform": kwargs.get('time_platform'), "time_device": kwargs.get('time_device'), "activity_info": kwargs.get('activity_info') }
        self.read(expected=expected)

    @allure.feature('read changed')
    def read_changed(self, **kwargs):
        ignore = {
                   "protocolId": "test",
                   "sessionKey": "7eb1b7f4-7f73-11e8-91f3-0242ac130003"
                  }
        expected = {
                       "deviceType": kwargs.get('deviceType'),
                       "producer": "drs",
                       "protocolId": "test",
                       "sessionKey": "7eb1b7f4-7f73-11e8-91f3-0242ac130003",
                       "statusId": 2,
                       "termId": kwargs.get('term_id'),
                       "uid": kwargs.get('uid'),
                   }

        self.read(expected=expected, ignore=ignore)