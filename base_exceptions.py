#usr/bin/python3
"""
Module introspection_lib.base_exceptions

Implements custom exception classes with the build-in human-readable inspection
of the traceback functionality.

Functions:
    GetObjectClass(gObject):
        type A -> str

Classes:
    TracebackPlugin: left plugin class implementing the built-in traceback
        analysis functionality
    UT_Exception: the base custom exception, parent to all custom exceptions
    UT_TypeError: custom version of TypeError
    UT_ValueError: custom version of ValueError
    UT_AttributeError: custom version of AttributeError
    UT_IndexError: custom version of IndexError
    UT_KeyError: custom version of KeyError
"""

__version__ = "1.0.0.0"
__date__ = "11-11-2020"
__status__ = "Production"

#imports

#+ standard libraries

import sys
import os
import collections
import types
import abc

from typing import Any, List, Optional, Union

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from introspection_lib.traceback import ExceptionTraceback

#types

TIntNone = Optional[int]
TTracebackNone = Optional[types.TracebackType]
TScalarSequence = Union[Any, List[Any]]

#functions

def GetObjectClass(gObject: Any) -> str:
    """
    Helper function. Attempts to extract the class's name of the passed class
    or instance of a class. The fallback option is str(type(Value)) when the
    class's name cannot be extracted.

    Signature:
        type A -> str
    
    Args:
        gObject: type A; the object to be analyzed
    
    Returns:
        str: the determined class or type name
    
    Version 1.0.0.0
    """
    if hasattr(gObject, '__name__'):
        strResult = gObject.__name__
    elif hasattr(gObject, '__class__'):
        strResult = gObject.__class__.__name__
    else:
        strResult = str(type(gObject))
    return strResult

#classes

#+ plugin class

class TracebackPlugin():
    """
    Left plugin class implementing the built-in traceback aalysis functionality.
    Cannot be instantiated by itself, since TypeError will be raised. Must be
    used only as left plugin for sub-classing exceptions.

    Properties:
        Traceback: (read-only) introspection_lib.traceback.ExceptionTraceback
    
    Methods:
        with_traceback(Traceback):
            types.TracebackType -> Exception
    
    Version 1.0.0.0
    """

    #special methods

    def __init__(self, *args, SkipFrames: TIntNone = None,
                             FromTraceback: TTracebackNone = None) -> None:
        """
        Hooks into instantiation of a custom exception. Passes the provided
        positional arguments into the standard parent exception initializer.
        Then if a substitution traceback is passed (FromTraceback keyword) the
        analysis object is created from it and stored (see Traceback property);
        otherwise - it will be created from the actual traceback upon accessing
        Traceback property. In the second case if the SkipFrames was passed as
        a positive integer, the respective number of the innermost frames will
        be skipped. Note, that call of the method with_traceback() overrides
        both the truncation and substitution of the traceback - the actual one
        will be used, including the extension frames.

        Signature:
            /type A, int > 0 OR None, types.TracebackType OR None/ -> None
        
        Args:
            *args: type A; any number of arguments of the exception
            SkipFrames: (keyword) int > 0 OR None; number of the innermost
                frames to remove from the actual traceback, ignored if the
                keyword argument FromTraceback holds a proper traceback object
            FromTraceback: (keyword) types.TracebackType OR None; substitute
                traceback (from another exception) to use; if it is provided and
                holds a proper traceback object the SkipFrames argument is
                ignored
        
        Version 1.0.0.0
        """
        super().__init__(*args)
        self._Traceback = None
        self._SkipFrames = SkipFrames
        if not (FromTraceback is None):
            self._Traceback = ExceptionTraceback(FromTraceback = FromTraceback)

    #added public API

    @property
    def Traceback(self):
        """
        Read-only property returning exception traceback analysis object. If
        such object does not yet exist, it is created 'on the fly' and is stored
        for the future references.

        Signature:
            None -> introspection_lib.traceback.ExceptionTraceback
        
        Version 1.0.0.0
        """
        if (self._Traceback is None):
            if self._SkipFrames is None:
                self._Traceback = ExceptionTraceback(FromTraceback
                                                        = self.__traceback__)
            else:
                self._Traceback = ExceptionTraceback(
                                                SkipFrames = self._SkipFrames)
        return self._Traceback
    
    def with_traceback(self, Traceback: types.TracebackType) -> Exception:
        """
        Overrides the standard exceptions' method; ensures the de-referencig of
        the stored exception traceback instance and sets the corresponding
        'private' attributes to None, thus when requested the traceback analysis
        object will be created from the actual traceback of the exception. Then
        it reverts to the original version of the same method.

        Signature:
            types.TracebackType -> Exception
        
        Args:
            Traceback: types.TracebackType; a traceback object of an exception,
                i.e. the value stored in the exception's attribute __traceback__
        
        Returns:
            Exception: instance of any sub-class of the standard exception, in
                fact, the reference to the instance of the same custom exception
                class, into which this plugin is added
        
        Version 1.0.0.0
        """
        del self._Traceback
        self._Traceback = None
        self._SkipFrames = None
        return super().with_traceback(Traceback)

#+ main classes

class UT_Exception(TracebackPlugin, Exception, abc.ABC):
    """
    Base custom exception, which is considered to be a base class (real or
    virtual) to all custom exceptions. Should be instantiated as:

    * UT_Exception('Message')
    * UT_Exception('Message', SkipFrames = N)
    * UT_Exception('Message', FromTraceback = Some_Traceback)

    Sub-classes the standard Exception and the left plugin TracebackPlugin.

    Attributes:
        args: tuple(str x1); one string element tuple storing the passed message
        __traceback__: types.TracebackType; stores the actual traceback of the
            exception
    
    Properties:
        Traceback: (read-only) introspection_lib.traceback.ExceptionTraceback;
            human readable traceback analysis object, may refer to the actual or
            substituted traceback depending on the mode of instantiation
    
    Methods:
        with_traceback(Traceback):
            types.TracebackType -> UT_Exception

    Version 1.0.0.0
    """

    #special methods

    @classmethod
    def __subclasshook__(cls, C):
        """
        Special class method to modify the behaviour of the standard functions
        issubclass() and isinstance() as follows:
            * Any class having attribute Traceback is considered to be a
                (virtual) sub-class of UT_Exception
            * Any direct or indirect (more than one step) descendant of the
                UT_Exception class is the sub-class of UT_Exception
            * For the sub-classes of UT_Exception the virtual inheritance
                (duck-typing, 'has a' check) is not applicable; only the actual
                sub-classing is concerned
        
        Signature:
            type A -> bool OR NotImplemented
        
        Args:
            C: type A; supposed to be a class / type to be checked for the
                relation with this class
        
        Returns:
            bool OR NotImplemented: special NotImplemented value is returned if
                the passed value is not a class / type (i.e. an instance) or the
                check class (current) is not UT_Exception itself, but its sub-
                class, in which case the usual resultion mechanism is used;
                otherwise either True or False value is returned
        
        Version 1.0.0.0
        """
        if cls is UT_Exception and hasattr(C, '__mro__'):
            #only this class, do not propagate!
            #+ C shold be a class, not an instance!
            if UT_Exception in C.__mro__:
                    #direct child
                gResult = True
            elif hasattr(C, 'Traceback'):  #has required property
                gResult = True
            else:
                gResult = False
        else: #use the standard check mechanism
            gResult = NotImplemented
        return gResult

    def __init__(self, Message: str, *, SkipFrames: TIntNone = None,
                    FromTraceback: TTracebackNone = None) -> None:
        """
        The single mandatory argument (the error message) is stored as the only
        element of the args tuple attribute. If the FromTraceback keyword
        argument holds the proper value, the traceback analysis object is
        created immediately from the substituion object; otherwise its creation
        is delayed until the first access of the property Traceback, in wich
        case the actual traceback can be truncated is SkipFrames is provided as
        a positive integer. Note that if the method with_traceback() is called
        the truncated or substituted traceback is replaced by the actual one,
        including the chained frames.

        Signature:
            str/, int > 0 OR None, types.TracebackType OR None/ -> None
        
        Args:
            Message: str; the error message
            SkipFrames: (keyword) int > 0 OR None; number of the innermost
                frames to remove from the actual traceback, ignored if the
                keyword argument FromTraceback holds a proper traceback object
            FromTraceback: (keyword) types.TracebackType OR None; substitute
                traceback (from another exception) to use; if it is provided and
                holds a proper traceback object the SkipFrames argument is
                ignored
        
        Version 1.0.0.0
        """
        super().__init__(Message, SkipFrames = SkipFrames,
                                    FromTraceback = FromTraceback)

class UT_TypeError(TracebackPlugin, TypeError):
    """
    Custom version of TypeError with the added human-readable traceback
    analysis. Should be instantiated as:

    * UT_TypeError(Value, type / class OR seq(type / class))
    * UT_TypeError(Value, type / class OR seq(type / class), SkipFrames = N)
    * UT_TypeError(Value, type / class OR seq(type / class),
                                                FromTraceback = Some_Traceback)

    Sub-classes the standard TypeError and the left plugin TracebackPlugin, also
    is a virtual sub-class of UT_Exception.

    Attributes:
        args: tuple(str x1); one string element tuple storing the passed message
        __traceback__: types.TracebackType; stores the actual traceback of the
            exception
    
    Properties:
        Traceback: (read-only) introspection_lib.traceback.ExceptionTraceback;
            human readable traceback analysis object, may refer to the actual or
            substituted traceback depending on the mode of instantiation
    
    Methods:
        with_traceback(Traceback):
            types.TracebackType -> UT_TypeError

    Version 1.0.0.0
    """

    #special methods

    def __init__(self, gObject: Any, seqTypes: TScalarSequence, *,
                    SkipFrames: TIntNone = None,
                    FromTraceback: TTracebackNone = None) -> None:
        """
        Converts the two passed mandatory (positional) arguments into a single
        string error message, which is stored as the only element of the args
        tuple attribute. If the FromTraceback keyword argument holds the proper
        value, the traceback analysis object is created immediately from the
        substituion object; otherwise its creation is delayed until the first
        access of the property Traceback, in wich case the actual traceback can
        be truncated is SkipFrames is provided as a positive integer. Note that
        if the method with_traceback() is called the truncated or substituted
        traceback is replaced by the actual one, including the chained frames.

        Signature:
            type A, type B/, int > 0 OR None, types.TracebackType OR None/
                -> None
        
        Args:
            gObject: type A; the object involved
            seqTypes: type B; any single type / class or a sequence of types
                or classes, which the object was expected to be
            SkipFrames: (keyword) int > 0 OR None; number of the innermost
                frames to remove from the actual traceback, ignored if the
                keyword argument FromTraceback holds a proper traceback object
            FromTraceback: (keyword) types.TracebackType OR None; substitute
                traceback (from another exception) to use; if it is provided and
                holds a proper traceback object the SkipFrames argument is
                ignored
        
        Version 1.0.0.0
        """
        if isinstance(seqTypes, collections.abc.Sequence):
            _seqTypes = seqTypes
        else:
            _seqTypes = [seqTypes]
        Message = '{} is not a sub-class of ({}, )'.format(
            GetObjectClass(gObject), ', '.join(map(GetObjectClass, _seqTypes)))
        super().__init__(Message, SkipFrames = SkipFrames,
                                    FromTraceback = FromTraceback)

class UT_ValueError(TracebackPlugin, ValueError):
    """
    Custom version of ValueError with the added human-readable traceback
    analysis. Should be instantiated as:

    * UT_ValueError(Value, 'Ranges message')
    * UT_ValueError(Value, 'Ranges message', SkipFrames = N)
    * UT_ValueError(Value, 'Ranges message', FromTraceback = Some_Traceback)

    Sub-classes the standard ValueError and the left plugin TracebackPlugin,
    also is a virtual sub-class of UT_Exception.

    Attributes:
        args: tuple(str x1); one string element tuple storing the passed message
        __traceback__: types.TracebackType; stores the actual traceback of the
            exception
    
    Properties:
        Traceback: (read-only) introspection_lib.traceback.ExceptionTraceback;
            human readable traceback analysis object, may refer to the actual or
            substituted traceback depending on the mode of instantiation
    
    Methods:
        with_traceback(Traceback):
            types.TracebackType -> UT_ValueError

    Version 1.0.0.0
    """

    #special methods

    def __init__(self, gObject: Any, strRanges: str, *,
                    SkipFrames: TIntNone = None,
                    FromTraceback: TTracebackNone = None) -> None:
        """
        Converts the two passed mandatory (positional) arguments into a single
        string error message, which is stored as the only element of the args
        tuple attribute. If the FromTraceback keyword argument holds the proper
        value, the traceback analysis object is created immediately from the
        substituion object; otherwise its creation is delayed until the first
        access of the property Traceback, in wich case the actual traceback can
        be truncated is SkipFrames is provided as a positive integer. Note that
        if the method with_traceback() is called the truncated or substituted
        traceback is replaced by the actual one, including the chained frames.

        Signature:
            type A, str/, int > 0 OR None, types.TracebackType OR None/ -> None
        
        Args:
            gObject: type A; the object involved
            strRanges: str; explanation on the violated limitations / ranges
            SkipFrames: (keyword) int > 0 OR None; number of the innermost
                frames to remove from the actual traceback, ignored if the
                keyword argument FromTraceback holds a proper traceback object
            FromTraceback: (keyword) types.TracebackType OR None; substitute
                traceback (from another exception) to use; if it is provided and
                holds a proper traceback object the SkipFrames argument is
                ignored
        
        Version 1.0.0.0
        """
        Message = '{} does not meet restriction {}'.format(str(gObject), 
                                                                    strRanges)
        super().__init__(Message, SkipFrames = SkipFrames,
                                    FromTraceback = FromTraceback)

class UT_AttributeError(TracebackPlugin, AttributeError):
    """
    Custom version of AttributeError with the added human-readable traceback
    analysis. Should be instantiated as:

    * UT_AttributeError(Object, 'Attr Name')
    * UT_AttributeError(Object, 'Attr Name', SkipFrames = N)
    * UT_AttributeError(Object, 'Attr Name', FromTraceback = Some_Traceback)

    Sub-classes the standard AttributeError and the left plugin TracebackPlugin,
    also is a virtual sub-class of UT_Exception.

    Attributes:
        args: tuple(str x1); one string element tuple storing the passed message
        __traceback__: types.TracebackType; stores the actual traceback of the
            exception
    
    Properties:
        Traceback: (read-only) introspection_lib.traceback.ExceptionTraceback;
            human readable traceback analysis object, may refer to the actual or
            substituted traceback depending on the mode of instantiation
    
    Methods:
        with_traceback(Traceback):
            types.TracebackType -> UT_AttributeError

    Version 1.0.0.0
    """

    #special methods

    def __init__(self, gObject: Any, strAttribute: str, *,
                    SkipFrames: TIntNone = None,
                    FromTraceback: TTracebackNone = None) -> None:
        """
        Converts the two passed mandatory (positional) arguments into a single
        string error message, which is stored as the only element of the args
        tuple attribute. If the FromTraceback keyword argument holds the proper
        value, the traceback analysis object is created immediately from the
        substituion object; otherwise its creation is delayed until the first
        access of the property Traceback, in wich case the actual traceback can
        be truncated is SkipFrames is provided as a positive integer. Note that
        if the method with_traceback() is called the truncated or substituted
        traceback is replaced by the actual one, including the chained frames.

        Signature:
            type A, str/, int > 0 OR None, types.TracebackType OR None/ -> None
        
        Args:
            gObject: type A; the object (class or instance) involved
            strAttribute: str; name of the involved attribute
            SkipFrames: (keyword) int > 0 OR None; number of the innermost
                frames to remove from the actual traceback, ignored if the
                keyword argument FromTraceback holds a proper traceback object
            FromTraceback: (keyword) types.TracebackType OR None; substitute
                traceback (from another exception) to use; if it is provided and
                holds a proper traceback object the SkipFrames argument is
                ignored
        
        Version 1.0.0.0
        """
        Message = '{}.{}'.format(GetObjectClass(gObject), strAttribute)
        super().__init__(Message, SkipFrames = SkipFrames,
                                    FromTraceback = FromTraceback)

class UT_IndexError(TracebackPlugin, IndexError):
    """
    Custom version of IndexError with the added human-readable traceback
    analysis. Should be instantiated as:

    * UT_IndexError('Object name', Index)
    * UT_IndexError('Object name', Index, SkipFrames = N)
    * UT_IndexError('Object name', Index, FromTraceback = Some_Traceback)

    Sub-classes the standard IndexError and the left plugin TracebackPlugin,
    also is a virtual sub-class of UT_Exception.

    Attributes:
        args: tuple(str x1); one string element tuple storing the passed message
        __traceback__: types.TracebackType; stores the actual traceback of the
            exception
    
    Properties:
        Traceback: (read-only) introspection_lib.traceback.ExceptionTraceback;
            human readable traceback analysis object, may refer to the actual or
            substituted traceback depending on the mode of instantiation
    
    Methods:
        with_traceback(Traceback):
            types.TracebackType -> UT_IndexError

    Version 1.0.0.0
    """

    #special methods

    def __init__(self, Name: str, Index: int, *,
                    SkipFrames: TIntNone = None,
                    FromTraceback: TTracebackNone = None) -> None:
        """
        Converts the two passed mandatory (positional) arguments into a single
        string error message, which is stored as the only element of the args
        tuple attribute. If the FromTraceback keyword argument holds the proper
        value, the traceback analysis object is created immediately from the
        substituion object; otherwise its creation is delayed until the first
        access of the property Traceback, in wich case the actual traceback can
        be truncated is SkipFrames is provided as a positive integer. Note that
        if the method with_traceback() is called the truncated or substituted
        traceback is replaced by the actual one, including the chained frames.

        Signature:
            str, int/, int > 0 OR None, types.TracebackType OR None/ -> None
        
        Args:
            Name: str; name of a sequence object involved
            Index: index; element's index, which is missing
            SkipFrames: (keyword) int > 0 OR None; number of the innermost
                frames to remove from the actual traceback, ignored if the
                keyword argument FromTraceback holds a proper traceback object
            FromTraceback: (keyword) types.TracebackType OR None; substitute
                traceback (from another exception) to use; if it is provided and
                holds a proper traceback object the SkipFrames argument is
                ignored
        
        Version 1.0.0.0
        """
        Message = 'Out of range index {}[{}]'.format(Name, Index)
        super().__init__(Message, SkipFrames = SkipFrames,
                                    FromTraceback = FromTraceback)

class UT_KeyError(TracebackPlugin, KeyError):
    """
    Custom version of KeyError with the added human-readable traceback
    analysis. Should be instantiated as:

    * UT_KeyError('Object name', 'Key Name')
    * UT_KeyError('Object name', 'Key Name', SkipFrames = N)
    * UT_KeyError('Object name', 'Key Name', FromTraceback = Some_Traceback)

    Sub-classes the standard KeyError and the left plugin TracebackPlugin, also
    is a virtual sub-class of UT_Exception.

    Attributes:
        args: tuple(str x1); one string element tuple storing the passed message
        __traceback__: types.TracebackType; stores the actual traceback of the
            exception
    
    Properties:
        Traceback: (read-only) introspection_lib.traceback.ExceptionTraceback;
            human readable traceback analysis object, may refer to the actual or
            substituted traceback depending on the mode of instantiation
    
    Methods:
        with_traceback(Traceback):
            types.TracebackType -> UT_KeyError

    Version 1.0.0.0
    """

    #special methods

    def __init__(self, Name: str, Key: str, *,
                    SkipFrames: TIntNone = None,
                    FromTraceback: TTracebackNone = None) -> None:
        """
        Converts the two passed mandatory (positional) arguments into a single
        string error message, which is stored as the only element of the args
        tuple attribute. If the FromTraceback keyword argument holds the proper
        value, the traceback analysis object is created immediately from the
        substituion object; otherwise its creation is delayed until the first
        access of the property Traceback, in wich case the actual traceback can
        be truncated is SkipFrames is provided as a positive integer. Note that
        if the method with_traceback() is called the truncated or substituted
        traceback is replaced by the actual one, including the chained frames.

        Signature:
            str, str/, int > 0 OR None, types.TracebackType OR None/ -> None
        
        Args:
            Name: str; name of a mapping object involved
            Key: str; name of the key, which is missing
            SkipFrames: (keyword) int > 0 OR None; number of the innermost
                frames to remove from the actual traceback, ignored if the
                keyword argument FromTraceback holds a proper traceback object
            FromTraceback: (keyword) types.TracebackType OR None; substitute
                traceback (from another exception) to use; if it is provided and
                holds a proper traceback object the SkipFrames argument is
                ignored
        
        Version 1.0.0.0
        """
        Message = 'Key not found {}[{}]'.format(Name, Key)
        super().__init__(Message, SkipFrames = SkipFrames,
                                    FromTraceback = FromTraceback)
