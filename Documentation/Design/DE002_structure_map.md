# DE002 Definition of JSON-encoding Ready Map of an Object Structure

## Goals

The purpose of this document is to describe the rules on how to create a map of an arbitrary Python object, including scalar data types, (nested) containers and associative arrays (dictionaries) as well as arbitrary class instances treated as C-struct like constructs. Such functionality is helpful for the automated serialization of the data (into and from the JSON format text files) and for data mapping between different structured storage types.

## JSON format

The full specification of the JSON syntax is regulated by the standard [ISO/IEC 21778:2017](https://www.iso.org/standard/71616.html), from which only a sub-set of features is applicable considering its usage to describe the structure of a Python data object.

```abnf
json    = LWSP (scalar / list / dict / "null") LWSP

scalar  = string / integer / float / bool

list    = "[" *1(json *("," json))"]"

dict    = "{" *1(entry, *("," entry))"}"

entry   = LWSP string LWSP ":" json

string  = DQUOTE *(VCHAR / ("\u" 4HEXDIG)) DQUOTE

integer = *1("+" / "-") 1*(DIGIT)

float   = integer "." *DIGIT *1(("e" / "E") integer)

bool    = "true" / "false"
```

## JSON to Python native types

The Standard Python Library provides JSON encoder and decoder (module *json*), but it cannot automatically (de-) serialize arbitrary class instances. The standard en- and decoding functionality is based on the following rules.

### JSON decoding (standard)

* JSON *scalar* types:
  * *integer* -> **int**
  * *float* -> **float**
  * *string* -> **str**
  * *bool* -> **bool** : **true** -> **True**, **false** -> **False**
  * *null* -> **None**
* JSON *list* (sequence, array) -> **list**
* JSON *dict* (object) -> **dict**

### JSON encoding (standard)

* Python *scalar* types:
  * **int** -> *integer*
  * **float** -> *float*
  * **str** -> *string*
  * **bool** -> *bool* : **True** -> **true**, **False** -> **false**
  * **None** -> *null*
* Any Python sequence type (mutable, or immutable) as **list**, **tuple**, **set** -> *list*
* Any Python mapping type (mutable, or immutable) as **dict**, **dictproxy**, etc. -> *dict*

### Proposed extentions

In terms of JSON encoding the arbitrary class instances should be treated as mapping types but only concerning their *data attributes* (*fields*) as well as *properties* but not the methods. Furthermore, the *read-access* and *write-access* structure map should be constructed under specific restriction.

#### Read-access mapping

* The 'basic' data types such as scalars, buit-in sequences and mapping types (list, tuple, set, dict, etc.) should be treated according the the standard parser rules with addition of the following restrictions:
  * All mapping types should be treated as ordered dictionaries (preserving their entries order) even if this is not the case
  * Named tuples should be treated as ordered dictionaries
* An instance of an arbitrary class should be represented by an ordered dictionary with the following additional rules:
  * The stucture is analized bottom-up, starting form the instance attributes (slots, then internal dictionary), followed by the class attributes defined in the class itself, followed by the class attributes inherited from the super classes in the exact MRO order, with the bottom level definitions 'shadowing' the upper level (inherited) values
  * Only the *data attributes* (not callable) should be considered, whereas the *properties* (with *getter* method defined) should be considered as *data attributes* as well
  * Attributes with the names starting with, at least, one underscore should be ignored
  * Attributes storing the references to the built-in types (as classes, not instances, e.g. **int** instead of 1) should be ignored
  * The name of the instance or (inherited) class attribute becomes the key name in the ordered dictionary, with the attribute value converted to JSON-ready format being assigned as the value of the key
* Callable objects, except for properties and C-struct like objects with an actual data, built-in data types (as classes, not instances) as the end-nodes should be ignored in the mapping types, named tuples and generic data storage user-defined classes, and replaced by the special value "!@#notJSON" in the sequences (isntead of the named tuples)
* These rules should be applied recursively to the nested structured elements

#### Write-access mapping

* The scalar types as well as *mutable* sequence and mapping types should be processed in the same manner as for the read-access mapping
* In case of the *immutable* sequences the following rules are applied:
  * The return type should be a list
  * All end-node elements (not nested containers / structures) should be replaced by the special string "!@#immutable"
  * All nested class instances, mapping and sequence type elements should be processed with the recursive application of these same rules
  * If such sequence does not contain any nested containers / structures with mutable end-nodes, the entire sequence should be represented as an empty list
* In case of the *immutable* mapping types and named tuples the following rules are applied:
  * The return type should be an ordered dictionary
  * All end-node elements (not nested containers / structures) - values bound to the keys - should be ignored
  * All nested class instances, mapping and sequence type elements as the values bound to the keys should be processed with the recursive application of these same rules
  * The order of the keys (if present) should be preserved
* The class instances should be represented by ordered dictionaries with the following rules applied:
  * Only instance attributes (defined in the slots or internal dictionary) as well as the properties with the setter method should be considered
  * All available properties with the setter method, including the inherited, should be concerned, taking the shadowing and MRO into account
  * If a property has a setter but not a getter method, it should be represented by the *None* value
  * Attributes with the names starting with, at least, one underscore should be ignored
  * Attributes storing the references to the built-in types (as classes, not instances, e.g. **int** instead of 1) or callables (e.g., methods, but not properties) should be ignored
* Callable objects, except for properties and C-struct like objects with an actual data, built-in data types (as classes, not instances) as the end-nodes should be ignored in the mapping types, named tuples and generic data storage user-defined classes, and replaced by the special value "!@#notJSON" in the mutable sequences
* These rules should be applied recursively to the nested structured elements
