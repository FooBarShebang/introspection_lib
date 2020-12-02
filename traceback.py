#usr/bin/python3
"""
Module introspection_lib.traceback

Implements classes to obtain, store and analyze the stack and exception
traceback.

Functions:
    ParseFramesList(Frames, *, SkipFrames = None):
        list(inspect.FrameInfo)/, int > 0 OR None/
            -> list(tuple(str, str, str, int >= 0, int >= 0, list(str) OR None))

Classes:
    StackTraceback: function / method call stack traceback
    ExceptionTraceback: exception traceback
"""

__version__ = "1.0.1.0"
__date__ = "06-11-2020"
__status__ = "Production"

#imports

#+ standard libraries

import inspect

from types import TracebackType
from typing import List, Tuple, Optional

#types

TIntNone = Optional[int]
TStringList = List[str]
TFramesList = List[inspect.FrameInfo]
TParsedFrame = List[Tuple[str, str, str, int, int, TStringList]]
TTracebackNone = Optional[TracebackType]

#helper functions

def ParseFramesList(Frames: TFramesList, *,
                    SkipFrames: TIntNone = None) -> TParsedFrame:
    """
    Parses the passed list of the inspect.FrameInfo objects into a list of
    tuples of simple atomic and atomic container objects not containg any frame
    object, which helps in avoiding the circular referencing.

    Signature:
        list(inspect.FrameInfo)/, int > 0 OR None/
            -> list(tuple(str, str, str, int >= 0, int >= 0, list(str) OR None))

    Args:
        Frames: list(inspect.FrameInfo); list of FrameInfo objects as named
            tuples
        SkipFrames: (keyword) int > 0 OR None; number of the most inner frames
            to skip as a non-negative integer, otherwise is ignored, defaults
            to None
    
    Returns:
        list(tuple(str, str, str, int > 0, int >= 0, list(str))): a list of
            tuples, possibly empty, with each element (tuple) being the parsed
            frame data not containg the a frame object itself, and the elements
            of each tuple being the path to the source code module, name of the
            caller (module or function / method), the fully qualified name of
            the caller, position index of the offending code line in the module,
            position index of the same line in the provided code sniplet, and
            the code sniplet as a list of the source code lines (strings)
    
    Version 1.0.0.0
    """
    iLen = len(Frames)
    gtuplstResult = []
    if iLen:
        if (isinstance(SkipFrames, int) and (0 < SkipFrames <= (iLen-1))):
            iEnd = iLen - SkipFrames
        else:
            iEnd = iLen
        for iIndex in range(iEnd):
            #resolving module, caller name and qualified name
            Item = Frames[iIndex]
            objFrame = Item.frame
            objModule = inspect.getmodule(objFrame)
            if objModule is None:
                strModule = '<console input>'
            else:
                strModule = objModule.__name__
            strCaller = Item.function
            if strCaller == '<module>':
                strFullName = strModule
            else:
                dictLocals = objFrame.f_locals
                if 'self' in dictLocals:
                    strClass = dictLocals['self'].__class__.__name__
                    strFullName = '.'.join([strModule, strClass, strCaller])
                elif 'cls' in dictLocals:
                    strClass = dictLocals['cls'].__name__
                    strFullName = '.'.join([strModule, strClass, strCaller])
                else:
                    strFullName = '.'.join([strModule, strCaller])
            strFilePath = Item.filename
            #getting content 
            iLineNum = Item.lineno
            iLineIndex = Item.index
            strlstCodeLines = Item.code_context
            #adding entry to the list
            glstTemp = (strFilePath, strCaller, strFullName, iLineNum,
                                                iLineIndex, strlstCodeLines)
            gtuplstResult.append(glstTemp)
    return gtuplstResult

#classes

class StackTraceback():
    """
    Utility class to obtain and analyze the traceback of the current state of
    the call stack up to but excluding the frame, where this object is
    instantiated, and to extract the call chain from it with an option to 'hide'
    the specified number of the deepest (inner) frames. Note that stack
    traceback created is in the reversed order with respect to that of the
    returned by the function inspect.stack(), i.e. the interpreter's loop
    (outmost call) is the first element, and the frame, where this class is
    instantiated, is the last element.
    
    Properties:
        CallChain: (read-only) list(str); list of the names of the callers
        Info: (read-only) str; human-readable frames data
    
    Version 1.0.1.0
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
        
        Version 1.0.1.0
        """
        if (isinstance(ContextLength, int) and ContextLength > 0):
            _ContextLenght = ContextLength
        else:
            _ContextLenght = self.ContextLenght
        if (isinstance(ConsoleWidth, int) and ConsoleWidth > 0):
            self.ConsoleWidth = ConsoleWidth
        tblstTemp = list(reversed(inspect.stack(_ContextLenght)))
        if isinstance(SkipFrames, int) and SkipFrames > 0:
            _SkipFrames = SkipFrames + 1
        else:
            _SkipFrames = 1
        self._lstTraceback = ParseFramesList(tblstTemp, SkipFrames= _SkipFrames)
        #cleaning up, removing the frame objects
        #+ de-referencing the invidual frames
        while len(tblstTemp):
            tblstTemp.pop()
        #+ de-referncing the temporary list
        del tblstTemp
    
    def __del__(self) -> None:
        """
        Special method to ensure proper deletion of the stored data, i.e. the
        parsed traceback data.
        
        Signature:
            None -> None
        
        Version 1.0.1.0
        """
        while len(self._lstTraceback):
            TempFrame = self._lstTraceback.pop()
            for gItem in TempFrame:
                if isinstance(gItem, list):
                    while len(gItem):
                        gItem.pop()
                del gItem
            del TempFrame
        self._lstTraceback = []
    
    #public methods
    
    #+ properties
    
    @property
    def CallChain(self) -> TStringList:
        """
        Extracts and returns the call chain from the stored parsed snapshot of
        the traceback. All callers names are fully qualified.
        
        Signature:
            None -> list(str)
        
        Version 1.0.1.0
        """
        strlstCallers = [Item[2] for Item in self._lstTraceback]
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
        the output width can be specified during instantiation (ContextLength
        and ContextWidth arguments) as non-negative integers; otherwise the
        default values stored in the class attributes ContextLength and
        ConsoleWidth are used.
        
        Signature:
            None -> str
        
        Version 1.0.1.0
        """
        strInfo = ''
        strlstCallers = self.CallChain
        for Frame in self._lstTraceback:
            (strFilePath, strCaller, strFullCaller, iLineNum,
                iLineIndex, strlstCodeLines) = Frame
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
    being handled was raised in. Alternatively, can be used for parsing of a
    traceback of any other exception (including the last one) stored in the
    exception instance itself.
    
    Built upon the functions inspect.trace() and inspect.getinnerframes();
    preserves the order of the frames.
    
    Extends the class StackTraceback and inherits the read-only properties.
    
    Properties:
        CallChain: (read-only) list(str); list of the names of the callers
        Info: (read-only) str; human-readable frames data
    
    Version 1.0.1.0
    """
    
    #special methods
    
    def __init__(self, *, SkipFrames: TIntNone = None,
                            ContextLength: TIntNone = None,
                            ConsoleWidth: TIntNone = None,
                            FromTraceback: TTracebackNone = None) -> None:
        """
        Initialization method. Attempts to retrieve and store the traceback of
        the last raised exception as a a list of frame records for the stack
        between the current frame and the frame in which an exception currently
        being handled was raised in. Can accept up to 3 optional positional
        arguments, which can be passed as the keyword arguments: SkipFrames,
        ConsoleWidth and ConsoleWidth.

        Alternatively, a traceback stored in an exception can be passed as the
        keyword argument FromTraceback, in which case the SkipFrames argument
        is ignored, and the traceback is reconstructed from the passed object.
        
        Signature:
            /int > 0 OR None, int > 0 OR None, int > 0 OR None,
                types.TracebackType OR None/ -> None
        
        Args:
            SkipFrames: (keyword) int > 0; number of the deepest (inner) frames
                to 'hide' in the traceback excluding the initialization method
                itself, which is always removed (default is None -> zero),
                ignored if FromTraceback argument is a proper traceback object
            ContextLength: (keyword) int > 0; total number of lines of the
                source code to retrieve around and including the one, there a
                call was made (default is None -> the value of the class field
                ContextLenght)
            ConsoleWidth: (keyword) int > 0; width to which the source code
                lines must be truncated, including the line's number + 2 extra
                characters (default is None -> the value of the class field
                ConsoleWidth)
            FromTraceback: (keyword) types.TracebackType OR None; an instance of
                a traceback object from which the extract the information, if
                provided and proper - the SkipFrames argument is ignored
                (defaults to None -> actual traceback stack is analyzed)
        
        Version 1.0.1.0
        """
        if (isinstance(ContextLength, int) and ContextLength > 0):
            _ContextLenght = ContextLength
        else:
            _ContextLenght = self.ContextLenght
        if (isinstance(ConsoleWidth, int) and ConsoleWidth > 0):
            self.ConsoleWidth = ConsoleWidth
        if ((not (FromTraceback is None)) and
                                    isinstance(FromTraceback, TracebackType)):
            tblstTemp = inspect.getinnerframes(FromTraceback, _ContextLenght)
            self._lstTraceback = ParseFramesList(tblstTemp)
        else:
            tblstTemp = inspect.trace(_ContextLenght)
            self._lstTraceback = ParseFramesList(tblstTemp,
                                                    SkipFrames = SkipFrames)
        #cleaning up, removing the frame objects
        #+ de-referencing the invidual frames
        while len(tblstTemp):
            tblstTemp.pop()
        #+ de-referncing the temporary list
        del tblstTemp
