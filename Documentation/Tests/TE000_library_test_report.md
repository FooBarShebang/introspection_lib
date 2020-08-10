# Test Report on the Library introspection_lib

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

## Tests definition (Test)

**Test Identifier:** TEST-T-000

**Requirement ID(s)**: REQ-FUN-000

**Verification method:** T

**Test goal:** Correctness of the implemenation of the call / exception traceback wrapper functionality.

**Expected result:** All tests defined in the document [TE001](./TE001_traceback_test_report.md) have passed.

**Test steps:** Run the unit-test module [Tests/UT001_traceback.py](../../Tests/UT001_traceback.py).

**Test result:** PASS

---

**Test Identifier:** TEST-T-001

**Requirement ID(s)**: REQ-IAR-000, REQ-IAR-002

**Verification method:** T

**Test goal:** System requirements check.

**Expected result:** The dependencies check script (module) is present and it detects the missing dependencies, too old versions as well as improper or too old Python interpreter version.

**Test steps:** Run the check module [check_dependencies.py](../../check_dependencies.py). All checks should pass. Then modify values in the check configuration file [dependencies.json](../../dependencies.json), i.e. names of the modules, or their versions, etc. Re-run the script; missing or too old dependencies should be reported. Revert the changes and change the required Python intepreter version (major) from 3 to 2. Re-run the script; the improper Python version should be reported. Change the major Python version back to 3, and set the minor version to 100 (nether should be there!). Re-run the script; the too old Python version should be reported. Revert all changes.

**Test result:** PASS

---

**Test Identifier:** TEST-T-002

**Requirement ID(s)**: REQ-IAR-001

**Verification method:** T

**Test goal:** Multi-platform functionality.

**Expected result:** All defined unit-tests pass under any tested OS.

**Test steps:** Run each of the defined unit-tests suites (./Tests folder) under, at least, MS Windows and GNU Linux OSes (current releases). Repeat this test under other OSes for which this library is to be tested and released. Mark the tested OS + Python version in the [tested_OS.md](./tested_OS.md) document.

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-000        | TEST-T-000             | YES                      |
| REQ-IAR-000        | TEST-T-001             | YES                      |
| REQ-IAR-001        | TEST-T-002             | YES                      |
| REQ-IAR-002        | TEST-T-001             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
