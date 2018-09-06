import allure
import logging

log = logging.getLogger('drs_operations')

class AllureTools():

    @staticmethod
    def set_allure_env(service='Service', **kwargs):
        #log.debug('[set_allure_env] service: ' + str(service))
        #log.debug('[set_allure_env] kwargs: ' + str(kwargs.items()))
        for key, value in kwargs.items():
            allure_key = str(service) + '_' + str(key)
            #kwargs[allure_key] = kwargs.pop(key)
            dict = {}
            dict[allure_key]=value
            #log.debug('[set_allure_env] kwargs: ' + str(kwargs.items()))
            allure.environment(**dict)
            #log.debug('[set_allure_env] dict: ' + str(dict.items()))