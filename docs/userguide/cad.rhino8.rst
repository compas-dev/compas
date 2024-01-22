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

* by using the ``compas_rhino.install_with_pip`` command, or
* by installing COMPAS in Rhino 8's Python environment using ``pip`` directly.


Using ``compas_rhino.install_with_pip``
---------------------------------------

Rhino 8 comes with its own CPython executable (Python 3.9).
This procedure simply uses that executable and its associated ``pip`` to install COMPAS.

Install from PyPI
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ python -m compas_rhino.install_with_pip "compas"


Install from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd path/to/compas
    $ python -m compas_rhino.install_with_pip "-e ."


Using ``pip``
-------------

The procedure above assumes Rhino 8 is installed in the default location, and my require some user priviliges that are not always available.
If the procedure doesn't work, you can install COMPAS (and other python packages), using the Rhino CPython executable and ``pip`` directly.

To do so, you need to know the path to the Python executable that comes with Rhino 8.
On macOS, this is typically something like ``~/.rhinocode/py39-rh8/python3.9``.

Install from PyPI
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install compas


Install from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd /path/to/compas
    $ ~/.rhinocode/py39-rh8/python3.9 -m pip install -e .


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

