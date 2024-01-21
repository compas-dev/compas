********************************************************************************
Working in Rhino 8
********************************************************************************

.. warning::

    Support for CPython scripting in the Rhino 8 ScriptEditor is experimental.


Installation
============

The installation of COMPAS in Rhino 8 can be done in two ways:

* by installing COMPAS in Rhino 8's Python environment using ``pip``, or
* by using the ``compas_rhino8.install`` command.

Using ``pip``
-------------

Rhino 8 comes with its own Python installation.
This procedure simply uses that Python installation and associated ``pip`` to install COMPAS.
It doesn't require an existing COMPAS installation on your system.

You need to know the path to the Python executable that comes with Rhino 8.
On macOS, this is typically something like ``~/.rhinocode/py39-rh8/python3.9``.

.. code-block:: bash

    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install compas


Using ``compas_rhino8.install``
-------------------------------

.. warning::

    This installation procedure will only install the specified COMPAS packages.
    The dependencies and requirements of these packages are not installed automatically.
    We recommend using the procedure with ``pip`` described above instead.


The ``compas_rhino8.install`` command installs COMPAS in Rhino 8's Python ``site-packages`` folder
by creating symlinks to COMPAS packages installed in an existing (``conda``) environment.
Therefore, before running the command below, you should activate the environment in which you have installed COMPAS.

.. code-block:: bash

    $ python -m compas_rhino8.install

To remove all previously installed symlinks before installing new ones, use the ``--clean`` flag.

.. code-block:: bash

    $ python -m compas_rhino8.install --clean


Verification
============


Visualisation
=============


Conversions
===========


Data Exchange
=============


Remote Procedure Calls
======================


Known Issues
============

