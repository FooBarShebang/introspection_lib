# Test Report on the Module introspection_lib.base_exceptions

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

Prepare the unit-test module with the test cases classes for the defined custom exception classes, see module [Tests/UT002_base_exceptions.py](../../Tests/UT002_base_exceptions.py). Define a set of helper functions for the exception traceback testing, which implement the following call chain: outer() -> middle() -> inner() -> exception raised. Define direct sub-classes of the custom exception classes, as well as the same test cases for them.

## Tests definition (Test)

**Test Identifier:** TEST-T-200

**Requirement ID(s)**: REQ-FUN-200

**Verification method:** T

**Test goal:** The sub- / super class relations between the defined custom exceptions and the standard exceptions.

**Expected result:** All defined custom exceptions are sub-classes of their actial super-classes (direct as well as **Exception**), but they are also registerd as virtual sub-classes of **UT_Exception**. Except for being virtual sub-classes of **UT_Exception** all other custom exception adhere to the standard 'is a' relation model.

**Test steps:** Excecute the prepared test cases, specifically the methods *test_IsChild*(), *test_IsNotChild*(), *test_IsParent*() and *test_IsNotParent*().

**Test result:** PASS

---

**Test Identifier:** TEST-T-201

**Requirement ID(s)**: REQ-FUN-201

**Verification method:** T

**Test goal:** The sub- / super class relations between the defined custom exceptions and the standard exceptions.

**Expected result:** All defined custom exceptions are sub-classes of their actial super-classes (direct as well as **Exception**), but they are also registerd as virtual sub-classes of **UT_Exception**. Except for being virtual sub-classes of **UT_Exception** all other custom exception adhere to the standard 'is a' relation model.

**Test steps:** Excecute the prepared test cases, specifically the methods *test_IsChild*(), *test_IsNotChild*(), *test_IsParent*() and *test_IsNotParent*().

**Test result:** PASS

---

**Test Identifier:** TEST-T-202

**Requirement ID(s)**: REQ-FUN-202

**Verification method:** T

**Test goal:** The *\_\_traceback\_\_* argument always holds the actual traceback of the exception (inlcuding the chained frames), whereas the *Traceback* property may refer to the actual or substituted / truncated traceback, unless explicit chaining is perfromed (*with_traceback*() method is called) when it must refer to the actual extended traceback.

**Expected result:** All defined custom exceptions are sub-classes of their actial super-classes (direct as well as **Exception**), but they are also registerd as virtual sub-classes of **UT_Exception**. Except for being virtual sub-classes of **UT_Exception** all other custom exception adhere to the standard 'is a' relation model.

**Test steps:** Excecute the prepared test cases, specifically the methods *test_RaiseSimple*(), *test_RaiseTruncated*(), *test_RaiseSubstituted*() and *test_RaiseChained*().

**Test result:** PASS

---

**Test Identifier:** TEST-T-203

**Requirement ID(s)**: REQ-FUN-204

**Verification method:** T

**Test goal:** The sub-classes of the tested custom exceptions behave exactly as the tested exception, except for S_Exception -> UT_Exception, which is not the (virtual) parent to all other custom exceptions.

**Expected result:** All test (TEST-T-200, TEST-T-201, TEST-T-202, and all TEST-T-2x0) defined for the base custom exceptions are also passed being applied to the direct sub-classes of the corresponding exception.

**Test steps:** Excecute the prepared test cases defined for the sub-classes as copies of the corresponding test suits for their parents.

**Test result:** PASS

## Tests definition (Demonstration)

**Test Identifier:** TEST-D-200

**Requirement ID(s)**: REQ-FUN-203

**Verification method:** D

**Test goal:** Implicit and explicit chaining of the not handled exception.

**Expected result:** The treatment of the context / cause of a chained exceptions is not modified. I.e. the original exception leading to the raise of the current one should be printed out if the current exception is not caught (propagated to the interactive console). This behaviour should be observed in the following cases:

* Explicit chaining as *raise ... from ...* (where the 'reason' part is not None)
* Implicit chaining - in *except* or *finally* (w/o *from None* modifier)

**Test steps:** Try to (re-) raise the defined custom exceptions within these contexts and let them propagate to the console top interaction loop. Check the printed out traceback information.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-200        | TEST-T-100             | YES                      |
| REQ-FUN-201        | TEST-T-201             | YES                      |
| REQ-FUN-202        | TEST-T-202             | YES                      |
| REQ-FUN-203        | TEST-D-200             | YES                      |
| REQ-FUN-204        | TEST-T-203             | YES                      |
| REQ-FUN-210        | TEST-T-210             | YES                      |
| REQ-FUN-220        | TEST-T-220             | YES                      |
| REQ-FUN-230        | TEST-T-230             | YES                      |
| REQ-FUN-240        | TEST-T-240             | YES                      |
| REQ-FUN-250        | TEST-T-250             | YES                      |
| REQ-FUN-260        | TEST-T-260             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**           |
| :------------------------------------------: | :---------------------- |
| YES                                          | All tests are passed    |
