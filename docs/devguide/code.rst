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
    Names should short but descriptive and ideally unambiguous in the field they are intended to be used.

Classes should be names using the `CamelCase` convention

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

**COMPAS uses a line length of 120 characters**. This is longer than the 80 characters recommended by ``PEP8`` and in our opinion a more reasonable limit for modern displays.
This is enforces and can be automatically set using ``black -l 120``.

**Indentations are 4 spaces**. Some editors like VScode can be configured to insert 4 spaces when pressing the tab key.

Imports
-------

Imports are grouped in the following order with a blank line between each group:

1. Python standard library imports
2. Third party imports
3. Local application imports

Single-item imports are preferred over multi-item imports

.. code-block:: python

    from compas.geometry import Frame
    from compas.geometry import Point

    # instead of:
    from compas.geometry import Frame, Point

Star (`*`) imports should be avoided.

Comments
--------

The code should be self-explanatory and comments should be used sparingly. However, if a portion of the code is best understood in a certain context, a comment could be added.

.. code-block:: python

    def my_function():
        # while seems unlikely, 42 is the answer to everything
        some_piece_of_code() * thats_counter_intuitive() + 42

Docstrings
----------

Docstings in the COMPAS ecosystem follow the `NumPy style docstrings <https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html>`_.
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
Packages that will for sure not be used in Rhino can utilies Python 3 features.
