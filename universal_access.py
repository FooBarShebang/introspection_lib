#usr/bin/python3
"""
Module introspection_lib.universal_access

Implements functions to provide unified access to the elements of sequences,
keys of mapping type objects and attributes of classes / instances, with the
support for nested elements path.

Functions:
    GetData(Object, gPath):
        type A, str OR int -> type B
    GetDataDefault(Object, Path, Default):
        type A, str OR int, type B -> type C
    SetDataStrict(Object, Path, Value):
        type A, str OR int, type B -> None
    SetData(Object, Path, Value):
        type A, str OR int, type B -> None
    FlattenPath(Path):
        str OR int OR seq(type A) -> list(str OR int)
    GetElement(Object, Path, *, IsStrict = True, Default = None):
        type A, str OR int OR seq(type B)/, *, bool, type C/ -> type D
    SetElement(Object, Path, Value, *, IsStrict = True):
        type A, str OR int OR seq(type B), type C/, *, bool/ -> None
"""

__version__ = "1.0.1.1"
__date__ = "21-04-2021"
__status__ = "Production"

#imports

#+ standard libraries

import collections

from typing import Any, Union, Sequence, List, Optional

#+ custom modules

from .base_exceptions import UT_TypeError, UT_ValueError, UT_AttributeError
from .base_exceptions import UT_KeyError, UT_IndexError, GetObjectClass

#types

TPathElement = Union[int, str]
TCannonicalPath = List[TPathElement]
TGenericPath = Union[int, str, Sequence[Any]]

#functions

def GetData(Object: Any, Path: TPathElement) -> Any:
    """
    Universal 'read' access to an element of a list, key : value pair entry of
    a mapping type or an attribute of a generic class or instance. Raises
    exceptions compatible with (sub-classes of) the standard exceptions
    IndexError, KeyError or AttributeError, which should be normally raised
    upon 'read' access to a non-existing element.
    
    Signature:
        type A, str OR int -> type B
    
    Args:
        Object: type A; the object to be inspected
        Path: str OR int; the attribute name / key or index of the element to
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
    
    Version 1.1.0.0
    """
    if not isinstance(Path, (int, str)):
        Error = UT_TypeError(Path, [int, str], SkipFrames = 1)
        Error.appendMessage(f'in "{Path}" path')
        raise Error
    if isinstance(Object, collections.abc.Sequence):
        #dirty hack to allow string (attrubute) access to named tuples
        if isinstance(Path, str) and (not hasattr(Object, '_fields')):
            Error = UT_TypeError(Path, int, SkipFrames = 1)
            Error.appendMessage(f'in "{Path}" path for sequence {Object}')
            raise Error
        if isinstance(Path, int): #index access
            Length = len(Object)
            if (Path < (- Length)) or (Path >= Length):
                Name = f'passed sequence {Object}'
                raise UT_IndexError(Name, Path, SkipFrames = 1)
            Result = Object[Path]
        else: #attribute access - for named tuples only
            if not hasattr(Object, Path):
                Error = UT_AttributeError(Object, Path, SkipFrames = 1)
                Error.appendMessage('not found attribute')
                raise Error
            Result = getattr(Object, Path)
    else:
        if not isinstance(Path, str):
            Error = UT_TypeError(Path, str, SkipFrames = 1)
            Error.appendMessage(f'in "{Path}" path for {Object}')
            raise Error
        if isinstance(Object, collections.abc.Mapping):
            if not Path in Object:
                Name = f'passed mapping {Object}'
                raise UT_KeyError(Name, Path, SkipFrames = 1)
            Result = Object[Path]
        else:
            if not hasattr(Object, Path):
                Error = UT_AttributeError(Object, Path, SkipFrames = 1)
                Error.appendMessage('not found attribute')
                raise Error
            Result = getattr(Object, Path)
    return Result

def GetDataDefault(Object: Any, Path: TPathElement, Default: Any) -> Any:
    """
    Universal 'read' access to an element of a list, key : value pair entry of
    a mapping type or an attribute of a generic class or instance with a default
    value, which should be returned upon 'read' access to a non-existing element
    instead of raising of a respective exception.
    
    Signature:
        type A, str OR int, type B -> type C
    
    Args:
        Object: type A; the object to be inspected
        Path: str OR int; the attribute name / key or index of the element to
            be accessed
        Default: type B; the default value to return, if such element is not
            found
    
    Returns:
        type C: the value of the found by attribute name, key or index element,
            OR the passed default value if such element is not found
    
    Raises:
        UT_TypeError: type mismatch between object and path - sequence object
            and non-integer path, non-sequence object and non-string path, OR
            the path is neither an integer or a string
    
    Version 1.1.0.0
    """
    if not isinstance(Path, (int, str)):
        Error = UT_TypeError(Path, [int, str], SkipFrames = 1)
        Error.appendMessage(f'in "{Path}" path')
        raise Error
    if isinstance(Object, collections.abc.Sequence):
        #dirty hack to allow string (attrubute) access to named tuples
        if isinstance(Path, str) and (not hasattr(Object, '_fields')):
            Error = UT_TypeError(Path, int, SkipFrames = 1)
            Error.appendMessage(f'in "{Path}" path for sequence {Object}')
            raise Error
        if isinstance(Path, int): #index access
            Length = len(Object)
            if (Path < (- Length)) or (Path >= Length):
                Result = Default
            else:
                Result = Object[Path]
        else: #attribute access - for named tuples only
            Result = getattr(Object, Path, Default)
    else:
        if not isinstance(Path, str):
            Error = UT_TypeError(Path, str, SkipFrames = 1)
            Error.appendMessage(f'in "{Path}" path for {Object}')
            raise Error
        if isinstance(Object, collections.abc.Mapping):
            Result = Object.get(Path, Default)
        else:
            Result = getattr(Object, Path, Default)
    return Result

def SetDataStrict(Object: Any, Path: TPathElement, Value: Any) -> None:
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
        Object: type A; the object to be inspected
        Path: str OR int; the attribute name / key or index of the element to
            be accessed
        Value: type B; the value assign
    
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
    if not isinstance(Path, (int, str)):
        Error = UT_TypeError(Path, [int, str], SkipFrames = 1)
        Error.appendMessage(f'in "{Path}" path')
        raise Error
    if isinstance(Object, collections.abc.Sequence):
        if not isinstance(Object, collections.abc.MutableSequence):
            raise UT_TypeError(Object, collections.abc.MutableSequence,
                                                                SkipFrames = 1)
        if not isinstance(Path, int):
            Error = UT_TypeError(Path, int, SkipFrames = 1)
            Error.appendMessage(f'in "{Path}" path for sequence {Object}')
            raise Error
        Length = len(Object)
        if (Path < (- Length)) or (Path >= Length):
            raise UT_IndexError(f'passed sequence {Object}', Path, SkipFrames=1)
        Object[Path] = Value
    else:
        if not isinstance(Path, str):
            Error = UT_TypeError(Path, str, SkipFrames = 1)
            Error.appendMessage(f'in "{Path}" path for {Object}')
            raise Error
        if isinstance(Object, collections.abc.Mapping):
            if not isinstance(Object, collections.abc.MutableMapping):
                raise UT_TypeError(Object, collections.abc.MutableMapping,
                                                                SkipFrames = 1)
            if not Path in Object:
                raise UT_KeyError(f'passed mapping {Object}', Path,
                                                                SkipFrames = 1)
            Object[Path] = Value
        else:
            if not hasattr(Object, Path):
                Error = UT_AttributeError(Object, Path, SkipFrames = 1)
                Error.appendMessage(f'not found attribute')
                raise Error
            setattr(Object, Path, Value)

def SetData(Object: Any, Path: TPathElement, Value: Any) -> None:
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
    if not isinstance(Path, (int, str)):
        Error = UT_TypeError(Path, [int, str], SkipFrames = 1)
        Error.appendMessage(f'in "{Path}" path')
        raise Error
    if isinstance(Object, collections.abc.Sequence):
        if not isinstance(Object, collections.abc.MutableSequence):
            raise UT_TypeError(Object, collections.abc.MutableSequence,
                                                                SkipFrames = 1)
        if not isinstance(Path, int):
            Error = UT_TypeError(Path, int, SkipFrames = 1)
            Error.appendMessage(f'in "{Path}" path for sequence {Object}')
            raise Error
        Length = len(Object)
        if Path < (- Length):
            Object.insert(0, Value)
        elif Path >= Length:
            Object.append(Value)
        else:
            Object[Path] = Value
    else:
        if not isinstance(Path, str):
            Error = UT_TypeError(Path, str, SkipFrames = 1)
            Error.appendMessage(f'in "{Path}" for {Object}')
            raise Error
        if isinstance(Object, collections.abc.Mapping):
            if not isinstance(Object, collections.abc.MutableMapping):
                raise UT_TypeError(Object, collections.abc.MutableMapping,
                                                                SkipFrames = 1)
            Object[Path] = Value
        else:
            setattr(Object, Path, Value)

def FlattenPath(Path: TGenericPath) -> TCannonicalPath:
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
        Path: str OR int OR seq(type A); the generic nested path description
            to be flattened
    
    Returns:
        list(str OR int): the flattened nested path description
    
    Raises:
        UT_TypeError: the passed generic path is not an integer, a string or
            a (nested) sequence of only strings and integers
    
    Version 1.0.0.0
    """
    if isinstance(Path, str):
        Result = Path.split(".")
    elif isinstance(Path, int):
        Result = [Path]
    elif isinstance(Path, collections.abc.Sequence):
        Result = []
        for Item in Path:
            try:
                Temp = FlattenPath(Item)
            except UT_TypeError as err:
                Error = UT_TypeError(1, int, SkipFrames = 1)
                Message = err.getMessage()
                Error.setMessage(f'{Message} in {Path}')
                raise Error from None
            Result.extend(Temp)
    else:
        Error = UT_TypeError(Path, [int, str, collections.abc.Sequence],
                                                                SkipFrames = 1)
        Error.appendMessage(f'in {Path}')
        raise Error
    return Result

def GetElement(Object: Any, Path: TGenericPath, *,
                IsStrict: bool = True,
                Default: Any = None) -> Any:
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
        Object: type A; the object to be inspected
        Path: str OR int OR seq(type B); the generic path to the end node
            of a nested struture object
        IsStrict: (keyword) bool; the flag if the strict access mode is to be
            used, defaults to True
        Default: (keyword) type C; the default value to return, if any level
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
        Path = FlattenPath(Path)
    except UT_TypeError as err:
        Message = err.getMessage()
        Error = UT_TypeError(1, int, SkipFrames = 1)
        Error.setMessage(f'{Message} - invalid path definition')
        raise Error from None
    if not Path:
        raise UT_ValueError(Path, 'not empty path', SkipFrames = 1)
    #walk the object structure
    CurrentObject = Object
    Name = GetObjectClass(CurrentObject)
    for Item in Path:
        #check the current level type to prepare the exceptions and construct
        #+ the already walked path
        if isinstance(CurrentObject, collections.abc.Sequence):
            ErrorClass = UT_IndexError
            FullName = f'{Name}[{Item}]'
        elif isinstance(CurrentObject, collections.abc.Mapping):
            ErrorClass = UT_KeyError
            FullName = f'{Name}[{Item}]'
        else:
            ErrorClass = UT_AttributeError
            FullName = f'{Name}.{Item}'
        try:
            Result = GetData(CurrentObject, Item)
        except UT_TypeError as err1: #object - path mismatch
            Message = err1.getMessage()
            Error = UT_TypeError(1, int, SkipFrames = 1)
            Error.setMessage(f'{FullName} - {Message}')
            raise Error from None
        except (UT_AttributeError, UT_IndexError, UT_KeyError):
            #not found level
            if IsStrict:
                raise ErrorClass(FullName, Item, SkipFrames = 1) from None
            else:
                Result = Default
                break
        CurrentObject = Result #reference to the next level
        Name = FullName
    # no errors or access error in 'relaxed' mode
    return Result

def SetElement(Object: Any, Path: TGenericPath, Value: Any, *,
                IsStrict: bool = True) -> Any:
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
        Object: type A; the object to be inspected
        Path: str OR int OR seq(type B); the generic path to the end node
            of a nested struture object
        Value: type C; the value to be assigned to the end node
        IsStrict: (keyword) bool; the flag if the strict access mode is to be
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
        Path = FlattenPath(Path)
    except UT_TypeError as err:
        Error = UT_TypeError(1, int, SkipFrames = 1)
        Message = err.getMessage()
        Error.setMessage(f'{Message} - invalid path definition')
        raise Error from None
    Length = len(Path)
    if not Length:
        raise UT_ValueError(Path, 'not empty path', SkipFrames = 1)
    #walk the object structure
    CurrentObject = Object
    Name = GetObjectClass(CurrentObject)
    for Index, Item in enumerate(Path):
        #check the current level type to prepare the exceptions and construct
        #+ the already walked path
        if isinstance(CurrentObject, collections.abc.Sequence):
            ErrorClass = UT_IndexError
            FullName = f'{Name}[{Item}]'
        elif isinstance(CurrentObject, collections.abc.Mapping):
            ErrorClass = UT_KeyError
            FullName = f'{Name}[{Item}]'
        else:
            ErrorClass = UT_AttributeError
            FullName = f'{Name}.{Item}'
        if Index < (Length - 1): #not last element in the path
            try:
                Result = GetData(CurrentObject, Item)
            except UT_TypeError as err1: #object - path mismatch
                Error = UT_TypeError(1, int, SkipFrames = 1)
                Message = err1.getMessage()
                Error.setMessage(f'{FullName} - {Message}')
                raise Error from None
            except (UT_AttributeError, UT_IndexError, UT_KeyError):
                #not found level
                if IsStrict:
                    raise ErrorClass(Name, Item, SkipFrames = 1) from None
                else:
                    NextElement = Path[Index + 1]
                    if isinstance(NextElement, int):
                        NewItem = list()
                    else:
                        NewItem = dict()
                    try:
                        SetData(CurrentObject, Item, NewItem)
                    except UT_TypeError as err2: #immutable at this level
                        Error = UT_TypeError(1, int, SkipFrames = 1)
                        Message = err2.getMessage()
                        Error.setMessage(f'{FullName} - {Message}')
                        raise Error from None
                    Result = NewItem
            CurrentObject = Result #reference to the next level
            Name = FullName
        else: #last element in the path
            try:
                if IsStrict:
                    SetDataStrict(CurrentObject, Item, Value)
                else:
                    SetData(CurrentObject, Item, Value)
            except UT_TypeError as err3: #object - path mismatch or immutable
                Error = UT_TypeError(1, int, SkipFrames = 1)
                Message = err3.getMessage()
                Error.setMessage(f'{FullName} - {Message}')
                raise Error from None
