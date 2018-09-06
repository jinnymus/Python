import logging
import os

log = logging.getLogger('nistest.basic.LogDirver')

class LogDriver(object):

    def __init__(self, file_name):
        log.debug("[LogDirver][init] start")
        self.file_name = file_name

    def clear_file(self):
        os.system('echo "" > ' + self.file_name)



