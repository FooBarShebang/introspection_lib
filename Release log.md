# Release log of the library introspection_lib

## 2020-11-06

* Re-factored the module *traceback.py* in order to avoid storage of the actual frame objects - only the already parsed data (strings and integers).
* Added instantiation of ExceptionTraceback from a traceback object.

## 2020-11-18

* Exceptions classes with the built-in human and machine-readable customizable traceback analysis - module *base_exceptions.py*.

## 2020-12-01

* Customized logger classes with min-max filtering and dual output - module *logging.py*.
* Fixed bug of not being able to skip exactly N-1 frame in *traceback.py*
* Added custom exceptions catching umbrella - a tuple *UT_Exception_Check* listing all defined exceptions in module *base_exceptions.py* as a walk around of Python 3 try...except not relying on isinstance() but direct MRO check
