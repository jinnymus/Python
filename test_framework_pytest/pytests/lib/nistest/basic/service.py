import logging
from nistest.basic.auth import auth
from nistest.basic.webdriver import WebDriver
from nistest.basic.kafkadriver import KafkaDriver
import re
from datetime import datetime
import pytest
import allure

log = logging.getLogger('nistest.basic.Service')

class Service(object):

    #auth = auth(user='test', pwd='12345678', use=False)

    def __init__(self, host='localhost', port='8080',
                 driverClass='WebDriver',
                 authorise=auth):

        log.debug('[Service][init] start')
        self.service_host = host
        self.service_port = port
        self.driverClass = driverClass
        self.authorise = authorise
        self.paths = {'create_device': '/create_device', 'delete_device': '/delete_device', 'change_device': '/change_device','get_device': '/get_device'}
        self.methods = {'create_device': 'POST', 'delete_device': 'DELETE', 'change_device': 'PATCH', 'get_device': 'GET'}
        self.driver = globals()[driverClass](host=self.service_host, port=self.service_port, authorise=self.authorise, methods=self.methods, paths=self.paths)

    @pytest.allure.step('Request')
    def request(self, device=None, method=None, payload=None, path=None, headers=None):
        log.debug('[request] method: ' + str(method) + ' payload: ' + str(payload) + ' path: ' + str(path) + ' content-type: ' + str(self.content))
        if (path is None):
           path = self.paths.get(method)
        response = self.driver.request(path=path, content_type=self.content, method=self.methods.get(method), payload=payload, headers=headers)
        if (device is not None):
            device.set_response(response)
        headers_expected = self.headers_expected
        log.debug('[request] method: ' + str(method))
        log.debug('[request] response: ' + str(response.text))
        self.check_headers(response=response, headers_expected=headers_expected, method=method)
        return response

    @pytest.allure.step('Check headers')
    def check_headers(self, response=None, headers_expected=None, method=None):
        if (self.methods.get(method) == 'DELETE'):
            del headers_expected['Content-Type']
            del headers_expected['Content-Length']
            log.debug('[request] delete content-type')
        log.debug('[check_headers] headers_expected: ' + str(headers_expected))
        log.debug('[check_headers] headers: ' + str(response.headers))
        for key, regexp in headers_expected.items():
            log.debug('[check_headers] key: ' + str(key))
            log.debug('[check_headers] regexp: ' + str(regexp))
            value = response.headers.get(key)
            if (key == 'Date'):
                # 'Date': 'Thu, 08 Feb 2018 13:56:48 GMT',
                try:
                    dt = datetime.strptime(str(value), "%a, %d %b %Y %H:%M:%S GMT")
                    #log.debug('[request] dt: ' + str(dt))
                except ValueError as e:
                    assert False, e
                    log.debug('[check_headers] e: ' + str(e))
                log.debug('[check_headers] =============================')
            else:
                log.debug('[check_headers] value from response: ' + str(value))
                pattern_regexp = re.compile(r'.*' + regexp + '.*')
                if (value == None):
                    log.debug('[check_headers] value is None')
                    assert False, 'Header: ' + str(key) + ' is None, response header: ' + str(value) + ' expected regexp: ' + str(regexp)
                else:
                    res = re.match(regexp, value)
                if (res):
                    log.debug('[check_headers] found')
                    log.debug('[check_headers] res: ' + str(res.groups()))
                    if (key == 'X-Server-Info'):
                        server = res.group(1)
                        version = res.group(2)
                        host = res.group(3)
                        log.debug('[check_headers][X-Server-Info] server: ' + str(server))
                        log.debug('[check_headers][X-Server-Info] version: ' + str(version))
                        log.debug('[check_headers][X-Server-Info] host: ' + str(host))
                    else:
                        log.debug('[check_headers] value: ' + str(value))
                        log.debug('[check_headers] search: ' + str(res.group(0)))
                        assert value == res.group(0)
                else:
                    log.debug('[check_headers] not found')
                    assert False, 'response header: ' + str(value) + ' expected regexp: ' + str(regexp)
                log.debug('[check_headers] =============================')