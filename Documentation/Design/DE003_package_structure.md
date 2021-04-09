# DE003 Design of automatic detection of the dependencies

## Introduction

The **setuptools** system provides a number of automatic discovery features, e.g. concerning the automatic detection of the sub-packages, but not for the auto-generation of the dependencies and restrictions. Of cause, there are ready solutions, e.g. [importlab](https://github.com/google/importlab), but they have own limitations. In general, it is possible to generate specific format configuration files based only on the static analysis of the source code and file system with the accepable data completeness - only minor manual adjustments will be required afterwards. With the most part of the 'boiler-plate' coding tasks being automated the amount of configuration work as well as probability of the errors is significantly reduced.

This document discussed the major design decisions / patterns used in the implementation of the static code analysis based dependencies and package structure detection in the module *package_structure*.

## Main design decisions

* The analysis is applied to a single folder at a time, but recursively including all its sub-folders
* The analyzed folder must be a proper Python package (as in *import*, not *distribution*); it can be a sub-package of another package, but not a loose collection of Python source files (as scripts, etc.) - this limitation is because of the *relative imports* processing requirement
* The folder being a Python *import package* can also include sub-folders, which are not sub-packages (e.g. collection of tests or specific task scripts), but automatically included into the *distribution package* to be created, unless explicitely instructed otherwise
* Only the Python source files to be included into *distribution package* are considered in the analysis
* The anlysis is designed to be completely static, based on the analysis of the file structure and source code, whereas neither the modules in the analyzed package nor any dependencies should be imported in the process in order to avoid possible side effects
* Only the *import statements* as `import something` and `from somewhere import something` are taken into considiration, the *dynamic* import using functional calls, as of Python Standard Library *importlib.import_module*(), are ignored
* In the case of the dotted import names, as `import os.path` only the 'top level' part of the name is considered; the following up parts may be real sub-modules / sub-packages of the 'top level' object, or may be other modules / packages imported into the namespace of the 'top level' object - in the both cases it is responsibility of the authors / maintainers of that 'top level' object to care about the proper distribution
* Only the 'top level' dependencies directly mentioned in the modules found whithin the package are considered; the code to be distributed is already expected to be tested and proven working, thus no need for the circular dependencies, dependencies propagation and conflict analysis is required - the 3rd party libraries used are supposed to be properly packaged and distributed via a package management system (e.g. *pip*), which, usually, takes care of the 'dependencies hell'
* The 'top level' dependencies found to belong to the Python Standard Library are not included into the generated dependencies configuration
* The version restrictions on the Python interpreter and dependencies are inferred from the environment used during the analysis; they may be manually corrected (extended, removed) manually before the packaging process

## Basics of the Python import mechanism

There are two versions of the import statement:

```python
import something
```

and

```python
from something import something_else
```

The first variant imports an entire (sub-) package or module and makes its content visible / accessible to the module as a nested namespace, which elements / components become accessible using dot notation. It is not possible to import a specific function or class using this variant.

Note that *something* may be a 'top level' module (as in `import os`) or a 'top level' package (as in `import collections`), in which case its elements must be addressed within the module by prepending the respective module / package name in the dot notation, e.g. `os.walk()` or `collections.abc`, etc. It also may be a sub-module / sub-package, in which case the import name should also use the dot notation, as in `import collections.abc`; and the entire import name must be used as the prefix for addressing the components in the code, e.g. `collections.abc.Sequence`. However, in order to avoid long names, the imported (sub-) module / (sub-) package may be aliased as

```python
import collections.abc as c_acb
```

in which case the component's names must be prefixed by that alias, as in `c_abc.Sequence`.

**NB**: this type of aliasing is not the same as

```python
import collections.abc
c_acb = collections.abc
```

since in the later case both `c_abc` and `collections.abc` can be used as the prefix (both names exits simultaneously), whereas in the former case - only `c_abc` name exists.

**Warning**: the first part of the dotted name of a (sub-) package / module MUST be a real base name of a module or package in any of the folders listed in the Python system variable *sys.path*, otherwise the import is not possible, and **ImportError** is raised. However, this rule is not applicable for the following up parts. Usually, the dotted names give an impression of the nested *package -> sub-package -> module*, etc. structure, but it is not always true. For instance, in the Python Standard Library: *os* is, in fact, a module, not a package, but it imports and aliases other modules, thus *os.path* is just an alias for another module (on POSIX systems - *posixpath*); whereas *collections* is a package, and it has *abc* module within, although that module simply imports everything from the 'top level' *_collections_abc* module, thus, effectively, *collections.abc* and *_collections_abc* refer to the same set of objects (the second one is considered to be 'private' implementation, and not intended to be imported directly). In short, without sofisticated analysis, it is not possible to say if any part of a dotted name in the import statement is a real module / package or not, except for the first one.

Finally, the first variant of the import statement allows multiple imports, e.g.

```python
import os, collections.abc as c_abc, sys
```

which is completely equivalent to

```python
import os
import collections.abc as c_abc
import sys
```

The second import variant is designed for importing only part (one or several components) from the namespace of an module / package directly into the namespace of another module. The *something* part of the statement foloows the same rules as above - it may refer only to a namespace ((sub-) module / (sub-) package). The *something_else* part is, usually, a variable, a function or a class, however, a sub-module or sub-package is allowed as well. The important thing is that this *something_else* name becomes visible directly in the namespace of the module. Consider the following equivalent examples (as long as it concerns *join*() function) for illustration:

```python
import os
print(os.path.join('a','b'))
...
import os.path
print(os.path.join('a','b'))
...
from os import path
print(path.join('a','b'))
...
from os.path import join
print(join('a','b'))
```

The imported name (*something_else* part) may also be aliased in order to avoid names conflict or reduce the amount of typing, and multiple imports are allowed:

```python
from os.path import join as m_join, isfile
print(isfile(m_join('a','b')))
```

or

```python
from os.path import join as m_join
from os.path import isfile
print(isfile(m_join('a','b')))
```

are equivalent.

The second import statement variant also support relative import notation. Suppose, in the package *some_package* there are two sub-packages: *sub1* and *sub2*, and the module *a* in *sub1* wants to import some function *get_it*() from the module *b* in *sub2*, in which case the following statement can be used:

```python
from ..sub2.b import get_it
```

Each consecutive leading dot in the name means jumping one level up in the package hierarchical structure tree starting from the position of the module, where the import is made.

There is also functional call interface for the imports provided by the Standard Library - *importlib*, however it is considered to be a bad programming practise to use it instead of the import statements outside the situations requiring *dynamic* import. With the *dynamic* import one or another module is imported on demand, depending on the user actions or data input. Such functional call imports are not taken into account in the static code analysis.
