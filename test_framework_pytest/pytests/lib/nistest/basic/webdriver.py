import logging
import os
import sys
import pytest
import allure
import lxml.etree
import requests, base64
import pprint
import json
import xmldiff
from xml_diff import compare
from jsondiff import diff
import re
import base64
import io
import collections
import struct
#from bson import json_util
import datetime
import time
import calendar
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


    def __init__(self, host, port, authorise, methods, paths):
        self.host = host
        self.port = port
        self.authorise = authorise
        self.methods = methods
        self.paths = paths

    def request(self, path, content_type, method, payload="", headers=None):
        log.debug('[WebDriver][request] request start')
        return self.__request(uri=path, method=method, content_type=content_type, x_sender='nistest', postdata=payload, user=self.authorise.user, pwd=self.authorise.pwd, auth=self.authorise.use, headers=headers)

    def __request(self, uri, method, content_type, x_sender, postdata, user, pwd, auth, headers):

        '''

        Send http request

        Send request

        '''

        log.debug('[WebDriver][__request] start')
        log.debug('[WebDriver][__request] host: ' + str(self.host))
        log.debug('[WebDriver][__request] port: ' + str(self.port))
        log.debug('[WebDriver][__request] uri: ' + str(uri))
        log.debug('[WebDriver][__request] auth: ' + str(auth))
        log.debug('[WebDriver][__request] method: ' + str(method))
        proxies = {
            "http": None,
            "https": None,
        }
        uri = "http://" + str(self.host) + ":" + str(self.port) + str(uri)
        usrPass = user + ":" + pwd
        b64Val = base64.b64encode(bytes(usrPass, 'utf-8')).decode("utf-8")
        if (headers is None):
            headers = {}
            if (auth == True):
                headers['Authorization'] = "Basic %s" % str(b64Val)
            headers['Content-Type'] = content_type
            headers['X-Sender'] = x_sender

        log.debug('[WebDriver][__request] headers: ' + str(headers))
        log.debug('[WebDriver][__request] postdata: ' + str(postdata))
        jpretty = json.dumps(postdata, ensure_ascii=False)
        log.debug('[WebDriver][__request] json: ' + str(jpretty))
        request = getattr(requests, method.lower())
        #response = request(uri, headers=headers, data=jpretty)
        response = None
        if (method == "POST"):
            response = requests.post(uri, headers=headers, data=jpretty, timeout=10)
        if (method == "GET"):
            response = requests.get(uri, headers=headers, timeout=10)
        if (method == "DELETE"):
            response = requests.delete(uri, headers=headers, timeout=10)
        if (method == "PATCH"):
            response = requests.patch(uri, headers=headers, data=jpretty, timeout=10)
        #response_json = response.json()
        status_code = response.status_code
        headers = response.headers
        log.debug('[WebDriver][request] response: ' + str(response))
        log.debug('[WebDriver][request] response.text: ' + str(response.text))
        log.debug('[WebDriver][request] status_code: ' + str(status_code))
        log.debug('[WebDriver][request] header: ' + str(headers))
        log.debug('[WebDriver][request] Content-Type: ' + str(headers.get('content-type')))
        return response
