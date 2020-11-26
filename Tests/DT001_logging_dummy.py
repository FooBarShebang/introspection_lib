#usr/bin/python3
"""
Module introspection_lib.Tests.DT001_logging_dummy

Implements demonstration testing of the module introspection_lib.logging.
Specifically, the 'dummy' logger's functionality.

Test ID: TEST-D-310. Covers requirement REQ-FUN-310.
"""

__version__ = "1.0.0.0"
__date__ = "26-11-2020"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import logging

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

from introspection_lib.logging import DummyLogger

#actual tests

if __name__ == '__main__':
    objTest = DummyLogger('test')
    #objTest = DummyLogger()
    #can be instantiated with or without a name passed
    objTest.setLevel(logging.DEBUG) #explicitely set to the lowest level
    #try to log at all possible levels
    objTest.debug('Debug test message')
    objTest.info('Info test message')
    objTest.warning('Warning test message')
    objTest.error('Error test message')
    objTest.exception('Exception test message')
    objTest.critical('Critical test message')
    objTest.fatal('Critical test message')
    #no messages should be printed, files created, or exceptions raised