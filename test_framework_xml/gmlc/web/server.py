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

#tree = ET.parse('user_data.xml')
#root = tree.getroot()
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	

urls = (
    '/', 'root',
)

app = web.application(urls, globals())

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

def request(uri,method,ContentType,usr,pwd,postdata):
	logging.debug('[request] start')	
	usrPass = usr + ":" + pwd
	b64Val = base64.b64encode(usrPass)
	if (method == "post"):
		resp = requests.post(uri, headers={"Authorization": "Basic %s" % b64Val, "Content-Type" : ContentType}, data=postdata)				
	response = resp.text
	status_code = resp.status_code
	headers = resp.headers
	logging.debug('[request] response: ' + response)	
	logging.debug('[request] status_code: ' + str(status_code))	
	logging.debug('[request] header: ' + str(headers))	
	return resp		
		
class root:      

	#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	

#	def POST_D(function_to_decorate): 
#		logging.debug('POST_D start')
#		def test_func(): 
#			function_to_decorate()
#		logging.debug('POST_D end')
#		return test_func
#
#	def POST(self): 
#		logging.debug('POST start')

#	@contextmanager
	def POST(self):
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
		logging.debug('web.data(): ' + web.data())
		xreq = etree.fromstring(web.data())
		msid = xreq.xpath('//slir')[0].xpath('//msid')[0].text
		#<slir ver="3.2.0" res_type="ASYNC">
		res_type = xreq.xpath('//slir')[0].attrib.get('res_type')
		logging.debug('res_type: ' + res_type)
		slia = '''<?xml version="1.0" encoding="utf-8"?>
				<!DOCTYPE svc_result PUBLIC "-//OMA//DTD SVC_RESULT 3.2//EN" "SVC_RESULT.DTD">
				<svc_result xmlns:ma="http://www.mobilearts.com/" ver="3.2.0">
						<slia ver="3.0.0">
								<req_id>''' + msid + '''</req_id>
						</slia>
				</svc_result>'''
		#logging.debug('slia: ' + slia)
		web.header('Content-Type', 'application/xml')
		#Content-Type: application/xml
		slia = re.sub("^\s+|>\n<|>\r<|\s+$", '', slia)
		slia = re.sub(">\s+<", '><', slia)
		#ServerResponse.Send(slia)
		logging.debug('slia: ' + slia)
		
		pool = multiprocessing.Pool(processes=1)
		res = pool.apply_async(slirep_request)
		
		return (slia)
		
		
	def GET(self):
	#output = 'users:[';
	#for child in root:
                #print 'child', child.tag, child.attrib
                #output += str(child.attrib) + ','
	#output += ']';
		slia = '''<?xml version="1.0" encoding="utf-8"?>
				<!DOCTYPE svc_result PUBLIC "-//OMA//DTD SVC_RESULT 3.2//EN" "SVC_RESULT.DTD">
				<svc_result xmlns:ma="http://www.mobilearts.com/" ver="3.2.0">
						<slia ver="3.0.0">
								<req_id>1</req_id>
						</slia>
				</svc_result>'''
		return slia
		
def slirep_request():
	xreq = etree.fromstring(web.data())
	res_type = xreq.xpath('//slir')[0].attrib.get('res_type')
	logging.debug('res_type: ' + res_type)
	if (res_type == "ASYNC"):
		logging.debug('async request')
		xreq = etree.fromstring(web.data())
		msid = xreq.xpath('//slir')[0].xpath('//msid')[0].text
		logging.debug('msid: ' + msid)	
		postdata='''<!DOCTYPE svc_result PUBLIC "-//OMA//DTD SVC_RESULT 3.2//EN" "SVC_RESULT.DTD">
				<svc_result ver="3.2.0" xmlns:ma="http://www.mobilearts.com/">
				   <slirep ver="3.0.0">
					<req_id>''' + msid +  '''</req_id>
					  <pos pos_method="UNKNOWN">
						 <msid type="MSISDN">''' + msid +  '''</msid>
						 <pd>
							<time utc_off="+0000">20170125154344</time>
							<shape>
							   <CircularArea>
								  <coord>
									 <X>55 47 40.921N</X>
									 <Y>37 33 42.731E</Y>
								  </coord>
								  <radius>271</radius>
								  <distanceUnit>meter</distanceUnit>
							   </CircularArea>
							</shape>
							<qos_not_met/>
						 </pd>
						 <gsm_net_param>
							<cgi>
							   <mcc>250</mcc>
							   <mnc>1</mnc>
							   <lac>6105</lac>
							   <cellid>42085</cellid>
							</cgi>
							<neid>
							   <vmscid>
								  <vmscno>79167494004</vmscno>
							   </vmscid>
							</neid>
							<imsi>250016176688306</imsi>
						 </gsm_net_param>
					  </pos>
				   </slirep>
				   <ma:slirep-extension ver="3.0.0">
					  <ma:trace-id type="XMLC" value="3647595252"/>
					  <ma:network-parameters msid-ref="79858808259">
						 <ma:msid-set ref-type="MSISDN" ref-value="79858808259">
							<ma:msid type="IMSI" value="250016176688306"/>
						 </ma:msid-set>
						 <ma:gsm-net-param timestamp="20170125154344.62">
							<ma:cgi>
							   <mcc>250</mcc>
							   <mnc>1</mnc>
							   <lac>6105</lac>
							   <cellid>42085</cellid>
							</ma:cgi>
							<neid>
							   <vmscid>
								  <vmscno>79167494004</vmscno>
							   </vmscid>
							</neid>
						 </ma:gsm-net-param>
					  </ma:network-parameters>
				   </ma:slirep-extension>
				</svc_result>'''
		postdata = re.sub("^\s+|>\n<|>\r<|\s+$", '', postdata)
		postdata = re.sub(">\s+<", '><', postdata)	
		authuser = "gmlcgwuser1"	
		authpass = "test123"
		ContentType="application/xml"
		uri="http://10.99.112.143:8086/gmlcgw/rest/v0/mlp32/slirep"
		logging.debug('try request')
		resp = request(uri,"post",ContentType,authuser,authpass,postdata)
		logging.debug('resp: ' + str(resp.text))	
	#return result
	
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
	app = MyApplication(urls, globals())
	#app.add_processor(slirep_request)
	#roo = root()
	#roo.POST = roo.POST_D(roo.POST_N())
	app.run(port=10002)
	

