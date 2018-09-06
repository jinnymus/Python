#!/usr/bin/python
import logging
import os
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
import re
import glob
import subprocess
import sys
from lxml import etree
import lxml.etree
import requests, base64
import pprint
import json
import xmldiff
from xml_diff import compare
from jsondiff import diff
import shutil
import os
import time
import reverse
import json, ast
import netsnmp
import numexpr as ne
import ast
from random import choice
from string import digits
import string
import random
from collections import OrderedDict
from datetime import date, timedelta
import csv

proxies = {
  "http": None,
  "https": None,
}

key = ""
testdir = ""

class report(object):
	
    def __init__(self):
        self.logfile = open(htmlfile, 'w')
		
    def log(self,msg):
        self.logfile.writelines(msg + '\n')
		
    def end(self):
        self.logfile.close()
	
class report_for_jenkins(object):
	
    def __init__(self):
        self.logfile = open(reportfile, 'w')
		
    def log(self,msg):
        self.logfile.writelines(msg + '\n')
		
    def end(self):
        self.logfile.close()
		
def copylog(file, testn, case, type):
	logging.debug('[copylog] file: ' + str(file))
	filename = file
	testn = testn[::-1]
	testn = testn.split('/')[0]
	testn = testn[::-1]
	filename = filename[::-1]
	filename = filename.split('/')[0]
	filename = filename[::-1]
	logging.debug('[copylog] filename: ' + str(filename))
	logging.debug('[copylog] ' + 'cp -rf ' + file + ' ' + testdir + '/logs/' + testn + '_case' + str(case) + '_.' + type + '_' + filename + ' >> ' + logname + ' 2>&1')
	res = os.system('cp -rf ' + file + ' ' + testdir + '/logs/' + testn + '_case' + str(case) + '_.' + type + '_' + filename + ' >> ' + logname + ' 2>&1')
	logging.debug('[copylog] res: ' + str(res))

def getNodePath(node):
    return node.getroottree().getpath(node)

def doStripWhitespaces(text):
    if text==None:
        return None
    else:
        return text.strip().replace('\n','').replace('\r','')

def text_compare(t1, t2,strip_whitespaces=False,  float_compare=False):
    if not t1 and not t2:
        return True
    if float_compare:
        try:
            f1 = float(t1)
            f2 = float(t2)
            return f1 == f2
        except ValueError, TypeError:
            pass
    if strip_whitespaces:
        return (doStripWhitespaces(t1) or '') == (doStripWhitespaces(t2) or '')
    else:
        return (t1 or '') == (t2 or '')

def doReport(reporter,x1,x2,errorMsg):
    #if reporter:
    #reporter(getNodePath(x1)+" "+getNodePath(x2)+os.linesep+errorMsg+os.linesep)		
	logging.error(getNodePath(x1)+" "+getNodePath(x2)+errorMsg)
		
def xml_compare(x1, x2, reporter=None, strip_whitespaces=False,ignore_order=False,float_compare=False):
    if x1.tag != x2.tag:
        doReport(reporter,x1,x2,'Tags do not match: %s and %s' % (x1.tag, x2.tag))
        return False

    for name, value in x1.attrib.items():
        if not text_compare(value, x2.attrib.get(name), strip_whitespaces=strip_whitespaces, float_compare=float_compare):
            doReport(reporter,x1,x2,'Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
            return False
    for name in x2.attrib.keys():
        if not x1.attrib.has_key(name):
            doReport(reporter,x1,x2,'x2 has an attribute x1 is missing: %s' % name)
            return False
    if not text_compare(x1.text, x2.text, strip_whitespaces=strip_whitespaces, float_compare=float_compare):
        doReport(reporter,x1,x2,'text: %r != %r' % (x1.text, x2.text))
        return False

    if not text_compare(x1.tail, x2.tail, strip_whitespaces=strip_whitespaces, float_compare=float_compare):
        doReport(reporter,x1,x2,'tail: %r != %r' % (x1.tail, x2.tail))
        return False

    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        doReport(reporter,x1,x2,'children length differs, %i != %i'% (len(cl1), len(cl2)))
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not xml_compare(c1, c2, reporter, strip_whitespaces=strip_whitespaces, float_compare=float_compare):
            doReport(reporter,c1,c2,'children %i do not match: %s'% (i, c1.tag))
            return False
    return True

def getSnmpMetric(metric):
	Var = netsnmp.Varbind(metric)
	Vars = netsnmp.VarList(Var)
	sess = netsnmp.Session(Version = 2, DestHost='localhost', Community='public')
	result = sess.walk(Vars)
	for i in Vars:
		name = i.tag
		value = i.val
		if (name == metric):
			return value	
	
def read_action_file(path):
	cases = {}
	case = []
	steps = {}
	logging.debug('[read_action_file] path: ' + path)
	#parser = etree.XMLParser(encoding="windows-1251")
	#parser = etree.XMLParser(encoding="utf-8")
	#tree = etree.parse( path + "/" + actionfile, parser=parser )
	tree = etree.parse(path + "/" + actionfile)
	root = tree.getroot()
	return root

def request(uri,method,ContentType,XSender,usr,pwd,postdata,auth):
	logging.debug('[request] start')	
	logging.debug('[request] uri: ' + uri)	
	logging.debug('[request] auth: ' + auth)	
	usrPass = usr + ":" + pwd
	b64Val = base64.b64encode(usrPass)
	headers= {}
	if (auth == "true"):
		headers['Authorization'] = "Basic %s" % b64Val
	headers['Content-Type'] = ContentType
	headers['X-Sender'] = XSender

	logging.debug('[request] headers: ' + str(headers))	
	if (method == "post"):
		resp = requests.post(uri, headers=headers, data=postdata, proxies=proxies)				
	if (method == "get"):
		resp = requests.get(uri, headers=headers, proxies=proxies)						
	response = resp.text
	status_code = resp.status_code
	headers = resp.headers
	logging.debug('[request] response: ' + response)	
	logging.debug('[request] status_code: ' + str(status_code))	
	logging.debug('[request] header: ' + str(headers))	
	return resp
	
def jsonpretty(jsonstr):
	try:
		jpretty = json.loads(jsonstr)
		jpretty = json.dumps(jpretty, indent=4, sort_keys=True)
		return jpretty
	except ValueError as e:
		logging.error("jsonpretty fail jsonpretty: " + str(jsonstr))
		logging.error("exception: " + str(e))

def xmlpretty(xmlstr):
	xresp = etree.fromstring(str(xmlstr))
	xpretty = etree.tostring(xresp, pretty_print=True)	
	return xpretty

def printlog(logg):
	logging.debug("[printlog] logg:" + str(logg))
	with open(logg, 'r') as logfile:
		lines = logfile.read().splitlines()
		#for line in lines:
			#logging.debug('[printlog] logline: ' + line)
def getcaseconfig(parameter):
	return config.get('cases', parameter)
			
def opentraff():
	logging.debug('[opentraff] tshark_file: ' + tshark_file)
	trafffile = open(tshark_file,'r')
	traff = trafffile.readlines()
	logging.debug('[opentraff] len traff: ' + str(len(traff)))
	trafffile.close()
	return traff
	
def cleardata(txt,type):
	try:
		if (str(txt) == "None"):
			txt = ""
		elif (type == "xml"):
			txt = re.sub("^\s+|\s+$", '', txt)
			txt = re.sub(">\s+<|>\n<|>\r<", '><', txt)
		elif (type == "json"):
			#txt = re.sub("^\s+|\s+$|\n|\r", '', txt)
			txt = re.sub("|\n|\r", '', txt)
	except UnicodeEncodeError as e:
		logging.debug('[cleardata] e: ' + str(e))

	return txt
	
def getdump(node, searchline):
	logging.debug("[getdump] node: " + node)
	logging.debug("[getdump] searchline: '" + searchline + "'")
	value = ""
	traff = opentraff()
	for line in traff:
		logging.debug("[getdump] line: " + str(line))
		if (line.strip() != ''):
			assertpretty = json.loads(str(line))
			pattern_search = re.compile(r'.*' + searchline + '.*')
			if ('timestamp' in assertpretty):
				logging.debug("[getdump] line: " + str(assertpretty))
				try:
					#if (assertpretty.has_key('timestamp')):
					if ("http_file_data" in assertpretty['layers']):
						logging.debug("[getdump] http_file_data exist")
						try:
							http_file_data = str(assertpretty['layers']['http_file_data'][0])
							logging.debug("[getdump] http_file_data: " + str(http_file_data))
							if (pattern_search.match(http_file_data)):
								logging.debug("[getdump] pattern_search detected with node: " + node + " searchline: " + searchline)
								value = locals()[node]
								logging.debug("[getdump] return value: " + value)
								return (value)
						except UnicodeEncodeError as e:
							logging.error("[getdump] assertpretty http_file_data UnicodeEncodeError: " + str(e))
						if ('http_request_version' in assertpretty['layers']):
							http_request_version = str(assertpretty['layers']['http_request_version'][0])
							logging.debug("[getdump] http_request_version: " + str(http_request_version))
						if ('http_content_type' in assertpretty['layers']):
							http_content_type = str(assertpretty['layers']['http_content_type'][0])
							if (http_content_type == "application/xml"):
								http_file_data = cleardata(http_file_data,"xml")
							if (http_content_type == "application/json"):
								http_file_data = cleardata(http_file_data,"json")
						if ('http_request_method' in assertpretty['layers']):
							http_request_method = str(assertpretty['layers']['http_request_method'][0])
							http_request_full_uri = str(assertpretty['layers']['http_request_full_uri'][0])
							http_request_uri = str(assertpretty['layers']['http_request_uri'][0])
							logging.debug("[getdump] http_request_method: " + str(http_request_method))
							logging.debug("[getdump] http_request_full_uri: " + str(http_request_full_uri))
							logging.debug("[getdump] http_request_uri: " + str(http_request_uri))

						if ('ip_src_host' in assertpretty['layers']):
							ip_src_host = str(assertpretty['layers']['ip_src_host'][0])
							logging.debug("[getdump] ip_src_host: " + str(ip_src_host))
						if ('ip_dst_host' in assertpretty['layers']):
							ip_dst_host = str(assertpretty['layers']['ip_dst_host'][0])
							logging.debug("[getdump] ip_dst_host: " + str(ip_dst_host))
						if ('tcp_dstport' in assertpretty['layers']):
							tcp_dstport = str(assertpretty['layers']['tcp_dstport'][0])
							logging.debug("[getdump] tcp_dstport: " + str(tcp_dstport))
						if ('tcp_srcport' in assertpretty['layers']):
							tcp_srcport = str(assertpretty['layers']['tcp_srcport'][0])
							logging.debug("[getdump] tcp_srcport: " + str(tcp_srcport))
						if ('tcp_port' in assertpretty['layers']):
							tcp_port_src = str(assertpretty['layers']['tcp_port'][0])
							logging.debug("[getdump] tcp_port_src: " + str(tcp_port_src))
						if ('tcp_port' in assertpretty['layers']):
							tcp_port_dst = str(assertpretty['layers']['tcp_port'][1])
							logging.debug("[getdump] tcp_port_dst: " + str(tcp_port_dst))
						if ('http_response_code' in assertpretty['layers']):
							http_response_code = str(assertpretty['layers']['http_response_code'][0])
							logging.debug("[getdump] http_response_code: " + str(http_response_code))
						if ('http_content_type' in assertpretty['layers']):
							logging.debug("[getdump] http_content_type: " + str(http_content_type))

					#else:
					#	logging.error("[getdump] http_file_data not exist")
					#	logging.error("[getdump] assertpretty: " + str(assertpretty))	
				except TypeError as e:
					logging.error("[getdump] http_file_data not exist searchline: '" + searchline + "' node: " + str(node))
					logging.error("[getdump] e: " + str(e))	
	return ""

def getPoolMatrix(case_dir):
	logging.debug('[main][getPoolValue] start')	
	logging.debug('[main][getPoolValue] case_dir: ' + case_dir)	
	pools = 1
	pools_dict = []
	c = []
	for node in read_action_file(case_dir).getchildren():
		#if read_action_file(case_dir).xpath('//datapools'):
		if node.tag == "datapools":
			logging.debug('[main][getPoolValue] tag datapools')
			datapoolsobj = read_action_file(case_dir).xpath('//datapools')[0]
			datapoolscount = len(read_action_file(case_dir).xpath('//datapools')[0].getchildren())
			logging.debug('[main][getPoolValue] datapoolscount: ' + str(datapoolscount))
			c = []				
			for pool in read_action_file(case_dir).xpath('//datapools')[0]:
				e = {}
				c_t = []
				poolscount = len(pool.getchildren())
				poolvalue = pool.attrib.get('value')				
				poolexpected = pool.attrib.get('expected')				
				#print str(i)
				if (len(c) != 0):
					for y in c:
						logging.debug('[main][getPoolValue] ----------------------------------')
						for p in pool.getchildren():
							w = {}
							logging.debug('[main][getPoolValue] --- row ------')
							logging.debug('[main][getPoolValue] poolvalue: ' + poolvalue)
							w[poolvalue + '#' + poolvalue] = str(p.xpath('.//value')[0].text)
							w[poolvalue + '#' + poolexpected] = str(p.xpath('.//expected')[0].text)							
							logging.debug('[main][getPoolValue] it: ' + str(p.xpath('.//value')[0].text) + ' it: ' + str(p.xpath('.//expected')[0].text))
							logging.debug('[main][getPoolValue] y: ' + str(y))
							w.update(p)
							w.update(y)
							logging.debug('[main][getPoolValue] w: ' + str(w))
							c_t.append(w)	
							logging.debug('[main][getPoolValue] c_t: ' + str(c_t))
							logging.debug('[main][getPoolValue] c: ' + str(c))
				else:
					for p in pool.getchildren():
						w = {}
						logging.debug('[main][getPoolValue] ---- row -----')
						logging.debug('[main][getPoolValue] poolvalue: ' + poolvalue)
						w[poolvalue + '#' + poolvalue] = str(p.xpath('.//value')[0].text)
						w[poolvalue + '#' + poolexpected] = str(p.xpath('.//expected')[0].text)			
						logging.debug('[main][getPoolValue] it: ' + str(p.xpath('.//value')[0].text) + ' it: ' + str(p.xpath('.//expected')[0].text))
						w.update(p)
						logging.debug('[main][getPoolValue] w: ' + str(w))
						c_t.append(w)	
						logging.debug('[main][getPoolValue] c_t: ' + str(c_t))
						logging.debug('[main][getPoolValue] c: ' + str(c))
				c = c_t
				usepool = 1
			logging.debug('[main][getPoolValue] c: ' + str(c))
	return c

def getPool(case_dir):
	logging.debug('[main][getPoolValue] start')	
	logging.debug('[main][getPoolValue] case_dir: ' + case_dir)	
	pools = 1
	pools_dict = []
	c = []
	for node in read_action_file(case_dir).getchildren():
		#if read_action_file(case_dir).xpath('//datapools'):
		if node.tag == "datapools":
			logging.debug('[main][getPoolValue] tag datapools')
			datapoolsobj = read_action_file(case_dir).xpath('//datapools')[0]
			datapoolscount = len(read_action_file(case_dir).xpath('//datapools')[0].getchildren())
			logging.debug('[main][getPoolValue] datapoolscount: ' + str(datapoolscount))
			c = []				
			for pool in read_action_file(case_dir).xpath('//datapools')[0]:
				e = {}
				c_t = []
				poolscount = len(pool.getchildren())
				poolname = pool.attrib.get('name')		
				logging.debug('[main][getPoolValue] poolname: ' + str(poolname) + ' #####################################')
				#poolexpected = pool.attrib.get('expected')				
				#print str(i)
				if (len(c) != 0):
					for y in c:
						logging.debug('[main][getPoolValue] ----------------------------------')
						for row in pool.getchildren():
							dict_tmp = {}
							logging.debug('[main][getPoolValue] --- row1 #################### ')
							logging.debug('[main][getPoolValue] params count: ' + str(len(row.getchildren())))
							for param in row.getchildren():
								logging.debug('[main][getPoolValue] --- parameter1 ------')
								param_value = param.attrib.get('value')		
								param_expected = param.attrib.get('expected')
								logging.debug('[main][getPoolValue] param_value: ' + param_value + " param_expected: " + param_expected)
								dict_tmp[param_value + '#' + param_value] = str(param.xpath('.//value')[0].text)
								dict_tmp[param_value + '#' + param_expected] = str(param.xpath('.//expected')[0].text)							
								logging.debug('[main][getPoolValue] it: ' + str(param.xpath('.//value')[0].text) + ' it: ' + str(param.xpath('.//expected')[0].text))
								logging.debug('[main][getPoolValue] y row in final dic: ' + str(y))
								dict_tmp.update(row)
								dict_tmp.update(y)
								logging.debug('[main][getPoolValue] dict_tmp: ' + str(dict_tmp))
							c_t.append(dict_tmp)	
							logging.debug('[main][getPoolValue] c_t dic prefinal: ' + str(c_t))
							logging.debug('[main][getPoolValue] c dic final: ' + str(c))
				else:
					for row in pool.getchildren():
						dict_tmp = {}
						logging.debug('[main][getPoolValue] --- row2 #################### ')
						logging.debug('[main][getPoolValue] params count: ' + str(len(row.getchildren())))
						for param in row.getchildren():
							logging.debug('[main][getPoolValue] --- parameter2 ------')
							param_value = param.attrib.get('value')		
							param_expected = param.attrib.get('expected')
							logging.debug('[main][getPoolValue] param_value: ' + str(param_value) + " param_expected: " + str(param_expected))
							dict_tmp[param_value + '#' + param_value] = str(param.xpath('.//value')[0].text)
							dict_tmp[param_value + '#' + param_expected] = str(param.xpath('.//expected')[0].text)			
							logging.debug('[main][getPoolValue] it: ' + str(param.xpath('.//value')[0].text) + ' it: ' + str(param.xpath('.//expected')[0].text))
							dict_tmp.update(row)
							logging.debug('[main][getPoolValue] dict_tmp: ' + str(dict_tmp))
						c_t.append(dict_tmp)	
						logging.debug('[main][getPoolValue] c_t dic prefinal: ' + str(c_t))
						logging.debug('[main][getPoolValue] c dic final: ' + str(c))
				c = c_t
				usepool = 1
			logging.debug('[main][getPoolValue] c: ' + str(c))
	return c	
	
def setPoolValue(pool, postdata, type):	
	logging.debug('[main][datapools][setPoolValue] start')
	logging.debug('[main][datapools][setPoolValue] type: ' + type)
	plvalue = "";	
	#for pool in poollist:
	logging.debug('[main][datapools][setPoolValue] pool: ' + str(pool))
	for val, data in pool.items():
		logging.debug('[main][datapools][setPoolValue] val: ' + str(val) + ' data: ' + str(data))
		poolvalue = val[0:val.index('#')]
		poolexpected = val[val.index('#')+1:None]
		if (poolvalue == poolexpected):
			if (type == "value"):
				logging.debug('[main][datapools][setPoolValue] poolvalue: ' + str(poolvalue) + ' data: ' + str(data))			
				logging.debug('[main][datapools][setPoolValue] setting value')
				postdata = re.sub('#{' + poolvalue + '}', data, postdata)
				logging.debug('[main][datapools][setPoolValue] postdata: ' + str(postdata))
		else:
			if (type == "expected"):			
				logging.debug('[main][datapools][setPoolValue] poolexpected: ' + str(poolexpected) + ' data: ' + str(data))	
				logging.debug('[main][datapools][setPoolValue] setting expected')
				postdata = re.sub('#{' + poolexpected + '}', data, postdata)
				#logging.debug('[main][datapools][setPoolValue] postdata: ' + str(postdata))
	#logging.debug('[main][datapools][setPoolValue] postdata: ' + str(postdata))						
	return postdata
	
def main(argv=None):
	logging.debug('[main] start testing')	
	with open(testdir + "/testplan.dat",'r') as f:
		testplan = f.read().splitlines()
	#testplanfile=open(testdir + "/testplan.dat","r")
	#testplan = testplanfile.readlines()
	#testplanfile.close()
	logging.debug('[main] testplan: ' + str(testplan))	
	cases_dir = glob.glob(cases_path + "/*")  
	cases_dir.sort(key=os.path.getmtime,reverse=False)
	tests = 0
	passed = 0
	failed = 0
	usepool = 0
	total_assertspassed = 0
	total_assertsfailed = 0
	html = report()
	reportj = report_for_jenkins()
	html.log('<table border="1" colspan="3">')
	html.log('<tr><td><b>Test Name</b></td><td><b>Steps</b></td><td><b>Asserts</b></td></tr>')
	for test in testplan:
		if (test != ""):
			case_dir = testdir + "/cases/" + test
			logging.debug('[main] run test: ' + test)
			logging.debug('[main] case_dir: ' + case_dir)
			logging.debug('[main] testdir: ' + testdir)
			testname = read_action_file(case_dir).attrib.get('name')
			logging.debug('[main] testname: ' + testname)
			fail=0
			maxrange = 1
			case = 0
			pools = 1
			for node in read_action_file(case_dir).getchildren():
				logging.debug('[main] case: ' + str(case))
				logging.debug('[main] test start #########################' + testname + '#' + case_dir + '###############################################################')								
				if node.tag == "datapools":
					logging.debug('[main] tag datapools')
				if node.tag == "steps":
					logging.debug('[main] tag steps')
					logging.debug('[main] maxrange: ' + str(maxrange))
					logging.debug('[main] pools: ' + str(pools))
					stepsscount = len(node.getchildren())
					logging.debug('[main] steps count: ' + str(stepsscount))
					#datapoollist = datapoolscount
					poollist = getPool(case_dir)
					if (len(poollist) != 0):
						usepool = 1
					else:
						usepool = 0
						d = {'test':'1'}
						poollist.append(d)
					logging.debug('[main] usepool: ' + str(usepool))
					#for x in range(0, maxrange):
					for pool in poollist:
						logging.debug('[main] test pool start ##########################' + testname + '#' + case_dir + '#############################################################')					
						logging.debug('[main] pool: ' + str(pool))
						plvalue = ""
						if (usepool == 1):
							for val, data in pool.items():
								poolvalue = val[0:val.index('#')]
								poolexpected = val[val.index('#')+1:None]
								if (poolvalue == poolexpected):
									logging.debug('[main][datapools][setPoolValue] setting value')
									plvalue += poolvalue + ':' + data + " "
						logging.debug('[main][datapools][datapool] plvalue: ' + str(plvalue))
						fail=0
						tests += 1
						case += 1			
						html_text_all = ""
						stepsfailed = 0
						assertspassed = 0
						assertsfailed = 0
						for step in node.getchildren():
							html_text = ""
							stepfail = 0
							authuser=""
							authpass=""
							auth="false"
							step_name = step.attrib.get('name')
							step_type = step.attrib.get('type')
							logging.debug('[main] step start ##############' + str(testname) + '#' + str(case_dir) + '#' + str(step_name) + '#' + str(step_type) + '##############################################################')								
							if (step.attrib.get('status') == "enabled"):
								logging.debug('[main] step_type: ' + str(step_type) + " enabled")
								if (step_type == "updatefile"):
									logging.debug('[main][' + step_name + '][' + step_type + '] start')
									upfile = step.attrib.get('file')
									for stepnode in step.getchildren():
										if (stepnode.tag == "data"):
											lang = step.attrib.get('lang')
											postdata = stepnode.text
											if (lang == "json"):
												postdata = cleardata(postdata,"json")
											elif (lang == "xml"):
												postdata = cleardata(postdata,"xml")									
											logging.debug('[main][' + step_type + '] upfile: ' + upfile)				
											if (patternconfig.match(upfile)):
												updatefile = getcaseconfig(patternconfig.match(upfile).group(1))
												logging.debug('[main][' + step_name + '][' + step_type + '][getcaseconfig] updatefile: ' + updatefile)
											with open(testdir + "/" + updatefile, 'w') as f:
												f.write(postdata)
									#os.system('echo "' + postdata + '" > ' + updatefile)
									assertspassed += 1								
								if (step_type == "daemon"):
									logging.debug('[main][' + step_name + '][' + step_type + '] start')
									daemon = step.attrib.get('daemon')
									action = step.attrib.get('action')
									#patternconfig = re.compile(r'.*#{([a-zA-Z0-9_]+)}.*')
									#if (patternconfig.match(logfile)):
									#	logf = getcaseconfig(patternconfig.match(logfile).group(1))
									#	logging.debug('[main][' + step_type + '] logf: ' + logf)				
									#	#open(logfile, 'w').close()
									cmd = 'systemctl ' + action + ' ' + daemon + ' >> ' + logname + ' 2>&1'
									logging.debug('[main][' + step_name + '][' + step_type + '] cmd: ' + str(cmd))
									os.system(cmd)
									assertspassed += 1			
								if (step_type == "clearlog"):
									logging.debug('[main][' + step_name + '][' + step_type + '] start')
									logfile = step.attrib.get('log')
									patternconfig = re.compile(r'.*#{([a-zA-Z0-9_]+)}.*')
									if (patternconfig.match(logfile)):
										logf = getcaseconfig(patternconfig.match(logfile).group(1))
										logging.debug('[main][' + step_type + '] logf: ' + logf)				
										#open(logfile, 'w').close()
										os.system('echo "" > ' + logf)
										assertspassed += 1											
								if (step_type == "tsharkdump"):
									logging.debug('[main][' + step_name + '][' + step_type + '] start')
									#logging.debug('[main][' + step_type + '] run: ' + binfolder + '/get_dump.sh ' + tshark_port1 + ' ' + tshark_port2 + ' '  + tshark_port3 + ' '  + tshark_file + ' ' + tshark_duration + ' &')
									kill=os.system("kill -9 `ps -Aef | awk '{if ($9 ~ /tshark/) print $2; if ($8 ~ /tshark/) print $2}'` >> " + logname + " 2>&1")
									logging.info("kill temp tshark: " + str(kill))
									#tshark_shell = 'tshark -s0 -i lo -V -Y "((http.request.method == POST or http.request.method == POST or http.response) and ((tcp.port == ' + tshark_port1 + ') or (tcp.port == ' + tshark_port2 + ') or (tcp.port == ' + tshark_port3 + '))) or http.content_encoding or http.response or http.request or http.request.method or http.response.code or http.content_type or http.file_data" -Tek -e http.file_data -e http.request.full_uri -e http.request.method -e http.request.version -e http.response.code -e http.content_type -e http.request.uri -e ip.src_host -e ip.dst_host -e tcp.srcport -e tcp.dstport -e tcp.port -Eseparator=# > ' + tshark_file + ' &'
									#shell_cmd = binfolder + '/get_dump.sh ' + tshark_file + ' ' + tshark_duration + ' ' + tshark_ports_count + ' ' 
									port_str = ''
									for cnt in range(1,int(tshark_ports_count)+1):
										tshark_port = config.get('tshark', 'port' + str(cnt))
										#shell_cmd += tshark_port + " "
										port_str += '(tcp.port == "' + str(tshark_port) + '")'
										if cnt < int(tshark_ports_count):
											port_str = port_str + ' or '
									#tshark_shell = os.system(binfolder + '/get_dump.sh ' + tshark_port1 + ' ' + tshark_port2 + ' '  + tshark_port3 + ' '  + tshark_file + ' ' + tshark_duration + ' &')
									tshark_shell = 'tshark -l -i lo -V -Y "((http.request.method == POST or http.request.method == POST or http.response) and (' + port_str + ')) or http.content_encoding or http.response or http.request or http.request.method or http.response.code or http.content_type or http.file_data" -Tek -e http.file_data -e http.request.full_uri -e http.request.method -e http.request.version -e http.response.code -e http.content_type -e http.request.uri -e ip.src_host -e ip.dst_host -e tcp.srcport -e tcp.dstport -e tcp.port -Eseparator=# > ' + tshark_file + ' &'
									#shell_cmd += " &"
									logging.debug('[main][' + step_type + '] run: ' + str(tshark_shell))
									tsh = os.system(tshark_shell)
									logging.debug('[main][' + step_type + '] tsh: ' + str(tsh))
									assertspassed += 1
								if (step_type == "delay"):
									logging.debug('[main][' + step_name + '][' + step_type + '] start')
									seconds = step.attrib.get('seconds')
									time.sleep(float(seconds))
									assertspassed += 1								
								if (step_type == "request"):
									resp=""
									logging.debug('[main][' + step_name + '][' + step_type + '] start')
									uri = step.attrib.get('uri')	
									method = step.attrib.get('method')
									ContentType = ""
									if 'ContentType' in step.attrib:
										ContentType = step.attrib.get('ContentType')
										logging.debug(
											'[main][' + step_name + '][' + step_type + '] ContentType: ' + str(ContentType))
									XSender = ""
									if 'XSender' in step.attrib:
										XSender = step.attrib.get('XSender')
										logging.debug('[main][' + step_name + '][' + step_type + '] XSender: ' + str(XSender))
									postdata=""
									if 'authuser' in step.attrib:
										logging.debug('[main][' + step_name + '][' + step_type + '] auth exist')
										authuser = step.attrib.get('authuser')	
										authpass = step.attrib.get('authpass')
										auth="true"
									try:
										host_ip = step.attrib.get('host')
										host_port = step.attrib.get('port')
									except TypeError as e:
										logging.debug('[main][' + testname + '][' + step_name + '][' + step_type + '] e: ' + str(e))
									logging.debug('[main][' + step_name + '][' + step_type + '] host_ip: ' + host_ip)								
									logging.debug('[main][' + step_name + '][' + step_type + '] host_port: ' + host_port)
									patternconfig = re.compile(r'.*#{([a-zA-Z0-9_]+)}.*')
									if (patternconfig.match(host_ip)):
										host_ip = getcaseconfig(patternconfig.match(host_ip).group(1))
										logging.debug('[main][' + step_name + '][' + step_type + '][getcaseconfig] host_ip: ' + host_ip)
									if (patternconfig.match(host_port)):
										host_port = getcaseconfig(patternconfig.match(host_port).group(1))									
										logging.debug('[main][' + step_name + '][' + step_type + '][getcaseconfig] host_port: ' + host_port)
									logging.debug('[main][' + step_type + '] uri: ' + uri)
									logging.debug('[main][' + step_type + '] method: ' + method)
									logging.debug('[main][' + step_type + '] ContentType: ' + ContentType)
									logging.debug('[main][' + step_type + '] authuser: ' + authuser)
									logging.debug('[main][' + step_type + '] authpass: ' + authpass)	
									for stepnode in step.getchildren():
										if (stepnode.tag == "data"):
											lang = step.attrib.get('lang')
											postdata = stepnode.text
											if (lang == "json"):
												postdata = cleardata(postdata,"json")
											elif (lang == "xml"):
												postdata = cleardata(postdata,"xml")
											if usepool == 1:
												logging.debug('[main][' + step_name + '][' + step_type + '] usepool replacing')	
												logging.debug('[main][' + step_name + '][' + step_type + '] postdata: ' +  postdata)	
												logging.debug('[main][' + step_name + '][' + step_type + '] start setPoolValue')
												postdata = setPoolValue(pool, postdata, 'value')
												logging.debug('[main][' + step_name + '][' + step_type + '] plvalue: ' +  plvalue)	
												logging.debug('[main][' + step_name + '][' + step_type + '] postdata: ' +  postdata)	
											if (stepnode.attrib.get("lang")=="json"):
												try:
													postdata = jsonpretty(postdata)
												except ValueError as e:
													logging.debug('[main][' + step_type + '] jsonpretty(postdata) ValueError: ' + str(e))	
												except Exception as e:
													logging.debug('[main][' + step_type + '] jsonpretty(postdata) ValueError: ' + str(e))													
											if (stepnode.attrib.get("lang")=="xml"):
												try:
													postdata = xmlpretty(postdata)
												except ValueError as e:
													logging.debug('[main][' + step_type + '] xmlpretty(postdata) ValueError: ' + str(e))													
												except Exception as e:
													logging.debug('[main][' + step_type + '] xmlpretty(postdata) ValueError: ' + str(e))															
											logging.debug('[main][request] postdata: ' + str(postdata))													
											if (method == "get"):
												uri = uri + "?"
												try:
													getdata = json.loads(postdata)
													for var, val in getdata.items():
														logging.debug('[main][request][' + method + '] var: ' + str(var) + ' val: ' + val)
														uri = uri + var + "=" + val + "&"
												except ValueError as e:
													logging.debug('[main][' + step_type + '] xmlpretty(postdata) ValueError: ' + str(e))													
												except Exception as e:
													logging.debug('[main][' + step_type + '] xmlpretty(postdata) ValueError: ' + str(e))																												
											try:
												resp = request("http://" + host_ip + ":" + host_port + uri,method,ContentType,XSender,authuser,authpass,postdata,auth)
												logging.debug('[main][' + step_type + '] request resp: ' + str(resp))
												if (resp == ""):
													printlog(log)
													fail = 1
													stepfail = 1
													assertsfailed += 1
													html_text += 'Assert ' + assername + ' ' + assertype + ' : '
													html_text += '<font color="red"><b>fail</b></font><br>'
													html_text += '\n'
													logging.error(
														'[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL responselog empty')
											except requests.ConnectionError as e:
												logging.debug('[main][' + step_type + '] request ConnectionError: ' + str(e))
												logging.debug('[main][' + step_type + '] request resp: ' + str(resp))
												fail=1
												stepfail=1
												assertsfailed += 1
												html_text += 'Assert request : '
												html_text += '<font color="red"><b>fail</b></font><br>'
												html_text += '\n'												
									if step.xpath('//asserts'):
										if (fail == 0):
											asserts = step.xpath('.//assert')
											assertscount = len(asserts)
											logging.debug('[main][' + step_type + '][assert] assertscount: ' + str(assertscount))
											for assertion in asserts:
												assertype = assertion.attrib.get("type")
												assername = assertion.attrib.get("name")
												if (assertype == "status_code"):
													logging.debug('[main][' + step_type + '][assert] assertdata: ' + str(assertion.text))
													logging.debug('[main][' + step_type + '][assert] response: ' + str(resp.status_code))
													if str(resp.status_code) == str(assertion.text):
														assertspassed += 1
														logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')	
													else:
														fail=1
														stepfail=1
														assertsfailed += 1 
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(assertion.text) + ' result: ' + str(resp.status_code))
														html_text += 'Assert '+ assername + ' ' + assertype + ' : '
														html_text += '<font color="red"><b>fail</b></font><br>'
														html_text += '\n'
												if (assertype == "response_data"):
													if (assertion.attrib.get("lang") == "json"):
														assertdata = assertion.text
														assertdata = cleardata(assertdata,"json")
														if usepool == 1:
															logging.debug('[main][' + step_name + '][' + step_type + '] usepool replacing')	
															logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)	
															assertdata = setPoolValue(pool, assertdata, 'expected')
															logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)	
														try:
															resppretty = jsonpretty(resp.text)
															assertpretty = jsonpretty(assertdata)													
															logging.debug('[main][' + step_type + '][assert] assertdata: ' + str(assertpretty))
															logging.debug('[main][' + step_type + '][assert] response: ' + str(resppretty))
															#if str(resppretty) == str(assertpretty):
															diff_result = diff(json.loads(resp.text), json.loads(assertdata))
															if (len(diff_result) == 0 or "ignore" in diff_result):
																assertspassed += 1
																logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')	
															else:
																fail=1
																stepfail=1														
																assertsfailed += 1
																html_text += 'Assert '+ assername + ' ' + assertype + ' : '
																html_text += '<font color="red"><b>fail</b></font><br>'
																html_text += '\n'
																logging.error(diff(json.loads(resp.text),json.loads(assertdata)))											
																logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(assertpretty))
																logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(resppretty))													
														except ValueError as e:
															logging.debug('[main][request] jsonpretty ValueError: ' + str(e))	
														except Exception as e:
															logging.debug('[main][request] jsonpretty ValueError: ' + str(e))
								if (step_type == "command"):
									logging.debug('[main][' + step_name + '][' + step_type + '] step_type start')
									for stepnode in step.getchildren():
										if (stepnode.tag == "data"):
											data = stepnode.text
											lang = stepnode.attrib.get("lang")
											logging.debug('[main][' + step_name + '][' + step_type + '] lang: ' + lang)
											r = '#{([a-zA-Z0-9_]+)}'
											reg_list = re.findall(r, data)
											logging.debug('[main][' + step_name + '][' + step_type + '] reg_list: ' + str(reg_list))
											reg_list = list(set(reg_list))
											for reg in reg_list:
												logging.debug('[main][' + step_name + '][' + step_type + '] reg: ' + str(reg))
												system = reg.split('_')[0]
												if (system == "locals"):
													config_value = locals()[reg.split('_')[1]]
													logging.debug('[main][' + step_name + '][' + step_type + '] locals()[reg]: ' + str(config_value))
												elif (system == "globals"):
													config_value = globals()[reg.split('_')[1]]
													logging.debug('[main][' + step_name + '][' + step_type + '] globals()[reg]: ' + str(config_value))
												else:
													config_value = getcaseconfig(reg)
												logging.debug('[main][' + step_name + '][' + step_type + '] config_value: ' + str(config_value))
												data = re.sub('#{' + reg + '}', config_value, data)
												logging.debug('[main][' + step_name + '][' + step_type + '] data: ' + str(data))
											if (lang == "python"):
												shell_code = "python -c '" + data + "'"
												ret = os.system(shell_code)	
											elif (lang == "shell"):
												shell_code = "sh -c '" + data + "'"
												#shell_code = data
												ret = os.system(shell_code)
											elif (lang == "shell_data"):
												#shell_code = "sh -c '" + data + "'"
												shell_code = data												
												ret = os.popen(shell_code).read().strip('\t\n')
											logging.debug('[main][' + step_name + '][' + step_type + '] shell_code: ' + str(shell_code))
											logging.debug('[main][' + step_name + '][' + step_type + '] ret: ' + str(ret))
									if step.xpath('//asserts'):
										asserts = step.xpath('.//assert')
										assertscount = len(asserts)
										for assertion in asserts:
											logging.debug('[main][' + step_type + '][asserts] assertspassed: ' + str(assertspassed))
											logging.debug('[main][' + step_type + '][asserts] assertsfailed: ' + str(assertsfailed))
											assertype = assertion.attrib.get("type")
											assername = assertion.attrib.get("name")
											assertdata = assertion.text
											logging.debug('[main][' + step_type + '][asserts] assertdata: ' + str(assertdata))
											if (assertype == "return_code"):
												logging.debug('[main][readlog][' + step_name + '][assertion] ret: ' + str(ret))
												if (str(ret) == ""):
													for servicelog in servicelogs:
														printlog(servicelog)
													fail=1
													stepfail=1													
													assertsfailed += 1											
													html_text += 'Assert '+ assername + ' ' + assertype + ' : '
													html_text += '<font color="red"><b>fail</b></font><br>'
													html_text += '\n'
													logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL ret empty')
												else:
													logging.debug('[main][' + step_type + '][' + step_name + '][assert] assertdata: ' + str(assertdata))
													logging.debug('[main][' + step_type + '][' + step_name + '][assert] ret: ' + str(ret))
													if str(ret) == str(assertdata):
														assertspassed += 1											
														logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')	
													else:
														fail=1
														stepfail=1															
														assertsfailed += 1											
														html_text += 'Assert '+ assername + ' ' + assertype + ' : '
														html_text += '<font color="red"><b>fail</b></font><br>'
														html_text += '\n'
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(assertdata))
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(ret))	
								if (step_type == "snmp"):
									logging.debug('[main][' + step_name + '][' + step_type + '] step_type start')
									logging.debug('[main][' + step_name + '][' + step_type + '] open traff')
									variable = step.attrib.get('variable')
									oid = step.attrib.get('oid')
									logging.debug('[main][' + step_name + '][' + step_type + '] variable: ' + str(variable))
									logging.debug('[main][' + step_name + '][' + step_type + '] oid: ' + str(oid))
									metrik_value = getSnmpMetric(oid)
									logging.debug('[main][' + step_name + '][' + step_type + '] metrik_value: ' + str(metrik_value))
									if (metrik_value == None):
										fail=1
										stepfail=1															
										logging.error('[' + testname + '][' + step_name + '][' + step_type + '] FAIL metrik_value: ' + str(metrik_value))
									else:
										logging.debug('[main][' + step_name + '][' + step_type + '] metrik_value: ' + str(metrik_value))
										if step.xpath('//asserts'):
											asserts = step.xpath('.//assert')
											assertscount = len(asserts)
											for assertion in asserts:
												logging.debug('[main][' + step_type + '][asserts] assertspassed: ' + str(assertspassed))
												logging.debug('[main][' + step_type + '][asserts] assertsfailed: ' + str(assertsfailed))
												assertype = assertion.attrib.get("type")
												assername = assertion.attrib.get("name")
												assertdata = assertion.text
												logging.debug('[main][' + step_type + '][asserts] assertdata: ' + str(assertdata))
												if (assertype == "evaluate"):
													if usepool == 1:
														logging.debug('[main][' + step_name + '][' + step_type + '] usepool replacing')	
														logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)	
														assertdata = setPoolValue(pool, assertdata, 'expected')
														logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)														
													patternconfig = re.compile(r'.*#{([a-zA-Z0-9_]+)}.*')
													logging.debug('[main][' + step_name + '][' + step_type + '] variable: ' +  str(variable))
													logging.debug('[main][' + step_name + '][' + step_type + '] variable: ' +  str(globals()[variable]))
													if (globals()[variable] == None):
														eval_res = ""
													else:
														if (patternconfig.match(assertdata)):
															assertdata = re.sub('#{' + variable + '}', globals()[variable], assertdata)
															logging.debug('[main][' + step_name + '][' + step_type + '] replace assertdata: ' + assertdata)
														logging.debug('[main][' + step_type + '][' + step_name + '][assert] assertdata: ' + str(assertdata))											
														try:
															eval_res = ne.evaluate(assertdata)
														except Exception as e:
															logging.error("exception: " + str(e))
															eval_res = ""
													logging.debug('[main][readlog][' + step_name + '][assertion] eval_res: ' + str(eval_res))
													if (str(eval_res) == ""):
														for servicelog in servicelogs:
															printlog(servicelog)
														fail=1
														stepfail=1													
														assertsfailed += 1											
														html_text += 'Assert '+ assername + ' ' + assertype + ' : '
														html_text += '<font color="red"><b>fail</b></font><br>'
														html_text += '\n'
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL eval_res empty')
													else:
														logging.debug('[main][' + step_type + '][' + step_name + '][assert] evalasssert: ' + str(eval_res))
														logging.debug('[main][' + step_type + '][' + step_name + '][assert] variable: ' + str(globals()[variable]))
														logging.debug('[main][' + step_type + '][' + step_name + '][assert] metrik_value: ' + str(metrik_value))
														if str(eval_res) == str(metrik_value):
															assertspassed += 1											
															logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')	
														else:
															fail=1
															stepfail=1															
															assertsfailed += 1											
															html_text += 'Assert '+ assername + ' ' + assertype + ' : '
															html_text += '<font color="red"><b>fail</b></font><br>'
															html_text += '\n'
															logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(eval_res))
															logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(globals()[variable]))
									globals()[variable] = metrik_value
								if (step_type == "readlog"):
									logging.debug('[main][' + step_name + '][' + step_type + '] start')
									if step.xpath('//asserts'):
										asserts = step.xpath('.//assert')
										assertscount = len(asserts)
										for assertion in asserts:
											assertype = assertion.attrib.get("type")
											assername = assertion.attrib.get("name")
											if (assertype == "log"):
												log = assertion.attrib.get('log')
												search_start = assertion.attrib.get('search_start')
												search_end = assertion.attrib.get('search_end')
												logging.debug('[main][' + step_name + '][' + step_type + '][assertion] search_start: ' + search_start)
												logging.debug('[main][' + step_name + '][' + step_type + '][assertion] search_end: ' + search_end)			
												pattern_start = re.compile(r'.*' + search_start + '.*')
												pattern_end = re.compile(r'.*' + search_end + '.*')
												responselog=""
												key=0
												with open(log, 'r') as logfile:
													lines = logfile.read().splitlines()
													for line in lines:
														#logging.debug('[main][' + step_type + '][' + step_name + '][assertion] logline: ' + line)
														if (key==1):
															responselog = responselog + line.strip('\t\n')											
														if pattern_start.match(line):
															responselog = responselog + line.strip('\t\n')
															if pattern_end.match(line):
																break
															key=1
														if (pattern_end.match(line) and key==1):
															break
												logging.debug('[main][' + step_type + '][' + step_name + '][assertion] log: ' + log)
												logging.debug('[main][' + step_type + '][' + step_name + '][assertion] key: ' + str(key))
												logging.debug('[main][' + step_type + '][' + step_name + '][assertion] responselog: "' + responselog + '"')
												if (assertion.attrib.get("lang") == "xml"):
													assertdata = assertion.text
													assertdata = cleardata(assertdata,"xml")
													responselog = cleardata(responselog,"xml")
													if usepool == 1:
														logging.debug('[main][' + step_name + '][' + step_type + '] usepool replacing')	
														logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)	
														assertdata = setPoolValue(pool, assertdata, 'expected')
														logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)	
													logging.debug('[main][' + step_type + '][' + step_name + '][assert] assertdata: ' + str(assertdata))
													logging.debug('[main][' + step_type + '][' + step_name + '][assert] responselog: ' + str(responselog))
													logging.debug('[main][' + step_type + '][' + step_name + '][assert] try pretty xml')
													if (responselog == ""):
														printlog(log)
														fail=1
														stepfail=1													
														assertsfailed += 1											
														html_text += 'Assert '+ assername + ' ' + assertype + ' : '
														html_text += '<font color="red"><b>fail</b></font><br>'
														html_text += '\n'
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL responselog empty')
													else:
														try:
															xmlresp = xmlpretty(responselog)
															xmlasssert = xmlpretty(assertdata)														
															logging.debug('[main][' + step_type + '][' + step_name + '][assert] xmlasssert: ' + str(xmlasssert))
															logging.debug('[main][' + step_type + '][' + step_name + '][assert] xmlresp: ' + str(xmlresp))
															if str(xmlasssert) == str(xmlresp):
																assertspassed += 1											
																logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')	
															else:
																fail=1
																stepfail=1															
																stepfail=1															
																assertsfailed += 1											
																dom1 = etree.fromstring(xmlasssert)
																dom2 = etree.fromstring(xmlresp)
																xml_compare(dom1, dom2, reporter=sys.stderr.write)
																html_text += 'Assert '+ assername + ' ' + assertype + ' : '
																html_text += '<font color="red"><b>fail</b></font><br>'
																html_text += '\n'
																logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(xmlasssert))
																logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(xmlresp))														
														except ValueError as e:
															logging.debug('[main][' + step_type + '] xmlpretty ValueError: ' + str(e))	
														except Exception as e:
															logging.debug('[main][' + step_type + '] xmlpretty ValueError: ' + str(e))													

												if (assertion.attrib.get("lang") == "json"):
													assertdata = assertion.text
													assertdata = cleardata(assertdata,"json")
													try:
														assertpretty = jsonpretty(assertdata)
														if usepool == 1:
															logging.debug('[main][' + step_name + '][' + step_type + '] usepool replacing')	
															logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)	
															assertdata = setPoolValue(pool, assertdata, 'expected')
															logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)															
														if (responselog == ""):
															printlog(log)
															fail=1
															stepfail=1														
															assertsfailed += 1				
															html_text += 'Assert '+ assername + ' ' + assertype + ' : '
															html_text += '<font color="red"><b>fail</b></font><br>'
															html_text += '\n'
															logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL responselog empty')
														else:
															try:
																assertdatapretty = jsonpretty(assertdata)
																resppretty = jsonpretty(responselog)
																logging.debug('[main][' + step_type + '][' + step_name + '][assert] assertpretty: ' + str(assertpretty))
																logging.debug('[main][' + step_type + '][' + step_name + '][assert] resppretty: ' + str(resppretty))											
																#if str(assertdatapretty) == str(resppretty):
																diff_result = diff(json.loads(responselog), json.loads(assertdata))
																if (len(diff_result) == 0 or "ignore" in diff_result):
																	assertspassed += 1
																	logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')
																else:
																	fail=1
																	stepfail=1																
																	assertsfailed += 1						
																	html_text += 'Assert '+ assername + ' ' + assertype + ' : '
																	html_text += '<font color="red"><b>fail</b></font><br>'
																	html_text += '\n'
																	logging.error(diff(json.loads(responselog),json.loads(assertdata)))
																	logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(assertdatapretty))
																	logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(resppretty))														
															except ValueError as e:
																logging.debug('[main][' + step_type + '] jsonpretty ValueError: ' + str(e))	
															except Exception as e:
																logging.debug('[main][' + step_type + '] jsonpretty ValueError: ' + str(e))															
													except ValueError as e:
														logging.debug('[main][' + step_type + '] jsonpretty ValueError: ' + str(e))	
													except Exception as e:
														logging.debug('[main][' + step_type + '] jsonpretty ValueError: ' + str(e))													

											if (assertype == "regexp"):
												assertdata = assertion.text
												if usepool == 1:
													logging.debug('[main][' + step_name + '][' + step_type + '] usepool replacing')	
													logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)	
													assertdata = setPoolValue(pool, assertdata, 'expected')
													logging.debug('[main][' + step_name + '][' + step_type + '] assertdata: ' +  assertdata)													
												log = assertion.attrib.get('log')
												search_start = assertion.attrib.get('search_start')
												search_end = assertion.attrib.get('search_end')
												regexp = assertion.attrib.get('regexp')
												logging.debug('[main][' + step_name + '][' + step_type + '][assertion] search_start: ' + search_start)
												logging.debug('[main][' + step_name + '][' + step_type + '][assertion] search_end: ' + search_end)			
												logging.debug('[main][' + step_name + '][' + step_type + '][assertion] regexp: ' + regexp)			
												pattern_start = re.compile(r'.*' + search_start + '.*')
												pattern_end = re.compile(r'.*' + search_end + '.*')
												responselog=""
												key=0
												with open(log, 'r') as logfile:
													for line in logfile:
														if (key==1):
															responselog = responselog + line.strip('\t\n')											
														if pattern_start.match(line):
															responselog = responselog+line.strip('\t\n')
															if pattern_end.match(line):
																break
															key=1
														if (pattern_end.match(line) and key==1):
															break
												logging.debug('[main][readlog][' + step_name + '][assertion] log: ' + log)
												logging.debug('[main][request][' + step_name + '][assert] responselog: ' + str(responselog))	
												if (responselog == ""):
													printlog(log)
													fail=1
													stepfail=1												
													assertsfailed += 1
													html_text += 'Assert '+ assername + ' ' + assertype + ' : '
													html_text += '<font color="red"><b>fail</b></font><br>'
													html_text += '\n'
													logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL responselog empty')
												else:
													pattern_regexp = re.compile(r'.*' + regexp + '.*')
													responsecode=pattern_regexp.match(responsecode).group(1) 
													logging.debug('[main][readlog][' + step_name + '][assertion] responsecode: ' + responsecode)
													if str(responsecode) == str(assertdata):
														assertspassed += 1											
														logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')
													else:
														fail=1
														stepfail=1													
														assertsfailed += 1
														html_text += 'Assert '+ assername + ' ' + assertype + ' : '
														html_text += '<font color="red"><b>fail</b></font><br>'
														html_text += '\n'
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: "' + str(assertdata) + '"')
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: "' + str(responsecode) + '"')										
								if (step_type == "tshark"):
									#step with tshark dump traffic
									logging.debug('[main][' + step_name + '][' + step_type + '] step_type start')
									logging.debug('[main][' + step_name + '][' + step_type + '] open traff')
									searchstring = step.attrib.get('search')
									if step.xpath('//asserts'):
										asserts = step.xpath('.//assert')
										assertscount = len(asserts)
										for assertion in asserts:
											logging.debug('[main][' + step_type + '][asserts] assertspassed: ' + str(assertspassed))
											logging.debug('[main][' + step_type + '][asserts] assertsfailed: ' + str(assertsfailed))
											assertype = assertion.attrib.get("type")
											assername = assertion.attrib.get("name")
											if (assertype == "tshark"):
												try:
													if (assername == "request" or assername == "response"):
														responselog=getdump("http_file_data",searchstring)
													elif (assername == "status_code"):
														responselog=getdump("http_response_code",searchstring)
													elif (assername == "content_type"):
														responselog=getdump("http_content_type",searchstring)
												except TypeError as e:
													logging.error("exception: " + str(e))
													responselog=""
												logging.debug('[main][readlog][' + step_name + '][assertion] responselog: "' + responselog + '"')
												if (assertion.attrib.get("lang") == "xml"):
													#assert with xml
													assertdata = assertion.text
													assertdata = cleardata(assertdata,"xml")
													logging.debug('[main][readlog][' + step_name + '][assertion] assertdata: "' + str(assertdata) + '"')
													if (str(responselog) == ""):
														if (str(assertdata) == ""):
															#check empty assert
															logging.debug('[main][request][' + step_name + '][assert] empty responselog: "' + str(responselog) + '"')
															logging.debug('[main][request][' + step_name + '][assert] empty assertdata: "' + str(assertdata) + '"')
															assertspassed += 1											
															logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')														
														else:
															for servicelog in servicelogs:
																printlog(servicelog)
															fail=1
															stepfail=1													
															assertsfailed += 1											
															html_text += 'Assert '+ assername + ' ' + assertype + ' : '
															html_text += '<font color="red"><b>fail</b></font><br>'
															html_text += '\n'
															logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL responselog empty')
													else:		
														#check not empty assert
														responselog = cleardata(responselog,"xml")
														if usepool == 1:
															logging.debug('[main][' + step_name + '][request] usepool replacing')	
															logging.debug('[main][' + step_name + '][request] assertdata: ' +  assertdata)	
															assertdata = setPoolValue(pool, assertdata, 'expected')
															logging.debug('[main][' + step_name + '][request] assertdata: ' +  assertdata)														
														logging.debug('[main][request][' + step_name + '][assert] assertdata: ' + str(assertdata))
														logging.debug('[main][request][' + step_name + '][assert] responselog: ' + str(responselog))
														logging.debug('[main][request][' + step_name + '][assert] try pretty xml')
														try:
															xmlasssert = xmlpretty(assertdata)
															xmlresp = xmlpretty(responselog)
															logging.debug('[main][request][' + step_name + '][assert] xmlasssert: ' + str(xmlasssert))
															logging.debug('[main][request][' + step_name + '][assert] xmlresp: ' + str(xmlresp))
															if str(xmlasssert) == str(xmlresp):
																assertspassed += 1											
																logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')	
															else:
																fail=1
																stepfail=1															
																assertsfailed += 1											
																dom1 = etree.fromstring(xmlasssert)
																dom2 = etree.fromstring(xmlresp)
																xml_compare(dom1, dom2, reporter=sys.stderr.write)
																html_text += 'Assert '+ assername + ' ' + assertype + ' : '
																html_text += '<font color="red"><b>fail</b></font><br>'
																html_text += '\n'
																logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(xmlasssert))
																logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(xmlresp))
														except ValueError as e:
															logging.debug('[main][request] xmlpretty ValueError: ' + str(e))	
														except Exception as e:
															logging.debug('[main][request] xmlpretty ValueError: ' + str(e))
												elif (assertion.attrib.get("lang") == "json"):
													##assert with json
													assertdata = assertion.text
													assertdata = cleardata(assertdata,"json")
													logging.debug('[main][readlog][' + step_name + '][assertion] assertdata: "' + str(assertdata) + '"')													
													if (str(responselog) == ""):
														if (str(assertdata) == ""):
															#check empty assert
															logging.debug('[main][request][' + step_name + '][assert] empty responselog: "' + str(responselog) + '"')
															logging.debug('[main][request][' + step_name + '][assert] empty assertdata: "' + str(assertdata) + '"')
															assertspassed += 1											
															logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')														
														else:
															for servicelog in servicelogs:
																printlog(servicelog)
															fail=1
															stepfail=1														
															assertsfailed += 1		
															html_text += 'Assert '+ assername + ' ' + assertype + ' : '
															html_text += '<font color="red"><b>fail</b></font><br>'
															html_text += '\n'
															logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL responselog empty')
													else:
														#check not empty assert
														try:
															assertpretty = jsonpretty(assertdata)
															if usepool == 1:
																logging.debug('[main][' + step_name + '][request] usepool replacing')	
																logging.debug('[main][' + step_name + '][request] assertdata: ' +  assertdata)	
																assertdata = setPoolValue(pool, assertdata, 'expected')
																logging.debug('[main][' + step_name + '][request] assertdata: ' +  assertdata)															
															try:
																assertdatapretty = jsonpretty(assertdata)
																resppretty = jsonpretty(responselog)
																logging.debug('[main][request][' + step_name + '][assert] assertpretty: ' + str(assertpretty))
																logging.debug('[main][request][' + step_name + '][assert] resppretty: ' + str(resppretty))											
																#if str(assertdatapretty) == str(resppretty):
																diff_result = diff(json.loads(responselog), json.loads(assertdata))
																logging.debug('[main][request][' + step_name + '] diff_result: ' + str(diff_result))
																if (len(diff_result) == 0 or "ignore" in str(diff_result)):
																	assertspassed += 1											
																	logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')
																else:
																	fail=1
																	stepfail=1																
																	assertsfailed += 1	
																	html_text += 'Assert '+ assername + ' ' + assertype + ' : '
																	html_text += '<font color="red"><b>fail</b></font><br>'
																	html_text += '\n'
																	logging.error(diff(json.loads(responselog),json.loads(assertdata)))
																	logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(assertdatapretty))
																	logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(resppretty))																	
															except ValueError as e:
																logging.debug('[main][request] jsonpretty ValueError: ' + str(e))
																fail = 1
																stepfail = 1
																assertsfailed += 1
																html_text += 'Assert ' + assername + ' ' + assertype + ' : '
																html_text += '<font color="red"><b>fail</b></font><br>'
																html_text += '\n'
																assert_fail(assertsfailed, html_text, assername, assertype, testname, step_name, step_type, responselog, assertdata)
															except Exception as e:
																logging.debug('[main][request] jsonpretty(responselog) ValueError: ' + str(e))
																fail = 1
																stepfail = 1
																assertsfailed += 1
																html_text += 'Assert ' + assername + ' ' + assertype + ' : '
																html_text += '<font color="red"><b>fail</b></font><br>'
																html_text += '\n'
																assert_fail(assertsfailed, html_text, assername,
																			assertype, testname, step_name, step_type,
																			responselog, assertdata)
														except ValueError as e:
															logging.debug('[main][request] jsonpretty(assertdata) ValueError: ' + str(e))
															fail = 1
															stepfail = 1
															assertsfailed += 1
															html_text += 'Assert ' + assername + ' ' + assertype + ' : '
															html_text += '<font color="red"><b>fail</b></font><br>'
															html_text += '\n'
															assert_fail(assertsfailed, html_text, assername, assertype,
																		testname, step_name, step_type, responselog,
																		assertdata)
														except Exception as e:
															logging.debug('[main][request] jsonpretty(assertdata) ValueError: ' + str(e))
															fail = 1
															stepfail = 1
															assertsfailed += 1
															html_text += 'Assert ' + assername + ' ' + assertype + ' : '
															html_text += '<font color="red"><b>fail</b></font><br>'
															html_text += '\n'
															assert_fail(assertsfailed, html_text, assername, assertype,
																		testname, step_name, step_type, responselog,
																		assertdata)

												else:
													assertdata = assertion.text
													if str(responselog) == str(assertdata):
														assertspassed += 1											
														logging.info('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] PASS')
													else:
														fail=1
														stepfail=1													
														assertsfailed += 1		
														html_text += 'Assert '+ assername + ' ' + assertype + ' : '
														html_text += '<font color="red"><b>fail</b></font><br>'
														html_text += '\n'
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(assertdata))
														logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(responselog))
									if fail==1:
										copylog(tshark_file, case_dir, case, 'pcap')
							else:
								logging.debug('[main] step_type: ' + str(step_type) + " disabled")
							logging.debug('[main] html_text: ' + str(html_text))
							logging.debug('[main] html_text_all: ' + str(html_text_all))
							if (stepfail == 1):
								stepsfailed += 1
								html_text_all += ' <td>Step '+ step_name + '</td><td>' + html_text + '</td></tr>'
							logging.debug('[main] assertspassed: ' + str(assertspassed))
							logging.debug('[main] assertsfailed: ' + str(assertsfailed))
							logging.debug('[main] step end ########################################################################################')								
						if fail==1:
							print "Test " + testname + " failed"
							logging.debug('[main] stepsfailed: ' + str(stepsfailed))
							failed += 1
							for servicelog in servicelogs:
								copylog(servicelog, case_dir, case, 'log')
							if usepool == 1:
								html.log('<tr><td rowspan="' + str(stepsfailed) + '">Test <b>' + testname + '</b><br>' + case_dir + '<br>' + 'pool_value: ' + plvalue + '</td>')	
							else:
								html.log('<tr><td rowspan="' + str(stepsfailed) + '">Test <b>' + testname + '</b><br>' + case_dir + '</td>')						
							#if (stepsfailed > 1):
								#html.log("<tr>")	
								#html_text = re.sub(' <td>Step', ' <tr><td>Step', html_text)												
							html.log(html_text_all)
						else:
							print "Test " + testname + " passed" 
							if usepool == 1:
								html.log('<tr><td rowspan="1">Test <b>' + testname + '</b><br>' + case_dir + '<br>' + 'pool_value: ' + plvalue + '</td>')	
							else:
								html.log('<tr><td rowspan="1">Test <b>' + testname + '</b><br>' + case_dir + '</td>')					
							html.log('<td>Steps ' + str(stepsscount) + '</td><td>Asserts ' + str(assertspassed) + ' <font color="green"><b>pass</b></font><br></td></tr>')
							passed += 1
						total_assertsfailed += assertsfailed
						total_assertspassed += assertspassed


	html.log('</table><br>')
	html.log('<br>Tests:  <b>' + str(tests) + '</b>')
	html.log('<br>Passed:  <b>' + str(passed) + '</b>')
	html.log('<br>Failed:  <b>' + str(failed) + '</b>')
	html.log('<br>Asserts passed:  <b>' + str(total_assertspassed) + '</b>')
	html.log('<br>Asserts failed:  <b>' + str(total_assertsfailed) + '</b>')
	html.end()
	logging.info('[main] Tests: ' + str(tests))
	logging.info('[main] Passed: ' + str(passed))
	logging.info('[main] Failed: ' + str(failed))
	logging.info('[main] Asserts passed: ' + str(total_assertspassed))
	logging.info('[main] Asserts failed: ' + str(total_assertsfailed))
	reportj.log('Tests: ' + str(tests))
	reportj.log('Passed: ' + str(passed))
	reportj.log('Failed: ' + str(failed))
	reportj.log('Asserts passed: ' + str(total_assertspassed))
	reportj.log('Asserts failed: ' + str(total_assertsfailed))
	reportj.end()
#if __name__ == "__main__":
#    sys.exit(main())
	

def assert_fail(assertsfailed, html_text, assername, assertype, testname, step_name, step_type, responselog, assertdata):
	fail = 1
	stepfail = 1
	assertsfailed += 1
	html_text += 'Assert ' + assername + ' ' + assertype + ' : '
	html_text += '<font color="red"><b>fail</b></font><br>'
	html_text += '\n'
	logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL expected: ' + str(assertdata))
	logging.error('[' + testname + '][' + step_name + '][' + step_type + '][' + assername + '][' + assertype + '] FAIL result: ' + str(responselog))

if (len(sys.argv) == 3):
	testdir = sys.argv[1]
	key = sys.argv[2]

	config = ConfigParser()
	configfile=testdir + '/config.ini'
	config.read(configfile)
	cases_path = config.get('testing', 'path')
	actionfile = config.get('testing', 'actionfile')
	htmlfile = testdir + "/" + config.get('testing', 'htmlfile')
	reportfile = testdir + "/" + config.get('testing', 'reportfile')
	logpath = config.get('testing', 'logpath')		
	host = config.get('deb', 'host')
	port = config.get('deb', 'port')
	servicelogs = ast.literal_eval(config.get('deb', 'servicelog'))
	binfolder = testdir
	logname = testdir + "/" + config.get('testing', 'log')
	errorlog = testdir + "/" + config.get('testing', 'errorlog')
	tshark_ports_count = config.get('tshark', 'ports')
	tshark_file = testdir + "/" + config.get('tshark', 'file')
	tshark_duration = config.get('tshark', 'duration')
	
	if (key == "forcestdout"):
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
	elif (key == "forcelog"):
		logging.basicConfig(filename=logname, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
		#logging.basicConfig(filename=errorlog, level=logging.ERROR, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
	elif (key == "stdout"):
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
	elif (key == "log"):
		logging.basicConfig(filename=logname, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
		#logging.basicConfig(filename=errorlog, level=logging.ERROR, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
	
	sys.exit(main())
else:
	print "Incorrect usage"


