# UD005 Reference on the Module introspection_lib.universal_access

## Scope

This document describes the design, intended usage, implementation details and API of the module *universal_access*, which implements a number of functions to provide a unified API for the read and write access to an attribute of a generic class or instance, key of a dictionary, and an element of a sequence (by index). This module also implements functions, which can navigate a complex structured data type down to a specific, deeply nested component using a generic path definition (see [DE001](../Design/DE001_element_path.md) design document).

The implemented functions are:

* *FlattenPath*()
* *GetData*()
* *GetDataDefault*()
* *SetDataStrict*()
* *SetData*()
* *GetElement*()
* *SetElement*()

## Intended Functionality and Use

The the Python programming language requires different syntax for accessing 'internal components' of the different data types. An attribute of a class object or a class instance object is, normally, addressed using 'dot notation' by the *attribute name* as `Object.Attribute` in the source code. An entry of a mapping object (associative array) is, normally, accessed by its *key name* as `Dict['Key']` (parenthesis mean that the key is a string, which is not always the case). And an element of a sequence is accessed by its integer *index* as `Sequence[Index]`. This distinction is helpful in understanding the source code, and it helps to reduce the number of programming errors.

However, there are alternative ways; for instance, an attribute of an object can be read and modified using the standard, built-in functions `getattr(Object, 'Attribute')` and `setattr(Object, 'Attribute', Value)` - which functions are very useful for the intro- and retrospection functionality. The mapping type objects have method *get*(), which can be used to retrieve the value bound to a specific key as `Dict.get('Key')`, whereas there is no method to modify the value of an existing key or to add a new key : value pair - it must be done using `Dict['Key']` notation. The *mutable* sequences have methods to insert and delete elements, but not to modify or retrieve the value of an element without it being removed, thus the `Sequence[Index]` notation is the only possible way to read the value of or modify an element.

There is also significant assymmetry of the read and write access methods, especially concering different data types. In the case of the mapping objects and classes / instances read access to a non-existing key or attribute results in an exception with the standard `Dict['Key']` and `Object.Attribute` notation, whereas an assignment (write access) to a non-existing key or attribute automatically creates it. *Note* that the distinction between the *class* and *instance* attributes complicates the matter further, although it is not relevant for the issue being discussed.

Both the modification (write) and data retrieval (read) access to a non-existing element of a *mutable* sequence by its positional index (index out of range) result in an exception. Although it is possible to insert a new element at any position within the current indexes range, including before and after the alreadt existing - it does not happen automatically if an assigment is attempter to an element of a mutable sequence with the index being out of range.

Thus, the first task of this module is to provide an unified procedural *get* / *set* interface in the form of `Getter(SomeObject, Element)` and `Setter(SomeObject, Element, Value)`, there `SomeObject` may be a sequence, a mapping type or a generic class / instance object, and the `Element` being either an integer index or a string key or attribute name.

## Design and Implementation

## API Reference

### Functions

**GetData**(gObject, gPath)

*Signature*:

type A, str OR int -> type B

*Args*:

* *gObject*: **type A**; the object to be inspected
* *gPath*: **str** OR **int**; the attribute name / key or index of the element to be accessed

*Returns*:

**type B**: the value of the found by attribute name, key or index element

*Raises*:

* **UT_TypeError**: type mismatch between object and path - sequence object and non-integer path, non-sequence object and non-string path, OR the path is neither an integer or a string
* **UT_IndexError**: object is a sequence, and path is an integer, but outside the range of the acceptable indexes, defined by the length of the sequence
* **UT_KeyError**: object is a mapping type, and path is a string, but it is not found among the keys
* **UT_AttributeError**: object is a genric class or instance, and path is a string, but it is not found among the attributes

*Description*:

Universal 'read' access to an element of a list, key : value pair entry of a mapping type or an attribute of a generic class or instance. Raises exceptions compatible with (sub-classes of) the standard exceptions **IndexError**, **KeyError** or **AttributeError**, which should be normally raised upon 'read' access to a non-existing element.

**GetDataDefault**(gObject, gPath, gValue)

*Signature*:

type A, str OR int, type B -> type C

*Args*:

* *gObject*: **type A**; the object to be inspected
* *gPath*: **str** OR **int**; the attribute name / key or index of the element to be accessed
* *gValue*: **type B**; the default value to return, if such element is not found

*Returns*:

**type C**: the value of the found by attribute name, key or index element, OR the passed default value is the node is not found

*Raises*:

* **UT_TypeError**: type mismatch between object and path - sequence object and non-integer path, non-sequence object and non-string path, OR the path is neither an integer or a string

*Description*:

Universal 'read' access to an element of a list, key : value pair entry of a mapping type or an attribute of a generic class or instance with a default value, which should be returned upon 'read' access to a non-existing element instead of raising of a respective exception.

**SetDataStrict**(gObject, gPath, gValue)

*Signature*:

type A, str OR int, type B -> None

*Args*:

* *gObject*: **type A**; the object to be inspected
* *gPath*: **str** OR **int**; the attribute name / key or index of the element to be accessed
* *gValue*: **type B**; the value assign

*Raises*:

* **UT_TypeError**: object (first argument) is immutable, OR type mismatch between object and path - sequence object and non-integer path, non-sequence object and non-string path, OR the path is neither an integer or a string
* **UT_IndexError**: object is a sequence, and path is an integer, but outside the range of the acceptable indexes, defined by the length of the sequence
* **UT_KeyError**: object is a mapping type, and path is a string, but it is not found among the keys
* **UT_AttributeError**: object is a genric class or instance, and path is a string, but it is not found among the attributes

*Description*:

Universal 'write' access to an element of a list, key : value pair entry of a mapping type or an attribute of a generic class or instance, but only to the existing ones of the mutable objects. New attributes, sequence elements or mapping type entries cannot be created even if the object itself is mutable. Existing elements of the immutable sequences or exsiting entries of the immutable mapping type objects cannot be modified.

**SetData**(gObject, gPath, gValue)

*Signature*:

type A, str OR int, type B -> None

*Args*:

* *gObject*: **type A**; the object to be inspected
* *gPath*: **str** OR **int**; the attribute name / key or index of the element to be accessed
* *gValue*: **type B**; the value assign

*Raises*:

* **UT_TypeError**: object (first argument) is immutable, OR type mismatch between object and path - sequence object and non-integer path, non-sequence object and non-string path, OR the path is neither an integer or a string

*Description*:

Universal 'write' access to an element of a list, key : value pair entry of a mapping type or an attribute of a generic class or instance. If such element is not found, it is created automatically, unless the object is immutable. In the case of a mutable sequence type object, the new element is prepended as a first element or appended as the last one if the passed index is outside the current range.

**FlattenPath**(gPath)

*Signature*:

str OR int OR seq(type A) -> list(str OR int)

*Args*:

* *gPath*: **str** OR **int** OR **seq**(type A); the generic nested path description to be flattened

*Returns*:

**list**(str OR int): the flattened nested path description

*Raises*:

* **UT_TypeError**: the passed generic path is not an integer, a string or a (nested) sequence of only strings and integers

*Description*:

Flattens a nested generic path definition into a plain list of only strings and integers defining a navigation path within a nested structured object, with each element in the path being an integer index or a string key or attribute name. The input is supposed to be a string, an integer or a flat or nested sequence of only integers and strings. Any string in the input may encode multiple levels using dot notation.

**GetElement**(gObject, gPath, *, bStrict = True, gDefault = None)

*Signature*:

type A, str OR int OR seq(type B)/, *, bool, type C/ -> type D

*Args*:

* *gObject*: **type A**; the object to be inspected
* *gPath*: **str** OR **int** OR **seq**(type B); the generic path to the end node of a nested struture object
* *bStrict*: (keyword) **bool**; the flag if the strict access mode is to be used, defaults to *True*
* *gDefault*: (keyword) **type C**; the default value to return, if any level element is not found along the path, defaults to *None*, has an effect only if the *bStrict* flag is *False*

*Returns*:

**type D**: the value of the last element along the passed path, OR the passed default value if such element is not found and the requested mode is not stict

*Raises*:

* **UT_TypeError**: the passed generic path is not an integer, a string or a (nested) sequence of only strings and integers, OR type mismatch between object level and path element - sequence object level and non-integer path element, non-sequence object level and non-string path element
* **UT_ValueError**: the passed generic path is an empty sequence
* **UT_IndexError**: an object along the path is a sequence, and the respective access index is outside the range - 'strict' mode only
* **UT_KeyError**: an object along the path is a mapping type, and the respective access key is not found - 'strict' mode only
* **UT_AttributeError**: an object along the path is a genric class or instance, and the respective attribute is not found - 'strict' mode only

*Description*:

Attempts to retrieve the value of an element (key, attribute) of the nested structured object (including nested sequences) defined by a generic path. Can operate in two modes: 'strict' and 'relaxed'. In the strict mode an exception is raised if the path is incorrect, i.e., at least, one element of the path is not found. In the 'relaxed' mode a default value is returned is the path is incorrect.

**SetElement**(gObject, gPath, gValue, *, bStrict = True)

*Signature*:

type A, str OR int OR seq(type B), type C/, *, bool/ -> None

*Args*:

* *gObject*: **type A**; the object to be inspected
* *gPath*: **str** OR **int** OR **seq**(type B); the generic path to the end node of a nested struture object
* *gValue*: **type C**; the value to be assigned to the end node
* *bStrict*: (keyword) **bool**; the flag if the strict access mode is to be used, defaults to *True*

*Raises*:

* **UT_TypeError**: the passed generic path is not an integer, a string or a (nested) sequence of only strings and integers, OR type mismatch between object level and path element - sequence object level and non-integer path element, non-sequence object level and non-string path element, OR an immutable object requires modification in order to complete the task
* **UT_ValueError**: the passed generic path is an empty sequence
* **UT_IndexError**: an object along the path is a sequence, and the respective access index is outside the range - 'strict' mode only
* **UT_KeyError**: an object along the path is a mapping type, and the respective access key is not found - 'strict' mode only
* **UT_AttributeError**: an object along the path is a genric class or instance, and the respective attribute is not found - 'strict' mode only

*Description*:

Attempts to assign a value to an element (key, attribute) of the nested structured object (including nested sequences) defined by a generic path. Can operate in two modes: 'strict' and 'relaxed'. In the strict mode an exception is raised if the path is incorrect, i.e., at least, one element of the path is not found. In the 'relaxed' mode the missing sub-path is created using nesting of dictionaries and lists, unless the new branch is to be attached to an immutable object.
