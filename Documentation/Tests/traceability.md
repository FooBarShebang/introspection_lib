# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* global requirements - 00x
* module **my_traceback** - 1xx
  * class *StackTraceback* - 10x
  * class *ExceptionTraceback* - 11x
* module **base_exceptions** - 2xx
  * common requirements for all classes - 20x
  * class *UT_Exception* specific - 210
  * class *UT_TypeError* specific - 220
  * class *UT_ValueError* specific - 230
  * class *UT_AttributeError* specific - 240
  * class *UT_IndexError* specific - 250
  * class *UT_KeyError* specific - 260
* module **my_logging** - 3xx
  * class *DualLogger* specific - 30x
  * class *DummyLogger* specific - 310
* module **dynamic_import** - 4xx
* module **universal_access** - 5xx
  * common requirements for all functions, including *FlattenPath*() - 50x
  * function *GetData*() - 510
  * function *GetDataDefault*() - 520
  * function *SetData*() - 530
  * function *SetDataStrict*() - 540
  * function *GetElement*() - 550
  * function *SetElement*() - 560
* module **structure_map** - 6xx
  * common requirements for all functions - 60x
* module **package_structure** - 7xx
  * common requirements for all functions - 70x
  * function *IsPyFile*() - 710
  * function *IsPyPackage*() - 720
  * function *SelectPySourceFiles*() - 730
  * function *GetQualifiedName*() - 740
  * function ResolveRelativeImport() - 750
  * class **PackageStructure** - 76x

## Requirements vs Tests Traceability

| **Requirement ID** | **Covered in test(s)**                                                             | **Verified \[YES/NO\]**  |
| :----------------- | :--------------------------------------------------------------------------------- | :----------------------- |
| REQ-FUN-000        | TEST-T-000                                                                         | YES                      |
| REQ-FUN-001        | TEST-T-003                                                                         | YES                      |
| REQ-FUN-002        | TEST-T-004                                                                         | YES                      |
| REQ-FUN-003        | TEST-T-005                                                                         | YES                      |
| REQ-FUN-004        | TEST-T-006                                                                         | YES                      |
| REQ-FUN-005        | TEST-T-007                                                                         | NO                       |
| REQ-FUN-006        | TEST-T-008                                                                         | YES                      |
| REQ-IAR-000        | TEST-T-001                                                                         | YES                      |
| REQ-IAR-001        | TEST-T-002                                                                         | YES                      |
| REQ-IAR-002        | TEST-T-001                                                                         | YES                      |
| REQ-FUN-100        | TEST-T-100                                                                         | YES                      |
| REQ-FUN-101        | TEST-T-101                                                                         | YES                      |
| REQ-FUN-102        | TEST-T-100                                                                         | YES                      |
| REQ-FUN-103        | TEST-A-100                                                                         | YES                      |
| REQ-FUN-110        | TEST-T-110                                                                         | YES                      |
| REQ-FUN-111        | TEST-T-111                                                                         | YES                      |
| REQ-FUN-112        | TEST-T-110                                                                         | YES                      |
| REQ-FUN-113        | TEST-A-100                                                                         | YES                      |
| REQ-FUN-114        | TEST-T-112                                                                         | YES                      |
| REQ-FUN-200        | TEST-T-100                                                                         | YES                      |
| REQ-FUN-201        | TEST-T-201                                                                         | YES                      |
| REQ-FUN-202        | TEST-T-202                                                                         | YES                      |
| REQ-FUN-203        | TEST-D-200                                                                         | YES                      |
| REQ-FUN-204        | TEST-T-203                                                                         | YES                      |
| REQ-FUN-205        | TEST-T-204                                                                         | YES                      |
| REQ-FUN-210        | TEST-T-210                                                                         | YES                      |
| REQ-FUN-220        | TEST-T-220                                                                         | YES                      |
| REQ-FUN-230        | TEST-T-230                                                                         | YES                      |
| REQ-FUN-240        | TEST-T-240                                                                         | YES                      |
| REQ-FUN-250        | TEST-T-250                                                                         | YES                      |
| REQ-FUN-260        | TEST-T-260                                                                         | YES                      |
| REQ-FUN-300        | TEST-D-300                                                                         | YES                      |
| REQ-FUN-301        | TEST-D-302, TEST-D-304                                                             | YES                      |
| REQ-FUN-302        | TEST-D-303, TEST-D-304                                                             | YES                      |
| REQ-FUN-303        | TEST-D-300                                                                         | YES                      |
| REQ-FUN-304        | TEST-D-303, TEST-D-304                                                             | YES                      |
| REQ-FUN-305        | TEST-D-300                                                                         | YES                      |
| REQ-FUN-306        | TEST-D-300, TEST-D-301                                                             | YES                      |
| REQ-FUN-307        | TEST-D-300                                                                         | YES                      |
| REQ-FUN-310        | TEST-D-310                                                                         | YES                      |
| REQ-FUN-400        | TEST-T-400                                                                         | YES                      |
| REQ-FUN-401        | TEST-T-401                                                                         | YES                      |
| REQ-FUN-410        | TEST-T-410                                                                         | YES                      |
| REQ-FUN-411        | TEST-T-411                                                                         | YES                      |
| REQ-FUN-420        | TEST-T-400, TEST-401, TEST-T-410, TEST-T-411                                       | YES                      |
| REQ-FUN-421        | TEST-T-400, TEST-401, TEST-T-410, TEST-T-411                                       | YES                      |
| REQ-AWM-400        | TEST-T-402, TEST-T-412                                                             | YES                      |
| REQ-AWM-401        | TEST-T-403, TEST-T-413                                                             | YES                      |
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
| REQ-FUN-710        | TEST-T-710                                                                         | YES                      |
| REQ-FUN-720        | TEST-T-720                                                                         | YES                      |
| REQ-FUN-730        | TEST-T-730                                                                         | YES                      |
| REQ-FUN-740        | TEST-T-740                                                                         | YES                      |
| REQ-FUN-750        | TEST-T-750                                                                         | YES                      |
| REQ-FUN-760        | TEST-T-760                                                                         | YES                      |
| REQ-FUN-761        | TEST-T-760                                                                         | YES                      |
| REQ-FUN-762        | TEST-T-761                                                                         | YES                      |
| REQ-FUN-763        | TEST-T-760                                                                         | YES                      |
| REQ-FUN-764        | TEST-T-760                                                                         | YES                      |
| REQ-AWM-700        | All TEST-T-7x0, TEST-T-761                                                         | YES                      |
| REQ-AWM-701        | TEST-T-750, TEST-T-760                                                             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**                 |
| :------------------------------------------: | :---------------------------- |
| NO                                           | Under development             |
