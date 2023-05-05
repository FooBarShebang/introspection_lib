#!/usr/bin/python3
"""
Module introspection_lib.package_structure

Static anaysis of the structure and dependencies of a Python import package.
Designed mostly as a helper tools set for distribution packaging.

Functions:
    IsPyFile(FileName):
        str -> bool
    IsPyPackage(FolderName):
        str -> bool
    SelectPySourceFiles(FolderName):
        str -> list(str)
    GetQualifiedName(Path):
        str -> str OR None
    ResolveRelativeImport(FileName, ImportName):
        str, str -> str

Classes:
    PackageStructure: static structure analyzer
"""

__version__ = "1.0.1.0"
__date__ = "21-04-2023"
__status__ = "Production"

#imports

#+ standard library modules

import os
import sys
import fnmatch
import collections.abc as c_abc
import importlib
import importlib.util #does not work in Windows 11 otherwise

from typing import List, Union, Dict, Sequence

#+ local libraries

from .base_exceptions import UT_TypeError, UT_ValueError

#globals

METADATA_KEYS = [ '__version_info__', '__version_suffix__', '__version__',
    '__author__', '__date__', '__status__', '__maintainer__', '__license__',
    '__copyright__', '__project__']

#functions

def IsPyFile(FileName: str) -> bool:
    """
    Checks if a file exists, it is not a link, and it has '.py' extention, i.e.
    it is a Python source file.
    
    Signature:
        str -> bool
    
    Args:
        FileName: str; a path to a file (absolute or relative to the current
            working directory)
    
    Returns:
        bool: the result of the check
    
    Raises:
        UT_TypeError: passed argument is not a string
    
    Version 1.0.0.0
    """
    if not isinstance(FileName, str):
        raise UT_TypeError(FileName, str, SkipFrames = 1)
    Result = (os.path.isfile(FileName) and (not os.path.islink(FileName))
                                                and FileName.endswith('.py'))
    return Result

def IsPyPackage(FolderName: str) -> bool:
    """
    Checks if a folder exists, it is not a link, and it has '__init__.py' file
    within (actual, not a link), i.e. it is a Python package.
    
    Signature:
        str -> bool
    
    Args:
        FolderName: str; a path to a folder (absolute or relative to the current
            working directory)
    
    Returns:
        bool: the result of the check
    
    Raises:
        UT_TypeError: passed argument is not a string
    
    Version 1.0.0.0
    """
    if not isinstance(FolderName, str):
        raise UT_TypeError(FolderName, str, SkipFrames = 1)
    if os.path.isdir(FolderName):
        if not os.path.islink(FolderName):
            Result = IsPyFile(os.path.join(FolderName, '__init__.py'))
        else:
            Result = False
    else:
        Result = False
    return Result

def SelectPySourceFiles(FolderName: str) -> List[str]:
    """
    Finds all Python source files (not symlinks) present in a directory (not a
    symlink itself).
    
    Signature:
        str -> list(str)
    
    Args:
        FolderName: str; a path to a folder (absolute or relative to the current
            working directory)
    
    Returns:
        list(str): the list of the base filenames of the found source files
    
    Raises:
        UT_TypeError: passed argument is not a string
    
    Version 1.0.0.0
    """
    if not isinstance(FolderName, str):
        raise UT_TypeError(FolderName, str, SkipFrames = 1)
    if os.path.isdir(FolderName) and (not os.path.islink(FolderName)):
        Result = list(map(os.path.basename,
                        filter(IsPyFile, [os.path.join(FolderName, FileName)
                                    for FileName in os.listdir(FolderName)])))
    else:
        Result = []
    return Result

def GetQualifiedName(Path: str) -> Union[str, None]:
    """
    Attempts to resolve the qualified (dot notation) of a module or (sub-)
    package from its path. The symlinks are ignored.
    
    Signature:
        str -> str OR None
    
    Args:
        Path: str; a path to a folder or module (absolute or relative to the
            current working directory)
    
    Returns:
        str: the fully qualified name of a module / (sub-) package, if it was
            resolved
        None: if it was not resolved
    
    Raises:
        UT_TypeError: passed argument is not a string
    
    Version 1.0.0.0
    """
    if not isinstance(Path, str):
        raise UT_TypeError(Path, str, SkipFrames = 1)
    Path = os.path.abspath(Path)
    PathLength = len(Path)
    Result = None
    if PathLength:
        if IsPyFile(Path):
            Result = os.path.basename(Path)[:-3]
        elif IsPyPackage(Path):
            Result = os.path.basename(Path)
    if not (Result is None):
        ParentPath = os.path.dirname(Path)
        if ParentPath:
            Temp = GetQualifiedName(ParentPath)
            if not (Temp is None):
                Result = '{}.{}'.format(Temp, Result)
    return Result

def ResolveRelativeImport(FileName: str, ImportName: str) -> str:
    """
    Attempts to resolve the relative import into an 'absolute' relatively to
    the 'root' package of the referenced by path module. The module must be
    whithin a package, and the relative path must end-up within the 'root' of
    the package structure, to which the referenced module belongs. The actual
    existence of a module referenced by the produced absolute path is not
    checked. The passed absolute imports are not modified.
    
    Signature:
        str, str -> str
    
    Args:
        FileName: str; a path to an actual Python source file, ignored in the
            case of an absolute import as long as it is string
        ImportName: str; an absolute or relative import name
    
    Returns:
        str: the absolute import path
    
    Raises:
        UT_TypeError: any of the arguments is not a string
        UT_ValueError: only in the case a relative import - first argument is
            not a path to an actual Python source file, OR the relative path
            leads to the outside of the 'root' package of the module, OR the
            module itself is not a part of a package
    
    Version 1.0.1.0
    """
    if not isinstance(FileName, str):
        raise UT_TypeError(FileName, str, SkipFrames = 1)
    elif not isinstance(ImportName, str):
        raise UT_TypeError(ImportName, str, SkipFrames = 1)
    if not ImportName.startswith('.'):
        Result = str(ImportName)
    else:
        FileName = os.path.abspath(FileName)
        if (IsPyFile(FileName)):
            Suffix = ImportName.lstrip('.')
            LevelsUp = len(ImportName) - len(Suffix)
            ModuleName = GetQualifiedName(FileName)
            Components = ModuleName.split('.')
            if len(Components) > LevelsUp:
                Prefix = '.'.join(Components[:-LevelsUp])
                Result = f'{Prefix}.{Suffix}'
            else:
                raise UT_ValueError(ImportName,
                                            f'within the root of {ModuleName}')
        else:
            raise UT_ValueError(FileName, 'existing Python source file')
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
        

    Version 1.0.0.1
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
        
        Version 1.0.0.1
        """
        if not isinstance(Path, str):
            raise UT_TypeError(Path, str, SkipFrames = 1)
        if len(Path):
            self._Path = os.path.abspath(Path)
            if not IsPyPackage(self.Path):
                raise UT_ValueError(Path, 'path to a Python package',
                                                                SkipFrames= 1)
        else:
            raise UT_ValueError('Empty string', 'path to a Python package',
                                                                SkipFrames= 1)
        self._Package = GetQualifiedName(self.Path)
        self._Metadata = None
        self._resetCache()
        self._FilesFilters = ['setup.py']
        self._FoldersFilters = ['build', 'build/*', '*/build',
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
        
        Version 1.0.0.1
        """
        return '{}(Package={}, Path={})'.format(self.__class__.__name__,
                                                        self.Package, self.Path)
    
    #private methods

    def _resetCache(self) -> None:
        """
        Helper 'private' method to invalidate the cached data when the filtering
        patterns set is changed.

        Signature:
            None -> None
        
        Version 1.0.0.1
        """
        self._Modules = None
        self._Dependences = None
        self._Imports = None
        self._Metadata = None

    def _isAcceptableFile(self, FileName: str) -> bool:
        """
        Helper 'private' method to check if the file (passed path string) should
        be included into the analysis, or not.

        Signature:
            str -> bool

        Returns:
            bool: True if the file is a Python source code and is not filtered
                out, False - otherwise
        
        Version 1.0.0.1
        """
        if IsPyFile(FileName):
            strName = os.path.basename(FileName)
            if any(map(
                    lambda x: fnmatch.fnmatch(strName, x), self.FilesFilters)):
                Result = False
            else:
                Result = True
        else:
            Result = True
        return Result
    
    def _isAcceptableFolder(self, FolderName: str) -> bool:
        """
        Helper 'private' method to check if the sub-folder (passed path string)
        should be included into the analysis, or not.

        Signature:
            str -> bool

        Returns:
            bool: True if the file is a Python source code and is not filtered
                out, False - otherwise
        
        Version 1.0.0.1
        """
        if os.sep != '/':
            _Folder = FolderName.replace(os.sep, '/')
        else:
            _Folder = FolderName
        if any(map(lambda x: fnmatch.fnmatch(_Folder, x), self.FoldersFilters)):
            Result = False
        else:
            Result = True
        return Result

    #public API

    #+ properties

    @property
    def Path(self) -> str:
        """
        Read-only property. The absolute path to the folder linked to this
        analyzer.

        Signature:
            None -> str
        
        Version 1.0.0.1
        """
        return str(self._Path)
    
    @property
    def Package(self) -> str:
        """
        Read-only property. The fully qualified name of the package linked to
        this analyzer.

        Signature:
            None -> str
        
        Version 1.0.0.1
        """
        return str(self._Package)
    
    @property
    def FilesFilters(self) -> List[str]:
        """
        Read-only property - the list of the string Unix shell matching patterns
        for filtering of the base filenames.

        Signature:
            None -> list(str)
        
        Version 1.0.0.1
        """
        return list(self._FilesFilters)
    
    @property
    def FoldersFilters(self) -> List[str]:
        """
        Read-only property - the list of the string Unix shell matching patterns
        for filtering of the remaining relative sub-folders names.

        Signature:
            None -> list(str)
        
        Version 1.0.0.1
        """
        return list(self._FoldersFilters)
    
    @property
    def Metadata(self) -> Dict[str, Dict[str, Union[str, int]]]:
        """
        Read-only property. The found metadata of the package.

        Signature:
            None -> dict(str -> dict(str -> str OR int))
        
        Version 1.0.0.1
        """
        if self._Metadata is None:
            self._Metadata = dict()
            Path = os.path.join(self.Path, '__init__.py')
            with open(Path, 'rt') as fFile:
                for Index, Line in enumerate(fFile.readlines()):
                    Cond1 = Line.startswith('__')
                    Cond2 = '=' in Line
                    if Cond1 and Cond2:
                        Temp = Line.rstrip().split('=')
                        Name = Temp[0].strip()
                        if len(Temp) >= 2:
                            Value = '='.join(Temp[1:]).strip()
                            if Name in METADATA_KEYS:
                                self._Metadata[Name] = {
                                    'line' : Index,
                                    'value' : Value}
        return dict(self._Metadata)
    
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
        
        Version 1.0.0.1
        """
        if self._Modules is None:
            Result = []
            PrefixLen = len(f'{self.Path}{os.sep}')
            for Root, _, Files in os.walk(self.Path):
                if Root != self.Path:
                    RelRoot = Root[PrefixLen:]
                    Check = self._isAcceptableFolder(RelRoot)
                else:
                    RelRoot = None
                    Check = True
                if Check:
                    for BaseName in Files:
                        FileName = os.path.join(Root, BaseName)
                        if self._isAcceptableFile(FileName):
                            if RelRoot is None:
                                Result.append(BaseName)
                            else:
                                Path = os.path.join(RelRoot, BaseName)
                                Path = Path.replace(os.sep, '/')
                                Result.append(Path)
            self._Modules = Result
        return list(self._Modules)

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
        
        Version 1.0.1.0
        """
        if self._Dependences is None:
            self._Dependences = []
            self._Imports = dict()
            Dependences = []
            RootPackages = self.Package.split('.')
            for RelPath in self.getModules():
                AbsPath = os.path.join(self.Path, RelPath.replace('/', os.sep))
                Packages = list(RootPackages)
                DirName = os.path.dirname(AbsPath)[len(self.Path)+1:]
                if len(DirName):
                    Packages.extend(DirName.split(os.sep))
                PackagesDepth = len(Packages)
                Temp = dict()
                with open(AbsPath, 'rt') as fFile:
                    for RawLine in fFile.readlines():
                        Line = RawLine.strip()
                        Cond1 = Line.startswith('import')
                        Cond2 = Line.startswith('from') and ('import' in Line)
                        if Cond1:
                            Imports = Line[6:].split(',')
                            for Entry in Imports:
                                Names = Entry.strip().split('as')
                                Name = Names[0].strip()
                                Top = Name.split('.')[0]
                                if (not (Top in Dependences) and
                                                            Top != Packages[0]):
                                    Dependences.append(Top)
                                if len(Names) == 2:
                                    Alias = Names[1].strip()
                                else:
                                    Alias = Name
                                Temp[Alias] = Name
                        elif Cond2:
                            TempLine = Line[4:].split('import')
                            Prefix = TempLine[0].strip()
                            Stripped = Prefix.lstrip('.')
                            Count = len(Prefix) - len(Stripped)
                            if Count > PackagesDepth:
                                break
                            else:
                                if Count > 1:
                                    Prefix = '.'.join(Packages[:-Count + 1])
                                if Count:
                                    Prefix = f'{Prefix}.{Stripped}'
                            Top = Prefix.split('.')[0]
                            if not (Top in Dependences) and Top != Packages[0]:
                                    Dependences.append(Top)
                            Imports = TempLine[1].strip().split(',')
                            for Entry in Imports:
                                Names = Entry.strip().split('as')
                                Name = Names[0].strip()
                                FullName = f'{Prefix}.{Name}'
                                if len(Names) == 2:
                                    Alias = Names[1].strip()
                                else:
                                    Alias = Name
                                Temp[Alias] = FullName
                if Temp:
                    self._Imports[RelPath] = Temp
            for Top in Dependences:
                #the most direct manner to get all system import names
                if Top in sys.builtin_module_names or (
                                        hasattr(sys, 'stdlib_module_names') and
                                            (Top in sys.stdlib_module_names)):
                    continue
                #fall-back option for Python < v3.10
                Specs = importlib.util.find_spec(Top)
                if not (Specs is None):
                    Location = Specs.origin
                    if not (Location is None):
                        Cond1 = (Location.startswith(sys.base_prefix) or
                                            Location.startswith(sys.prefix))
                        Cond2 = not (('site-packages' in Location) or
                                            ('dist-packages' in Location))
                        Cond3 = Location == 'built-in'
                        IsSystem = (Cond1 and Cond2) or Cond3
                        if not IsSystem:
                            self._Dependences.append(Top)
                else:
                    self._Dependences.append(Top)
        return list(self._Dependences)

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
        if self._Imports is None:
            self.getDependencies()
        return dict(self._Imports)
    
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
        Root = self.Package.split('.')[-1]
        Names = [Root]
        for RelPath in self.getModules():
            DirPath = os.path.dirname(RelPath.replace('/', os.sep))
            if len(DirPath):
                Suffix = DirPath.replace(os.sep, '.')
                Package = f'{Root}.{Suffix}'
                if not (Package in Names):
                    Names.append(Package)
        return Names
    
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
        
        Version 1.0.0.1
        """
        if not isinstance(Pattern, str):
            raise UT_TypeError(Pattern, str, SkipFrames = 1)
        if Pattern in self.FilesFilters:
            Result = False
        else:
            Result = True
            self._FilesFilters.append(Pattern)
            self._resetCache()
        return Result
    
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
        
        Version 1.0.0.1
        """
        if not isinstance(Pattern, str):
            raise UT_TypeError(Pattern, str, SkipFrames = 1)
        if Pattern in self.FilesFilters:
            Result = True
            self._FilesFilters.remove(Pattern)
            self._resetCache()
        else:
            Result = False
        return Result
    
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
        
        Version 1.0.0.1
        """
        if not isinstance(Patterns, c_abc.Sequence):
            raise UT_TypeError(Patterns, c_abc.Sequence, SkipFrames = 1)
        for Index, Pattern in enumerate(Patterns):
            if not isinstance(Pattern, str):
                Error = UT_TypeError(Pattern, str, SkipFrames = 1)
                Error.appendMessage(f'at position {Index}')
                raise Error
        self._FilesFilters = list(Patterns)
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
        
        Version 1.0.0.1
        """
        if not isinstance(Pattern, str):
            raise UT_TypeError(Pattern, str, SkipFrames = 1)
        if Pattern in self.FilesFilters:
            Result = False
        else:
            Result = True
            self._FoldersFilters.append(Pattern)
            self._resetCache()
        return Result
    
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
        
        Version 1.0.0.1
        """
        if not isinstance(Pattern, str):
            raise UT_TypeError(Pattern, str, SkipFrames = 1)
        if Pattern in self.FoldersFilters:
            Result = True
            self._FoldersFilters.remove(Pattern)
            self._resetCache()
        else:
            Result = False
        return Result
    
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
        for Index, Pattern in enumerate(Patterns):
            if not isinstance(Pattern, str):
                Error = UT_TypeError(Pattern, str, SkipFrames = 1)
                Error.appendMessage(f'at position {Index}')
                raise Error
        self._FoldersFilters = list(Patterns)
        self._resetCache()