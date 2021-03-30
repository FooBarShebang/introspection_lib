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

## 2020-12-10 v0.3.0-dev1

Bug fix:

* Discovered: Python 3.8.5 (Linux Mint 20, kernel 5.4.0)
* Affected: the treshold severity level of the logger is ignored if it is a root and has attached handlers - and no other loggers are attached
* Fix: the logger's own severity threshold level is checked by the filters attached to it and its handlers

## 2021-02-26 v0.4.0-dev1

* Added *dynamic_import* module with the tests and documentation
* Updated the existing documentation

## 2021-03-30

Renamed modules *traceback* and *logging* to *my_traceback* and *my_logging* respectively, otherwise the packaging doesn't work.
