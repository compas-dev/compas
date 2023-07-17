********
Geometry
********

.. currentmodule:: compas.geometry

The geometry package of COMPAS (:mod:`compas.geometry`) provides implementations of
various basic geometry objetcs, transformations, curves, surfaces, boundary representation objects (BREPs),
and many algorithms that operate on these geometric entities.

Points and Vectors
==================

Points and vectors are the most fundamental geometric entities in the COMPAS geometry library.
They are explicitly defined through their XYZ coordinates.

>>> from compas.geometry import Point, Vector
>>> point = Point(0, 0, 0)
>>> point
Point(0.000, 0.000, 0.000)
>>> vector = Vector(1, 0, 0)
>>> vector
Vector(1.000, 0.000, 0.000)

.. note::

    The string representation of points and vectors uses the COMPAS precision setting (``compas.PRECISION``) to determine the number of decimals used.

The coordinates of a point or vector can be accessed by their respective properties ``x``, ``y``, and ``z``,
or through the corresponding indexes ``[0] => x``, ``[1] => y``, and ``[2] => z``.

>>> from compas.geometry import Point
>>> a = Point(1, 2, 3)
>>> a.x
1.0
>>> a[0]
1.0

Points and vectors support basic arithmetic operations such as addition, subtraction, multiplication, and division.

>>> from compas.geometry import Point
>>> a = Point(1, 0, 0)
>>> b = Point(2, 0, 0)
>>> a + b
Point(3.000, 0.000, 0.000)
>>> b - a
Vector(1.000, 0.000, 0.000)
>>> a * 2
Point(2.000, 0.000, 0.000)
>>> b / 2
Point(1.000, 0.000, 0.000)

.. note::

    Note that by subtracting one point from another, we obtain a vector.

The operations can be used to generate new objects, or to modify existing objects.

>>> from compas.geometry import Point
>>> a = Point(1, 0, 0)
>>> b = Point(2, 0, 0)
>>> a += b
>>> a
Point(3.000, 0.000, 0.000)

Points and vectors can be compared with one another using the standard comparison operators.

>>> from compas.geometry import Point
>>> a = Point(1, 0, 0)
>>> b = Point(2, 0, 0)
>>> a == b
False
>>> a != b
True

In addition to their XYZ coordinates, vectors also have a length.

>>> from compas.geometry import Vector
>>> a = Vector(1, 0, 0)
>>> a.x
1.0
>>> a.length
1.0

Vectors support additional operations such as dot product, cross product, angle calculation, unitisation, scaling, etc.

>>> from compas.geometry import Vector
>>> u = Vector(3, 0, 0)
>>> v = Vector(0, 1, 0)
>>> u.dot(v)
0.0
>>> u.cross(v)
Vector(0.000, 0.000, 3.000)
>>> u.length
3.0
>>> u.angle(v)
1.5707963267948966
>>> u.unitize()
None
>>> u.length
1.0


Planes
======

Planes are defined by a base point and a normal vector.

>>> from compas.geometry import Point, Vector, Plane
>>> plane = Plane(Point(0, 0, 0), Vector(0, 0, 1))
>>> plane
Plane(Point(0.000, 0.000, 0.000), Vector(0.000, 0.000, 1.000))

Note that planes can also be constructed from simple lists or tuples containing the XYZ coordinates of the base point and the normal vector.
The input will be converted to the appropriate geometry objects, automatically.

>>> from compas.geometry import Point, Vector, Plane
>>> plane = Plane([0, 0, 0], [0, 0, 1])
>>> plane
Plane(Point(0.000, 0.000, 0.000), Vector(0.000, 0.000, 1.000))

The base point and normal vector can be accessed by their respective properties ``point`` and ``normal``,
or with the corresponding indexes: ``[0] => point``, ``[1] => normal``.

>>> from compas.geometry import Plane
>>> plane = Plane([0, 0, 0], [0, 0, 1])
>>> plane.point
Point(0.000, 0.000, 0.000)
>>> plane[0]
Point(0.000, 0.000, 0.000)
>>> plane.normal
Vector(0.000, 0.000, 1.000)
>>> plane[1]
Vector(0.000, 0.000, 1.000)

Alternatively, planes can be constructed from various other types of input.

* :meth:`Plane.from_three_points`
* :meth:`Plane.from_point_and_two_vectors`
* :meth:`Plane.from_points`
* :meth:`Plane.from_frame`
* :meth:`Plane.from_abcd`

>>> from compas.geometry import Plane
>>> plane = Plane.from_three_points([0, 0, 0], [1, 0, 0], [0, 1, 0])
>>> plane
Plane(Point(0.000, 0.000, 0.000), Vector(0.000, 0.000, 1.000))

In addition, the :class:`Plane` class provides various methods for identifying relationships to other objects, and computing distances, intersections, projections, etc.
For a complete overview of the available methods, please refer to the :class:`Plane` documentation.


Frames
======

