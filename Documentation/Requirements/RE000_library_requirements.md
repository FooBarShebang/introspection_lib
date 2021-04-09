# Requirements for the Library introspection_lib

## Conventions

Requirements listed in this document are constructed according to the following structure:

**Requirement ID:** REQ-UVW-XYZ

**Title:** Title / name of the requirement

**Description:** Descriprion / definition of the requirement

**Verification Method:** I / A / T / D

The requirement ID starts with the fixed prefix 'REQ'. The prefix is followed by 3 letters abbreviation (in here 'UVW'), which defines the requiement type - e.g. 'FUN' for a functional and capability requirement, 'AWM' for an alarm, warnings and operator messages, etc. The last part of the ID is a 3-digits *hexadecimal* number (0..9|A..F), with the first digit identifing the module, the second digit identifing a class / function, and the last digit - the requirement ordering number for this object. E.g. 'REQ-FUN-112'. Each requirement type has its own counter, thus 'REQ-FUN-112' and 'REQ-AWN-112' requirements are different entities, but they refer to the same object (class or function) within the same module.

The verification method for a requirement is given by a single letter according to the table below:

| **Term**          | **Definition**                                                               |
| :---------------- | :--------------------------------------------------------------------------- |
| Inspection (I)    | Control or visual verification                                               |
| Analysis (A)      | Verification based upon analytical evidences                                 |
| Test (T)          | Verification of quantitative characteristics with quantitative measurement   |
| Demonstration (D) | Verification of operational characteristics without quantitative measurement |

## Functional and capability requirements

**Requirement ID:** REQ-FUN-000

**Title:** Function / method call stack and exception traceback analysis

**Description:** The library should provide functionality for the analysis of a function / method call stack as well as of an exception traceback as a wrapper around the standard library's module *inspect*. The goal is to facilitate the creation of a call chain (machine analysis) and of a human-readable frames info list. See document [RE001](./RE001_traceback_requirements.md).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-001

**Title:** Custom exceptions framework

**Description:** The library should provide a framework of custom exceptions, which are properly integrated into the structure of the standard exceptions and provide the extended version of the corresponding standard ones with the added human-readable traceback analysis functionality. See document [RE002](./RE002_base_exceptions_requirements.md).

---

**Requirement ID:** REQ-FUN-002

**Title:** Custom logger wrappers

**Description:** The library should provide a customized logger class preserving the **logging.Logger** API from the Standard Library but with the modified functionality: not only the minimum but the maximum severity level to log per handler as well as to propagate to the ancestors' handlers. See document [RE003](./RE003_logging_requirements.md).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-003

**Title:** Custom wrappers for Standard Library API for importing a module or a component of a module 'on demand'.

**Description:** The library should provide functions or classes (methods) to import a module or component 'on demand'. The Standard Library *importlib* already provides a function to import a module, which should be augmented with the input arguments sanity checks and import of a single compoent from a module. See document [RE004](./RE004_dynamic_import_requirements.md).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-004

**Title:** Unified access method for sequence, mapping and class objects.

**Description:** The library should provide functions or methods to get and set values of an sequence, mapping or class (instance) object, whith the object itself and the respective index, key or attribute name being passed as arguments. These functions should operate similar to the *getattribute*() and *setattr*() standard functions, but for the sequence and mapping type objects as well. The actual data access function or method should be selected automatically based on the type of the object and the second attribute (index, key or attribute name). An access to the direct 'end-node' element as well as nested element should be supported. See document [RE005](./RE005_universal_access_requirements.md).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-005

**Title:** Mapping of the objects.

**Description:** The library should provide functions or methods to:

* Construct JSON-encoding ready structure of an object concerning all (nested) element, which can be accessed for reading
* Construct JSON-encoding ready structure of an object concerning all (nested) element, which can be accessed for writing
* Perform data mapping from one (nested) structured object onto another one (nested) strucutured object

See documents [DE002](../Design/DE002_structure_map.md) and [RE006](./RE006_structure_map_requirements.md).

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-006

**Title:** Static inspection of dependencies.

**Description:** The library should provide functions or methods to:

* Construct a list of all unique 'top level' dependencies (stand alone module or root packages) directly imported by a module / script or all modules / scripts found in all sub-folders of a folder, with each (sub-) folder not necessarily being a package, whilst ignoring links.
* Construct a list of all unique dependencies (modules or (sub-) packages) directly imported by a module / script.
* Construct a dictionary of all dependencies (modules or (sub-) packages) directly imported by each module / script found in all sub-folders of a folder, with each (sub-) folder not necessarily being a package, whilst ignoring links. The paths to the modules relative to the 'root' folder should be the keys, and the values - lists of unique dependencies specific for that module / script.
* Construct a dictionary mapping the import names / aliases (visible in the local namespace of a module) to their fully qualified (dot notation) names, including the parent module and all parent packages.
* Construct a nested dictionary mapping the paths to the modules (relative to the 'root' folder) to the dictionaries mapping the import names / aliases (visible in the local namespace of each module) to their fully qualified (dot notation) names for all modules / scripts found in all sub-folders of a folder, with each (sub-) folder not necessarily being a package, whilst ignoring links.
* Determine if a 'top level' module or package is a system one, or it is already installed via pip, or it is located in some non-standard folder and is installed by other means, or it cannot be currently found.

The analysis should be completely static, no imports except for the system / standard modules are allowed. The determination if an import name / alias refers to a package, a module or a component within module should be based solely on the analysis of the file structure of the known *sys.path* entries. Relative imports should be resolved into the absolute ones.

See documents [DE003](../Design/DE003_package_structure.md) and [RE007](./RE007_package_structure_requirements.md).

**Verification Method:** T

## Installation and acceptance requirements

**Requirement ID:** REQ-IAR-000

**Title:** Python interpreter version

**Description:** The library should be used with Python 3 interpreter. The minimum version requirement is Python v3.6.

**Verification Method:** T

---

**Requirement ID:** REQ-IAR-001

**Title:** Operational system

**Description:** The library should work, at least, under MS Windows and GNU Linux operational systems. Ideally, it should not utilize any platform-specific functionality, therefore it should work under any OS, for which Python 3 interpreter is available.

**Verification Method:** T

---

**Requirement ID:** REQ-IAR-002

**Title:** System requirements check

**Description:** The library should provide a module / script to check if all system requirements are met, i.e. the Python interpreter version, other required libraries / packages presence as well as their versions. This module / script should report the missing requriements.

**Verification Method:** T
