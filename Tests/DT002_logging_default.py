#usr/bin/python3
"""
Module introspection_lib.Tests.DT001_logging_default

Implements demonstration testing of the module introspection_lib.logging.
Specifically, the default functionality and message propagation without level
filtering of the dual logging class.

Test ID: TEST-D-300. Covers requirement REQ-FUN-300, REQ-FUN-303, REQ-FUN-305
and REQ-FUN-306.
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

from introspection_lib.logging import DualLogger

#help functions

def Helper1(objLogger):
    objLogger.debug('Debug from Helper1 function')
    objLogger.info('Info from Helper1 function')
    objLogger.warning('Warning from Helper1 function')
    objLogger.error('Error from Helper1 function')
    objLogger.critical('Critical from Helper1 function')

def Helper2(objLogger):
    objLogger.debug('Debug from Helper2 function')
    objLogger.info('Info from Helper2 function')
    objLogger.warning('Warning from Helper2 function')
    objLogger.error('Error from Helper2 function')
    objLogger.critical('Critical from Helper2 function')

#testing

if __name__ == '__main__':
    ErrorLogger = DualLogger() #default logger name
    ErrorLogger.setLogFile() #default file name
    assert (isinstance(ErrorLogger, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (logging.NOTSET < ErrorLogger.getEffectiveLevel() < logging.DEBUG
            ), 'Logger should be set to between NOTSET and DEBUG'
    iMin, iMax = ErrorLogger.getConsoleRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min console level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max console level should be set to above CRITICAL'
    iMin, iMax = ErrorLogger.getFileRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min file log level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max file log level should be set to above CRITICAL'
    iMin, iMax = ErrorLogger.getPropagateRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min propagate level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max propagate level should be set to above CRITICAL'
    ProcessLogger = ErrorLogger.getChild('process')
    ProcessLogger.setLogFile() #default file name
    assert (isinstance(ProcessLogger, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (logging.NOTSET < ProcessLogger.getEffectiveLevel() < logging.DEBUG
            ), 'Logger should be set to between NOTSET and DEBUG'
    iMin, iMax = ProcessLogger.getConsoleRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min console level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max console level should be set to above CRITICAL'
    iMin, iMax = ProcessLogger.getFileRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min file log level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max file log level should be set to above CRITICAL'
    iMin, iMax = ProcessLogger.getPropagateRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min propagate level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max propagate level should be set to above CRITICAL'
    DebugLogger1 = ProcessLogger.getChild('debug1')
    DebugLogger1.setLogFile() #default file name
    assert (isinstance(DebugLogger1, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (logging.NOTSET < DebugLogger1.getEffectiveLevel() < logging.DEBUG
            ), 'Logger should be set to between NOTSET and DEBUG'
    iMin, iMax = DebugLogger1.getConsoleRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min console level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max console level should be set to above CRITICAL'
    iMin, iMax = DebugLogger1.getFileRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min file log level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max file log level should be set to above CRITICAL'
    iMin, iMax = DebugLogger1.getPropagateRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min propagate level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max propagate level should be set to above CRITICAL'
    DebugLogger2 = ProcessLogger.getChild('debug2')
    DebugLogger2.setLogFile() #default file name
    assert (isinstance(DebugLogger2, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (logging.NOTSET < DebugLogger2.getEffectiveLevel() < logging.DEBUG
            ), 'Logger should be set to between NOTSET and DEBUG'
    iMin, iMax = DebugLogger2.getConsoleRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min console level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max console level should be set to above CRITICAL'
    iMin, iMax = DebugLogger2.getFileRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min file log level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max file log level should be set to above CRITICAL'
    iMin, iMax = DebugLogger2.getPropagateRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min propagate level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max propagate level should be set to above CRITICAL'
    #testing top level logger
    #+ all messages should be printed into the console and its own file
    ErrorLogger.debug('Debug from ErrorLogger')
    ErrorLogger.info('Info from ErrorLogger')
    ErrorLogger.warning('Warning from ErrorLogger')
    ErrorLogger.error('Error from ErrorLogger')
    ErrorLogger.critical('Critcial from ErrorLogger')
    #testing middle level logger
    #+ all messages should be printed into the console (once only), into its own
    #+ file, and into the top level logger's file
    ProcessLogger.debug('Debug from ProcessLogger')
    ProcessLogger.info('Info from ProcessLogger')
    ProcessLogger.warning('Warning from ProcessLogger')
    ProcessLogger.error('Error from ProcessLogger')
    ProcessLogger.critical('Critcial from ProcessLogger')
    #testing the bottom level loggers
    #+ all messages should be printed into the console (once only), into its own
    #+ file (but not its sibling's), into the top level and middle level
    #+ loggers' files
    Helper1(DebugLogger1)
    Helper2(DebugLogger2)
