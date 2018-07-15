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
from libs.notam import NotamTest
import libs.notam

config = {
            'host': 'notamdev.qantor.ru',
            'schema' : 'https',
            'port' : 443
          }

auth = auth('admin','admin', False)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

logger = logging.getLogger(__name__)

@pytest.fixture(scope='class')
def web_driver():
    token = libs.notam.auth_key()
    auth.use = True
    auth.token = token
    logger.debug('[test_one] token: ' + str(token))
    logger.debug('[test_one] auth.token: ' + str(auth.token))
    driver = WebDriver(schema=config.get('schema'), host=config.get('host'), port=config.get('port'), authorise=auth, content='application/json')
    yield driver

nt = NotamTest()


@pytest.mark.skip(reason="no way of currently testing this")
def test_get_user(web_driver):
    response = nt.get_user(web_driver)
    logger.debug('[test_get_user] response: ' + str(response.text))
    assert response.status_code == 200
    assert response.json().get('username') == 'admin'

@pytest.mark.skip(reason="no way of currently testing this")
def test_get_languages(web_driver):
    response = nt.get_languages(web_driver)
    logger.debug('[test_get_languages] response: ' + str(response.text))
    assert response.status_code == 200
    assert response.json()[0].get('name') == 'English'

@pytest.mark.skip(reason="no way of currently testing this")
def test_get_projects_review_count(web_driver):
    response = nt.get_projects_review_count(web_driver)
    logger.debug('[test_get_projects_review_count] response: ' + str(response.text))
    assert response.status_code == 200
    assert response.json().get('count')


def get_entities_list():
    web_driver = libs.notam.web_driver2()
    is_parent = 'true'
    response = nt.get_entities_tree(web_driver, is_parent)
    #logger.debug('[get_entities_list] response: ' + str(response.text))
    entities = list()
    [entities.append(entity.get('id')) for entity in response.json()]
    logger.debug('[get_entities_list] len: ' + str(len(entities)))
    #logger.debug('[get_entities_list] entities: ' + str(entities))
    return entities

#@pytest.fixture(scope='function')
def get_entity_layer_list():
    web_driver = libs.notam.web_driver2()
    is_parent = 'true'
    response = nt.get_entities_tree(web_driver, is_parent)
    #logger.debug('[get_entities_list] response: ' + str(response.text))
    entity_layers = list()
    #[entity_layers.append(ids.get('id')) for ids in guid.get('layers') for guid in response.json()]
    for entity in response.json():
        logger.debug('[get_entities_list] entity: ' + str(entity))
        if (len(entity.get('layers')) > 0):
            for layer in entity.get('layers'):
                entity_layers.append(layer.get('id'))
        else:
            logger.debug('[get_entities_list] len: ' + str(len(entity_layers)))
    logger.debug('[get_entities_list] len: ' + str(len(entity_layers)))
    logger.debug('[get_entities_list] entity_layers: ' + str(entity_layers))
    return entity_layers

def get_entity_layer_features_list():
    web_driver = libs.notam.web_driver2()
    page = 1
    page_size = 20
    feature_list = list()
    for entity_layer in get_entity_layer_list():
        response = nt.get_entity_layer_features(web_driver, entity_layer=entity_layer, page=page, page_size=page_size )
        #logger.debug('[get_entities_list] response: ' + str(response.text))
        for item in response.json().get('results'):
            feature_list.append(item.get('id'))
    logger.debug('[get_entities_list] len: ' + str(len(feature_list)))
    #logger.debug('[get_entities_list] entities: ' + str(entities))
    return feature_list

@pytest.mark.skip(reason="no way of currently testing this")
def test_get_entities_tree(web_driver):
    is_parent = 'true'
    response = nt.get_entities_tree(web_driver, is_parent)
    #logger.debug('[test_get_entities_tree] response: ' + str(response.text))
    assert response.status_code == 200, response.text
    assert response.json()[0].get('name')
    #locals()['entities'] = get_entities_list(web_driver)
    #locals()['entity_layers'] = get_entity_layer_list(web_driver)

@pytest.mark.parametrize('entity_layer', get_entity_layer_list())
#@pytest.mark.skip(reason="no way of currently testing this")
def test_get_entity_layer(web_driver, entity_layer):
    #entity_layer = "3aa564f4-7ee4-4dd9-b509-10d22a9478d8"
    response = nt.get_entity_layer(web_driver, entity_layer=entity_layer)
    logger.debug('[test_get_entity_layer] response: ' + str(response.text))
    assert response.status_code == 200, response.text
    assert response.json().get('id') == entity_layer

@pytest.mark.parametrize('entity_layer', get_entity_layer_list())
#@pytest.mark.skip(reason="no way of currently testing this")
def test_get_entity_layer_features(web_driver, entity_layer):
    entity_layer = "3aa564f4-7ee4-4dd9-b509-10d22a9478d8"
    page = 1
    page_size = 20
    response = nt.get_entity_layer_features(web_driver, entity_layer=entity_layer, page=page, page_size=page_size)
    logger.debug('[test_get_entity_layer_features] response: ' + str(response.text))
    assert response.status_code == 200, response.text
    assert response.json().get('count')
    #get_entity_layer_features_list(web_driver=web_driver, entity_layer=entity_layer, page=page, page_size=page_size)

@pytest.mark.parametrize('entity_layer', get_entity_layer_list())
#@pytest.mark.skip(reason="no way of currently testing this")
def test_get_entity_layer_scenarios(web_driver, entity_layer):
    entity_layer = "3aa564f4-7ee4-4dd9-b509-10d22a9478d8"
    type = 'N'
    response = nt.get_entity_layer_scenarios(web_driver, entity_layer=entity_layer, type=type)
    logger.debug('[test_get_entity_layer_scenarios] response: ' + str(response.text))
    assert response.status_code == 200, response.text
    assert response.json()[0].get('id')

@pytest.mark.parametrize('feature', get_entity_layer_features_list())
#@pytest.mark.skip(reason="no way of currently testing this")
def test_get_feature(web_driver, feature):
    #feature = "fdb7a5fd-3b99-44dd-868b-8849a3eeac01"
    response = nt.get_feature(web_driver, feature=feature)
    logger.debug('[test_get_feature] response: ' + str(response.text))
    assert response.status_code == 200, response.text
    assert response.json().get('id') == feature
    #get_entity_layer_features_list()


@pytest.mark.parametrize('feature', get_entity_layer_features_list())
#@pytest.mark.skip(reason="no way of currently testing this")
def test_get_feature_info(web_driver, feature):
    #feature = "fdac0ce0-7c30-48be-825c-845b56d2c50a"
    response = nt.get_feature_info(web_driver, feature=feature)
    logger.debug('[test_get_feature_info] response: ' + str(response.text))
    assert response.status_code == 200, response.text



def test_create_project(web_driver):
    feature = "fdac0ce0-7c30-48be-825c-845b56d2c50a"
    entity_layer = "14d9ade6-69b1-46cc-bf32-035778b73cd1"
    scenario = "8a4e73ef-b4cc-402c-81cf-b20e8a7ecf02"

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

    response = nt.create_project(web_driver=web_driver,
                                 start="2018-07-23T00:00:00Z",
                                 end="2018-07-29T00:00:00Z",
                                 estimated="false",
                                 perm="false",
                                 wie="false",
                                 languages= ["en", "ru"],
                                 features=[feature],
                                 id="null",
                                 entity_layer=entity_layer,
                                 scenario=scenario
                                 )

    logger.debug('[test_create_project] response: ' + str(response.text))
    assert response.status_code == 201, response.text
    assert response.json().get('id')
    project_id = response.json().get('id')
    logger.debug('[test_create_project] project_id: ' + str(project_id))
    response_patch = nt.patch_project(web_driver=web_driver,
                                 start="2018-07-23T00:00:00Z",
                                 end="2018-07-29T00:00:00Z",
                                 estimated="false",
                                 perm="false",
                                 wie="false",
                                 languages=["en", "ru"],
                                 features=[feature],
                                 id=str(project_id)
                                 )
    assert response_patch.status_code == 200, response_patch.text
    assert response_patch.json().get('id')
    logger.debug('[test_create_project] project_id: ' + str(project_id))
    response_change_state = nt.change_state(web_driver=web_driver,
                                 id=str(project_id)
                                 )
    assert response_change_state.status_code == 200, response_change_state.text
    assert response_change_state.json().get('id')

    response_change_state = nt.approve_project(web_driver=web_driver,
                                 id=str(project_id)
                                 )
    assert response_change_state.status_code == 200, response_change_state.text
    assert response_change_state.json().get('id')