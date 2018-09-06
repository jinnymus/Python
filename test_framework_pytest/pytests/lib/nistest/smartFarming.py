import logging
import nistest.basic
import sqlalchemy
import json
import allure
import pytest

log = logging.getLogger('nistest.SmartFarming')

headers_expected = {
    'Date': 'Thu, 08 Feb 2018 13:56:48 GMT',
    'X-Server-Info': '(^[A-Za-z-]+)_([0-9\.]+) (\([0-9A-Za-z-]+\)$)',
    'X-Server-Stream': '(^[0-9]+$)',
    'Connection': '(^Keep-Alive$)',
    'Content-Type': '(^application/json$)',
    'Content-Length': '(^[0-9]+$)'
}


class DRS(nistest.basic.Service):

    def __init__(self, host, port, authorise):
        super().__init__(host=host, port=port, authorise=authorise)
        log.debug('[DRS][init] start')
        self.content = 'application/json'
        self.paths = {'create_device': '/public/rest/v1/drs', 'delete_device': '/public/rest/v1/drs', 'change_device': '/public/rest/v1/drs', 'get_device': '/public/rest/v1/drs'}
        self.methods = {'create_device': 'POST', 'delete_device': 'DELETE', 'change_device': 'PATCH', 'get_device': 'GET', 'get_history': 'POST'}
        self.headers_expected = headers_expected
        self.log_path = '/logs/drs/drs.log'
        lgd = nistest.basic.LogDriver(self.log_path)
        lgd.clear_file()

    @pytest.allure.step('Create device')
    def create_device(self, no_check=False, **kwargs):
        smartFarmingDevice = nistest.SmartFarmingDevice(self)
        payload = smartFarmingDevice.get_create_data(**kwargs)
        super().request(device=smartFarmingDevice, method='create_device', payload=payload)
        logging.debug('[SmartFarming][create_device] response: ' + str(smartFarmingDevice.response))
        logging.debug('[SmartFarming][create_device] response: ' + str(smartFarmingDevice.response.text))
        logging.debug('[SmartFarming][create_device] no_check: ' + str(no_check))

        try:
            if (no_check==False):
                assert smartFarmingDevice.response.status_code == 200, smartFarmingDevice.response.text
                smartFarmingDevice.set_id(self.get_id_from_response(smartFarmingDevice.response))
                for key, value in smartFarmingDevice.response.json().items():
                    #print "%s == %s" % (key, vaue)
                    logging.debug('[SmartFarming][create_device] key: ' + str(key) + ' value: ' + str(value))
                    smartFarmingDevice.set_key_value(key,value)
        except KeyError:
            pass
        return smartFarmingDevice

    @pytest.allure.step('Create device')
    def create_device_raw(self, payload):
        smartFarmingDevice = nistest.SmartFarmingDevice(self)
        super().request(device=smartFarmingDevice, method='create_device', payload=payload)
        try:
            smartFarmingDevice.set_id(self.get_id_from_response(smartFarmingDevice.response))
        except KeyError:
            pass
        logging.debug('[SmartFarming][createDeviceRaw] response: ' + str(smartFarmingDevice.response))
        return smartFarmingDevice

    @pytest.allure.step('Change device')
    def change_device(self, smartFarmingDevice, **kwargs):
        payload = smartFarmingDevice.get_change_data(**kwargs)
        path = smartFarmingDevice.get_change_path()
        super().request(device=smartFarmingDevice, method='change_device', payload=payload, path=path)
        for key, value in smartFarmingDevice.response.json().items():
            # print "%s == %s" % (key, vaue)
            logging.debug('[SmartFarming][change_device] key: ' + str(key) + ' value: ' + str(value))
            smartFarmingDevice.set_key_value(key, value)
        logging.debug('[SmartFarming][change_device] response: ' + str(smartFarmingDevice.response))
        return smartFarmingDevice

    @pytest.allure.step('Change device')
    def change_device_raw(self, smartFarmingDevice, payload):
        path = smartFarmingDevice.get_change_path()
        super().request(device=smartFarmingDevice, method='change_device', payload=payload, path=path)
        logging.debug('[SmartFarming][change_device_raw] response: ' + str(smartFarmingDevice.response))
        return smartFarmingDevice

    @pytest.allure.step('Delete device')
    def delete_device(self, smartFarmingDevice):
        path = smartFarmingDevice.get_change_path()
        super().request(device=smartFarmingDevice, method='delete_device', path=path)
        logging.debug('[SmartFarming][delete_device] response: ' + str(smartFarmingDevice.response))
        return smartFarmingDevice

    @pytest.allure.step('Get device')
    def get_device(self, id):
        smartFarmingDevice = nistest.SmartFarmingDevice(self)
        smartFarmingDevice.termId = id
        logging.debug('[SmartFarming][get_device] id: ' + str(id))
        path = smartFarmingDevice.get_read_path()
        super().request(device=smartFarmingDevice, method='get_device', path=path)
        for key, value in smartFarmingDevice.response.json().items():
            # print "%s == %s" % (key, vaue)
            logging.debug('[SmartFarming][create_device] key: ' + str(key) + ' value: ' + str(value))
            smartFarmingDevice.set_key_value(key, value)
        logging.debug('[SmartFarming][get_device] response: ' + str(smartFarmingDevice.response))
        return smartFarmingDevice

    @pytest.allure.step('Get id from response')
    def get_id_from_response(self, response):
        logging.debug('[SmartFarming][get_id_from_response] response: ' + str(response.json()))
        id = response.json()['termId']
        logging.debug('[SmartFarming][get_id_from_response] id: ' + str(id))
        return id

class HDS(nistest.basic.Service):

    def __init__(self, host, port, authorise):
        super().__init__(host=host, port=port, authorise=authorise)
        log.debug('[HDS][init] start')
        self.content = 'application/json2'
        self.paths = {'get_history': '/public/rest/v1/hds/?'}
        self.methods = {'get_history': 'POST'}
        self.headers_expected = headers_expected
        self.log_path = '/logs/hds/hds.log'
        lgd = nistest.basic.LogDriver(self.log_path)
        lgd.clear_file()


    @pytest.allure.step('Get history')
    def get_history(self, **kwargs):

        params_list = ['termId', 'filter', 'limit', 'sort']
        params = ""
        for item in params_list:
            if (kwargs[item] is not None):
                param  = item + '=' + str(kwargs[item]) + '&'
                params = str(params) + str(param)

        #params = 'termId={0}&filter={1}&limit={2}&sort={3}'.format(kwargs['termId'], kwargs['filter'], kwargs['limit'], kwargs['sort'])

        log.debug('[get_history] params: ' + str(params))

        payload = {
          "startTime": str(kwargs['startTime']),
          "endTime": str(kwargs['endTime']),
          "hideTimes": [
             { "from": str(kwargs['dateFrom']), "to": str(kwargs['dateTo'])}
          ]
        }

        response = super().request(method='get_history', path=self.paths.get('get_history') + str(params), payload=payload)
        log.debug('[HDS][get_history] response: ' + str(response.text))
        return response


class INFO(nistest.basic.Service):

    def __init__(self, host, port, authorise):
        super().__init__(host=host, port=port, authorise=authorise)
        log.debug('[INFO][init] start')
        self.content = 'application/json'
        self.paths = {'get_device': '/public/rest/v1/info?list=deviceType', 'get_model': '/public/rest/v1/info?list=model', 'get_protocol': '/public/rest/v1/info?list=protocol'}
        self.methods = {'get_device': 'GET', 'get_model': 'GET', 'get_protocol': 'GET'}
        self.headers_expected = headers_expected
        self.log_path = '/logs/info-serviced/info-serviced.log'
        lgd = nistest.basic.LogDriver(self.log_path)
        lgd.clear_file()

    @pytest.allure.step('Get device')
    def get_device(self):
        response = super().request(method='get_device')
        return response

    @pytest.allure.step('Get model')
    def get_model(self):
        response = super().request(method='get_model')
        return response

    @pytest.allure.step('Get protocol')
    def get_protocol(self):
        response = super().request(method='get_protocol')
        return response

class DB(nistest.basic.DbDriver2):

    def __init__(self, db_host, db_port, db_user, db_pwd, db_database):
        log.debug('[DB][' + str(__name__) + '] start')
        super().__init__(db_host=db_host, db_port=db_port, db_user=db_user, db_pwd=db_pwd, db_database=db_database)
        self.functions = {'create_device': 'f_set_smart_farm', 'get_device': 'f_get_device_farm', 'set_status': 'f_set_status_smart_farm', 'get_dict_device': 'f_get_device_farm', 'get_dict_device_type': 'f_get_device_type', 'get_dict_protocol_family': 'f_get_protocol_family', 'get_start_data': 'f_get_start_data', 'get_history': 'f_get_smart_farm'}
        self.log_path = None

    @pytest.allure.step('Create device')
    def create_device(self, **kwargs):
        try:
            result = super().select_function('create_device', **kwargs)
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    @pytest.allure.step('Set status')
    def set_status(self, **kwargs):
        try:
            result = super().select_function('set_status', **kwargs)
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    @pytest.allure.step('Get device')
    def get_device(self, **kwargs):
        try:
            result = super().select_function('get_device', **kwargs)
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    @pytest.allure.step('Get history')
    def get_history(self, **kwargs):
        try:
            result = super().select_function('get_history', **kwargs)
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    @pytest.allure.step('Get dict device')
    def get_dict_device(self):
        try:
            result = super().select_function('get_dict_device')
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    @pytest.allure.step('Get dict protocol')
    def get_dict_protocol(self):
        try:
            result = super().select_function('get_dict_protocol')
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    @pytest.allure.step('Get dict device type')
    def get_dict_device_type(self):
        try:
            result = super().select_function('get_dict_device_type')
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    @pytest.allure.step('Truncate')
    def truncate(self, table):
        try:
            result = super().truncate(table)
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise

        return result



class KAFKA(nistest.basic.KafkaDriver):

    def __init__(self, topic, lang='json', server='kafka1', schema_registry = 'kafka-schema-registry', server_zoo = 'zoo1' ):
        self.topic = topic
        self.schema_registry = schema_registry
        self.server_zoo = server_zoo
        self.lang = lang
        log.debug('[KAFKA] topic: ' + str(topic))
        log.debug('[KAFKA] server: ' + str(server))
        log.debug('[KAFKA] lang: ' + str(lang))
        log.debug('[KAFKA] schema_registry: ' + str(schema_registry))
        log.debug('[KAFKA] server_zoo: ' + str(schema_registry))
        self.schema = '''{
              "type":"record",
              "name":"Farming",
              "namespace":"nis.dev.validator.avro",
              "fields":[
                {
                  "name": "term_id",
                  "type": "long"
                },
                {
                  "name": "time_platform",
                  "type": {
                    "type": "long",
                    "logicalType": "timestamp-millis"
                  }
                },
                {
                  "name": "time_device",
                  "type": {
                    "type": "long",
                    "logicalType": "timestamp-millis"
                  }
                },
                {
                  "name": "activity_info",
                  "type": "int"
                }
              ]
            }'''
        super().__init__(topic=topic, server=server, schema_registry=schema_registry)
        self.log_path = None

    @pytest.allure.step('Send to kafka')
    def send(self, data):
        log.debug('[KAFKA][send] lang: ' + str(self.lang))
        log.debug('[KAFKA][send] data: ' + str(data))
        log.debug('[KAFKA][send] schema: ' + str(self.schema))
        if (self.lang == 'json'):
            data = json.dumps(data, sort_keys=True).encode('utf-8')
        #else:
            #schema = json.dumps(schema, sort_keys=False).encode('utf-8')
        self.last_offset = super().get_last_offset()
        super().send(msg=data, lang=self.lang, schema=self.schema)

    @pytest.allure.step('Read from kafka')
    def read(self, offset=None):
        if (offset is None):
            offset = self.last_offset
        log.debug('[KAFKA] offset: ' + str(offset))
        result = super().read_from_offset(offset=offset, lang=self.lang, schema=self.schema)
        return result



