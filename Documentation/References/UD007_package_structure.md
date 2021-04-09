# UD007 Reference on the Module introspection_lib.package_structure

## Scope

This document describes the design, intended usage, implementation details and API of the module *package_structure*, which implements a number of functions and classes for the static analysis (source code inspection without imports) of the structure of Python packages in order to construct a hierarchical tree structure of the package (with the adjustible selection / exclusion criteria), a list of the dependencies and mapping of the local namespace names / aliases to the imported objects. This functionality is to be used, primarily, for the automated creation of the build configuration files.

The implemented functional components are:

* Functions
  * *IsPyFile*()
  * *IsPyPackage*()
  * *SelectPySourceFiles*()
  * *GetQualifiedName*()
  * *ResolveRelativeImport*()
* Classes
  * **PackageStructure**

## Intended Functionality and Use

This module is intended to be used a tool to help in the automated creation of the configuration files for the **setuptools** based packaging systems. The purpose is to perform the static analysis of the file system and the content of the found source files in order to build a hierarchical structure of a package and to generate the list of dependencies of the package. The **setuptools** system provides a number of automatic discovery features, but they have their own limitations. The idea behind this module is to generate explicit lists of options in the configuration files instead of relying on the auto-detection methods of the **setuptools** system.

For example, a package may contain a number of modules, sub-packages and sub-modules, which implement the base functionality. But, in addition, it may contain a number of executable scripts designed for some specific tasks based on the functionality of the package. I, personally, also prefer to distribute the packages (as libraries) together with the test suits. Neither the work script sets, nor the test suits are, strictly speaking, part of the library concerining the API, therefore there is no logic in turning the respective sub-folders into sub-packages. Thus, the auto-detection features of the **setuptools** system ignore such not sub-packages sub-folders. The algorithm used in this module, on contrary, is gready - every found Python source file in any of the sub-folders is included into the analysis, unless explicitely requested otherwise.

Both individual source files and the entire sub-folders (including all their nested sub-sub-folders) can be excluded using simple match patterns including Unix shell-style wildcards (see **fnmatch** in the Python Standard Library). The individual files are filtered by application of the patterns to the base filenames, whereas the folder names are matched on the remaining part of the path after the removal of the common prefix (path to the 'root' folder of the analysis). All sub-folders remaining after application of the filtering and containg, at least, one Python source file (not filtered out by the second set of patterns) will be included into the distibution configuration file. Another convention is that the 'root' folder in the analysis will be made into the 'top level' element ('root' package).

The detection of dependencies is based solely on the static analysis of the source code of the source files selected for the packaging. Only the direct importing statements as `import module` and `from module import something` are concerned. The functional call based imports (e.g. using **importlib**) are ignored. There several reasons for this design decision:

* Dynamic (functional call) imports is mostly used to 'load-on-demand' specific modules in response to the specific user input or received data, thus the names of the respective packages or module may be even indeductible using static source code analysis
* There are may other user-defined functions or methods, which perform dynamic import, and cannot be deducted without very sofisticated lexic analysis / parsing of the code; therefore spending a lot of efforts on the analysis of the *importlib.import_module*() alike calls may not solve the dynamic import problem
* The static import - import statements - on the other hand, are explicit and they do not allow usage of aliases in place of the actual names of the modules / packages, at least, the root of the qualified dot-notation name - which can be found in the file system without doing actual imports

Basically, the algorithm looks up all `import ...` and `from ... import ...` statements and forms a list of the unique 'root' / 'top level' names of the imports (the first part in the dot notation name) and filters out all names referencing the Python Standard Library top level modules (like *os*) and packages (like *collections*). The remainder of the list is the 3rd party packages, i.e. the dependencies, which can be put into the dependencies part of the configuration file. The currently installed versions of the respective packages are indicated as the initial restrictions. See [DE003](../Design/DE003_package_structure.md) design document for further references.

The automatically generated configuration files, in many cases, may be used directly; but, in general, they must be adjusted / corrected manually, especially concerning the restrictions. However, the proper structure (template) is guaranteed in the auto-generated configuration files, as well as proper filling-in of the majority of the 'boiler-plate' information.

As the added functionality, the mappings of the imported and aliased names into the fully qualified names of the imported objects (per namespace / source code module) is generated during the analysis, cached and made available for more detailed analysis of the source code tasks.

## Design and Implementation

The components diagram of the module is shown below:

![Components diagram](../UML/package_structure/package_structure_components.png)

The clients of the module are supposed to work mostly with the implemented classes. The implemented functions are intended primarily to be called by the methods of those classes, however, they can be helpful on their own. Therefore, they are implemented as 'public' functions, and not as 'private' one or internal methods of the said classes.

The function *IsPyFile*() checks if the passed argument is the path to an existing Python source file, not a symlink. Thus, the argument must be as string - otherwise **UT_TypeError** exception is raised; the file must exist, it must have the '.py' extension, and it must be not a symlink.

The function *IsPyPackage*() checks if the passed argument is the path to an existing folder, not a symlink, which is considered to be a Python package. Thus, the argument must be as string - otherwise **UT_TypeError** exception is raised; the folder must exist, it must have the '\_\_init\_\_.py' file within, and it must be not a symlink.

The function *SelectPySourceFiles*() generates a list of the base filenames of all actual Python source files (ignoring the symlinks) found within a specified folder, which also should not be a symlink. The returned list is empty if there no actual Python source files within the folder, or the passed path is symlink itself. The function does not look inside the sub-folders, only within the specified folder. The argument must be as string - otherwise **UT_TypeError** exception is raised.

The function *GetQualifiedName*() attempts to create a fully qualified import name for a module or a (sub-) package. Basically, if it finds a Python source file or a Python package located at the passed path, the function checks if the parent folder to this file or folder is a Python package. Thus, it climbs up the file structure hierarchy until it reaches the folder, which is not a Python package, or the root of the tree. The *base filename* of a Python source file without the '.py' extension is used as the *module* name, and the base name of a folder is used as the respective (sub-) package name. Depending on the type and value of the argument the returned value is constructed following the rules below:

* Not a string input -> **UT_TypeError** is raised
* An arbitrary string, which is not an existing file / folder path -> **None** value is returned
* String path leading to a symlink to a file or folder -> **None** value is returned
* String path leading to an actual file (not a symlink), but not a Python source file -> **None** value is returned
* String path leading to an actual folder (not a symlink), but not a Python package -> **None** value is returned
* Path to a stand-alone Python module / script, which is not part of a package -> string *module* name value (see above)
* Path to a 'root' (not nested) Python package -> string *package* name value (see above)
* Path to Python module, wich is a part of a package -> string *package/.subpackage/.module* import name with a variable depth of inclusion
* Path to Python package, wich is a part of another package -> string *package/.subpackage/.subpackage* import name with a variable depth of inclusion

The function *ResolveRelativeImport*() is designed for the resolution of the relative imports into absolute import names relative to the qualified name of the module, where these imports are made. It requires two arguments: a path to a Python module, and the absolute or relative import name. The both arguments must be strings, otherwise **UT_TypeError** exception is raised. If the passed import name is absolute - i.e. it doesn't start with any number of dots '.', the file path is ignored and the passed absolute import name is returned. If the passed import name is relative - i.e. it starts with one or more consecutive dots, the passed file path must lead to an existing actual Python source file - otherwise **UT_ValueError** is raised. The fully qualified name of the module is resolved (see *GetQualifiedName*()) by the passed file path. The number of leading dots in the import name is counted, and the corresponding number of the tailing elements in the module's qualified name are removed. The import name is stripped of the leading dots and the remaining part is attached via dot to the tail-stripped module's qualified name. Note, that the relative import cannot point outside the 'root' package of the respective module - otherwise **UT_ValueError** is raised.

## API Reference

### Functions

**IsPyFile**(strFile)

*Signature*:

str -> bool

*Args*:

* *strFile*: **str**; a path to a file (absolute or relative to the current working directory)

*Returns*:

**bool**: the result of the check

*Raises*:

**UT_TypeError**: passed argument is not a string

*Description*:

Checks if a file exists, it is not a link, and it has '.py' extention, i.e. it is a Python source file.

**IsPyPackage**(strFolder)

*Signature*:

str -> bool

*Args*:

* *strFolder*: **str**; a path to a folder (absolute or relative to the current working directory)

*Returns*:

**bool**: the result of the check

*Raises*:

**UT_TypeError**: passed argument is not a string

*Description*:

Checks if a folder exists, it is not a link, and it has *\_\_init\_\_.py* file within (actual, not a link), i.e. it is a Python package.

**SelectPySourceFiles**(strFolder)

*Signature*:

str -> list(str)

*Args*:

* *strFolder*: **str**; a path to a file (absolute or relative to the current working directory)

*Returns*:

**list(str)**: the list of the base filenames of the found source files

*Raises*:

**UT_TypeError**: passed argument is not a string

*Description*:

Finds all Python source files (not symlinks) present in a directory (not a symlink itself).

**GetQualifiedName**(strPath)

*Signature*:

str -> str OR None

*Args*:

* *strPath*: **str**; a path to a folder or module (absolute or relative to the current working directory)

*Returns*:

* **str**: the fully qualified name of a module / (sub-) package, if it was resolved
* **None**: if it was not resolved

*Raises*:

**UT_TypeError**: passed argument is not a string

*Description*:

Attempts to resolve the qualified (dot notation) of a module or (sub-) package from its path. The symlinks are ignored.

**ResolveRelativeImport**(strFile, strImportName)

*Signature*:

str, str -> str

*Args*:

* *strFile*: **str**; a path to an actual Python source file, ignored in the case of an absolute import as long as it is string
* *strImportName*: **str**; an absolute or relative import name

*Returns*:

**str**: the absolute import path

*Raises*:

* **UT_TypeError**: any of the arguments is not a string
* **UT_ValueError**: only in the case a relative import - first argument is not a path to an actual Python source file, OR the relative path leads to the outside of the 'root' package of the module, OR the module itself is not a part of a package

*Description*:

Attempts to resolve the relative import into an absolute relatively to the 'root' package of the referenced by path module. The module must be whithin a package, and the relative path must end-up within the 'root' of the package structure, to which the referenced module belongs. The actual existence of a module referenced by the produced absolute path is not checked. The passed absolute imports are not modified.

### Classes

#### PackageStructure
