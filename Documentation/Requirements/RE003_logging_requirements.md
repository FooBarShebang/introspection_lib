# Requirements for the Module introspection_lib.logging

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

**Requirement ID:** REQ-FUN-300

**Title:** Standard API of the custom logger class

**Description:** The custom logger class should preserve the API of the standard logger (Standard Library *logging*), i.e. provide all methods / public attributes of the standard logger with the same signatures; the added functionality should be implemented via new methods and attributes. It is allowed to change the signature of the initialization method, since this class should be instantiated expliciptly, not via *getLogger*() function. It is also allowed to add keyword arguments to the existing methods.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-301

**Title:** Severity level of the logger object.

**Description:** The logging (severity) level of the logger object itself should affect only the minimum request level, upon which this specific logger object emmits a log message, which should be then passed to the handlers attached to this logger as well as passed up to its ancestor logger (unless specified otherwise, see REQ-FUN-304). The level of the logger should not interfere with the log messages propagation / delegation scheme: a message received from a descendant logger should be passed to the handlers attached to this logger and than to this logger's ancestor logger regardless of the level of the received message.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-302

**Title:** Severity level of the handlers attached to the logger object.

**Description:** A handler attached to a logger object can reject a message received: either from this logger object itself or from its descendant loggers - if the level of the message is below the severity level of the handler - as the standard functionality. However, it should also be possible to define the maximum level of the message accepted and handled by this handler. The rejection or acception of a message by a handler should not affect the further message's propagation up the ancestors loggers.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-303

**Title:** Logging to the different streams / files.

**Description:** A logger should be able to send messages to a console and / or own log file and / or a log file of one of its ancestors. A logger can use any combination of these 3 output channels (1, any 2 of them, or all 3 simultaneously), but to use, at least, 1 output channel, otherwise such a logger is useless.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-304

**Title:** Preventing or allowing generated message propagation to the ancestor logger.

**Description:** If a logger generates a message, it may propagate or not this message to the ancestor logger class based on the message's level and a predefined min-max range. The handlers of the ancestor loggers should output this message only if its level is whithin the levels range defined by the logger issued this message **and** whithin the acceptance levels range of the handler in question.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-305

**Title:** Preventing doubling of messages in the console output.

**Description:** Although the same message is allowed to be logged in the different files as it propagates up the ancestor loggers, if it is printed into the console, it should be printed out only once.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-306

**Title:** Rotation of the log file.

**Description:** By default, a logger object has no own file handler attached, however the user can initiate the file's logging at the runtime. If the log file name is not specified explicitely, it should be created automatically from the date-time stamp and the logger's name. The user should be able to switch to another log file (new or existing), which should be openned in the attach mode (not overwritten). The user should be able to disable the logging into a file at any time.

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-310

**Title:** 'Dummy' logger class.

**Description:** A 'dummy' logger should be also implemented, wich provides the standard API of a logger class: logging at the different levels of severity, changing the severity threshold level of the logger itself - but simply dumps everything into NIL-stream. With such a 'dummy' logger passed or defined as a default value a client method / function can always issue log messages without checking. The user of such a method / function can pass a real logger object with the defined severity logging levels when required.

**Verification Method:** D
