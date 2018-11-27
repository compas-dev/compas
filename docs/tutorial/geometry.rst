********************************************************************************
Geometry processing
********************************************************************************


Object representations
======================

The functions, methods and algorithms of the geometry package take various geometric
primitives and objects as input parameters. These primitives and objects may be passed
into those functions as instances of the corresponding classes defined in :mod:`compas.geometry`
or as an equivalent representation using (combinations of) built-in Python objects.
The following table defines those representations.


.. rst-class:: table table-responsive table-bordered

=========== ====================================================================
parameter   representation
=========== ====================================================================
vector      list of XYZ coordinates.
point       list of XYZ coordinates.
segment     2-tuple of points.
line        2-tuple of points.
ray         2-tuple of points.
polyline    list of points.
polygon     list of points.
plane       2-tuple of origin (point) and normal (vector).
frame       3-tuple of origin (point), U axis (vector) and V axis (vector).
circle      3-tuple of center (point), normal (vector) and radius (float).
=========== ====================================================================


.. code-block:: python

    from compas.geometry import distance_point_plane

    from compas.geometry import Point
    from compas.geometry import Plane

    point = Point(0, 0, 0)
    plane = Plane([2, 0, 0], [1, 0, 0])

    distance_point_plane(point, plane)

.. parsed-literal::

    2.0


.. code-block:: python

    from compas.geometry import distance_point_plane

    point = [0, 0, 0]
    plane = ([2, 0, 0], [1, 0, 0])

    distance_point_plane(point, plane)

.. parsed-literal::

    2.0


XY variations
=============

Many functions have an "_xy" version. These functions also accept 2D representations
of geometric objects.
However, they always return 3D objects.
For example, ``scale_vector_xy`` accepts both 2D and 3D vectors,
but always returns a 3D vector with the Z-component set to zero.


.. code-block:: python

    from compas.geometry import scale_vector

    vector = [1.0, 0.0, 2.0]
    scale_vector(vector, 3.0)

.. parsed-literal::

    [3.0, 0.0, 6.0]


.. code-block:: python

    from compas.geometry import scale_vector_xy

    v2 = [1.0, 0.0]
    v3 = [1.0, 0.0, 3.0]

    v2 = scale_vector_xy(v2, 3.0)
    v3 = scale_vector_xy(v3, 3.0)

    v2 == v3

.. parsed-literal::

    True

