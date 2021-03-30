# TE004 Test Report on the Module introspection_lib.universal_access

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

Define the test cases in the unit-test module [UT004](../../Tests/UT004_universal_access.py). Define simple storage (structured or container) classes:

* Emulating C struct-like (mutable)
* Emulating immutable (frozen) dictionary
* Named tuple class
* Complex stucture incorporating mutable and immutable sequences and mappings as well as a simple structure on the different levels of nesting

## Tests definition (Test)

**Test Identifier:** TEST-T-500

**Requirement ID(s)**: REQ-FUN-500, REQ-AWM-500

**Verification method:** T

**Test goal:** Proper flattening of the generic 'nested' path definition into its canonical form according to the specifications in [DE001](../Design/DE001_element_path.md).

**Expected result:** The properly formed generic 'nested' paths are transformed according the following rules:

* The returned result is always a list, which can contain only integers and strings
* An integer or a string without dots within are returned as a single element list containg the input value
* An empty top level sequence is returned as an empty list
* An empty sequence nested in other sequence is ignored regardless of the depth of nesting
* The flattening is 'depth-first', i.e. strings with dots and nested sequences are expanded into the individual components of the returned flat list before proceeding to the next element at the same level of nesting
* The 'depth-first' principle is applied recursively to the sequences

The impoper format of the passed path definition results in an exception, which is considered to sub-class **TypeError**:

* The passed argument is not an integer, string or sequence
* The passed sequence contains, at least, one element, which is not an integer, string or sequence itself
* (Recursively) any nested sequence contains, at least, one element, which is not an integer, string or sequence itself - regardless of the depth of nesting

**Test steps:** Execute the unit-test module UT004. Run test cases defined in the class **Test_FlattenPath**. Check that the proper defined generic paths are flattened as expected, whereas the definitions non-conforming DE001 result in an exception compatible with **TypeError**.

**Test result:** PASS

---

**Test Identifier:** TEST-T-510

**Requirement ID(s)**: REQ-FUN-501, REQ-FUN-510, REQ-AWM-500, REQ-AWM-503

**Verification method:** T

**Test goal:** 'Strict' mode read access to the direct end-node by its index, key or attribute name

**Expected result:** The values of existing nodes are retried with the type of access selected automatically based on the type of the object and path:

* Index access - for sequence types, including immutable and, specificically, named tuple - with an integer path argument
* Key name access - for the mapping types, including immutable - with a string path argument
* Attribute name access - for the other types, expected to be generic classes or instances - with a string path argument. Also for a named tuple.

Specific exceptions are raised in the following situations:

* Neither integer, nor string argument as the path - sub-class of **TypeError**
* String argument for index access (sequences, except for named tuple) - sub-class of **TypeError**
* Integer argument for key or attribute access (mappings and generic classes, except for named tuples) - sub-class of **TypeError**
* Integer index is out of the range (any sequence) - sub-class of **IndexError**
* Non-existing key (any mapping) - sub-class of **KeyError**
* Non-existing attribute (object instance and named tuple) - sub-class of **AttributeError**

**Test steps:** Execute the unit-test module UT004. Run test cases defined in the class **Test_GetData**. Create instances of the different data types, inculding struct-like class instance, a mutable and immutable dictionaries, mutable and immutable sequences, including named tuple. Retrieve the values of the components using function being tested with a proper type and value of the path argument, and compare the returned values with those accessed directly in the same object using the standard for that type access mode - dot notation, key or index. In the case of the sequences try negative indexes as well (full range from -len() to len()-1 inclusively). Check that the requried exceptions are raised in the all cases discussed in the expected results.

**Test result:** PASS

---

**Test Identifier:** TEST-T-520

**Requirement ID(s)**: REQ-FUN-501, REQ-FUN-520, REQ-AWM-500

**Verification method:** T

**Test goal:** 'Relaxed' mode read access to the direct end-node by its index, key or attribute name

**Expected result:** The values of existing nodes are retried with the type of access selected automatically based on the type of the object and path:

* Index access - for sequence types, including immutable and, specificically, named tuple - with an integer path argument
* Key name access - for the mapping types, including immutable - with a string path argument
* Attribute name access - for the other types, expected to be generic classes or instances - with a string path argument. Also for a named tuple.

Specific exceptions are raised in the following situations:

* Neither integer, nor string argument as the path - sub-class of **TypeError**
* String argument for index access (sequences, except for named tuple) - sub-class of **TypeError**
* Integer argument for key or attribute access (mappings and generic classes, except for named tuples) - sub-class of **TypeError**

When accessing the out of range indexes or non-existing keys or attributes a specific default value is returned, and no exceptions occurs.

**Test steps:** Execute the unit-test module UT004. Run test cases defined in the class **Test_GetDataDefault**. Create instances of the different data types, inculding struct-like class instance, a mutable and immutable dictionaries, mutable and immutable sequences, including named tuple. Retrieve the values of the components using function being tested with a proper type and value of the path argument, and compare the returned values with those accessed directly in the same object using the standard for that type access mode - dot notation, key or index. In the case of the sequences try negative indexes as well (full range from -len() to len()-1 inclusively). Check that the requried exceptions are raised in the all cases discussed in the expected results.

**Test result:** PASS

---

**Test Identifier:** TEST-T-530

**Requirement ID(s)**: REQ-FUN-530, REQ-AWM-500 and REQ-AWM-502

**Verification method:** T

**Test goal:** 'Relaxed' mode write access to the direct end-node by its index, key or attribute name

**Expected result:** The values of existing nodes are modified as expected with the type of access selected automatically based on the type of the object and path:

* Index access - for mutable sequence types - with an integer path argument
* Key name access - for the mutable mapping types - with a string path argument
* Attribute name access - for the other types, expected to be generic classes or instances - with a string path argument

Specific exceptions are raised in the following situations:

* Attempted modification of an immutable object (e.g. tuple, named tuple, frozen dict), even in the case of the matching type of the path (integer or string) - sub-class of **TypeError**
* Neither integer, nor string argument as the path - sub-class of **TypeError**
* String argument for index access (sequences, except for named tuple) - sub-class of **TypeError**
* Integer argument for key or attribute access (mappings and generic classes, except for named tuples) - sub-class of **TypeError**

When accessing the non-existing keys or attributes the corresponding key (entry) or attribute are added to the mutable object. In the case of the mutable sequences and out of the range index:

* An element is added before the already existed (at index 0) if the passed index is negative and less than - len() of the sequence
* An element is added after the already existed (at index len()) if the passed index is positive and greater than len() of the sequence - 1

**Test steps:** Execute the unit-test module UT004. Run test cases defined in the class **Test_SetData**. Create instances of the different data types, inculding struct-like class instance, a mutable and immutable dictionaries, mutable and immutable sequences, including named tuple. Check that the values of the existing elements / keys / attributes of the mutable objects can be changed. Check that setting of an element / key / attribute of the mutable objects, which does not exist yet, does occur as expected (especially for sequences) . Check that the requried exceptions are raised in the all cases discussed in the expected results, especially if an immutable object is considered.

**Test result:** PASS

---

**Test Identifier:** TEST-T-540

**Requirement ID(s)**: REQ-FUN-540, REQ-AWM-500, REQ-AWM-502 and REQ-AWM-503.

**Verification method:** T

**Test goal:** 'Strict' mode write access to the direct end-node by its index, key or attribute name

**Expected result:** The values of existing nodes are modified as expected with the type of access selected automatically based on the type of the object and path:

* Index access - for mutable sequence types - with an integer path argument
* Key name access - for the mutable mapping types - with a string path argument
* Attribute name access - for the other types, expected to be generic classes or instances - with a string path argument

Specific exceptions are raised in the following situations:

* Attempted modification of an immutable object (e.g. tuple, named tuple, frozen dict), even in the case of the matching type of the path (integer or string) - sub-class of **TypeError**
* Neither integer, nor string argument as the path - sub-class of **TypeError**
* String argument for index access (sequences, except for named tuple) - sub-class of **TypeError**
* Integer argument for key or attribute access (mappings and generic classes, except for named tuples) - sub-class of **TypeError**
* Integer index is out of the range (any sequence) - sub-class of **IndexError**
* Non-existing key (any mapping) - sub-class of **KeyError**
* Non-existing attribute (object instance and named tuple) - sub-class of **AttributeError**

**Test steps:** Execute the unit-test module UT004. Run test cases defined in the class **Test_SetDataStrict**. Create instances of the different data types, inculding struct-like class instance, a mutable and immutable dictionaries, mutable and immutable sequences, including named tuple. Check that the values of the existing elements / keys / attributes of the mutable objects can be changed. Check that the requried exceptions are raised in the all cases discussed in the expected results, especially if an immutable object is considered, and the non-existing index, key or attribute.

**Test result:** PASS

---

**Test Identifier:** TEST-T-550

**Requirement ID(s)**: REQ-FUN-500, REQ-FUN-501, REQ-FUN-550, REQ-AWM-500, REQ-AWM-501 and REQ-AWM-503

**Verification method:** T

**Test goal:** 'Strict' and 'Relaxed' mode read access to the 'nested' mode by generic path definition

**Expected result:** The values of existing nodes are accessed as expected with the type of access selected automatically based on the type of the object and path - in both 'strict' and 'relaxed' modes, with and without the default value provided. When accessing the non-existing nodes in the 'relaxed' mode the passed default value is returned, or None is returned if the default value is not provided. When accessing the non-existing nodes in the 'strict' mode the sub-class of **IndexError**, **AttributeError** or **KeyError** is raised, based on the type of the last found node along the path. The sub-class of **ValueError** is raised if the path is reducible to an empty list regardless of the used mode and default value. **TypeError** sub-class exception is raised if the provided path is not proper (see DE001), or there is a mismatch between the type of an existing node and the type of the path element for its component to be obtained - regardless of the used mode and default value.

**Test steps:** Execute the unit-test module UT004. Run test cases defined in the class **Test_GetElement**. Create an instance of the complex structure (make new before each test). Pass the improper format, reducible to empty, proper formed but not matching the specific level access type and proper formed but refering to a non-existent branch or end-node paths (the last is only in the 'strict' mode). Check that the proper type of an exception is raised. Access different branches and end-nodes using different notation allowed for the proper path definition, and compare the returned values with those retrieved using direct dot-notation (attribute), index and key access, which can be mixed for deeply nested nodes. Attempt to retrive the value of a non-existing node with and without the provided default value in the 'relaxed' mode - the returned values should the passed default one and None respectively.

**Test result:** PASS

---

**Test Identifier:** TEST-T-560

**Requirement ID(s)**: REQ-FUN-500, REQ-FUN-501, REQ-FUN-560, REQ-AWM-500, REQ-AWM-501, REQ-AWM-502 and REQ-AWM-503

**Verification method:** T

**Test goal:** 'Strict' and 'Relaxed' mode write access to the 'nested' mode by generic path definition

**Expected result:** The values of existing nodes are accessed and modified as expected with the type of access selected automatically based on the type of the object and path - in both 'strict' and 'relaxed' modes, with and without the default value provided - but only if the respective node is mutable. Modification of an immutable object (or its element) should result in a sub-class of **TypeError** exception. When accessing the non-existing nodes in the 'relaxed' the missing part of the path is created automatically using nesting of dictionaries and lists (is the missing sub-path is longer than 1 element), unless the node to which a branch will be attached is immutable. When accessing the non-existing nodes of in the 'strict' mode the sub-class of **IndexError**, **AttributeError** or **KeyError** is raised, based on the type of the last found node along the path. The sub-class of **ValueError** is raised if the path is reducible to an empty list regardless of the used mode and default value. **TypeError** sub-class exception is raised if the provided path is not proper (see DE001), or there is a mismatch between the type of an existing node and the type of the path element for its component to be obtained - regardless of the used mode and default value.

Note, that named tuple is immutable for the both index and attribute access.

**Test steps:** Execute the unit-test module UT004. Run test cases defined in the class **Test_SetElement**. Create an instance of the complex structure (make new before each test). Pass the improper format, reducible to empty, proper formed but not matching the specific level access type and proper formed but refering to a non-existent branch or end-node paths (the last is only in the 'strict' mode for mutable, in the both modes for immutable types). Check that the proper type of an exception is raised. Access different existing and mutable end-nodes using different notation allowed for the proper path definition, and check that their values are properly changed using direct dot-notation (attribute), index and key access, which can be mixed for deeply nested nodes. Attempt to assign a value to a non-existing end-node and check the result. Attempt to attach a branch (sub-path of more than 2 element from the last found level, which must be mutable) and check that it is created properly.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                                             | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------------------------------------------------------------------- | :----------------------- |
| REQ-FUN-500        | TEST-T-500, TEST-T-550, TEST-T-560                                                 | YES                      |
| REQ-FUN-501        | TEST-T-510, TEST-T-520, TEST-T-550, TEST-T-560                                     | YES                      |
| REQ-FUN-510        | TEST-T-510                                                                         | YES                      |
| REQ-FUN-520        | TEST-T-520                                                                         | YES                      |
| REQ-FUN-530        | TEST-T-530                                                                         | YES                      |
| REQ-FUN-540        | TEST-T-540                                                                         | YES                      |
| REQ-FUN-550        | TEST-T-550                                                                         | YES                      |
| REQ-FUN-560        | TEST-T-560                                                                         | YES                      |
| REQ-AWM-500        | TEST-T-500, TEST-T-510, TEST-T-520, TEST-T-530, TEST-T-540, TEST-T-550, TEST-T-560 | YES                      |
| REQ-AWM-501        | TEST-T-550, TEST-T-560                                                             | YES                      |
| REQ-AWM-502        | TEST-T-530, TEST-T-540, TEST-T-560                                                 | YES                      |
| REQ-AWM-503        | TEST-T-510, TEST-T-540, TEST-T-550, TEST-T-560                                     | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
