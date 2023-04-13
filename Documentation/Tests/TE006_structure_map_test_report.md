# TE006 Test Report on the Module structure_map

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

Define the test cases in the unit-test module [UT005](../../Tests/UT005_structure_map.py). *TODO*

## Tests definition (Test)

**Test Identifier:** TEST-T-600

**Requirement ID(s)**: REQ-AWM-600

**Verification method:** T

**Test goal:** An improper type of the argument for the functions *GetReadMap*() and *GetWriteMap*() is an error, resulting in an exception.

**Expected result:** A sub-class of the standard **TypeError** exception is raised if the passed object to be mapped is

* Anything but a scalar (int, float, bool, string, None), a mapping type, a sequence type or a generic data storage class (C-struct like), i.e.:
  * Any buit-in or user-defined function
  * Method of a class or class instance
  * Iterators, generators, etc. - callables, but not data storage classes
  * A type, not a value (e.g. **int** instead of 1, as a class and not an instance)
* A dictionary (top level or nested) containing not a string key

**Test steps:** Execute the unittest suite *UT005*, specifically the test case *test_TypeError* defined in the classes **Test_GetReadMap** and **Test_WriteMap**.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-610

**Requirement ID(s)**: REQ-FUN-600, REQ-FUN-601, REQ-FUN-602, REQ-FUN-610, REQ-FUN-611 and REQ-FUN-612

**Verification method:** T

**Test goal:** Check that the function *GetReadMap*() operates according to the specs in [DE002](../Design/DE002_structure_map.md).

**Expected result:** The following mapping rules are implemented:

* Any scalar (int, float, bool, str, None) is returned as it is
* Any empty sequence, except for named tuples passed is returned as an empty list
* Any empty mapping type or an empty named tuple passed is returned as an empty ordered dictionary
* Any plain mutable or immutable sequence, i.e. without nested sequences, mapping type or data storage class instances as elements, but not a named tuple is converted into a list with the values and order of the scalar (int, float, bool, str, None) elements being preserved, but all callable (but not data storage class instance) elements being removed
* Any plain mutable or immutable mapping type or a named tuple, i.e. without nested sequences, mapping type or data storage class instances as values of the keys, is converted into a list with the key:value pairs holding the scalar (int, float, bool, str, None) values being preserved, but all callable (but not data storage class instance) entries being removed. The order of keys is preserved, if the original data object had ordered keys. All keys should be strings.

**Test steps:** Execute the unittest suite *UT005*, specifically the test cases defined in the class **Test_GetReadMap**.

**Test result:** PASS/FAIL

---

**Test Identifier:** TEST-T-620

**Requirement ID(s)**: REQ-FUN-600, REQ-FUN-601, REQ-FUN-602, REQ-FUN-620, REQ-FUN-621 and REQ-FUN-622

**Verification method:** T

**Test goal:** Check that the function *GetReadMap*() operates according to the specs in [DE002](../Design/DE002_structure_map.md).

**Expected result:** The following mapping rules are implemented:

* Any scalar (int, float, bool, str, None) is returned as it is
* Any empty sequence, except for named tuples passed is returned as an empty list
* Any empty mapping type or an empty named tuple passed is returned as an empty ordered dictionary
* Any plain mutable sequence, i.e. without nested sequences, mapping type or data storage class instances as elements, but not a named tuple is converted into a list with the values and order of the scalar (int, float, bool, str, None) elements being preserved, but all callable (but not data storage class instance) elements being removed
* Any plain immutable sequence, i.e. without nested sequences, mapping type or data storage class instances as elements, but not a named tuple is converted into an empty list regardless the amount of scalar elements being present in the source object
* Any plain mutable mapping type, i.e. without nested sequences, mapping type or data storage class instances as values of the keys, is converted into a list with the key:value pairs holding the scalar (int, float, bool, str, None) values being preserved, but all callable (but not data storage class instance) entries being removed. The order of keys is preserved, if the original data object had ordered keys. All keys should be strings.
* Any plain immutable maping type or a plain named tuples, i.e. without nested sequences, mapping type or data storage class instances as values of the keys, is converted into an empty ordered dictionary regardless the amount of scalar values being present in the source object

**Test steps:** Execute the unittest suite *UT005*, specifically the test cases defined in the class **Test_GetWriteMap**.

**Test result:** PASS/FAIL

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                                             | **Verified \[YES/NO\]**  |
| :----------------- | :--------------------------------------------------------------------------------- | :----------------------- |
| REQ-FUN-600        | TEST-T-610, TEST-T-620                                                             | NO                       |
| REQ-FUN-601        | TEST-T-610, TEST-T-620                                                             | NO                       |
| REQ-FUN-602        | TEST-T-610, TEST-T-620                                                             | NO                       |
| REQ-FUN-610        | TEST-T-610                                                                         | NO                       |
| REQ-FUN-611        | TEST-T-610                                                                         | NO                       |
| REQ-FUN-612        | TEST-T-610                                                                         | NO                       |
| REQ-FUN-620        | TEST-T-620                                                                         | NO                       |
| REQ-FUN-621        | TEST-T-620                                                                         | NO                       |
| REQ-FUN-622        | TEST-T-620                                                                         | NO                       |
| REQ-AWM-600        | TEST-T-600                                                                         | NO                       |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | Under development             |
