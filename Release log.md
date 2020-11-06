# Release log of the library introspection_lib

## 2020-11-06

* Re-factored the module *traceback.py* in order to avoid storage of the actual frame objects - only the already parsed data (strings and integers).
* Added instantiation of ExceptionTraceback from a traceback object.
