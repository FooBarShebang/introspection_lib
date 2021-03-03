# DE001 Resolution of a Path to a Nested Element

The generic definition of a path to be acceptable by the enhanced attribribute resolution function can be a string, an integer number or a (nested) sequence of strings and integer numbers.

```abnf
accepted-input   = any-string / integer / sequence

any-string       = (DQUOTE no-dquote *("." no-dquote) DQUOTE)
any-string       =/ (quote no-quote *("." no-quote) quote)

integer          = ["+" / "-"] 1*DIGIT

sequence         = "[" LWSP sequence-element *(LWSP "," LWSP sequence-element) LWSP "]"
sequence         =/ "(" LWSP sequence-element *(LWSP "," LWSP sequence-element) LWSP ")"

no-dquote        = 1*(%x21 / %x23-2E / %x30-7E / (%x5C DQUOTE))
; any number of visible ASCII characters (VCHAR) except for a dot and a double
; quote (unescaped)

no-quote        = 1*(%x21-26 / %x28-2E / %x30-7E / (%x5C quote) )
; any number of visible ASCII characters (VCHAR) except for a dot and a single
; quote (unescaped)

quote = %x27; single qoute

sequence-element = any-string / integer / sequence
```

This generic definition should be converted into the cannonical form - a list of string or integer elements identifing a single level of nesting - containing one or more elements.

```abnf
canonical-input  = "[" path-element *(SP "," SP path-element) "]"

path-element     = string-node / integer

string-node      = (DQUOTE no-dquote DQUOTE)
string-node      =/ (quote no-quote quote)
```

Thus, any string in the initial, generic definition should be treated as possibly nested attribute or key definition with "." (dot) separation of the level. Each such string should be split into a list of strings by the dot separators. The nested sequences should be flattened into a plain list. I.e. `[1, "a.b", ["c", ["d.e", 1], "f"]]` should become `[1, "a", "b", "c", "d", "e", 1, "f"]`.

Note that the attributes of an object are supposed to be valid Python identifiers to be accessible via dot-notation in the source code; i.e. they may contain only letters, digits and underscores, but the first character must be either a letter or an undescore. Hence, as a string arguments of an attribute resolution function they are supposed to be signle or double quoted proper identifier.

```abnf
attr-name        = (DQUOTE identifier DQUOTE) / (quote identifier quote)

identifier       = (ALPHA / "_") *(ALPHA / DIGIT / "_"); proper Python identifier
```

On the other hand, any proper Python string can be a key of a dictionary (mapping / associative array object). Since the internal implementation of the attributes resolution and storage is based on the dictionaries, any proper Python string can be used as an attribure name as long as it is accessed via *getattribute*() and *setattr*() functions instead of dot-notation. This walk-around is cumbersome for the direct coding, but is well-accepted for the intro- and retro-spection functionality.

Furthermore, integer numbers as well as any hashable type can be used as a key. Therefore, in order to avoid ambiquity it is not allowed to use integers as keys of a dictionary if this dictionary is supposed to be used in the scope of the enhanced attribribute resolution functionality. The integers are reserved to indicate the index access.

Thus, the following design is proposed:

* The nested element resolution functions must expect the generic (mixed / nested) definition of the path, which should be converted into the canonical form
* Within the canonical form each element of the list represents a single level of nesting
* The canonical form path should be traversed one element at the time, and the specific mode of the access should be chosen on the basis of the type of the current level object and the type of the element:
  * Element is an integer number
    * Current level object is a sequence - use indexing access
    * Current level object is not a sequence - raise **TypeError** compatible exception
  * Element is a string
    * Current level object is a mapping type - use access by key
    * Current level object is a sequence type - raise **TypeError** compatible exception
    * Current level object is any other type - use attribute access

The standard Python 'read' access methods / functions raise **IndexError**, **KeyError** and **AttributeError** if the respective element (at any level of nesting) is not found. In the case of the 'write' access methods / functions the situation is more complex. If the target object is immutable, the **TypeError** exception is raised regardless if the respective element is present or not. In the case of mutable mapping types and generic class instances the non-existing key or attribute is created automatically, whereas **IndexError** exception is raised upon assignment to the non-existing element of a mutable sequence.

In order to provide a more 'unified' access scheme the following behaviour of the enhanced access functions is proposed:

* Both 'read' and 'write' functions should work in two modes: *strict* and *relaxed*
* 'Read' access:
  * In the 'strict' mode the **IndexError**, **KeyError** and **AttributeError** compatible exception should be raised if an element at any level of the path is missing - based on the type of the object already accessed (all levels up to the offending one)
  * In the 'relaxed' mode an additional argument is required - the default value, which should be returned is an element at any level is not found
* 'Write' access:
  * In the 'strict' mode the **IndexError**, **KeyError** and **AttributeError** compatible exception should be raised if an element at any level of the path is missing - based on the type of the object already accessed (all levels up to the offending one)
  * In the 'relaxed' mode:
    * If the current level object (up to the missing one) is mutable - add a new sequence element, key or attribute (depending on the type of the current level object), with its value being:
      * The passed value to be assigned - for the last element in the path
      * A dictionary or a list depending on the next element in the path definition being a string or or an integer - for the not last element in the path
    * If the current level object (up to the missing one) is immutable - raise **TypeError** compatible exception
  * If the 'end-node' is found (all path is successfully traversed) but it is immutable - raise **TypeError** compatible exception
