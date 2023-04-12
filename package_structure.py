#!/usr/bin/python3
"""
Module introspection_lib.package_structure

Static anaysis of the structure and dependencies of a Python import package.
Designed mostly as a helper tools set for distribution packaging.

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

Classes:
    PackageStructure: static structure analyzer
"""

__version__ = "1.0.0.0"
__date__ = "14-04-2021"
__status__ = "Production"

#imports

#+ standard library modules

import os
import sys
import fnmatch
import importlib
import collections.abc as c_abc

from typing import List, Union, Dict, Sequence

#+ local libraries

LIB_ROOT = os.path.dirname(os.path.realpath(__file__))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#++ actual imports

from introspection_lib.base_exceptions import UT_TypeError, UT_ValueError

#globals

METADATA_KEYS = [ '__version_info__', '__version_suffix__', '__version__',
    '__author__', '__date__', '__status__', '__maintainer__', '__license__',
    '__copyright__', '__project__']

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

class PackageStructure:
    """
    Static analyzer of a Python package folder structure.

    Properties:
        Path: (read-only) str; path to the folder
        Package: (read-only) str; fully qualified package name
        FilesFilers: (read-only) list(str); Unix shell base filenames filtering
            patterns
        FoldersFilers: (read-only) list(str); Unix shell sub-folders names
            filtering patterns
        Metadata: (read-only) dict(str -> dict(str -> int OR str)); metadata
            found for the package
    
    Methods:
        getModules():
            None -> list(str)
        getDependencies():
            None -> list(str)
        getImportNames():
            None -> dict(str -> dict(str -> str))
        getPackagingNames():
            None -> list(str)
        addFilesFilter():
            str -> bool
        removeFilesFilter():
            str -> bool
        setFilesFilters():
            seq(str) -> None
        addFoldersFilter():
            str -> bool
        removeFoldersFilter():
            str -> bool
        setFoldersFilters():
            seq(str) -> None
        

    Version 1.0.0.0
    """
    
    #magic methods

    def __init__(self, Path: str) -> None:
        """
        Initializer. Checks and stores the folder path and the fully qualified
        package name. Sets the files and folders filtering option to the default
        values, i.e. to ignore everthing related to the setuptools packaging
        process.

        Signature:
            str -> None
        
        Args:
            Path: str; path to a Python package (as folder)
        
        Raises:
            * UT_TypeError: passed argument is not a string
            * UT_ValueError: passed argument is a string, but not a path to
                a Python package folder
        
        Version 1.0.0.0
        """
        if not isinstance(Path, str):
            raise UT_TypeError(Path, str, SkipFrames = 1)
        if len(Path):
            self._strPath = os.path.abspath(Path)
            if not IsPyPackage(self.Path):
                raise UT_ValueError(Path, 'path to a Python package',
                                                                SkipFrames= 1)
        else:
            raise UT_ValueError('Empty string', 'path to a Python package',
                                                                SkipFrames= 1)
        self._strPackage = GetQualifiedName(self.Path)
        self._dictMeta = None
        self._resetCache()
        self._strlstFilesFilters = ['setup.py']
        self._strlstFoldersFilters = ['build', 'build/*', '*/build',
                                        '*/build/*', 'dist', 'dist/*',
                                        '*/dist', '*/dist/*', '*egg-info*',
                                        '*dist-info*']
    
    def __str__(self) -> str:
        """
        Hook method for the str() function.

        Signature:
            None -> str
        
        Returns:
            str: human readable instance content representation, including name
                of the class, name of the package and folder path linked to it
        
        Version 1.0.0.0
        """
        return '{}(Package={}, Path={}'.format(self.__class__.__name__,
                                                        self.Package, self.Path)
    
    #private methods

    def _resetCache(self) -> None:
        """
        Helper 'private' method to invalidate the cached data when the filtering
        patterns set is changed.

        Signature:
            None -> None
        
        Version 1.0.0.0
        """
        self._strlstModules = None
        self._strlstDependences = None
        self._dictImports = None

    def _isAcceptableFile(self, strFile: str) -> bool:
        """
        Helper 'private' method to check if the file (passed path string) should
        be included into the analysis, or not.

        Signature:
            str -> bool

        Returns:
            bool: True if the file is a Python source code and is not filtered
                out, False - otherwise
        
        Version 1.0.0.0
        """
        if IsPyFile(strFile):
            strName = os.path.basename(strFile)
            if any(map(
                    lambda x: fnmatch.fnmatch(strName, x), self.FilesFilters)):
                bResult = False
            else:
                bResult = True
        else:
            bResult = True
        return bResult
    
    def _isAcceptableFolder(self, strFolder: str) -> bool:
        """
        Helper 'private' method to check if the sub-folder (passed path string)
        should be included into the analysis, or not.

        Signature:
            str -> bool

        Returns:
            bool: True if the file is a Python source code and is not filtered
                out, False - otherwise
        
        Version 1.0.0.0
        """
        if os.sep != '/':
            _Folder = strFolder.replace(os.sep, '/')
        else:
            _Folder = strFolder
        if any(map(lambda x: fnmatch.fnmatch(_Folder, x), self.FoldersFilters)):
            bResult = False
        else:
            bResult = True
        return bResult

    #public API

    #+ properties

    @property
    def Path(self) -> str:
        """
        Read-only property. The absolute path to the folder linked to this
        analyzer.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return str(self._strPath)
    
    @property
    def Package(self) -> str:
        """
        Read-only property. The fully qualified name of the package linked to
        this analyzer.

        Signature:
            None -> str
        
        Version 1.0.0.0
        """
        return str(self._strPackage)
    
    @property
    def FilesFilters(self) -> List[str]:
        """
        Read-only property - the list of the string Unix shell matching patterns
        for filtering of the base filenames.

        Signature:
            None -> list(str)
        
        Version 1.0.0.0
        """
        return list(self._strlstFilesFilters)
    
    @property
    def FoldersFilters(self) -> List[str]:
        """
        Read-only property - the list of the string Unix shell matching patterns
        for filtering of the remaining relative sub-folders names.

        Signature:
            None -> list(str)
        
        Version 1.0.0.0
        """
        return list(self._strlstFoldersFilters)
    
    @property
    def Metadata(self) -> Dict[str, Dict[str, Union[str, int]]]:
        """
        Read-only property. The found metadata of the package.

        Signature:
            None -> dict(str -> dict(str -> str OR int))
        
        Version 1.0.0.0
        """
        if self._dictMeta is None:
            self._dictMeta = dict()
            strPath = os.path.join(self.Path, '__init__.py')
            with open(strPath, 'rt') as fFile:
                for iIndex, strLine in enumerate(fFile.readlines()):
                    bCond1 = strLine.startswith('__')
                    bCond2 = '=' in strLine
                    if bCond1 and bCond2:
                        lstTemp = strLine.rstrip().split('=')
                        strName = lstTemp[0].strip()
                        if len(lstTemp) >= 2:
                            strValue = '='.join(lstTemp[1:]).strip()
                            if strName in METADATA_KEYS:
                                self._dictMeta[strName] = {
                                    'line' : iIndex,
                                    'value' : strValue}
        return dict(self._dictMeta)
    
    #+ public methods

    def getModules(self) -> List[str]:
        """
        Makes a list of the relative paths to all found Python source modules,
        recursively checking all sub-folders, even if they are not sub-packages.
        Folders and files filtering patterns are applied.

        Signature:
            None -> list(str)
        
        Returns:
            list(str): remaining parts of the paths to the modules, relative to
                the package's folder
        
        Version 1.0.0.0
        """
        if self._strlstModules is None:
            strlstResult = []
            iPrefixLen = len('{}{}'.format(self.Path, os.sep))
            for strRoot, _, strlstFiles in os.walk(self.Path):
                if strRoot != self.Path:
                    strRelRoot = strRoot[iPrefixLen:]
                    bCheck = self._isAcceptableFolder(strRelRoot)
                else:
                    strRelRoot = None
                    bCheck = True
                if bCheck:
                    for strBaseName in strlstFiles:
                        strFile = os.path.join(strRoot, strBaseName)
                        if self._isAcceptableFile(strFile):
                            if strRelRoot is None:
                                strlstResult.append(strBaseName)
                            else:
                                strPath = os.path.join(strRelRoot, strBaseName)
                                strPath = strPath.replace(os.sep, '/')
                                strlstResult.append(strPath)
            self._strlstModules = strlstResult
        return list(self._strlstModules)

    def getDependencies(self) -> List[str]:
        """
        Makes a list of the top level dependencies found in the Python source
        modules, recursively checking all sub-folders, even if they are not
        sub-packages. Folders and files filtering patterns are applied.

        Signature:
            None -> list(str)
        
        Returns:
            list(str): found unique 'top level' dependencies, excluding the
                Standard Library
        
        Version 1.0.0.0
        """
        if self._strlstDependences is None:
            self._strlstDependences = []
            self._dictImports = dict()
            strlstDependences = []
            lstRootPackages = self.Package.split('.')
            for strRelPath in self.getModules():
                strAbsPath = os.path.join(self.Path,
                                                strRelPath.replace('/', os.sep))
                lstPackages = list(lstRootPackages)
                strDirName = os.path.dirname(strAbsPath)[len(self.Path)+1:]
                if len(strDirName):
                    lstPackages.extend(strDirName.split(os.sep))
                iLenPackages = len(lstPackages)
                dictTemp = dict()
                with open(strAbsPath, 'rt') as fFile:
                    for strRawLine in fFile.readlines():
                        strLine = strRawLine.strip()
                        bCond1 = strLine.startswith('import')
                        bCond2 = ((strLine.startswith('from'))
                                                    and ('import' in strLine))
                        if bCond1:
                            lstImports = strLine[6:].split(',')
                            for strEntry in lstImports:
                                lstNames = strEntry.strip().split('as')
                                strName = lstNames[0].strip()
                                strTop = strName.split('.')[0]
                                if not (strTop in strlstDependences):
                                    if strTop != lstPackages[0]:
                                        strlstDependences.append(strTop)
                                if len(lstNames) == 2:
                                    strAlias = lstNames[1].strip()
                                else:
                                    strAlias = strName
                                dictTemp[strAlias] = strName
                        elif bCond2:
                            lstTemp = strLine[4:].split('import')
                            strPrefix = lstTemp[0].strip()
                            strStripped = strPrefix.lstrip('.')
                            iCount = len(strPrefix) - len(strStripped)
                            if iCount > iLenPackages:
                                break
                            elif iCount > 1:
                                strPrefix = '.'.join(lstPackages[:-iCount + 1])
                                strPrefix='{}.{}'.format(strPrefix, strStripped)
                            elif iCount:
                                strPrefix='{}.{}'.format(strPrefix, strStripped)
                            strTop = strPrefix.split('.')[0]
                            if not (strTop in strlstDependences):
                                if strTop != lstPackages[0]:
                                    strlstDependences.append(strTop)
                            lstImports = lstTemp[1].strip().split(',')
                            for strEntry in lstImports:
                                lstNames = strEntry.strip().split('as')
                                strName = lstNames[0].strip()
                                strFullName = '.'.join([strPrefix, strName])
                                if len(lstNames) == 2:
                                    strAlias = lstNames[1].strip()
                                else:
                                    strAlias = strName
                                dictTemp[strAlias] = strFullName
                if len(dictTemp):
                    self._dictImports[strRelPath] = dictTemp
            for strTop in strlstDependences:
                gSpecs = importlib.util.find_spec(strTop)
                if not (gSpecs is None):
                    strLocation = gSpecs.origin
                    if not (strLocation is None):
                        bCond1 = (strLocation.startswith(sys.base_prefix) or
                                            strLocation.startswith(sys.prefix))
                        bCond2 = not (('site-packages' in strLocation) or
                                            ('dist-packages' in strLocation))
                        if not(bCond1 and bCond2):
                            self._strlstDependences.append(strTop)
                else:
                    self._strlstDependences.append(strTop)
        return list(self._strlstDependences)

    def getImportNames(self) -> Dict[str, Dict[str, str]]:
        """
        Creates a look-up table mapping per module the local names of the
        imported components to their fully qualified names.

        Signature:
            None -> dict(str -> dict(str -> str))
        
        Returns:
            dict(str -> dict(str -> str)): per module mapping of the local
                (namespace) names (as aliases) to the fully qualified names of
                the imported components; the top level keys are the relative
                paths to the respective modules
        
        Version 1.0.0.0
        """
        if self._dictImports is None:
            self.getDependencies()
        return dict(self._dictImports)
    
    def getPackagingNames(self) -> List[str]:
        """
        Creates a list of the (sub-) packages names relative to this one, which
        is to be packaged as 'top level'.

        Signature:
            None -> list(str)
        
        Returns:
            list(str): dot-separated qualified names of the package and
                sub-packages, assuming this one being installed as 'top level'
        
        Version 1.0.0.0
        """
        strRoot = self.Package.split('.')[-1]
        lstNames = [strRoot]
        for strRelPath in self.getModules():
            strDirPath = os.path.dirname(strRelPath.replace('/', os.sep))
            if len(strDirPath):
                strSuffix = strDirPath.replace(os.sep, '.')
                strPackage = '{}.{}'.format(strRoot, strSuffix)
                if not (strPackage in lstNames):
                    lstNames.append(strPackage)
        return lstNames
    
    def addFilesFilter(self, Pattern: str) -> bool:
        """
        Method to add a new base filename matching pattern for filtering.

        Signature:
            str -> bool
        
        Args:
            Pattern: str; Unix shell wildcard-enabled match pattern
        
        Returns:
            bool: True if the pattern is added, False - if it is not added (was
                present already)
        
        Raises:
            UT_TypeError: passed argument is not a string
        
        Version 1.0.0.0
        """
        if not isinstance(Pattern, str):
            raise UT_TypeError(Pattern, str, SkipFrames = 1)
        if Pattern in self.FilesFilters:
            bResult = False
        else:
            bResult = True
            self._strlstFilesFilters.append(Pattern)
            self._resetCache()
        return bResult
    
    def removeFilesFilter(self, Pattern: str) -> bool:
        """
        Method to remove an existing base filename matching pattern for
        filtering.

        Signature:
            str -> bool
        
        Args:
            Pattern: str; Unix shell wildcard-enabled match pattern
        
        Returns:
            bool: True if the pattern is removed, False - if it is not removed
                (was not present)
        
        Raises:
            UT_TypeError: passed argument is not a string
        
        Version 1.0.0.0
        """
        if not isinstance(Pattern, str):
            raise UT_TypeError(Pattern, str, SkipFrames = 1)
        if Pattern in self.FilesFilters:
            bResult = True
            self._strlstFilesFilters.remove(Pattern)
            self._resetCache()
        else:
            bResult = False
        return bResult
    
    def setFilesFilters(self, Patterns: Sequence[str]) -> None:
        """
        Method to set the entire list of the base filename matching pattern for
        filtering.

        Signature:
            seq(str) -> None
        
        Args:
            Patterns: seq(str); Unix shell wildcard-enabled match patterns

        Raises:
            UT_TypeError: passed argument is not a sequence of strings
        
        Version 1.0.0.0
        """
        if not isinstance(Patterns, c_abc.Sequence):
            raise UT_TypeError(Patterns, c_abc.Sequence, SkipFrames = 1)
        for iIndex, Pattern in enumerate(Patterns):
            if not isinstance(Pattern, str):
                objError = UT_TypeError(Pattern, str, SkipFrames = 1)
                strMessage = '{} at position {}'.format(objError.args[0],
                                                                    iIndex)
                objError.args = (strMessage, )
                raise objError
        self._strlstFilesFilters = list(Patterns)
        self._resetCache()

    def addFoldersFilter(self, Pattern: str) -> bool:
        """
        Method to add a new sub-folder matching pattern for filtering.

        Signature:
            str -> bool
        
        Args:
            Pattern: str; Unix shell wildcard-enabled match pattern
        
        Returns:
            bool: True if the pattern is added, False - if it is not added (was
                present already)
        
        Raises:
            UT_TypeError: passed argument is not a string
        
        Version 1.0.0.0
        """
        if not isinstance(Pattern, str):
            raise UT_TypeError(Pattern, str, SkipFrames = 1)
        if Pattern in self.FilesFilters:
            bResult = False
        else:
            bResult = True
            self._strlstFoldersFilters.append(Pattern)
            self._resetCache()
        return bResult
    
    def removeFoldersFilter(self, Pattern: str) -> bool:
        """
        Method to remove an existing sub-folder matching pattern for filtering.

        Signature:
            str -> bool
        
        Args:
            Pattern: str; Unix shell wildcard-enabled match pattern
        
        Returns:
            bool: True if the pattern is removed, False - if it is not removed
                (was not present)
        
        Raises:
            UT_TypeError: passed argument is not a string
        
        Version 1.0.0.0
        """
        if not isinstance(Pattern, str):
            raise UT_TypeError(Pattern, str, SkipFrames = 1)
        if Pattern in self.FoldersFilters:
            bResult = True
            self._strlstFoldersFilters.remove(Pattern)
            self._resetCache()
        else:
            bResult = False
        return bResult
    
    def setFoldersFilters(self, Patterns: Sequence[str]) -> None:
        """
        Method to set the entire list of the sub-folder matching pattern for
        filtering.

        Signature:
            seq(str) -> None
        
        Args:
            Patterns: seq(str); Unix shell wildcard-enabled match patterns
        
        Raises:
            UT_TypeError: passed argument is not a sequence of strings
        
        Version 1.0.0.0
        """
        if not isinstance(Patterns, c_abc.Sequence):
            raise UT_TypeError(Patterns, c_abc.Sequence, SkipFrames = 1)
        for iIndex, Pattern in enumerate(Patterns):
            if not isinstance(Pattern, str):
                objError = UT_TypeError(Pattern, str, SkipFrames = 1)
                strMessage = '{} at position {}'.format(objError.args[0],
                                                                    iIndex)
                objError.args = (strMessage, )
                raise objError
        self._strlstFoldersFilters = list(Patterns)
        self._resetCache()