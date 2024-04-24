.. _code-contributions:

Code Contributions
===================

.. note::
    For the proper way of contributing code to COMPAS, please follow the :ref:`development-workflow`.

To keep code clean, consistent and readable we try to follow the following guidelines when developing COMPAS.
Generally, we try to follow the `PEP8 <https://peps.python.org/pep-0008/>`_ style guide for Python code.

Naming conventions
------------------

.. note::

    When naming **variables**, **functions**, **classes** and **modules** it is important to take the time and choose meaningful names.
    Names should be short but descriptive and ideally unambiguous in the field they are intended to be used.

**Classes** should be named using the ``CamelCase`` convention

.. code-block:: python

    class MyClass(object):
        ...

**Functions**, **methods**, **arguments** and **local/member variables** should be named using the ``snake_case`` convention

.. code-block:: python

    def my_function():
        ...

    def add(self, x, y):
        result = x + y
        return result

**Functions**, **methods** and **member variables** which are intended for internal use only should be prefixed with an ``_`` (underscore)

.. code-block:: python

    class Rectangle(object):

        def __init__(self, width, lentgh):
            self._width = width
            self._length = length
            self._area = None
            self._init_class()

        def _init_class():
            self._area = self._width * self._length

        @staticmethod
        def _some_helper_function():
            ...


**Class attributes** should be named using all caps and underscores

.. code-block:: python

    class MyClass(object):
        MY_CONSTANT = 42

        def __init__(self):
            self.my_attribute = 0

        def my_method(self):
            return self.my_attribute + self.MY_CONSTANT

Line length
-----------

**COMPAS uses a line length of 180 characters**. While longer than the 80 characters recommended by ``PEP8``, it is in our opinion a more reasonable limit for modern displays.

**Indentations are 4 spaces**. Tab to spaces setting can be set in ``.editorconfig`` which is respected by most editors. For more information see `EditorConfig <https://editorconfig.org/>`_.

Imports
-------

Imports are grouped in the following order with a blank line between each group:

1. Python standard library imports
2. Third party imports
3. Local application imports

Single-item imports are preferred over multi-item imports

.. code-block:: python

    # use:
    from compas.geometry import Frame
    from compas.geometry import Point

    # instead of:
    from compas.geometry import Frame, Point

Star (``*``) imports should be avoided.

Second-level imports
--------------------
To keep the API clean and consistent, any new public functions or classes should be importable from a second-level package.
This is achieved by importing the function or class in the ``__init__.py`` file of the package.

For example:

.. code-block:: bash

    compas
    ├── __init__.py
    └── my_package
        ├── __init__.py
        └── new_module.py

.. code-block:: python

    # new_module.py
    class NewClass(object):
        ...

.. code-block:: python

    # compas.my_package.__init__.py
    from .new_module import NewClass

    __all__ = ['NewClass']

The result should be:

.. code-block:: python

    >>> from compas.my_package import NewClass

Comments
--------

The code should be self-explanatory and comments should be used sparingly. However, if a portion of the code is best understood in a certain context, a comment could be added.

.. code-block:: python

    def my_function():
        # while seems unlikely, 42 is the answer to everything
        return some_piece_of_code() + 42

Docstrings
----------

Docstings in the COMPAS ecosystem follow the `NumPy style docstrings <https://numpydoc.readthedocs.io/en/latest/format.html>`_.
These docstrings are later used by `Sphinx <https://www.sphinx-doc.org/en/master/>`_ to generate the API documentation.

Therefore, it is important that functions and methods have at least the following docstrings:

.. code-block:: python

        def my_function(point, line):
            """This is a one-line description of the function.

            This is a longer description of the function.
            It can span multiple lines.

            Parameters
            ----------
            point : :class:`~compas.geometry.Point`
                Point to check.
            line : :class:`~compas.geometry.Line`
                Line to analyze.

            Returns
            -------
            :class:`~compas.geometry.Plane`
                The resulting plane of the operation.

            """
            ...

Python 2.7 compatibility
------------------------

**To keep COMPAS usable in Rhino, we make sure to maintain Python 2.7 compatibility** in parts of the package which are used in Rhino.
Packages that are not intended to be used in Rhino can utilise Python 3 features.
