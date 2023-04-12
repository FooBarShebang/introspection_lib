#!/usr/bin/python
"""
Module introspection_lib.Tests.UT005_structure_map

Implements unit testing of the module structure_map. See test report TE006.
"""

__version__ = "1.0.0.0"
__date__ = "26-03-2021"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import collections

#+ tested module

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import introspection_lib.structure_map as TestModule

#helper functions

def TestFunc():
    pass

#classes

#+ helper classes

class FrozenDict(collections.abc.Mapping): #immutable dictionary
    def __init__(self, Other):
        self._Data = {strKey: gValue for strKey, gValue in Other.items()}
    
    def __getitem__(self, strKey):
        return self._Data[strKey]
    
    def __iter__(self):
        return iter(self._Data)
    
    def __len__(self):
        return len(self._Data.keys())

TestNamedTuple = collections.namedtuple('TestNamedTuple',
                                                ['a','b','c','d', 'e'])

#+ test cases

class Test_GetReadMap(unittest.TestCase):
    """
    Test cases for the function GetReadMap() from the module structure_map.
    
    Implements tests ID TEST-T-600 and TEST-T-610. Covers requirements
    REQ-FUN-600, REQ-FUN-601, REQ-FUN-602, REQ-FUN-610, REQ-FUN-611, REQ-FUN-612
    and REQ-AWM-600.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.GetReadMap)
        cls.EmptySequences = [list(), [], tuple(), ()]
        cls.EmptyMappings = [dict(), {}, FrozenDict({}),
                                collections.OrderedDict(),
                                collections.namedtuple('whatever', [])]
        cls.Scalars = [None, 1, -25, 1.2, 1.2E-3, True, False, "",
            '', "absd", 'a1nffc', '1', "4acc5.4e-3", 'abs']
        cls.MutableSequences = [
            [[1], [1]], [['a'], ['a']],
                [[int, 1, 'a', abs, 1.2, str], [1, 'a', 1.2]]
        ]
        cls.ImmutableSequences = [
            [(1,), [1]], [('a',), ['a']],
                [(int, 1, 'a', abs, 1.2, str), [1, 'a', 1.2]]
        ]
        cls.MutableMappings = [
            [{'a' : 1, 'b' : int}, collections.OrderedDict({'a' : 1})],
            [{'b' : str, 'a' : 'a'}, collections.OrderedDict({'a' : 'a'})],
            [{'a' : 1, 'b' : 'a', 'c' : abs, 'd' : 1.2, 'e' : TestFunc}, 
            collections.OrderedDict([('a' , 1), ('b' , 'a'), ('d' , 1.2)])]
        ]
        cls.ImmutableMappings = [
            [FrozenDict({'a' : 1, 'b' : int}),
                            collections.OrderedDict({'a' : 1})],
            [FrozenDict({'b' : str, 'a' : 'a'}),
                            collections.OrderedDict({'a' : 'a'})],
            [FrozenDict({'a' : 1, 'b' : 'a', 'c' : abs, 'd' : 1.2}), 
                collections.OrderedDict([('a' , 1), ('b' , 'a'), ('d' , 1.2)])],
            [TestNamedTuple(1, 'a', abs, 1.2, TestFunc), 
                collections.OrderedDict([('a' , 1), ('b' , 'a'), ('d' , 1.2)])]
        ]
        cls.ClassInstances = []
        cls.GenericNestedObjects = []
        cls.ImproperInput = [int, float, bool, str, abs, round, TestFunc,
                                range(0, 100), {1, 2, 3}, {1: 'a', 'b' : 'b'},
                                [1, 2, 'c', {1 : 'a'}]]
    
    def test_EmptySequences(self):
        """
        Checks that any empty sequence, except for a named tuple is converted
        into an empty list.

        TEST-T-610. Requirements REQ-FUN-600, REQ-FUN-601, REQ-FUN-610.
        """
        for gElement in self.EmptySequences:
            gTest = self.TestFunction(gElement)
            self.assertIsInstance(gTest, list)
            self.assertTrue(len(gTest) == 0, msg = 'Length of the sequence')

    def test_EmptyMappings(self):
        """
        Checks that any empty mapping type or named tuple is convered into an
        empty ordered dictionary.

        TEST-T-610. Requirements REQ-FUN-600, REQ-FUN-601, REQ-FUN-611.
        """
        for gElement in self.EmptyMappings:
            gTest = self.TestFunction(gElement)
            self.assertIsInstance(gTest, collections.OrderedDict)
            self.assertTrue(len(gTest.keys()) == 0,
                                                msg = 'Length of the sequence')

    def test_Scalars(self):
        """
        Checks that the same type and value is returned with a scalar input.

        TEST-T-610. Requirements REQ-FUN-600, REQ-FUN-601.
        """
        for gElement in self.EmptyMappings:
            gTest = self.TestFunction(gElement)
            if gElement is None:
                self.assertIsNone(gTest)
            else:
                self.assertIsInstance(gTest, type(gElement))
                self.assertEqual(gTest, gElement)

    def test_PlainSequences(self):
        """
        Checks the proper structure mapping of plain sequences, except fo the
        named tuples. The returned type should be a list, the elements are
        preserved by order and values, except for the callable elements, which
        should be removed.

        TEST-T-610. Requirements REQ-FUN-600, REQ-FUN-601, REQ-FUN-610.
        """
        for gInput, gOutput in self.MutableSequences:
            gTest = self.TestFunction(gInput)
            self.assertIsInstance(gTest, list)
            self.assertListEqual(gTest, gOutput)
        for gInput, gOutput in self.ImmutableSequences:
            gTest = self.TestFunction(gInput)
            self.assertIsInstance(gTest, list)
            self.assertListEqual(gTest, gOutput)

    def test_PlainMappings(self):
        """
        Checks the proper structure mapping of plain mapping types and named
        tuples. The returned type should be an ordered dict with the callable
        values entries being ignored, but the rest of the key:value pairs
        preserved and in order.

        TEST-T-610. Requirements REQ-FUN-600, REQ-FUN-601, REQ-FUN-611.
        """
        for gInput, gOutput in self.MutableMappings:
            gTest = self.TestFunction(gInput)
            self.assertIsInstance(gTest, collections.OrderedDict)
            self.assertDictEqual(gTest, gOutput)
            self.assertSequenceEqual(gTest.keys(), gOutput.keys())
        for gInput, gOutput in self.ImmutableMappings:
            gTest = self.TestFunction(gInput)
            self.assertIsInstance(gTest, collections.OrderedDict)
            self.assertDictEqual(gTest, gOutput)
            self.assertSequenceEqual(gTest.keys(), gOutput.keys())

    def test_ClassInstances(self):
        """
        TEST-T-610. Requirements REQ-FUN-600, REQ-FUN-601, REQ-FUN-602,
        REQ-FUN-612.
        """
        pass

    def test_GenericNestedObjects(self):
        """
        TEST-T-610. Requirements REQ-FUN-600, REQ-FUN-601, REQ-FUN-602,
        REQ-FUN-610, REQ-FUN-611, REQ-FUN-612.
        """
        pass

    def test_TypeError(self):
        """
        Checks that a sub-class of TypeError is raised with improper type of
        the input argument.

        TEST-T-600. Requirements REQ-AWM-600.
        """
        for gElement in self.ImproperInput:
            with self.assertRaises(TypeError, msg= '{}'.format(type(gElement))):
                self.TestFunction(gElement)

class Test_GetWriteMap(Test_GetReadMap):
    """
    Test cases for the function GetWriteMap() from the module structure_map.
    
    Implements tests ID TEST-T-600 and TEST-T-620. Covers requirements
    REQ-FUN-600, REQ-FUN-601, REQ-FUN-602, REQ-FUN-620, REQ-FUN-621, REQ-FUN-622
    and REQ-AWM-600
    """

    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        super().setUpClass()
        cls.TestFunction = staticmethod(TestModule.GetWriteMap)
    
    def test_PlainSequences(self):
        """
        Checks the proper structure mapping of plain mutable sequences. The
        returned type should be a list, the elements are preserved by order and
        values, except for the callable elements, which should be removed.

        Any immutable sequence, except for a named tuple, should be converted
        into an empty list.

        TEST-T-610. Requirements REQ-FUN-600, REQ-FUN-601, REQ-FUN-620.
        """
        for gInput, gOutput in self.MutableSequences:
            gTest = self.TestFunction(gInput)
            self.assertIsInstance(gTest, list)
            self.assertListEqual(gTest, gOutput)
        for gInput, gOutput in self.ImmutableSequences:
            gTest = self.TestFunction(gInput)
            self.assertIsInstance(gTest, list)
            self.assertTrue(len(gTest) == 0, msg = 'Length of the sequence')

    def test_PlainMappings(self):
        """
        Checks the proper structure mapping of plain mutable mapping types. The
        returned type should be an ordered dict with the callable values entries
        being ignored, but the rest of the key:value pairs preserved and in
        order.

        For any immutable mapping type or a named tuple (plain) the returned
        value should be an empty ordered dictionary.

        TEST-T-620. Requirements REQ-FUN-600, REQ-FUN-601, REQ-FUN-621.
        """
        for gInput, gOutput in self.MutableMappings:
            gTest = self.TestFunction(gInput)
            self.assertIsInstance(gTest, collections.OrderedDict)
            self.assertDictEqual(gTest, gOutput)
            self.assertSequenceEqual(gTest.keys(), gOutput.keys())
        for gInput, gOutput in self.ImmutableMappings:
            gTest = self.TestFunction(gInput)
            self.assertIsInstance(gTest, collections.OrderedDict)
            self.assertIsInstance(gTest, collections.OrderedDict)
            self.assertTrue(len(gTest.keys()) == 0,
                                                msg = 'Length of the sequence')

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_GetReadMap)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_GetWriteMap)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting introspection_lib.structure_map module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)