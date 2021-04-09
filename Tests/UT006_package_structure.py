#!/usr/bin/python
"""
Module introspection_lib.Tests.UT006_package_structure

Implements unit testing of the module package_structure. See test report TE007.
"""

__version__ = "1.0.0.0"
__date__ = "07-04-2021"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
#import collections

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

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_IsPyFile)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_IsPyPackage)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_SelectPySourceFiles)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_GetQualifiedName)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_ResolveRelativeImport)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting introspection_lib.package_structure module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)