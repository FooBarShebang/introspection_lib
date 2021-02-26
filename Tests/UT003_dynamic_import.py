#!/usr/bin/python
"""
Module introspection_lib.Tests.UT003_dynamic_import

Implements unit testing of the module dynamic_import. See test report TE004.
"""

__version__ = "1.0.0.0"
__date__ = "26-02-2021"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest

#+ tested module

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import introspection_lib.dynamic_import as TestModule

#globals - helper test values

FILENAME = os.path.basename(__file__)

#helper functions

def UnloadOS():
    """
    Unloads the package 'os', hence all its modules.
    """
    if 'os' in dir():
        del os
        sys.stdout.write('\nModule "os" is not unloaded\n')
        sys.stdout.flush()
        sys.exit(1)
    try:
        print(os.path.basename(__file__))
    except NameError:
        sys.stdout.write('\nModule "os" is unloaded\n')
        sys.stdout.flush()

#classes

#+ test cases

class Test_import_module(unittest.TestCase):
    """
    Test cases for the function import_module from the module dynamic_import.
    
    Implements tests ID TEST-T-400, TEST-T-401, TEST-T-402 and TEST-T-403.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.import_module)
        cls.NotStrings = [1, 1.0, [1], ("1",), {1, "1"}, int, float, str, dict,
                                                                    {"1" : 1}]
        cls.NotDict =[1, 1.0, [1], ("1",), {1, "1"}, int, float, str, dict, "1"]
    
    def test_import_module(self):
        """
        Tests the functional importing of a module.

        Test ID - TEST-T-400. Covers requirements REQ-FUN-400, REQ-FUN-420
        and REQ-FUN-421
        """
        Temp = self.TestFunction('os.path', dictGlobals = globals())
        self.assertEqual(Temp.basename(__file__), FILENAME,
                                                    msg = 'By module reference')
        self.assertEqual(os.path.basename(__file__), FILENAME,
                                                    msg = 'By module name')
        del Temp
        Temp = None
        UnloadOS()
    
    def test_import_module_alias(self):
        """
        Tests the functional importing of a module with aliasing.

        Test ID - TEST-T-401. Covers requirements REQ-FUN-401, REQ-FUN-420
        and REQ-FUN-421
        """
        Temp = self.TestFunction('os.path', 'Alias', dictGlobals = globals())
        self.assertEqual(Temp.basename(__file__), FILENAME,
                                                    msg = 'By module reference')
        self.assertEqual(Alias.basename(__file__), FILENAME,
                                                    msg = 'By module alias')
        del Temp
        Temp = None
        UnloadOS()
    
    def test_TypeError(self):
        """
        Checks that a sub-class of TypeError exception is raised if a wrong type
        argument is receviced.

        Test ID - TEST-T-402. Covers requirement REQ-AWM-400.
        """
        for gValue in self.NotStrings:
            with self.assertRaises(TypeError):
                self.TestFunction(gValue, 'Alias')
            with self.assertRaises(TypeError):
                self.TestFunction('os.path', gValue)
        for gValue in self.NotDict:
            with self.assertRaises(TypeError):
                self.TestFunction('os.path', 'Alias', dictGlobals = gValue)
    
    def test_ValueError(self):
        """
        Checks that a sub-class of ValueError exception is raised if a string
        but not-existing value is received as the module name argument.

        Test ID - TEST-T-403. Covers requirement REQ-AWM-401.
        """
        with self.assertRaises(ValueError):
            self.TestFunction('ois.path', 'Alias')
        with self.assertRaises(ValueError):
            self.TestFunction('os.patih', 'Alias')

class Test_import_from_module(unittest.TestCase):
    """
    Test cases for the function import_from_module from the module
    dynamic_import.
    
    Implements tests ID TEST-T-410, TEST-T-411, TEST-T-412 and TEST-T-413.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.import_from_module)
        cls.NotStrings = [1, 1.0, [1], ("1",), {1, "1"}, int, float, str, dict,
                                                                    {"1" : 1}]
        cls.NotDict =[1, 1.0, [1], ("1",), {1, "1"}, int, float, str, dict, "1"]
    
    def test_import_from_module(self):
        """
        Tests the functional importing of a module.

        Test ID - TEST-T-410. Covers requirements REQ-FUN-410, REQ-FUN-420
        and REQ-FUN-421
        """
        Temp = self.TestFunction('os.path', 'basename', dictGlobals = globals())
        self.assertEqual(Temp(__file__), FILENAME,
                                                msg = 'By function reference')
        self.assertEqual(basename(__file__), FILENAME,
                                                msg = 'By function name')
        del Temp
        Temp = None
        UnloadOS()
    
    def test_import_from_module_alias(self):
        """
        Tests the functional importing of a module with aliasing.

        Test ID - TEST-T-411. Covers requirements REQ-FUN-411, REQ-FUN-420
        and REQ-FUN-421
        """
        Temp = self.TestFunction('os.path', 'basename', 'Alias',
                                                    dictGlobals = globals())
        self.assertEqual(Temp(__file__), FILENAME,
                                                msg = 'By function reference')
        self.assertEqual(Alias(__file__), FILENAME,
                                                msg = 'By function alias')
        del Temp
        Temp = None
        UnloadOS()
    
    def test_TypeError(self):
        """
        Checks that a sub-class of TypeError exception is raised if a wrong type
        argument is receviced.

        Test ID - TEST-T-412. Covers requirement REQ-AWM-400.
        """
        for gValue in self.NotStrings:
            with self.assertRaises(TypeError):
                self.TestFunction(gValue, 'basename', 'Alias')
            with self.assertRaises(TypeError):
                self.TestFunction('os.path', gValue, 'Alias')
            with self.assertRaises(TypeError):
                self.TestFunction('os.path', 'basename', gValue)
        for gValue in self.NotDict:
            with self.assertRaises(TypeError):
                self.TestFunction('os.path', 'basename', 'Alias',
                                                        dictGlobals = gValue)
    
    def test_ValueError(self):
        """
        Checks that a sub-class of ValueError exception is raised if a string
        but not-existing value is received as the module or component name
        argument.

        Test ID - TEST-T-413. Covers requirement REQ-AWM-401.
        """
        with self.assertRaises(ValueError):
            self.TestFunction('ois.path', 'basename', 'Alias')
        with self.assertRaises(ValueError):
            self.TestFunction('os.patih', 'basename', 'Alias')
        with self.assertRaises(ValueError):
            self.TestFunction('os.path', 'baisename', 'Alias')

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_import_module)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(
                                                    Test_import_from_module)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write(
                "Conducting introspection_lib.dynamic_import module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)