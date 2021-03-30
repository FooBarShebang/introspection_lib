#usr/bin/python3
"""
Module introspection_lib.Tests.DT006_logging_handler_level

Implements demonstration testing of the module introspection_lib.my_logging.
Specifically, the default functionality and message propagation with the
filtering by the handlers of the dual logging class as well as by the threshold
level of the logger itself.

Test ID: TEST-D-304. Covers requirements REQ-FUN-301, REQ-FUN-302 and
REQ-FUN-304.
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
    objLogger.debug('Debug from Helper1 function') #child1.log only
    objLogger.info('Info from Helper1 function') #console and process.log
    objLogger.warning('Warning from Helper1 function') #console and process.log
    objLogger.error('Error from Helper1 function') #error.log only
    objLogger.critical('Critical from Helper1 function') #error.log only

def Helper2(objLogger):
    objLogger.debug('Debug from Helper2 function') #child2.log only
    objLogger.info('Info from Helper2 function') #console and process.log
    objLogger.warning('Warning from Helper2 function') #console and process.log
    objLogger.error('Error from Helper2 function') #error.log only
    objLogger.critical('Critical from Helper2 function') #error.log only

#testing

if __name__ == '__main__':
    ErrorLogger = DualLogger('main')
    ErrorLogger.setLogFile('errors.log')
    ErrorLogger.setLevel('none')
    ErrorLogger.setMinFileLevel('error')
    assert (isinstance(ErrorLogger, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (logging.CRITICAL < ErrorLogger.getEffectiveLevel()
            ), 'Logger should be set to above CRITICAL'
    iMin, iMax = ErrorLogger.getConsoleRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min console level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max console level should be set to above CRITICAL'
    iMin, iMax = ErrorLogger.getFileRange()
    assert (iMin == logging.ERROR
            ), 'Min file log level should be set to ERROR'
    assert (logging.CRITICAL < iMax
            ), 'Max file log level should be set to above CRITICAL'
    iMin, iMax = ErrorLogger.getPropagateRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min propagate level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max propagate level should be set to above CRITICAL'
    ProcessLogger = ErrorLogger.getChild('process')
    ProcessLogger.setLogFile('process.log')
    ProcessLogger.setLevel('info')
    ProcessLogger.setMinFileLevel('info')
    ProcessLogger.setMaxFileLevel('warning')
    ProcessLogger.setMinPropagateLevel('warning')
    assert (isinstance(ProcessLogger, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (ProcessLogger.getEffectiveLevel() == logging.INFO
            ), 'Logger should be set to INFO'
    iMin, iMax = ProcessLogger.getConsoleRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min console level should be set to between NOTSET and DEBUG'
    assert (logging.CRITICAL < iMax
            ), 'Max console level should be set to above CRITICAL'
    iMin, iMax = ProcessLogger.getFileRange()
    assert (iMin == logging.INFO
            ), 'Min console level should be set to INFO'
    assert (iMax == logging.WARNING
            ), 'Max console level should be set to WARNING'
    iMin, iMax = ProcessLogger.getPropagateRange()
    assert (iMin == logging.WARNING
            ), 'Min propagate level should be set to WARNING'
    assert (logging.CRITICAL < iMax
            ), 'Max propagate level should be set to above CRITICAL'
    DebugLogger1 = ProcessLogger.getChild('debug1')
    DebugLogger1.setLogFile('child1.log')
    DebugLogger1.setMinConsoleLevel('info')
    DebugLogger1.setMaxConsoleLevel('warning')
    DebugLogger1.setMaxFileLevel('debug')
    DebugLogger1.setMinPropagateLevel('info')
    assert (isinstance(DebugLogger1, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (logging.NOTSET < DebugLogger1.getEffectiveLevel() < logging.DEBUG
            ), 'Logger should be set to between NOTSET and DEBUG'
    iMin, iMax = DebugLogger1.getConsoleRange()
    assert (iMin == logging.INFO
            ), 'Min console level should be set to INFO'
    assert (iMax == logging.WARNING
            ), 'Max console level should be set to WARNING'
    iMin, iMax = DebugLogger1.getFileRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min file log level should be set to between NOTSET and DEBUG'
    assert (iMax == logging.DEBUG
            ), 'Max file log level should be set to DEBUG'
    iMin, iMax = DebugLogger1.getPropagateRange()
    assert (iMin == logging.INFO
            ), 'Min propagate level should be set to INFO'
    assert (logging.CRITICAL < iMax
            ), 'Max propagate level should be set to above CRITICAL'
    DebugLogger2 = ProcessLogger.getChild('debug2')
    DebugLogger2.setLogFile('child2.log')
    DebugLogger2.setMinConsoleLevel('info')
    DebugLogger2.setMaxConsoleLevel('warning')
    DebugLogger2.setMaxFileLevel('debug')
    DebugLogger2.setMinPropagateLevel('info')
    assert (isinstance(DebugLogger2, DualLogger)
                ), 'Logger should be instance of DualLogger class'
    assert (logging.NOTSET < DebugLogger2.getEffectiveLevel() < logging.DEBUG
            ), 'Logger should be set to between NOTSET and DEBUG'
    iMin, iMax = DebugLogger2.getConsoleRange()
    assert (iMin == logging.INFO
            ), 'Min console level should be set to INFO'
    assert (iMax == logging.WARNING
            ), 'Max console level should be set to WARNING'
    iMin, iMax = DebugLogger2.getFileRange()
    assert (logging.NOTSET < iMin < logging.DEBUG
            ), 'Min file log level should be set to between NOTSET and DEBUG'
    assert (iMax == logging.DEBUG
            ), 'Max file log level should be set to DEBUG'
    iMin, iMax = DebugLogger2.getPropagateRange()
    assert (iMin == logging.INFO
            ), 'Min propagate level should be set to INFO'
    assert (logging.CRITICAL < iMax
            ), 'Max propagate level should be set to above CRITICAL'
    #testing top level logger
    ErrorLogger.debug('Debug from ErrorLogger') #not logged at all
    ErrorLogger.info('Info from ErrorLogger') #not logged at all
    ErrorLogger.warning('Warning from ErrorLogger') #not logged at all
    ErrorLogger.error('Error from ErrorLogger') #not logged at all
    ErrorLogger.critical('Critical from ErrorLogger') #not logged at all
    #testing middle level logger
    ProcessLogger.debug('Debug from ProcessLogger') #not logged at all
    ProcessLogger.info('Info from ProcessLogger') #console and process.log
    ProcessLogger.warning('Warning from ProcessLogger') #console and process.log
    ProcessLogger.error('Error from ProcessLogger') #console and error.log
    ProcessLogger.critical('Critical from ProcessLogger') #console and error.log
    #testing the bottom level loggers
    #+ see expectations in the functions definitions
    Helper1(DebugLogger1)
    Helper2(DebugLogger2)