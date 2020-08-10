# Requirements for the Module introspection_lib.traceback

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

**Requirement ID:** REQ-FUN-100

**Title:** Normal function or method call chain

**Description:** The module should provide a function or class method, which will return the entire call chain from the main module or interactive console to the place (stack frame) where this function or method is called. The call chain should be in the human readable form, but it should be also easy to process by a machine code, e.g. a sequence (list, tuple, etc.) of the fully qualified names of the functions and methods along the chain, i.e. *module.function* or *module.class.method*. The top level frame (bottom of the stack) shold be the first element, whereas the current frame (top of the stach) should be the last element in that sequence.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-101

**Title:** Detailed frame information on the normal call chain

**Description:** The module should provide a function or class method, which will return the human readable digest on the involved frames for the entire call chain from the main module or interactive console to the place (stack frame) where this function or method is called. The order of the frames should be the same as for the call chain function / method. For each frame the following information must be provided: filename of the module, fully qualified name of the 'caller' (function / method), line number in the source code where this call is made, and the source code sniplet around the line in question. The entire number of the source code lines shown for each frame should be adjustable. The shown source code lines should be truncated to the specific length, which should be adjustable. The returned value (call chain frames information) should be in the form of a multi-line string.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-102

**Title:** Length of the call chain stack trace

**Description:** Both functions / methods (simple call chain and detailed stack frames information) should allow 'hidding' of the specificed number of the latest (topmost) 'callers' in the chain.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-110

**Title:** Exception traceback

**Description:** The module should provide a function or class method, which will return the entire call chain, which led to a caught exception. For instance, *function1* calls *function2* within **try... except**, which calls *function3*, which raises an exception, which is caught in the *function1*. Thus the call chain is *function1* -> *function2* -> *function3*. The call chain should be in the human readable form, but it should be also easy to process by a machine code, e.g. a sequence (list, tuple, etc.) of the fully qualified names of the functions and methods along the chain, i.e. *module.function* or *module.class.method*. The frame where the exception is caught shold be the first element, whereas the frame where it is raised should be the last element in that sequence.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-111

**Title:** Detailed frame information on the exception traceback

**Description:** The module should provide a function or class method, which will return the human readable digest on the involved frames for the entire exception traceback. The order of the frames should be the same as for the call chain function / method. For each frame the following information must be provided: filename of the module, fully qualified name of the 'caller' (function / method), line number in the source code where this call is made or exception is raised, and the source code sniplet around the line in question. The entire number of the source code lines shown for each frame should be adjustable. The shown source code lines should be truncated to the specific length, which should be adjustable. The returned value (call chain frames information) should be in the form of a multi-line string.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-112

**Title:** Length of the exception stack trace

**Description:** Both functions / methods (simple call chain and detailed stack frames information) should allow 'hidding' of the specificed number of the latest (bottom-most, closest to the place, where the exception is raised) 'callers' in the chain.

**Verification Method:** T
