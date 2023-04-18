#usr/bin/python
"""
Module introspection_lib.dynamic_import

Implements functions to import modules or objects from modules dynamically, i.e.
using their string names at the runtime.

Functions:
    import_module(Path, Alias = None, *, Globals = None)
        str/, str, *, dict/ -> __builtins__.module
    import_from_module(Path, Name, Alias = None, *, Globals = None)
        str, str/, str, *, dict/ -> type A
"""

__version__ = "1.0.1.0"
__date__ = "17-04-2023"
__status__ = "Production"

#imports

#+ standard libraries

import sys
import os
import importlib
import collections
import types

from typing import Optional, Any

#+ other modules / libraries (DO)

LIB_ROOT = os.path.dirname(os.path.realpath(__file__))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual import

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#functions

def import_module(Path:str, Alias:Optional[str] = None, *,
                        Globals:Optional[dict] = None) -> types.ModuleType:
    """
    Dynamic import of a module, optionally, with aliasing of its name. In order
    to place the reference to the imported module into the global symbol table
    of the caller's module such table must be passed as the keyword argument
    'Globals' or a the third positional argument; otherwise the reference
    to the module is placed into the global symbol table of the module
    introspection_lib.dynamic_import itself.
    
    Example:
        import_module('library.package.module', Globals = globals())
            ~ is equivalent to ~
                import library.package.module
        MyModule =import_module('library.package.module', Globals = globals())
            ~ is equivalent to ~
                import library.package.module
                MyModule = library.package.module
        import_module('library.package.module', 'Alias', Globals = globals())
            ~ is equivalent to ~
                import library.package.module as Alias
        MyModule = import_module('library.package.module', 'Alias',
                                                            Globals = globals())
            ~ is equivalent to ~
                import library.package.module as Alias
                MyModule = Alias
    
    Signature:
        str/, str, *, dict/ -> __builtins__.module
    
    Args:
        Path: string; path to a module, e.g. 'library.package.module'
        Alias: (optional) string; alias to be assigned to the imported module
        Globals: (keyword) dict; dictionary representing the global symbol table
    
    Returns:
        __builtins__.module: a reference to the imported module
    
    Raises:
        UT_TypeError: passed path to the module is not a string; or passed alias
            is not a string or None;  or the passed global symbols table is not
            a dictionary or None
        UT_ValueError: required module is not found
    
    Version 1.1.0.0
    """
    #input data sanity checks
    if not isinstance(Path, str):
        raise UT_TypeError(Path, str, SkipFrames = 1)
    if (not (Alias is None)) and (not isinstance(Alias, str)):
        raise UT_TypeError(Alias, str, SkipFrames = 1)
    if (not (Globals is None)) and (not isinstance(Globals,
                                                    collections.abc.Mapping)):
        raise UT_TypeError(Globals, collections.abc.Mapping, SkipFrames = 1)
    #actual job
    if Globals is None:
        Globals = globals()
    try:
        Module = importlib.import_module(Path)
    except ImportError as err:
        Error = UT_ValueError(1, 'Import error - ', SkipFrames = 1)
        Error.appendMessage(''.join(map(str, err.args)))
        raise Error from None
    if Alias is None:
        Name = Path.split('.')[0]
        Globals[Name] = sys.modules[Name]
    else:
        Globals[Alias] = Module
    return Module

def import_from_module(Path:str, Name:str, Alias:Optional[str] = None, *,
                                        Globals:Optional[dict] = None) -> Any:
    """
    Dynamic import of an object from a module, optionally, with aliasing of its
    name. In order to place the reference to the imported object into the global
    symbol table of the caller's module such table must be passed as the keyword
    argument 'dictGlobals' or a the fourth positional argument; otherwise the
    reference to the object is placed into the global symbol table of the module
    introspection_lib.dynamic_import itself.
    
    Example:
        import_from_module('library.module', 'SomeClass', Globals = globals())
            ~ is equivalent to ~
                from library.module import SomeClass
        MyClass=import_from_module('library', 'S_Class', Globals = globals())
            ~ is equivalent to ~
                from library import S_Class
                MyClass = S_Class
        import_from_module('library', 'SomeClass', 'Alias', Globals = globals())
            ~ is equivalent to ~
                from library import SomeClass as Alias
        MyClass = import_from_module('library', 'SomeClass', 'Alias',
                                                            Globals=globals())
            ~ is equivalent to ~
                from library import SomeClass as Alias
                MyClass = Alias
    
    Signature:
        str, str/, str, *, dict/ -> type A
    
    Args:
        Path: string, path to a module, e.g. 'library.package.module'
        Name: name of an object defined in the module, e.g. 'SomeClass'
        Alias: (optional) string, alias to be assigned to the imported object
        Globals: (keyword) dictionary representing the global symbol table
    
    Returns:
        type A: a reference to the imported object
    
    Raises:
        UT_TypeError: passed path to the module is not a string; or passed name
            of the object is not a string; or the passed alias is not a string
            or None; or the passed global symbols table is not a dictionary or
            None
        UT_ValueError: required module is not found, OR required object is not
            found in the module
    
    Version 1.1.0.0
    """
    #input data sanity checks
    if not isinstance(Path, str):
        raise UT_TypeError(Path, str, SkipFrames = 1)
    if not isinstance(Name, str):
        raise UT_TypeError(Name, str, SkipFrames = 1)
    if (not (Alias is None)) and (not isinstance(Alias, str)):
        raise UT_TypeError(Alias, str, SkipFrames = 1)
    if (not (Globals is None)) and (not isinstance(Globals,
                                                    collections.abc.Mapping)):
        raise UT_TypeError(Globals, collections.abc.Mapping, SkipFrames = 1)
    #actual job
    if Globals is None:
        Globals = globals()
    try:
        Object = getattr(importlib.import_module(Path), Name)
    except (ImportError, AttributeError) as err:
        Error = UT_ValueError(1, 'Import error - ', SkipFrames = 1)
        Error.appendMessage(''.join(map(str, err.args)))
        raise Error from None
    if Alias is None:
        Globals[Name] = Object
    else:
        Globals[Alias] = Object
    return Object