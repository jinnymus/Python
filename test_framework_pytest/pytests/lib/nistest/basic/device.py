import logging

log = logging.getLogger('nistest.basic.Device')

class Device(object):

    def __init__(self):
        log.debug("[SmartFarming][Device][init] start")

    def set_response(self, response):
        self.response = response

    def set_id(self, id):
        self.id = id

    def set_key_value(self, key, value):
        setattr(self, key, value)

    def get_key_value(self, key):
        return getattr(self, key)

    def get_response(self):
        return self.response

    def get_id(self):
        return self.id



