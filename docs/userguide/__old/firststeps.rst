***********
First Steps
***********

Once COMPAS is installed, you can start using it in your Python scripts.
Here are some some super simple examples to get you started.

The visualisations shown on this page are generated with the COMPAS Viewer in VS Code.
See the :doc:`basics.visualisation` for more information on how to set it up and use it.
Alternatively, you can run the examples in Rhino or Blender.
See the :doc:`cad.rhino` and :doc:`cad.blender` for more information on how to get started with that.


Random Geometry
---------------


Containment and Membership
--------------------------


Oriented Bounding Box
---------------------

.. code-block:: python

    import math

    from compas.geometry import Pointcloud, Box, Rotation
    from compas.geometry import oriented_bounding_box_numpy

    Rz = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], math.radians(60))
    Ry = Rotation.from_axis_and_angle([0.0, 1.0, 0.0], math.radians(20))
    Rx = Rotation.from_axis_and_angle([1.0, 0.0, 0.0], math.radians(10))

    points = Pointcloud.from_bounds(x=10, y=5, z=3, n=100)

    points.transform(Rz * Ry * Rx)

    obb = oriented_bounding_box_numpy(points)
    box = Box.from_bounding_box(obb)


Shortest Path
-------------


Loops and Strips
----------------


Mesh Subdivision
----------------


Conway Operators
----------------



