********************************************************************************
Working in Blender
********************************************************************************

.. rst-class:: lead

COMPAS packages can be installed in Blender and used in Blender scripts.
Blender is also a supported visualisation backend for COMPAS scenes,
and :mod:`compas_blender` provides functionality for converting COMPAS objects to Blender objects, and vice versa.

.. note::

    COMPAS is distributed as a Blender extension for Blender 4.2 and newer.
    Older versions of Blender are not supported.


Installation
============

COMPAS is packaged as a `Blender extension <https://docs.blender.org/manual/en/latest/advanced/extensions/index.html>`_.
The extension is self-contained: it bundles COMPAS and its dependencies (except ``numpy``, which ships with Blender),
so there is no need to install anything into Blender's Python environment manually.

Blender ships different versions of Python, and some dependencies contain compiled code,
so there is one extension package per Blender version range and operating system:

=========================  =======================================================
Blender                    Extension package
=========================  =======================================================
4.2 to 5.0                 ``compas-<version>-blender4.2-<platform>.zip``
5.1 and newer              ``compas-<version>-blender5.1-<platform>.zip``
=========================  =======================================================

where ``<platform>`` is one of ``windows_x64``, ``windows_arm64`` (Blender 5.1+ only),
``macos_arm64``, ``macos_x64`` (Blender 4.2 to 5.0 only) or ``linux_x64``.

Install from disk
-----------------

1. Download the extension package for your Blender version and operating system from the
   `COMPAS releases <https://github.com/compas-dev/compas/releases>`_.
2. In Blender, open *Edit > Preferences > Get Extensions*.
3. In the drop-down menu in the top right corner, select *Install from Disk...* and pick the downloaded ``.zip`` file.

Alternatively, drag and drop the ``.zip`` file onto the Blender window,
or install it from the command line:

.. code-block:: bash

    $ blender --command extension install-file -r user_default -e compas-<version>-blender5.1-macos_arm64.zip

Once the extension is enabled, ``compas`` and ``compas_blender`` can be imported in the Python console,
in scripts in the Text Editor, and from other add-ons.
To update COMPAS, install the package of the newer version in the same way.
To uninstall it, remove the extension from the *Get Extensions* panel.

Build from source
-----------------

To build the extension packages from a checkout of the COMPAS repository,
you need a Python environment with ``pip`` and a Blender executable (4.2 or newer):

.. code-block:: bash

    $ cd path/to/compas
    $ invoke build-blender-extension --blender /Applications/Blender.app/Contents/MacOS/Blender

This builds a ``compas`` wheel from the source, downloads the wheels of all dependencies for every supported
platform and Python version, and writes the extension packages to ``dist/blender``.
See ``extensions/blender/build.py`` for more options.


Verification
============

To test if the installation was successful, you can run the following on the Blender Python console.

>>> import compas
>>> print(compas.__version__)
'2.15.0'


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
