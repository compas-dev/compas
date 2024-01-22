********************************************************************************
Working in Rhino 8
********************************************************************************

.. warning::

    Support for the new Rhino 8 ScriptEditor is experimental.

.. info::

    The installation procedures listed here are for using COMPAS with CPython in Rhino 8.
    For using COMPAS with IronPython in Rhino 8, see :doc:`/userguide/cad.rhino`.


Installation
============

The installation of COMPAS in Rhino 8 can be done in two ways:

* by installing COMPAS in Rhino 8's Python environment using ``pip``, or
* by using the ``compas_rhino.install_with_pip`` command.

Using ``pip``
-------------

Rhino 8 comes with its own Python installation.
This procedure simply uses that Python installation and associated ``pip`` to install COMPAS.
It doesn't require an existing COMPAS installation on your system.

You need to know the path to the Python executable that comes with Rhino 8.
On macOS, this is typically something like ``~/.rhinocode/py39-rh8/python3.9``.

.. code-block:: bash

    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install compas


Using ``compas_rhino.install_with_pip``
---------------------------------------

**Under Construction...**


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

