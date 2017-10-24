.. _acadia2017_day1_python101:

********************************************************************************
Python 101
********************************************************************************

The compas framework is based on Python.
Python 3 is fully supported and the code is backwards compatible with Python +2.6.


Built-in types
==============

https://docs.python.org/3/library/stdtypes.html

* numeric types: int, float, complex
* iterator types
* sequence types: list, tuple, range
* text sequence type: str
  Textual data in Python is handled with str objects, or strings.
  Strings are immutable sequences of Unicode code points.
* binary sequence types: bytes, bytearray, memoryview
* set types: set, frozenset
* mapping types: dict
  A mapping object maps hashable values to arbitrary objects.
  Mappings are mutable objects.
  There is currently only one standard mapping type, the dictionary.
* context manager types:
  Python's with statement supports the concept of a runtime context defined by a context manager.
* other types: modules, classes and class instances, functions, methods,
  code objects, type objects, null object, ellipsis object, notimplemented object,
  boolean values, internal objects


Container types
===============

https://wiki.python.org/moin/TimeComplexity

* list
* set
* tuple
* dict
* collections module

List
----

https://docs.python.org/3/library/stdtypes.html#lists

    Lists are mutable sequences, typically used to store collections of homogeneous items
    (where the precise degree of similarity will vary by application).

* Ordered collection of items.
* List items can be of any type.
* One list can contain many different types.
* Lists are mutable.
* Behaves like a stack (LIFO)


.. code-block:: python

    items = [1, 2, 3, 4]

    for item in items:
        print item

    items.append(5)
    items.insert(0, 6)
    items = items + [7, 8, 9]
    items.extend([11, 12, 13])

    # 6, 1, 2, 3, 4, 5, 7, 8, 9, 11, 12, 13

    # http://stackoverflow.com/questions/11520492/difference-between-del-remove-and-pop-on-lists

    items.remove(8)
    del items[1]
    print items.pop(3)

    print items[::2]
    print items[1::2]
    print items[::-1]
    print items
    print items[:]
    print items[0:]
    print items[:-1]

.. code-block:: python

    items = [0] * 4
    items = [None] * 4

    items[0] = 1

    items = [[0]] * 4

    items[0][0] = 1


Built-in functions
==================

Comprehensions
==============

Flow control
============

Functions
=========

Classes
=======

Syntactic sugar
===============
