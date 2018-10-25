#!/usr/bin/python3
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger('nistest.basic.StubDirver')
val = "name"
log.debug(f"{val}")
