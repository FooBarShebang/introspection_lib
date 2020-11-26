# Test Report on the Module introspection_lib.logging

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

## Tests definition (Demonstration)

**Test Identifier:** TEST-D-300

**Requirement ID(s)**: REQ-FUN-300, REQ-FUN-303, REQ-FUN-305 and REQ-FUN-306.

**Verification method:** D

**Test goal:** Basic functionality, API and message propagation of a dual logger class.

**Expected result:** A dual logger class can be instantiated, and attached 'children' loggers can be created. Own file log can be attached to any of the chained loggers. With the default settings any of the chained loggers handles any level of the log message severity from DEBUG to CRITICAL; with any message being printed into the console only once, whereas it is added into the own log file (if attahced) as well as into any parents' log files up to the root of the hierarchy, but not into the log files of its siblings.

**Test steps:** Instantiate a dual class logger, create its 'child' logger and two 'grand-children' loggers. Leave the default settings of the logger instances, but attach own log files to each of the logger - do not specify the names, i.e. automatic log files names should be created. Issue all level messages from DEBUG to CRITICAL with each of the loggers in turn. Use the prepared module [DT002_logging_default](../../Tests/DT002_logging_default.py). Analyze the console output and the content of the created log files.

**Test result:** PASS

---

**Test Identifier:** TEST-D-301

**Requirement ID(s)**: REQ-FUN-306.

**Verification method:** D

**Test goal:** Manual rotation of the log files.

**Expected result:** A dual logger class can be instantiated, and attached 'children' loggers can be created. Own file log can be attached to any of the chained loggers. With the default settings any of the chained loggers handles any level of the log message severity from DEBUG to CRITICAL; with any message being printed into the console only once, whereas it is added into the own log file (if attahced) as well as into any parents' log files up to the root of the hierarchy, but not into the log files of its siblings.

**Test steps:** Instantiate a dual class logger, create its 'child' logger and two 'grand-children' loggers. Leave the default settings of the logger instances, but attach own log file to the 'root' logger. Issue info log message with the child logger. Try to disbale the file logging of the child logger - nothing should happen, then issue info log message with the child logger. Attach own log file to the child logger and issue a message. Switch to another file with the child logger and issue a message. Switch back to the original file of the child logger and issue another message. Dsiable file logging of the both loggers and issue the last message. Use the prepared module [DT003_logging_files](../../Tests/DT002_logging_files.py). Analyze the console output and the content of the created log files.

**Test result:** PASS

---

**Test Identifier:** TEST-D-310

**Requirement ID(s)**: REQ-FUN-310

**Verification method:** D

**Test goal:** Implementation of the 'dummy' logger.

**Expected result:** A 'dummy' logger class is defined, it can be instantiated, and it provides the minimum API set expected from a logger object: setLevel(), debug(), info(), warning(), error(), exception() and critical() - whilst no console or file output is actually created regardless of the logger's severity freshold or the level of the issued log message.

**Test steps:** Instantiate a 'dummy' logger class, set its severity threshold to the lowest ('DEBUG') level, issue one message at each level from 'DEBUG' to 'CRITICAL' - no console output log messages are printed, no any log file is created, thereas none of the exceptions is raised either. Use the prepared module [DT001_logging_dummy](../../Tests/DT001_logging_dummy.py).

**Test result:** PASS

## Traceability

For traceability the relation between tests and requirements is summarized in the table below:

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-300        | TEST-D-300             | YES                      |
| REQ-FUN-301        | TEST-D-30?             | NO                       |
| REQ-FUN-302        | TEST-D-30?             | NO                       |
| REQ-FUN-303        | TEST-D-300             | YES                      |
| REQ-FUN-304        | TEST-D-30?             | NO                       |
| REQ-FUN-305        | TEST-D-300             | YES                      |
| REQ-FUN-306        | TEST-D-300, TEST-D-301 | YES                      |
| REQ-FUN-310        | TEST-D-310             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | Under development             |
