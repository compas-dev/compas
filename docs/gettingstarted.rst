********************************************************************************
Getting started
********************************************************************************

Installation
============

The recommended way to install **COMPAS** is to use `Anaconda/conda <https://conda.io/docs/>`_::

    $ conda config --add channels conda-forge
    $ conda install COMPAS

But it can also be installed using `pip`::

    $ pip install COMPAS

To verify your setup, start Python from the command line and run the following:

.. code-block:: python

    >>> import compas
    >>> import compas_rhino
    >>> import compas_blender
    >>> import compas_ghpython

Optionally, you can also install from source.
Check the `Developer Guide <https://compas-dev.github.io/main/devguide.html>`_ for more info.
To install the *bleeding edge version* directly from the GitHub repo

::

    $ pip install git+https://github.com/compas-dev/compas.git


Updates
=======

**COMPAS** is still under very active development, with new versions being released
frequently. Updating your installation to the latest version is easy.

Using conda

::

    $ conda update COMPAS


Using pip

::

    $ pip install COMPAS --upgrade


Virtual environments
====================

One of the reasons to use virtual environments is be able to work with different versions
of Python and/or different versions and combinations of packages.
For example, if you have old code that was written for a version of Python or for
a version of a package that is incompatible with the current or latest version,
you can use a virtual environment to make sure you can keep running that code
without constantly having to update your entire development setup.

Create an environment using conda

::

    $ conda create -n OldCode


Create an environment with a specific version of Python

::

    $ conda create -n OldCode python=2.7


Install **COMPAS** (or other packages) for this environment

::

    $ conda install -n OldCode COMPAS=0.3.0


For further instructions about managing virtual environments with conda
`see the docs <https://conda.io/docs/user-guide/tasks/manage-environments.html>`_.


First Steps
===========

* https://compas-dev.github.io/main/examples.html
* https://compas-dev.github.io/main/tutorial.html
* https://compas-dev.github.io/main/api.html

