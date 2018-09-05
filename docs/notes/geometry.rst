********************************************************************************
Geometry
********************************************************************************

This package provides functionality for working with geometry independent of CAD software.
The package defines geometric primitives, basic geometry functions, and an implementation
of a wide range of geometric algorithms.

The functions, methods and algorithms of the geometry package take various geometric
primitives and objects as input parameters. These primitives and objects may be passed
into those functions as instances of the corresponding classes defined in :mod:`compas.geometry.objects`
or as an equivalent representation using (combinations of) built-in Python objects.
The following table defines those representations.

.. rst-class:: table table-responsive table-bordered

=========== ====================================================================
parameter   representation
=========== ====================================================================
vector      :obj:`list` of XYZ coordinates.
point       :obj:`list` of XYZ coordinates.
segment     2-:obj:`tuple` of points.
line        2-:obj:`tuple` of points.
ray         2-:obj:`tuple` of points.
polyline    :obj:`list` of points.
polygon     :obj:`list` of points.
plane       2-:obj:`tuple` of origin (point) and normal (vector).
frame       3-:obj:`tuple` of origin (point), U axis (vector) and V axis (vector).
circle      3-:obj:`tuple` of center (point), normal (vector) and radius (float).
=========== ====================================================================

.. note::

    Many functions have an "_xy" version. These functions also accept 2D representations
    of geometric objects. However, all functions always return 3D representations
    of geometric objects. For example, `scale_vector_xy` accepts both 2D and 3D
    vectors, but always returns a 3D vector with the Z-component set to zero::

.. code-block:: python

    >>> v3 = [1.0, 0.0, 2.0]
    >>> scale_vector_xy(v3, 3.0)
    [3.0, 0.0, 0.0]

    >>> v2 = [1.0, 0.0]
    >>> scale_vector_xy(v2, 3.0)
    [3.0, 0.0, 0.0]

