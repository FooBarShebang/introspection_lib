# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* global requirements - 00x
* module **traceback** - 1xx
  * class *StackTraceback* - 10x
  * class *ExceptionTraceback* - 11x
* module **base_exceptions** - 2(0|1|2)x
  * common requirements for all classes - 20x
  * class *UT_Exception* specific - 210
  * class *UT_TypeError* specific - 220
  * class *UT_ValueError* specific - 230
  * class *UT_AttributeError* specific - 240
  * class *UT_IndexError* specific - 250
  * class *UT_KeyError* specific - 260
* module **logging** - 30x

## Requirements vs Tests Traceability

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-000        | TEST-T-000             | YES                      |
| REQ-FUN-001        | TEST-T-003             | YES                      |
| REQ-FUN-002        | TEST-T-004             | NO                       |
| REQ-IAR-000        | TEST-T-001             | YES                      |
| REQ-IAR-001        | TEST-T-002             | YES                      |
| REQ-IAR-002        | TEST-T-001             | YES                      |
| REQ-FUN-100        | TEST-T-100             | YES                      |
| REQ-FUN-101        | TEST-T-101             | YES                      |
| REQ-FUN-102        | TEST-T-100             | YES                      |
| REQ-FUN-103        | TEST-A-100             | YES                      |
| REQ-FUN-110        | TEST-T-110             | YES                      |
| REQ-FUN-111        | TEST-T-111             | YES                      |
| REQ-FUN-112        | TEST-T-110             | YES                      |
| REQ-FUN-113        | TEST-A-100             | YES                      |
| REQ-FUN-114        | TEST-T-112             | YES                      |
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
| NO                                           | Under development             |
