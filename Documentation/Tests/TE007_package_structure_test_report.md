# TE007 Test Report on the Module package_structure

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

Implement the unit test cases in the [UT006_package_structure](../../Tests/UT006_package_structure.py) module.

## Tests definition (Test)

**Test Identifier:** TEST-T-710

**Requirement ID(s)**: REQ-FUN-710, REQ-AWM-700

**Verification method:** T

**Test goal:** Checking if a path is a Python source module.

**Expected result:** **True** is returned if the passed path points to an existing, actual '.py' file, not a symlink. **False** is returned if the path points to a symlink, or such file does not exist. A (sub-) class of **TypeError** is raised if the argument is not a string.

**Test steps:**

* Execute the unit test cases defined in the class **Test_IsPyFile**.
* Create a temporary 'temp.py' file directly in the tests folder, and write a single line `raise ImportError` into it. Create a symlink 'link.py' to this file also in the tests folder directly.
* Pass into the tested function the paths to the created temporary file and to the unit tests suite file itself. No exceptions should be raised, returned value should be True.
* Pass as the argument the paths to the tests folder, to the created symlink, to a non-existing file and to a non-existing folder. No exceptions should be raised, returned value should be False.
* Pass different arguments of non-string types. An instance of (sub-class of) TypeError should be raised each time.
* Delete the created symlink and the temporary file.

**Test result:** PASS

---

**Test Identifier:** TEST-T-720

**Requirement ID(s)**: REQ-FUN-720, REQ-AWM-700

**Verification method:** T

**Test goal:** Checking if a path is a Python package.

**Expected result:** **True** is returned if the passed path points to an existing folder containing '\_\_init\_\_.py' file; both the folder and the required file should not be links. **False** is returned if the path points to a symlink, or such real file does not exist in the folder, or such folder is not found. A (sub-) class of **TypeError** is raised if the argument is not a string.

**Test steps:**

* Execute the unit test cases defined in the class **Test_IsPyPackage**.
* Create a temporary 'temp' folder directly in the tests folder, create the '\_\_init\_\_.py' therein and write a single line `raise ImportError` into it. Create a symlink 'link' to this new folder also in the tests folder directly.
* Pass into the tested function the paths to the created temporary folder and to the library itself. No exceptions should be raised, returned value should be True.
* Pass as the argument the paths to the tests folder, to the created symlink, to an existing source file, to a non-existing file and to a non-existing folder. No exceptions should be raised, returned value should be False.
* Pass different arguments of non-string types. An instance of (sub-class of) TypeError should be raised each time.
* Delete the created symlink and the temporary file.

---

**Test Identifier:** TEST-T-730

**Requirement ID(s)**: REQ-FUN-730, REQ-AWM-700

**Verification method:** T

**Test goal:** Find all actual Python source code files in an actual folder.

**Expected result:** An empty list is returned, if the folder does not exists, it is a symlink, or it contains no actual (not symlinks) Python source code files. A list of the base filenames of all found actual Python source code files in an actual folder is returned otherwise. A (sub-) class of **TypeError** is raised if the argument is not a string.

**Test steps:**

* Execute the unit test cases defined in the class **Test_SelectPySourceFiles**.
* Create a temporary 'temp' folder directly in the tests folder, create a number of '.py' files therein (e.g. 'a.py', 'b.py', 'c.py') and write a single line `raise ImportError` into each. Create a symlink 'link.py' to the last created '.py' file. Create a symlink 'link' to this new (top) folder also in the tests folder directly. Create a subfolder 'test' in the created folder (not in symlink), add a Python file ('d.py') and write `raise ImportError` into it.
* Pass into the tested function the paths to the created temporary folder. No exceptions should be raised, returned value should be a list containg only the base filenames (i.e. 'a.py', 'b.py', 'c.py') of the created files, whereas the symlink to a source file should not be included.
* Pass as the argument the paths  to the created symlink to a folder, to an existing source file, to a non-existing file and to a non-existing folder, and to an existing folder containing no Python source files. No exceptions should be raised, returned value should be an empty list.
* Pass different arguments of non-string types. An instance of (sub-class of) TypeError should be raised each time.
* Delete the created symlinks, the temporary files and folder.

**Test result:** PASS

---

**Test Identifier:** TEST-T-740

**Requirement ID(s)**: REQ-FUN-740, REQ-AWM-700

**Verification method:** T

**Test goal:** Proper resolution of the fully qualified module / package name.

**Expected result:** The base name without the extension should be returned for a stand-alone module / script (not a part of a package). The folder's base name should be returned for the 'root' package path. For the modules and sub-packages nested inside another package the returned strings should be formed as
'package.subpackage.{...}.module' and 'package.{...}.subpackage' respectively, where {...} is the all intermediate sub-packages hierarchy. **None** value should be returned for the passed paths to symlinks, files being not Python source files, folders being not Python packages, and non-existing files or folders. A (sub-) class of **TypeError** is raised if the argument is not a string.

**Test steps:**

* Execute the unit test cases defined in the class **Test_GetQualifiedName**.
* Create a temporary 'temp' folder directly in the tests folder, create two '.py' files therein - 'a.py' and '\_\_init\_\_.py', and write a single line `raise ImportError` into each. Create a symlink 'link' to this new (top) folder also in the tests folder directly. Create a subfolder 'test' in the created folder (not in symlink), add two Python files - 'a.py' and '\_\_init\_\_.py', and write `raise ImportError` into each. Create a symlink 'link.py' to the last created 'a.py' file within the nested sub-folder. Also create 'a.py' file directly in the tests folder, and write `raise ImportError` into it.
* Pass into the tested function the following paths (here indicated relative to the test folders) and compare the returned values with the expected ones:
  * '../' -> 'introspection_lib'
  * '../package_structure.py' -> 'introspection_lib.package_structure'
  * '../README.md' -> None
  * './' -> None
  * './temp2' -> None
  * './whatever.py' -> None
  * './a.py' -> 'a'
  * './temp' -> 'temp'
  * './temp/a.py' -> 'temp.a'
  * './temp/test' -> 'temp.test'
  * './temp/test/a.py' -> 'temp.test.a'
  * './temp/test/link.py' -> None
  * './link' -> None
  * './link/a.py' -> None
  * './link/test' -> None
  * './link/test/a.py' -> None
  * './link/test/link.py' -> None
* Pass different arguments of non-string types. An instance of (sub-class of) TypeError should be raised each time.
* Delete the created symlinks, the temporary files and folders.

**Test result:** PASS

---

**Test Identifier:** TEST-T-750

**Requirement ID(s)**: REQ-FUN-750, REQ-AWM-700, REQ-AWM-701

**Verification method:** T

**Test goal:** Proper conversion of a relative import name, preservation of an absolute import name.

**Expected result:** The passed absolute import name should be preserved regardless of the value of the passed file path, as long as it is a string. The passed relative import name should be converted into an absolute one, starting from the 'root' package, as longs as: a) the passed file path points to an actual Python source file, and b) the relative path remains within the 'root' package, even if the resulting module / sub-package does not exist. A (sub-) class of **TypeError** is raised if any of the two arguments is not a string. A (sub-) class of **ValueError** is raised if the file path does not point to an actual Python source file in the case of the relative import path, OR the relative path leads to outside of the 'root' package for the module.

**Test steps:**

* Execute the unit test cases defined in the class **Test_GetQualifiedName**.
* Create a temporary 'temp' folder directly in the library folder, create two '.py' files therein - 'a.py' and '\_\_init\_\_.py', and write a single line `raise ImportError` into each. Create a symlink 'link' to this new (top) folder also in the library folder directly. Create a subfolder 'test' in the created folder (not in symlink), add two Python files - 'a.py' and '\_\_init\_\_.py', and write `raise ImportError` into each. Create a symlink 'link.py' to the last created 'a.py' file within the nested sub-folder.
* Try to pass an arbitrary string as the first argument, and and arbitrary string but not starting with '.' as the second argument. The unmodified value of the second argument must be returned.
* Try different valid relative imports (relatively to and exisiting module within the entire library or any of its sub-packages, including the created folders) - the returned values should be the same as the expected
* Try different invalid relative imports (check for **ValueError** being raised, or any of its sub-classes):
  * The file argument does not point to an existing source file, being a module in a package as
    * A symlink to a module in a package
    * A symlink to a package
    * An existing file, but not a Python source file
    * An existing stand-alone Python source file, not in a package
    * An existing generic folder (not a package)
    * A non-existing path
  * Different relative paths with too long 'climbing-up' suffix relative to the 'root' package of an existing module
* Pass different values of non-string types as the first, the second or both arguments. An instance of (sub-class of) **TypeError** should be raised each time.
* Delete the created symlinks, the temporary files and folders.

## Tests definition (Analysis)

**Test Identifier:** TEST-A-700

**Requirement ID(s)**: REQ-FUN-700

**Verification method:** A

**Test goal:** Completeness and correctness of the required functionality of the module

**Expected result:** All tests defined in *Tests definition (Tests)* section are passed.

**Test steps:** Execute the unit test module [UT006_package_structure](../../Tests/UT006_package_structure.py), and perform all defined test cases.

**Test result:** PASS/FAIL

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)**                                                             | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------------------------------------------------------------------- | :----------------------- |
| REQ-FUN-700        | TEST-A-700                                                                         | NO                       |
| REQ-FUN-710        | TEST-T-710                                                                         | YES                      |
| REQ-FUN-720        | TEST-T-720                                                                         | YES                      |
| REQ-FUN-730        | TEST-T-730                                                                         | YES                      |
| REQ-FUN-740        | TEST-T-740                                                                         | YES                      |
| REQ-FUN-750        | TEST-T-750                                                                         | YES                      |
| REQ-AWM-700        | All TEST-T-7??                                                                     | NO                       |
| REQ-AWM-701        | TEST-T-750                                                                         | NO                       |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | Under development             |
