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

**Requirement ID(s)**: REQ-FUN-300, REQ-FUN-303, REQ-FUN-305, REQ-FUN-306 and REQ-FUN-307.

**Verification method:** D

**Test goal:** Basic functionality, API and message propagation of a dual logger class.

**Expected result:** A dual logger class can be instantiated, and attached 'children' loggers can be created. Own file log can be attached to any of the chained loggers. With the default settings any of the chained loggers handles any level of the log message severity from DEBUG to CRITICAL; with any message being printed into the console only once, whereas it is added into the own log file (if attahced) as well as into any parents' log files up to the root of the hierarchy, but not into the log files of its siblings.

**Test steps:** Instantiate a dual class logger, create its 'child' logger and two 'grand-children' loggers. Leave the default settings of the logger instances, but attach own log files to each of the logger - do not specify the names, i.e. automatic log files names should be created. Issue all level messages from DEBUG to CRITICAL with each of the loggers in turn. Use the prepared module [DT002_logging_default](../../Tests/DT002_logging_default.py). Analyze the console output and the content of the created log files. Check the structure of the enties, if it satisfies the REQ-FUN-307, i.e. has all the required fields.

**Test result:** PASS

---

**Test Identifier:** TEST-D-301

**Requirement ID(s)**: REQ-FUN-306.

**Verification method:** D

**Test goal:** Manual rotation of the log files.

**Expected result:** A dual logger class can be instantiated, and attached 'children' loggers can be created. Own file log can be attached to any of the chained loggers. With the default settings any of the chained loggers handles any level of the log message severity from DEBUG to CRITICAL; with any message being printed into the console only once, whereas it is added into the own log file (if attahced) as well as into any parents' log files up to the root of the hierarchy, but not into the log files of its siblings.

**Test steps:** Instantiate a dual class logger, create its 'child' logger and two 'grand-children' loggers. Leave the default settings of the logger instances, but attach own log file to the 'root' logger. Issue info log message with the child logger. Try to disbale the file logging of the child logger - nothing should happen, then issue info log message with the child logger. Attach own log file to the child logger and issue a message. Switch to another file with the child logger and issue a message. Switch back to the original file of the child logger and issue another message. Disable file logging of the both loggers and issue the last message. Use the prepared module [DT003_logging_files](../../Tests/DT003_logging_files.py). Analyze the console output and the content of the created log files.

**Test result:** PASS

---

**Test Identifier:** TEST-D-302

**Requirement ID(s)**: REQ-FUN-301.

**Verification method:** D

**Test goal:** Application of the logger's severity level to the own messages and those received from the children.

**Expected result:** Any logger along the message propagation chain issues only the messages with the severity level above its own threshold, but handles and propagates further to its parent all messages received from its children. If this logger has an attached handler (without filters / severity level limitations), this handler logs all messages issued by this logger as well as all messages received from the children of this logger. Since there is only one console handler, all messages issued by any of the loggers. The log file attached to any logger should contained all messages issued by this logger and all of its children, but not of the loggers higher in the chain.

**Test steps:** Instantiate a dual class logger, create its 'child' logger and two 'grand-children' loggers. Attach own log file to each of the loggers with the defined file names. Set the top level logger to ERROR level, the middle logger to WARNING level, and the bottom level loggers - to INFO level. Issue all level messages from DEBUG to CRITICAL with each of the loggers in turn. Use the prepared module [DT004_logging_logger_level](../../Tests/DT004_logging_logger_level.py).
Analyze the console output and the content of the created log files. Only ERROR and CRITICAL messages from the top level logger should be printed out as well as logged into the top level log file. Only WARNING, ERROR and CRITICAL messages from the middle level logger should be printed out as well as logged into the top level and middle level log files. For the bottom level loggers only the DEBUG level messages are ignored, other messages are printed out into the console as well as logged into the top and middle level log files, and into the log file attached to this logger, but not the log file of its sibling. In the console, each message appears only once.

**Test result:** PASS

---

**Test Identifier:** TEST-D-303

**Requirement ID(s)**: REQ-FUN-302 and REQ-FUN-304.

**Verification method:** D

**Test goal:** Application of the handlers filters and propagation filter.

**Expected result:** Without threshold levels set to any of the loggers, any message issued by any of the loggers is printed into the console only once and only if its level is within the range defined by the logger issued it. The file logging handlers should log a message issued by the logger this handler is attached, but only if the message's level is within the range defined for this handler. Considering the messages received from the children of the logger, the message's level must be within the acceptable values range of the handler, and the range of the values allowed for the upward propagation defined by the logger which issued this message.

**Test steps:** Instantiate a dual class logger, create its 'child' logger and two 'grand-children' loggers. Attach own log file to each of the loggers with the defined file names. Set the console and file handler filters of the top level to >= ERROR, and of the middle level logger - from INFO to WARNING. Set the console filter of the bottom level loggers to from INFO to WARNING, and the file handlers - to <= DEBUG. Set the propagation filter to >= WARNING for the the middle level logger, and <= ERROR for the bottom level loggers. Leave other settings at their default values. Issue all level messages from DEBUG to CRITICAL with each of the loggers in turn. Use the prepared module [DT005_logging_handler_level](../../Tests/DT005_logging_handler_level.py).
Analyze the console output and the content of the created log files. Only ERROR and CRITICAL messages from the top level logger are printed out and logged into the top level file, others are ignored. The DEBUG messages from the middle level logger are ignored; INFO and WARNING - printed into the console and logged into its own file; ERROR and CRITICAL - only logged into the top level log file. For the bottom level loggers the DEBUG level messages are only logged into their own files; INFO and WARNING - are printed out and logged into the middle level log file; ERROR - only logged into the top level file, and CRITICAL - ignored. In the console, each message appears only once.

**Test result:** PASS

---

**Test Identifier:** TEST-D-304

**Requirement ID(s)**: REQ-FUN-301, REQ-FUN-302 and REQ-FUN-304.

**Verification method:** D

**Test goal:** Combination of the loggers' thresholds and handlers and propagation filters.

**Expected result:** The severity threshold level of a logger defines the minimum level of a message, which can be issued by this logger, but doen not affect the propagation. Any message issued by any of the loggers is printed into the console only once and only if its level is within the range defined by the logger issued it. The file logging handlers should log a message issued by the logger this handler is attached, but only if the message's level is within the range defined for this handler. Considering the messages received from the children of the logger, the message's level must be within the acceptable values range of the handler, and the range of the values allowed for the upward propagation defined by the logger which issued this message.

**Test steps:** Instantiate a dual class logger, create its 'child' logger and two 'grand-children' loggers. Attach own log file to each of the loggers with the defined file names. Set the top level logger to NONE level, the middle logger to INFO level, and the bottom level loggers are left at the default (ALL) level. Set file handler filter of the top level to >= WARNING, middle level logger - from INFO to WARNING, and of the bottom level loggers - to <= DEBUG. Set the propagation filter to >= WARNING for the the middle level logger, and >= INFO for the bottom level loggers. Set the console output filter to from INFO to WARING for the bottom level loggeres. Leave other settings at their default values. Issue all level messages from DEBUG to CRITICAL with each of the loggers in turn. Use the prepared module [DT006_logging_both_levels](../../Tests/DT006_logging_both_levels.py).
Analyze the console output and the content of the created log files. All messages from the top logger should be ignored. The DEBUG message from the middle logger should be ignored; INFO and WARNING - printed into the console as well as logged into its own file; ERROR and CRITICAL - printed into the console and logged into the top logger's file. For the bottom level loggers, the DEBUG messages should be logged only into their own log files (not into sibling's file!); INFO and WARNING messages - printed into the console and logged into the middle level logger's file; ERROR and CRITICAL - only logged into the top level log file. In the console, each message appears only once.

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
| REQ-FUN-301        | TEST-D-302, TEST-D-304 | YES                      |
| REQ-FUN-302        | TEST-D-303, TEST-D-304 | YES                      |
| REQ-FUN-303        | TEST-D-300             | YES                      |
| REQ-FUN-304        | TEST-D-303, TEST-D-304 | YES                      |
| REQ-FUN-305        | TEST-D-300             | YES                      |
| REQ-FUN-306        | TEST-D-300, TEST-D-301 | YES                      |
| REQ-FUN-307        | TEST-D-300             | YES                      |
| REQ-FUN-310        | TEST-D-310             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | All tests are passed          |
