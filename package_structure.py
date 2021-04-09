#!/usr/bin/python3
"""
Functions:
    IsPyFile(strFile):
        str -> bool
    IsPyPackage(strFolder):
        str -> bool
    SelectPySourceFiles(strFolder):
        str -> list(str)
    GetQualifiedName(strPath):
        str -> str OR None
    ResolveRelativeImport(strFile, strImportName):
        str, str -> str
"""

#imports

#+ standard library modules

import os
import sys

#import collections.abc as c_abc

#import copy

from typing import List, Union

#+ local libraries

LIB_ROOT = os.path.dirname(os.path.realpath(__file__))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#functions

def IsPyFile(strFile: str) -> bool:
    """
    Checks if a file exists, it is not a link, and it has '.py' extention, i.e.
    it is a Python source file.
    
    Signature:
        str -> bool
    
    Args:
        strFile: str; a path to a file (absolute or relative to the current
            working directory)
    
    Returns:
        bool: the result of the check
    
    Raises:
        UT_TypeError: passed argument is not a string
    
    Version 1.0.0.0
    """
    if not isinstance(strFile, str):
        raise UT_TypeError(strFile, str, SkipFrames = 1)
    Result = (os.path.isfile(strFile) and (not os.path.islink(strFile))
                                                and strFile.endswith('.py'))
    return Result

def IsPyPackage(strFolder: str) -> bool:
    """
    Checks if a folder exists, it is not a link, and it has '__init__.py' file
    within (actual, not a link), i.e. it is a Python package.
    
    Signature:
        str -> bool
    
    Args:
        strFolder: str; a path to a folder (absolute or relative to the current
            working directory)
    
    Returns:
        bool: the result of the check
    
    Raises:
        UT_TypeError: passed argument is not a string
    
    Version 1.0.0.0
    """
    if not isinstance(strFolder, str):
        raise UT_TypeError(strFolder, str, SkipFrames = 1)
    if os.path.isdir(strFolder):
        if not os.path.islink(strFolder):
            Result = IsPyFile(os.path.join(strFolder, '__init__.py'))
        else:
            Result = False
    else:
        Result = False
    return Result

def SelectPySourceFiles(strFolder: str) -> List[str]:
    """
    Finds all Python source files (not symlinks) present in a directory (not a
    symlink itself).
    
    Signature:
        str -> list(str)
    
    Args:
        strFolder: str; a path to a folder (absolute or relative to the current
            working directory)
    
    Returns:
        list(str): the list of the base filenames of the found source files
    
    Raises:
        UT_TypeError: passed argument is not a string
    
    Version 1.0.0.0
    """
    if not isinstance(strFolder, str):
        raise UT_TypeError(strFolder, str, SkipFrames = 1)
    if os.path.isdir(strFolder) and (not os.path.islink(strFolder)):
        Result = list(map(os.path.basename,
                        filter(IsPyFile, [os.path.join(strFolder, strFile)
                                        for strFile in os.listdir(strFolder)])))
    else:
        Result = []
    return Result

def GetQualifiedName(strPath: str) -> Union[str, None]:
    """
    Attempts to resolve the qualified (dot notation) of a module or (sub-)
    package from its path. The symlinks are ignored.
    
    Signature:
        str -> str OR None
    
    Args:
        strPath: str; a path to a folder or module (absolute or relative to the
            current working directory)
    
    Returns:
        str: the fully qualified name of a module / (sub-) package, if it was
            resolved
        None: if it was not resolved
    
    Raises:
        UT_TypeError: passed argument is not a string
    
    Version 1.0.0.0
    """
    if not isinstance(strPath, str):
        raise UT_TypeError(strPath, str, SkipFrames = 1)
    strPath = os.path.abspath(strPath)
    PathLen = len(strPath)
    if PathLen and IsPyFile(strPath):
        Result = os.path.basename(strPath)[:-3]
    elif PathLen and IsPyPackage(strPath):
        Result = os.path.basename(strPath)
    else:
        Result = None
    if not (Result is None):
        ParentPath = os.path.dirname(strPath)
        if len(ParentPath):
            Temp = GetQualifiedName(ParentPath)
            if not (Temp is None):
                Result = '{}.{}'.format(Temp, Result)
    return Result

def ResolveRelativeImport(strFile: str, strImportName: str) -> str:
    """
    Attempts to resolve the relative import into an absolute relatively to
    the 'root' package of the referenced by path module. The module must be
    whithin a package, and the relative path must end-up within the 'root' of
    the package structure, to which the referenced module belongs. The actual
    existence of a module referenced by the produced absolute path is not
    checked. The passed absolute imports are not modified.
    
    Signature:
        str, str -> str
    
    Args:
        strFile: str; a path to an actual Python source file, ignored in the
            case of an absolute import as long as it is string
        strImportName: str; an absolute or relative import name
    
    Returns:
        str: the absolute import path
    
    Raises:
        UT_TypeError: any of the arguments is not a string
        UT_ValueError: only in the case a relative import - first argument is
            not a path to an actual Python source file, OR the relative path
            leads to the outside of the 'root' package of the module, OR the
            module itself is not a part of a package
    
    Version 1.0.0.0
    """
    if not isinstance(strFile, str):
        raise UT_TypeError(strFile, str, SkipFrames = 1)
    elif not isinstance(strImportName, str):
        raise UT_TypeError(strImportName, str, SkipFrames = 1)
    if not strImportName.startswith('.'):
        Result = str(strImportName)
    else:
        strFile = os.path.abspath(strFile)
        if (IsPyFile(strFile)):
            strSuffix = strImportName.lstrip('.')
            iLevelsUp = len(strImportName) - len(strSuffix)
            strModuleName = GetQualifiedName(strFile)
            lstComponents = strModuleName.split('.')
            if len(lstComponents) > iLevelsUp:
                strPrefix = '.'.join(lstComponents[:-iLevelsUp])
                Result = '{}.{}'.format(strPrefix, strSuffix)
            else:
                raise UT_ValueError(strImportName,
                                'within the root of {}'.format(strModuleName))
        else:
            raise UT_ValueError(strFile, 'existing Python source file')
    return Result