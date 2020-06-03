===============
Developer Guide
===============

This guide is intended for people who want to contribute to the code and documentation
of the core COMPAS packages:

* :mod:`compas`
* :mod:`compas_blender`
* :mod:`compas_ghpython`
* :mod:`compas_plotters`
* :mod:`compas_rhino`

Note, however, that the general procedure is applicable to all COMPAS package development.

Setup/Installation
==================

To set up a developer environment

1. Fork [the repository](https://github.com/compas-dev/compas) and clone the fork.
2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).

.. code-block:: bash

    conda create -n compas-dev python=3.7
    conda activate compas-dev

3. Install development dependencies:

.. code-block:: bash

    cd path/to/compas
    pip install -r requirements-dev.txt

4. Make sure all tests pass:

.. code-block:: bash

    invoke test

5. Create a branch for your contributions.

.. code-block::

    git branch title-proposed-changes
    git checkout title-proposed-changes

6. Start making changes!


Submitting a PR
===============

Once you are done making changes, you have to submit your contribution through a pull request (PR).
The procedure for submitting a PR is the following.

1. Make sure all tests still pass:

.. code-block:: bash

    invoke test

2. Add yourself to `AUTHORS.md`.
3. Commit your changes and push your branch to GitHub.
4. Create a [pull request](https://help.github.com/articles/about-pull-requests/) through the GitHub website.

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `invoke clean`: Clean all generated artifacts.
* `invoke check`: Run various code and documentation style checks.
* `invoke docs`: Generate documentation.
* `invoke test`: Run all tests and checks in one swift command.


Style guide
===========

* PEP 8
* flake8
* naming conventions
* consistency
* foolish consistency
* principle of least astonishment


Documentation
=============

* sphinx
* RestructuredText
* docs structure
* api docs
  * napoleon
  * Numpy-style
* examples
* references
* see also


Code structure
==============

Each of the core packages is divided into subpackages that group functionality into logical components.
For example, :mod:`compas` is divided into:

* :mod:`compas.datastructures`
* :mod:`compas.files`
* :mod:`compas.geometry`

The API of each subpackage is documented in the docstring of its ``__init__.py`` file using basic RestructuredText.
From outside of these packages, functionality should be imported directly from the subpackage level,
regardless of the code structure underneath.

For example, in some ``script.py``:

.. code-block:: python

    from compas.geometry import add_vectors
    from compas.geometry import oriented_bounding_box_numpy
    from compas.geometry import Polygon
    from compas.geometry import Transformation

    from compas.numerical

To allow the public API of the modules and packages contained in a subpackage to reach the subpackage level,
each module should declare the classes, functions and variables of its public API in the module's ``__all__`` variable.
Per package, the APIs of the contained module are collected in ``__all__`` variable of the package (in the ``__init__.py``).

.. code-block:: python

    __all__ = [_ for _ in dir() if not _.startswith('_')]



Numpy/Numba/... implementations
===============================


Testing
=======

