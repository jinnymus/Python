import logging
import os
import sys
import pytest
import allure
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
import io
import collections
import struct
#from bson import json_util
import datetime
import time
import calendar
from hamcrest import *
import random

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
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


    def __init__(self, schema, host, port, authorise, content):
        self.schema = schema
        self.host = host
        self.port = port
        self.authorise = authorise
        self.content = content

    def request(self, path, method, payload=None, params=None):
        return self.__request(uri=path, method=method, ContentType=self.content, XSender='tests', postdata=payload, auth=self.authorise, params=None)

    def __request(self, uri='/', method='POST', ContentType=None, XSender=None, postdata=None, auth=None, params=None):

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
        uri = str(self.schema) + "://" + str(self.host) + ":" + str(self.port) + str(uri)
        #uri = str(schema) + "://" + str(self.host) + str(uri)
        #usrPass = user + ":" + pwd
        #b64Val = base64.b64encode(bytes(usrPass, 'utf-8')).decode("utf-8")
        headers = {}
        if (auth.use == True):
            headers['Authorization'] = "Token %s" % str(auth.token)
        headers['Content-Type'] = ContentType
        headers['X-Sender'] = XSender

        logging.debug('[WebDriver][request] headers: ' + str(headers))
        logging.debug('[WebDriver][request] postdata: ' + str(postdata))
        #jpretty = json.dumps(postdata, ensure_ascii=False)
        #logging.debug('[WebDriver][request] json: ' + str(jpretty))
        request = getattr(requests, method.lower())
        #response = request(uri, headers=headers, data=jpretty)
        if (method == "POST"):
            response = request(uri, data=postdata, headers=headers)
        if (method == "GET"):
            response = requests.get(uri, headers=headers, params=params)
        if (method == "DELETE"):
            response = requests.delete(uri, headers=headers)
        if (method == "PATCH"):
            response = requests.patch(uri, headers=headers, data=postdata)
        #response_json = response.json()
        status_code = response.status_code
        headers = response.headers
        #logging.debug('[WebDriver][request] response: ' + str(response))
        #logging.debug('[WebDriver][request] response.text: ' + str(response.text))
        logging.debug('[WebDriver][request] status_code: ' + str(status_code))
        logging.debug('[WebDriver][request] header: ' + str(headers))
        logging.debug('[WebDriver][request] Content-Type: ' + str(headers.get('content-type')))
        return response
