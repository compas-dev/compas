.. _acadia2017_day1_python101:

********************************************************************************
Python 101
********************************************************************************

The compas framework is based on Python.
Python 3 is fully supported and the code is backwards compatible with Python +2.6.


Implementations
===============

https://wiki.python.org/moin/PythonImplementations


CPython
-------

`The Official Python Documentation <https://docs.python.org/2/index.html>`_

.. code-block:: python

    # many packages are wrappers around powerful C/C++ libraries

    import sys
    import os

    import ctypes
    import cProfile
    import scipy
    import numpy
    import shapely


IronPython
----------

`IronPython .NET integration <http://ironpython.net/documentation/dotnet/>`_

.. code-block:: python

    # packages that are wrappers for C/C++ code are not available
    # access to Windows ecosystem

    import sys
    import os

    import System
    import System.Windows.Forms
    import System.Drawing.Image
    import System.Environment.NewLine


Jython
------

`The Definitive Guide to Jython <http://www.jython.org/jythonbook/en/1.0/index.html>`_

.. code-block:: python

    # packages that are wrappers for C/C++ code are not available
    # access to Java ecosystem

    import sys
    import os

    from java.lang import System
    from java.util import Vector
    from java.io import FileOuputStream


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

List
----

https://docs.python.org/3/library/stdtypes.html#lists

* Ordered collection of items.
* List items can be of any type.
* One list can contain many different types.
* Lists are mutable.
* Behaves like a stack (LIFO)

From the docs:

    Lists are mutable sequences, typically used to store collections of homogeneous items
    (where the precise degree of similarity will vary by application).

.. code-block:: python

    items = [1, 2, 3, 4]

    for item in items:
        print item

    items.append(5)
    items.insert(0, 6)
    items = items + [7, 8, 9]
    items.extend([11, 12, 13])

    items.remove(8)
    del items[1]
    print items.pop(3)

    print items

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


Tuple
-----

https://docs.python.org/3/library/stdtypes.html#tuples

* Ordered collection of items.
* Tuple items can be of any type.
* One tuple can contain multiple types.
* Tuples are immutable.

From the docs:

    Tuples are immutable sequences, typically used to store collections of heterogeneous data (such as the 2-tuples produced by the enumerate() built-in).
    Tuples are also used for cases where an immutable sequence of homogeneous data is needed (such as allowing storage in a set or dict instance).

.. code-block:: python

    items = (1, 2, 3, 4)
    items = 1, 2, 3, 4

    for item in items:
        print item

    print items[0]
    print items[-2]

    a, b = 1, 2
    b, a = a, b

    print a, b

    items[0] = 1
    del items[0]


Set
---

https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

* Unordered collection of unique items
* Mutable
* Use frozenset for immutable
* Support for set operations

From the docs:

    A set object is an unordered collection of distinct hashable objects.
    Common uses include membership testing, removing duplicates from a sequence, and computing mathematical operations such as intersection, union, difference, and symmetric difference.
    (For other containers see the built-in dict, list, and tuple classes, and the collections module.)

.. code-block:: python

    items = set()

    items.add(1)
    items.add(2)
    items.add(1)

    items = set([1, 1, 2, 3, 4, 4])

.. code-block:: python

    # set operations

    numbers = range(100)
    odd     = range(1, 100, 2)

    even = set(numbers) - set(odd)
    even = list(even)  

    even = list(set(numbers) - set(odd))

.. code-block:: python

    import random

    items = random.sample(xrange(1000000), 10000)
    exclude = random.sample(xrange(1000000), 10000)

    result = [item for item in items if item not in exclude]

.. code-block:: python

    exclude = set(exclude)

    result = [item for item in items if item not in exclude]

.. code-block:: python
  
    items = set(items)
    exclude = set(exclude)

    result = list(items - exclude)

.. code-block:: python

    import random
    import timeit

    def filter_list():
        items = random.sample(xrange(1000000), 10000)
        exclude = random.sample(xrange(1000000), 10000)
        result = [item for item in items if item not in exclude]

    def filter_set():
        items = random.sample(xrange(1000000), 10000)
        exclude = random.sample(xrange(1000000), 10000)
        exclude = set(exclude)
        result = [item for item in items if item not in exclude]


    if __name__ == "__main__":

        t0 = timeit.timeit("filter_list()", "from __main__ import filter_list", number=100)
        t1 = timeit.timeit("filter_set()", "from __main__ import filter_set", number=100)

        print t0
        print t1


Dictionary
----------

https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

* Unordered collection of key-value pairs
* Values can be of any type.
* Keys have to be hashable (immutable): string, integer, float, tuple, frozenset
* Using strings as keys is the preferred standard

From the docs:

    A mapping object maps hashable values to arbitrary objects.
    Mappings are mutable objects.
    There is currently only one standard mapping type, the dictionary.
    (For other containers see the built-in list, set, and tuple classes, and the collections module.)

    A dictionary’s keys are almost arbitrary values.
    Values that are not hashable, that is, values containing lists, dictionaries or other mutable types (that are compared by value rather than by object identity) may not be used as keys.
    Numeric types used for keys obey the normal rules for numeric comparison: if two numbers compare equal (such as 1 and 1.0) then they can be used interchangeably to index the same dictionary entry.
    (Note however, that since computers store floating-point numbers as approximations it is usually unwise to use them as dictionary keys.)

.. code-block:: python

    items = {}

    items['1'] = 1 
    items['2'] = 2 
    items['3'] = 3
    items['4'] = 4 

    items = {'1': 1, '2': 2, '3': 3, '4': 4}

    # items = dict((str(key), value) for key, value in enumerate([1, 2, 3, 4]))
    # items = {str(key): value for key, value in enumerate([1, 2, 3, 4])}

    for key in items:
        value = items[key]
        print key, value

    for item in items.items():
        key = item[0]
        value = item[1]
        print key, value

    for item in items.items():
        key, value = item
        print key, value

    for key, value in items.items():
        print key, value

    for key, value in items.iteritems():
        print key, value

    keys = items.keys()
    key = keys[0]

    values = items.values()
    value = values[0]

    print key, value

    del items[key]

    # pop
    # popitem
    # setdefault
    # get

    # sort dictionary based on values


Built-in functions
==================

.. all, any, sum, min, max, str, repr, zip, enumerate, format, open, sorted, type

https://docs.python.org/3/library/functions.html

.. code-block:: python

    # range

    numbers = range(10)
    numbers = range(1, 10)
    numbers = range(0, 10, 2)
    numbers = range(1, 10, 2)

    # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

.. code-block:: python

    # all, any
    
    numbers = range(10)

    # numbers = range(0, 10, 2)
    # numbers = range(2, 10, 2)

    print(all(i % 2 == 0 for i in numbers))
    print(any(i % 2 == 0 for i in numbers))

.. code-block:: python
    
    # enumerate

    abc = ['a', 'b', 'c']

    i = 0
    for letter in abc:
        print i, letter
        i += 1

    for i in range(len(abc)):
        letter = abc[i]
        print i, letter

    for i, letter in enumerate(abc):
        print i, letter

.. code-block:: python

    # format

    # https://docs.python.org/2/library/string.html#formatspec
    # http://stackoverflow.com/questions/16683518/why-does-python-have-a-format-function-as-well-as-a-format-method

    from math import pi

    print format(pi, 'f')
    print format(pi, 'g')
    print format(pi, 'n')
    print format(pi, 'e')
    print format(pi, '')

    print '{0:f}'.format(pi)
    print '{0:.3f}'.format(pi)
    print '{0:.0f}'.format(pi)

    xyz = (1, 2, 3)

    print '{0[0]},{0[1]},{0[2]}'.format(xyz)
    print '{0},{1},{2}'.format(*xyz)

    xyz = {'x': 1, 'y': 2, 'z': 3}

    print '{0[x]},{0[y]},{0[z]}'.format(xyz)

.. code-block:: python

    # map
    # see also: list comprehensions

    pi = 3.14159

    map(str, [1, 2, 3])
    map(round, [pi, pi, pi], [1, 2, 3])
    map(pow, [1, 2, 3], [3, 3, 3])

.. code-block:: python

    # sorted

    from random import shuffle

    numbers = range(0, 100)
    shuffle(numbers)

    print numbers
    print sorted(numbers)

    numbers = map(str, numbers)

    print sorted(numbers)
    print sorted(numbers, key=int)
    print sorted(numbers, key=lambda x: int(x))

.. code-block:: python

    # zip

    rows = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    cols = zip(*rows)


Comprehensions
==============


List comprehensions
-------------------

Generate lists with an expression in brackets.


.. code-block:: python

    # odd  = range(1, 10, 2)
    # even = range(0, 10, 2) 

    numbers = [i for i in range(10)]
    odd     = [number for number in numbers if number % 2]
    even    = [number for number in numbers if number % 2 == 0]
    even    = [number for number in numbers if number not in odd]


.. code-block:: python

    # centroid (average)

    vertices = [[x, y, z], ...]
    centroid = [sum(axis) / len(vertices) for axis in zip(* vertices)]


Dict comprehensions
-------------------

.. code-block:: python

    # items = {1: 1, 2: 2, 3: 3, 4: 4}

    items = {index: value for index, value in enumerate(range(10))}


Functions
=========

Definitions
-----------

http://stackoverflow.com/questions/9872824/calling-a-python-function-with-args-kwargs-and-optional-default-arguments

.. code-block:: python

    def f():
        pass

    def f(a):
        pass

    def f(a1, a2):
        pass

    def f(a1, a2=None):
        pass

    def f(a1=None, a2):
        pass

    def f(*args):
        pass

    def f(**kwargs):
        pass

    def f(a1, a2, *args):
        pass

    def f(a1, a2, *args, **kwargs):
        pass


Variable Scope
--------------

.. code-block:: python

    globals()
    locals()


Default values
--------------

.. code-block:: python

    def f(a, b, c=[]):
        pass

    def f(a, b, c=None):
        if c is None:
            c = []

    def f(a, b, c=None):
        if not c:
            c = []

    def f(a, b, c=None):
        c = c or []


Classes
=======

.. code-block:: python

    class Vector():

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z


    class Vector():

        def __init__(self, x, y=0, z=0):
            try:
                len(x)
            except:
                x = [x, y, z]
            if len(x) == 1:
                x = [x[0], y, z]
            elif len(x) == 2:
                x = [x[0], x[1], z]
            self.x = x[0]
            self.y = x[1]
            self.z = x[2]


    class Vector():

        def __init__(self, end, start=None):
            if not start:
                start = [0, 0, 0]
            x = end[0] - start[0]
            y = end[1] - start[1]
            z = end[2] - start[2]
            self.x = x
            self.y = y
            self.z = z


.. code-block:: python

    class Vector():
        ...

        def add(self, other):
            self.x += other.x
            self.y += other.y
            self.z += other.z


.. code-block:: python

    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)

    v1.add(v2)


.. code-block:: python

    v3 = [0, 0, 1]

    v1.add(v3)


Magic methods
-------------

.. code-block:: python

    class Vector(object):
        ...

        def __getitem__(self, key):
            i = key % 3
            if i == 0:
                return self.x
            if i == 1:
                return self.y
            if i == 2:
                return self.z
            raise KeyError

        def __setitem__(self, key, value):
            i = key % 3
            if i == 0:
                self.x = value
                return
            if i == 1:
                self.y = value
                return
            if i == 2:
                self.z = value
                return
            raise KeyError

        def __iter__(self):
            return iter([self.x, self.y, self.z])

        def add(self, other):
            self.x += other[0]
            self.y += other[1]
            self.z += other[2]


    v1 = Vector(1, 0, 0)
    v2 = Vector(0, 1, 0)
    v3 = [0, 0, 1]

    v1.add(v2)
    v1.add(v3)


.. code-block:: python

    class Vector(object):
        ...

        def __add__(self, other):
            return Vector([self.x + other[0], self.y + other[1], self.z + other[2]])

        def __sub__(self, other):
            return Vector([self.x - other[0], self.y - other[1], self.z - other[2]])

        def __mul__(self, n):
            return Vector([self.x * n, self.y * n, self.z * n])

        def __pow__(self, n):
            return Vector([self.x ** n, self.y ** n, self.z ** n])


    v = v1 + v2
    v = v1 + v3
    v = v1 * 2
    v = v1 ** 2


Descriptors
-----------

`Descriptor HowTo Guide <https://docs.python.org/2/howto/descriptor.html>`_


.. code-block:: python

    class Vector(object):

        def __init__(self, end, start=None):
            self._x = None
            self._y = None
            self._z = None
            if not start:
                start = [0, 0, 0]
            x = end[0] - start[0]
            y = end[1] - start[1]
            z = end[2] - start[2]
            self.x = x
            self.y = y
            self.z = z

        @property
        def x(self):
            return self._x

        @x.setter
        def x(self, x):
            self._x = float(x)

        @property
        def y(self):
            return self._y

        @y.setter
        def y(self, y):
            self._y = float(y)

        @property
        def z(self):
            return self._z

        @z.setter
        def z(self, z):
            self._z = float(z)


.. code-block:: python

    class Vector(object):
        ...

        @property
        def length(self):
            return (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5


Classmethods
------------

.. code-block:: python

    class Vector(object):

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

        @classmethod
        def from_points(cls, start, end):
            x = end[0] - start[0]
            y = end[1] - start[1]
            z = end[2] - start[2]
            return cls(x, y, z)


    v = Vector.from_points([1, 0, 0], [2, 0, 0])


Meta Classes
------------


Abstract Base Classes
---------------------

.. code-block:: python

    from abc import ABCMeta
    from abc import abstractmethod


    class Vector(object):

        __metaclass__ = ABCMeta

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

        ...

        @abstractmethod
        def add(self, other):
            # raise NotImplementedError
            pass


    class Vector2(Vector):

        def add(self, other):
            ...


    class Vector3(Vector):

        def add(self, other):
            ...


Script, Module, Package
=======================

.. code-block:: python

    # simple script

    a = 1
    b = 2
    c = a + b

    print c


.. code-block:: python

    # script vs. module
    # http://stackoverflow.com/questions/419163/what-does-if-name-main-do

    def f1():
        ...

    def f2():
        ...

    if __name__ == '__main__':
        # this part is only executed when the module is run as a script
        # this part does not get executed when the module is imported
        # all other code will get executed when the module is imported!

        f1()
        f2()


.. code-block:: python

    # module a.py

    def b():
        print 'b'


    # script main.py

    from a import b

    b()


.. code-block:: python

    # packages
    #
    # - a
    #     __init__.py
    #     - b.py
    #         def b1():
    #             ...
    #         def b2():
    #             ...
    #     - c
    #         __init__.py
    #         d.py
    #             def d1():
    #                 ...
    #             def d2():
    #                 ...

    from a.b import b1
    import a.c.d
    from a.c.d import d2

    b1()

    a.c.d.d1()

    d2()


.. code-block:: python

    # a.__init__.py

    from b import b1
    from b import b2
    from c.d import d1
    from c.d import d2

    # main.py

    import a
    from a import b1

    a.d1()

    b1()


Core packages
=============

https://docs.python.org/3/library/index.html

* abc
* array
* ast
* calendar
* collections
* collections.abc
* colorsys
* contextlib
* copy
* csv
* ctypes
* inspect
* io
* itertools
* json
* math
* multiprocessing
* operators
* os
* platform
* random
* subprocess
* sys
* time
* traceback
* urllib2
* xml
* xmlrpclib


User packages
=============

* cairo: library for drawing vector graphics
* cvxopt: convex optimisation
* cvxpy: convex optimisation
* cython: optimising static compiler
* joblib: parallel for loops using multiprocessing
* matlab:
* matplotlib: (mainly) 2D plotting library
* meshpy: triangular and tetrahedral mesh generation
* networkx: creation, manipulation, and study of the structure, dynamics, and functions of complex networks
* numba: just-in-time compiler
* numpy: fundamental package for scientific computing
* pandas: data structures and data analysis tools
* paramiko:
* planarity:
* pycuda: binding of Nvidia's CUDA parallel computation API
* PyOpenGL: cross platform binding to OpenGL
* pyopt: nonlinear constrained optimization problems
* PySide: binding of the cross-platform GUI toolkit Qt
* scipy: scientific computing
* shapely: manipulation and analysis of planar geometric objects
* sphinx: documentation
* sympy: symbolic mathematics


Install Modules and Packages
============================

* `Python Packaging User Guide <http://python-packaging-user-guide.readthedocs.org/en/latest/installing/>`_
* `StackOverflow: Why use pip over easy_install? <http://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install>`_
* `Unofficial Windows Binaries for Python Extension Packages <http://www.lfd.uci.edu/~gohlke/pythonlibs/>`_
* `Anaconda Python distribution <http://docs.continuum.io/anaconda/index>`_
* `MacPorts <https://www.macports.org/>`_
