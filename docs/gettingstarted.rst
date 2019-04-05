********************************************************************************
Getting started
********************************************************************************

.. highlight:: bash


Installation
============

The recommended way to install COMPAS is to use `Anaconda/conda <https://conda.io/docs/>`_

::

    $ conda config --add channels conda-forge
    $ conda install COMPAS


But it can also be installed using `pip`

::

    $ pip install COMPAS


To verify your setup, start Python from the command line and run the following:

::

    >>> import compas
    >>> import compas_rhino
    >>> import compas_blender
    >>> import compas_ghpython


Updates
=======

COMPAS is still under very active development, with new versions being released
frequently. Updating your installation to the latest version is easy.

Using conda

::

    $ conda update COMPAS


Using pip

::

    $ pip install COMPAS --upgrade


Virtual environments
====================

One of the reasons to use virtual environments is to isolate dependencies, to
be able to create a fully reproducible setup, and to be able to work with
different versions of Python and/or different versions and combinations of
packages.

For example, if you work on a project that requires a specific version of Python or
a specific version of a package that is incompatible with the ones required by another
project, you can use environments to make sure both projects can run side-by-side
without constantly having to update your entire development setup.

Create an environment using conda

::

    $ conda create -n my-project


Create an environment with a specific version of Python

::

    $ conda create -n my-project python=3.6


Install COMPAS (or other packages) for this environment

::

    $ conda install -n my-project COMPAS=0.5.1


For further instructions about managing virtual environments with conda
`see the docs <https://conda.io/docs/user-guide/tasks/manage-environments.html>`_.


First Steps
===========

* https://compas-dev.github.io/main/examples.html
* https://compas-dev.github.io/main/tutorial.html
* https://compas-dev.github.io/main/api.html


Known Issues
============

Plotter errors
--------------

**Problem** You get an error similar to the following when trying to run
anything involving a `Plotter` (or even just `matplotlib`)

.. code-block:: none

    2019-04-02 16:10:39.181 python[2619:857913] -[NSApplication _setup:]: unrecognized selector sent to instance 0x7f8c389244b0
    2019-04-02 16:10:39.183 python[2619:857913] *** Terminating app due to uncaught exception 'NSInvalidArgumentException', reason: '-[NSApplication _setup:]: unrecognized selector sent to instance 0x7f8c389244b0'
    *** First throw call stack:
    (
        0   CoreFoundation                      0x00007fff33adbecd __exceptionPreprocess + 256
        1   libobjc.A.dylib                     0x00007fff5fba3720 objc_exception_throw + 48
        2   CoreFoundation                      0x00007fff33b59275 -[NSObject(NSObject) __retain_OA] + 0
        3   CoreFoundation                      0x00007fff33a7db40 ___forwarding___ + 1486
        4   CoreFoundation                      0x00007fff33a7d4e8 _CF_forwarding_prep_0 + 120
        5   libtk8.6.dylib                      0x000000011c566154 TkpInit + 324
        6   libtk8.6.dylib                      0x000000011c4be0ee Initialize + 2622
        7   _tkinter.cpython-37m-darwin.so      0x0000000118bf3a3f _tkinter_create + 1183
        8   python                              0x000000010a706fe6 _PyMethodDef_RawFastCallKeywords + 230
        9   python                              0x000000010a8438b2 call_function + 306
        10  python                              0x000000010a841565 _PyEval_EvalFrameDefault + 46165

        ...

        60  python                              0x000000010a6d942d main + 125
        61  libdyld.dylib                       0x00007fff60c71ed9 start + 1
        62  ???                                 0x0000000000000002 0x0 + 2
    )
    libc++abi.dylib: terminating with uncaught exception of type NSException
    Abort trap: 6

**Solution** Install python.app

From https://matplotlib.org/faq/osx_framework.html:

The default python provided in (Ana)conda is not a framework build.
However, a framework build can easily be installed,
both in the main environment and in conda envs:
install python.app (``conda install python.app``)
and use ``pythonw`` rather than ``python``.

To install python.app when you create an environment do

::

    $ conda create -n myenv -c conda-forge python=3.7 python.app COMPAS


To install python.app in an already existing environment

::

    $ conda activate myenv
    $ conda install python.app
