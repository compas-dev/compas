********************
Geometric Primitives
********************

Points and Vectors
==================

A :class:`compas.geometry.Point` object represents a location in 3D space.

>>> from compas.geometry import Point
>>> a = Point(1, 2, 3)
>>> a
Point(1.0, 2.0, z=3.0)

The coordinates of a point can be accessed by their names, or by their index.

>>> a.x
1.0
>>> a.y
2.0
>>> a.z
3.0

>>> a[0]
1.0
>>> a[1]
2.0
>>> a[2]
3.0

When construction a point, the Z coordinate is optional and defaults to zero.

>>> b = Point(1, 2)
>>> b
Point(1.0, 2.0, z=0.0)
>>> b.z
0.0

A :class:`compas.geometry.Vector` object represents a direction and magnitude in 3D spaces.

>>> from compas.geometry import Vector
>>> u = Vector(1, 2, 3)
>>> u
Vector(1.0, 2.0, z=3.0)

As with points, the components of a vector can be accessed by their names, or by their index.

>>> u.x
1.0
>>> u.y
2.0
>>> u.z
3.0

>>> u[0]
1.0
>>> u[1]
2.0
>>> u[2]
3.0

Also here, the Z component is optional and defaults to zero.

>>> v = Vector(1, 2)
>>> v
Vector(1.0, 2.0, z=0.0)
>>> v.z
0.0


Operators
---------

Points and vectors can be added, subtracted, and multiplied with or divided by a scalar.

>>> a = Point(1, 0, 0)
>>> b = Point(0, 1, 0)
>>> a + b
Point(1.0, 1.0, z=0.0)
>>> a - b
Vector(1.0, -1.0, z=0.0)
>>> a * 2
Point(2.0, 0.0, z=0.0)
>>> a / 2
Point(0.5, 0.0, z=0.0)

>>> u = Vector(1, 0, 0)
>>> v = Vector(0, 1, 0)
>>> u + v
Vector(1.0, 1.0, z=0.0)
>>> u - v
Vector(1.0, -1.0, z=0.0)
>>> u * 2
Vector(2.0, 0.0, z=0.0)
>>> u / 2
Vector(0.5, 0.0, z=0.0)

Note that the second operand of addition and subtraction can also be a Python list or tuple.

>>> a + [0, 1, 0]
Point(1.0, 1.0, z=0.0)
>>> u + [0, 1, 0]
Vector(1.0, 1.0, z=0.0)

Also the in-place variants of the operators are supported.

>>> a += b
>>> a
Point(1.0, 1.0, z=0.0)

>>> u += v
>>> u
Vector(1.0, 1.0, z=0.0)


Comparison
----------

Points and vectors can be compared.

>>> a == b
False
>>> a != b
True

>>> u == v
False
>>> u != v
True

The comparison is based on the coordinates and components of the points and vectors.
The tolerance for the comparison defaults to the global COMPAS tolerance.

>>> a = Point(1.0, 0, 0)
>>> b = Point(1.0 + 1e-3, 0, 0)
>>> a == b
False

>>> a = Point(1.0, 0, 0)
>>> b = Point(1.0 + 1e-9, 0, 0)
>>> a == b
True

To use a different tolerance for a specific comparison, you have to use the corresponding comparison method instead, and provide the tolerance as an argument.

>>> a = Point(1.0, 0, 0)
>>> b = Point(1.0 + 1e-3, 0, 0)
>>> a.is_equal(b, tol=1e-3)
True

For more information about working with tolerances in COMPAS, see :doc:`advanced.tolerance`.


Planes
======

Frames
======
