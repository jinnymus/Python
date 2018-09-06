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
import time
from datetime import datetime

log = logging.getLogger('kafka_operations')

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
def KAFKAimage():

    testlib = TestLib.KAFKALib(topic='ALCOHOL2', lang='json', server='10.97.51.43',
                                 schema_registry = config.get('kafka_schema'), server_zoo = '10.97.51.43')
    testlib.service.delete_topic()
    yield testlib


@pytest.fixture(scope="class")
def KAFKAjson():

    testlib = TestLib.KAFKALib(topic=config.get('kafka_topic_raw'), lang='json', server=config.get('kafka_server'),
                                 schema_registry = config.get('kafka_schema'), server_zoo = config.get('kafka_schema'))
    #testlib.service.delete_topic()
    yield testlib

@pytest.fixture(scope="class")
def KAFKAjson2():

    testlib = TestLib.KAFKALib(topic=config.get('kafka_topic_valid'), lang='json', server=config.get('kafka_server'),
                                 schema_registry = config.get('kafka_schema'), server_zoo = config.get('kafka_schema'))
    #testlib.service.delete_topic()
    yield testlib

@allure.feature('Kafka operations')
@allure.feature('validator')
class TestBar:

    @allure.testcase('Testcase-1 Test create topic')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Create topic')
    def test_create_kafka(self):

        allure.description('Testing create topic')
        allure.label('kafka operations')
        log.debug('start test_kafka')

        d1 = nistest.KafkaDriver(topic=config.get('kafka_topic_raw'))
        res_create = d1.create_topic('testtopic2')
        assert res_create == None
        #res_delete = d1.delete_topic()
        #assert res_delete == 0


    @allure.testcase('Testcase-2 Test send raw json to validator topic')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Send raw to validator')
    def test_send_raw_to_validator(self, KAFKAjson, KAFKAjson2):

        allure.description('Testing send raw json to validator topic')
        allure.label('kafka operations')

        d1 = nistest.KafkaDriver(topic=config.get('kafka_topic_raw'), server=config.get('kafka_server'), schema_registry=config.get('kafka_schema'))

        offset1 = d1.get_last_offset()
        rawData = {
              "producer": "test",
              "sessionKey": "123e4567-e89b-12d3-a456-426655440002",
              "termId": 123,
              "protocolId": 1,
              "deviceTypeId": 100,
              "timePlatformFrom1970": 1527601137000,
              "timeDeviceFrom1970": 1527601137000,
              "activityInfo": 1
            }

        rawData = json.dumps(rawData, sort_keys=True).encode('utf-8')
        last_offset = d1.get_last_offset()
        d1.send(msg=rawData, lang='json', schema=None)

        res = d1.read_from_offset(offset1)
        result = d1.read_from_offset(offset=last_offset, lang='json', schema=None)

        log.debug('result: ' + str(result))
        assert rawData == result
        res_delete = d1.delete_topic()
        assert res_delete == 0

    @allure.testcase('Testcase-3 Test send raw json to validator topic')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Send raw to validator new')
    def test_send_raw_to_validator_new(self, KAFKAjson, KAFKAjson2):
        allure.description('Testing send raw json to validator topic')
        allure.label('kafka operations')
        device_time_device = 1530523171000
        device_time_device_utc = datetime.fromtimestamp(int(device_time_device / 1000)).strftime('%Y-%m-%dT%H:%M:%SZ')

        KAFKAjson.send_raw(termId=100, protocolId=200, deviceTypeId=100,
                                     timePlatformFrom1970=device_time_device, timeDeviceFrom1970=device_time_device,
                                     activityInfo=300)

    @allure.testcase('Testcase-4 Test send avro to validator topic')
    #@pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Send avro')
    def test_kafka_send_avro(self, KAFKAjson, KAFKAjson2):

        allure.description('Testing send raw json to validator topic')
        allure.label('kafka operations')

        d2 = nistest.KafkaDriver(topic=config.get('kafka_topic_valid'), server=config.get('kafka_server'), schema_registry=config.get('kafka_schema'))
        res_delete = d2.delete_topic()
        offset2 = d2.get_last_offset()
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
        rawData2 = {"term_id": 100, "time_platform": 1527685363266, "time_device": 1527685363266, "activity_info": 300 }
        expected = json.dumps(rawData2, indent=4, sort_keys=True, default=str)

        last_offset = d2.get_last_offset()
        d2.send(msg=rawData2, lang='avro', schema=schemaSF)

        res = d2.read_from_offset(offset2,'avro',schemaSF)
        result = d2.read_from_offset(offset=offset2, lang='avro', schema=schemaSF)

        log.debug('result: ' + str(result))

        assert expected == result

        res_delete = d2.delete_topic()
        assert res_delete == 0

    @pytest.mark.skip(reason="no way of currently testing this")
    @allure.story('Send image')
    def test_kafka_image(self,KAFKAimage):

        #http://10.97.51.43
        #ALCOHOL

        f = json.loads(open('/nis-test/JSON2.txt').read())
        time.sleep(2)
        KAFKAimage.send(message=f)
        #KAFKAjson.read(no_check=True)

        #bin/kafka_2.12-1.1.0/bin/kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list kafka1:9092 --topic topicimage2 --time -1
        #bin/kafka_2.12-1.1.0/bin/kafka-console-consumer.sh --zookeeper zoo1:2181 --topic topicimage2 --from-beginning