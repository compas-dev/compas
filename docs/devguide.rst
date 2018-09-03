********************************************************************************
Developer Guide
********************************************************************************

.. warning::

    Under construction...


This guide provides basic information about setting up a development environment
and writing code for the **COMPAS** framework.

For instructions on how to submit contributions, see `Contributions <https://compas-dev.github.io/main/contributions.html>`_


Installation
============

* https://pip.pypa.io/en/stable/user_guide
* https://pip.pypa.io/en/stable/reference/pip_install


1. clone repo
2. install from source (dependencies + dev tools)

::

    $ pip install -r requirements-dev.txt


Writing code
============

* https://www.python.org/dev/peps/pep-0008/
* https://www.python.org/dev/peps/pep-0020/


Naming conventions
==================

* US English

  * https://en.wikisource.org/wiki/The_Elements_of_Style
  * https://en.wikipedia.org/wiki/The_Elements_of_Programming_Style



Package structure
=================

* https://github.com/audreyr/cookiecutter


Module structure
================


Docstrings
==========

* We use the `sphinxcontrib` extension *Napoleon - Marching towards legible docstrings* (https://sphinxcontrib-napoleon.readthedocs.io/en/latest/)
* We prefer Numpy-style docstrings (https://numpydoc.readthedocs.io/en/latest/format.html)
*


Testing
=======

* We use `pytest` for writing unit tests

Benchmarking
============


