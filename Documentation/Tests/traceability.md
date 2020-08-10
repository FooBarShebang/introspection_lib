# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* global requirements - 00x
* module **traceback** - 1xx
  * class *StackTraceback* - 10x
  * class *ExceptionTraceback* - 11x

## Requirements vs Tests Traceability

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-000        | TEST-T-000             | YES                      |
| REQ-IAR-000        | TEST-T-001             | YES                      |
| REQ-IAR-001        | TEST-T-002             | YES                      |
| REQ-IAR-002        | TEST-T-001             | YES                      |
| REQ-FUN-100        | TEST-T-100             | YES                      |
| REQ-FUN-101        | TEST-T-101             | YES                      |
| REQ-FUN-102        | TEST-T-100             | YES                      |
| REQ-FUN-110        | TEST-T-110             | YES                      |
| REQ-FUN-111        | TEST-T-111             | YES                      |
| REQ-FUN-112        | TEST-T-110             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| YES                                          | All tests are passed          |
