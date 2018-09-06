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
import os
import sys
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0

urls = (
    '/slir', 'root',
)

testdir = sys.argv[1]
slirep = sys.argv[2]
config = ConfigParser()
configfile=testdir + '/config.ini'
config.read(configfile)
gmlcgw_port = config.get('web_mock', 'gmlcgw_port')
updatefile = config.get('testing', 'updatefile')

app = web.application(urls, globals())

def cleardata(txt,type):
	logging.debug("txt:" + str(txt))
	logging.debug("type:" + str(type))
	if (type == "xml"):
		txt = re.sub("^\s+|\s+$", '', str(txt))
		txt = re.sub(">\s+<|>\n<|>\r<", '><', str(txt))
		txt = re.sub("\t", '', str(txt))
		txt = re.sub("\n", '', str(txt))
	elif (type == "json"):
		#txt = re.sub("^\s+|\s+$|\n|\r", '', txt)
		txt = re.sub("|\n|\r", '', str(txt))
	return txt

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

def request(uri,method,ContentType,usr,pwd,postdata):
	#logging.debug('[request] start')	
	usrPass = usr + ":" + pwd
	b64Val = base64.b64encode(usrPass)
	if (method == "post"):
		resp = requests.post(uri, headers={"Authorization": "Basic %s" % b64Val, "Content-Type" : ContentType}, data=postdata)				
	response = resp.text
	status_code = resp.status_code
	headers = resp.headers
	#logging.debug('[request] response: ' + response)	
	#logging.debug('[request] status_code: ' + str(status_code))	
	#logging.debug('[request] header: ' + str(headers))	
	return resp		
		
class root:      

	def POST(self):
		logging.basicConfig(filename="/tmp/log/gmlc/server_gmlc.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
		#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
		#logging.debug('web.data(): ' + web.data())
		xreq = etree.fromstring(web.data())
		msid = xreq.xpath('//slir')[0].xpath('//msid')[0].text
		#<slir ver="3.2.0" res_type="ASYNC">
		res_type = xreq.xpath('//slir')[0].attrib.get('res_type')
		#logging.debug('res_type: ' + res_type)
		if (res_type == "ASYNC"):
			pushaddr = xreq.xpath('//slir')[0].xpath('//pushaddr')[0].xpath('//url')[0].text
			slia = '''<?xml version="1.0" encoding="utf-8"?>
					<!DOCTYPE svc_result PUBLIC "-//OMA//DTD SVC_RESULT 3.2//EN" "SVC_RESULT.DTD">
					<svc_result xmlns:ma="http://www.mobilearts.com/" ver="3.2.0">
							<slia ver="3.0.0">
									<req_id>''' + msid + '''</req_id>
							</slia>
					</svc_result>'''
			#pool = multiprocessing.Pool(processes=1)
			#res = pool.apply_async(slirep_request)
			slia = re.sub("^\s+|\s+$", '', slia)
			slia = re.sub(">\s+<|>\n<|>\r<", '><', slia)		
			slirep_uri = pushaddr + "gmlcgw/rest/v0/mlp32/slirep"
			if (slirep == "true"):
				os.system("sleep 1 && /app/gmlc/slirep_request.py " + testdir + " " + msid + " " + slirep_uri + " &")

		else:
			f = open(testdir + "/" + updatefile, 'r')
			text = f.read()
			f.close()
			slia = cleardata(text,"xml")
			slia_f = '''<!DOCTYPE svc_result PUBLIC "-//OMA//DTD SVC_RESULT 3.2//EN" "SVC_RESULT.DTD">
			<svc_result ver="3.2.0" xmlns:ma="http://www.mobilearts.com/">
			   <slia ver="3.0.0">
				  <pos pos_method="UNKNOWN">
					 <msid type="MSISDN">''' + msid + '''</msid>
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
						<lev_conf>0</lev_conf>
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
			   </slia>
			   <ma:slia-extension ver="3.0.0">
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
			   </ma:slia-extension>
			</svc_result>'''

		web.header('Content-Type', 'application/xml')
		logging.debug("slia:" + str(slia))
		slia = re.sub("^\s+|\s+$", '', slia)
		slia = re.sub(">\s+<|>\n<|>\r<", '><', slia)
		#logging.debug('slia: ' + slia)
		logging.debug("request:" + str(web.data()))
		logging.debug("response:" + str(slia))		
		print("request:" + str(web.data()))
		print("response:" + str(slia))							
		return (slia)
		
def slirep_request(uri):
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
		#uri="http://10.99.112.143:8086/gmlcgw/rest/v0/mlp32/slirep"
		logging.debug('try request')
		resp = request(uri,"post",ContentType,authuser,authpass,postdata)
		logging.debug('resp: ' + str(resp.text))	

	
if __name__ == "__main__":
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
	app = MyApplication(urls, globals())
	app.run(port=int(gmlcgw_port))	
	

