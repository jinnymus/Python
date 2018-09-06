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
import TestLib
import random
from datetime import datetime

kafka_topic1 = 'ru.nis.idg.terminal.rawData.smartFarm'
kafka_topic2 = 'ru.nis.idg.terminal.validData.smartFarm'
db_host = 'sql'
db_port = 5433
db_database = 'sodmtd'
db_user = 'postgres'
db_pwd = 'pg123QWEasd'

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


log = logging.getLogger('validator_operations')

@pytest.fixture(scope="function")
def ServiceObjKAFKAavro():
    testlib = TestLib.KAFKALib(topic=config.get('kafka_topic_valid'), lang='avro', server=config.get('kafka_server'),
                                 schema_registry = config.get('kafka_schema'), server_zoo = config.get('kafka_schema'))
    testlib.service.delete_topic()
    yield testlib

@allure.feature('Validator operation feature')
@allure.feature('validator')
class TestBar:

    @allure.testcase('Testcase-1 Test Kafka')
    @pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Validator processing message')
    def test_validator_processing_message(self):
        allure.description('Testing validator processing message')
        allure.label('validator operations')

        d1 = nistest.KafkaDriver(topic=config.get('kafka_topic_raw'), server=config.get('kafka_server'), schema_registry=config.get('kafka_schema'))
        d2 = nistest.KafkaDriver(topic=config.get('kafka_topic_valid'), server=config.get('kafka_server'), schema_registry=config.get('kafka_schema'))


        res1_delete = d2.delete_topic()
        #assert res1_delete == 0
        res2_delete = d1.delete_topic()
        #assert res2_delete == 0

        offset1 = d1.get_last_offset()
        offset2 = d2.get_last_offset()
        rawData = {
              "producer": "test",
              "sessionKey": "123e4567-e89b-12d3-a456-426655440002",
              "termId": 123,
              "protocolId": 1,
              "deviceTypeId": 100,
              "timePlatformFrom1970": 1527601137000,
              "timeDeviceFrom1970": 1527601137001,
              "activityInfo": 1
            }

        schemaSF = '''{
              "type":"record",
              "name":"Farming",
              "namespace":"nis.dev.validator.avro",
              "fields":[
                {
                  "name": "term_id",
                  "type": "long"
                },
                {
                  "name": "time_platform",
                  "type": {
                    "type": "long",
                    "logicalType": "timestamp-millis"
                  }
                },
                {
                  "name": "time_device",
                  "type": {
                    "type": "long",
                    "logicalType": "timestamp-millis"
                  }
                },
                {
                  "name": "activity_info",
                  "type": "int"
                }
              ]
            }'''

        rawData = json.dumps(rawData, sort_keys=True).encode('utf-8')
        d1.send(msg=rawData, lang='json', schema=None)

        rawData2 = {"term_id": 123, "time_platform": 1527601137000, "time_device": 1527601137001, "activity_info": 1 }
        rawDataJson2 = json.dumps(rawData2, indent=4, sort_keys=True, default=str)

        log.debug('offset1: ' + str(offset1))
        log.debug('offset2: ' + str(offset2))
        res1 = d1.read_from_offset(offset1)
        res2 = d2.read_from_offset(offset2,'avro',schemaSF)
        #res2 = json.dumps(res2, sort_keys=True)
        log.debug('result1 json: ' + str(res1))
        log.debug('result2 avro: ' + str(res2))

        assert rawData == res1
        assert rawDataJson2 == res2

        #res1_delete = d2.delete_topic()
        #assert res1_delete == 0
        #res2_delete = d1.delete_topic()
        #assert res2_delete == 0

    @allure.testcase('Testcase-2 Test Kafka')
    # @pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Validator processing message new')
    def test_validator_processing_message_new(self, ServiceObjKAFKAavro):
        allure.description('Testing validator processing message new')
        allure.label('validator operations')

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

        for time in range(2):

            device_activity_info = random.randint(1, 100000)
            device_time_device = 1530523171000 + 1000 * time
            device_time_device_utc = datetime.fromtimestamp(int(device_time_device / 1000)).strftime(
                '%Y-%m-%dT%H:%M:%SZ')

            ServiceObjKAFKAavro.send_valid(termId=device_v_term_id, time_platform=device_time_device, time_device=device_time_device,
                                       activity_info=device_activity_info)
