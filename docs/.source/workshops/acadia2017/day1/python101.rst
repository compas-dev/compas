.. _acadia2017_day1_python101:

********************************************************************************
Python 101
********************************************************************************

The compas framework is based on Python.
Python 3 is fully supported and the code is backwards compatible with Python +2.6.


Built-in types and functions
============================

* https://docs.python.org/3/library/stdtypes.html
* https://docs.python.org/3/library/functions.html

============= =========== ============ ========== ==============
abs()         dict()      help()       min()      setattr()
all()         dir()       hex()        next()     slice()
any()         divmod()    id()         object()   sorted()
ascii()       enumerate() input()      oct()      staticmethod()
bin()         eval()      int()        open()     str()
bool()        exec()      isinstance() ord()      sum()
bytearray()   filter()    issubclass() pow()      super()
bytes()       float()     iter()       print()    tuple()
callable()    format()    len()        property() type()
chr()         frozenset() list()       range()    vars()
classmethod() getattr()   locals()     repr()     zip()
compile()     globals()   map()        reversed() __import__()
complex()     hasattr()   max()        round()      
delattr()     hash()      memoryview() set()
============= =========== ============ ========== ==============

* numeric types: :obj:`int`, :obj:`float`, :obj:`complex`
* iterator types: 
* sequence types: :obj:`list`, :obj:`tuple`, :obj:`range`
* text sequence type: :obj:`str`
* binary sequence types: :obj:`bytes`, :obj:`bytearray`, :obj:`memoryview`
* set types: :obj:`set`, :obj:`frozenset`
* mapping types: :obj:`dict`
* context manager types:
* other types: modules, classes and class instances, functions, methods,
  code objects, type objects), null object (``None``),
  ellipsis object (``...``), notimplemented object (``NotImplemented``),
  boolean values (``True``, ``False``), internal objects


Container types
===============

https://wiki.python.org/moin/TimeComplexity

List
----

https://docs.python.org/3/library/stdtypes.html#lists

* Ordered collection of items of any type.
* **Mutable**

.. code-block:: python

    items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

.. code-block:: python

    # indexing & slicing

    items[0]     # 0  
    items[-1]    # 9

    items[:5]    # [0, 1, 2, 3, 4]
    items[5:]    # [5, 6, 7, 8, 9]

    items[::-1]  # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    items[::2]   # [0, 2, 4, 6, 8]

.. code-block:: python

    # methods

    items = [0, 1, 2, 3, 4, 5]

    items.append(6)                  # [1, 2, 3, 4, 5, 6]
    items.insert(0, 0)               # [0, 1, 2, 3, 4, 5, 6]
    items.extend([7, 8, 9, 10, 11])  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    items.pop()                      # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    items.remove(-1)                 # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


Tuple
-----

https://docs.python.org/3/library/stdtypes.html#tuples

* Ordered collection of items of any type.
* **Immutable**

.. code-block:: python

    rgb = 255, 0, 0

    rgb[0]  # 255
    rgb[1]  # 0
    rgb[2]  # 0

.. code-block:: python

    rgb[0] = 0
    rgb[1] = 255


Set
---

https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

* Unordered collection of distinct hashable objects.
* **Mutable**

.. code-block:: python

    items = set([1, 2, 3, 4])

.. code-block:: python
    
    # membership testing
    # removing duplicates
    # set operations

    from random import sample
    from timeit import timeit

    n = 100000
    m = 10000

    items = sample(range(n), m)
    exclude = sample(range(n), m)

    result = set(items) - set(exclude)
    result = [i for i in items if i not in exclude]

    # timeit("result = set(items) - set(exclude)", "from __main__ import items, exclude", number=10)
    # timeit("result = [i for i in items if i not in exclude]", "from __main__ import items, exclude", number=10)

    # 0.02
    # 12.58


Dictionary
----------

https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

* Maps hashable values (*keys*) to arbitrary objects
* Mutable
* Unordered

.. code-block:: python

    items = {'1': 1, '2': 2, '3': 3, '4': 4}

    for key in items:
        print key, items[key]

    for key in items.keys():
        print key, items[key]

    for key, value in items.items():
        print key, value

    for value in items.values():
        print value

.. code-block:: python

    # pop
    # popitem
    # setdefault
    # get

.. code-block:: python

    # sort dictionary based on values

**Example**

Given a set of lines, defined by start and end point coordinates,
determine the connectivity of the lines.

.. code-block:: python

    import compas
    from compas.files import OBJReader

    obj = OBJReader(compas.get('lines.obj'))

    index_key = {}
    vertex = {}

    for index, xyz in enumerate(iter(obj.vertices)):
        key = '{0[0]:.3f},{0[1]:.3f},{0[2]:.3f}'.format(xyz)
        index_key[index] = key
        vertex[key] = xyz

    # for index in index_key:
    #     print index, index_key[index], vertex[index_key[index]]

    key_index = {key: index for index, key in enumerate(vertex.keys())}
    index_index = {index: key_index[key] for index, key in iter(index_key.items())}

    vertices = [xyz for xyz in iter(vertex.values())]
    lines    = [[index_index[index] for index in line] for line in obj.lines if len(line) == 2]

    # print vertices
    # print lines


Comprehensions
==============

List comprehensions
-------------------

Generate lists with an expression in brackets.

.. code-block:: python

    # list construction

    numbers = [n for n in range(10)]
    odd     = [n for n in range(10) if n % 2 == 1]
    even    = [n for n in range(10) if n % 2 == 0]
    squares = [n ** 2 for n in range(10)]
    even    = [n if n % 2 == 0 else None for n in range(10)]

.. code-block:: python

    # vector length

    vector = [1.0, 0.0]
    length = sum([x ** 2 for x in vector]) ** 0.5

.. code-block:: python

    # dot product

    vectors = [[1.0, 0.0], [0.0, 1.0]]
    dot = sum([a * b for a, b in zip(* vectors)])

.. code-block:: python

    # centroid

    points = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
    centroid = [sum(axis) / len(vertices) for axis in zip(* vertices)]


Dict comprehensions
-------------------

.. code-block:: python

    items = {index: value for index, value in enumerate(range(10))}


Functions
=========

.. code-block:: python

    def f():
        pass

    def f(a):
        pass

    def f(a, b):
        pass

    def f(a, b=None):
        print(a, b)

    # f('a')      => 'a', None
    # f('a', 'b') => 'a', 'b' 

    def f(*args):
        print(args)

    # f('a')           => ['a']
    # f('a', 'b', 'c') => ['a', 'b', 'c']

    def f(**kwargs):
        pass

    def f(a, b, *args):
        pass

    def f(a, b, *args, **kwargs):
        pass


Classes
=======

.. code-block:: python

    class Vector():

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z


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
