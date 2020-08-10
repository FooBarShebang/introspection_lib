# Test Report on the Module introspection_lib.traceback

## Conventions

Each test is defined following the same format. Each test receives a unique test identifier and a reference to the ID(s) of the requirements it covers (if applicable). The goal of the test is described to clarify what is to be tested. The test steps are described in brief but clear instructions. For each test it is defined what the expected results are for the test to pass. Finally, the test result is given, this can be only pass or fail.

The test format is as follows:

**Test Identifier:** TEST-\[I/A/D/T\]-XYZ

**Requirement ID(s)**: REQ-uvw-xyz

**Verification method:** I/A/D/T

**Test goal:** Description of what is to be tested

**Expected result:** What test result is expected for the test to pass

**Test steps:** Step by step instructions on how to perform the test

**Test result:** PASS/FAIL

The test ID starts with the fixed prefix 'TEST'. The prefix is followed by a single letter, which defines the test type / verification method. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the test ordering number for this object. E.g. 'TEST-T-112'. Each test type has its own counter, thus 'TEST-T-112' and 'TEST-A-112' tests are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Tests preparations

Prepare the unit-test module with the test cases classes for the StackTraceback and ExceptionTraceback classes, see module [Tests/UT001_traceback.py](../../Tests/UT001_traceback.py). Also define a set of helper functions for the exception traceback testing, which implement the following call chain: outer() -> middle() -> inner() -> exception raised.

See unit-test module libexceptions.tests.traceback_ut.

## Tests definition (Test)

**Test Identifier:** TEST-T-100

**Requirement ID(s)**: REQ-FUN-100, REQ-FUN-102

**Verification method:** T

**Test goal:** Correctness of the call chain: order, names and number of the 'callers'.

**Expected result:** The call chain is returned as a list of strings, each string being a fully qualified name of the 'caller', i.e. *module.function* or *module.class.method*. The top level caller - main module or console - is represented as '\_\_main\_\_' and '\<console input\>' respectively. The order of the callers is from the top level towards the frame, where the class StackTraceback is instantiated. When specified during the instantiation, the required number of the 'callers' is removed from the tail of the list (the latest, closest to the frame of the unit-test, where the class is instantiated).

**Test steps:** Run the unit-test module, specifically the test case (method of the test cases class) designed for testing the property StackTraceback.CallChain. Instantiate the StackTraceback class within the test case without arguments. Access its property CallChain. Check that a sequence is returned. Check that the first element of the sequence is '\_\_main\_\_'. Check that the last element of the sequence is in the form 'test_module_name.test_class_name.test_method_name'. Instantiate the StackTraceback class again, specifing 1 or 2 frames to skip (as a keyword argument). Check that the CallChain property of that instance returns a sequence, which is shorter by the specified number, and it is simply a truncated version of the first sequence. Open interactive (console) session of Python, import and instantiate StackTraceback class. Check that the first element of the sequence returned by the property CallChain is '\<console input\>'.

**Test result:** PASS

---

**Test Identifier:** TEST-T-101

**Requirement ID(s)**: REQ-FUN-101

**Verification method:** T

**Test goal:** Correctness of the call chain frames information: order, amount of data, formatting of the source code sniplets.

**Expected result:** The call chain frames data is returned as a single string with multiple line separated by a single newline character. The total amount of lines equals the number of frames times 2 + number of the source code lines for each frame. Number and order of frames are the same as in the simple call chain call result. For each frame the first line contains the filename of the module, fully qualified name of the 'caller' and the number of the line in the source code. Starting from the 3rd line (for each frame separately) and to the end of this frame data each line shows the source code line number and its content truncated to the specified width. The source code sniplet is centered around the line, where the call is made.

**Test steps:** Run the unit-test module, specifically the test case (method of the test cases class) designed for testing the property StackTraceback.Info. Instantiate the StackTraceback class within the test case with the keyword arguments specifing the number of the source code line per frame and the width, to which they should be truncated. Retrieve the values of the prorties CallChain and Info. Check that the Info property yielded a string. Split the string into a list of strings by the newlines. The length of the resulting list must be equal to the length of the list returned by the CallChain property multiplied by the number of the source code lines per frame plus 2. Iterate through the call chain and analyse the lines of the Info value. For each frame / 'caller' the first line must contain (as sub-string) the same 'caller' fully qualified name, as it is listed in the call chain sequence. Skip the next line. Check that the next number of the source code lines per frame plus 2 lines are not longer than the specified truncation width.

Print the content of the Info property into the console and visually analyze / verify that for each frame the printed data conforms the design specifications.

**Test result:** PASS

---

**Test Identifier:** TEST-T-110

**Requirement ID(s)**: REQ-FUN-110, REQ-FUN-112

**Verification method:** T

**Test goal:** Correctness of the call chain of an exception traceback: order, names and number of the 'callers'.

**Expected result:** The call chain is returned as a list of strings, each string being a fully qualified name of the 'caller', i.e. *module.function* or *module.class.method*. The order of the callers is from the frame where the exception is captured towards the frame, where the exception is raised. When specified during the instantiation of the ExceptionTraceback, the required number of the 'callers' is removed from the tail of the list (the latest, closest to the frame, where the exception is raised).

**Test steps:** Run the unit-test module, specifically the test case (method of the test cases class) designed for testing the property ExceptionTraceback.CallChain. Call function outer() with try ... except clause, i.e. initiate outer() -> middle() -> inner() -> ValueError exception raised chain. Simply catch the ValueException and do not (re-) raise any exception. Instantiate the ExceptionTraceback class within the test case without arguments. Access its property CallChain. Check that a sequence is returned. Check that the first element of the sequence is '\_\_main\_\_'. Check that the last element of the sequence is in the form 'test_module_name.test_class_name.test_method_name'. Instantiate the ExceptionTraceback class again, specifing 1 or 2 frames to skip (as a keyword argument). Check that the CallChain property of that instance returns a sequence, which is shorter by the specified number, and it is simply a truncated version of the first sequence.

**Test result:** PASS

---

**Test Identifier:** TEST-T-111

**Requirement ID(s)**: REQ-FUN-111

**Verification method:** T

**Test goal:** Correctness of the exception traceback frames information: order, amount of data, formatting of the source code sniplets.

**Expected result:** The exception traceback frames data is returned as a single string with multiple line separated by a single newline character. The total amount of lines equals the number of frames times 2 + number of the source code lines for each frame. Number and order of frames are the same as in the simple call chain call result. For each frame the first line contains the filename of the module, fully qualified name of the 'caller' and the number of the line in the source code. Starting from the 3rd line (for each frame separately) and to the end of this frame data each line shows the source code line number and its content truncated to the specified width. The source code sniplet is centered around the line, where the call is made.

**Test steps:** Run the unit-test module, specifically the test case (method of the test cases class) designed for testing the property ExceptionTraceback.Info. Call function outer() with try ... except clause, i.e. initiate outer() -> middle() -> inner() -> ValueError exception raised chain. Simply catch the ValueException and do not (re-) raise any exception. Instantiate the ExceptionTraceback class within the test case with the keyword arguments specifing the number of the source code line per frame and the width, to which they should be truncated. Retrieve the values of the prorties CallChain and Info. Check that the Info property yielded a string. Split the string into a list of strings by the newlines. The length of the resulting list must be equal to the length of the list returned by the CallChain property multiplied by the number of the source code lines per frame plus 2. Iterate through the call chain and analyse the lines of the Info value. For each frame / 'caller' the first line must contain (as sub-string) the same 'caller' fully qualified name, as it is listed in the call chain sequence. Skip the next line. Check that the next number of the source code lines per frame plus 2 lines are not longer than the specified truncation width.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-100        | TEST-T-100             | YES                      |
| REQ-FUN-101        | TEST-T-101             | YES                      |
| REQ-FUN-102        | TEST-T-100             | YES                      |
| REQ-FUN-110        | TEST-T-110             | YES                      |
| REQ-FUN-111        | TEST-T-111             | YES                      |
| REQ-FUN-112        | TEST-T-110             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
