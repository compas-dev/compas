***********
First Steps
***********

Once COMPAS is installed, you can start using it in your Python scripts.
On this page are a few simple snippets to get you started.

.. note::

    The visualisations shown on this page are generated with the COMPAS Viewer in VS Code.
    See :doc:`basics.visualisation` for more information on how to set it up and use it.

    Alternatively, you can run the examples in Rhino or Blender.
    See :doc:`cad.rhino` and :doc:`cad.blender` for more information on how to get started with that.


A Simple Box
============

.. code-block:: python

    from compas.geometry import Box
    from compas.scene import Scene

    box = Box(1, 1, 1)

    scene = Scene()
    scene.add(box)
    scene.redraw()


Points-in-box Test
==================

.. code-block:: python

    from compas.geometry import Box, Pointcloud
    from compas.colors import Color
    from compas.scene import Scene

    box = Box(1, 1, 1)
    pcl = Pointcloud.from_bounds(x=10, y=10, z=10, n=100)

    box.rotate([0, 0, 1], 45)
    box.translate(pcl.centroid)

    scene = Scene()
    scene.add(box)
    for point in pcl:
        color = Color.red() if box.contains(point) else Color.blue()
        scene.add(point, color=color)
    scene.redraw()


Creating a Mesh From an OBJ File
================================

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas.scene import Scene

    mesh = Mesh.from_obj(compas.get('tubemesh.obj'))

    scene = Scene()
    scene.add(mesh)
    scene.redraw()
