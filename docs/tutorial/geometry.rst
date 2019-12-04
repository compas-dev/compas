Geometry Processing
===================

The functions of this package take various geometric primitives as input parameters.
These primitives may be passed into those functions as instances of the
corresponding classes or as an equivalent representation using (combinations of)
built-in Python objects. The following table defines those equivalent representations.

.. rst-class:: longtable table table-bordered

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

    >>> cross_vectors([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    [0.0, 0.0, 1.0]
    >>> cross_vectors(Vector(1, 0, 0), [0, 1, 0])
    [0.0, 0.0, 1.0]
    >>> cross_vectors(Vector(1, 0, 0), Vector(0, 1, 0))
    [0.0, 0.0, 1.0]
    >>> points = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]]
    >>> area_polygon(points) == area_polygon(Polygon(points))
    True

Many functions also have an ``_xy`` variant.
These variants ignore the Z-component of the input parameters.
Therefore, they also accept 2D representations of geometric objects.
However, they always return a 3D result in the XY plane (with ``z = 0``).
For example, ``scale_vector_xy`` accepts both 2D and 3D vectors,
but always returns a 3D vector with the Z-component set to zero.

.. code-block:: python

    >>> points = [[0.0, 0.0, 1.0], [1.0, 0.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 0.0]]
    >>> area_polygon_xy(points) == area_polygon(points)
    False
