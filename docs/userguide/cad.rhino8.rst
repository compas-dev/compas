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


Using ``pip``
-------------

Rhino 8 comes with its own CPython executable (Python 3.9).
This procedure simply uses that executable and its associated ``pip`` to install COMPAS.
The location of the executable is different on different platforms.

* Windows: ``%USERPROFILE%\.rhinocode\py39-rh8\python.exe``
* macOS: ``~/.rhinocode/py39-rh8/python3.9``

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


Using ``compas_rhino.install_with_pip``
---------------------------------------

To simplify the above procedure, ``compas_rhino`` provides a convnience command.

.. warning::

    This command is experimental and may not yet work properly on your system.

Install from PyPI
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ python -m compas_rhino.install_with_pip compas


Install from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd /path/to/compas
    $ python -m compas_rhino.install_with_pip "-e ."


Verification
============

In Rhino 8, open the Python editor (just type ``ScriptEditor``), open an new ``Python 3`` edito tab, and type the following:

.. code-block:: python

    import compas
    print(compas.__version__)

If everything is installed correctly, this should print the version number of the installed COMPAS package.


Visualisation
=============

Visualisation of COMPAS objects in Rhino 8 is handled the same way as in other Rhino version, using viualisation scenes.
For more information on visualisation scenes, see :doc:`/userguide/basics.visualisation`.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas.scene import Scene

    mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

    scene = Scene()
    scene.clear()
    scene.add(mesh)
    scene.draw()


Conversions
===========


Data Exchange
=============


Remote Procedure Calls
======================


Known Issues
============

