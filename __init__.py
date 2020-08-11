#!/usr/bin/python3
"""
Library introspection_lib

Python introspection framework - wrapping Standard Library functionality.

Modules:
    traceback: function / method call stack and exception traceback analysis
"""

__project__ ='Python introspection framework'
__version_info__= (0, 1, 0)
__version_suffix__= '-dev1'
__version__= ''.join(['.'.join(map(str, __version_info__)), __version_suffix__])
__date__ = '11-08-2020'
__status__ = 'Development'
__author__ = 'Anton Azarov'
__maintainer__ = 'a.azarov@diagnoptics.com'
__license__ = 'Public Domain'
__copyright__ = 'Diagnoptics Technologies B.V.'

__all__ = ['traceback']