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
import random

class auth(object):
    def __init__(self, user, pwd, use):
        self.user = user
        self.pwd = pwd
        self.use = use
