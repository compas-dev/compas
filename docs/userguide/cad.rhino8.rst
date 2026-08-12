********************************************************************************
Working in Rhino 8 (with CPython)
********************************************************************************

.. warning::

    Support for the new Rhino 8 Script Editor is experimental.


Rhino 8 supports both CPython and IronPython.
The instructions on this page are for working with COMPAS in the new Script Editor using CPython.
More information about the Script Editor is available here: <https://www.rhino3d.com/features/developer/scripting/>

For working with COMPAS in Rhino 8 with IronPython,
or for information about working in earlier versions of Rhino, see :doc:`/userguide/cad.rhino`.

.. note::

    To launch Rhino 8 Script Editor, simply type `ScriptEditor` at the Rhino 8 command prompt.

Installation
============

To use COMPAS packages in your Rhino 8 CPython scripts,
you can now simply add the packages as requirements in a comment.

.. code-block:: python

    #! python3
    # r: compas

    import compas
    from compas.datastructures import Mesh

    mesh = ...

More information is available here: <https://developer.rhino3d.com/guides/scripting/scripting-command>

.. note::

    This also works in the Python 3 Script node in Grasshopper.

Alternative Method
==================

The above method only works if the package you want to install is available on `PyPI <https://pypi.org/>`_.
If you want to install a package from local source,
you can use `pip` directly in combination with the Python executable that is included in Rhino.
The default location of the executable is different for Windows and Mac.

* Windows: ``%USERPROFILE%\.rhinocode\py39-rh8\python.exe``
* macOS: ``~/.rhinocode/py39-rh8/python3.9``

.. code-block:: bash

    $ cd path/to/compas
    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install .

To create an editable install, you should update `pip` itself, first.

.. code-block:: bash

    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install --upgrade pip

.. code-block:: bash

    $ cd path/to/compas
    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install -e .


Experimental Method
===================

COMPAS now makes the `install_in_rhino` command line utility available to simplify the installation of Python packages in Rhino 8 CPython.
This utility is available after installing the main `compas` package:

Install any Python package from PyPI

.. code-block:: bash

    install_in_rhino requests numpy

Install from the current directory

.. code-block:: bash

    install_in_rhino .

Install from a local path

.. code-block:: bash

    install_in_rhino path/to/package

Install from a requirements file

.. code-block:: bash

    install_in_rhino -r requirements.txt

Install in a specific site environment.

.. code-block:: bash

    install_in_rhino compas --env compas-dev

Clear the site environment before installing

.. code-block:: bash

    install_in_rhino compas --env compas-dev --clear


For more information, see :func:`compas_rhino.install_with_pip.install_in_rhino_with_pip`.


Verification
============

In Rhino 8, open the Python editor (just type ``ScriptEditor``), open an new ``Python 3`` edito tab, and type the following:

.. code-block:: python

    import compas
    print(compas.__version__)

If everything is installed correctly, this should print the version number of the installed COMPAS package.
