import logging
from sqlalchemy import create_engine
import sqlalchemy

log = logging.getLogger('db_driver2')

class DbDriver2(object):

    def __init__(self, db_host, db_port, db_user, db_pwd, db_database):
        log.debug('[DB][' + str(__name__) + '] start')
        self.functions = {'create_device': 'create_device', 'get_device': 'get_device', 'set_status': 'set_status',
                          'get_dict_device': 'get_dict_device', 'get_dict_device_type': 'get_dict_device_type',
                          'get_dict_protocol_family': 'get_dict_protocol_family'}
        log.debug('[DB][' + str(__name__) + '] db_host: ' + str(db_host))
        log.debug('[DB][' + str(__name__) + '] db_port: ' + str(db_port))
        log.debug('[DB][' + str(__name__) + '] db_user: ' + str(db_user))
        log.debug('[DB][' + str(__name__) + '] db_database: ' + str(db_database))
        conn_string = 'postgres://{0}:{1}@{2}:{3}/{4}'.format(db_user, db_pwd, db_host, db_port, db_database)
        log.debug('[DB]' + str(__name__) + '] conn_string: ' + str(conn_string))
        engine = create_engine(conn_string, echo=True, isolation_level="AUTOCOMMIT")
        self.connection = engine.connect()

    def select(self, st):
        log.debug('[DB][' + str(__name__) + '] start')
        try:
            result = self.connection.execute(st)
            log.debug('[DB] result:' + str(result))
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    def procedure(self, st):
        log.debug('[DB][' + str(__name__) + '] start')
        try:
            self.connection.execute(st)
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        except AttributeError as error:
            log.error(error)
            #raise

    def select_args(self, st, **kwargs):
        log.debug('[DB][' + str(__name__) + '] start')
        try:
            result = self.connection.execute(st, list(kwargs.values()))
            log.debug('[DB] result:' + str(result))
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        except AttributeError as error:
            log.error(error)
            raise
        return result

    def select_function(self, function_name, **kwargs):
        log.debug('[DB][' + str(__name__) + '] start')
        log.debug('[DB][' + str(__name__) + '] function_name: ' + str(function_name))
        # params = lambda kwargs: (key + ', :' + key for key, value in kwargs.items())
        st = 'select * from ' + self.functions.get(function_name) + '( ' + self.params(**kwargs) + ')'
        log.debug('[DB][' + str(__name__) + '] st: ' + str(st))
        log.debug('[DB][' + str(__name__) + '] kwargs: ' + str(kwargs))
        try:
            result = self.select_args(st, **kwargs)
        except sqlalchemy.exc.InternalError as error:
            log.error(error)
            raise
        return result

    def truncate(self, name):
        st = 'truncate table ' + str(name) + ' cascade'
        result = self.procedure(st)
        return result

    def params(self, **kwargs):
        params_string = None
        for key, value in kwargs.items():
            if params_string is None:
                params_string = '%s'
            else:
                params_string = params_string + ', %s'
        return params_string

    def close(self):
        self.connection.close()
