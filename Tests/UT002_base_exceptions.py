#usr/bin/python3
"""
Module introspection_lib.Tests.UT002_base_exceptions

Implements unit testing of the module introspection_lib.base_exceptions.
"""

__version__ = "1.0.1.0"
__date__ = "06-11-2020"
__status__ = "Testing"

#imports

#+ standard libraries

import sys
import os
import unittest
import types

#+ my libraries

ROOT_FOLDER = os.path.dirname(os.path.dirname(
                                os.path.dirname(os.path.realpath(__file__))))

if not (ROOT_FOLDER) in sys.path:
    sys.path.append(ROOT_FOLDER)

import introspection_lib.base_exceptions as testmodule

from introspection_lib.traceback import ExceptionTraceback

#helper functions

def inner(clsError, *args, SkipFrames = None, FromTraceback = None):
    """
    The inner function in the chain outer() -> middle() -> inner(), which,
    actually, raises the required exception.
    """
    raise clsError(*args, SkipFrames= SkipFrames, FromTraceback= FromTraceback)

def middle(clsError, *args, SkipFrames = None, FromTraceback = None):
    """
    The middle function in the chain outer() -> middle() -> inner(), which leads
    to the required exception.
    """
    return inner(clsError, *args, SkipFrames = SkipFrames,
                                    FromTraceback = FromTraceback)

def outer(clsError, *args, SkipFrames = None, FromTraceback = None):
    """
    The outer function in the chain outer() -> middle() -> inner(), which leads
    to the required exception.
    """
    return middle(clsError, *args, SkipFrames = SkipFrames,
                                    FromTraceback = FromTraceback)

#helper classes

class S_Exception(testmodule.UT_Exception):
    """
    Helper class - just sub-classes UT_Exception w/o any other changes.
    """
    pass

class S_TypeError(testmodule.UT_TypeError):
    """
    Helper class - just sub-classes UT_TypeError w/o any other changes.
    """
    pass

class S_ValueError(testmodule.UT_ValueError):
    """
    Helper class - just sub-classes UT_ValueError w/o any other changes.
    """
    pass

class S_AttributeError(testmodule.UT_AttributeError):
    """
    Helper class - just sub-classes UT_AttributeError w/o any other changes.
    """
    pass

class S_IndexError(testmodule.UT_IndexError):
    """
    Helper class - just sub-classes UT_IndexError w/o any other changes.
    """
    pass

class S_KeyError(testmodule.UT_KeyError):
    """
    Helper class - just sub-classes UT_KeyError w/o any other changes.
    """
    pass

#test case classes

class Test_UT_Exception(unittest.TestCase):
    """
    Test cases for the class introspection_lib.base_exceptions.UT_Exception.
    
    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-210. Covers
    the requirements REQ-FUN-200, REQ-FUN-201, REQ-FUN-202 and REQ-FUN-210.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.UT_Exception
        cls.ChildOf = [Exception, BaseException]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError,
                            ValueError, testmodule.UT_ValueError,
                            AttributeError, testmodule.UT_AttributeError,
                            IndexError, testmodule.UT_IndexError,
                            KeyError, testmodule.UT_KeyError]
        cls.ParentOf = [testmodule.UT_TypeError, testmodule.UT_ValueError,
                        testmodule.UT_AttributeError, testmodule.UT_IndexError,
                        testmodule.UT_KeyError, S_Exception, S_TypeError,
                        S_ValueError, S_AttributeError, S_IndexError,
                        S_KeyError]
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError]
        cls.DefArguments = ['test']
    
    def test_IsChild(self):
        """
        Checks if the test class is actual or virtual sub-class of specific
        exception classes.

        Test ID: TEST-T-200. Covers the requirement REQ-FUN-200.
        """
        for clsException in self.ChildOf:
            self.assertTrue(issubclass(self.TestClass, clsException),
                msg = '{} is not subclass of {}'.format(self.TestClass.__name__,
                                                        clsException.__name__))
    
    def test_IsNotChild(self):
        """
        Checks if the test class is neither actual nor virtual sub-class of
        specific exception classes.

        Test ID: TEST-T-200. Covers the requirement REQ-FUN-200.
        """
        for clsException in self.NotChildOf:
            self.assertFalse(issubclass(self.TestClass, clsException),
                    msg = '{} is subclass of {}'.format(self.TestClass.__name__,
                                                        clsException.__name__))
    
    def test_IsParent(self):
        """
        Checks if the test class is actual or virtual super class for specific
        exception classes.

        Test ID: TEST-T-200. Covers the requirement REQ-FUN-200.
        """
        for clsException in self.ParentOf:
            self.assertTrue(issubclass(clsException, self.TestClass),
                msg = '{} is not super class for {}'.format(
                                                        self.TestClass.__name__,
                                                        clsException.__name__))
    
    def test_IsNotParent(self):
        """
        Checks if the test class is neither actual nor virtual super class for
        specific exception classes.

        Test ID: TEST-T-200. Covers the requirement REQ-FUN-200.
        """
        for clsException in self.NotParentOf:
            self.assertFalse(issubclass(clsException, self.TestClass),
                msg = '{} is super class for {}'.format(self.TestClass.__name__,
                                                        clsException.__name__))
    
    def test_Attributes(self):
        """
        Check the presence and type of all required attributes, except the
        method with_traceback(), which is only checked for presence.

        Test ID: TEST-T-201. Covers the requirement REQ-FUN-201.
        """
        try:
            raise self.TestClass(*self.DefArguments)
        except self.TestClass as err:
            self.assertTrue(hasattr(err, 'args'), msg = 'No args attribute')
            self.assertTrue(isinstance(err.args, tuple),
                            msg = 'args attribute is not a tuple')
            self.assertEqual(len(err.args), 1, msg = 'length of args tuple')
            self.assertTrue(isinstance(err.args[0], str),
                            msg = 'args[0] is not a string')
            self.assertTrue(hasattr(err, '__traceback__'),
                            msg = 'No __traceback__ attribute')
            self.assertTrue(isinstance(err.__traceback__, types.TracebackType),
                            msg = '__traceback__ is not a traceback instance')
            self.assertTrue(hasattr(err, 'with_traceback'),
                            msg = 'No with_traceback attribute')
            self.assertTrue(hasattr(err, 'Traceback'),
                            msg = 'No Traceback attribute')
            self.assertTrue(hasattr(err.Traceback, 'Info'),
                            msg = 'Traceback has no Info attribute')
            self.assertIsInstance(err.Traceback.Info, str,
                            msg = 'Traceback.Info is not a string')
            self.assertTrue(hasattr(err.Traceback, 'CallChain'),
                            msg = 'Traceback has no CallChain attribute')
            self.assertIsInstance(err.Traceback.CallChain, list,
                            msg = 'Traceback.CallCain is not a list')
            self.assertTrue(all(map(lambda x: isinstance(x, str), 
                                            err.Traceback.CallChain)),
                            msg = 'Traceback.CallCain is not a list')
    
    def test_RaiseSimple(self):
        """
        Checks that both Traceback and __traceback__ refer to the same actual
        traceback of the exception if a simple instantation is used.

        Test ID: TEST-T-202. Covers requirement: REQ-FUN-202.
        """
        try:
            outer(self.TestClass, *self.DefArguments)
        except self.TestClass as err:
            strInfo = err.Traceback.Info
            lstCallChain = err.Traceback.CallChain
            objDirect = ExceptionTraceback()
            objFromTB = ExceptionTraceback(FromTraceback = err.__traceback__)
        #must contain exactly 4 elements
        self.assertEqual(len(lstCallChain), 4,
                'traceback size must be 4 not {}'.format(len(lstCallChain)))
        #must start always in this method
        self.assertEqual(lstCallChain[0],
            '{}.{}.test_RaiseSimple'.format(__name__, self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        # second element must point to the outer() function
        self.assertEqual(lstCallChain[1],
                '{}.outer'.format(__name__),
                    'second element - {} not "{}.outer"'.format(
                                                    lstCallChain[1], __name__))
        # third element must point to the middle() function
        self.assertEqual(lstCallChain[2],
                '{}.middle'.format(__name__),
                    'third element - {} not "{}.middle"'.format(
                                                    lstCallChain[2], __name__))
        # last element must point to the inner() function
        self.assertEqual(lstCallChain[3],
                '{}.inner'.format(__name__),
                    'forth element - {} not "{}.inner"'.format(
                                                    lstCallChain[3], __name__))
        #compare 3 traceback versions
        self.assertEqual(strInfo, objDirect.Info,
                                msg = 'Info of built-in and direct tracebacks')
        self.assertEqual(objDirect.Info, objFromTB.Info,
                            msg = 'Info of __traceback__ and direct tracebacks')
        self.assertEqual(lstCallChain, objDirect.CallChain,
                    msg = 'CallChain of built-in and direct tracebacks')
        self.assertEqual(objDirect.CallChain, objFromTB.CallChain,
                    msg = 'CallChain of __traceback__ and direct tracebacks')
        del objDirect
        del objFromTB
        #short chain
        try:
            raise self.TestClass(*self.DefArguments)
        except self.TestClass as err:
            strInfo = err.Traceback.Info
            lstCallChain = err.Traceback.CallChain
            objDirect = ExceptionTraceback()
            objFromTB = ExceptionTraceback(FromTraceback = err.__traceback__)
        #must contain exactly 1 element
        self.assertEqual(len(lstCallChain), 1,
                'traceback size must be 1 not {}'.format(len(lstCallChain)))
        #must start always in this method
        self.assertEqual(lstCallChain[0],
            '{}.{}.test_RaiseSimple'.format(__name__, self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        #compare 3 traceback versions
        self.assertEqual(strInfo, objDirect.Info,
                                msg = 'Info of built-in and direct tracebacks')
        self.assertEqual(objDirect.Info, objFromTB.Info,
                            msg = 'Info of __traceback__ and direct tracebacks')
        self.assertEqual(lstCallChain, objDirect.CallChain,
                    msg = 'CallChain of built-in and direct tracebacks')
        self.assertEqual(objDirect.CallChain, objFromTB.CallChain,
                    msg = 'CallChain of __traceback__ and direct tracebacks')
        del objDirect
        del objFromTB
    
    def test_RaiseTruncated(self):
        """
        Checks that the __traceback__ refers to the actual traceback, whereas
        Traceback - to the truncated version of the same traceback of the
        exception if the instantation with truncation is used.

        Test ID: TEST-T-202. Covers requirement: REQ-FUN-202.
        """
        try:
            outer(self.TestClass, *self.DefArguments, SkipFrames = 2)
        except self.TestClass as err:
            lstCallChain = err.Traceback.CallChain
            strInfo = err.Traceback.Info
            objDirect = ExceptionTraceback()
            objFromTB = ExceptionTraceback(FromTraceback = err.__traceback__)
        #must contain exactly 2 elements
        self.assertEqual(len(lstCallChain), 2,
                'traceback size must be 2 not {}'.format(len(lstCallChain)))
        #must start always in this method
        self.assertEqual(lstCallChain[0],
            '{}.{}.test_RaiseTruncated'.format(__name__,
                                                    self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        # second element must point to the outer() function
        self.assertEqual(lstCallChain[1],
                '{}.outer'.format(__name__),
                    'second element - {} not "{}.outer"'.format(
                                                    lstCallChain[1], __name__))
        #compare 3 traceback versions
        self.assertTrue(objDirect.Info.startswith(strInfo),
                    msg = 'Info of built-in and direct tracebacks - inclusion')
        self.assertEqual(objDirect.Info, objFromTB.Info,
                    msg = 'Info of __traceback__ and direct tracebacks')
        self.assertEqual(lstCallChain, objDirect.CallChain[:2],
                msg = 'CallChain of built-in and direct tracebacks - inclusion')
        self.assertEqual(objDirect.CallChain, objFromTB.CallChain,
                    msg = 'CallChain of __traceback__ and direct tracebacks')
        del objDirect
        del objFromTB

    def test_RaiseSubstituted(self):
        """
        Checks that the __traceback__ refers to the actual traceback, whereas
        Traceback - to the substitution traceback of another exception if the
        instantation with substitution is used.

        Test ID: TEST-T-202. Covers requirement: REQ-FUN-202.
        """
        try:
            outer(self.TestClass, *self.DefArguments)
        except self.TestClass as err:
            try:
                raise self.TestClass(*self.DefArguments,
                                            FromTraceback = err.__traceback__)
            except self.TestClass as err2:
                strInfo = err2.Traceback.Info
                lstCallChain = err2.Traceback.CallChain
                objDirect = ExceptionTraceback()
                objFromTB = ExceptionTraceback(
                                            FromTraceback = err2.__traceback__)
        #must contain exactly 4 elements
        self.assertEqual(len(lstCallChain), 4,
                'traceback size must be 4 not {}'.format(len(lstCallChain)))
        #must start always in this method
        self.assertEqual(lstCallChain[0],
            '{}.{}.test_RaiseSubstituted'.format(__name__,
                                                    self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        # second element must point to the outer() function
        self.assertEqual(lstCallChain[1],
                '{}.outer'.format(__name__),
                    'second element - {} not "{}.outer"'.format(
                                                    lstCallChain[1], __name__))
        # third element must point to the middle() function
        self.assertEqual(lstCallChain[2],
                '{}.middle'.format(__name__),
                    'third element - {} not "{}.middle"'.format(
                                                    lstCallChain[2], __name__))
        # last element must point to the inner() function
        self.assertEqual(lstCallChain[3],
                '{}.inner'.format(__name__),
                    'forth element - {} not "{}.inner"'.format(
                                                    lstCallChain[3], __name__))
        #compare 3 traceback versions
        self.assertEqual(len(objDirect.CallChain), 1,
            'Direct traceback size must be 1 not {}'.format(len(lstCallChain)))
        self.assertEqual(objDirect.CallChain, objFromTB.CallChain,
                    msg = 'CallChain of __traceback__ and direct tracebacks')
        self.assertEqual(objDirect.Info, objFromTB.Info,
                            msg = 'Info of __traceback__ and direct tracebacks')
        del objDirect
        del objFromTB
    
    def test_RaiseChained(self):
        """
        Checks that both the __traceback__ attribute and the Traceback property
        refer to the actual traceback, extended with another extension's
        traceback, if the explicit chaining (with_traceback() method call) is
        used regardless of the mode of instantiation.

        Test ID: TEST-T-202. Covers requirement: REQ-FUN-202.
        """
        #simple instantiation
        try:
            outer(self.TestClass, *self.DefArguments)
        except self.TestClass as err:
            try:
                raise self.TestClass(*self.DefArguments).with_traceback(
                                                            err.__traceback__)
            except self.TestClass as err2:
                strInfo = err2.Traceback.Info
                lstCallChain = err2.Traceback.CallChain
                objFromTB = ExceptionTraceback(
                                            FromTraceback = err2.__traceback__)
        #must contain exactly 5 elements
        self.assertEqual(len(lstCallChain), 5,
                'traceback size must be 5 not {}'.format(len(lstCallChain)))
        #must start always in this method
        self.assertEqual(lstCallChain[0],
            '{}.{}.test_RaiseChained'.format(__name__,
                                                    self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        #must start always in this method
        self.assertEqual(lstCallChain[1],
            '{}.{}.test_RaiseChained'.format(__name__,
                                                    self.__class__.__name__),
                    'second element - {} not this method'.format(
                                                            lstCallChain[1]))
        # third element must point to the outer() function
        self.assertEqual(lstCallChain[2],
                '{}.outer'.format(__name__),
                    'third element - {} not "{}.outer"'.format(
                                                    lstCallChain[2], __name__))
        # fourth element must point to the middle() function
        self.assertEqual(lstCallChain[3],
                '{}.middle'.format(__name__),
                    'fourth element - {} not "{}.middle"'.format(
                                                    lstCallChain[3], __name__))
        # last element must point to the inner() function
        self.assertEqual(lstCallChain[4],
                '{}.inner'.format(__name__),
                    'fifth element - {} not "{}.inner"'.format(
                                                    lstCallChain[4], __name__))
        #compare 2 traceback versions
        self.assertEqual(strInfo, objFromTB.Info,
                        msg = 'Info of built-in and __traceback__ tracebacks')
        self.assertEqual(lstCallChain, objFromTB.CallChain,
                    msg = 'CallChain of built-in and __traceback__ tracebacks')
        del objFromTB
        #substitution instantiation
        try:
            outer(self.TestClass, *self.DefArguments)
        except self.TestClass as err:
            try:
                raise self.TestClass(*self.DefArguments,
                            FromTraceback = err.__traceback__).with_traceback(
                                                            err.__traceback__)
            except self.TestClass as err2:
                strInfo = err2.Traceback.Info
                lstCallChain = err2.Traceback.CallChain
                objFromTB = ExceptionTraceback(
                                            FromTraceback = err2.__traceback__)
        #must contain exactly 5 elements
        self.assertEqual(len(lstCallChain), 5,
                'traceback size must be 5 not {}'.format(len(lstCallChain)))
        #must start always in this method
        self.assertEqual(lstCallChain[0],
            '{}.{}.test_RaiseChained'.format(__name__,
                                                    self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        #must start always in this method
        self.assertEqual(lstCallChain[1],
            '{}.{}.test_RaiseChained'.format(__name__,
                                                    self.__class__.__name__),
                    'second element - {} not this method'.format(
                                                            lstCallChain[1]))
        # third element must point to the outer() function
        self.assertEqual(lstCallChain[2],
                '{}.outer'.format(__name__),
                    'third element - {} not "{}.outer"'.format(
                                                    lstCallChain[2], __name__))
        # fourth element must point to the middle() function
        self.assertEqual(lstCallChain[3],
                '{}.middle'.format(__name__),
                    'fourth element - {} not "{}.middle"'.format(
                                                    lstCallChain[3], __name__))
        # last element must point to the inner() function
        self.assertEqual(lstCallChain[4],
                '{}.inner'.format(__name__),
                    'fifth element - {} not "{}.inner"'.format(
                                                    lstCallChain[4], __name__))
        #compare 2 traceback versions
        self.assertEqual(strInfo, objFromTB.Info,
                        msg = 'Info of built-in and __traceback__ tracebacks')
        self.assertEqual(lstCallChain, objFromTB.CallChain,
                    msg = 'CallChain of built-in and __traceback__ tracebacks')
        del objFromTB
        #truncation instantiation
        try:
            outer(self.TestClass, *self.DefArguments)
        except self.TestClass as err:
            try:
                raise self.TestClass(*self.DefArguments,
                            SkipFrames = 2).with_traceback(err.__traceback__)
            except self.TestClass as err2:
                strInfo = err2.Traceback.Info
                lstCallChain = err2.Traceback.CallChain
                objFromTB = ExceptionTraceback(
                                            FromTraceback = err2.__traceback__)
        #must contain exactly 5 elements
        self.assertEqual(len(lstCallChain), 5,
                'traceback size must be 5 not {}'.format(len(lstCallChain)))
        #must start always in this method
        self.assertEqual(lstCallChain[0],
            '{}.{}.test_RaiseChained'.format(__name__,
                                                    self.__class__.__name__),
                    'top of the traceback - {} not this method'.format(
                                                            lstCallChain[0]))
        #must start always in this method
        self.assertEqual(lstCallChain[1],
            '{}.{}.test_RaiseChained'.format(__name__,
                                                    self.__class__.__name__),
                    'second element - {} not this method'.format(
                                                            lstCallChain[1]))
        # third element must point to the outer() function
        self.assertEqual(lstCallChain[2],
                '{}.outer'.format(__name__),
                    'third element - {} not "{}.outer"'.format(
                                                    lstCallChain[2], __name__))
        # fourth element must point to the middle() function
        self.assertEqual(lstCallChain[3],
                '{}.middle'.format(__name__),
                    'fourth element - {} not "{}.middle"'.format(
                                                    lstCallChain[3], __name__))
        # last element must point to the inner() function
        self.assertEqual(lstCallChain[4],
                '{}.inner'.format(__name__),
                    'fifth element - {} not "{}.inner"'.format(
                                                    lstCallChain[4], __name__))
        #compare 2 traceback versions
        self.assertEqual(strInfo, objFromTB.Info,
                        msg = 'Info of built-in and __traceback__ tracebacks')
        self.assertEqual(lstCallChain, objFromTB.CallChain,
                    msg = 'CallChain of built-in and __traceback__ tracebacks')
        del objFromTB
    
    def test_ArgsContent(self):
        """
        Checks that the args attribute is always a single string element tuple,
        and this string (error message) is formed properly regardless of the
        manner of the exception's instantiation.

        Test ID: TEST-T-210. Covers the requirement: REQ-FUN-210.
        """
        objError = self.TestClass('test')
        self.assertEqual(objError.args, ('test',),
                            msg = 'simple instantiation')
        del objError
        try:
            raise self.TestClass('test1', SkipFrames = 1)
        except self.TestClass as err:
            self.assertEqual(err.args, ('test1',),
                            msg = 'truncated instantiation')
            tbTemp = err.__traceback__
        objError = self.TestClass('test2', FromTraceback = tbTemp)
        self.assertEqual(objError.args, ('test2',),
                            msg = 'substitution instantiation')
        del objError
        objError = self.TestClass('test3').with_traceback(tbTemp)
        self.assertEqual(objError.args, ('test3',),
                            msg = 'simple instantiation -> chained')
        del objError
        objError = self.TestClass('test4',
                                    SkipFrames = 1).with_traceback(tbTemp)
        self.assertEqual(objError.args, ('test4',),
                            msg = 'truncated instantiation -> chained')

        del objError
        objError = self.TestClass('test5',
                                FromTraceback = tbTemp).with_traceback(tbTemp)
        self.assertEqual(objError.args, ('test5',),
                            msg = 'substitution instantiation -> chained')
        del objError
        del tbTemp
    
    def test_InitArguments(self):
        """
        Checks that initialization method accepts only the defined number of 
        the positional arguments.

        Test ID: TEST-T-210, TEST-T-220. TEST-T-230, TEST-T-240, TEST-T-250 and
        TEST-T-260. Covers the requirement: REQ-FUN-210, REQ-FUN-220,
        REQ-FUN-230, REQ-FUN-240, REQ-FUN-250 and REQ-FUN-260.
        """
        #too little arguments
        if len(self.DefArguments) == 1:
            with self.assertRaises(TypeError):
                self.TestClass()
        else:
            lstTemp = self.DefArguments[:-1]
            with self.assertRaises(TypeError):
                self.TestClass(*lstTemp)
            del lstTemp
        #too many arguments
        lstTemp = list(self.DefArguments)
        lstTemp.append(1)
        with self.assertRaises(TypeError):
            self.TestClass(*lstTemp)
        del lstTemp

class Test_Sub_Exception(Test_UT_Exception):
    """
    Test cases for the sub-class of
    introspection_lib.base_exceptions.UT_Exception.
    
    Implements tests: TEST-T-203. Covers the requirement REQ-FUN-204.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = S_Exception
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError,
                            S_TypeError,
                            ValueError, testmodule.UT_ValueError,
                            S_ValueError,
                            AttributeError, testmodule.UT_AttributeError,
                            S_AttributeError,
                            IndexError, testmodule.UT_IndexError,
                            S_IndexError,
                            KeyError, testmodule.UT_KeyError, S_KeyError]
        cls.ParentOf = []
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError,
                            S_TypeError, S_AttributeError, S_IndexError,
                            S_ValueError, S_KeyError]
        cls.DefArguments = ['test']
    

class Test_UT_TypeError(Test_UT_Exception):
    """
    Test cases for the class introspection_lib.base_exceptions.UT_TypeError.
    
    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-220. Covers
    the requirements REQ-FUN-200, REQ-FUN-201, REQ-FUN-202 and REQ-FUN-220.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.UT_TypeError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        TypeError]
        cls.NotChildOf = [ValueError, testmodule.UT_ValueError,
                            AttributeError, testmodule.UT_AttributeError,
                            IndexError, testmodule.UT_IndexError,
                            KeyError, testmodule.UT_KeyError,
                            S_Exception]
        cls.ParentOf = [S_TypeError]
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError, S_Exception,
                            S_ValueError, S_AttributeError, S_IndexError,
                            S_KeyError]
        cls.DefArguments = ['test', int]
    
    def test_ArgsContent(self):
        """
        Checks that the args attribute is always a single string element tuple,
        and this string (error message) is formed properly regardless of the
        manner of the exception's instantiation.

        Test ID: TEST-T-220. Covers the requirement: REQ-FUN-220.
        """
        tupError = ('S_Exception is not a sub-class of (int, )', )
        objError = self.TestClass(S_Exception, int)
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation')
        del objError
        try:
            raise self.TestClass(S_Exception, (int, ), SkipFrames = 1)
        except self.TestClass as err:
            self.assertEqual(err.args, tupError,
                            msg = 'truncated instantiation')
            tbTemp = err.__traceback__
        objError = self.TestClass(S_Exception, [int], FromTraceback = tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation')
        del objError
        objError = self.TestClass(S_Exception, int).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation -> chained')
        del objError
        objError = self.TestClass(S_Exception, (int, ),
                                    SkipFrames = 1).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'truncated instantiation -> chained')

        del objError
        objError = self.TestClass(S_Exception, [int],
                                FromTraceback = tbTemp).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation -> chained')
        del objError
        del tbTemp

class Test_UT_ValueError(Test_UT_Exception):
    """
    Test cases for the class introspection_lib.base_exceptions.UT_ValueError.
    
    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-230. Covers
    the requirements REQ-FUN-200, REQ-FUN-201, REQ-FUN-202 and REQ-FUN-230.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.UT_ValueError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        ValueError]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError,
                            AttributeError, testmodule.UT_AttributeError,
                            IndexError, testmodule.UT_IndexError,
                            KeyError, testmodule.UT_KeyError,
                            S_Exception]
        cls.ParentOf = [S_ValueError]
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError, S_Exception,
                            S_TypeError, S_AttributeError, S_IndexError,
                            S_KeyError]
        cls.DefArguments = ['test', 'whatever']
    
    def test_ArgsContent(self):
        """
        Checks that the args attribute is always a single string element tuple,
        and this string (error message) is formed properly regardless of the
        manner of the exception's instantiation.

        Test ID: TEST-T-230. Covers the requirement: REQ-FUN-230.
        """
        tupError = ('1 does not meet restriction < 0', )
        objError = self.TestClass(1, '< 0')
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation')
        del objError
        try:
            raise self.TestClass(1, '< 0', SkipFrames = 1)
        except self.TestClass as err:
            self.assertEqual(err.args, tupError,
                            msg = 'truncated instantiation')
            tbTemp = err.__traceback__
        objError = self.TestClass(1, '< 0', FromTraceback = tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation')
        del objError
        objError = self.TestClass(1, '< 0').with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation -> chained')
        del objError
        objError = self.TestClass(1, '< 0',
                                    SkipFrames = 1).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'truncated instantiation -> chained')

        del objError
        objError = self.TestClass(1, '< 0',
                                FromTraceback = tbTemp).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation -> chained')
        del objError
        del tbTemp

class Test_UT_AttributeError(Test_UT_Exception):
    """
    Test cases for the class introspection_lib.base_exceptions.UT_AttributeError
    
    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-240. Covers
    the requirements REQ-FUN-200, REQ-FUN-201, REQ-FUN-202 and REQ-FUN-240.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.UT_AttributeError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        AttributeError]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError,
                            ValueError, testmodule.UT_ValueError,
                            IndexError, testmodule.UT_IndexError,
                            KeyError, testmodule.UT_KeyError,
                            S_Exception]
        cls.ParentOf = [S_AttributeError]
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError, S_Exception,
                            S_TypeError, S_ValueError, S_IndexError,
                            S_KeyError]
        cls.DefArguments = ['test', 'whatever']
    
    def test_ArgsContent(self):
        """
        Checks that the args attribute is always a single string element tuple,
        and this string (error message) is formed properly regardless of the
        manner of the exception's instantiation.

        Test ID: TEST-T-240. Covers the requirement: REQ-FUN-240.
        """
        tupError = ('S_Exception.test', )
        objError = self.TestClass(S_Exception, 'test')
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation')
        del objError
        try:
            raise self.TestClass(S_Exception, 'test', SkipFrames = 1)
        except self.TestClass as err:
            self.assertEqual(err.args, tupError,
                            msg = 'truncated instantiation')
            tbTemp = err.__traceback__
        objError = self.TestClass(S_Exception, 'test', FromTraceback = tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation')
        del objError
        objError = self.TestClass(S_Exception, 'test').with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation -> chained')
        del objError
        objError = self.TestClass(S_Exception, 'test',
                                    SkipFrames = 1).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'truncated instantiation -> chained')

        del objError
        objError = self.TestClass(S_Exception, 'test',
                                FromTraceback = tbTemp).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation -> chained')
        del objError
        del tbTemp

class Test_UT_IndexError(Test_UT_Exception):
    """
    Test cases for the class introspection_lib.base_exceptions.UT_IndexError.
    
    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-250. Covers
    the requirements REQ-FUN-200, REQ-FUN-201, REQ-FUN-202 and REQ-FUN-250.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.UT_IndexError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        IndexError]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError,
                            ValueError, testmodule.UT_ValueError,
                            AttributeError, testmodule.UT_AttributeError,
                            KeyError, testmodule.UT_KeyError,
                            S_Exception]
        cls.ParentOf = [S_IndexError]
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_KeyError, S_Exception,
                            S_TypeError, S_AttributeError, S_ValueError,
                            S_KeyError]
        cls.DefArguments = ['test', 1]
    
    def test_ArgsContent(self):
        """
        Checks that the args attribute is always a single string element tuple,
        and this string (error message) is formed properly regardless of the
        manner of the exception's instantiation.

        Test ID: TEST-T-250. Covers the requirement: REQ-FUN-250.
        """
        tupError = ('Out of range index S_Exception[1]', )
        objError = self.TestClass('S_Exception', 1)
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation')
        del objError
        try:
            raise self.TestClass('S_Exception', 1, SkipFrames = 1)
        except self.TestClass as err:
            self.assertEqual(err.args, tupError,
                            msg = 'truncated instantiation')
            tbTemp = err.__traceback__
        objError = self.TestClass('S_Exception', 1, FromTraceback = tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation')
        del objError
        objError = self.TestClass('S_Exception', 1).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation -> chained')
        del objError
        objError = self.TestClass('S_Exception', 1,
                                    SkipFrames = 1).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'truncated instantiation -> chained')

        del objError
        objError = self.TestClass('S_Exception', 1,
                                FromTraceback = tbTemp).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation -> chained')
        del objError
        del tbTemp

class Test_UT_KeyError(Test_UT_Exception):
    """
    Test cases for the class introspection_lib.base_exceptions.UT_KeyError.
    
    Implements tests: TEST-T-200, TEST-T-201, TEST-T-202 and TEST-T-260. Covers
    the requirements REQ-FUN-200, REQ-FUN-201, REQ-FUN-202 and REQ-FUN-260.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = testmodule.UT_KeyError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        KeyError]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError,
                            ValueError, testmodule.UT_ValueError,
                            AttributeError, testmodule.UT_AttributeError,
                            IndexError, testmodule.UT_IndexError,
                            S_Exception]
        cls.ParentOf = [S_KeyError]
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            S_Exception,
                            S_TypeError, S_AttributeError, S_IndexError,
                            S_ValueError]
        cls.DefArguments = ['test', 'whatever']
    
    def test_ArgsContent(self):
        """
        Checks that the args attribute is always a single string element tuple,
        and this string (error message) is formed properly regardless of the
        manner of the exception's instantiation.

        Test ID: TEST-T-260. Covers the requirement: REQ-FUN-260.
        """
        tupError = ('Key not found S_Exception[test]', )
        objError = self.TestClass('S_Exception', 'test')
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation')
        del objError
        try:
            raise self.TestClass('S_Exception', 'test', SkipFrames = 1)
        except self.TestClass as err:
            self.assertEqual(err.args, tupError,
                            msg = 'truncated instantiation')
            tbTemp = err.__traceback__
        objError = self.TestClass('S_Exception', 'test', FromTraceback = tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation')
        del objError
        objError = self.TestClass('S_Exception', 'test').with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'simple instantiation -> chained')
        del objError
        objError = self.TestClass('S_Exception', 'test',
                                    SkipFrames = 1).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'truncated instantiation -> chained')

        del objError
        objError = self.TestClass('S_Exception', 'test',
                                FromTraceback = tbTemp).with_traceback(tbTemp)
        self.assertEqual(objError.args, tupError,
                            msg = 'substitution instantiation -> chained')
        del objError
        del tbTemp

class Test_Sub_TypeError(Test_UT_TypeError):
    """
    Test cases for the sub-class of
    introspection_lib.base_exceptions.UT_TypeError.
    
    Implements tests: TEST-T-203. Covers the requirement REQ-FUN-204.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = S_TypeError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        TypeError, testmodule.UT_TypeError]
        cls.NotChildOf = [ValueError, testmodule.UT_ValueError,
                            S_ValueError,
                            AttributeError, testmodule.UT_AttributeError,
                            S_AttributeError,
                            IndexError, testmodule.UT_IndexError,
                            S_IndexError,
                            KeyError, testmodule.UT_KeyError, S_KeyError,
                            S_Exception]
        cls.ParentOf = []
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError, S_Exception,
                            S_AttributeError, S_IndexError,
                            S_ValueError, S_KeyError]
        cls.DefArguments = ['test', int]

class Test_Sub_ValueError(Test_UT_ValueError):
    """
    Test cases for the sub-class of
    introspection_lib.base_exceptions.UT_ValueError.
    
    Implements tests: TEST-T-203. Covers the requirement REQ-FUN-204.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = S_ValueError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        ValueError, testmodule.UT_ValueError]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError, S_TypeError,
                            AttributeError, testmodule.UT_AttributeError,
                            S_AttributeError,
                            IndexError, testmodule.UT_IndexError,
                            S_IndexError,
                            KeyError, testmodule.UT_KeyError, S_KeyError,
                            S_Exception]
        cls.ParentOf = []
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError, S_Exception,
                            S_TypeError, S_AttributeError, S_IndexError,
                            S_KeyError]
        cls.DefArguments = ['test', 'whatever']

class Test_Sub_AttributeError(Test_UT_AttributeError):
    """
    Test cases for the sub-class of
    introspection_lib.base_exceptions.UT_AttributeError.
    
    Implements tests: TEST-T-203. Covers the requirement REQ-FUN-204.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = S_AttributeError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        AttributeError, testmodule.UT_AttributeError]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError, S_TypeError,
                            ValueError, testmodule.UT_ValueError, S_ValueError,
                            IndexError, testmodule.UT_IndexError, S_IndexError,
                            KeyError, testmodule.UT_KeyError, S_KeyError,
                            S_Exception]
        cls.ParentOf = []
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError, S_Exception,
                            S_TypeError, S_IndexError,
                            S_ValueError, S_KeyError]
        cls.DefArguments = ['test', 'whatever']

class Test_Sub_IndexError(Test_UT_IndexError):
    """
    Test cases for the sub-class of
    introspection_lib.base_exceptions.UT_IndexError.
    
    Implements tests: TEST-T-203. Covers the requirement REQ-FUN-204.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = S_IndexError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        IndexError, testmodule.UT_IndexError]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError, S_TypeError,
                            ValueError, testmodule.UT_ValueError, S_ValueError,
                            AttributeError, testmodule.UT_AttributeError,
                            S_AttributeError,
                            KeyError, testmodule.UT_KeyError, S_KeyError,
                            S_Exception]
        cls.ParentOf = []
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError, S_Exception,
                            S_TypeError, S_AttributeError,
                            S_ValueError, S_KeyError]
        cls.DefArguments = ['test', 1]

class Test_Sub_KeyError(Test_UT_KeyError):
    """
    Test cases for the sub-class of
    introspection_lib.base_exceptions.UT_KeyError.
    
    Implements tests: TEST-T-203. Covers the requirement REQ-FUN-204.
    """
    
    @classmethod
    def setUpClass(cls):
        """
        Preparation for the test cases, done only once.
        """
        cls.TestClass = S_KeyError
        cls.ChildOf = [Exception, BaseException, testmodule.UT_Exception,
                        KeyError, testmodule.UT_KeyError]
        cls.NotChildOf = [TypeError, testmodule.UT_TypeError, S_TypeError,
                            ValueError, testmodule.UT_ValueError, S_ValueError,
                            AttributeError, testmodule.UT_AttributeError,
                            S_AttributeError,
                            IndexError, testmodule.UT_IndexError, S_IndexError,
                            S_Exception]
        cls.ParentOf = []
        cls.NotParentOf = [TypeError, ValueError, AttributeError, IndexError,
                            KeyError, Exception, testmodule.UT_TypeError,
                            testmodule.UT_ValueError,
                            testmodule.UT_AttributeError,
                            testmodule.UT_IndexError,
                            testmodule.UT_KeyError, S_Exception,
                            S_TypeError, S_AttributeError, S_IndexError,
                            S_ValueError]
        cls.DefArguments = ['test', 'whatever']

#+ test suites

TestSuite1 = unittest.TestLoader().loadTestsFromTestCase(Test_UT_Exception)
TestSuite2 = unittest.TestLoader().loadTestsFromTestCase(Test_UT_TypeError)
TestSuite3 = unittest.TestLoader().loadTestsFromTestCase(Test_UT_ValueError)
TestSuite4 = unittest.TestLoader().loadTestsFromTestCase(Test_UT_AttributeError)
TestSuite5 = unittest.TestLoader().loadTestsFromTestCase(Test_UT_IndexError)
TestSuite6 = unittest.TestLoader().loadTestsFromTestCase(Test_UT_KeyError)
TestSuite7 = unittest.TestLoader().loadTestsFromTestCase(Test_Sub_Exception)
TestSuite8 = unittest.TestLoader().loadTestsFromTestCase(Test_Sub_TypeError)
TestSuite9 = unittest.TestLoader().loadTestsFromTestCase(Test_Sub_ValueError)
TestSuite10=unittest.TestLoader().loadTestsFromTestCase(Test_Sub_AttributeError)
TestSuite11 = unittest.TestLoader().loadTestsFromTestCase(Test_Sub_IndexError)
TestSuite12 = unittest.TestLoader().loadTestsFromTestCase(Test_Sub_KeyError)
TestSuite = unittest.TestSuite()
TestSuite.addTests([TestSuite1, TestSuite2, TestSuite3, TestSuite4, TestSuite5,
                    TestSuite6, TestSuite7, TestSuite8, TestSuite9, TestSuite10,
                    TestSuite11, TestSuite12])

if __name__ == "__main__":
    sys.stdout.write(
            "Conducting introspection_lib.base_exceptions module tests...\n")
    sys.stdout.flush()
    unittest.TextTestRunner(verbosity = 2).run(TestSuite)