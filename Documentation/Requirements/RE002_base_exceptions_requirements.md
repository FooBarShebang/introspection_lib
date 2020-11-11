# Requirements for the Module introspection_lib.base_exceptions

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

**Requirement ID:** REQ-FUN-200

**Title:** Integration of the custom exceptions into the standard exceptions' tree structure

**Description:** The custom exceptions should sub-class the respective standard exceptions: **Exception**, **AttributeError**, **IndexError**, **KeyError**, **ValueError** and **TypeError** - and be in the same relation to each other as their parent exceptions. E.g. a custom version of **TypeError** as **UT_TypeError** should be considered being a sub-class of **TypeError** and **Exception** as well as **UT_Exception** (as direct child of **Exception**), but not of the **ValueError**, **AttributeError**, **IndexError** and **KeyError** as well as of their sub-classes.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-201

**Title:** Extended introspection functionality

**Description:** The custom exceptions should inherit the traceback inspection functionality of the standard exceptions, i.e. proper handling of the special instance attribute \_\_*traceback*\_\_, but also include a read-only property *Traceback*, which should reference an instance of **introspection_lib.traceback.ExceptionTraceback** class, thus the exception traceback can be easily analyzed as *SomeException.Traceback.CallChain* and *SomeException.Traceback.Info*.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-202

**Title:** Extention (chaining), truncating and replacement of the exception's traceback.

**Description:** The custom exceptions should support the following modes of the traceback handling:

* 'As it is' - e.g. *raise SomeException(some_args)* - both the \_\_*traceback*\_\_ attribute and the *Traceback* property should refer to the same *actual* traceback of the exception from the point of its handling to the point where is has been raised
* 'Chaining' - e.g. *raise SomeException(some_args).with_traceback(some_traceback)* - both the \_\_*traceback*\_\_ attribute and the *Traceback* property should refer to the same traceback - as the *actual* of the exception extended by the passed traceback; see the [Python 3 Built-in Exceptions](https://docs.python.org/3/library/exceptions.html#bltin-exceptions)
* 'Truncating' - e.g. *raise SomeException(some_args, SkipFrames = N)* - the \_\_*traceback*\_\_ attribute should refer to the *actual* traceback of the exception, but the *Traceback* property should show the traceback of the exception with the *N* innermost frames being removed
* 'Replacing' - e.g. *raise SomeException(some_args, FromTraceback = SomeTraceback)* - the \_\_*traceback*\_\_ attribute should refer to the *actual* traceback of the exception, but the *Traceback* property should show the traceback another exception, from wich the tracback object is passed into the initialization method

**Notes** - If the 'replacing' mode is activated, the corresponding keyword argument for the 'truncating' mode should be ignored even if passed. The method *with_traceback*() can be applied only on the already created instance, thus the 'chaining' mode should override the 'truncating' or 'chaining' modes used during the instantiation.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-203

**Title:** Chainging of exceptions using *raise ... from ...* or (re-) raising within *except* or *finally* clause

**Description:** The standard chaining of the exceptions by (re-) raising within *except* or *finally* clause or using explicit chaining with *raise ... from ...* should be preserved (i.e. \_\_cause\_\_ and \_\_context\_\_ attributes should not be modified).

**Verification Method:** D

---

**Requirement ID:** REQ-FUN-204

**Title:** Sub-classing of the custom exception

**Description:** The defined custom exception could be sub-classed preserving the described functionality. The signature of the initialization method could be changed.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-210

**Title:** Initialization of the custom sub-class of **Exception**

**Description:** The initalization method should accept one mandatory positional argument of any type, which can be converted into a string, and two optional (keyword only) arguments *SkipFrames* (int > 0) and *FromTraceback* (**types.TracebackType**). The sting representation of the positional argument should be stored in the *args* attribute as a single element tuple. The keyword arguments should be used only during the instantiation for the creation of the content of the *Traceback* property.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-220

**Title:** Initialization of the custom sub-class of **TypeError**

**Description:** The initalization method should accept two mandatory positional arguments: 1) any type value, which caused the exception, and 2) a sequence of the acceptable types or a single type; and two optional (keyword only) arguments *SkipFrames* (int > 0) and *FromTraceback* (**types.TracebackType**). The error message should be constructed in the following manner: '{type of the passed value} is not a sub-class of ({acceptable types}, )' - and this message should be stored in the *args* attribute as a single element tuple. The keyword arguments should be used only during the instantiation for the creation of the content of the *Traceback* property.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-230

**Title:** Initialization of the custom sub-class of **ValueError**

**Description:** The initalization method should accept two mandatory positional arguments: 1) any type value, which caused the exception, and 2) a string reprenting the accepted range(s) of values; and two optional (keyword only) arguments *SkipFrames* (int > 0) and *FromTraceback* (**types.TracebackType**). The error message should be constructed in the following manner: '{passed value} does not meet restriction {acceptable range(s)}' - and this message should be stored in the *args* attribute as a single element tuple. The keyword arguments should be used only during the instantiation for the creation of the content of the *Traceback* property.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-240

**Title:** Initialization of the custom sub-class of **AttributeError**

**Description:** The initalization method should accept two mandatory positional arguments: 1) any type value, object which is accessed, and 2) a string name of the accessed attribute; and two optional (keyword only) arguments *SkipFrames* (int > 0) and *FromTraceback* (**types.TracebackType**). The error message should be constructed in the following manner: '{object's class name}.{attribute name}' - and this message should be stored in the *args* attribute as a single element tuple. The keyword arguments should be used only during the instantiation for the creation of the content of the *Traceback* property.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-250

**Title:** Initialization of the custom sub-class of **IndexError**

**Description:** The initalization method should accept two mandatory positional arguments: 1) string name of a sequence object, and 2) an integer index, which cannot be accessed; and two optional (keyword only) arguments *SkipFrames* (int > 0) and *FromTraceback* (**types.TracebackType**). The error message should be constructed in the following manner: 'Out of range index {sequence name}[{index}]' - and this message should be stored in the *args* attribute as a single element tuple. The keyword arguments should be used only during the instantiation for the creation of the content of the *Traceback* property.

**Verification Method:** T

---

**Requirement ID:** REQ-FUN-260

**Title:** Initialization of the custom sub-class of **KeyError**

**Description:** The initalization method should accept two mandatory positional arguments: 1) string name of a mapping object, and 2) a string key name, which cannot be accessed; and two optional (keyword only) arguments *SkipFrames* (int > 0) and *FromTraceback* (**types.TracebackType**). The error message should be constructed in the following manner: 'Key not found {mapping name}[{key}]' - and this message should be stored in the *args* attribute as a single element tuple. The keyword arguments should be used only during the instantiation for the creation of the content of the *Traceback* property.

**Verification Method:** T
