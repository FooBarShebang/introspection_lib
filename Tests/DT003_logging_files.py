#usr/bin/python3
"""
Module introspection_lib.Tests.DT001_logging_files

Implements demonstration testing of the module introspection_lib.logging.
Specifically, rotation of log files and enabling / disabling logging into a
file.

Test ID: TEST-D-301. Covers requirement REQ-FUN-306.
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

#testing

if __name__ == '__main__':
    ErrorLogger = DualLogger('main')
    ErrorLogger.setLogFile('main.log') #default file name
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
    ProcessLogger.info('Message 1') #should be in the console and main.log
    #try disable file logging whilst it not yet enabled
    ProcessLogger.disableFileLogging()
    ProcessLogger.info('Message 2') #should be in the console and main.log
    ProcessLogger.setLogFile('process.log')
    ProcessLogger.info('Message 3') #should be in the console and main.log
    #+ and process.log
    ProcessLogger.setLogFile('errors.log')
    ProcessLogger.info('Message 4') #should be in the console and main.log
    #+ and errors.log
    ProcessLogger.setLogFile('process.log')
    ProcessLogger.info('Message 5') #should be in the console and main.log
    #+ and process.log again
    ProcessLogger.disableFileLogging()
    ErrorLogger.disableFileLogging()
    ProcessLogger.info('Message 6') #should be in the console only