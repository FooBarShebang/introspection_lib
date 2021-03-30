# RE004 Requirements for the Module introspection_lib.universal_access

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

**Requirement ID:** REQ-FUN-500

**Title:** Support for 'nested' component path definition

**Description:** The module should provide functionality to traverse nested structure or container objects using 'nested' component path definition, which can be a string, an integer or a (nested) sequence with the 'end-elements' being strings or integers. Any string in such a path can contain 'dot-notation', i.e. sub-strings separated by a dot should be considered as 'identifiers' (keys or attribute names) of respective nesting levels components. See [DE001](../Design/DE001_element_path.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-501

**Title:** Treatment of named tuples

**Description:** The named tuples should be treated both as immutable sequences with index access and as immutable struct-like objects with access by attribute name.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-510

**Title:** Universal 'strict read' access to a sequence element, mapping object entry or attribute of a class or instance

**Description:** The module should provide function, that implements a universal 'strict read' access to an existed sequence element (by integer index), mapping object entry (by string key) or attribute of a class or instance (by string name), with both the object and the 'identifier' of the its component being passed as arguments. If such component is not found an exception should be raised.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-520

**Title:** Universal 'relaxed read' access to a sequence element, mapping object entry or attribute of a class or instance

**Description:** The module should provide function, that implements a universal 'relaxed read' access to a sequence element (by integer index), mapping object entry (by string key) or attribute of a class or instance (by string name), with both the object and the 'identifier' of the its component being passed as arguments. If such component is not found the default value should be returned, which also must be passed as an argument.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-530

**Title:** Universal 'relaxed write' access to a sequence element, mapping object entry or attribute of a class or instance

**Description:** The module should provide function, that implements a universal 'strict write' access to an existed mutable sequence element (by integer index), mutable mapping object entry (by string key) or attribute of a class or instance (by string name), with both the object and the 'identifier' of the its component as well as the value to assign being passed as arguments. If such component is not found, it must be created. Write access to a component of immutable object must result in an exception.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-540

**Title:** Universal 'strict write' access to a sequence element, mapping object entry or attribute of a class or instance

**Description:** The module should provide function, that implements a universal 'strict write' access to an existed mutable sequence element (by integer index), mutable mapping object entry (by string key) or attribute of a class or instance (by string name), with both the object and the 'identifier' of the its component as well as the value to assign being passed as arguments. If such component is not found, or it is immutable an exception should be raised. Write access to a component of immutable object must result in an exception.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-550

**Title:** Universal 'read' access to a nested component

**Description:** The module should provide function, that implements a universal 'read' access to a nested component of a container or structured object using the generic 'nested' path definition (see REQ-FUN-500), with the object and such path being passed as arguments. This function should support two modes of operation: 'strict' and 'relaxed'. In the 'strict' mode an exception must be raised if a specific nested component along the path does not exist. In the 'relaxed' mode a default value must be returned if a specific nested component along the path does not exist.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-560

**Title:** Universal 'write' access to a nested component

**Description:** The module should provide function, that implements a universal 'write' access to a nested component of a container or structured object using the generic 'nested' path definition (see REQ-FUN-500), with the object and such path being passed as arguments as well as the value to assign. This function should support two modes of operation: 'strict' and 'relaxed'. In the 'strict' mode an exception must be raised if a specific nested component along the path does not exist. In the 'relaxed' mode the missing sub-path must be created using nesting of dictionaries and lists to satisfy the entire path, unless the last currently found component (to which a new branch must be attached) is immutable.

**Verification Method:** T

## Alarms, warnings and operator messages

**Requirement ID:** REQ-AWM-500

**Title:** Improper defined path

**Description:** An exception compatible with **TypeError** must be raised if

* Any 'end-element' of a 'nested' path definition or a 'simple' path (single not nested element) is not an integer or a string
* 'Nested' path definition contains any other types apart from an integer, a string or a (nested) sequence of stings and integers
* Mis-match of the current level object type and the path element type:
  * Current level object is a sequence (but not a named tuple), but the path element to be accessed is a string
  * Current level object is a not a sequence, but the path element to be accessed is an integer

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-501

**Title:** Empty path

**Description:** An exception compatible with **ValueError** must be raised if the passed 'simple' or 'nested' path definition is reduced to an empty list in the canonical form.

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-502

**Title:** Modification of an immutable object

**Description:** An exception compatible with **TypeError** must be raised if the 'write' access functionality requires modification of an immutable object

**Verification Method:** T

---

**Requirement ID:** REQ-AWM-503

**Title:** Non-existing component access in the 'strict' mode

**Description:** Both 'read' and 'write' access functions in the 'strict' mode must raise:

* **IndexError** compatible - index out of range for a sequence object (first occured error along the path)
* **KeyError** compatible  key is not found in a mapping object (first occured error along the path)
* **AttributeError** compatible - attribute is not present in a class or instance object (first occured error along the path)

**Verification Method:** T
