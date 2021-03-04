#!/usr/bin/python
"""
Module introspection_lib.Tests.UT004_universal_access

Implements unit testing of the module universal_access. See test report TE005.
"""

__version__ = "1.0.0.0"
__date__ = "26-02-2021"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import collections
import random

#+ tested module

LIB_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

ROOT_FOLDER = os.path.dirname(LIB_ROOT)

if not (ROOT_FOLDER in sys.path):
    sys.path.append(ROOT_FOLDER)

import introspection_lib.universal_access as TestModule

#classes

#+ helper classes

class SimpleStruct(): #mutable plain structure
    a = 1
    b = 2
    c = 3

NamedTuple = collections.namedtuple('NamedTuple', ['a', 'b', 'c'])

#named tuple - immutable sequence and struct at the same time

class FrozenDict(collections.abc.Mapping): #immutable dictionary
    def __init__(self, Other):
        self._Data = {strKey: gValue for strKey, gValue in Other.items()}
    
    def __getitem__(self, strKey):
        return self._Data[strKey]
    
    def __iter__(self):
        return iter(self._Data)
    
    def __len__(self):
        return len(self._Data.keys())

class ComplexStruct(): #mutable object of complex structure
    
    def __init__(self):
        self.a = 1
        self.b = [1, 2, 3]
        self.c = {
            'a' : 1,
            'b' : NamedTuple(1, 2, 3),
            'c' : FrozenDict({'a' : 1, 'b' : {'a' : 1}}),
            'd' : (1, 2),
            'e' : [
                [1, 2, 3],
                {'a' : 1},
                SimpleStruct()
            ]
        }

#+ test cases

class Test_FlattenPath(unittest.TestCase):
    """
    Test cases for the function FlattenPath() from the module universal_access.
    
    Implements tests ID TEST-T-500. Covers requirements REQ-FUN-500 and
    REQ-AWM-500.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestFunction = staticmethod(TestModule.FlattenPath)
    
    def test_NormalOperation(self):
        """
        Tests that the proper defined paths in generic form are properly
        converted into canonical form, according to the rules in DE001.

        Test ID - TEST-T-500. Covers requirements REQ-FUN-500.
        """
        tuplstCases = [
            (1, [1]),
            ('1', ['1']),
            ('a', ['a']),
            ('a.b', ['a', 'b']),
            ('a.b.c', ['a', 'b', 'c']),
            ((1, ), [1]),
            (('1', ), ['1']),
            (('a', ), ['a']),
            (('a.b', ), ['a', 'b']),
            (('a.b.c', ), ['a', 'b', 'c']),
            ([1], [1]),
            (['1'], ['1']),
            (['a'], ['a']),
            (['a.b'], ['a', 'b']),
            (['a.b.c'], ['a', 'b', 'c']),
            ([1, 'a.b.c'], [1, 'a', 'b', 'c']),
            (['a.b.c', 1], ['a', 'b', 'c', 1]),
            (['a.b.c', 1, "d.e", 2], ['a', 'b', 'c', 1, 'd', 'e', 2]),
            (['a.b.c', [1, "d.e"], 2], ['a', 'b', 'c', 1, 'd', 'e', 2]),
            (['a.b.c', [1, ["d.e"]], 2], ['a', 'b', 'c', 1, 'd', 'e', 2]),
            (['a.b.c', [1, ["d.e", 'f']], 2],
                                        ['a', 'b', 'c', 1, 'd', 'e', 'f', 2]),
            (['a.b.c', [1, ["d.e", 'f', []]], 2],
                                        ['a', 'b', 'c', 1, 'd', 'e', 'f', 2]),
            (('a.b.c', [1, ["d.e", 'f', []], []], 2),
                                        ['a', 'b', 'c', 1, 'd', 'e', 'f', 2]),
            (('a.b.c', [1, ["d.e", 'f', []], []], 2, tuple()),
                                        ['a', 'b', 'c', 1, 'd', 'e', 'f', 2]),
            ([[], 1], [1]),
            ([], []),
            (tuple(), [])
        ]
        for GPath, CPath in tuplstCases:
            self.assertListEqual(self.TestFunction(GPath), CPath,
                                                msg = 'from {}'.format(GPath))
    
    def test_NonConformPath(self):
        """
        Tests that TypeError compatible exception is raised when the passed
        generic path is not formed according to the rules in DE001.

        Test ID - TEST-T-500. Covers requirements REQ-AWM-500.
        """
        lstCases = [1.0, int, str, {"a" : 1}, FrozenDict({"a" : 1}),
            [1.0], [int], [str], [{"a" : 1}], [FrozenDict({"a" : 1})],
            [1, [1.0]], [1, [int]], [1, [str]], [1, [{"a" : 1}]],
            [1, [FrozenDict({"a" : 1})]],
            ('a', [1, [1.0]]), ('a', [1, [int]]), ('a', [1, [str]]),
            ('a', [1, [{"a" : 1}]]), ('a', [1, [FrozenDict({"a" : 1})]])
        ]
        for GPath in lstCases:
            with self.assertRaises(TypeError):
                self.TestFunction(GPath)

class Test_GetData(unittest.TestCase):
    """
    Test cases for the function GetData() from the module universal_access.
    
    Implements tests ID TEST-T-510. Covers requirements REQ-FUN-501,
    REQ-FUN-510, REQ-AWM-500 and REQ-AWM-503.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.BadTypes = [[1], 1.0, ('a',), int, str, {'a' : 1}]
    
    #+helper method
    
    def TestFunction(self, gTarget, gPath):
        """
        Wraps the call of the function being actually tested.
        """
        return TestModule.GetData(gTarget, gPath)
    
    def setUp(self):
        """
        Preparations for the individual test-cases. Executed before each test.
        """
        self.List = [1, 2, 3]
        self.Tuple = (1, 2, 4)
        self.Dict = {'a' : 1, 'b' : 2, 'c' : 3}
        self.NamedTuple = NamedTuple(1, 2, 3)
        self.FrozenDict = FrozenDict({'a' : 1, 'b' : 2, 'c' : 3})
        self.Struct = SimpleStruct()
    
    def tearDown(self):
        """
        Cleaning-up. Executed after each individual test
        """
        del self.List
        self.List = None
        del self.Tuple
        self.Tuple = None
        del self.Dict
        self.Dict = None
        del self.NamedTuple
        self.NamedTuple = None
        del self.FrozenDict
        self.FrozenDict = None
        del self.Struct
        self.Struct = None
    
    def test_BadInput(self):
        """
        Checks that sub-class of TypeError is raised if the input is anything
        but integer or string.
        
        Implements tests ID TEST-T-510. Covers requirement REQ-AWM-500.
        """
        for gPath in self.BadTypes:
            with self.assertRaises(TypeError, msg = 'list type'):
                self.TestFunction(self.List, gPath)
            with self.assertRaises(TypeError, msg = 'tuple type'):
                self.TestFunction(self.Tuple, gPath)
            with self.assertRaises(TypeError, msg = 'named tuple type'):
                self.TestFunction(self.NamedTuple, gPath)
            with self.assertRaises(TypeError, msg = 'dict type'):
                self.TestFunction(self.Dict, gPath)
            with self.assertRaises(TypeError, msg = 'frozen dict type'):
                self.TestFunction(self.FrozenDict, gPath)
            with self.assertRaises(TypeError, msg = 'struct type'):
                self.TestFunction(self.Struct, gPath)
    
    def test_IndexAccess(self):
        """
        Checks that the exising elements of sequences can be accessed by an
        integer argument
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-501 and
        REQ-FUN-510.
        """
        for gTarget in [self.List, self.Tuple, self.NamedTuple]:
            iLen = len(gTarget)
            for iIndex in range(-iLen, iLen):
                self.assertEqual(self.TestFunction(gTarget, iIndex),
                                        gTarget[iIndex], msg = str(gTarget))
    
    def test_IndexAccessNonExisting(self):
        """
        Checks that the index argument outside the range results in IndexError
        sub-class exception.
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-501,
        REQ-FUN-510 and REQ-AMW-503.
        """
        for gTarget in [self.List, self.Tuple, self.NamedTuple]:
            iLen = len(gTarget)
            for iIndex in range(1, 5):
                with self.assertRaises(IndexError, msg = str(gTarget)):
                    self.TestFunction(gTarget, -iLen - iIndex)
                with self.assertRaises(IndexError, msg = str(gTarget)):
                    self.TestFunction(gTarget, iLen + iIndex - 1)
    
    def test_IndexAccessByString(self):
        """
        Checks that the string argument passed results in TypeError
        sub-class exception.
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-510,
        and REQ-AMW-500.
        """
        with self.assertRaises(TypeError, msg = 'list type'):
            self.TestFunction(self.List, 'a')
        with self.assertRaises(TypeError, msg = 'tuple type'):
            self.TestFunction(self.Tuple, 'a')
    
    def test_KeyAccess(self):
        """
        Checks that the exising entries of mappings can be accessed by a
        string argument
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-510.
        """
        for gTarget in [self.Dict, self.FrozenDict]:
            for strKey in ['a', 'b', 'c']:
                self.assertEqual(self.TestFunction(gTarget, strKey),
                                        gTarget[strKey], msg = str(gTarget))
    
    def test_KeyAccessNonExisting(self):
        """
        Checks that the non-exisiting mapping key access results in KeyError
        sub-class exception.
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-510 and
        REQ-AMW-503.
        """
        for gTarget in [self.Dict, self.FrozenDict]:
            for strKey in ['e', 'f', 'g']:
                with self.assertRaises(KeyError, msg = str(gTarget)):
                    self.TestFunction(gTarget, strKey)
    
    def test_KeyAccessByInteger(self):
        """
        Checks that the integer argument passed results in TypeError
        sub-class exception.
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-510,
        and REQ-AMW-500.
        """
        with self.assertRaises(TypeError, msg = 'dict type'):
            self.TestFunction(self.Dict, 1)
        with self.assertRaises(TypeError, msg = 'frozen dict type'):
            self.TestFunction(self.FrozenDict, 1)
    
    def test_AttributeAccess(self):
        """
        Checks that the exising attributes of objects can be accessed by a
        string argument
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-501 and
        REQ-FUN-510.
        """
        for gTarget in [self.Struct, self.NamedTuple]:
            self.assertEqual(self.TestFunction(gTarget, 'a'),
                                        gTarget.a, msg = str(gTarget))
            self.assertEqual(self.TestFunction(gTarget, 'b'),
                                        gTarget.b, msg = str(gTarget))
            self.assertEqual(self.TestFunction(gTarget, 'c'),
                                        gTarget.c, msg = str(gTarget))
    
    def test_AttributeAccessNonExisting(self):
        """
        Checks that the non-exisiting attribute access results in AttributeError
        sub-class exception.
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-501,
        REQ-FUN-510 and REQ-AMW-503.
        """
        for gTarget in [self.Struct, self.NamedTuple]:
            for strKey in ['e', 'f', 'g']:
                with self.assertRaises(AttributeError, msg = str(gTarget)):
                    self.TestFunction(gTarget, strKey)
    
    def test_AttributeAccessByInteger(self):
        """
        Checks that the integer argument passed results in TypeError
        sub-class exception.
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-510,
        and REQ-AMW-500.
        """
        with self.assertRaises(TypeError, msg = 'struct type'):
            self.TestFunction(self.Struct, 1)

class Test_GetDataDefault(Test_GetData):
    """
    Test cases for the function GetDataDefault() from the module
    universal_access.
    
    Implements tests ID TEST-T-520. Covers requirements REQ-FUN-501,
    REQ-FUN-520 and REQ-AWM-500.
    """
    
    #+helper method
    
    def TestFunction(self, gTarget, gPath):
        """
        Wraps the call of the function being actually tested.
        """
        return TestModule.GetDataDefault(gTarget, gPath, 6)
    
    def test_IndexAccessNonExisting(self):
        """
        Checks that the index argument outside the range results the default
        value being returned.
        
        Implements tests ID TEST-T-520. Covers requirements REQ-FUN-501,
        REQ-FUN-520.
        """
        for gTarget in [self.List, self.Tuple, self.NamedTuple]:
            iLen = len(gTarget)
            for iIndex in range(1, 5):
                self.assertEqual(self.TestFunction(gTarget, -iLen - iIndex),
                                                        6, msg = str(gTarget))
                self.assertEqual(self.TestFunction(gTarget, iLen + iIndex - 1),
                                                        6, msg = str(gTarget))
    
    def test_KeyAccessNonExisting(self):
        """
        Checks that the non-exisiting mapping key access results in the default
        value being returned.
        
        Implements tests ID TEST-T-520. Covers requirements REQ-FUN-501 and
        REQ-FUN-520.
        """
        for gTarget in [self.Dict, self.FrozenDict]:
            for strKey in ['e', 'f', 'g']:
                self.assertEqual(self.TestFunction(gTarget, strKey), 6,
                                                            msg = str(gTarget))
    
    def test_AttributeAccessNonExisting(self):
        """
        Checks that the non-exisiting attribute access results in the default
        value being returned.
        
        Implements tests ID TEST-T-520. Covers requirements REQ-FUN-501 and
        REQ-FUN-520.
        """
        for gTarget in [self.Struct, self.NamedTuple]:
            for strKey in ['e', 'f', 'g']:
                self.assertEqual(self.TestFunction(gTarget, strKey), 6,
                                                            msg = str(gTarget))

class Test_SetData(unittest.TestCase):
    """
    Test cases for the function SetData() from the module universal_access.
    
    Implements tests ID TEST-T-530. Covers requirements REQ-FUN-530,
    REQ-AWM-500 and REQ-AWM-502.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.BadTypes = [[1], 1.0, ('a',), int, str, {'a' : 1}]
    
    #+helper method
    
    def TestFunction(self, gTarget, gPath, gValue):
        """
        Wraps the call of the function being actually tested.
        """
        TestModule.SetData(gTarget, gPath, gValue)
    
    def setUp(self):
        """
        Preparations for the individual test-cases. Executed before each test.
        """
        self.List = [1, 2, 3]
        self.Tuple = (1, 2, 4)
        self.Dict = {'a' : 1, 'b' : 2, 'c' : 3}
        self.NamedTuple = NamedTuple(1, 2, 3)
        self.FrozenDict = FrozenDict({'a' : 1, 'b' : 2, 'c' : 3})
        self.Struct = SimpleStruct()
    
    def tearDown(self):
        """
        Cleaning-up. Executed after each individual test
        """
        del self.List
        self.List = None
        del self.Tuple
        self.Tuple = None
        del self.Dict
        self.Dict = None
        del self.NamedTuple
        self.NamedTuple = None
        del self.FrozenDict
        self.FrozenDict = None
        del self.Struct
        self.Struct = None
    
    def test_BadInput(self):
        """
        Checks that sub-class of TypeError is raised if the input is anything
        but integer or string.
        
        Implements tests ID TEST-T-530. Covers requirement REQ-AWM-500.
        """
        for gPath in self.BadTypes:
            with self.assertRaises(TypeError, msg = 'list type'):
                self.TestFunction(self.List, gPath)
            with self.assertRaises(TypeError, msg = 'tuple type'):
                self.TestFunction(self.Tuple, gPath)
            with self.assertRaises(TypeError, msg = 'named tuple type'):
                self.TestFunction(self.NamedTuple, gPath)
            with self.assertRaises(TypeError, msg = 'dict type'):
                self.TestFunction(self.Dict, gPath)
            with self.assertRaises(TypeError, msg = 'frozen dict type'):
                self.TestFunction(self.FrozenDict, gPath)
            with self.assertRaises(TypeError, msg = 'struct type'):
                self.TestFunction(self.Struct, gPath)
    
    def test_ModifyImmutable(self):
        """
        Checks that sub-class of **TypeError** is raised if the target object
        is immutable regardless of the (proper type) value of the path argument.
        
        Implements tests ID TEST-T-530. Covers requirement REQ-AWM-502.
        """
        for gTarget in [self.FrozenDict, self.NamedTuple]:
            for strName in ['a', 'b', 'c', 'd', 'e', 'f']:
                with self.assertRaises(TypeError, msg = '{} with {}'.format(
                                                            gTarget, strName)):
                    self.TestFunction(gTarget, strName, 9)
        for gTarget in [self.Tuple, self.NamedTuple]:
            iLen = len(gTarget)
            for iIndex in range(-2 * iLen, 2 * iLen):
                with self.assertRaises(TypeError, msg = '{} with {}'.format(
                                                            gTarget, strName)):
                    self.TestFunction(gTarget, strName, 9)
    
    def test_IndexAccess(self):
        """
        Checks that the exising elements of sequences can be accessed by an
        integer argument
        
        Implements tests ID TEST-T-530. Covers requirement REQ-FUN-530.
        """
        iLen = len(self.List)
        for iIndex in range(-iLen, iLen):
            iValue = random.randint(6, 15)
            self.TestFunction(self.List, iIndex, iValue)
            self.assertEqual(self.List[iIndex], iValue)
    
    def test_IndexAccessNonExisting(self):
        """
        Checks that the index argument outside the range results in the new
        element being added in front (for negative indexes) or after (for the
        positive index) existing elements - only for mutable sequences.
        
        Implements tests ID TEST-T-510. Covers requirements REQ-FUN-530.
        """
        iLen = len(self.List)
        for iIndex in range(1, 5):
            gTarget = list(self.List)#make a copy
            lstTest = [9]
            lstTest.extend(self.List)
            self.TestFunction(gTarget, -iLen - iIndex, 9)
            self.assertListEqual(gTarget, lstTest, msg = 'before')
            gTarget = list(self.List)#make a copy
            lstTest = list(self.List)
            lstTest.append(9)
            self.TestFunction(gTarget, iLen + iIndex - 1, 9)
            self.assertListEqual(gTarget, lstTest, msg = 'after')
    
    def test_IndexAccessByString(self):
        """
        Checks that the string argument passed results in TypeError
        sub-class exception.
        
        Implements tests ID TEST-T-530. Covers requirements REQ-FUN-530,
        and REQ-AMW-500.
        """
        with self.assertRaises(TypeError, msg = 'list type'):
            self.TestFunction(self.List, 'a', 9)
    
    def test_KeyAccess(self):
        """
        Checks that the exising entries of mappings can be accessed by a
        string argument
        
        Implements tests ID TEST-T-530. Covers requirements REQ-FUN-530.
        """
        for strKey in ['a', 'b', 'c']:
            self.TestFunction(self.Dict, strKey, 9)
            self.assertEqual(self.Dict[strKey], 9,
                                msg = '{} in dict'.format(strKey))
    
    def test_KeyAccessNonExisting(self):
        """
        Checks that the non-exisiting mapping key access results in a new key
        being added to a mutable mapping type.
        
        Implements tests ID TEST-T-530. Covers requirement REQ-FUN-530.
        """
        for strKey in ['e', 'f', 'g']:
            self.TestFunction(self.Dict, strKey, 9)
            self.assertEqual(self.Dict[strKey], 9,
                                msg = '{} in dict'.format(strKey))
    
    def test_KeyAccessByInteger(self):
        """
        Checks that the integer argument passed results in TypeError
        sub-class exception.
        
        Implements tests ID TEST-T-530. Covers requirements REQ-FUN-530,
        and REQ-AMW-500.
        """
        with self.assertRaises(TypeError, msg = 'dict type'):
            self.TestFunction(self.Dict, 1, 9)
    
    def test_AttributeAccess(self):
        """
        Checks that the exising attributes of objects can be accessed by a
        string argument
        
        Implements tests ID TEST-T-530. Covers requirement REQ-FUN-530.
        """
        self.TestFunction(self.Struct, 'a', 9)
        self.assertEqual(self.Struct.a, 9, msg = 'Struct.a')
        self.TestFunction(self.Struct, 'b', 10)
        self.assertEqual(self.Struct.b, 10, msg = 'Struct.b')
        self.TestFunction(self.Struct, 'c', 11)
        self.assertEqual(self.Struct.c, 11, msg = 'Struct.c')
    
    def test_AttributeAccessNonExisting(self):
        """
        Checks that the non-exisiting attribute access results in a new instance
        attribute created.
        
        Implements tests ID TEST-T-530. Covers requirement REQ-FUN-530.
        """
        self.TestFunction(self.Struct, 'd', 9)
        self.assertEqual(self.Struct.d, 9, msg = 'Struct.a')
        self.TestFunction(self.Struct, 'e', 10)
        self.assertEqual(self.Struct.e, 10, msg = 'Struct.b')
        self.TestFunction(self.Struct, 'f', 11)
        self.assertEqual(self.Struct.f, 11, msg = 'Struct.c')
    
    def test_AttributeAccessByInteger(self):
        """
        Checks that the integer argument passed results in TypeError
        sub-class exception.
        
        Implements tests ID TEST-T-530. Covers requirements REQ-FUN-530,
        and REQ-AMW-500.
        """
        with self.assertRaises(TypeError, msg = 'struct type'):
            self.TestFunction(self.Struct, 1, 9)

class Test_SetDataStrict(Test_SetData):
    """
    Test cases for the function SetDataStrict() from the module
    universal_access.
    
    Implements tests ID TEST-T-540. Covers requirements REQ-FUN-540,
    REQ-AWM-500, REQ-AWM-502 and REQ-AWM-503.
    """
    
    def TestFunction(self, gTarget, gPath, gValue):
        """
        Wraps the call of the function being actually tested.
        """
        TestModule.SetDataStrict(gTarget, gPath, gValue)
    
    def test_IndexAccessNonExisting(self):
        """
        Checks that the index argument outside the range results in IndexError
        sub-class exception.
        
        Implements tests ID TEST-T-540. Covers requirements REQ-FUN-540 and
        REQ-AMW-503.
        """
        iLen = len(self.List)
        for iIndex in range(1, 5):
            with self.assertRaises(IndexError, msg = 'too negative'):
                    self.TestFunction(self.List, -iLen - iIndex, 9)
            with self.assertRaises(IndexError, msg = 'too positive'):
                    self.TestFunction(self.List, iLen + iIndex - 1, 9)
    
    def test_KeyAccessNonExisting(self):
        """
        Checks that the non-exisiting mapping key access results in KeyError
        sub-class exception.
        
        Implements tests ID TEST-T-540. Covers requirements REQ-FUN-540 and
        REQ-AMW-503.
        """
        for strKey in ['e', 'f', 'g']:
            with self.assertRaises(KeyError, msg = '{} in dict'.format(strKey)):
                self.TestFunction(self.Dict, strKey, 9)
    
    def test_AttributeAccessNonExisting(self):
        """
        Checks that the non-exisiting attribute access results in AttributeError
        sub-class exception.
        
        Implements tests ID TEST-T-540. Covers requirements REQ-FUN-540 and
        REQ-AMW-503.
        """
        for strKey in ['e', 'f', 'g']:
            with self.assertRaises(AttributeError, msg = 'struct'):
                self.TestFunction(self.Struct, strKey, 9)

class Test_GetElement(unittest.TestCase):
    """
    Test cases for the function GetElement() from the module universal_access.
    
    Implements tests ID TEST-T-550. Covers requirements REQ-FUN-500,
    REQ-FUN-501, REQ-FUN-550, REQ-AWM-500, REQ-AWM-501 and REQ-AWM-503.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.BadTypes = [[1, 1.0], 1.0, ('a', 1.0), int, str, {'a' : 1}]
        cls.EmptyPaths = [[], tuple(), [[]], [[],[]], [[], [[]]]]
        cls.AttrMissingPaths = ['d', 'd.a', ['d'], ['d.a'], ['c', 'e', 2, 'd']]
        cls.IndexMissingPaths = [['b', 3], ['b', -4], ['c', 'b', 3],
                                    ['c', 'b', -4], ['c', 'd', 3],
                                    ['c', 'd', -4], ['c', 'e', 3],
                                    ['c', 'e', -4]]
        cls.KeyMissingPaths = ['c.f', ['c.f'], ['c', 'f'], 'c.c.c',
                                ['c', 'c.c'], ['c', 'c', 'c'], 'c.c.b.b',
                                ['c.c', 'b.b'], ['c', 'c', 'b', 'b']]
        cls.PathMissMatch = ['b.a', ['b', 'a'], ['c', 1], ['c', 'c', 1],
                                ['c', 'd', 'a'], ['c', 'e', 'a'],
                                ['c', 'e', 0, 'a'], ['c', 'e', 1, 1],
                                ['c', 'e', 2, 1]]
    
    #helper method
    
    def TestFunction(self, gTarget, gPath, **kwargs):
        return TestModule.GetElement(gTarget, gPath, **kwargs)
    
    def setUp(self):
        """
        Preparations for the individual test-cases. Executed before each test.
        """
        self.Data = ComplexStruct()
    
    def tearDown(self):
        """
        Cleaning-up. Executed after each individual test
        """
        del self.Data
        self.Data = None
    
    def test_EmptySequence(self):
        """
        Checks that ValueError sub-class exception is raised if a generic path
        reducible to an empty list (canonical form) is passed as an argument.
        
        Test ID: TEST-T-550. Covers requirements REQ-FUN-550 and REQ-AWM-501
        """
        for gPath in self.EmptyPaths:
            with self.assertRaises(ValueError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = True)
            with self.assertRaises(ValueError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = False)
            with self.assertRaises(ValueError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = False, gDefault=9)
            with self.assertRaises(ValueError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath)
    
    def test_BadInput(self):
        """
        Checks that TypeError sub-class exception is raised if a generic path
        is not of the proper type (regardless of the structure of the target).
        
        Test ID: TEST-T-550. Covers requirements REQ-FUN-550 and REQ-AWM-500.
        """
        for gPath in self.BadTypes:
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = True)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = False)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = False, gDefault=9)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath)
    
    def test_PathMismatch(self):
        """
        Checks that TypeError sub-class exception is raised if a generic path
        is of the proper type, but the path element type does not match the
        type of the object at the respective nesting level.
        
        Test ID: TEST-T-550. Covers requirements REQ-FUN-550 and REQ-AWM-500.
        """
        for gPath in self.PathMissMatch:
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = True)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = False)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, bStrict = False, gDefault=9)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath)
    
    def test_MissingPathStrict(self):
        """
        Checks that sub-class of IndexError, KeyError or AttributeError is
        raised with a missing element of the path - depending on the respective
        nesting level type.
        
        Test ID: TEST-T-550. Covers requirements REQ-FUN-550 and REQ-AWM-503.
        """
        #missing attribute
        for gPath in self.AttrMissingPaths:
            with self.assertRaises(AttributeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath)
            with self.assertRaises(AttributeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, gDefault = 9)
            with self.assertRaises(AttributeError):
                self.TestFunction(self.Data, gPath, bStrict = True)
            with self.assertRaises(AttributeError):
                self.TestFunction(self.Data, gPath, bStrict = True, gDefault= 9)
        #missing index
        for gPath in self.IndexMissingPaths:
            with self.assertRaises(IndexError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath)
            with self.assertRaises(IndexError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, gDefault = 9)
            with self.assertRaises(IndexError):
                self.TestFunction(self.Data, gPath, bStrict = True)
            with self.assertRaises(IndexError):
                self.TestFunction(self.Data, gPath, bStrict = True, gDefault= 9)
        #missing key
        for gPath in self.KeyMissingPaths:
            with self.assertRaises(KeyError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath)
            with self.assertRaises(KeyError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, gDefault = 9)
            with self.assertRaises(KeyError):
                self.TestFunction(self.Data, gPath, bStrict = True)
            with self.assertRaises(KeyError):
                self.TestFunction(self.Data, gPath, bStrict = True, gDefault= 9)
    
    def test_MissingPathRelaxed(self):
        """
        Checks that the passed default value is returned (or None if it is not
        provided) with a missing element of the path.
        
        Test ID: TEST-T-550. Covers requirement REQ-FUN-550.
        """
        for lstPaths in [self.AttrMissingPaths, self.IndexMissingPaths,
                                                        self.KeyMissingPaths]:
            for gPath in lstPaths:
                gResult = self.TestFunction(self.Data, gPath, bStrict = False)
                self.assertIsNone(gResult, msg = str(gPath))
                gResult = self.TestFunction(self.Data, gPath, bStrict = False,
                                                                gDefault = 9)
                self.assertEqual(gResult, 9, msg = str(gPath))
    
    def test_NormalOperation(self):
        """
        Checks that the existing nodes can be accessed using different notations
        of the generic 'nested' path definition in both strict and relaxed modes
        of operation.
        
        Test ID: TEST-T-550. Covers requirement REQ-FUN-550.
        """
        for DefVal in [None, 9]:
            for bMode in [True, False]:
                gResult = self.TestFunction(self.Data, 'a',
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.a)
                gResult = self.TestFunction(self.Data, ['b'],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertListEqual(gResult, self.Data.b)
                gResult = self.TestFunction(self.Data, ['b', 0],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.b[0])
                gResult = self.TestFunction(self.Data, 'c.a',
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['a'])
                gResult = self.TestFunction(self.Data, ['c.b', 0],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['b'][0])
                gResult = self.TestFunction(self.Data, ['c.b', 'a'],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['b'].a)
                gResult = self.TestFunction(self.Data, ['c', 'b', 'a'],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['b'].a)
                gResult = self.TestFunction(self.Data, 'c.b.a',
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['b'].a)
                gResult = self.TestFunction(self.Data, ['c', 'c.b', 'a'],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['c']['b']['a'])
                gResult = self.TestFunction(self.Data, ['c', 'd', 0],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['d'][0])
                gResult = self.TestFunction(self.Data, ['c.e', 0, 0],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['e'][0][0])
                gResult = self.TestFunction(self.Data, ['c.e', 1, 'a'],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['e'][1]['a'])
                gResult = self.TestFunction(self.Data, ['c', 'e', 2, 'a'],
                                            bStrict= bMode , gDefault= DefVal)
                self.assertEqual(gResult, self.Data.c['e'][2].a)

class Test_SetElement(unittest.TestCase):
    """
    Test cases for the function SetElement() from the module universal_access.
    
    Implements tests ID TEST-T-560. Covers requirements REQ-FUN-500,
    REQ-FUN-501, REQ-FUN-560, REQ-AWM-500, REQ-AWM-501, REQ-AWM-502 and
    REQ-AWM-503.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.BadTypes = [[1, 1.0], 1.0, ('a', 1.0), int, str, {'a' : 1}]
        cls.EmptyPaths = [[], tuple(), [[]], [[],[]], [[], [[]]]]
        cls.AttrMissingPaths = ['d', 'd.a', ['d'], ['d.a'], ['c', 'e', 2, 'd']]
        cls.IndexMissingPaths = [['b', 3], ['b', -4], ['c', 'e', 3],
                                    ['c', 'e', -4]]
        cls.KeyMissingPaths = ['c.f', ['c.f'], ['c', 'f'], ['c','e', 1, 'b']]
        cls.PathMissMatch = ['b.a', ['b', 'a'], ['c', 1], ['c', 'c', 1],
                                ['c', 'd', 'a'], ['c', 'e', 'a'],
                                ['c', 'e', 0, 'a'], ['c', 'e', 1, 1],
                                ['c', 'e', 2, 1]]
    
    #helper method
    
    def TestFunction(self, gTarget, gPath, gValue, **kwargs):
        return TestModule.SetElement(gTarget, gPath, gValue, **kwargs)
    
    def setUp(self):
        """
        Preparations for the individual test-cases. Executed before each test.
        """
        self.Data = ComplexStruct()
    
    def tearDown(self):
        """
        Cleaning-up. Executed after each individual test
        """
        del self.Data
        self.Data = None
    
    def test_EmptySequence(self):
        """
        Checks that ValueError sub-class exception is raised if a generic path
        reducible to an empty list (canonical form) is passed as an argument.
        
        Test ID: TEST-T-560. Covers requirements REQ-FUN-560 and REQ-AWM-501
        """
        for gPath in self.EmptyPaths:
            with self.assertRaises(ValueError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9, bStrict = True)
            with self.assertRaises(ValueError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9, bStrict = False)
            with self.assertRaises(ValueError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9)
    
    def test_BadInput(self):
        """
        Checks that TypeError sub-class exception is raised if a generic path
        is not of the proper type (regardless of the structure of the target).
        
        Test ID: TEST-T-560. Covers requirements REQ-FUN-560 and REQ-AWM-500.
        """
        for gPath in self.BadTypes:
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9, bStrict = True)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9, bStrict = False)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9)
    
    def test_PathMismatch(self):
        """
        Checks that TypeError sub-class exception is raised if a generic path
        is of the proper type, but the path element type does not match the
        type of the object at the respective nesting level.
        
        Test ID: TEST-T-550. Covers requirements REQ-FUN-550 and REQ-AWM-500.
        """
        for gPath in self.PathMissMatch:
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9, bStrict = True)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9, bStrict = False)
            with self.assertRaises(TypeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9)
    
    def test_MissingPathStrict(self):
        """
        Checks that sub-class of IndexError, KeyError or AttributeError is
        raised with a missing element of the path - depending on the respective
        nesting level type.
        
        Test ID: TEST-T-550. Covers requirements REQ-FUN-550 and REQ-AWM-503.
        """
        #missing attribute
        for gPath in self.AttrMissingPaths:
            with self.assertRaises(AttributeError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9)
            with self.assertRaises(AttributeError):
                self.TestFunction(self.Data, gPath, 9, bStrict = True)
        #missing index
        for gPath in self.IndexMissingPaths:
            with self.assertRaises(IndexError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9)
            with self.assertRaises(IndexError):
                self.TestFunction(self.Data, gPath, 9, bStrict = True)
        #missing key
        for gPath in self.KeyMissingPaths:
            with self.assertRaises(KeyError, msg = str(gPath)):
                self.TestFunction(self.Data, gPath, 9)
            with self.assertRaises(KeyError):
                self.TestFunction(self.Data, gPath, 9, bStrict = True)
    
    def test_MissingPathRelaxed(self):
        """
        Checks that the passed default value is returned (or None if it is not
        provided) with a missing element of the path.
        
        Test ID: TEST-T-550. Covers requirement REQ-FUN-550.
        """
       #missing end-nodes belonging to mutable non-sequences
        lstPaths = ['d', ['d'], ['c', 'f'], ['c.e', 1, 'b'], ['c', 'e', 2, 'd'],
                    ['c', 'c', 'b', 'd']]
        for gPath in lstPaths:
            iNumber = random.randint(6, 12)
            self.TestFunction(self.Data, gPath, iNumber, bStrict = False)
            self.assertEqual(TestModule.GetElement(self.Data, gPath), iNumber)
        #adding missing elements to mutable sequences
        for gPath in ['b', ['c', 'e', 0]]:
            iNumber = random.randint(6, 12)
            lstTest = [1, 2, 3, iNumber]
            self.TestFunction(self.Data, [gPath, 5], iNumber, bStrict = False)
            self.assertListEqual(TestModule.GetElement(self.Data, gPath),
                                                                        lstTest)
            iNumber = random.randint(6, 12)
            lstTest.insert(0, iNumber)
            self.TestFunction(self.Data, [gPath, -6], iNumber, bStrict = False)
            self.assertListEqual(TestModule.GetElement(self.Data, gPath),
                                                                        lstTest)
        #adding missing branches to mutable objects
        iNumber = random.randint(6, 12)
        gPath = ['e', 1, 1, 'a'] #dict in a list in a list as d attr of top lev.
        self.TestFunction(self.Data, gPath, iNumber, bStrict = False)
        self.assertEqual(self.Data.e[0][0]['a'], iNumber)
        gPath = ['c', 'e', 5, 'e', 1, 1, 'a'] #dict in a list in a list
        #appended as the last element to an exising list in a dict at top lev.
        self.TestFunction(self.Data, gPath, iNumber, bStrict = False)
        self.assertEqual(self.Data.c['e'][3]['e'][0][0]['a'], iNumber)
    
    def test_NormalOperation(self):
        """
        Checks that the existing nodes can be accessed using different notations
        of the generic 'nested' path definition in both strict and relaxed modes
        of operation.
        
        Test ID: TEST-T-550. Covers requirements REQ-FUN-500 and REQ-FUN-550.
        """
        for bMode in [True, False]:
            iNumber = random.randint(6, 12)
            self.TestFunction(self.Data, 'a', iNumber, bStrict = bMode)
            self.assertEqual(self.Data.a, iNumber)
            iNumber = random.randint(6, 12)
            self.TestFunction(self.Data, ['b', 0], iNumber, bStrict = bMode)
            self.assertEqual(self.Data.b[0], iNumber)
            iNumber = random.randint(6, 12)
            self.TestFunction(self.Data, 'c.a', iNumber, bStrict= bMode)
            self.assertEqual(self.Data.c['a'], iNumber)
            iNumber = random.randint(6, 12)
            self.TestFunction(self.Data, ['c.e', 0, 0], iNumber, bStrict= bMode)
            self.assertEqual(self.Data.c['e'][0][0], iNumber)
            iNumber = random.randint(6, 12)
            self.TestFunction(self.Data, ['c.e', 1, 'a'], iNumber,
                                                                bStrict = bMode)
            self.assertEqual(self.Data.c['e'][1]['a'], iNumber)
            iNumber = random.randint(6, 12)
            self.TestFunction(self.Data, ['c', 'e', 2, 'a'], iNumber,
                                                                bStrict= bMode)
            self.assertEqual(self.Data.c['e'][2].a, iNumber)
    
    def test_ImmutableNodes(self):
        """
        Checks that the existing nodes cannot be modified using different
        notations of the generic 'nested' path definition in both strict and
        relaxed modes of operation. Sub-class of TypeError must be raised.
        
        Test ID: TEST-T-550. Covers requirements REQ-FUN-500, REQ-FUN-550 and
        REQ-AWM-502.
        """
        for bMode in [True, False]:
            for gPath in ['c.b.a', ['c.b', 0], ['c.c.a'], ['c', 'c', 'b'],
                                                                    ['c.d', 0]]:
                with self.assertRaises(TypeError,
                                msg = '{} in strict {}'.format(gPath, bMode)):
                    self.TestFunction(self.Data, gPath, 9, bStrict = bMode)

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_FlattenPath)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_GetData)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_GetDataDefault)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_SetData)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_SetDataStrict)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_GetElement)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_SetElement)

TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6, TestSuite7])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting introspection_lib.universal_access module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)