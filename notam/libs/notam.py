import pytest
import allure
import selenium
from selenium.webdriver.common.keys import Keys
import logging
from selenium.common.exceptions import TimeoutException
import sys
import itertools
from selenium import webdriver
from libs.webdriver import WebDriver
from libs.auth import auth
from django.conf import settings
from unittest import TestCase
from django.conf import settings
import json

config = {
            'host': 'notamdev.qantor.ru',
            'schema' : 'https',
            'port' : 443
          }

auth = auth('admin','admin', False)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

settings.configure()
logger = logging.getLogger(__name__)


def auth_key():
    uri = '/api/auth/login/'
    driver = WebDriver(schema=config.get('schema'), host=config.get('host'), port=443, authorise=auth, content='application/json')
    response = driver.request(path=uri, method='POST', payload=auth.payload)
    value = get_value(response=response, key='key')
    return value

def get_value(response, key):
    logger.debug('[get_value] key: ' + str(key))
    value = response.json().get(key)
    logger.debug('[get_value] value: ' + str(value))
    return value

@pytest.fixture(scope='class')
def web_driver():
    auth.token = auth_key()
    auth.use = True
    driver = WebDriver(schema=config.get('schema'), host=config.get('host'), port=443, authorise=auth, content='application/json')
    yield driver

def web_driver2():
    auth.token = auth_key()
    auth.use = True
    driver = WebDriver(schema=config.get('schema'), host=config.get('host'), port=443, authorise=auth, content='application/json')
    return driver

def send_request(driver, uri, method=None, data=None, params=None):
    logger.debug('[request] data: ' + str(data))
    response=driver.request(path=uri, method=method, payload=data, params=params)
    logger.debug('[request] response code: ' + str(response.status_code))
    #logger.debug('[request] response text: ' + str(response.text))
    return response

class NotamTest():

    def get_user(self, web_driver):

        url = "/api/auth/user/"
        response = send_request(driver=web_driver, uri=url, method="GET")
        logger.debug('[get_user] response: ' + str(response.text))
        return response

    def get_languages(self, web_driver):

        url = "/api/languages/"
        response = send_request(driver=web_driver, uri=url, method="GET")
        logger.debug('[get_languages] response: ' + str(response.text))
        return response

    def get_projects_review_count(self, web_driver):

        url = "/api/projects/review_count/"
        response = send_request(driver=web_driver, uri=url, method="GET")
        logger.debug('[get_projects_review_count] response: ' + str(response.text))
        return response

    def get_entities_tree(self, web_driver, is_parent):

        url = "/api/entities/"

        querystring = {"is_parent": is_parent}

        response = send_request(driver=web_driver, uri=url, method="GET", params=querystring)
        #logger.debug('[get_entities_tree] response: ' + str(response.text))
        return response

    def get_entity_layer(self, web_driver, entity_layer):

        url = "/api/entity_layers/" + str(entity_layer) + "/"

        response = send_request(driver=web_driver, uri=url, method="GET")
        #logger.debug('[get_entity_layers] response: ' + str(response.text))
        return response

    def get_entity_layer_features(self, web_driver, page, page_size, entity_layer):

        url = "/api/features/"

        querystring = {"page": page, "page_size": page_size, "entity_layer": entity_layer}

        response = send_request(driver=web_driver, uri=url, method="GET", params=querystring)
        #logger.debug('[get_entity_layer_features] response: ' + str(response.text))
        return response

    def get_entity_layer_scenarios(self, web_driver, entity_layer, type):

        url = "/api/scenarios/"

        querystring = {"entity_layer": entity_layer, "type": type}

        response = send_request(driver=web_driver, uri=url, method="GET", params=querystring)
        logger.debug('[get_entity_layer_scenarios] response: ' + str(response.text))
        return response

    def get_feature(self, web_driver, feature):

        url = "/api/features/" + str(feature) + "/"

        response = send_request(driver=web_driver, uri=url, method="GET")
        logger.debug('[get_feature] response: ' + str(response.text))
        return response

    def get_feature_info(self, web_driver, feature):

        url = "/api/features/" + str(feature) + "/info/"
        response = send_request(driver=web_driver, uri=url, method="GET")
        logger.debug('[get_feature_info] response: ' + str(response.text))
        return response


    def create_project(self, **kwargs):
        url = "/api/projects/"

        payload = {} #"{\n    \"start\":\"2018-06-23T00:00:00Z\",\n    \"end\":\"2018-06-29T00:00:00Z\",\n    \"estimated\":false,\n    \"perm\":false,\n    \"wie\":false,\n    \"languages\":[\"en\",\"ru\"],\n    \"features\":[\"e4e063f0-e865-49c4-a2de-7f0c8ab80210\"],\n    \"id\":null,\n    \"entity_layer\":\"14d9ade6-69b1-46cc-bf32-035778b73cd1\",\n    \"scenario\":\"12f4f102-72fe-49a6-99dc-6400e4bf8355\"\n}"

        # {
        #     "start": "2018-06-23T00:00:00Z",
        #     "end": "2018-06-29T00:00:00Z",
        #     "estimated": false,
        #     "perm": false,
        #     "wie": false,
        #     "languages": ["en", "ru"],
        #     "features": ["e4e063f0-e865-49c4-a2de-7f0c8ab80210"],
        #     "id": null,
        #     "entity_layer": "14d9ade6-69b1-46cc-bf32-035778b73cd1",
        #     "scenario": "12f4f102-72fe-49a6-99dc-6400e4bf8355"
        # }

        for key, value in kwargs.items():
            if (key != 'web_driver'):
                payload[key] = value
        jpretty = json.dumps(payload, ensure_ascii=False)
        response = send_request(driver=kwargs.get('web_driver'), uri=url, method="POST", data=jpretty)
        logger.debug('[create_project] response: ' + str(response.text))

        return response

    def patch_project(self, **kwargs):
        logger.debug('[patch_project] project_id: ' + str(kwargs.get('id')))
        url = "/api/projects/" + str(kwargs.get('id')) + "/"

        payload = {}  # "{\n    \"start\":\"2018-06-23T00:00:00Z\",\n    \"end\":\"2018-06-29T00:00:00Z\",\n    \"estimated\":false,\n    \"perm\":false,\n    \"wie\":false,\n    \"languages\":[\"en\",\"ru\"],\n    \"features\":[\"e4e063f0-e865-49c4-a2de-7f0c8ab80210\"],\n    \"id\":null,\n    \"entity_layer\":\"14d9ade6-69b1-46cc-bf32-035778b73cd1\",\n    \"scenario\":\"12f4f102-72fe-49a6-99dc-6400e4bf8355\"\n}"

        # {
        #     "start": "2018-06-23T00:00:00Z",
        #     "end": "2018-06-29T00:00:00Z",
        #     "estimated": false,
        #     "perm": false,
        #     "wie": false,
        #     "languages": ["en", "ru"],
        #     "features": ["e4e063f0-e865-49c4-a2de-7f0c8ab80210"],
        #     "id": null,
        #     "entity_layer": "14d9ade6-69b1-46cc-bf32-035778b73cd1",
        #     "scenario": "12f4f102-72fe-49a6-99dc-6400e4bf8355"
        # }

        for key, value in kwargs.items():
            if (key != 'web_driver'):
                payload[key] = value
        jpretty = json.dumps(payload, ensure_ascii=False)
        response = send_request(driver=kwargs.get('web_driver'), uri=url, method="PATCH", data=jpretty)
        logger.debug('[patch_project] response: ' + str(response.text))

        return response

    def change_state(self, **kwargs):
        logger.debug('[patch_project] project_id: ' + str(kwargs.get('id')))
        url = "/api/projects/" + kwargs.get('id') + "/change_state/"

        payload = {"state": "STAGED"}

        jpretty = json.dumps(payload, ensure_ascii=False)
        response = send_request(driver=kwargs.get('web_driver'), uri=url, method="POST", data=jpretty)
        logger.debug('[change_state] response: ' + str(response.text))

        return response

    def approve_project(self, **kwargs):
        logger.debug('[patch_project] project_id: ' + str(kwargs.get('id')))
        url = "/api/projects/" + kwargs.get('id') + "/approve/"

        payload = {}

        jpretty = json.dumps(payload, ensure_ascii=False)
        response = send_request(driver=kwargs.get('web_driver'), uri=url, method="POST", data=jpretty)
        logger.debug('[change_state] response: ' + str(response.text))

        return response