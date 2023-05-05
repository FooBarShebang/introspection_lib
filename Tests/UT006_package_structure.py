#!/usr/bin/python
"""
Module introspection_lib.Tests.UT006_package_structure

Implements unit testing of the module package_structure. See test report TE007.

NOTE: Must be executed with administrative privelegies in Windows 11, because
of issues with os.symlink() in Windows.
"""

__version__ = "1.0.0.0"
__date__ = "07-04-2021"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import shutil
import collections.abc as c_abc

MODULE_PATH = os.path.realpath(__file__)

MODULE_ROOT = os.path.dirname(MODULE_PATH)

LIB_ROOT = os.path.dirname(MODULE_ROOT)

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

#+ tested module

import introspection_lib.package_structure as TestModule

#+ test cases

class Test_IsPyFile(unittest.TestCase):
    """
    Test cases for the function IsPyFile() from the module package_structure.
    
    Implements tests ID TEST-T-710. Covers requirements REQ-FUN-710 and
    REQ-AWM-700.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.IsPyFile)
        strPath = os.path.join(MODULE_ROOT, 'temp.py')
        strPathLink = os.path.join(MODULE_ROOT, 'link.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        os.symlink(strPath, strPathLink)
        cls.NewFile = strPath
        cls.Link = strPathLink
        cls.BadCases = [1, 1.0, int, float, str, [1], (2.0, 'a'), ['a'],
                        {'a': 1}, {'a', 'b', 'c'}]
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleaning-up. Done only once.
        """
        os.remove(cls.Link)
        os.remove(cls.NewFile)
    
    def test_Check_Ok(self):
        """
        Should return True in the case of the existing actual (not links) Python
        source files.
        
        Test ID TEST-T-710. Covers requirements REQ-FUN-710.
        """
        Result = self.TestFunction(MODULE_PATH) #this test file itself
        self.assertIsInstance(Result, bool)
        self.assertTrue(Result)
        Result = self.TestFunction(self.NewFile) #created temp file
        self.assertIsInstance(Result, bool)
        self.assertTrue(Result)
    
    def test_Check_Nok(self):
        """
        Should return False in the case of the existing link (not file), a
        folder or non-existing path.
        
        Test ID TEST-T-710. Covers requirements REQ-FUN-710.
        """
        Result = self.TestFunction(MODULE_ROOT) #an exising folder
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
        Result = self.TestFunction(self.Link) #created link
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
        Result = self.TestFunction(os.path.join(MODULE_ROOT,'temp'))
        #a non-exising folder
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
        Result = self.TestFunction(os.path.join(MODULE_ROOT,'whatever.py'))
        #a non-exising file
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
    
    def test_Raises(self):
        """
        Should raise a (sub-) class TypeError exception if not a string argument
        is received.
        
        Test ID TEST-T-710. Covers requirements REQ-AWM-700.
        """
        for gItem in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(gItem)

class Test_IsPyPackage(unittest.TestCase):
    """
    Test cases for the function IsPyPackage() from the module package_structure.
    
    Implements tests ID TEST-T-720. Covers requirements REQ-FUN-720 and
    REQ-AWM-700.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.IsPyPackage)
        strPath = os.path.join(MODULE_ROOT, 'temp')
        os.mkdir(strPath)
        cls.NewDir = strPath
        strPathLink = os.path.join(MODULE_ROOT, 'link')
        os.symlink(strPath, strPathLink, target_is_directory = True)
        cls.Link = strPathLink
        strPath = os.path.join(strPath, '__init__.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        cls.NewFile = strPath
        cls.BadCases = [1, 1.0, int, float, str, [1], (2.0, 'a'), ['a'],
                        {'a': 1}, {'a', 'b', 'c'}]
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleaning-up. Done only once.
        """
        os.remove(cls.Link)
        os.remove(cls.NewFile)
        os.rmdir(cls.NewDir)
    
    def test_Check_Ok(self):
        """
        Should return True in the case of the existing actual (not links) Python
        source files.
        
        Test ID TEST-T-720. Covers requirements REQ-FUN-720.
        """
        Result = self.TestFunction(LIB_ROOT) #this library itself
        self.assertIsInstance(Result, bool)
        self.assertTrue(Result)
        Result = self.TestFunction(self.NewDir) #created temp directory
        self.assertIsInstance(Result, bool)
        self.assertTrue(Result)
    
    def test_Check_Nok(self):
        """
        Should return False in the case of the existing link (not file), a
        folder or non-existing path.
        
        Test ID TEST-T-720. Covers requirements REQ-FUN-720.
        """
        Result = self.TestFunction(MODULE_ROOT)
        #an exising folder, but not a package
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
        Result = self.TestFunction(self.Link) #created link
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
        Result = self.TestFunction(self.NewFile) #existing file
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
        Result = self.TestFunction(os.path.join(MODULE_ROOT,'temp2'))
        #a non-exising folder
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
        Result = self.TestFunction(os.path.join(MODULE_ROOT,'whatever.py'))
        #a non-exising file
        self.assertIsInstance(Result, bool)
        self.assertFalse(Result)
    
    def test_Raises(self):
        """
        Should raise a (sub-) class TypeError exception if not a string argument
        is received.
        
        Test ID TEST-T-720. Covers requirements REQ-AWM-700.
        """
        for gItem in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(gItem)

class Test_SelectPySourceFiles(unittest.TestCase):
    """
    Test cases for the function SelectPySourceFiles() from the module
    package_structure.
    
    Implements tests ID TEST-T-730. Covers requirements REQ-FUN-730 and
    REQ-AWM-700.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.SelectPySourceFiles)
        strPath = os.path.join(MODULE_ROOT, 'temp')
        os.mkdir(strPath)
        cls.NewDir = strPath
        cls.Files = ['a.py', 'b.py', 'c.py']
        strPathLink = os.path.join(MODULE_ROOT, 'link')
        os.symlink(strPath, strPathLink, target_is_directory = True)
        cls.Link = strPathLink
        for strFile in cls.Files:
            strPath = os.path.join(cls.NewDir, strFile)
            with open(strPath, 'wt') as fFile:
                fFile.write('raise ImportError')
        strPath = os.path.join(cls.NewDir, cls.Files[-1])
        strLinkPath = os.path.join(cls.NewDir, 'link.py')
        cls.FileLink = strLinkPath
        os.symlink(strPath, strLinkPath)
        cls.NestedDir = os.path.join(cls.NewDir, 'test')
        os.mkdir(cls.NestedDir)
        cls.NestedFile = os.path.join(cls.NestedDir, 'd.py')
        with open(cls.NestedFile, 'wt') as fFile:
            fFile.write('raise ImportError')
        cls.BadCases = [1, 1.0, int, float, str, [1], (2.0, 'a'), ['a'],
                        {'a': 1}, {'a', 'b', 'c'}]
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleaning-up. Done only once.
        """
        os.remove(cls.Link)
        os.remove(cls.FileLink)
        os.remove(cls.NestedFile)
        os.rmdir(cls.NestedDir)
        for strFile in cls.Files:
            os.remove(os.path.join(cls.NewDir, strFile))
        os.rmdir(cls.NewDir)
    
    def test_Check_Ok(self):
        """
        Should return a list ['a.py', 'b.py', 'c.py'] (order of elements is
        not checked).
        
        Test ID TEST-T-730. Covers requirements REQ-FUN-730.
        """
        Result = self.TestFunction(self.NewDir)
        self.assertIsInstance(Result, list)
        self.assertCountEqual(Result, self.Files)
    
    def test_Check_Nok(self):
        """
        Should return an empty list.
        
        Test ID TEST-T-730. Covers requirements REQ-FUN-730.
        """
        Result = self.TestFunction(os.path.join(LIB_ROOT, 'Documentation'))
        #an exising folder, but without .py files
        self.assertIsInstance(Result, list)
        self.assertEqual(len(Result), 0)
        Result = self.TestFunction(self.Link) #created link
        self.assertIsInstance(Result, list)
        self.assertEqual(len(Result), 0)
        Result = self.TestFunction(MODULE_PATH) #existing file
        self.assertIsInstance(Result, list)
        self.assertEqual(len(Result), 0)
        Result = self.TestFunction(os.path.join(MODULE_ROOT,'temp2'))
        #a non-exising folder
        self.assertIsInstance(Result, list)
        self.assertEqual(len(Result), 0)
        Result = self.TestFunction(os.path.join(MODULE_ROOT,'whatever.py'))
        #a non-exising file
        self.assertIsInstance(Result, list)
        self.assertEqual(len(Result), 0)
    
    def test_Raises(self):
        """
        Should raise a (sub-) class TypeError exception if not a string argument
        is received.
        
        Test ID TEST-T-730. Covers requirements REQ-AWM-700.
        """
        for gItem in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(gItem)

class Test_GetQualifiedName(unittest.TestCase):
    """
    Test cases for the function GetQualifiedName() from the module
    package_structure.
    
    Implements tests ID TEST-T-740. Covers requirements REQ-FUN-740 and
    REQ-AWM-700.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.GetQualifiedName)
        cls.OldCWD = os.getcwd()
        strPath = os.path.join(MODULE_ROOT, 'a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        strPath = os.path.join(MODULE_ROOT, 'temp')
        os.mkdir(strPath)
        strPathLink = os.path.join(MODULE_ROOT, 'link')
        os.symlink(strPath, strPathLink, target_is_directory = True)
        os.mkdir(os.path.join(strPath, 'test'))
        strPath = os.path.join(MODULE_ROOT, 'temp', 'a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        strPath = os.path.join(MODULE_ROOT, 'temp', '__init__.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        strPath = os.path.join(MODULE_ROOT, 'temp', 'test', 'a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        strLinkPath = os.path.join(MODULE_ROOT, 'temp', 'test', 'link.py')
        os.symlink(strPath, strLinkPath)
        strPath = os.path.join(MODULE_ROOT, 'temp', 'test', '__init__.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        cls.BadCases = [1, 1.0, int, float, str, [1], (2.0, 'a'), ['a'],
                        {'a': 1}, {'a', 'b', 'c'}]
        os.chdir(MODULE_ROOT)
        cls.Resolved = {
            './a.py' : 'a',
            './temp' : 'temp',
            './temp/a.py' : 'temp.a',
            './temp/test' : 'temp.test',
            './temp/test/a.py' : 'temp.test.a',
            '../package_structure.py' : 'introspection_lib.package_structure',
            '../../introspection_lib' : 'introspection_lib'
        }
        cls.Unresolved = [ './b.py', './temp/test/b.py',  './temp/b.py',
                            './temp2', './link', '../README.md',
                            './temp/test/link.py']
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleaning-up. Done only once.
        """
        os.remove('./a.py')
        os.remove('./link')
        os.remove('./temp/test/link.py')
        os.remove('./temp/test/a.py')
        os.remove('./temp/test/__init__.py')
        os.remove('./temp/a.py')
        os.remove('./temp/__init__.py')
        os.rmdir('./temp/test')
        os.rmdir('./temp')
        os.chdir(cls.OldCWD)
    
    def test_Check_Ok(self):
        """
        Should return exactly the expected value.
        
        Test ID TEST-T-740. Covers requirements REQ-FUN-740.
        """
        for Value, Expected in self.Resolved.items():
            Result = self.TestFunction(Value)
            self.assertIsInstance(Result, str)
            self.assertEqual(Result, Expected)
    
    def test_Check_Nok(self):
        """
        Should return the None value.
        
        Test ID TEST-T-740. Covers requirements REQ-FUN-740.
        """
        for Value in self.Unresolved:
            Result = self.TestFunction(Value)
            self.assertIsNone(Result)
    
    def test_Raises(self):
        """
        Should raise a (sub-) class TypeError exception if not a string argument
        is received.
        
        Test ID TEST-T-740. Covers requirements REQ-AWM-700.
        """
        for gItem in self.BadCases:
            with self.assertRaises(TypeError):
                self.TestFunction(gItem)

class Test_ResolveRelativeImport(unittest.TestCase):
    """
    Test cases for the function ResolveRelativeImport() from the module
    package_structure.
    
    Implements tests ID TEST-T-750. Covers requirements REQ-FUN-750,
    REQ-AWM-700 and REQ-AWM-701.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.ResolveRelativeImport)
        cls.OldCWD = os.getcwd()
        strPath = os.path.join(LIB_ROOT, 'temp')
        os.mkdir(strPath)
        for strFile in ['a.py', '__init__.py']:
            with open(os.path.join(strPath, strFile), 'wt') as fFile:
                fFile.write('raise ImportError')
        strLink = os.path.join(LIB_ROOT, 'link')
        os.symlink(strPath, strLink, target_is_directory = True)
        strPath = os.path.join(strPath, 'test')
        os.mkdir(strPath)
        for strFile in ['a.py', '__init__.py']:
            with open(os.path.join(strPath, strFile), 'wt') as fFile:
                fFile.write('raise ImportError')
        strLink = os.path.join(strPath, 'link.py')
        strPath = os.path.join(strPath, 'a.py')
        os.symlink(strPath, strLink)
        os.chdir(LIB_ROOT)
        cls.BadTypes = [1, 1.0, int, float, str, [1], (2.0, 'a'), ['a'],
                        {'a': 1}, {'a', 'b', 'c'}]
        cls.AbsoluteImports = { #file path : import name
            'whatever' : 'whoever',
            './README.md' : 'os',
            './README.md' : 'os.path',
            './temp/test/a.py' : 'os',
            './temp/test/a.py' : 'os.path',
            './temp/test/a.py' : 'introspection_lib.temp.a'
        }
        cls.RelativeImports = [
            ['./package_structure.py', '.a', 'introspection_lib.a'],
            ['./temp/a.py', '.b', 'introspection_lib.temp.b'],
            ['./temp/a.py', '..package_structure',
                                        'introspection_lib.package_structure'],
            ['./temp/test/a.py', '.b', 'introspection_lib.temp.test.b'],
            ['./temp/test/a.py', '..test2.b', 'introspection_lib.temp.test2.b'],
            ['./temp/test/a.py', '..b', 'introspection_lib.temp.b'],
            ['./temp/test/a.py', '...package_structure',
                                        'introspection_lib.package_structure'],
            ['./temp/test/a.py', '...temp2.test2.b.c',
                                        'introspection_lib.temp2.test2.b.c']
        ]
        cls.WrongValues = [
            ['./temp', '.b'], #not a module but package
            ['./Documentation', '.b'], #not a module but a folder
            ['./temp2', '.b'], #not a module but a non-existing folder
            ['./whatever.py', '.b'], #not an existing file
            ['./README.md', '.b'], # existing, but not a source file
            ['./link', '.b'], #not a module but a symlink to a folder
            ['./temp/test/link.py', '.b'], #not a module but a symlink to a file
            ['./package_structure.py', '..b'], #outside the 'root'
            ['./temp/a.py', '...b'],
            ['./temp/test/a.py', '....b'],
            [MODULE_PATH, '.a'] #stand-alone module
        ]
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleaning-up. Done only once.
        """
        os.remove('./link')
        os.remove('./temp/test/link.py')
        os.remove('./temp/test/a.py')
        os.remove('./temp/test/__init__.py')
        os.remove('./temp/a.py')
        os.remove('./temp/__init__.py')
        os.rmdir('./temp/test')
        os.rmdir('./temp')
        os.chdir(cls.OldCWD)
    
    def test_RaisesTypeError(self):
        """
        Should raise a (sub-) class TypeError exception if not a string argument
        is received - any of two, or both
        
        Test ID TEST-T-750. Covers requirements REQ-AWM-700.
        """
        for Value in self.BadTypes:
            #first argument
            with self.assertRaises(TypeError):
                self.TestFunction(Value, 'os')
            with self.assertRaises(TypeError):
                self.TestFunction(Value, 'os.path')
            with self.assertRaises(TypeError):
                self.TestFunction(Value, '.a')
            #second argument
            with self.assertRaises(TypeError):
                self.TestFunction('whatever', Value)
            #both arguments
            with self.assertRaises(TypeError):
                self.TestFunction(Value, Value)
    
    def test_AbsoluteImport(self):
        """
        The second parameter should be returned regardless of the values of the
        both parameters, as long as both are strings.
        
        Test ID TEST-T-750. Covers requirements REQ-FUN-750.
        """
        for File, ImportName in self.AbsoluteImports.items():
            Result = self.TestFunction(File, ImportName)
            self.assertIsInstance(Result, str)
            self.assertEqual(Result, ImportName)
    
    def test_RelativeImport(self):
        """
        The relative import should be resolved properly as long as the both
        arguments are strings, the first argument points to an actual source
        file whithin a package, and the relative path does not lead outside the
        'root' package of the module.
        
        Test ID TEST-T-750. Covers requirements REQ-FUN-750.
        """
        for File, ImportName, Expected in self.RelativeImports:
            Result = self.TestFunction(File, ImportName)
            self.assertIsInstance(Result, str)
            self.assertEqual(Result, Expected)
    
    def test_RaisesValueError(self):
        """
        Should raise a (sub-) class ValueError exception if the relative import
        cannot be resolved properly.
        
        Test ID TEST-T-750. Covers requirements REQ-AWM-701.
        """
        for File, ImportName in self.WrongValues:
            with self.assertRaises(ValueError):
                self.TestFunction(File, ImportName)

class Test_PackageStructure(unittest.TestCase):
    """
    Test cases for the class PackageStructure from the module package_structure.
    
    Implements tests ID TEST-T-760 and TEST-T-761. Covers requirements
    REQ-FUN-760, REQ-FUN-761, REQ-FUN-762, REQ-FUN-763, REQ-AWM-700
    and REQ-AWM-701.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = TestModule.PackageStructure
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub1', 'subsub')
        os.makedirs(strPath)
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub2')
        os.makedirs(strPath)
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'build', 'lib64')
        os.makedirs(strPath)
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'tests')
        os.makedirs(strPath)
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'dist')
        os.makedirs(strPath)
        strPath = os.path.join(ROOT_FOLDER, 'test_package',
                                                        'test_package.egg-info')
        os.makedirs(strPath)
        strPath = os.path.join(ROOT_FOLDER, 'test_package', '__init__.py')
        with open(strPath, 'wt') as fFile:
            fFile.write("__project__ = 'test'\n")
            fFile.write("__version_info__ = (0.1.2)\n")
            fFile.write("__version_suffix__ = '-dev1'\n")
            fFile.write("__version__ = '.'.join(map(str, __version_info__))\n")
            fFile.write("__author__ = 'anton'\n")
            fFile.write("_author__ = 'john'\n")
            fFile.write("__date__ = 'jan 01'\n")
            fFile.write("__status__ = 'whatever'\n")
            fFile.write("__maintainer__ = 'whoever'\n")
            fFile.write("__license__ = 'LSD'\n")
            fFile.write("__copyright__ = 'what?'\n")
            fFile.write('import os, sys as my_sys\n')
            fFile.write('raise ImportError\n')
            fFile.write("def a():\n    __author__ = 'john'")
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('import os.path as os_path\n')
            fFile.write('import some_package\n')
            fFile.write('from sys import path\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'setup.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('import setuptools\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub1',
                                                                '__init__.py')
        with open(strPath, 'wt') as fFile:
            fFile.write("__version__ = '0.1.1'\n")
            fFile.write('import os.path\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub1', 'sub1_a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('import some_package.sub\n')
            fFile.write('from os.path import join as my_join, isdir\n')
            fFile.write('from ..a import something\n')
            fFile.write('from ...introspection_lib.package_structure import something_else\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub1', 'subsub',
                                                                '__init__.py')
        with open(strPath, 'wt') as fFile:
            fFile.write("__whatever__ = ''\n")
            fFile.write('import pip\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub1', 'subsub',
                                                                'subsub_a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('from ...sub2 import sub2_a\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub2',
                                                                '__init__.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub2', 'sub2_a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('from ..sub1.sub1_a import something\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'tests',
                                                                'test_a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('import unittest\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'build',
                                                                'build_a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('import package1\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'build', 'lib64',
                                                                'lib_a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('import package2\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'dist',
                                                                'dist_b.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('import package3\n')
            fFile.write('raise ImportError')
        strPath = os.path.join(ROOT_FOLDER, 'test_package',
                                            'test_package.egg-info', 'egg_a.py')
        with open(strPath, 'wt') as fFile:
            fFile.write('raise ImportError')
        cls.Dependencies = ['some_package', 'setuptools', 'pip', 'package1',
                            'package2', 'package3']
        cls.DefDependencies = ['some_package', 'pip']
        cls.Mapping = {
            '__init__.py' : {
                'os' : 'os',
                'my_sys' : 'sys'
            },
            'a.py' : {
                'os_path' : 'os.path',
                'some_package' : 'some_package',
                'path' : 'sys.path'
            },
            'setup.py' : {
                'setuptools' : 'setuptools'
            },
            'sub1/__init__.py' : {
                'os.path' : 'os.path'
            },
            'sub1/sub1_a.py' : {
                'some_package.sub' : 'some_package.sub',
                'my_join' : 'os.path.join',
                'isdir' : 'os.path.isdir',
                'something' : 'test_package.a.something'
            },
            'sub1/subsub/__init__.py' : {
                'pip' : 'pip'
            },
            'sub1/subsub/subsub_a.py' : {
                'sub2_a' : 'test_package.sub2.sub2_a' 
            },
            'sub2/sub2_a.py' : {
                'something' : 'test_package.sub1.sub1_a.something'
            },
            'tests/test_a.py' : {
                'unittest' : 'unittest'
            },
            'build/build_a.py' : {
                'package1' : 'package1'
            },
            'build/lib64/lib_a.py' : {
                'package2' : 'package2'
            },
            'dist/dist_b.py' : {
                'package3' : 'package3'
            }
        }
        cls.DefMapping = {
            '__init__.py' : {
                'os' : 'os',
                'my_sys' : 'sys'
            },
            'a.py' : {
                'os_path' : 'os.path',
                'some_package' : 'some_package',
                'path' : 'sys.path'
            },
            'sub1/__init__.py' : {
                'os.path' : 'os.path'
            },
            'sub1/sub1_a.py' : {
                'some_package.sub' : 'some_package.sub',
                'my_join' : 'os.path.join',
                'isdir' : 'os.path.isdir',
                'something' : 'test_package.a.something'
            },
            'sub1/subsub/__init__.py' : {
                'pip' : 'pip'
            },
            'sub1/subsub/subsub_a.py' : {
                'sub2_a' : 'test_package.sub2.sub2_a' 
            },
            'sub2/sub2_a.py' : {
                'something' : 'test_package.sub1.sub1_a.something'
            },
            'tests/test_a.py' : {
                'unittest' : 'unittest'
            }
        }
        cls.Paths = [
            '__init__.py',
            'setup.py',
            'a.py',
            'sub1/__init__.py',
            'sub1/sub1_a.py',
            'sub1/subsub/__init__.py',
            'sub1/subsub/subsub_a.py',
            'sub2/__init__.py',
            'sub2/sub2_a.py',
            'tests/test_a.py',
            'build/build_a.py',
            'build/lib64/lib_a.py',
            'dist/dist_b.py',
            'test_package.egg-info/egg_a.py'
        ]
        cls.DefPaths = [
            '__init__.py',
            'a.py',
            'sub1/__init__.py',
            'sub1/sub1_a.py',
            'sub1/subsub/__init__.py',
            'sub1/subsub/subsub_a.py',
            'sub2/__init__.py',
            'sub2/sub2_a.py',
            'tests/test_a.py',
        ]
        cls.RootPath = os.path.join(ROOT_FOLDER, 'test_package')
        cls.Packages = ['test_package', 'test_package.sub1',
                            'test_package.sub1.subsub', 'test_package.sub2',
                            'test_package.tests', 'test_package.build',
                            'test_package.build.lib64',
                            'test_package.dist',
                            'test_package.test_package.egg-info']
        cls.DefPackages = ['test_package', 'test_package.sub1',
                            'test_package.sub1.subsub', 'test_package.sub2',
                            'test_package.tests']
        cls.NotString = [1, 1.0, ['absdf'], tuple(MODULE_ROOT), int, float, str,
                                                                {'a' : 'b'}]
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleaning-up. Done only once.
        """
        shutil.rmtree(cls.RootPath)
    
    def test_init(self):
        """
        Proper default functionality of the class.

        Test ID: TEST-T-760. Covers requirements REQ-FUN-760, REQ-FUN-761
        and REQ-FUN-763.
        """
        self.maxDiff = None
        objTest = self.TestClass(self.RootPath)
        self.assertEqual(objTest.Package, 'test_package')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, self.DefPaths)
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, self.DefDependencies)
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, self.DefMapping)
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, self.DefPackages)
        dictTest = {
            '__project__' : {
                'line' : 0,
                'value' : "'test'"
            },
            '__version_info__' : {
                'line' : 1,
                'value' : '(0.1.2)'
            },
            '__version_suffix__' : {
                'line' : 2,
                'value' : "'-dev1'"
            },
            '__version__' : {
                'line' : 3,
                'value' : "'.'.join(map(str, __version_info__))"
            },
            '__author__' : {
                'line' : 4,
                'value' : "'anton'"
            },
            '__date__' : {
                'line' : 6,
                'value' : "'jan 01'"
            },
            '__status__' : {
                'line' : 7,
                'value' : "'whatever'"
            },
            '__maintainer__' : {
                'line' : 8,
                'value' :  "'whoever'"
            },
            '__license__' : {
                'line' : 9,
                'value' :  "'LSD'"
            },
            '__copyright__' : {
                'line' : 10,
                'value' :  "'what?'"
            }
        }
        gTest = objTest.Metadata
        self.assertCountEqual(list(gTest.keys()), list(dictTest.keys()))
        for strKey in dictTest.keys():
            self.assertDictEqual(gTest[strKey], dictTest[strKey])
        del objTest
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub1')
        objTest = self.TestClass(strPath)
        self.assertEqual(objTest.Package, 'test_package.sub1')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, ['__init__.py', 'sub1_a.py',
                                    'subsub/__init__.py', 'subsub/subsub_a.py'])
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, ['pip', 'some_package'])
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, {'subsub/subsub_a.py' :
                                        {'sub2_a' : 'test_package.sub2.sub2_a'},
                                    'subsub/__init__.py' : {'pip' : 'pip'},
                                    '__init__.py' : {'os.path' : 'os.path'},
                                    'sub1_a.py' : {
                                        'some_package.sub' : 'some_package.sub',
                                        'my_join' : 'os.path.join',
                                        'isdir' : 'os.path.isdir',
                                        'something' : 'test_package.a.something'
                                        }})
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, ['sub1', 'sub1.subsub'])
        gTest = objTest.Metadata
        self.assertIsInstance(gTest, dict)
        self.assertCountEqual(list(gTest.keys()), ['__version__'])
        self.assertDictEqual(gTest['__version__'], {'line' : 0,
                                                    'value' : "'0.1.1'"})
        del objTest
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub1', 'subsub')
        objTest = self.TestClass(strPath)
        self.assertEqual(objTest.Package, 'test_package.sub1.subsub')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, ['__init__.py', 'subsub_a.py'])
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, ['pip'])
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, {'subsub_a.py' :
                                        {'sub2_a' : 'test_package.sub2.sub2_a'},
                                    '__init__.py' : {'pip' : 'pip'}})
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, ['subsub'])
        gTest = objTest.Metadata
        self.assertDictEqual(gTest, dict())
        del objTest
        strPath = os.path.join(ROOT_FOLDER, 'test_package', 'sub2')
        objTest = self.TestClass(strPath)
        self.assertEqual(objTest.Package, 'test_package.sub2')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, ['__init__.py', 'sub2_a.py'])
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, [])
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, {'sub2_a.py' :
                        {'something' : 'test_package.sub1.sub1_a.something'}})
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, ['sub2'])
        gTest = objTest.Metadata
        self.assertDictEqual(gTest, dict())
        del objTest

    def test_init_TypeError(self):
        """
        Should raise TypeError or its sub-class if the argument of the
        initializer method is not a string.

        Test ID: TEST-T-760. Covers requirement REQ-AWM-700.
        """
        for gPath in self.NotString:
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestClass(gPath)

    def test_init_ValueError(self):
        """
        Should raise ValueError or its sub-class if the argument of the
        initializer method is a string, but not a path to a Python package

        Test ID: TEST-T-760. Covers requirement REQ-AWM-701.
        """
        for strPath in ['', ROOT_FOLDER, 'absdf', MODULE_ROOT,
                            os.path.join(ROOT_FOLDER, 'test_package', 'tests')]:
            with self.assertRaises(ValueError, msg = strPath):
                self.TestClass(strPath)
    
    def test_ModifyFiltering(self):
        """
        Checks correctness of modification of the filtering parameters. The
        alreade cached data should be invalidated.

        Test ID: TEST-T-761. Covers requirement REQ-FUN-762.
        """
        objTest = self.TestClass(self.RootPath)
        self.assertEqual(objTest.Package, 'test_package')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, self.DefPaths)
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, self.DefDependencies)
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, self.DefMapping)
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, self.DefPackages)
        objTest.addFilesFilter('*a.py')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, ['__init__.py', 'sub1/__init__.py',
                                        'sub1/subsub/__init__.py',
                                        'sub2/__init__.py'])
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, ['pip'])
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, {'__init__.py' : {
                                                    'os' : 'os',
                                                    'my_sys' : 'sys'
                                                },
                                        'sub1/__init__.py' : {
                                                    'os.path' : 'os.path'
                                                },
                                        'sub1/subsub/__init__.py' : {
                                                    'pip' : 'pip'
                                                }})
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, ['test_package', 'test_package.sub1',
                            'test_package.sub1.subsub', 'test_package.sub2'])
        objTest.removeFilesFilter('setup.py')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, ['__init__.py', 'sub1/__init__.py',
                                        'sub1/subsub/__init__.py',
                                        'sub2/__init__.py', 'setup.py'])
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, ['pip', 'setuptools'])
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, {'__init__.py' : {
                                                    'os' : 'os',
                                                    'my_sys' : 'sys'
                                                },
                                        'sub1/__init__.py' : {
                                                    'os.path' : 'os.path'
                                                },
                                        'sub1/subsub/__init__.py' : {
                                                    'pip' : 'pip'
                                                },
                                        'setup.py' : {
                                            'setuptools' : 'setuptools'}})
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, ['test_package', 'test_package.sub1',
                            'test_package.sub1.subsub', 'test_package.sub2'])
        objTest.addFoldersFilter('*subsub')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, ['__init__.py', 'sub1/__init__.py',
                                        'sub2/__init__.py', 'setup.py'])
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, ['setuptools'])
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, {'__init__.py' : {
                                                    'os' : 'os',
                                                    'my_sys' : 'sys'
                                                },
                                        'sub1/__init__.py' : {
                                                    'os.path' : 'os.path'
                                                },
                                        'setup.py' : {
                                            'setuptools' : 'setuptools'}})
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, ['test_package', 'test_package.sub1',
                            'test_package.sub2'])
        objTest.removeFoldersFilter('dist')
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, ['__init__.py', 'sub1/__init__.py',
                                        'sub2/__init__.py', 'setup.py',
                                        'dist/dist_b.py'])
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, ['setuptools', 'package3'])
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, {'__init__.py' : {
                                                    'os' : 'os',
                                                    'my_sys' : 'sys'
                                                },
                                        'sub1/__init__.py' : {
                                                    'os.path' : 'os.path'
                                                },
                                        'setup.py' : {
                                            'setuptools' : 'setuptools'},
                                        'dist/dist_b.py' : {
                                            'package3' : 'package3'}})
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, ['test_package', 'test_package.sub1',
                            'test_package.sub2', 'test_package.dist'])
        objTest.setFilesFilters([])
        objTest.setFoldersFilters([])
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, self.Paths)
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, self.Dependencies)
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, self.Mapping)
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, self.Packages)
        objTest.setFilesFilters(['setup.py'])
        objTest.setFoldersFilters(['*build*', '*dist*', '*egg*'])
        gTest = objTest.getModules()
        self.assertCountEqual(gTest, self.DefPaths)
        gTest = objTest.getDependencies()
        self.assertCountEqual(gTest, self.DefDependencies)
        gTest = objTest.getImportNames()
        self.assertDictEqual(gTest, self.DefMapping)
        gTest = objTest.getPackagingNames()
        self.assertCountEqual(gTest, self.DefPackages)
        del objTest
    
    def test_addFilesFilter_Raises(self):
        """
        Should raise TypeError or its sub-class if the argument of the
        method is not a string.

        Test ID: TEST-T-761. Covers requirement REQ-AWM-700.
        """
        objTest = self.TestClass(self.RootPath)
        for gPath in self.NotString:
            with self.assertRaises(TypeError, msg = str(gPath)):
                objTest.addFilesFilter(gPath)
        del objTest
    
    def test_removeFilesFilter_Raises(self):
        """
        Should raise TypeError or its sub-class if the argument of the
        method is not a string.

        Test ID: TEST-T-761. Covers requirement REQ-AWM-700.
        """
        objTest = self.TestClass(self.RootPath)
        for gPath in self.NotString:
            with self.assertRaises(TypeError, msg = str(gPath)):
                objTest.removeFilesFilter(gPath)
        del objTest
    
    def test_setFilesFilters_Raises(self):
        """
        Should raise TypeError or its sub-class if the argument of the
        method is not a sequence of strings.

        Test ID: TEST-T-761. Covers requirement REQ-AWM-700.
        """
        objTest = self.TestClass(self.RootPath)
        for gPath in self.NotString:
            with self.assertRaises(TypeError, msg = str(gPath)):
                objTest.setFilesFilters(['a', gPath])
            if not isinstance(gPath, c_abc.Sequence):
                with self.assertRaises(TypeError, msg = str(gPath)):
                    objTest.setFilesFilters(gPath)
        del objTest

    def test_addFoldersFilter_Raises(self):
        """
        Should raise TypeError or its sub-class if the argument of the
        method is not a string.

        Test ID: TEST-T-761. Covers requirement REQ-AWM-700.
        """
        objTest = self.TestClass(self.RootPath)
        for gPath in self.NotString:
            with self.assertRaises(TypeError, msg = str(gPath)):
                objTest.addFoldersFilter(gPath)
        del objTest
    
    def test_removeFoldersFilter_Raises(self):
        """
        Should raise TypeError or its sub-class if the argument of the
        method is not a string.

        Test ID: TEST-T-761. Covers requirement REQ-AWM-700.
        """
        objTest = self.TestClass(self.RootPath)
        for gPath in self.NotString:
            with self.assertRaises(TypeError, msg = str(gPath)):
                objTest.removeFoldersFilter(gPath)
        del objTest
    
    def test_setFoldersFilters_Raises(self):
        """
        Should raise TypeError or its sub-class if the argument of the
        method is not a sequence of strings.

        Test ID: TEST-T-761. Covers requirement REQ-AWM-700.
        """
        objTest = self.TestClass(self.RootPath)
        for gPath in self.NotString:
            with self.assertRaises(TypeError, msg = str(gPath)):
                objTest.setFoldersFilters(['a', gPath])
            if not isinstance(gPath, c_abc.Sequence):
                with self.assertRaises(TypeError, msg = str(gPath)):
                    objTest.setFoldersFilters(gPath)
        del objTest

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_IsPyFile)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_IsPyPackage)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_SelectPySourceFiles)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetQualifiedName)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_ResolveRelativeImport)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_PackageStructure)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting introspection_lib.package_structure module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)