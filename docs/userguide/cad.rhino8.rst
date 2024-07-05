********************************************************************************
Working in Rhino 8
********************************************************************************

.. warning::

    Support for the new Rhino 8 ScriptEditor is experimental.

.. note::

    The installation procedures listed here are for using COMPAS with CPython in Rhino 8.
    For using COMPAS with IronPython in Rhino 8, see :doc:`/userguide/cad.rhino`.


Installation
============

Rhino 8 comes with its own CPython executable (Python 3.9).
This procedure simply uses that executable and its associated ``pip`` to install COMPAS.
The location of the executable is different on different platforms.

* Windows: ``%USERPROFILE%\.rhinocode\py39-rh8\python.exe``
* macOS: ``~/.rhinocode/py39-rh8/python3.9``

.. note::

    If you already have an installation of COMPAS on your system, you can try finding the Rhino 8 Python executable by running the following in a terminal or command prompt:

    .. code-block:: bash

        python -m compas_rhino.print_python_path

Update `pip`
~~~~~~~~~~~~

Before installing `compas` with `pip`, it is highly recommended that you update `pip` itself.

.. code-block:: bash

    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install --upgrade pip


Install from PyPI
~~~~~~~~~~~~~~~~~

For example on Mac:

.. code-block:: bash

    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install compas


Install from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd path/to/compas
    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install -e .


Verification
============

In Rhino 8, open the Python editor (just type ``ScriptEditor``), open an new ``Python 3`` edito tab, and type the following:

.. code-block:: python

    import compas
    print(compas.__version__)

If everything is installed correctly, this should print the version number of the installed COMPAS package.
