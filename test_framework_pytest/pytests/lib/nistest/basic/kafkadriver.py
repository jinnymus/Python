import logging
import os
import sys
import pytest
import allure
import kafka
from kafka import KafkaConsumer, KafkaProducer, KafkaClient, TopicPartition
from kazoo.client import KazooClient
from kazoo.security import make_digest_acl_credential, CREATOR_ALL_ACL
#import zc.zk
import lxml.etree
import requests, base64
import pprint
import json
import xmldiff
from xml_diff import compare
from jsondiff import diff
import re
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.base_matcher import BaseMatcher
import base64
import avro as avro2
import io
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka import Producer, Consumer
from confluent_kafka.avro.error import ClientError
from confluent_kafka.avro.load import load, loads  # noqa
from confluent_kafka.avro.cached_schema_registry_client import CachedSchemaRegistryClient
from confluent_kafka.avro.serializer import (SerializerError,  # noqa
                                             KeySerializerError,
                                             ValueSerializerError)
from confluent_kafka.avro.serializer.message_serializer import MessageSerializer
import collections
from fastavro import schemaless_reader
import struct
#from bson import json_util
import datetime
import time
import calendar
from hamcrest import *
import nistest
import random

log = logging.getLogger('nistest.basic.KafkaDriver')

class KafkaDriver(object):

    '''

    Kafka driver class

    Can send json and avro mesages

    '''

    last_offset = 0

    def __init__(self, topic, server='kafka1', schema_registry = 'kafka-schema-registry'):
        self.server = server
        self.topic = topic
        self.schema_registry = schema_registry
        schema_registryObj = CachedSchemaRegistryClient(url='http://' + self.schema_registry + ':8081')
        self.serializer = MessageSerializer(schema_registryObj)

    def create_topic(self, topic):

        '''

        Create topic

        '''

        client = kafka.KafkaClient(hosts=self.server + ':9092')
        res = client.ensure_topic_exists(topic)
        return res

    def delete_topic(self, topic=None, server='zoo1'):

        '''

        Delete topic

        '''
        if (topic is None):
            topic = self.topic
        cmd = '/nis-test/bin/kafka_2.12-1.1.0/bin/kafka-topics.sh --delete --topic ' + topic + ' --zookeeper ' + server
        logging.debug('[KafkaDriver][delete_topic] cmd: ' + str(cmd))
        ret = os.system(cmd)
        logging.debug('[KafkaDriver][delete_topic] ret: ' + str(ret))
        #assert ret == 0
        return ret

    @pytest.allure.step('kafka_list')
    def list(self):

        '''

        Kafka list topics

        List exist topics

        '''

        consumer = KafkaConsumer(bootstrap_servers=self.server + ':9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        log.debug("[KafkaDriver][list] list start")
        list = consumer.topics()
        for topic in list:
           log.debug("[KafkaDriver][list] topic: " + str(topic))
        log.debug("[KafkaDriver][list] self.topic: " + str(self.topic))
        assert self.topic in list
    #
    # Kafka get last offset of topic
    #
    @pytest.allure.step('get_last_offset')
    def get_last_offset(self):

        '''

        Kafka get last offset

        Get last message offset

        '''

        log.debug("[KafkaDriver][get_last_offset] start")
        # consumer = KafkaConsumer(bootstrap_servers=self.server + ':9092',
        #                          group_id = None,
        #                          enable_auto_commit = False)
        consumer = KafkaConsumer(bootstrap_servers=self.server + ':9092',
                                 consumer_timeout_ms=1000)
        log.debug("[KafkaDriver][get_last_offset] TopicPartition")
        tp = TopicPartition(self.topic, 0)
        log.debug("[KafkaDriver][get_last_offset] assign")
        consumer.assign([tp])
        log.debug("[KafkaDriver][get_last_offset] seek_to_end")
        consumer.seek_to_end(tp)
        log.debug("[KafkaDriver][get_last_offset] position")
        last_offset = consumer.position(tp)
        log.debug("[KafkaDriver][get_last_offset] topic: " + str(self.topic))
        log.debug("[KafkaDriver][get_last_offset] last_offset: " + str(last_offset))
        #consumer.close(autocommit=False)
        consumer.close()
        return last_offset


    @pytest.allure.step('read_from_offset')
    def read_from_offset(self, offset=0, lang='json', schema=None):

        '''

        Kafka read message

        Read json and avro messages from consumer

        '''
        log.debug("[KafkaDriver][read_from_offset] lang: " + str(lang))
        log.debug("[KafkaDriver][read_from_offset] offset: " + str(offset))

        def outputJSON(obj):

            '''

            Default JSON serializer.

            '''

            if isinstance(obj, datetime.datetime):
                return int(obj.strftime("%s%f")[:-3])
            return obj


        ret = None
        log.debug("[KafkaDriver][read_from_offset] read start: " + str(self.server))
        consumer = KafkaConsumer(bootstrap_servers=self.server + ':9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)

        partition = TopicPartition(self.topic, 0)
        consumer.assign([partition])
        consumer.seek_to_end(partition)
        start = int(offset)
        consumer.seek(partition, offset)

        for msg in consumer:
            if (lang == 'avro'):
                #message = AvroDecoder.decode(schema, msg.value)
                schema_registry = CachedSchemaRegistryClient(url='http://' + self.schema_registry + ':8081')
                self._serializer = MessageSerializer(schema_registry)
                message = self._serializer.decode_message(msg.value)
                message = json.dumps(message, indent=4, sort_keys=True, default=outputJSON)
                #log.debug("[KafkaDriver][read_from_offset] avro message: " + str(message))
                ret = message
            else:
                message = msg.value
                #log.debug("[KafkaDriver][read_from_offset] other message: " + str(message))
                ret = msg.value
            log.debug("[KafkaDriver][read_from_offset] msg: " + str(message) + " msg.offset: " + str(msg.offset))
        consumer.close()
        log.debug("[KafkaDriver][read_from_offset] read end")
        return ret

    @pytest.allure.step('kafka_producer')
    def send(self, topic=None, msg="{'foo':'bar'}", lang='json', schema=None):

        '''

        Kafka send message

        Send json and avro messages

        '''


        log.debug("[KafkaDriver][send] producer start: " + str(self.server))
        log.debug("[KafkaDriver][send] send message: " + str(msg))
        if (topic is None):
            topic = self.topic
        log.debug("[KafkaDriver][send] topic: " + str(topic))
        if (lang == 'json'):
            producer = KafkaProducer(bootstrap_servers=self.server + ':9092')
            log.debug("[KafkaDriver][send] json msg")
            res = producer.send(self.topic, key=None, value=msg)
            log.debug("[KafkaDriver][send] produce result: " + str(res.get()))
            time.sleep(1)
            producer.close
            log.debug("[KafkaDriver][send] end")
        elif (lang == 'avro'):
            log.debug("[KafkaDriver][send] avro msg")
            log.debug("[KafkaDriver][send] schema: " + str(schema))
            value_schema = avro.loads(schema)
            avroProducer = AvroProducer({
                 'bootstrap.servers': self.server,
                 'schema.registry.url': 'http://' + self.schema_registry + ':8081'
                 }, default_value_schema=value_schema)

            res = avroProducer.produce(topic=self.topic, value=msg)
            log.debug("[KafkaDriver][send] produce result: " + str(res))
            time.sleep(1)
            avroProducer.flush()
            log.debug("[KafkaDriver][send] end")
