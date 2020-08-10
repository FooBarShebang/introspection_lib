#usr/bin/python3
"""
Module introspection_lib.traceback

Implements classes to obtain, store and analyze the stack and exception
traceback.

Classes:
    StackTraceback: function / method call stack traceback
    ExceptionTraceback: exception traceback
"""

__version__ = "1.0.0.0"
__date__ = "10-08-2020"
__status__ = "Production"

#imports

#+ standard libraries

import inspect

import os

from typing import TypeVar, List

#types

TIntNone = TypeVar('TStrNone', int, None)
TStringList = List[str]

#classes

class StackTraceback():
    """
    Utility class to obtain and analyze the traceback of the current state of
    the call stack up to the frame, where this object is instantiated, and to
    extract the call chain from it with an option to 'hide' the specified number
    of the deepest (inner) frames. Note that stack traceback created is in the
    reversed order with respect to that of the returned by the function
    inspect.stack(), i.e. the interpreter's loop (outmost call) is the first
    element, and the frame, where this class is instantiated, is the last
    element.
    
    Properties:
        CallChain: (read-only) list(str); list of the names of the callers
        Info: (read-only) str; human-readable frames data
    
    Version 1.0.0.0
    """
    
    #class data attributes
    
    ConsoleWidth: int = 80 #max width of the lines in the Info output
    
    ContextLenght: int = 3 #number of the lines of the source code per frame
    
    #special methods
    
    def __init__(self, *, SkipFrames: TIntNone = None,
                            ContextLength: TIntNone = None,
                            ConsoleWidth: TIntNone = None) -> None:
        """
        Initialization method. Attempts to retrieve and store the traceback of
        the current stack excluding the instantiation method itself. Can accept
        up to 3 keyword arguments: SkipFrames, ContextLength, ConsoleWidth.
        
        Signature:
            /int > 0 OR None, int > 0 OR None, int > 0 OR None/ -> None
        
        Args:
            SkipFrames: (keyword) int > 0; number of the deepest (inner) frames
                to 'hide' in the traceback excluding the initialization method
                itself, which is always removed (default is None -> zero)
            ContextLength: (keyword) int > 0; total number of lines of the
                source code to retrieve around and including the one, there a
                call was made (default is None -> the value of the class field
                ContextLenght)
            ConsoleWidth: (keyword) int > 0; width to which the source code
                lines must be truncated, including the line's number + 2 extra
                characters (default is None -> the value of the class field
                ConsoleWidth)
        
        Version 1.0.0.0
        """
        if (isinstance(ContextLength, int) and ContextLength > 0):
            self.ContextLenght = ContextLength
        if (isinstance(ConsoleWidth, int) and ConsoleWidth > 0):
            self.ConsoleWidth = ConsoleWidth
        try:
            tblstTemp = list(reversed(inspect.stack(self.ContextLenght)))
            if (isinstance(SkipFrames, int) and
                                        (0 < SkipFrames < (len(tblstTemp)-1))):
                self._tblstTraceback = tblstTemp[ : -(SkipFrames + 1)]
            else:
                self._tblstTraceback = tblstTemp[ : - 1]
            del tblstTemp
        except:
            self._tblstTraceback = None
    
    def __del__(self) -> None:
        """
        Special method to ensure proper deletion of the frame objects references
        when the class instance is deleted, so to avoid orphan references.
        
        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        if not (self._tblstTraceback is None):
            while len(self._tblstTraceback):
                try:
                    TempFrame = self._tblstTraceback.pop()
                    del TempFrame
                except:
                    pass
            del self._tblstTraceback
        self._tblstTraceback = None
    
    #public methods
    
    #+ properties
    
    @property
    def CallChain(self) -> TStringList:
        """
        Extracts and returns the call chain from the stored snapshot of the
        the traceback. All callers names are fully qualified.
        
        Signature:
            None -> list(str)
        
        Version 1.0.0.0
        """
        strlstCallers = []
        if not (self._tblstTraceback is None):
            for Frame in self._tblstTraceback:
                objFrame = Frame.frame
                objModule = inspect.getmodule(objFrame)
                if objModule is None:
                    strModule = '<console input>'
                else:
                    strModule = objModule.__name__
                strCaller = Frame.function
                if strCaller == '<module>':
                    strlstCallers.append(strModule)
                else:
                    dictLocals = objFrame.f_locals
                    if 'self' in dictLocals:
                        strClass = dictLocals['self'].__class__.__name__
                        strlstCallers.append('.'.join([strModule, strClass,
                                                                    strCaller]))
                    elif 'cls' in dictLocals:
                        strClass = dictLocals['cls'].__name__
                        strlstCallers.append('.'.join([strModule, strClass,
                                                                    strCaller]))
                    else:
                        strlstCallers.append('.'.join([strModule, strCaller]))
        return strlstCallers
    
    @property
    def Info(self) -> str:
        """
        Prepares and returns a human-readable representation of the frames
        within the obtained traceback as a single string composed of multiple
        lines separated by the new-line character ('\n'). For each frame record
        the first line indicates the fully qualified name of the caller, and the
        second line - the path to the corresponding module and the line number
        in the source code, where the call has occurred. These lines are
        followed by the extract from the source code containing a specified
        number of lines centered around the one, where the call has occurred.
        The lines are prefixed with the line number left padded when required
        with zero in order to preserve the indentation. The line, where the
        call has occurred is indicated by '>' character. The lines are truncated
        when required such that the total length together with the line number
        prefix (and two extra characters) does not exceed the specified width
        of the output. The number of the source code lines per frame as well as
        the output width can be specified during instantiation (iContext and
        iWidth arguments) as non-negative integers; otherwise the default values
        stored in the class attributes ContextLength and ConsoleWidth are used.
        
        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        strInfo = ''
        strlstCallers = self.CallChain
        if len(strlstCallers):
            for iIdx, Frame in enumerate(self._tblstTraceback):
                strFilePath = Frame.filename
                iLineNum = Frame.lineno
                strCaller = Frame.function
                strFullCaller = strlstCallers[iIdx]
                strlstCodeLines = Frame.code_context
                iLineIndex = Frame.index
                if not (strlstCodeLines is None):
                    iMaxDigits = len(str(iLineNum + iLineIndex))
                    if strCaller == '<module>':
                        strCallerInfo = 'In module {}'.format(strFullCaller)
                    else:
                        strCallerInfo = 'Caller {}()'.format(strFullCaller)
                    strFileInfo = 'Line {} in {}'.format(iLineNum, strFilePath)
                    strlstCodeInfo = []
                    for iLineIdx, _strLine in enumerate(strlstCodeLines):
                        strLine = _strLine.rstrip()
                        iRealLineNum = iLineNum - iLineIndex + iLineIdx
                        strLineNum = str(iRealLineNum)
                        while len(strLineNum) < iMaxDigits:
                            strLineNum = '0{}'.format(strLineNum)
                        if iRealLineNum == iLineNum:
                            strLineNum = '>{} '.format(strLineNum)
                        else:
                            strLineNum = ' {} '.format(strLineNum)
                        if len(strLine) > (self.ConsoleWidth - 2 - iMaxDigits):
                            strFullLine = '{}{}...'.format(strLineNum,
                                strLine[ : self.ConsoleWidth - 5 - iMaxDigits])
                        else:
                            strFullLine = '{}{}'.format(strLineNum, strLine)
                        strlstCodeInfo.append(strFullLine)
                    strCodeInfo = '\n'.join(strlstCodeInfo)
                    strInfo = '\n'.join([strInfo, strCallerInfo, strFileInfo,
                                                                strCodeInfo])
                else:
                    strInfo = '\n'.join([strInfo, '<console input>',
                                'Line {} in console input'.format(iLineNum)])
        if len(strInfo):
            strInfo = strInfo.lstrip()
        return strInfo

class ExceptionTraceback(StackTraceback):
    """
    Utility class to obtain and analyze the traceback of the last raised
    exception currently being handled as a a list of frame records for the stack
    between the current frame and the frame in which an exception currently
    being handled was raised in. Built upon the function inspect.trace();
    preserves the order of the frames.
    
    Extends the class StackTraceback and inherits the read-only properties.
    
    Properties:
        CallChain: (read-only) list(str); list of the names of the callers
        Info: (read-only) str; human-readable frames data
    
    Version 1.0.0.0
    """
    
    #special methods
    
    def __init__(self, *, SkipFrames: TIntNone = None,
                            ContextLength: TIntNone = None,
                            ConsoleWidth: TIntNone = None) -> None:
        """
        Initialization method. Attempts to retrieve and store the traceback of
        the last raised exception as a a list of frame records for the stack
        between the current frame and the frame in which an exception currently
        being handled was raised in. Can accept up to 3 optional positional
        arguments, which can also be passed as the keyword arguments: iSkip,
        iContext, iWidth.
        
        Signature:
            /int > 0 OR None, int > 0 OR None, int > 0 OR None/ -> None
        
        Args:
            SkipFrames: (keyword) int > 0; number of the deepest (inner) frames
                to 'hide' in the traceback excluding the initialization method
                itself, which is always removed (default is None -> zero)
            ContextLength: (keyword) int > 0; total number of lines of the
                source code to retrieve around and including the one, there a
                call was made (default is None -> the value of the class field
                ContextLenght)
            ConsoleWidth: (keyword) int > 0; width to which the source code
                lines must be truncated, including the line's number + 2 extra
                characters (default is None -> the value of the class field
                ConsoleWidth)
        
        Version 1.0.0.0
        """
        if (isinstance(ContextLength, int) and ContextLength > 0):
            self.ContextLenght = ContextLength
        if (isinstance(ConsoleWidth, int) and ConsoleWidth > 0):
            self.ConsoleWidth = ConsoleWidth
        try:
            tblstTemp = inspect.trace(self.ContextLenght)
            if (isinstance(SkipFrames, int) and
                                        (0 < SkipFrames < (len(tblstTemp)-1))):
                self._tblstTraceback = tblstTemp[ : -SkipFrames ]
            else:
                self._tblstTraceback = tblstTemp
            del tblstTemp
        except:
            self._tblstTraceback = None