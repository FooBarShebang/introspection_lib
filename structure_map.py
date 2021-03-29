#usr/bin/python3
"""
Module introspection_lib.structure_map

Implements functions to create a map of the internal structure of an object and
to map the data from one structured (nested) object into another structured
(nested) object.

Functions:
    GetReadMap(gObject):
        int OR float OR str OR bool OR None OR seq(type A) OR
            dict(str -> type A) -> int OR float OR str OR bool OR None OR
                list(type A) OR OrderedDict(str -> type A)
    GetWriteMap(gObject):
        int OR float OR str OR bool OR None OR seq(type A) OR
            dict(str -> type A) -> int OR float OR str OR bool OR None OR
                list(type A) OR OrderedDict(str -> type A)
"""

__version__ = "0.1.0.0"
__date__ = "26-03-2021"
__status__ = "Development"

#imports

#+ standard libraries

import sys
import os
import collections

from typing import Any, Union, Sequence, Mapping, List, OrderedDict

#+ custom modules

MODULE_PATH = os.path.realpath(__file__)
LIB_FOLDER = os.path.dirname(MODULE_PATH)
ROOT_FOLDER = os.path.dirname(LIB_FOLDER)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from introspection_lib.base_exceptions import UT_TypeError

#types

TScalar = Union[int, float, str, bool, None]

TInput = Union[TScalar, Sequence[Any], Mapping[str, Any], object]

TOutput = Union[TScalar, List[Any], OrderedDict[str, Any]]

#main functions - visible, to be imported.

def GetReadMap(gObject: TInput) -> TOutput:
    """
    Creates a map of the internal structure of a (nested) structured data
    storage object, which (map) is JSON-format serialization ready. All
    end-nodes, which can be accessed for reading are included.

    Signature:
        int OR float OR str OR bool OR None OR seq(type A) OR
            dict(str -> type A) -> int OR float OR str OR bool OR None OR
                list(type A) OR OrderedDict(str -> type A)
    
    Args:
        gObject: int OR float OR str OR bool OR None OR seq(type A) OR
            dict(str -> type A); any non-callable Python type (except for the
            classes and their instanes, which can callable as well, but are
            acceptable). Expected types are scalar, sequence, mapping types or
            generic classes instances to be treated as C-struct like constructs.
    
    Returns:
        type int OR float OR str OR bool OR None OR list(type A) OR
            OrderedDict(str -> type A): a scalar, a (nested) list or dictionary
    
    Raises:
        UT_TypeError: unacceptable type of the argument, e.g. a function,
            an itterator, a generator, a co-routine, etc., OR a dictionary type
            (nested) containing non-string keys.
    
    Version 1.0.0.0
    """
    pass

def GetWriteMap(gObject: TInput) -> TOutput:
    """
    Creates a map of the internal structure of a (nested) structured data
    storage object, which (map) is JSON-format serialization ready. Only the
    end-nodes, which can be accessed for writing are included. End-nodes, which
    cannot be modified, but are required for the preservation of the structure
    of an object are represented by the special value '!@#immutable'. Immutable
    sequences and dictionaries without nested mutable elements are represented
    by an empty list or empty OrderedDict respectively

    Signature:
        int OR float OR str OR bool OR None OR seq(type A) OR
            dict(str -> type A) -> int OR float OR str OR bool OR None OR
                list(type A) OR OrderedDict(str -> type A)
    
    Args:
        gObject: int OR float OR str OR bool OR None OR seq(type A) OR
            dict(str -> type A); any non-callable Python type (except for the
            classes and their instanes, which can callable as well, but are
            acceptable). Expected types are scalar, sequence, mapping types or
            generic classes instances to be treated as C-struct like constructs.
    
    Returns:
        type int OR float OR str OR bool OR None OR list(type A) OR
            OrderedDict(str -> type A): a scalar, a (nested) list or dictionary
    
    Raises:
        UT_TypeError: unacceptable type of the argument, e.g. a function,
            an itterator, a generator, a co-routine, etc., OR a dictionary type
            (nested) containing non-string keys.
    
    Version 1.0.0.0
    """
    pass
