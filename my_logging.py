#usr/bin/python3
"""
Module introspection_lib.logging

Implements custom logging classes.

Classes:
    DummyLogger: all messages are dumped into NIL-stream
    DualLogger: can simulataneously log into a console and a file and filter
        messages by min and max levels in terms of handling and propagation
    LoggerFilter: helper class - logger level filter
    ConsoleHandlerFilter: helper class - console handler
    FileHandlerFilter: helper class - file logging handler

"""

__version__ = "1.0.1.0"
__date__ = "16-12-2020"
__status__ = "Production"

#imports

#+ standard libraries

import os
import weakref
import datetime
import logging as base_logging

from typing import Optional, Union, Tuple

#types

TStrNone = Optional[str]

TStrInt = Union[str, int]

TRange = Tuple[int, int]

#global variables

ALL = base_logging.DEBUG - 1 #allows everything
DEBUG = base_logging.DEBUG
INFO = base_logging.INFO
WARNING = base_logging.WARNING
ERROR = base_logging.ERROR
CRITICAL = base_logging.CRITICAL
NONE = base_logging.CRITICAL + 1 #forbids everything

LOOKUP_TABLE = {
    'all' : ALL,
    'debug' : DEBUG,
    'info' : INFO,
    'warning' : WARNING,
    'error' : ERROR,
    'critical' : CRITICAL,
    'none' : NONE
}

#helper functions

def _ResolveLevel(Level: TStrInt) -> int:
    """
    Converts the logging severity level passed as a non-negative integer or a
    sting alias into the integer value of the severity level. The acceptable
    aliases (case-insensitive) are: 'ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR',
    'CRITICAL' and 'NONE'.

    Signature:
        str OR int >= 0 -> int >= 0
    
    Args:
        Level: str OR int >=0; severity level passed as a non-negative integer,
            or a string alias (case-insensitive)
    
    Returns:
        int >= 0: integer represenation of the severity level
    
    Raises:
        TypeError: the passed argument is neither string nor an ineteger
        ValueError: the passed argument is a negative integer, or a string
            representing the unknown level
    
    Version 1.0.0.0
    """
    if isinstance(Level, int):
        if Level < 0:
            raise ValueError('Severity level must be a non-negative integer')
        iResult = Level
    elif isinstance(Level, str):
        iResult = LOOKUP_TABLE.get(Level.lower(), None)
        if iResult is None:
            raise ValueError('Unknown level alias: {}'.format(Level))
    else:
        strError = ' '.join(['Severity level must be a string or an integer,',
                                'not {}'.format(type(Level))])
        raise TypeError(strError)
    return iResult

#classes

#+ helper classes

class LoggerFilter:
    """
    A simple data modifying filter intended to be used with a logger object, not
    with a handler. Adds two flag attributes to a record object - IsToPrint and
    IsToPropagate - to indicate if the message is intended to be handled by the
    console handler of this logger or its parent, and the file handler of its
    parent only respectively. The boolean value True is set if the issued
    message level is within the corresponding acceptance ranges defined by the
    logger, and False - otherwise. A reference to the concerned logger is to
    passed during instantiation of this class.

    Methods:
        filter(Parent):
            logging.LogRecord -> bool
    
    Attributes:
        parent: introspection_lib.logging.DualLogger
    
    Version 1.0.0.1
    """

    #special methods

    def __init__(self, Parent: base_logging.Logger) -> None:
        """
        Initialization method. Simply stores the passed reference to a logger
        object in the instance attribite 'parent' as a proxy weak reference.

        Signature:
            introspection_lib.logging.DualLogger -> None
        
        Args:
            Parent: introspection_lib.logging.DualLogger; reference to a logger

        Version 1.0.0.0
        """
        self.parent = weakref.proxy(Parent)
    
    def __del__(self) -> None:
        """
        Finalization method. Removes the circular referencing concerning the
        parent logger object. Note, that this method is not strictly speaking
        needed, since the garbage collector seems to handle the situation fine
        without it.
        
        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        del self.parent
        self.parent = None
    
    #public API

    def filter(self, Record: base_logging.LogRecord) -> bool:
        """
        Adds two flag attributes to a record object - IsToPrint and
        IsToPropagate - to indicate if the message is intended to be handled by
        the console handler of this logger or its parent, and the file handler
        of its parent only respectively. The boolean value True is set if the
        issued message level is within the corresponding acceptance ranges
        defined by the logger, and False - otherwise.

        Signature:
            logging.LogRecord -> bool
        
        Args:
            Record: logging.Record; the log message to be processed

        Returns:
            bool: always True value
        
        Version 1.0.0.0
        """
        iMin, iMax = self.parent.getConsoleRange()
        iLoggerLevel = self.parent.getEffectiveLevel()
        if ((Record.levelno >= iMin) and (Record.levelno <= iMax)
                                        and (Record.levelno >= iLoggerLevel)):
            Record.IsToPrint = True
        else:
            Record.IsToPrint = False
        iMin, iMax = self.parent.getPropagateRange()
        if ((Record.levelno >= iMin) and (Record.levelno <= iMax)
                                        and (Record.levelno >= iLoggerLevel)):
            Record.IsToPropagate = True
        else:
            Record.IsToPropagate = False
        return True

class ConsoleHandlerFilter(LoggerFilter):
    """
    Filter for a console hanlder of a logger object. Allows only the messages,
    witch are marked to be intended for the console by a logger object, which
    issued that message - may be this logger or one of its children. The
    reference to the logger with the concerned handler attached must be passed
    to the instantiation method of this class. Sub-classes LoggerFilter.

    Methods:
        filter(Parent):
            logging.LogRecord -> bool
    
    Attributes:
        parent: introspection_lib.logging.DualLogger
    
    Version 1.0.0.0
    """

    #public API

    def filter(self, Record: base_logging.LogRecord) -> bool:
        """
        Actual file handler filter functionality. Simply returns the value of
        the boolean flag IsToPrint of the passed LogRecord object.

        Signature:
            logging.LogRecord -> bool
        
        Args:
            Record: logging.Record; the log message to be processed

        Returns:
            bool: True if the message must be processed by the handler, False
                otherwise
        
        Version 1.0.0.0
        """
        return Record.IsToPrint

class FileHandlerFilter(LoggerFilter):
    """
    Filter for a file hanlder of a logger object. Allows only the messages with
    the level within the acceptance range of this handler (defined by the logger
    object) and either the message is issued by this logger or it is marked as
    to be propaged by a child logger issued this message. The reference to the
    logger with the concerned handler attached must be passed to the
    instantiation method of this class. Sub-classes LoggerFilter.
    
    Methods:
        filter(Parent):
            logging.LogRecord -> bool
    
    Attributes:
        parent: introspection_lib.logging.DualLogger
    
    Version 1.0.0.0
    """

    #public API

    def filter(self, Record: base_logging.LogRecord) -> bool:
        """
        Actual file handler filter functionality. Returns True only if the
        message level is within the acceptance range of this handler (defined by
        the logger object) and either the message is issued by this logger or
        marked as to be propaged by a child logger issued this message.

        Signature:
            logging.LogRecord -> bool
        
        Args:
            Record: logging.Record; the log message to be processed

        Returns:
            bool: True if the message must be processed by the handler, False
                otherwise
        
        Version 1.0.0.0
        """
        iMin, iMax = self.parent.getFileRange()
        if (Record.levelno >= iMin) and (Record.levelno <= iMax):
            if Record.name == self.parent.name:
                if Record.levelno >= self.parent.getEffectiveLevel():
                    bResult = True
                else:
                    bResult = False
            else:
                bResult = Record.IsToPropagate
        else:
            bResult = False
        return bResult

#+ main classes
class DummyLogger(base_logging.Logger):
    """
    Specialized sub-class of the logging.Logger class (Standard Python Library),
    which upon instantiation has no parent logger, but an instance of the class
    NullHandler attached as a handler. Inherits all API from the super class
    without changes except for the ininitalization method.

    Version 1.0.0.1
    """

    #special methods

    def __init__(self, Name: TStrNone = None) -> None:
        """
        Initialization method. Assigns a name, creates and attaches a single
        handler - NullHandler to the instance.

        Signature:
            /str OR None/ -> None
        
        Args:
            Name: (optional) str; a name to be assigned to a logger, defaults to
                None, in which case the class' name is used instead
        
        Version 1.0.0.1
        """
        if isinstance(Name, str):
            strName = Name
        else:
            strName = self.__class__.__name__
        super().__init__(strName)
        self.parent = None
        self.propagate = False
        objTemp = base_logging.NullHandler()
        self.addHandler(objTemp)

class DualLogger(base_logging.Logger):
    """
    Specialized sub-class of the logging.Logger class (Standard Python Library),
    which implements possibility of simultaneous logging into a console and one
    or more files with the minimalistic setting up at the user's side.

    Inherits the API from the super class, re-defines getChild() and setLevel()
    methods and adds some new methods.

    Methods:
        getChild(Name):
            str -> DualLogger
        setLevel(Level):
            str OR int >= 0 -> None
        setMinConsoleLevel(Level):
            str OR int >= 0 -> None
        setMaxConsoleLevel(Level):
            str OR int >= 0 -> None
        getConsoleRange():
            None -> tuple(int >= 0, int >= 0)
        setLogFile(FileName = None):
            /str/ -> None
        disableFileLogging():
            None -> None
        setMinFileLevel(Level):
            str OR int >= 0 -> None
        setMaxFileLevel(Level):
            str OR int >= 0 -> None
        getFileRange():
            None -> tuple(int >= 0, int >= 0)
        setMinPropagateLevel(Level):
            str OR int >= 0 -> None
        setMaxPropagateLevel(Level):
            str OR int >= 0 -> None
        getPropagateRange():
            None -> tuple(int >= 0, int >= 0)
        setConsoleStream(Stream):
            type A -> None

    Version 1.1.0.0
    """

    #private class attributes

    _DefaultFormatter = base_logging.Formatter(' '.join(['{asctime}',
                            '{levelname}@{name} FROM {funcName} IN {filename}',
                            '(LINE {lineno})\n{message}']),
                            datefmt = '%Y-%m-%d %H:%M:%S',
                            style = '{')

    #special methods

    def __init__(self, Name: TStrNone = None,
                        Parent: Optional[base_logging.Logger] = None) -> None:
        """
        Initialization method. Assigns a name, creates and attaches a single
        handler - StreamHandler, but only to a 'root' instance. Special keywoard
        argument Parent can be passed referencing to another instance of a
        logger class as the parent of this instance, in which case a console
        handler is not attached. Do not use this functionality directly - it is
        reserved for the implemetation of the getChild() method.
        
        Note that for a 'root' logger the 'parent' attribute is set to None and
        the 'propagate' attribute - to False. For a 'child' logger the
        'propagate' attribute is set to True, and the 'parent' holds the
        reference to the parent logger.

        Signature:
            /str OR None, base_logging.Logger OR None/ -> None
        
        Args:
            Name: (optional) str; a name to be assigned to a logger, defaults to
                None, in which case the class' name is used instead
            Parent: (optional) logging.Logger; a reference to the 'parent'
                logger, defaults to None, in which case the instance is created
                as a 'root' logger
        
        Version 1.0.0.1
        """
        if isinstance(Name, str):
            strName = Name
        else:
            strName = self.__class__.__name__
        if isinstance(Parent, DualLogger):
            strName = '{}.{}'.format(Parent.name, strName)
            super().__init__(strName)
            self.parent = Parent
            self.propagate = True
        else:
            super().__init__(strName)
        if ((self.parent is None) or
                            isinstance(self.parent, base_logging.RootLogger)):
            self.parent = None
            self._ConsoleHandler = base_logging.StreamHandler()
            self._ConsoleHandler.setLevel(ALL)
            self._ConsoleHandler.addFilter(ConsoleHandlerFilter(self))
            self._ConsoleHandler.setFormatter(self._DefaultFormatter)
            self.addHandler(self._ConsoleHandler)
            self.propagate = False
        else:
            self.propagate = True
            self._ConsoleHandler = None
        self.setLevel('ALL')
        self.addFilter(LoggerFilter(self))
        self.setMinConsoleLevel('ALL')
        self.setMaxConsoleLevel('NONE')
        self.setMinFileLevel('ALL')
        self.setMaxFileLevel('NONE')
        self.setMinPropagateLevel('ALL')
        self.setMaxPropagateLevel('NONE')
        self._LogFile = None
        self._FileHandler = None
    
    #public API

    def getChild(self, Name: str) -> base_logging.Logger:
        """
        Creates and returns a child logger with respect to the current one.

        Signature:
            str -> DualLogger
        
        Args:
            Name: str; 'base' name of the child logger, will be attached through
                a dot to the name of the current logger
        
        Returns:
            DualLogger: another instance of the same class as the current logger
                with the name constructed from the name of the current one and
                the passed string argument attached via a dot; the current
                logger instance is set as the parent of the created one
        
        Version 1.0.0.0
        """
        return self.__class__(Name, Parent = self)

    def setLevel(self, Level: TStrInt) -> None:
        """
        Sets the severity level of the logger itself by a non-negative integer
        or a string alias. The acceptable aliases (case-insensitive) are: 'ALL',
        'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' and 'NONE'.

        Signature:
            str OR int >= 0 -> None
    
        Args:
            Level: str OR int >=0; severity level passed as a non-negative
                integer, or a string alias (case-insensitive)

        Raises:
            TypeError: the passed argument is neither string nor an ineteger
            ValueError: the passed argument is a negative integer, or a string
                representing the unknown level

        Version 1.0.0.0
        """
        iLevel = _ResolveLevel(Level)
        super().setLevel(iLevel)
    
    def setMinConsoleLevel(self, Level: TStrInt) -> None:
        """
        Sets the minimum severity level of the console output by a non-negative
        integer or a string alias. The acceptable aliases (case-insensitive)
        are: 'ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' and 'NONE'.

        Signature:
            str OR int >= 0 -> None
    
        Args:
            Level: str OR int >=0; severity level passed as a non-negative
                integer, or a string alias (case-insensitive)

        Raises:
            TypeError: the passed argument is neither string nor an ineteger
            ValueError: the passed argument is a negative integer, or a string
                representing the unknown level

        Version 1.0.0.0
        """
        self._MinConsoleLevel = _ResolveLevel(Level)
    
    def setMaxConsoleLevel(self, Level: TStrInt) -> None:
        """
        Sets the maximum severity level of the console output by a non-negative
        integer or a string alias. The acceptable aliases (case-insensitive)
        are: 'ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL' and 'NONE'.

        Signature:
            str OR int >= 0 -> None
    
        Args:
            Level: str OR int >=0; severity level passed as a non-negative
                integer, or a string alias (case-insensitive)

        Raises:
            TypeError: the passed argument is neither string nor an ineteger
            ValueError: the passed argument is a negative integer, or a string
                representing the unknown level

        Version 1.0.0.0
        """
        self._MaxConsoleLevel = _ResolveLevel(Level)
    
    def getConsoleRange(self) -> int:
        """
        Returns the current min and max severity levels of the console output
        as a 2-tuple of non-negative integers.

        Signature:
            None -> tuple(int >= 0, int >= 0)
        
        Version 1.0.0.0
        """
        return (self._MinConsoleLevel, self._MaxConsoleLevel)
    
    def setLogFile(self, FileName: TStrNone = None) -> None:
        """
        Sets the current output log file path and attaches an file handler. The
        currently used (if exists) log file is flushed and closed, unless the
        path is the same. If the file name (path) is not provided, the log file
        is created is placed into the current working folder with the base file-
        name as '{YYYYMMDD_HHMMSS}_{LoggerName}.log'. The already existing log
        files are opened in the attach mode.

        Signature:
            /str/ -> None
        
        Args:
            FileName: (optional) str; a path to a file to use as the log output,
                defaults to None, in wich case the log file is created in the
                current working directory with the name constructed from the
                current date-time stamp and the logger's name, with the '.log'
                extension.
        
        Version 1.0.0.0
        """
        if isinstance(FileName, str):
            strFilePath = os.path.abspath(FileName)
        else:
            strTime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            strName = '{}_{}.log'.format(strTime, self.name)
            strFilePath = os.path.abspath(strName)
        if not (self._FileHandler is None) and self._LogFile != strFilePath:
            self.disableFileLogging()
        if self._FileHandler is None:
            self._FileHandler = base_logging.FileHandler(strFilePath)
            self._FileHandler.setLevel(ALL)
            self._FileHandler.addFilter(FileHandlerFilter(self))
            self._FileHandler.setFormatter(self._DefaultFormatter)
            self.addHandler(self._FileHandler)

    def disableFileLogging(self) -> None:
        """
        Flushes and closes the currently used log file (if any exists) and
        removes the attached file handler.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        if not (self._FileHandler is None):
            self._FileHandler.flush()
            self._FileHandler.close()
            self.removeHandler(self._FileHandler)
            self._FileHandler = None
            self._LogFile = None
    
    def setMinFileLevel(self, Level: TStrInt) -> None:
        """
        Sets the minimum severity level of the output into own log file by a
        non-negative integer or a string alias. The acceptable aliases
        (case-insensitive) are: 'ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR',
        'CRITICAL' and 'NONE'.

        Signature:
            str OR int >= 0 -> None
    
        Args:
            Level: str OR int >=0; severity level passed as a non-negative
                integer, or a string alias (case-insensitive)

        Raises:
            TypeError: the passed argument is neither string nor an ineteger
            ValueError: the passed argument is a negative integer, or a string
                representing the unknown level

        Version 1.0.0.0
        """
        self._MinFileLevel = _ResolveLevel(Level)
    
    def setMaxFileLevel(self, Level: TStrInt) -> None:
        """
        Sets the maximum severity level of the output into own log file by a
        non-negative integer or a string alias. The acceptable aliases
        (case-insensitive) are: 'ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR',
        'CRITICAL' and 'NONE'.

        Signature:
            str OR int >= 0 -> None
    
        Args:
            Level: str OR int >=0; severity level passed as a non-negative
                integer, or a string alias (case-insensitive)

        Raises:
            TypeError: the passed argument is neither string nor an ineteger
            ValueError: the passed argument is a negative integer, or a string
                representing the unknown level

        Version 1.0.0.0
        """
        self._MaxFileLevel = _ResolveLevel(Level)
    
    def getFileRange(self) -> int:
        """
        Returns the current min and max severity levels of the own file output
        as a 2-tuple of non-negative integers.

        Signature:
            None -> tuple(int >= 0, int >= 0)
        
        Version 1.0.0.0
        """
        return (self._MinFileLevel, self._MaxFileLevel)

    def setMinPropagateLevel(self, Level: TStrInt) -> None:
        """
        Sets the minimum severity level of a message to be propagated into the
        parent's file handler by a non-negative integer or a string alias. The
        acceptable aliases (case-insensitive) are: 'ALL', 'DEBUG', 'INFO',
        'WARNING', 'ERROR', 'CRITICAL' and 'NONE'.

        Signature:
            str OR int >= 0 -> None
    
        Args:
            Level: str OR int >=0; severity level passed as a non-negative
                integer, or a string alias (case-insensitive)

        Raises:
            TypeError: the passed argument is neither string nor an ineteger
            ValueError: the passed argument is a negative integer, or a string
                representing the unknown level

        Version 1.0.0.0
        """
        self._MinPropagateLevel = _ResolveLevel(Level)
    
    def setMaxPropagateLevel(self, Level: TStrInt) -> None:
        """
        Sets the maximum severity level of a message to be propagated into the
        parent's file handler by a non-negative integer or a string alias. The
        acceptable aliases (case-insensitive) are: 'ALL', 'DEBUG', 'INFO',
        'WARNING', 'ERROR', 'CRITICAL' and 'NONE'.

        Signature:
            str OR int >= 0 -> None
    
        Args:
            Level: str OR int >=0; severity level passed as a non-negative
                integer, or a string alias (case-insensitive)

        Raises:
            TypeError: the passed argument is neither string nor an ineteger
            ValueError: the passed argument is a negative integer, or a string
                representing the unknown level

        Version 1.0.0.0
        """
        self._MaxPropagateLevel = _ResolveLevel(Level)
    
    def getPropagateRange(self) -> int:
        """
        Returns the current min and max severity levels of a message to be
        propagated to a parent's file handler as a 2-tuple of non-negative
        integers.

        Signature:
            None -> tuple(int >= 0, int >= 0)
        
        Version 1.0.0.0
        """
        return (self._MinPropagateLevel, self._MaxPropagateLevel)
    
    def setConsoleStream(self, Stream) -> None:
        """
        Redirects the console output into another stream-like object, which
        must have, at least, write() and flush() methods. Affects all loggers
        within a single tree, even when called from any (grand-) child, since
        the console handler is always attached to the root.
        
        Signature:
            type A -> None
        
        Args:
            Stream: type A; any stream-like object
        
        Version 1.0.0.0
        """
        if self._ConsoleHandler is None:
            if not (self.parent is None):
                self.parent.setConsoleStream(Stream)
        else:
            self.removeHandler(self._ConsoleHandler)
            del self._ConsoleHandler
            self._ConsoleHandler = base_logging.StreamHandler(Stream)
            self._ConsoleHandler.setLevel(ALL)
            self._ConsoleHandler.addFilter(ConsoleHandlerFilter(self))
            self._ConsoleHandler.setFormatter(self._DefaultFormatter)
            self.addHandler(self._ConsoleHandler)