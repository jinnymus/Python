import logging
import os
import sys
import pytest
import allure
import kafka
from kafka import KafkaConsumer, KafkaProducer, KafkaClient, TopicPartition
from kazoo.client import KazooClient
from kazoo.security import make_digest_acl_credential, CREATOR_ALL_ACL
import psycopg2
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

log = logging.getLogger('nistest.basic.DbDriver')

class DbDriver(object):
    def __init__(self, db, user, pwd, server='postgres', port=5432):
        self.server = server
        self.port = port
        self.db = db
        self.user = user
        self.pwd = pwd
        self.conn = psycopg2.connect(dbname=db, user=user, password=pwd, host=server, port=port)
        logging.debug('[DbDriver][select] dbName:' + str(db))
        logging.debug('[DbDriver][select] dbHost:' + str(server))

    def select(self, st):
        log.debug('DB processing')
        cur = self.conn.cursor()
        cur.execute("set search_path=main;")
        res = cur.execute(st)
        rows = cur.fetchall()
        #args = [st]
        #cur.callproc()
        for row in rows:
            logging.debug('row: ' + str(row[0]))
        return rows