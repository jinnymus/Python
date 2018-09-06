#!/usr/bin/env python
import web
import xml.etree.ElementTree as ET
import json
from lxml import etree
import lxml.etree
import logging
import re
import requests, base64
from contextlib import contextmanager
import time
import multiprocessing
from multiprocessing import Process, Value, Array
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
import sys	
	
urls = (
    '/msgxsvc/rest/v0/sms/receiver', 'receiver',
	'/msgxsvc/rest/v0/sms/textmessages', 'textmessages',
	'/msgxsvc/rest/v0/sms/textmessages/listenuris', 'listenuris',
)

testdir = sys.argv[1]
config = ConfigParser()
configfile=testdir + '/config.ini'
config.read(configfile)
sos_port = config.get('web_mock', 'sos_port')

app = web.application(urls, globals())

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

class receiver:

	def POST(self):
		print("1 request:" + str(web.data()))
		logging.basicConfig(filename=testdir + "/logs/server_sos.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
		#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
		#logging.debug('web.data(): ' + web.data())
		resp = '''{"profile":"poisk_info","id":"uuidd5df0d39-196b-4fec-aa26-5dc56a50dd0b"}'''
		web.header('Content-Type', 'application/json')
		resp = re.sub("^\s+||\n|\r|\s+$", '', resp)
		logging.debug("request:" + str(web.data()))
		logging.debug("response:" + str(resp))			
		print("request:" + str(web.data()))
		print("response:" + str(resp))					
		return (resp)

class textmessages:

	def POST(self):
		print("1 request:" + str(web.data()))
		logging.basicConfig(filename=testdir + "/logs/server_sos.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
		#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
		#logging.debug('web.data(): ' + web.data())
		request = json.loads(web.data())
		logging.debug('request: ' + str(request))
		msisdn = request.get('subscriberId')
		logging.debug('msisdn: ' + str(msisdn))
		resp = '''{"profile":"poisk_info","subscriberId":"''' + str(msisdn) + '''","id":"uuidd2df70aa-ed6d-460a-abfb-627cf3bef15a","status":1}'''
		web.header('Content-Type', 'application/json')
		resp = re.sub("^\s+||\n|\r|\s+$", '', resp)
		logging.debug("request:" + str(web.data()))
		logging.debug("response:" + str(resp))
		print("request:" + str(web.data()))
		print("response:" + str(resp))
		return (resp)


class listenuris:

	def POST(self):
		print("1 request:" + str(web.data()))
		logging.basicConfig(filename=testdir + "/logs/server_sos.log", level=logging.DEBUG,
							format='%(asctime)s - %(levelname)s - %(message)s')
		# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
		# logging.debug('web.data(): ' + web.data())
		resp = '''{"uriList":[{"profile":"poisk_ctl","uriid":"7","uri":"http:\/\/inside.poisk.kubernetes\/sms-receiver\/m2m-nis-sms-receiver-rest-api\/public\/rest\/sms","startTime":"2017-12-22T18:50:00+03:00","endTime":null,"uritype":1,"basicAuthFlag":false}]}'''
		web.header('Content-Type', 'application/json')
		resp = re.sub("^\s+||\n|\r|\s+$", '', resp)
		logging.debug("request:" + str(web.data()))
		logging.debug("response:" + str(resp))
		print("request:" + str(web.data()))
		print("response:" + str(resp))
		return (resp)

	def GET(self):
		print("1 request:" + str(web.data()))
		logging.basicConfig(filename=testdir + "/logs/server_sos.log", level=logging.DEBUG,
							format='%(asctime)s - %(levelname)s - %(message)s')
		# logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
		# logging.debug('web.data(): ' + web.data())
		resp = ''''''
		resp = re.sub("^\s+||\n|\r|\s+$", '', resp)
		return (resp)


if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
	app = MyApplication(urls, globals())
	app.run(port=int(sos_port))
	

