******************************************************************************
Points and Vectors
******************************************************************************

Points and vectors are represented by three floats, planes by a point and a vector, and frames by a point and two vectors.

Points
==============================================================================

A :class:`~compas.geometry.Point` represents a location in 3D space.

>>> from compas.geometry import Point
>>> a = Point(1, 2, 3)
>>> a
Point(x=1.0, y=2.0, z=3.0)

The individual coordinates of a point can be accessed by their names,
or by the corresponding index of each name (``0 -> x, 1 -> y, 2 -> z``).

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
Point(x=1.0, y=2.0, z=0.0)
>>> b.z
0.0

The coordinates of a point can be modified by assigning new values to the corresponding attributes.

>>> a = Point(0, 0, 0)
>>> b = Point(0, 0, 0)
>>> a.x = 1
>>> a
Point(x=1.0, y=0.0, z=0.0)
>>> b[1] = 1
>>> b
Point(x=0.0, y=1.0, z=0.0)

Point objects have various methods for distance calculations, and for membership tests.
See :doc:`/userguide/basics.geometry.distance_and_membership` for more information.


Vectors
==============================================================================

A :class:`~compas.geometry.Vector` represents a direction in 3D space
and a distance or magnitude along that direction (the length of the vector).
Vectors are always based at the origin of the coordinate system.
A vector is the direction, and distance along that direction,
from the origin of the coordinate system to a point in space.

>>> from compas.geometry import Vector
>>> u = Vector(1.0, 0.0, 0.0)
>>> u
Vector(x=1.0, y=0.0, z=0.0)

Special vectors can be constructed using predefined constructor methods.

>>> Vector.Xaxis()
Vector(x=1.0, y=0.0, z=0.0)
>>> Vector.Yaxis()
Vector(x=0.0, y=1.0, z=0.0)
>>> Vector.Zaxis()
Vector(x=0.0, y=0.0, z=1.0)

Working with vectors is very similar to working with points.
Vector components can be accessed using the component attribute names, or using the corresponding indices.

>>> u.x == u[0]
True
>>> u.y = 1.0
>>> u[2] = 1.0
>>> u
Vector(x=1.0, y=1.0, z=1.0)

All components are automatically converted to floats.
The Z component is optional and defaults to zero.

>>> Vector(1, 0)
Vector(x=1.0, y=0.0, z=0.0)

In addition to information about components or coordinates, vectors have a direction and magnitude.

>>> u.direction
Vector(x=0.5773502691896258, y=0.5773502691896258, z=0.5773502691896258)
>>> u.magnitude
1.7320508075688772

An alias for ``magnitude`` is ``length``.

>>> u.length
1.7320508075688772

Vector objects support dot and cross product calculations.

>>> u = Vector(1, 0, 0)
>>> v = Vector(0, 1, 0)
>>> u.dot(v)
0.0
>>> u.cross(v)
Vector(x=0.0, y=0.0, z=1.0)

Angles between two vectors can also be calculated.
Note that the angles are always returned in radians.

>>> u = Vector(1, 0, 0)
>>> v = Vector(0, 1, 0)
>>> u.angle(v)
1.5707963267948966
>>> u.angles(v)
(1.5707963267948966, 4.71238898038469)
>>> u.angle_signed(v, normal=[0, 0, -1])
-1.5707963267948966


Basic Arithmetic
==============================================================================

:class:`~compas.geometry.Point` and :class:`~compas.geometry.Vector` objects support basic arithmetic
through Python's built-in operators.

>>> a = Point(1, 0, 0)
>>> b = Point(0, 1, 0)
>>> a + b
Point(x=1.0, y=1.0, z=0.0)
>>> a - b
Vector(x=1.0, y=-1.0, z=0.0)  # not sure that this is helpful
>>> a * 2
Point(x=2.0, y=0.0, z=0.0)
>>> a / 2
Point(x=0.5, x=0.0, z=0.0)

>>> u = Vector(1, 0, 0)
>>> v = Vector(0, 1, 0)
>>> u + v
Vector(x=1.0, y=1.0, z=0.0)
>>> u - v
Vector(x=1.0, y=-1.0, z=0.0)
>>> u * 2
Vector(x=2.0, y=0.0, z=0.0)
>>> u / 2
Vector(x=0.5, y=0.0, z=0.0)

The second operand of addition and subtraction can also be a Python list or tuple.

>>> a + [0, 1, 0]
Point(x=1.0, y=1.0, z=0.0)

>>> u + [0, 1, 0]
Vector(x=1.0, y=1.0, z=0.0)

A binary operator involving points and vectors returns a new object.
Therefore the operators can be chained.

>>> a = Point(1, 0, 0)
>>> b = Point(0, 1, 0)
>>> c = Point(0, 0, 1)
>>> a + b * 2 + c * 3
Point(x=1.0, y=2.0, z=3.0)

The in-place variants of binary operators modify the objects in place.
Chaining is therefore not possible.

>>> u = Vector(1, 0, 0)
>>> v = Vector(0, 1, 0)
>>> u += v
None
>>> u
Vector(x=1.0, y=1.0, z=0.0)
