********************************************************************************
Working in Blender
********************************************************************************

.. rst-class:: lead

COMPAS packages can be installed in Blender and used in Blender scripts.
Blender is also a supported visualisation backend for COMPAS scenes,
and :mod:`compas_blender` provides functionality for converting COMPAS objects to Blender objects, and vice versa.

.. note::

    These instructions are for the current LTS versions of Blender (3.3, 3.6 and 4.2).
    Other versions are currently not supported.

.. warning::

    The installation procedure is a work in progress.
    It has currently only been tested on macOS, and may change in the future.


Installation
============

The installation of COMPAS in Blender can be done in two ways:

* by installing COMPAS in Blender's Python environment using ``pip``, or
* by using the ``compas_blender.install`` command.

Using ``pip`` (recommended)
---------------------------

Blender comes with its own Python installation.
This procedure simply uses that Python installation and associated ``pip`` to install COMPAS.
The location of the executable is different on different platforms.
The default locations are:

* Windows: ``C:\Program Files\Blender Foundation\Blender 4.2\4.2\python\bin\python.exe``
* macOS: ``/Applications/Blender.app/Contents/Resources/4.2/python/bin/python3.10``
* Linux: ``/usr/share/blender/4.2/python/bin/python3.10`` (i think :)

.. note::

    If you already have an installation of COMPAS on your system, you can try finding the Blender Python executable by running the following in a terminal or command prompt:

    .. code-block:: python

        python -m compas_blender.print_python_path

Update `pip`
~~~~~~~~~~~~

Before installing `compas` with `pip`, it is highly recommended that you update `pip` itself.

.. code-block:: bash

    $ /Applications/Blender.app/Contents/Resources/4.2/python/bin/python3.10 -m pip install --upgrade pip


Install from PyPI
~~~~~~~~~~~~~~~~~

For example on Mac:

.. code-block:: bash

    $ /Applications/Blender.app/Contents/Resources/4.2/python/bin/python3.10 -m pip install compas


Install from Source
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    $ cd path/to/compas
    $ /Applications/Blender.app/Contents/Resources/4.2/python/bin/python3.10 -m pip install -e .


Using ``compas_blender.install``
--------------------------------

.. warning::

    This procedure will not install any of the dependencies required by COMPAS.
    They have to already be present in the Blender Python environment.

The ``compas_blender.install`` command installs COMPAS in Blender's Python ``site-packages`` folder
by creating symlinks to COMPAS packages installed in an existing (``conda``) environment.
Therefore, before running the command below, you should activate the environment in which you have installed COMPAS.

.. code-block:: bash

    $ python -m compas_blender.install

Optionally, you can specify the version of Blender using the ``-v`` flag.

.. code-block:: bash

    $ python -m compas_blender.install -v 4.2

To remove all previously installed symlinks before installing new ones, use the ``--clean`` flag.

.. code-block:: bash

    $ python -m compas_blender.install --clean


Verification
============

To test if the installation was successful, you can run the following on the Blender command line.

>>> import compas
>>> print(compas.__version__)
'2.4.0'


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
    scene.draw()


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
