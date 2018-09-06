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
    '/ldtdpsvc/rest/v0/ldtd/gmlc', 'root',
	'ldtdpsvc/rest/v0/ldtd/gmlc', 'root',
)

testdir = sys.argv[1]
config = ConfigParser()
configfile=testdir + '/config.ini'
config.read(configfile)
sodtmd_port = config.get('web_mock', 'sodtmd_port')

app = web.application(urls, globals())

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

class root:      

	def POST(self):
		print("1 request:" + str(web.data()))
		logging.basicConfig(filename=testdir + "/logs/server_sodtmd.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
		#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
		#logging.debug('web.data(): ' + web.data())
		resp = '''{"sender":"asfaw","profile":"poisk"}'''
		web.header('Content-Type', 'application/json')
		resp = re.sub("^\s+||\n|\r|\s+$", '', resp)
		logging.debug("request:" + str(web.data()))
		logging.debug("response:" + str(resp))			
		print("request:" + str(web.data()))
		print("response:" + str(resp))					
		return (resp)
		#return web.notfound("Sorry, the page you were looking for was not found.")
	
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
	app = MyApplication(urls, globals())
	app.run(port=int(sodtmd_port))
	

