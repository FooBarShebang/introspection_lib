#!/usr/bin/python3
"""
Library introspection_lib

Python introspection framework - wrapping Standard Library functionality.

Modules:
    my_traceback: function / method call stack and exception traceback analysis
    base_exceptions: custom exceptions with the enhanced built-in traceback
        analysis functionality
    my_logging: custom 'dummy' and dual (console + file) loggers with min-max
        filtering of the messages handling and propagation
    dynamic_import: 'on demand' import of a module or its component
    package_structure: static analysis of an import package structure and
        dependencies
"""

__project__ = 'Python introspection framework'
__version_info__= (0, 5, 0)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '16-04-2021'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['my_traceback', 'base_exceptions', 'my_logging', 'dynamic_import',
            'package_structure']