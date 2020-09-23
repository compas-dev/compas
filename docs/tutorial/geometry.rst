********
Geometry
********

.. currentmodule:: compas.geometry

.. highlight:: python

This tutorial provides a quick tour of the functionality in :mod:`compas.geometry`.
For a complete overview, visit the API Reference:
https://compas-dev.github.io/main/api/compas.geometry.html

An interactive version of this tutorial in the form of a *jupyter notebook* is available here:
`COMPAS geometry notebook <https://colab.research.google.com/drive/1GaLTCDMYS0_HdZJjkb6eRfFZ3BvZSpR2?usp=sharing>`_


Points and Vectors
==================

In Python, the simplest way to represent a point or a vector is through a list of XYZ components.
To retrieve or modify one of the components, simply access the corresponding index in the list::

    >>> point = [1, 1, 1]
    >>> point[0]
    1
    >>> point[0] = 5
    >>> point[0]
    5
    >>> point
    [5, 1, 1]


To add two points, compute the length of a vector, ... you can apply simple math to the items
of these lists::

    >>> a = [1, 0, 0]
    >>> b = [0, 1, 0]
    >>> c = [a[i] + b[i] for i in range(3)]
    >>> c
    [1, 1, 0]


Most geometric operations can not be expressed so concisely as the addition of two points or vectors,
and writing this out quickly becomes quite tedious.

Therefore, COMPAS provides many functions for points and vectors that simplify the use of basic operations.

::

    >>> from compas.geometry import add_vectors, cross_vectors

::

    >>> a = [1, 0, 0]
    >>> b = [0, 1, 0]
    >>> add_vectors(a, b)
    [1, 1, 0]

    >>> cross_vectors(a, b)
    [0, 0, 1]


In addition to basic vector algebra functions, COMPAS provides :class:`Point` and :class:`Vector` classes
that can be used interchangeably with native Python types for geometrical calculations.
They provide access to XYZ coordinates through indexing as well as through ``x``, ``y``, and ``z`` attributes,
support basic operations such as addition, subtraction, and multiplication,
and bind many of the basic geometry functions as methods.

::

    >>> from compas.geometry import Point, Vector

::

    >>> point = Point(1, 0, 0)
    >>> point[0]
    1
    >>> point.x
    1

::

    >>> a = Point(1, 0, 0)
    >>> b = Point(0, 1, 0)
    >>> c = a + b
    >>> c
    Point(1.000, 1.000, 0.000)

::

    >>> u = Vector(1, 0, 0)
    >>> u * 3


Operators such as ``+`` or ``*`` involving COMPAS geometry objects always return a new COMPAS geometry object.
However, the result type is not always the same as the type of the inputs::

    >>> a = Point(0, 0, 0)
    >>> b = Point(1, 1, 0)
    >>> b - a
    Vector(1.000, 1.000, 0.000)


Basic functions, on the other hand, always return native Python objects, regardless of the input::

    >>> x = Vector(1, 0, 0)
    >>> y = Vector(0, 1, 0)
    >>> cross_vectors(x, y)
    [0.0, 0.0, 1.0]


Many of the basic functions are also available as object methods::

    >>> x.cross(y)
    Vector(0.000, 0.000, 1.000)

    >>> x.scale(3)
    None

    >>> x[0]
    3.0

    >>> x.scaled(3)
    Vector(9.000, 0.000, 0.000)

    >>> x[0]
    3.0

    >>> x.dot(y)
    0.0

    >>> x.normalize()

    >>> x.cross([0, 1, 0])
    Vector(0.000, 0.000, 1.000)

    >>> x.angle(y)
    1.5707963267948966


For an overview of all functionality, see *Points and Vectors* in the API Reference.


Other Primitives
================

In addition to points and vectors, COMPAS provides :class:`Line`, :class:`Plane`,
:class:`Polyline`, :class:`Polygon`, :class:`Circle`, :class:`Ellipse`, :class:`Frame`, and :class:`Quaternion`.

All COMPAS primitives can be used interchangeably with native Python objects as input for geometry functions and object methods.
The following representations of geometric objects are entirely equivalent.

.. rst-class:: table table-bordered

.. list-table::
    :widths: auto
    :header-rows: 1

    * - Object
      - Python
      - COMPAS
    * - point
      - ``point = [0, 0, 0]``
      - ``point = Point(0, 0, 0)``
    * - vector
      - ``vector = [0, 0, 1]``
      - ``vector = Vector(0, 0, 1)``
    * - line
      - ``line = [0, 0, 0], [1, 0, 0]``
      - ``line = Line(point, point)``
    * - plane
      - ``plane = [0, 0, 0], [0, 0, 1]``
      - ``plane = Plane(point, vector)``
    * - circle
      - ``circle = ([0, 0, 0], [0, 0, 1]), 1.0``
      - ``circle = Circle(plane, radius)``
    * - polyline
      - ``polyline = [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 0, 0]``
      - ``polyline = Polyline(points)``
    * - polygon
      - ``polygon = [0, 0, 0], [1, 0, 0], [1, 1, 0]``
      - ``polygon = Polygon(points)``
    * - frame
      - ``frame = [0, 0, 0], [1, 0, 0], [0, 1, 0]``
      - ``frame = Frame(point, xaxis, xypoint)``


In addition to the default instantiation mechanism, which is always based on the default representation of geometric entities,
many primitives provide "alternative constructors".

::

    >>> a = Vector(1, 0, 0)
    >>> b = Vector.from_start_end([1, 0, 0], [2, 0, 0])
    >>> a == b
    True

::

    >>> a = Plane([0, 0, 0], [0, 0, 1])
    >>> b = Plane.from_three_points([0, 0, 0], [1, 0, 0], [0, 1, 0])
    >>> a == b
    True

::

    >>> a = Frame([0, 0, 0], [3, 0, 0], [0, 2, 0])
    >>> b = Frame.from_points([0, 0, 0], [5, 0, 0], [1, 2, 0])
    >>> a == b
    True

.. add Polyline.from_lines
.. remove _xy from sides and radius constructor

Primitives also provide easy access to many of the geometric properties of the represented objects.

::

    >>> line = Line([0, 0, 0], [2, 0, 0])

    >>> line.start
    Point(0.000, 0.000, 0.000)

    >>> line.start.x
    0.0

    >>> line.end
    Point(2.000, 0.000, 0.000)

    >>> line.vector
    Vector(2.000, 0.000, 0.000)

    >>> line.vector[0]
    2.0

    >>> line.direction
    Vector(1.000, 0.000, 0.000)

    >>> line.midpoint
    Point(1.000, 0.000, 0.000)

    >>> line.length
    2.0


:class:`Frame` and :class:`Quaternion` are special primitives that play an important role
in transformations (see `Transformations`_).
A frame defines a local coordinate system and quaternions provide an alternative formulation for rotations.


.. Predicates
   ==========




Intersections
=============

To compute intersections between primitives and/or shapes, use the intersection functions.

::

    >>> line = [1, 1, 0], [1, 1, 1]
    >>> plane = [0, 0, 0], [0, 0, 1]
    >>> intersection_line_plane(line, plane)
    [1.0, 1.0, 0.0]

::

    >>> line = [1, 1, 0], [1, 1, 1]
    >>> plane = Plane.worldXY()
    >>> intersection_line_plane(line, plane)
    [1.0, 1.0, 0.0]

::

    >>> line = Line([1, 1, 0], [1, 1, 1])
    >>> plane = Plane.worldXY()
    >>> line.intersection(plane)
    Point(1.000, 1.000, 0.000)


Transformations
===============

.. is this correct?
.. split affine and projection

All transformations of geometric objects are based on :class:`Transformation`,
which defines a general projective or affine transformation in eucledian space,
represented by a 4x4 transformation matrix.
The default transformation is an identity::

    >>> from compas.geometry import Transformation
    >>> X = Transformation()
    >>> a = Point(1, 0, 0)
    >>> b = a.transformed(X)
    >>> a == b
    True


The base transformation object provides alternative constructors
to create transformations between different coordinate systems represented by frames::

    >>> X = Transformation.from_frame(frame)
    >>> X = Transformation.from_frame_to_frame(frame1, frame2)
    >>> X = Transformation.from_change_of_basis(frame1, frame2)


:class:`Translation`, :class:`Rotation`, :class:`Scale`, :class:`Shear`, and :class:`Projection`
define specific transformations::

    >>> import math
    >>> from compas.geometry import Rotation
    >>> R = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))

All primitives support transformations through the methods :func:`Primitive.transform` and  :func:`Primitive.transformed`.
The former modifies the object in place, whereas the latter returns a new object::

    >>> point = Point(1, 0, 0)
    >>> point.transformed(R)
    Point(0.000, 1.000, 0.000)
    >>> point.transform(R)
    None
    >>> point.y
    1.0


All transformation objects support matrix multiplication with the ``*`` operator.
Remember that the multiplication order of transformation matrices is important!::

    >>> T = Translation.from_vector([1, 1, 0])
    >>> R = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
    >>> point = Point(1, 0, 0)
    >>> point.transformed(T * R)
    Point(1.000, 2.000, 0.000)
    >>> point.transformed(R * T)
    Point(-1.000, 2.000, 0.000)


Note that points and vectors behave different in transformations.
Applying the same transformation above to a vector instead of a point,
we get a different result, because the translation component is ignored::

    >>> vector = Vector(1, 0, 0)
    >>> vector.transformed(R * T)
    Vector(0.000, 1.000, 0.000)
    >>> vector.transformed(T * R)
    Vector(0.000, 1.000, 0.000)

.. rename to angle_and_axis
.. make axis optional
.. add deg option (default is True)

Note that geometries are not implicitly linked::

    >>> a = Point(0, 0, 0)
    >>> b = Point(1, 0, 0)
    >>> ab = Line(a, b)
    >>> R = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
    >>> ab.transform(R)
    >>> ab.end
    Point(0.000, 1.000, 0.000)
    >>> ab.end == b
    False

.. add cutting data example to examples
.. add from_reference?
.. add from_objects?
.. how to make linked diagrams?
.. mention tha all objects are independent
.. bidirectional link with cad geometry?


Shapes
======

"Shapes" (or "Solids") extend the primitives with volumetric geometries.
:class:`Box`, :class:`Capsule`, :class:`Cone`, :class:`Cylinder`, :class:`Polyhedron`, :class:`Sphere`, and :class:`Torus`
are available.

As usual, there is a default "constructor" and several "alternative constructors".
The default constructor, corresponds to the canonical representation of the geometrical objects.

After construction, all shapes are axis-aligned and centered at the origin.
To move shapes to different locations in 3D space, change their orientations,
or modify their geometry, use transformations::

    >>> b1 = Box(Frame.worldXY(), 5, 1, 3)
    >>> b2 = Box.from_width_height_depth(5, 1, 3)
    >>> b1 == b2
    True


Boolean Operations
==================

3D boolean operations are not supported in COMPAS by default,
but are available if the plugin :mod:`compas_cgal` is installed::

    >>>


Algorithms
==========


Serialization
=============


Precision
=========


.. add somewhere 2D v. 3D

.. add something about geometric maps (separate tutorial)

.. geometry formats
