# Library introspection_lib

## Purpose

Functionality enhancements and usage convenience wrappers for the Python 3 Standard Library introspection functionality. E.g. call stack and exception traceback analysis, signature of the methods and functions, class composition, etc. It provides framework of the traceback enhanced analysis custom exceptions and customized logging classes.

## Installation

Clone the official repository into your local workspace / project folder:

```bash
$git clone <repository_path> "your projects folder"/introspection_lib
```

Check the system requirements and dependencies:

```bash
$cd "your projects folder"/introspection_lib
$python3 ./check_dependencies.py
```

### For developers only

Initialize the UML templates submodule

```bash
$cd "your projects folder"/introspection_lib/Documentation/UML/Templates
$git submodule init
```

Download the content of the UML templates submodule

```bash
$git submodule update --recursive --remote
```

## System requirements

This library is written in Python 3 programming language (>= v3.6) and is intended to be OS platform independent. At least, it is tested under MS Windows and GNU Linux OSes, see [Documentation/Tests/tested_OS.md](./Documentation/Tests/tested_OS.md).

This library does not depend on any other Python library / package except for the Standard Library (see [Dependencies.md](./Dependencies.md)).

## Library structure

![Component diagram](./Documentation/UML/components.png)

## Documentation

All documentation on the library is written in Markdown format, see the [index list](./Documentation/index.md).

* [Requirements](./Documentation/Requirements/index.md)
* [Design](./Documentation/Design/index.md)
* [Tests](./Documentation/Tests/index.md)
* [User and API References](./Documentation/References/index.md)
