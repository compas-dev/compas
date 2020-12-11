.. _tut-blender:

*******
Blender
*******

To follow this tutorial, first install COMPAS for Blender as described
in the :ref:`Getting Started with Blender <gs-blender>`.

Blender redirects error messages of Python scripts to the ``stdout`` stream.
On Mac and Linuc, start Blender from the command line to be able to see those error messages.
On Windows this happens automatically.

Scripting Interface
===================

To switch to the scripting interface, simply select the "Scripting" tab of the main window.

The scripting interface has an embedded interactive Python terminal, which is located in the bottom half of the main window on the left.
If COMPAS was successfully installed you can use it to directly access the ``conda`` environment from where the installation was executed.

.. code-block:: python

    >>> import compas
    >>> import compas_blender
    >>> import numpy
    >>> import scipy
    >>> import bpy

The script editor is quite simple but good enough for basic development.
Line numbers and syntax highlighting should be on by default, but if that is not the case,
they can be turned on with toggle buttons at the top right of the area.
Further customisation of the editor appearance is possible by opening the sidebar from the "View" menu of the editor.

Basic Usage
===========

One of the main advantages of working in Blender is that Blender Python is CPython, and not IronPython like in Rhino and Grasshopper.
This means that all cool Python libraries are directly available and do not need to be accessed through remote procedure calls (RPC).
Especially for code that relies heavily on libraries such as Numpy and Scipy this simplifies the development process quite significantly.

.. code-block:: python

    import compas
    import compas_blender
    from compas.datastructures import Mesh
    from compas_blender.artists import MeshArtist

    compas_blender.clear()

    mesh = Mesh.from_ply(compas.get('bunny.ply'))

    artist = MeshArtist(mesh)
    artist.draw_mesh()


Data Blocks
-----------

Something worth explaining is the use of ``compas_blender.clear()`` in this script.
Blender uses (and re-uses) something called "data blocks".
Objects in the scene have instances of these data blocks assigned to them.
Multiple objects can be linked to the same data block.
As a result, simply deleting an object from the scene will delete the object but not the underlying data block.

If you run a script multiple times,
even if you delete the scene objects between consecutive runs,
you will accumulate the data blocks from previous runs and after a while Blender will become very slow.

``compas_blender.clear()`` attempts to clean up not only the scene objects but also the data blocks.
If somehow you still experience a slowdown, restarting Blender will help (all unused data blocks are then automatically removed).


Layers
------

There are no real layers in Blender; at least not like the layers in, for example, Rhino.
Therefore, the Blender artists have no optional ``layer`` parameter and no ``clear_layer`` method.
Instead, objects are grouped in collections, which can be turned on and off in the Blender UI similar to layers in Rhino.


Collections
-----------


Limitations
===========

``compas_blender`` is not yet as well developed as, ``compas_rhino`` and ``compas_ghpython``.
For example, COMPAS geometry objects do not yet have a corresponding artist in ``compas_blender``.
Artists are currently only available for data structures and robots.

There is also no official system yet for making custom COMPAS tools in Blender.
Therefore, COMPAS Blender development is somewhat limited to individual scripts.
