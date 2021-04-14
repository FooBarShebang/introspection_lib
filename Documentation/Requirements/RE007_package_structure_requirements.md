# RE007 Requirements for the Module package_structure

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Description / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requirement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-700

**Title:** Static analysis of a Python module or folder with Python modules concerning the dependencies and import names / aliases.

**Description:** The module should provide functionality to statically analize the source code in order to map (per module) the import names / aliases local to that module namespace to their fully qualified (dot notation) names, as in *package* or *module*, *package.subpackage* or *package.module*, *package.subpackage.module.component* or *package.module.component* or *module.component*, etc. It should also provide functionality to retrieve the qualified names of all modules to be imported (per module in the analyzed folder and all its sub-folders recursively), and list of all 'top level' imports (stand-alone modules or 'roots' of the packages). All this data should be retrived based on the source code analysis of the modules in the folder being analyzed, but not involving the recursive source code analysis of the found 'direct' dependencies. Nor the modules being analyzed, neither their dependencies should be imported.

**Verification Method:** A

---

**Requirement ID:** REQ-FUN-710

**Title:** Check if a path refers to a source code file.

**Description:** The module should provide function, which should return **True** if a passed path refers to an actual, existing Python source file, but not a link to such a file; otherwise it should return **False**. This function should accept only a string argument.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-720

**Title:** Check if a path refers to a Python package.

**Description:** The module should provide function, which should return **True** if a passed path refers to an actual, existing Python package (a folder, containing *\_\_init\_\_.py* modules), but not a link to such a folder; otherwise it should return **False**. This function should accept only a string argument.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-730

**Title:** Find all Python source files in a folder.

**Description:** The module should provide function, which should return a list of the base filenames of all actual (not symlinks) Python source files found in a folder, but not in its sub-folders. If the folder itself is a symlink, or it does not exist, or there are no actual Python source files within it, the returned value should be an empty string. This function should accept only a string argument.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-740

**Title:** Determine the fully qualified module or (sub-) package name.

**Description:** The module should provide function, which should return a string representing the fully qualified (dot notation) name of a Python module or (sub-) package, or **None** value, if it is not a Python module or package. In case of the passed path to a Python module or (sub-) package, the passed path should be traversed upward, until a parent folder found, which is not a Python package. The dot connected string name should be constructed from the top-most found package downwards. In case of the stand-alone modules, the name should be only the base filename of the module, with the '.py' extension removed. This function should accept only a string argument.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-750

**Title:** Coonvertion of relative imports.

**Description:** The module should provide function, which accepts a path to the actual Python source file (not a symlink) and a relative or absolute import path. If the passed import path is absolute it should be returned regardless of the value of the file path, even if it is not a path to an actual Python source file. If the passed import path is relative, the file path must point to an actual source file, and the relative path must point to inside the 'root' package of that file, otherwise the value check has failed. The relative import path should be converted to an absolute one, starting from the 'root' package. This function should accept only two string arguments.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-760

**Title:** Package dependencies analysis.

**Description:** The module should provide a class, which is instantiated with a path to a Python package; and which can automatically find all Python source files within all its sub-folder, even if those subfolders are not sub-packages - and all 'top level' dependencies found in the import statements in those source files (see DE003 document). By default, all modules and sub-folders related to the packaging using **setuptools** should be ignored. Non-string argument passed is considred to be a *type error*, whereas not a path to a package string - *value error*.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-761

**Title:** Package structure analysis - import names.

**Description:** This class should also produce a look-up table of the correspondence of the local (per module) import names to the fully qualified names of the imported object, supporting the relative import.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-762

**Title:** Package structure analysis - filtering.

**Description:** This class should also provide methods to modify the sub-folders and Python modules base filenames filters: extend, reduce or replace the filter patterns using Unix shell-style wildcards or exact match strings. The modification of the filter should has immeditate effect on the dependencies and import names analysis.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-763

**Title:** Package structure analysis - names of the packaging sub-packages.

**Description:** This class should also provide method to generate a list of all sub-packages to be included into the distribution, assuming that the package itself is to be made into 'top level', even if it is a sub-package of another one.

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-700

**Title:** Wrong type of the arguments.

**Description:** All functions / methods defined in the module should raise an excepton of (sub-) class of **TypeError** if the passed argument doesn't meet the expected data type limitation. E.g., a function requiring a string input receieves an integer as the argument.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-701

**Title:** Wrong value of the arguments.

**Description:** All functions / methods defined in the module and performing data value checks should raise an excepton of (sub-) class of **ValueError** if the passed argument doesn't meet the expected data value limitation. E.g., a relative path pointing outside the 'root' package for this module.

**Verification Method:** T
