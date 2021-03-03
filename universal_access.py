#usr/bin/python3
"""
Module introspection_lib.universal_access

Implements functions to provide unified access to the elements of sequences,
keys of mapping type objects and attributes of classes / instances, with the
support for nested elements path.

Functions:
    GetData(gObject, gPath):
        type A, str OR int -> type B
    GetDataDefault(gObject, gPath, gValue):
        type A, str OR int, type B -> type C
    SetDataStrict(gObject, gPath, gValue):
        type A, str OR int, type B -> None
    SetData(gObject, gPath, gValue):
        type A, str OR int, type B -> None
    FlattenPath(gPath):
        str OR int OR seq(type A) -> list(str OR int)
    GetElement(gObject, gPath, *, bStrict = True, gDefault = None):
        type A, str OR int OR seq(type B)/, *, bool, type C/ -> type D
    SetElement(gObject, gPath, gValue, *, bStrict = True):
        type A, str OR int OR seq(type B), type C/, *, bool/ -> None
"""

__version__ = "1.0.0.0"
__date__ = "03-03-2021"
__status__ = "Development"

#imports

#+ standard libraries

import sys
import os
import collections

from typing import Any, Union, Sequence, List, Optional

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

from introspection_lib.base_exceptions import UT_TypeError
from introspection_lib.base_exceptions import UT_ValueError
from introspection_lib.base_exceptions import UT_AttributeError
from introspection_lib.base_exceptions import UT_KeyError
from introspection_lib.base_exceptions import UT_IndexError
from introspection_lib.base_exceptions import GetObjectClass

#types

TPathElement = Union[int, str]
TCannonicalPath = List[TPathElement]
TGenericPath = Union[int, str, Sequence[Any]]

#functions

def GetData(gObject: Any, gPath: TPathElement) -> Any:
    """
    Universal 'read' access to an element of a list, key : value pair entry of
    a mapping type or an attribute of a generic class or instance. Raises
    exceptions compatible with (sub-classes of) the standard exceptions
    IndexError, KeyError or AttributeError, which should be normally raised
    upon 'read' access to a non-existing element.
    
    Signature:
        type A, str OR int -> type B
    
    Args:
        gObject: type A; the object to be inspected
        gPath: str OR int; the attribute name / key or index of the element to
            be accessed
    
    Returns:
        type B: the value of the found by attribute name, key or index element
    
    Raises:
        UT_TypeError: type mismatch between object and path - sequence object
            and non-integer path, non-sequence object and non-string path, OR
            the path is neither an integer or a string
        UT_IndexError: object is a sequence, and path is an integer, but outside
            the range of the acceptable indexes, defined by the length of the
            sequence
        UT_KeyError: object is a mapping type, and path is a string, but it is
            not found among the keys
        UT_AttributeError: object is a genric class or instance, and path is a
            string, but it is not found among the attributes
    
    Version 1.0.0.0
    """
    if not isinstance(gPath, (int, str)):
        raise UT_TypeError(gPath, [int, str], SkipFrames = 1)
    if isinstance(gObject, collections.abc.Sequence):
        if not isinstance(gPath, int):
            raise UT_TypeError(gPath, int, SkipFrames = 1)
        iLen = len(gObject)
        if (gPath < (- iLen)) or (gPath >= iLen):
            strName = 'passed sequence {}'.format(GetObjectClass(gObject))
            raise UT_IndexError(strName, gPath, SkipFrames = 1)
        gResult = gObject[gPath]
    else:
        if not isinstance(gPath, str):
            raise UT_TypeError(gPath, str, SkipFrames = 1)
        if isinstance(gObject, collections.abc.Mapping):
            if not gPath in gObject:
                strName = 'passed mapping {}'.format(GetObjectClass(gObject))
                raise UT_KeyError(strName, gPath, SkipFrames = 1)
            gResult = gObject[gPath]
        else:
            if not hasattr(gObject, gPath):
                raise UT_AttributeError(gObject, gPath, SkipFrames = 1)
            gResult = getattr(gObject, gPath)
    return gResult

def GetDataDefault(gObject: Any, gPath: TPathElement, gValue: Any) -> Any:
    """
    Universal 'read' access to an element of a list, key : value pair entry of
    a mapping type or an attribute of a generic class or instance with a default
    value, which should be returned upon 'read' access to a non-existing element
    instead of raising of a respective exception.
    
    Signature:
        type A, str OR int, type B -> type C
    
    Args:
        gObject: type A; the object to be inspected
        gPath: str OR int; the attribute name / key or index of the element to
            be accessed
        gValue: type B; the default value to return, if such element is not
            found
    
    Returns:
        type C: the value of the found by attribute name, key or index element,
            OR the passed default value if such element is not found
    
    Raises:
        UT_TypeError: type mismatch between object and path - sequence object
            and non-integer path, non-sequence object and non-string path, OR
            the path is neither an integer or a string
    
    Version 1.0.0.0
    """
    if not isinstance(gPath, (int, str)):
        raise UT_TypeError(gPath, [int, str], SkipFrames = 1)
    if isinstance(gObject, collections.abc.Sequence):
        if not isinstance(gPath, int):
            raise UT_TypeError(gPath, int, SkipFrames = 1)
        iLen = len(gObject)
        if (gPath < (- iLen)) or (gPath >= iLen):
            gResult = gValue
        else:
            gResult = gObject[gPath]
    else:
        if not isinstance(gPath, str):
            raise UT_TypeError(gPath, str, SkipFrames = 1)
        if isinstance(gObject, collections.abc.Mapping):
            gResult = gObject.get(gPath, gValue)
        else:
            gResult = getattr(gObject, gPath, gValue)
    return gResult

def SetDataStrict(gObject: Any, gPath: TPathElement, gValue: Any) -> None:
    """
    Universal 'write' access to an element of a list, key : value pair entry of
    a mapping type or an attribute of a generic class or instance, but only to
    the existing ones of the mutable objects. New attributes, sequence elements
    or mapping type entries cannot be created even if the object itself is
    mutable. Existing elements of the immutable sequences or exsiting entries of
    the immutable mapping type objects cannot be modified.
    
    Signature:
        type A, str OR int, type B -> None
    
    Args:
        gObject: type A; the object to be inspected
        gPath: str OR int; the attribute name / key or index of the element to
            be accessed
        gValue: type B; the value assign
    
    Raises:
        UT_TypeError: object (first argument) is immutable, OR type mismatch
            between object and path - sequence object and non-integer path,
            non-sequence object and non-string path, OR the path is neither an
            integer or a string
        UT_IndexError: object is a sequence, and path is an integer, but outside
            the range of the acceptable indexes, defined by the length of the
            sequence
        UT_KeyError: object is a mapping type, and path is a string, but it is
            not found among the keys
        UT_AttributeError: object is a genric class or instance, and path is a
            string, but it is not found among the attributes
    
    Version 1.0.0.0
    """
    if not isinstance(gPath, (int, str)):
        raise UT_TypeError(gPath, [int, str], SkipFrames = 1)
    if isinstance(gObject, collections.abc.Sequence):
        if not isinstance(gObject, collections.abc.MutableSequence):
            raise UT_TypeError(gObject, collections.abc.MutableSequence,
                                                                SkipFrames = 1)
        if not isinstance(gPath, int):
            raise UT_TypeError(gPath, int, SkipFrames = 1)
        iLen = len(gObject)
        if (gPath < (- iLen)) or (gPath >= iLen):
            strName = 'passed sequence {}'.format(GetObjectClass(gObject))
            raise UT_IndexError(strName, gPath, SkipFrames = 1)
        gObject[gPath] = gValue
    else:
        if not isinstance(gPath, str):
            raise UT_TypeError(gPath, str, SkipFrames = 1)
        if isinstance(gObject, collections.abc.Mapping):
            if not isinstance(gObject, collections.abc.MutableMapping):
                raise UT_TypeError(gObject, collections.abc.MutableMapping,
                                                                SkipFrames = 1)
            if not gPath in gObject:
                strName = 'passed mapping {}'.format(GetObjectClass(gObject))
                raise UT_KeyError(strName, gPath, SkipFrames = 1)
            gObject[gPath] = gValue
        else:
            if not hasattr(gObject, gPath):
                raise UT_AttributeError(gObject, gPath, SkipFrames = 1)
            setattr(gObject, gPath, gValue)

def SetData(gObject: Any, gPath: TPathElement, gValue: Any) -> None:
    """
    Universal 'write' access to an element of a list, key : value pair entry of
    a mapping type or an attribute of a generic class or instance. If such
    element is not found, it is created automatically, unless the object is
    immutable. In the case of a mutable sequence type object, the new element
    is prepended as a first element or appended as the last one if the passed
    index is outside the current range.
    
    The elements of the immutable sequences or entries in the  immutable mapping
    types cannot be modified, as well as new elements / entries cannot be added.
    
    Signature:
        type A, str OR int, type B -> None
    
    Args:
        gObject: type A; the object to be inspected
        gPath: str OR int; the attribute name / key or index of the element to
            be accessed
        gValue: type B; the value assign
    
    Raises:
        UT_TypeError: object (first argument) is immutable, OR type mismatch
            between object and path - sequence object and non-integer path,
            non-sequence object and non-string path, OR the path is neither an
            integer or a string
    
    Version 1.0.0.0
    """
    if not isinstance(gPath, (int, str)):
        raise UT_TypeError(gPath, [int, str], SkipFrames = 1)
    if isinstance(gObject, collections.abc.Sequence):
        if not isinstance(gObject, collections.abc.MutableSequence):
            raise UT_TypeError(gObject, collections.abc.MutableSequence,
                                                                SkipFrames = 1)
        if not isinstance(gPath, int):
            raise UT_TypeError(gPath, int, SkipFrames = 1)
        iLen = len(gObject)
        if gPath < (- iLen):
            gObject.insert(0, gValue)
        elif gPath >= iLen:
            gObject.append(gValue)
        else:
            gObject[gPath] = gValue
    else:
        if not isinstance(gPath, str):
            raise UT_TypeError(gPath, str, SkipFrames = 1)
        if isinstance(gObject, collections.abc.Mapping):
            if not isinstance(gObject, collections.abc.MutableMapping):
                raise UT_TypeError(gObject, collections.abc.MutableMapping,
                                                                SkipFrames = 1)
            gObject[gPath] = gValue
        else:
            setattr(gObject, gPath, gValue)

def FlattenPath(gPath: TGenericPath) -> TCannonicalPath:
    """
    Flattens a nested generic path definition into a plain list of only strings
    and integers defining a navigation path within a nested structured object,
    with each element in the path being an integer index or a string key or
    attribute name. The input is supposed to be a string, an integer or a flat
    or nested sequence of only integers and strings. Any string in the input may
    encode multiple levels using dot notation.
    
    Signature:
        str OR int OR seq(type A) -> list(str OR int)
    
    Args:
        gPath: str OR int OR seq(type A); the generic nested path description
            to be flattened
    
    Returns:
        list(str OR int): the flattened nested path description
    
    Raises:
        UT_TypeError: the passed generic path is not an integer, a string or
            a (nested) sequence of only strings and integers
    
    Version 1.0.0.0
    """
    if isinstance(gPath, str):
        lstResult = gPath.split(".")
    elif isinstance(gPath, int):
        lstResult = [gPath]
    elif isinstance(gPath, collections.abc.Sequence):
        lstResult = []
        for gItem in gPath:
            try:
                lstTemp = FlattenPath(gItem)
            except UT_TypeError as err:
                objError = UT_TypeError(1, int, SkipFrames = 1)
                objError.args = (err.args[0], )
                raise objError from None
            lstResult.extend(lstTemp)
    else:
        raise UT_TypeError(gPath, [int, str, collections.abc.Sequence],
                                                                SkipFrames = 1)
    return lstResult

def GetElement(gObject: Any, gPath: TGenericPath, *,
                bStrict: Optional[bool] = True,
                gDefault: Optional[Any] = None) -> Any:
    """
    Attempts to retrieve the value of an element (key, attribute) of the nested
    structured object (including nested sequences) defined by a generic path.
    Can operate in two modes: 'strict' and 'relaxed'. In the strict mode an
    exception is raised if the path is incorrect, i.e., at least, one element
    of the path is not found. In the 'relaxed' mode a default value is returned
    is the path is incorrect.
    
    Signature:
        type A, str OR int OR seq(type B)/, *, bool, type C/ -> type D
    
    Args:
        gObject: type A; the object to be inspected
        gPath: str OR int OR seq(type B); the generic path to the end node
            of a nested struture object
        bStrict: (keyword) bool; the flag if the strict access mode is to be
            used, defaults to True
        gDefault: (keyword) type C; the default value to return, if any level
            element is not found along the path, defaults to None, has an effect
            only if the bStrict flag is False
    
    Returns:
        type D: the value of the last element along the passed path, OR the
            passed default value if such element is not found and the requested
            mode is not stict
    
    Raises:
        UT_TypeError: the passed generic path is not an integer, a string or
            a (nested) sequence of only strings and integers, OR type mismatch
            between object level and path element - sequence object level
            and non-integer path element, non-sequence object level and
            non-string path element
        UT_ValueError: the passed generic path is an empty sequence
        UT_IndexError: an object along the path is a sequence, and the
            respective access index is outside the range - 'strict' mode only
        UT_KeyError: an object along the path is a mapping type, and the
            respective access key is not found - 'strict' mode only
        UT_AttributeError: an object along the path is a genric class or
            instance, and the respective attribute is not found - 'strict' mode
            only
    
    Version 1.0.0.0
    """
    #convert the path into the canonical form - and check that it is not empty
    try:
        lstPath = FlattenPath(gItem)
    except UT_TypeError as err:
        objError = UT_TypeError(1, int, SkipFrames = 1)
        objError.args = (err.args[0], )
        raise objError from None
    if not len(lstPath):
        raise UT_ValueError(gPath, 'not empty path', SkipFrames = 1)
    #walk the object structure
    gCurrentObject = gObject
    strName = GetObjectClass(gTemp)
    for gItem in lstPath:
        #check the current level type to prepare the exceptions and construct
        #+ the already walked path
        if isinstance(gCurrentObject, collections.abc.Sequence):
            clsError = UT_IndexError
            strNewName = '{}[{}]'.format(strName, gItem)
        elif isinstance(gCurrentObject, collections.abc.Mapping):
            clsError = UT_KeyError
            strNewName = '{}[{}]'.format(strName, gItem)
        else:
            clsError = UT_AttributeError
            strNewName = '{}.{}'.format(strName, gItem)
        try:
            gResult = GetData(gCurrentObject, gItem)
        except UT_TypeError as err1: #object - path mismatch
            objError = UT_TypeError(1, int, SkipFrames = 1)
            strMessage = '{} - {}'.format(strNewName, err1.args[1])
            objError.args = (strMessage, )
            raise objError from None
        except (UT_AttributeError, UT_IndexError, UT_KeyError) as err2:
            #not found level
            if bStrict:
                raise clsError(strName, gItem, SkipFrames = 1) from None
            else:
                gResult = gDefault
                break
        gCurrentObject = gResult #reference to the next level
        strName = strNewName
    # no errors or access error in 'relaxed' mode
    return gResult

def SetElement(gObject: Any, gPath: TGenericPath, gValue: Any, *,
                bStrict: Optional[bool] = True) -> Any:
    """
    Attempts to assign a value to an element (key, attribute) of the nested
    structured object (including nested sequences) defined by a generic path.
    Can operate in two modes: 'strict' and 'relaxed'. In the strict mode an
    exception is raised if the path is incorrect, i.e., at least, one element
    of the path is not found. In the 'relaxed' mode the missing sub-path is
    created using nesting of dictionaries and lists, unless the new branch is
    to be attached to an immutable object.
    
    Signature:
        type A, str OR int OR seq(type B), type C/, *, bool/ -> None
    
    Args:
        gObject: type A; the object to be inspected
        gPath: str OR int OR seq(type B); the generic path to the end node
            of a nested struture object
        gValue: type C; the value to be assigned to the end node
        bStrict: (keyword) bool; the flag if the strict access mode is to be
            used, defaults to True
    
    Raises:
        UT_TypeError: the passed generic path is not an integer, a string or
            a (nested) sequence of only strings and integers, OR type mismatch
            between object level and path element - sequence object level
            and non-integer path element, non-sequence object level and
            non-string path element, OR an immutable object requires
            modification in order to complete the task
        UT_ValueError: the passed generic path is an empty sequence
        UT_IndexError: an object along the path is a sequence, and the
            respective access index is outside the range - 'strict' mode only
        UT_KeyError: an object along the path is a mapping type, and the
            respective access key is not found - 'strict' mode only
        UT_AttributeError: an object along the path is a genric class or
            instance, and the respective attribute is not found - 'strict' mode
            only
    
    Version 1.0.0.0
    """
    #convert the path into the canonical form - and check that it is not empty
    try:
        lstPath = FlattenPath(gItem)
    except UT_TypeError as err:
        objError = UT_TypeError(1, int, SkipFrames = 1)
        objError.args = (err.args[0], )
        raise objError from None
    iLen = len(lstPath)
    if not iLen:
        raise UT_ValueError(gPath, 'not empty path', SkipFrames = 1)
    #walk the object structure
    gCurrentObject = gObject
    strName = GetObjectClass(gTemp)
    for iIndex, gItem in enumerate(lstPath):
        #check the current level type to prepare the exceptions and construct
        #+ the already walked path
        if isinstance(gCurrentObject, collections.abc.Sequence):
            clsError = UT_IndexError
            strNewName = '{}[{}]'.format(strName, gItem)
        elif isinstance(gCurrentObject, collections.abc.Mapping):
            clsError = UT_KeyError
            strNewName = '{}[{}]'.format(strName, gItem)
        else:
            clsError = UT_AttributeError
            strNewName = '{}.{}'.format(strName, gItem)
        if iIndex < (iLen - 1): #not last element in the path
            try:
                gResult = GetData(gCurrentObject, gItem)
            except UT_TypeError as err1: #object - path mismatch
                objError = UT_TypeError(1, int, SkipFrames = 1)
                strMessage = '{} - {}'.format(strNewName, err1.args[1])
                objError.args = (strMessage, )
                raise objError from None
            except (UT_AttributeError, UT_IndexError, UT_KeyError):
                #not found level
                if bStrict:
                    raise clsError(strName, gItem, SkipFrames = 1) from None
                else:
                    gNextElement = lstPath[iIndex + 1]
                    if isinstance(gNextElement, int):
                        gNewItem = list()
                    else:
                        gNewItem = dict()
                    try:
                        SetData(gCurrentObject, gItem, gNewItem)
                    except UT_TypeError as err2: #immutable at this level
                        objError = UT_TypeError(1, int, SkipFrames = 1)
                        strMessage = '{} - {}'.format(strNewName, err2.args[1])
                        objError.args = (strMessage, )
                        raise objError from None
                    gResult = GetData(gCurrentObject, gItem)
            gCurrentObject = gResult #reference to the next level
            strName = strNewName
        else: #last element in the path
            try:
                if bStrict:
                    SetDataStrict(gCurrentObject, gItem, gValue)
                else:
                    SetData(gCurrentObject, gItem, gValue)
            except UT_TypeError as err1: #object - path mismatch or immutable
                objError = UT_TypeError(1, int, SkipFrames = 1)
                strMessage = '{} - {}'.format(strNewName, err1.args[1])
                objError.args = (strMessage, )
                raise objError from None
