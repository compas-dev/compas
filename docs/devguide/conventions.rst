***********
Conventions
***********

Style guide
===========

Please run ``invoke format`` to auto-format your code.

The command ``invoke lint`` runs the entire codebase through both ``black`` and ``flake8``.
As described in the `docs <https://flake8.pycqa.org/en/latest/manpage.html>`_,
``flake8`` includes lint checks provided by the PyFlakes project,
PEP-0008 inspired style checks provided by the PyCodeStyle project,
and McCabe complexity checking provided by the McCabe project.

The list of potential error codes issued by ``flake8`` are available here:
https://flake8.pycqa.org/en/latest/user/error-codes.html

The PEP-0008 style guide is available here:
https://www.python.org/dev/peps/pep-0008/

Note that the maximum line length is set to 120 rather 79 in the ``setup.cfg`` of the repo.


Naming conventions
==================

We (intend to) use the following naming conventions.

1. variables, functions, methods, attributes use "snake_case":
   they are written in lowercase and spaces between words are replaced by underscores.

2. class names use (Upper) "CamelCase":
   The are written in lowercase, with the first letter of each word capitalized
   and spaces between words removed.

3. module or package level variables are in uppercase
   and with spaces between words replaced by underscores.


Quotes
======

Ideally, we would use the following conventions for quotes.

1. Double quotation marks for multiline statements and docstrings.
   For example, ``"""Calculate the sum of two numbers."""``

2. Single quotation marks for strings that are used "as variables".
   For example, ``config['param'] = 1``.

3. Double quotation marks for strings that are meant to be used as text.
   For examples, ``message = "Select one or more points."``


Documentation
=============

The documentation of COMPAS is generated with Sphinx.
This means that code docstrings and general documentation pages
have to be written in RestructuredText.

Each function, method, and class should have a docstring describing its behaviour.
We use ``sphinx.ext.napoleon`` to allow for human-readable docstrings,
and prefer Numpy-style docstring formatting rules.

* https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
* https://numpydoc.readthedocs.io/en/latest/format.html

To include a new function or class in the documentation,
it should be added to the API docstring in ``__init__.py`` of the main package it belongs to.

For example, if you add a function somewhere in the geometry package,
make sure to include it in the docstring of ``compas.geometry.__init__.py``.


Type hints
==========

Type hints should be added to stub files at the public API level
of the main packages (see :ref:`code-structure`).
This allows the type hints to be written using Python 3 style
annotations while maintaining compatibility with Python 2.7 for Rhino/GH.

For example, the type hints for ``compas.datastructures`` should be defined in
``compas.datastructures.__init__.pyi``.


.. _code-structure:

Code structure
==============

Each of the core packages is divided into subpackages that group functionality into logical components.
For example, :mod:`compas` is divided into:

* :mod:`compas.datastructures`
* :mod:`compas.files`
* :mod:`compas.geometry`
* :mod:`compas.numerical`
* :mod:`compas.robots`
* :mod:`compas.rpc`
* :mod:`compas.topology`
* :mod:`compas.utilities`

The API of each subpackage is documented in the docstring of its ``__init__.py`` file using basic RestructuredText.
From outside of these packages, functionality should be imported directly from the subpackage level,
regardless of the code structure underneath.

For example, in some ``script.py``:

.. code-block:: python

    from compas.datastructures import Mesh
    from compas.datastructures import Network

    from compas.geometry import add_vectors
    from compas.geometry import oriented_bounding_box_numpy
    from compas.geometry import Polygon
    from compas.geometry import Transformation

    from compas.numerical import pca_numpy
    from compas.numerical import fd_numpy

To allow the public API of the modules and packages contained in a subpackage to reach the subpackage level,
each module should declare the classes, functions and variables of its public API in the module's ``__all__`` variable.
Per package, the APIs of the contained module are collected in the ``__all__`` variable of the package (in the ``__init__.py``).

.. code-block:: python

    __all__ = [_ for _ in dir() if not _.startswith('_')]
