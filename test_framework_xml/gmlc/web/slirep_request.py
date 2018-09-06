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
import sys

proxies = {
  "http": None,
  "https": None,
}


def request(uri,method,ContentType,usr,pwd,postdata):
	#logging.debug('[request] start')	
	logging.basicConfig(filename=testdir + "/logs/server_slirep.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
	usrPass = usr + ":" + pwd
	b64Val = base64.b64encode(usrPass)
	if (method == "post"):
		resp = requests.post(uri, headers={"Authorization": "Basic %s" % b64Val, "Content-Type" : ContentType, "Accept-Encoding" : "identity"}, data=postdata, proxies=proxies)				
	response = resp.text
	status_code = resp.status_code
	headers = resp.headers
	#logging.debug('[request] response: ' + response)	
	#logging.debug('[request] status_code: ' + str(status_code))	
	#logging.debug('[request] header: ' + str(headers))	
	#logging.debug("request:" + str(web.data()))
	#logging.debug("response:" + str(resp))		
	return resp		
		
def slirep_request(msid,uri):
	logging.debug('msid: ' + msid)	
	#print "msid: " + msid
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
								 <X>55 47 42.731N</X>
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
	#logging.debug('try request')
	resp = request(uri,"post",ContentType,authuser,authpass,postdata)
	#logging.debug('resp: ' + str(resp.text))	
	logging.debug("request:" + str(postdata))
	logging.debug("response:" + str(resp))		
	
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
testdir = sys.argv[1]
msid = sys.argv[2]
uri = sys.argv[3]
logging.basicConfig(filename=testdir + "/logs/server_slirep.log", level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')	
slirep_request(msid,uri)	
	

