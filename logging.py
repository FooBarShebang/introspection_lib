#usr/bin/python3
"""
Module introspection_lib.logging

Implements custom logging classes.

Classes:
    DummyLogger: all messages are dumped into NIL-stream
    DualLogger: can simulataneously log into a console and a file
"""

__version__ = "1.0.0.0"
__date__ = "26-11-2020"
__status__ = "Development"

#imports

#+ standard libraries

import os
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

class DummyLogger(base_logging.Logger):
    """
    Specialized sub-class of the logging.Logger class (Standard Python Library),
    which upon instantiation has no parent logger, but an instance of the class
    NullHandler attached as a handler. Inherits all API from the super class
    without changes except for the ininitalization method.

    Version 1.0.0.0
    """

    #special methods

    def __init__(self, Name: TStrNone = None, *args, **kwargs) -> None:
        """
        Initialization method. Assigns a name, creates and attaches a single
        handler - NullHandler to the instance.

        Signature:
            str OR None/, ..., *, .../ -> None
        
        Args:
            Name: (optional) str; a name to be assigned to a logger, defaults to
                None, in which case the class' name is used instead
            *args: (optional) type A; any number of optional positional
                arguments, simply ignored - for the compatibility only
            **kwargs: (keyword) type B; any number of optional keyword
                arguments, simply ignored - for the compatibility only
        
        Version 1.0.0.0
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

    Inherits the API from the super class, but overwrites few public methods
    and adds some new methods.

    Methods:
        getChild(Name):
            str -> DualLogger
        setLevel(Level):
            str OR int >= 0 -> int >= 0
        setMinConsoleLevel(Level):
            str OR int >= 0 -> int >= 0
        setMaxConsoleLevel(Level):
            str OR int >= 0 -> int >= 0
        getConsoleRange():
            None -> tuple(int >= 0, int >= 0)
        setLogFile(File = None):
            /str/ -> None
        disableFileLogging():
            None -> None
        setMinFileLevel(Level):
            str OR int >= 0 -> int >= 0
        setMaxFileLevel(Level):
            str OR int >= 0 -> int >= 0
        getFileRange():
            None -> tuple(int >= 0, int >= 0)
        setMinPropagateLevel(Level):
            str OR int >= 0 -> int >= 0
        setMaxPropagateLevel(Level):
            str OR int >= 0 -> int >= 0
        getPropagateRange():
            None -> tuple(int >= 0, int >= 0)

    Version 1.0.0.0
    """

    #special methods

    def __init__(self, Name: TStrNone = None, *args, **kwargs) -> None:
        """
        Initialization method. Assigns a name, creates and attaches a single
        handler - NullHandler to the instance. Special keywoard argument Parent
        can be passed referencing to another instance of DualLogger class as the
        parent of this instance. Do not use this functionality directly - it is
        reserved for the implemetation of the getChild() method.

        Signature:
            str OR None/, DualLogger, ..., *, .../ -> None
        
        Args:
            Name: (optional) str; a name to be assigned to a logger, defaults to
                None, in which case the class' name is used instead
            *args: (optional) type A; any number of optional positional
                arguments, simply ignored - for the compatibility only
            **kwargs: (keyword) type B; any number of optional keyword
                arguments, simply ignored - for the compatibility only
        
        Version 1.0.0.0
        """
        if isinstance(Name, str):
            strName = Name
        else:
            strName = self.__class__.__name__
        Parent = kwargs.get('Parent', None)
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
            objTemp = base_logging.StreamHandler()
            objTemp.setLevel(ALL)
            self.addHandler(objTemp)
            self.propagate = False
        else:
            self.propagate = True
        self.setLevel('ALL')
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
            str OR int >= 0 -> int >= 0
    
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
            str OR int >= 0 -> int >= 0
    
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
            str OR int >= 0 -> int >= 0
    
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
        pass is the same. If the file name (path) is not provided, the log file
        is created is placed into the current working folder with the base file-
        name as '{YYYYMMDD_HHMM}_{logger.name}.log'. The already existing log
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
            strTime = datetime.datetime.now().strftime('%Y%m%d_%H%M')
            strName = '{}_{}.log'.format(strTime, self.name)
            strFilePath = os.path.abspath(strName)
        if not (self._FileHandler is None) and self._LogFile != strFilePath:
            self.disableFileLogging()
        if self._FileHandler is None:
            self._FileHandler = base_logging.FileHandler(strFilePath)
            self._FileHandler.setLevel(ALL)
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
            str OR int >= 0 -> int >= 0
    
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
        Sets the minimum severity level of the output into own log file by a
        non-negative integer or a string alias. The acceptable aliases
        (case-insensitive) are: 'ALL', 'DEBUG', 'INFO', 'WARNING', 'ERROR',
        'CRITICAL' and 'NONE'.

        Signature:
            str OR int >= 0 -> int >= 0
    
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
            str OR int >= 0 -> int >= 0
    
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
            str OR int >= 0 -> int >= 0
    
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