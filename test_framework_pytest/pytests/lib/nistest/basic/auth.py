import nistest
#from nistest.basic.alluredriver import AllureTools
import logging
import inspect
import base64

from nistest.basic.alluredriver import AllureTools

log = logging.getLogger('drs_operations')

class auth(object):
    def __init__(self, **kwargs):
        self.user = kwargs.get('user')
        self.pwd = kwargs.get('pwd')
        self.use = kwargs.get('use')
        service = inspect.stack()[1][3]
        log.debug('[auth] service: ' + str(service))
        for key, value in kwargs.items():
            log.debug('[auth] key: ' + str(key) + ' value: ' + str(value))
        #    dict = {}
        #    dict[key] = value
        #a = AllureTools()
        AllureTools.set_allure_env(service=service, **kwargs)
            #nistest.basic.alluredriver.set_allure_env(service='DRS', pwd=pwd)
            #nistest.basic.alluredriver.set_allure_env(service='DRS', use_authr=use)

    def get_basic_auth(self):
        usrPass = str(self.user) + ":" + str(self.pwd)
        b64Val = base64.b64encode(bytes(usrPass, 'utf-8')).decode("utf-8")
        headers = {}
        return "Basic %s" % str(b64Val)

    def set(self, key, value):
        setattr(self, key, value)