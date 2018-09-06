import logging
import os
import sys
import pytest
import allure
#import zc.zk
import lxml.etree
import requests, base64
import pprint
import json
import xmldiff
from xml_diff import compare
from jsondiff import diff
import re
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.base_matcher import BaseMatcher
import base64
import avro as avro2
import io
import collections
from fastavro import schemaless_reader
import struct
#from bson import json_util
import datetime
import time
import calendar
from hamcrest import *
import random

log = logging.getLogger('nistest.basic.CompareDriver')

class Ignore(object):
        def __init__(self, data, lang):
            if (lang == 'json'):
                try:
                    #data = json.loads(data)
                    self.data = json.dumps(data, indent=4, sort_keys=True)
                    self.lang = lang
                except ValueError as e:
                    logging.error("[Ignore][init] jsonpretty fail jsonpretty: " + str(data))
                    logging.error("[Ignore][init] exception: " + str(e))


class CompareDriver(object):

    '''

    Compare driver class

    Some compare functions

    '''

    def __init__(self, data_result, data_expected, lang, dump=False, ignore_data=False):
        #self.data_result = self.cleardata(data_result, lang)
        #self.data_expected = self.cleardata(data_expected, lang)
        if (ignore_data is not False):
            ignore_data = Ignore(ignore_data,lang)
            logging.debug('[CompareDriver] ignore_data: ' + str(ignore_data.data))
            logging.debug('[CompareDriver] ignore_lang: ' + str(ignore_data.lang))

        self.data_result = data_result
        self.data_expected = data_expected
        self.pretty_expected = self.toPretty(self.data_expected, lang, dump)
        self.pretty_result = self.toPretty(self.data_result, lang, dump)
        self.lang = lang
        logging.debug('[CompareDriver] pretty_expected: ' + str(self.pretty_expected))
        logging.debug('[CompareDriver] pretty_result: ' + str(self.pretty_result))
        logging.debug('[CompareDriver] lang: ' + str(self.lang))

        if (lang == 'xml'):
            self.xml_comparer(ignore_data)
        elif (lang == 'json'):
            self.json_comparer(ignore_data)

    def xml_comparer(self, ignore):
        logging.debug('[CompareDriver][xml_comparer] start')
        dom1 = lxml.etree.fromstring(self.pretty_expected)
        dom2 = lxml.etree.fromstring(self.pretty_result)
        if (str(self.pretty_expected) == str(self.pretty_result)):
            assert True
        else:
            assert str(self.pretty_expected) == str(self.pretty_result), "\r\n result: " + self.pretty_result + "\r\n must be: " + str(self.pretty_expected)

        #logging.debug('[xml_comparer] diff_result: ' + str(diff_result))
        #assert diff_result
        #assert self.xml_compare(dom1, dom2, reporter=sys.stderr.write)
        #assert self.text_compare("test", "test2", False, False)
        #return True

    def json_comparer(self, ignore_data):
        logging.debug('[CompareDriver][json_comparer] start')
        diff_result = diff(json.loads(self.pretty_result),json.loads(self.pretty_expected))
        logging.debug('[CompareDriver][json_comparer] diff_result: ' + str(diff_result))
        if len(diff_result) == 0:
            return True
        else:
            if (ignore_data is not False):
                diff_result = self.toPretty(diff_result, self.lang, False)
                if (ignore_data.data == diff_result):
                   diff_result = 0
                   logging.debug('[CompareDriver][json_comparer] ignore diff_result: ' + str(diff_result))
                else:
                    logging.debug('[CompareDriver][json_comparer] ignore != diff_result, ignore_data.dat : ' + str(ignore_data.data) + ' diff_result: ' + str(diff_result))

            assert diff_result == 0, str(diff_result) + "\r\n result: " + self.pretty_result + "\r\n must be: " + str(self.pretty_expected)

    def cleardata(self, txt, type):
        try:
            if (str(txt) == "None"):
                txt = ""
            elif (type == "xml"):
                txt = re.sub("^\s+|\s+$", '', txt)
                txt = re.sub(">\s+<|>\n<|>\r<", '><', txt)
            elif (type == "json"):
                # txt = re.sub("^\s+|\s+$|\n|\r", '', txt)
                txt = re.sub("|\n|\r", '', txt)
        except UnicodeEncodeError as e:
            logging.debug('[CompareDriver][cleardata] e: ' + str(e))

        return txt

    def getNodePath(self, node):
        return node.getroottree().getpath(node)

    def doReport(self, reporter, x1, x2, errorMsg):
        # if reporter:
        # reporter(getNodePath(x1)+" "+getNodePath(x2)+os.linesep+errorMsg+os.linesep)
        logging.error(self.getNodePath(x1) + " " + self.getNodePath(x2) + errorMsg)

    def doStripWhitespaces(self, text):
        if text == None:
            return None
        else:
            return text.strip().replace('\n', '').replace('\r', '')

    def text_compare(self, t1, t2, strip_whitespaces=False, float_compare=False):
        logging.debug('[CompareDriver][text_compare] text_compare start t1: ' + str(t1) + ' t2: ' + str(t2) + ' strip_whitespaces: ' + str(strip_whitespaces) + ' float_compare: ' + str(float_compare))
        if not t1 and not t2:
            return True
        if float_compare:
            try:
                f1 = float(t1)
                f2 = float(t2)
                return f1 == f2
            except ValueError:
                pass
        if strip_whitespaces:
            return (self.doStripWhitespaces(t1) or '') == (self.doStripWhitespaces(t2) or '')
        else:
            return (t1 or '') == (t2 or '')

    def xml_compare(self, x1, x2, reporter=None, strip_whitespaces=False, ignore_order=False, float_compare=False):
        logging.debug('[CompareDriver][xml_compare] xml_compare start')
        if x1.tag != x2.tag:
            self.doReport(reporter, x1, x2, 'Tags do not match: %s and %s' % (x1.tag, x2.tag))
            return False
        for name, value in x1.attrib.items():
            if not self.text_compare(value, x2.attrib.get(name), strip_whitespaces=strip_whitespaces, float_compare=float_compare):
                self.doReport(reporter, x1, x2, 'Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
                return False
        for name in x2.attrib.keys():
            if not x1.attrib.has_key(name):
                self.doReport(reporter, x1, x2, 'x2 has an attribute x1 is missing: %s' % name)
                return False
        if not self.text_compare(x1.text, x2.text, strip_whitespaces=strip_whitespaces, float_compare=float_compare):
            self.doReport(reporter, x1, x2, 'text: %r != %r' % (x1.text, x2.text))
            return False

        if not self.text_compare(x1.tail, x2.tail, strip_whitespaces=strip_whitespaces, float_compare=float_compare):
            self.doReport(reporter, x1, x2, 'tail: %r != %r' % (x1.tail, x2.tail))
            return False

        cl1 = x1.getchildren()
        cl2 = x2.getchildren()
        if len(cl1) != len(cl2):
            self.doReport(reporter, x1, x2, 'children length differs, %i != %i' % (len(cl1), len(cl2)))
            return False
        i = 0
        for c1, c2 in zip(cl1, cl2):
            i += 1
            logging.debug('[CompareDriver][xml_compare] strip_whitespaces: ' + str(strip_whitespaces))
            logging.debug('[CompareDriver][xml_compare] start c1: ' + str(c1) + ' t2: ' + str(c1) + ' strip_whitespaces: ' + str(strip_whitespaces) + ' float_compare: ' + str(float_compare))

            if not self.text_compare(c1, c2, reporter, strip_whitespaces=strip_whitespaces, float_compare=float_compare):
                logging.debug('[xml_compare] strip_whitespaces1: ' + str(strip_whitespaces))
                self.doReport(reporter, c1, c2, 'children %i do not match: %s' % (i, c1.tag))
                return False
            logging.debug('[CompareDriver][xml_compare] strip_whitespaces2: ' + str(strip_whitespaces))
        return True

    @staticmethod
    def toPretty(data, lang, dump):
        if (lang == 'json'):
            try:
                if (dump):
                    data = json.loads(data)
                jpretty = json.dumps(data, indent=4, sort_keys=True)
                return jpretty
            except ValueError as e:
                logging.error("[CompareDriver][toPretty] jsonpretty fail jsonpretty: " + str(data))
                logging.error("[CompareDriver][toPretty] exception: " + str(e))
        elif (lang == 'xml'):
            xresp = lxml.etree.fromstring(str(data))
            xpretty = lxml.etree.tostring(xresp, pretty_print=True)
            return xpretty


