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

log = logging.getLogger('nistest.basic.WebDriver')

class WebDriver(object):

    '''

    Web driver class

    Send http request and get response

    '''

    proxies = {
        "http": None,
        "https": None,
    }


    def __init__(self, host, port, authorise, methods, content, paths):
        self.host = host
        self.port = port
        self.authorise = authorise
        self.methods = methods
        self.content = content
        self.paths = paths

    def request(self, path, method, payload=""):
        return self.__request(path, method, self.content, 'nistest', payload, self.authorise.user, self.authorise.pwd, self.authorise.use)

    def __request(self, uri, method, ContentType, XSender, postdata, user, pwd, auth):

        '''

        Send http request

        Send request

        '''

        logging.debug('[WebDriver][request] start')
        logging.debug('[WebDriver][request] uri: ' + str(uri))
        logging.debug('[WebDriver][request] auth: ' + str(auth))
        logging.debug('[WebDriver][request] method: ' + str(method))
        proxies = {
            "http": None,
            "https": None,
        }
        uri = "http://" + str(self.host) + ":" + str(self.port) + str(uri)
        usrPass = user + ":" + pwd
        b64Val = base64.b64encode(bytes(usrPass, 'utf-8')).decode("utf-8")
        headers = {}
        if (auth == True):
            headers['Authorization'] = "Basic %s" % str(b64Val)
        headers['Content-Type'] = ContentType
        headers['X-Sender'] = XSender

        logging.debug('[WebDriver][request] headers: ' + str(headers))
        logging.debug('[WebDriver][request] postdata: ' + str(postdata))
        jpretty = json.dumps(postdata, ensure_ascii=False)
        logging.debug('[WebDriver][request] json: ' + str(jpretty))
        request = getattr(requests, method.lower())
        #response = request(uri, headers=headers, data=jpretty)
        if (method == "POST"):
            response = request(uri, headers=headers, data=jpretty)
        if (method == "GET"):
            response = requests.get(uri, headers=headers)
        if (method == "DELETE"):
            response = requests.delete(uri, headers=headers)
        if (method == "PATCH"):
            response = requests.patch(uri, headers=headers, data=jpretty)
        #response_json = response.json()
        status_code = response.status_code
        headers = response.headers
        logging.debug('[WebDriver][request] response: ' + str(response))
        logging.debug('[WebDriver][request] response.text: ' + str(response.text))
        logging.debug('[WebDriver][request] status_code: ' + str(status_code))
        logging.debug('[WebDriver][request] header: ' + str(headers))
        logging.debug('[WebDriver][request] Content-Type: ' + str(headers.get('content-type')))
        return response
