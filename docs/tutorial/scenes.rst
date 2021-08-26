****************
Scenes
****************

.. rst-class:: lead

    The COMPAS scene management framework provides a unified system
    for visualization and user interaction across CAD systems and other Graphical User Interfaces.


Basic Usage
===========

Using scenes is really simple:
just create a scene and add COMPAS geometry, data structure, oor robots.

.. code-block:: python

    import compas
    from compas.geometry import Point, Sphere, Box, Frame
    from compas.datastructures import Mesh

    import compas_rhino
    from compas_rhino.scene import Scene

    compas_rhino.clear()

    scene = Scene()

    scene.add(Sphere(Point(1.5, 1.5, 1.5), 1.0))
    scene.add(Box(Frame.worldXY(), 3, 3, 3))
    scene.add(Mesh.from_obj(compas.get('tubemesh.obj')))

    scene.update()


.. figure:: /_images/tutorial/scenes_basic-usage.png
    :figclass: figure
    :class: figure-img img-fluid


Scene Configuration
===================


Scene Save/Load
===============


Object Data
===========

When a data object is added to the scene, a scene object is returned.
The scene object keeps a reference to the data object in the ``item`` attribute.
The name "item" is used instead of "data" to avoid confusion with the ``data`` attribute of the data object.

.. code-block:: python

    box = Box(Frame.worldXY(), 1, 1, 1)
    obj = scene.add(box)

    obj.item is box  # -> True


Changes in the underlying data will be visible whenever the scene is updated.

.. code-block:: python

    obj.item.frame.point = Point(3, 0, 0)
    obj.draw()  # -> the scene update function should be modified such that this is no longer necessary

    scene.update()


Transformations
===============

.. code-block:: python

    from compas.geometry import Translation

    # ...

    box = Box(Frame.worldXY(), 1, 1, 1)
    obj = scene.add(box)

    obj.transform(Translation.from_vector([3, 0, 0]))

    scene.update()


Note that the transformation only affects the scene object.
The data object is still in the original location.

.. code-block:: python

    obj.item.frame.point  # -> Point(0.000, 0.000, 0.000)
    box.frame.point  # -> Point(0.000, 0.000, 0.000)


To propagate the scene changes back onto the data,
scene object and data have to be synchronized.

.. code-block:: python

    obj.synchronize()

    obj.item.frame.point  # -> Point(3.000, 0.000, 0.000)
    box.frame.point  # -> Point(3.000, 0.000, 0.000)


Shared Object Data
==================

Since a scene object can be transformed independently from the underlying data,
multiple scene objects can share the same data object.

.. code-block:: python

    pass


Dynamic Visualization
=====================


Recordings
==========
