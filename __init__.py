#!/usr/bin/python3
"""
Library introspection_lib

Python introspection framework - wrapping Standard Library functionality.

Modules:
    traceback: function / method call stack and exception traceback analysis
    base_exceptions: custom exceptions with the enhanced built-in traceback
        analysis functionality
    logging: custom 'dummy' and dual (console + file) loggers with min-max
        filtering of the messages handling and propagation
    dynamic_import: 'on demand' import of a module or its component
"""

__project__ ='Python introspection framework'
__version_info__= (0, 4, 0)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '26-02-2021'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['traceback', 'base_exceptions', 'logging', 'dynamic_import']