#usr/bin/python3
"""
Module introspection_lib.Tests.DT004_logging_logger_level

Implements demonstration testing of the module introspection_lib.my_logging.
Specifically, the default functionality and message propagation with only the
logger's own severity level filtering of the dual logging class.

Test ID: TEST-D-302. Covers requirement REQ-FUN-301.
"""

__version__ = "1.0.0.0"
__date__ = "27-11-2020"
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

from introspection_lib.my_logging import DualLogger

#help functions

def Helper1(objLogger):
    objLogger.debug('Debug from Helper1 function') #not logged at all
    objLogger.info('Info from Helper1 function')
    #logged into console, errors.log, process.log and child1.log
    objLogger.warning('Warning from Helper1 function')
    #logged into console, errors.log, process.log and child1.log
    objLogger.error('Error from Helper1 function')
    #logged into console, errors.log, process.log and child1.log
    objLogger.critical('Critical from Helper1 function')
    #logged into console, errors.log, process.log and child1.log

def Helper2(objLogger):
    objLogger.debug('Debug from Helper2 function') #not logged at all
    objLogger.info('Info from Helper2 function')
    #logged into console, errors.log, process.log and child2.log
    objLogger.warning('Warning from Helper2 function')
    #logged into console, errors.log, process.log and child2.log
    objLogger.error('Error from Helper2 function')
    #logged into console, errors.log, process.log and child2.log
    objLogger.critical('Critical from Helper2 function')
    #logged into console, errors.log, process.log and child2.log

#testing

if __name__ == '__main__':
    ErrorLogger = DualLogger('main')
    ErrorLogger.setLogFile('errors.log')
    ErrorLogger.setLevel('error')
    assert (isinstance(ErrorLogger, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (ErrorLogger.getEffectiveLevel() == logging.ERROR
            ), 'Logger should be set to ERROR'
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
    ProcessLogger.setLogFile('process.log')
    ProcessLogger.setLevel('warning')
    assert (isinstance(ProcessLogger, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (ProcessLogger.getEffectiveLevel() == logging.WARNING
            ), 'Logger should be set to WARNING'
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
    DebugLogger1.setLogFile('child1.log')
    DebugLogger1.setLevel('info')
    assert (isinstance(DebugLogger1, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (DebugLogger1.getEffectiveLevel() == logging.INFO
            ), 'Logger should be set to INFO'
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
    DebugLogger2.setLogFile('child2.log')
    DebugLogger2.setLevel('info')
    assert (isinstance(DebugLogger2, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (DebugLogger2.getEffectiveLevel() == logging.INFO
            ), 'Logger should be set to INFO'
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
    ErrorLogger.debug('Debug from ErrorLogger') #not logged at all
    ErrorLogger.info('Info from ErrorLogger') #not logged at all
    ErrorLogger.warning('Warning from ErrorLogger') #not logged at all
    ErrorLogger.error('Error from ErrorLogger')
    #logged into console and errors.log
    ErrorLogger.critical('Critical from ErrorLogger')
    #logged into console and errors.log
    #testing middle level logger
    #+ all messages should be printed into the console (once only), into its own
    #+ file, and into the top level logger's file
    ProcessLogger.debug('Debug from ProcessLogger') #not logged at all
    ProcessLogger.info('Info from ProcessLogger') #not logged at all
    ProcessLogger.warning('Warning from ProcessLogger')
    #logged into console, errors.log and process.log
    ProcessLogger.error('Error from ProcessLogger')
    #logged into console, errors.log and process.log
    ProcessLogger.critical('Critical from ProcessLogger')
    #logged into console, errors.log and process.log
    #testing the bottom level loggers
    #+ see functions for the expected log messages
    Helper1(DebugLogger1)
    Helper2(DebugLogger2)
