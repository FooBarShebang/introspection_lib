# RE006 Requirements for the Module structure_map

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

**Requirement ID:** REQ-FUN-600

**Title:** Creation of a map of a ((nested) structured) object

**Description:** The module should provide functionality to traverse an arbitrary Python object: from a scalar to a nested strucutured type (container or mapping type) to a nested C-struct like class instances - and produce a map of the object structure including the values of its end-nodes. The created map should be in the JSON-encoding ready format stored:

* Scalar types: integer, floating point, strings, boolean, None - should be presented 'as is'
* Any sequence type, except for the named tuples, should be represented by a list
* Any mapping type, named tuples and generic class instances should be represented by ordered dictionaries, preserving the keys order (if the keys are ordered in the source object)
* Any callable types (except for properties) should be ignored
* These rules are applied recursively to the nested elements

See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-601

**Title:** Read- and write-access maps

**Description:** Two modes of operation should be supported considering the creation of the object structure map - all read-accessible nodes and all write-accessible nodes. See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-602

**Title:** Mapping structure of class instances

**Description:** Only properties and the attributes storing non-callable values (not methods) should be considered. Attributes with the names starting with, at least, one underscore should be ignored ('private', magic and name mangling attributes). See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-610

**Title:** Read-mapping of sequences

**Description:** The structure of any mutable or immutable sequence, except for the named tuples, should be represented by a list containing only JSON-encoding ready elements (recursive application of the rules) and preserving the original order of the elements. See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-611

**Title:** Read-mapping of mapping types and named tuples

**Description:** The structure of any mutable or immutable sequence and named tuple should be represented by an ordered dictionary containing only JSON-encoding ready elements (recursive application of the rules) and preserving the original order of the entries, if the original object is ordered. See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-612

**Title:** Read-mapping of class instances

**Description:** The structure of any class instance should be represented by an ordered dictionary containing only JSON-encoding ready elements (recursive application of the rules), with the following limitations:

* The name of an attribute cannot begin with an underscore
* An attribute can be either a property with the getter method defined, or it can store any scalar value, any sequence, mapping type or an instance of a class
* Other callable attributes except for properties, i.e. methods or stored references to functions should be ignored
* The standard attributes resolution scheme is applied, considering MRO and 'shadowing' of the names
  * Instance attributes, stored in the local slots or internal dictionary
  * Class attributes defined in this class
  * Class attributes inherited from the super classes

See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-620

**Title:** Write-mapping of sequences

**Description:** The structure of any mutable or immutable sequence, except for the named tuples, should be represented by a list containing only JSON-encoding ready elements (recursive application of the rules) and preserving the original order of the elements. Additional limitations are applied to the immutable sequences:

* Immutable sequences containing only scalar elements or nested immutable sequences, immutbale mapping types or class instances without write-accessible end-nodes should be represented by an empty list
* Immutable sequences containing, at least, one nested structured element with write-accessible end-node should be represented by a list of the same length as the initial sequence with all immutable elements being replaced by a special value "!@#immutable"

See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-621

**Title:** Write-mapping of mapping types and named tuples

**Description:** The structure of any mutable or immutable sequence and named tuple should be represented by an ordered dictionary containing only JSON-encoding ready elements (recursive application of the rules) and preserving the original order of the entries, if the original object is ordered.

* Immutable mapping types and named tuples containing only scalar elements or nested immutable sequences, immutbale mapping types or class instances without write-accessible end-nodes should be represented by an empty ordered dictionary
* Immutable mapping types and named tuples containing, at least, one nested structured element with write-accessible end-node should be represented by an ordered dictionary with the same keys as the original object with all immutable values being replaced by a special value "!@#immutable"

See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-622

**Title:** Write-mapping of class instances

**Description:** The structure of any class instance should be represented by an ordered dictionary containing only JSON-encoding ready elements (recursive application of the rules), with the following limitations:

* The name of an attribute cannot begin with an underscore
* An attribute can be either a property with the setter method defined, or it can store any scalar value, any sequence, mapping type or an instance of a class
* Other callable attributes except for properties, i.e. methods or stored references to functions should be ignored
* The modified attributes resolution scheme is applied
  * Instance attributes, stored in the local slots or internal dictionary
  * Setter properties defined in this class or inherited from the super classes, considering MRO and 'shadowing' of the names

See [DE002](../Design/DE002_structure_map.md) document.

**Verification Method:** T

---
