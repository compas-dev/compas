********************************************************************************
Working in Blender
********************************************************************************

.. rst-class:: lead

COMPAS packages can be installed in Blender and used in Blender scripts.
Blender is also a supported visualisation backend for COMPAS scenes,
and :mod:`compas_blender` provides functionality for converting COMPAS objects to Blender objects, and vice versa.

.. note::

    These instructions are for the latest version of Blender (4.0) and for the current LTS versions (3.3 and 3.6).

.. warning::

    The installation procedure is a work in progress.
    It has currently only been tested on macOS, and may change in the future.


Installation
============

The installation of COMPAS in Blender can be done in two ways:

* by installing COMPAS in Blender's Python environment using ``pip``, or
* by using the ``compas_blender.install`` command.

Using ``pip``
-------------

Blender comes with its own Python installation.
This procedure simply uses that Python installation and associated ``pip`` to install COMPAS.
It doesn't require an existing COMPAS installation on your system.

You need to know the path to the Python executable that comes with Blender.
On macOS, this is typically something like ``/Applications/Blender.app/Contents/Resources/4.0/python/bin/python3.10``.

.. code-block:: bash

    $ /Applications/Blender.app/Contents/Resources/4.0/python/bin/python3.10 -m pip install compas


Using ``compas_blender.install``
--------------------------------

The ``compas_blender.install`` command installs COMPAS in Blender's Python ``site-packages`` folder
by creating symlinks to COMPAS packages installed in an existing (``conda``) environment.
Therefore, before running the command below, you should activate the environment in which you have installed COMPAS.

.. code-block:: bash

    $ python -m compas_blender.install

Optionally, you can specify the version of Blender using the ``-v`` flag.

.. code-block:: bash

    $ python -m compas_blender.install -v 4.0

To remove all previously installed symlinks before installing new ones, use the ``--clean`` flag.

.. code-block:: bash

    $ python -m compas_blender.install --clean


Verification
============

To test if the installation was successful, you can run the following on the Blender command line.

>>> import compas
>>> print(compas.__version__)
'2.0.0'


Visualisation
=============

Visualisation of COMPAS objects in Blender is handled using viualisation scenes.
For more information on visualisation scenes, see :doc:`/userguide/basics.visualisation`.

.. figure:: /_images/userguide/cad.blender.visualisation.png

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas.scene import Scene

    mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

    scene = Scene()
    scene.clear()
    scene.add(mesh)
    scene.redraw()


Conversions
===========

More info coming soon...

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas_blender import conversions

    mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

    blender_mesh = conversions.mesh_to_blender(mesh)

    mesh = conversions.mesh_to_compas(blender_mesh)


Data Exchange
=============


Remote Procedure Calls
======================


Known Issues
============

