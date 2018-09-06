#!/usr/bin/python
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0
import os
import re
import glob
import logging
import subprocess
import sys
import socket
import time
from lxml import etree
import lxml.etree
import requests, base64
import pprint
import json
from xml_diff import compare
from jsondiff import diff
import shutil
import os
import time
import reverse
import json, ast
from random import choice
from string import digits
import string
import random
from collections import OrderedDict
from sh import tail
import ast

def update_config(configfile, section, system, value):
	value = json.dumps(value)
	logging.debug('update_config: ' + str(configfile) + " section: " + str(section) + " system: " + str(system) + " value: " + str(value))
	config.read(configfile)
	#cfgfile = open(configfile, 'w')
	config.set(section, system, str(value))
	with open(configfile, 'w') as configf:
		config.write(configf)
	#cfgfile.write(config)
	#cfgfile.close()

def checkfile(logfile,string):
	while True:
		file = open(logfile,'r')
		lines = file.readlines()
		pattern = re.compile(r'.*' + string + '.*')
		for line in lines:
			if pattern.match(line):
				return True
		time.sleep(1)
		file.close()

def tails():
	for servicelog in servicelogs:
		for line in tail("-50", servicelog, _iter=True):
			logging.info("log line: " + str(line))
	#file = open("tail -20 " + servicelog,'r')
	#lines = file.readlines()
	#for line in lines:
	#	logging.info("log line: " + str(line))		
	#file.close()
	
		
def checklog(logfile,string):
	file = open(logfile,'r')
	lines = file.readlines()
	pattern = re.compile(r'.*' + string + '.*')
	key=0
	for line in lines:
		if pattern.match(line):
			key=1
			return True
	if (key == 0):
		return False
	else:
		return True
	file.close()
	
testdir = ""	
key = ""	
stub_fail = 0


if (len(sys.argv) == 3):
	key = sys.argv[2]
	testdir = sys.argv[1]
	os.system("rm -rf " + testdir + "/logs/*")		
	config = ConfigParser()
	configfile=testdir + '/config.ini'
	config.read(configfile)
	output = config.get('deb', 'output')
	deb_path = config.get('deb', 'path')
	sleep = config.get('deb', 'sleep')
	packages = config.get('deb', 'packages')
	host = config.get('deb', 'host')
	port = config.get('deb', 'port')
	logname = testdir + "/" + config.get('deb', 'log')
	servicelogs = ast.literal_eval(config.get('deb', 'servicelog'))
	servicenames = ast.literal_eval(config.get('deb', 'servicename'))
	server_conf_location = config.get('deb', 'server_conf_location')
	server_confs = ast.literal_eval(config.get('deb', 'server_conf'))
	scripts_path = testdir + "/" + config.get('testing', 'scripts')
	testing = config.get('testing', 'testing')
	casing = config.get('testing', 'casing')
	install_deb = config.get('testing', 'install_deb')
	mock_type = config.get('testing', 'mock_type')
	mock_count = config.get('testing', 'mock_count')
	mailing = config.get('testing', 'mailing')
	mail_subject = config.get('testing', 'mail_subject')
	logpath = testdir + "/" + config.get('testing', 'logpath')
	reportfile = testdir + "/" + config.get('testing', 'reportfile')
	binfolder = "./"
	
	os.system("mkdir " + logpath)
	os.system("mkdir " + logpath + " >> " + logname + " 2>&1")

	if (key == "forcestdout"):
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
	elif (key == "stdout"):
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
	elif (key == "log"):
		logging.basicConfig(filename=logname, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')
	elif (key == "forcelog"):
		logging.basicConfig(filename=logname, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [%(lineno)d] - %(message)s')

	
	logging.debug('deb_path: ' + deb_path)	
	logging.debug('scripts_path: ' + scripts_path)	
	logging.debug('sleep: ' + sleep)	
	logging.debug('package: ' + str(packages))
	logging.debug('host: ' + host)
	logging.debug('port: ' + port)
	packages_json = json.loads(packages)
	servicename_json = json.loads(packages)
	package_new=""

	if (install_deb == "true"):
		os.system("ls " + deb_path + " >> " + logname + " 2>&1")
	if (key == "force" or key == "forcestdout" or key == "forcelog"):
		if (testing == "true"):
			if (install_deb == "true"):
				for package_filter, package_data in packages_json.items():
					logging.debug("package_filter: " + str(package_filter) + " package_data: " + package_data)			
					files = glob.glob(deb_path + "/*" + package_filter + "*.deb")   
					files.sort(key=os.path.getmtime,reverse=True)
					for f in files:
						logging.debug("file in dir: " + str(f))
					package_new = files[0]
					logging.debug("filter file package_new: " + str(package_new))
					dpkg = "sudo dpkg -i " + str(package_new) + " >> " + logname + " 2>&1"
					logging.info('install command: ' + dpkg)						
					inst = os.system(dpkg)
					logging.info('install res: ' + str(inst))
					packages_json[package_filter]=package_new
				update_config(configfile, 'deb', 'packages', packages_json)
			else:
				logging.info('install disabled')		
				inst=0
			logging.info("install deb: " + str(inst))	
			if (inst != 0 and inst != 2):
				logging.error("install failed")
				for servicename in servicenames:
					os.system("echo 'install failed' > " + testdir + "/logs/report.html")
					os.system("sudo systemctl status " + servicename + " >> " + logname + " 2>&1")
					for servicelog in servicelogs:
						os.system("echo '#################### servicelog ########################'")
						os.system("tail -20 " + servicelog)
					os.system("echo '#################### servicelog ########################'")
					os.system("echo '#################### logname ########################'")
					os.system("tail -20 " + logname)
					os.system("echo '#################### logname ########################'")
					raise Exception("Script failed: install failed")
				#os.system(testdir + "/mail_report.py " + logname + " install_failed >> " + logname + " 2>&1")
			else:           
				logging.info("install passed")
				logging.info("copy config")
				for server_cnf in server_confs:
					run = os.system("cp -rf  " + testdir + "/" + server_cnf + " " + server_conf_location + " >> " + logname + " 2>&1")
					logging.debug("cp -rf  " + testdir + "/" + server_cnf + " " + server_conf_location + " >> " + logname + " 2>&1 run: " + str(run))
				logging.info("restart service")
				server_run = True
				for servicename in servicenames:
					run = os.system("sudo systemctl restart " + servicename + " >> " + logname + " 2>&1")
					logging.info(str(servicename) + " run: " + str(run))
					if (run != 0):
						logging.error("server run failed")
						for servicename in servicenames:
							os.system("echo 'server run failed' > " + testdir + "/logs/report.html")
							os.system("sudo systemctl status " + servicename + " >> " + logname + " 2>&1")
							for servicelog in servicelogs:
								os.system("echo '#################### servicelog ########################'")
								os.system("tail -20 " + servicelog)
							os.system("echo '#################### servicelog ########################'")
							os.system("echo '#################### logname ########################'")
							os.system("tail -20 " + logname)
							os.system("echo '#################### logname ########################'")
							raise Exception("Script failed: server run failed")
							#os.system(testdir + "/mail_report.py " + logname + " run_failed >> " + logname + " 2>&1")
							server_run = False
				if (server_run is False):
					logging.error("server run failed")
				else:
					time.sleep(float(1))
					logging.info("check port")
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					result = sock.connect_ex((host,int(port)))
					logging.info("check port result: " + str(result))
					if (result == 0):
						if (mock_type == "web_mock"):
							for cnt in range(1,int(mock_count)+1):
								logging.info("kill and start port cnt: " + str(cnt))
								stub_port = config.get('testing', 'mock_bin' + str(cnt) + '_port')
								stub_search = config.get('testing', 'mock_bin' + str(cnt) + '_search')
								stub_path = config.get('testing', 'mock_bin' + str(cnt) + '_path')
								logging.info("stub_port: " + str(stub_port))
								logging.info("kill temp mock")
								kill_cmd="kill -9 `ps -Aef | awk '{if ($9 ~ /" + stub_search + "/) print $2; if ($8 ~ /" + stub_search + "/) print $2}'` >> " + logname + " 2>&1"
								logging.info("kill_cmd: " + str(kill_cmd))
								kill1=os.system(kill_cmd)
								logging.info("kill1 temp mock: " + str(kill1))
								logging.info("start mocks")
								start_cmd = testdir + "/" + stub_path + " " + testdir + " false >> " + logname + " 2>&1 &"
								#mock1_res = os.system(testdir + "/web/server_gmlc.py " + testdir + " false false >> " + logname + " 2>&1 &")
								logging.info("start_cmd: " + str(start_cmd))
								mock1_res = os.system(start_cmd)
								logging.info("mock1_res: " + str(mock1_res))
						if (mock_type == "soapui"):
							soapui_project = config.get('mock', 'soapui_project')
							soapui_mock_runner = config.get('mock', 'soapui_mock_runner')
							stub1 = config.get('mock', 'stub1')
							stub2 = config.get('mock', 'stub2')
							stub1_port = config.get('mock', 'stub1_port')
							stub2_port = config.get('mock', 'stub2_port')
							logging.info("kill temp mock")
							kill1=os.system("kill -9 `ps -Aef | awk '{if ($9 ~ /server_gmlc/) print $2; if ($8 ~ /server_gmlc/) print $2}'` >> " + logname + " 2>&1")
							kill2=os.system("kill -9 `ps -Aef | awk '{if ($9 ~ /server_sodmtd/) print $2; if ($8 ~ /server_sodmtd/) print $2}'` >> " + logname + " 2>&1")
							kill3=os.system("kill -9 `ps -Aef | awk '{if ($9 ~ /soapui_gmlcgw/) print $2; if ($8 ~ /soapui_gmlcgw/) print $2}'` >> " + logname + " 2>&1")
							logging.info("kill1 temp mock: " + str(kill1))
							logging.info("kill2 temp mock: " + str(kill2))
							logging.info("kill3 temp mock: " + str(kill3))							
							logging.info("start mocks: " + soapui_mock_runner + " -m " + stub1 + " " + soapui_project + " >> " + logname + " 2>&1 &")
							mock1_res = os.system(soapui_mock_runner + " -m " + stub1  + " " + soapui_project + " >> " + logname + " 2>&1 &")
							logging.info("wait for start Stub 1")
							checkfile(logname, "Started mockService \[REST MockService GMLC\]")
							logging.info("Stub 1 started")
							logging.info("start mocks: " + soapui_mock_runner + " -m " + stub2 + " " + soapui_project + " >> " + logname + " 2>&1 &")					
							mock2_res = os.system(soapui_mock_runner + " -m " + stub2  + " " + soapui_project + " >> " + logname + " 2>&1 &")
							logging.info("wait for start mock 2")
							checkfile(logname, "Started mockService \[REST MockService SODMTD\]")					
							logging.info("Stub 2 started")
							logging.info("mock1_res: " + str(mock1_res))
						elif (mock_type == "manual"):
							mock1_res = 0
						if (mock1_res == 0):
							if (mock_type == "manual"):
								stub_fail = 0
							else:
								for cnt in range(1,int(mock_count)+1):
									logging.info("check port cnt: " + str(cnt))
									stub_port = config.get('testing', 'mock_bin' + str(cnt) + '_port')
									stub_search = config.get('testing', 'mock_bin' + str(cnt) + '_search')
									stub_path = config.get('testing', 'mock_bin' + str(cnt) + '_path')							
									logging.info("check stub ports host: " + host + " stub1: " + str(stub_port))
									sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
									result1 = sock.connect_ex((host,int(stub_port)))
									logging.info("stub1 result1: " + str(result1))	
									if (result1 != 0 and result1 != 106):
										logging.info("stub1 result1: " + str(result1))	
										stub_fail = 1
										for servicelog in servicelogs:
											os.system("echo '#################### servicelog ########################'")
											os.system("tail -20 " + servicelog)
										os.system("echo '#################### servicelog ########################'")
										os.system("echo '#################### logname ########################'")
										os.system("tail -20 " + logname)
										os.system("echo '#################### logname ########################'")									
							if (stub_fail == 0):
								if (casing == "true"):
									logging.info("run testing: " + binfolder + "/cases.py " + scripts_path + " >> " + logname + " 2>&1")
									if (key == "forcestdout"):
										os.system(binfolder + "/cases.py " + scripts_path + " " + key)
									else:
										os.system(binfolder + "/cases.py " + scripts_path + " " + key + " >> " + logname + " 2>&1")
									if (os.path.exists(testdir + "/logs/report.html") == False):
										os.system("echo 'fail testing' > " + testdir + "/logs/report.html")	
									if (mock_type != "manual"):
										logging.info("stopping mock")
										kill1=os.system("kill -9 `ps -Aef | awk '{if ($9 ~ /server_gmlc/) print $2; if ($8 ~ /server_gmlc/) print $2}'` >> " + logname + " 2>&1")
										kill2=os.system("kill -9 `ps -Aef | awk '{if ($9 ~ /server_sodmtd/) print $2; if ($8 ~ /server_sodmtd/) print $2}'` >> " + logname + " 2>&1")
										kill3=os.system("kill -9 `ps -Aef | awk '{if ($9 ~ /soapui_gmlcgw/) print $2; if ($8 ~ /soapui_gmlcgw/) print $2}'` >> " + logname + " 2>&1")
										logging.info("kill1 temp mock: " + str(kill1))
										logging.info("kill2 temp mock: " + str(kill2))
										logging.info("kill3 temp mock: " + str(kill3))
									logging.info("reporting")	
									#os.system(testdir + "/mail_report.py " + testdir + "/logs/report.html " + package_new + " >> " + logname + " 2>&1")		   
							else:
								logging.info("stubs port check fail")	
								os.system("echo 'stubs port check fail' > " + testdir + "/logs/report.html")
								for servicelog in servicelogs:
									os.system("echo '#################### servicelog ########################'")
									os.system("tail -20 " + servicelog)
								os.system("echo '#################### servicelog ########################'")
								os.system("echo '#################### logname ########################'")
								os.system("tail -20 " + logname)
								os.system("echo '#################### logname ########################'")								
								raise Exception("Script failed: stubs port check fail")
						else:
							logging.error("fail start mock")
							os.system("echo 'fail start mock' > " + testdir + "/logs/report.html")
							for servicelog in servicelogs:
								os.system("echo '#################### servicelog ########################'")
								os.system("tail -20 " + servicelog)
							os.system("echo '#################### servicelog ########################'")
							os.system("echo '#################### logname ########################'")
							os.system("tail -20 " + logname)
							os.system("echo '#################### logname ########################'")							
							raise Exception("Script failed: fail start mock")
							#os.system(testdir + "/mail_report.py " + logname + " fail_start_mock >> " + logname + " 2>&1")					
					else:
						logging.error("port not listening host: " + host + " port: " + str(port))
						os.system("echo 'port not listening' > " + testdir + "/logs/report.html")
						os.system("echo 'fail start mock' > " + testdir + "/logs/report.html")
						os.system("echo '#################### servicelog ########################'")
						#os.system("tail -20 " + servicelog)
						tails()
						os.system("echo '#################### servicelog ########################'")
						os.system("echo '#################### logname ########################'")
						os.system("tail -20 " + logname)
						os.system("echo '#################### logname ########################'")							
						raise Exception("Script failed: port not listening host: " + host + " port: " + str(port))
						#os.system(testdir + "/mail_report.py " + logname + " port_not_listen >> " + logname + " 2>&1")
			if os.path.exists(testdir + "/logs/report.html"):
				if (checklog(testdir + "/logs/report.html", "Failed:  <b>0</b>")):
					print "Test Passed"
					test_result = "Passed"
					if os.path.exists(reportfile):
						with open(reportfile,'r') as f:
							reportf = f.read().splitlines()				
							print reportf				
					if (mailing == "true"):
						os.system(binfolder + "/mail_report.py " + testdir + "/logs/report.html " + mail_subject + " " + package_new + " " + test_result + " >> " + logname + " 2>&1")							
				else:
					print "Test Failed"
					test_result = "Failed"
					if os.path.exists(reportfile):
						with open(reportfile,'r') as f:
							reportf = f.read().splitlines()				
							print reportf
					if (mailing == "true"):
						os.system(binfolder + "/mail_report.py " + testdir + "/logs/report.html " + mail_subject + " " + package_new + " " + test_result + " >> " + logname + " 2>&1")						
					for servicelog in servicelogs:
						os.system("echo '#################### servicelog ########################'")
						os.system("tail -20 " + servicelog)
					os.system("echo '#################### servicelog ########################'")
					os.system("echo '#################### logname ########################'")
					os.system("tail -20 " + logname)
					os.system("echo '#################### logname ########################'")						
					raise Exception("Script failed")
	else:
		logging.info('package not updated')	
else:
	print ("Usage start.py <testdir> <loglevel>")
	print ("testdir:")
	print ("  /home/core/tests #directory with scripts")
	print ("loglevel:")
	print ("  forcestdout #force testing without check new deb, log to stdout")
	print ("  stdout #log to stdout")
	print ("  log #log to file")

