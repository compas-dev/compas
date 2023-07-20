************
Introduction
************

.. currentmodule:: compas.geometry

The geometry package of COMPAS (:mod:`compas.geometry`) provides implementations of
various basic geometry objects, frames, transformations, curves, surfaces, solids, boundary representation objects (BREPs),
and many algorithms that operate on these geometric entities.

All classes and functions in the examples of this introduction can be imported directly from the :mod:`compas.geometry` module.
We will omit the import statements in the examples for brevity.

Points and Vectors
==================

Points and vectors are the most fundamental geometric entities in the COMPAS geometry library.
They are explicitly defined through their XYZ coordinates.

>>> point = Point(0, 0, 0)
>>> vector = Vector(1, 0, 0)

The coordinates of a point or vector can be accessed by their respective properties ``x``, ``y``, and ``z``,
or through the corresponding indexes ``[0] => x``, ``[1] => y``, and ``[2] => z``.

>>> a = Point(1, 2, 3)
>>> a.x
1.0
>>> a[0]
1.0

Points and vectors support basic arithmetic operations such as addition, subtraction, multiplication, and division.

>>> a = Point(1, 0, 0)
>>> b = Point(2, 0, 0)
>>> a + b
Point(3.000, 0.000, 0.000)
>>> a * 2
Point(2.000, 0.000, 0.000)
>>> b / 2
Point(1.000, 0.000, 0.000)

The basic arithmetic operations return new objects of the same type as the first operand.
Note, however, that subtraction of two points returns a vector.
This is the vector pointing from the second point tothe first.

>>> b - a
Vector(1.000, 0.000, 0.000)

To modify an object in-place instead of returning a new object, use the corresponding in-place operators.

>>> a += b
>>> a
Point(3.000, 0.000, 0.000)

Points and vectors can be compared with one another using the standard comparison operators.

>>> a == b
False
>>> a != b
True

Vectors have a length, and support operations such as dot product, cross product, angle calculation, unitisation, scaling, etc.

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

For a complete overview of the available methods, please refer to the :class:`Point` and :class:`Vector` documentation.


Planes
======

Planes are defined by a base point and a normal vector.
The base point and normal vector can be accessed by their respective properties ``point`` and ``normal``,
or with the corresponding indexes: ``[0] => point``, ``[1] => normal``.
The indexes correspond to the order in which the properties are listed as input arguments when constructing the plane.

>>> plane = Plane(Point(0, 0, 0), Vector(0, 0, 1))
>>> plane.point
Point(0.000, 0.000, 0.000)
>>> plane.point == plane[0]
True
>>> plane.normal
Vector(0.000, 0.000, 1.000)
>>> plane.normal == plane[1]
True

Note that planes can also be constructed from simple lists or tuples containing the XYZ coordinates of the base point and the normal vector.
The input will be converted automatically to the appropriate geometry objects.

>>> plane = Plane([0, 0, 0], [0, 0, 1])
>>> plane.point
Point(0.000, 0.000, 0.000)
>>> plane.normal
Vector(0.000, 0.000, 1.000)

Planes can also be constructed from various other types of input using alternative constructor methods.

* :meth:`Plane.from_three_points`
* :meth:`Plane.from_point_and_two_vectors`
* :meth:`Plane.from_points`
* :meth:`Plane.from_frame`
* :meth:`Plane.from_abcd`

>>> plane = Plane.from_three_points([0, 0, 0], [1, 0, 0], [0, 1, 0])
>>> plane
Plane(Point(0.000, 0.000, 0.000), Vector(0.000, 0.000, 1.000))

The :class:`Plane` class provides various methods for identifying relationships to other objects, and computing distances, intersections, projections, etc.
For a complete overview of the available methods, please refer to the :class:`Plane` documentation.


Frames
======

Frames represent right-handed coordinate systems, and are defined by a base point and two input vectors.
The base point is the origin of the frame.
The cross product of the two input vectors defines the Z axis of the frame, or the normal vector of the XY plane.
The first input vector defines the X axis.
The Y axis is determined by the cross product of the Z and X axes.
Frames are mostly used to define (local) coordinate systems and are closely related to transformations.

>>> frame = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0))
>>> frame
Frame(Point(0.000, 0.000, 0.000), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))

Note that the second input vector only defines the orientation of the XY plane.
It doesn't have to be perpendicular to the first one.


>>> frame = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(1, 1, 0))
>>> frame
Frame(Point(0.000, 0.000, 0.000), Vector(1.000, 0.000, 0.000), Vector(0.000, 1.000, 0.000))

The base point and the three axes of the frame can be accessed by their respective properties ``point``, ``xaxis``, ``yaxis``, and ``zaxis``,
or through the corresponding indexes, with: ``[0] => point``, ``[1] => xaxis``, ``[2] => yaxis``, and ``[3] => zaxis``.

>>> frame.point
Point(0.000, 0.000, 0.000)
>>> frame[0]
Point(0.000, 0.000, 0.000)

>>> frame.xaxis.cross(frame.yaxis) == frame.zaxis == frame[3]
True

Frames can also be constructed from simple lists or tuples containing the XYZ coordinates of the base point and the two input vectors.

>>> frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
>>> frame.point
Point(0.000, 0.000, 0.000)
>>> frame.xaxis
Vector(1.000, 0.000, 0.000)

Frames can also be constructed from various other types of input using alternative constructor methods.

* :meth:`Frame.from_axis_angle_vector`
* :meth:`Frame.from_euler_angles`
* :meth:`Frame.from_list`
* :meth:`Frame.from_matrix`
* :meth:`Frame.from_plane`
* :meth:`Frame.from_points`
* :meth:`Frame.from_quaternion`
* :meth:`Frame.from_rotation`
* :meth:`Frame.from_transformation`

And to match specific planes of the world coordinate system.

* :meth:`Frame.worldXY`
* :meth:`Frame.worldYZ`
* :meth:`Frame.worldZX`

For a complete overview of the available methods, please refer to the :class:`Frame` documentation.
For more information about transformations, please refer to the :ref:`Transformations` section.
For more information about working with frames and transformations, please refer to :ref:`Working with Frames and Transformations`.


Transformations
===============

Transformation objects represent transformations in 3D space.
They can be used to transform points, vectors, frames, and other geometric objects.
Transformation objects are implemented using 4x4 transformation matrices, which support homogenous coordinates and allow to distinguish between points and vectors.
These matrices acan also be used to perform perspective projections, in addition to translations, rotations, and scale and shear transformations.

The default transformation is the identity transformation, which does not change the input.

>>> T = Transformation()

Transformations can be applied to all geometry objects through the :meth:`Geometry.transform` method.

>>> point = Point(1, 0, 0)
>>> point.transform(T)
Point(1.000, 0.000, 0.000)

To return a transformed copy of the object instead of transforming the object in-place, use the method :meth:`Geometry.transformed` instead.

>>> a = Point(1, 0, 0)
>>> b = point.transformed(T)
>>> a == b
True
>>> a is b
False

Elements of the transformation matrix can be accessed (and modified) by their row and column index.

>>> T[0, 0]
1.0
>>> T[1, 1]
1.0
>>> T[2, 2]
1.0
>>> T[3, 3]
1.0

General transformation matrices can be constructed from various types of input using alternative constructor methods.
The most interesting ones are those that relate to transformations between different coordinate systems, or "frames".

* :meth:`Transformation.from_change_of_basis`
* :meth:`Transformation.from_frame`
* :meth:`Transformation.from_frame_to_frame`

:meth:`Transformation.from_frame_to_frame` generates a transformation matrix that transforms points from one frame to another.
The coordinates of the points are the same in both frames, but the frames themselves are oriented differently in space, and therefore the points are as well.

>>> frame1 = Frame.worldXY()
>>> frame2 = Frame.worldZX()
>>> T = Transformation.from_frame_to_frame(frame1, frame2)
>>> point = Point(1, 0, 0)
>>> point.transform(T)
>>> point
Point(0.000, 0.000, 1.000)

:meth:`Transformation.from_change_of_basis` generates a transformation matrix that transforms points from one frame to another,
such that their coordinates in the first frame stay the same, but expressed with respect to the second coordinate system.

>>> frame1 = Frame.worldXY()
>>> frame2 = Frame.worldZX()
>>> T = Transformation.from_change_of_basis(frame1, frame2)
>>> point = Point(1, 0, 0)
>>> point.transform(T)
>>> point
Point(0.000, 1.000, 0.000)

Several subclasses of the :class:`Transformation` class are available to construct specific types of transformations.
Each of these have their own constructor methods.

* :class:`Translation`
* :class:`Rotation`
* :class:`Scale`
* :class:`Reflection`
* :class:`Projection`
* :class:`Shear`

>>> R = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
>>> point = Point(1, 0, 0)
>>> point.transform(R)
>>> point
Point(0.000, 1.000, 0.000)

Transformations can be combined through multiplication.

>>> T = Translation.from_vector([1, 0, 0])
>>> R = Rotation.from_axis_and_angle([0, 0, 1], math.radians(90))
>>> X = T * R
>>> point = Point(1, 0, 0)
>>> point.transform(X)
>>> point
Point(1.000, 1.000, 0.000)

For a complete overview of the available methods, please refer to the documentation of
:class:`Transformation`, :class:`Translation`, :class:`Rotation`, :class:`Scale`, :class:`Reflection`, :class:`Projection`, and :class:`Shear`.


Parametric Curves
=================

The geometry package of COMPAS provides a number of parametric curves.
All parametric curves inherit from a base curve object and implement at least the following methods.

* :meth:`Curve.point_at`
* :meth:`Curve.tangent_at`
* :meth:`Curve.normal_at`

All parametric curves can be converted to a sequence of points spread evenly over their parameter space, using :meth:`Curve.to_points`,
or directly to a :class:`Polyline` using :meth:`Curve.to_polyline`.
For a complete overview of the curve interface, please refer to the :class:`Curve` documentation.


Lines and Polylines
-------------------

Lines are defined by a start point and a direction vector.
The direction vector points from the start point of the curve to the end point.
The direction vector is unitized.
The parameter domain is defined such that the start point of the line segment corresponds to parameter ``0.0`` and the end point to parameter ``1.0``.

>>> line = Line([0, 0, 0], [2, 0, 0])
>>> line.point_at(0.0) == line.start
True
>>> line.point_at(1.0) == line.end
True
>>> line.start + line.direction * line.length == line.end
True
>>> line.direction * line.length == line.vector
True

Other points on the line can be constructed using the base point and direction vector.

>>> line.start + line.direction * 3
Point(3.000, 0.000, 0.000)

Or by evaluating the line at a specific parameter value.
Note that the parametrisation is related to the length of the line segment, i.e. to the distance between the start and end point.

>>> line.point_at(3)
Point(6.000, 0.000, 0.000)

Polylines are defined by a sequence of points, with a line segment defined between each two consecutive points.

>>> polyline = Polyline([[0, 0, 0], [1, 0, 0], [2, 0, 0]])
>>> polyline.points[0] == [0, 0, 0]
True
>>> polyline.points[1] == [1, 0, 0]
True
>>> polyline.lines[0].start == polyline.points[0]
True
>>> polyline.lines[0].end == polyline.points[1]
True

The parameter domain of a polyline is defined such that the start point of the first line segment corresponds to parameter ``0.0`` and the end point of the last line segment to parameter ``1.0``.

>>> polyline.point_at(0.0) == polyline.lines[0].start == polyline.points[0]
True
>>> polyline.point_at(1.0) == polyline.lines[-1].end == polyline.points[-1]
True

For a complete overview of the available methods, please refer to the documentation for :class:`Line` and :class:`Polyline`.


Conic Sections
--------------

The conic sections include the circle (:class:`Circle`), ellipse (:class:`Ellipse`), hyperbola (:class:`Hyperbola`), and parabola (:class:`Parabola`).
Each of these curves is defined parametrically with respect to a local coordinate system, represented by a frame (:class:`Frame`).
The default frame is the world XY plane (:meth:`Frame.worldXY`).

>>> circle = Circle(radius=1.0)
>>> circle.radius
1.0
>>> circle.frame.point
Point(0.000, 0.000, 0.000)
>>> circle.frame.xaxis
Vector(1.000, 0.000, 0.000)
>>> circle.frame.yaxis
Vector(0.000, 1.000, 0.000)

To create a conic section with a different orientation, simply specify the desired frame as an input argument.

>>> circle = Circle(radius=1.0, frame=Frame.worldZX())

The geometry methods listed above, can be used to evaluate the curve at a specific parameter value.
By default, the returned points and vectors are defined with respect to the world coordinate system.

>>> circle = Circle(radius=1.0, frame=Frame.worldZX())
>>> circle.point_at(0.0)
Point(1.000, 0.000, 0.000)
>>> circle.point_at(0.25)
Point(0.000, 0.000, 1.000)

In order to obtain local coordinates, set the optional argument ``local`` to ``True``.

>>> circle.point_at(0.25, local=True)
Point(0.000, 1.000, 0.000)

To transform local coordinates to world coordinates, use the :attr:`Circle.transformation` property.

>>> point = circle_at(0.25, local=True)
>>> point.transform(circle.transformation)
Point(0.000, 0.000, 1.000)

For a complete overview of the available methods, please refer to the documentation for :class:`Circle`, :class:`Ellipse`, :class:`Hyperbola`, and :class:`Parabola`.


Bézier Curves
-------------

Bézier curves are defined by a set of control points.
The degree of the curve is the number of control points minus one.

>>> points = [[0, 0, 0], [1, 1, 0], [2, 0, 0]]
>>> curve = Bezier(points)
>>> curve.degree
2

Bézier curves are always defined with respect to the world coordinate system.

>>> curve.frame == Frame.worldXY()
True

The geometry methods listed above, can be used to evaluate the curve at a specific parameter value.
The parameter domain of a Bézier curve is always [0.0, 1.0].

>>> curve.point_at(0.0) == curve.points[0]
True
>>> curve.point_at(1.0) == curve.points[-1]
True

The tangent vector points in the direction of the curve at the evaluated point.
The normal vector points in the direction of the center of the oscillating circle at the evaluated point.

>>> curve.tangent_at(0.5)
Vector(1.000, 0.000, 0.000)
>>> curve.normal_at(0.5)
Vector(0.000, -1.000, 0.000)

For a complete overview of the available methods, please refer to the documentation for :class:`Bezier`.


NURBS Curves
------------

NURBS curves are defined by control points, weights, a knot vector, and a curve degree.
Currently, COMPAS doesn't provide an implementation of NURBS curves directly.
Instead, NURBS curves are pluggables and receive their implementation from plugins.
Two plugins exist.
The first one is based on the NURBS implementation of RhinoCommon, and is available when COMPAS is used in Rhino or Grasshopper.
The second one is based on the NURBS implmentation of OpenCasCade, and is available when :mod:`compas_occ` is installed in the same environment as COMPAS.
In both cases, the implementations can be accessed through the :class:`NurbsCurve` class of :mod:`compas.geometry`.

As with other geometries, many different constructors exist to produce NURBS curves from different types of geometric input.

* :meth:`NurbsCurve.from_points`
* :meth:`NurbsCurve.from_parameters`
* :meth:`NurbsCurve.from_interpolation`
* :meth:`NurbsCurve.from_arc`
* :meth:`NurbsCurve.from_ellipse`
* :meth:`NurbsCurve.from_circle`
* :meth:`NurbsCurve.from_line`

>>> curve = NurbsCurve.from_points([[0, 0, 0], [1, 1, 0], [2, 0, 0]])
>>> curve.degree
2
>>> curve.domain
(0.0, 1.0)
>>> curve.weights
[1.0, 1.0, 1.0]
>>> curve.knots
[0.0, 1.0]
>>> curve.multiplicities
[3, 3]
>>> curve.knotsequence
[0.0, 0.0, 0.0, 1.0, 1.0, 1.0]

Alternatively, a NURBS curve can be loaded from a STP file.

>>> curve = NurbsCurve.from_stp('curve.stp')

The curve can be evaluated over its parameter domain using the geometry methods listed above.

>>> curve.point_at(0.0) == curve.points[0]
True
>>> curve.point_at(1.0) == curve.points[-1]
True

The tangent vector points in the direction of the curve at the evaluated point.
The normal vector points in the direction of the center of the oscillating circle at the evaluated point.

>>> curve.tangent_at(0.5)
Vector(1.000, 0.000, 0.000)
>>> curve.normal_at(0.5)
Vector(0.000, -1.000, 0.000)

For a complete overview of the available methods, please refer to the documentation for :class:`NurbsCurve`.


Parametric Surfaces
===================

The geometry package provides a number of parametric surfaces, which inherit from the base surface class (:class:`Surface`).

* :class:`PlanarSurface`
* :class:`CylindricalSurface`
* :class:`SphericalSurface`
* :class:`ConicalSurface`
* :class:`ToroidalSurface`
* :class:`NurbsSurface`

All parametric surface have methods to evaluate the surface geometry a specific parameter values,

* :meth:`Surface.point_at`
* :meth:`Surface.normal_at`
* :meth:`Surface.frame_at`

and can be converted to various discretised representations.

* :meth:`Surface.to_vertices_and_faces`
* :meth:`Surface.to_triangles`
* :meth:`Surface.to_quads`
* :meth:`Surface.to_polyhedron`
* :meth:`Surface.to_mesh`

For a complete overview of the surface API, see the documentation for :class:`Surface`.

Elementary Surfaces
-------------------

* :class:`PlanarSurface`
* :class:`CylindricalSurface`
* :class:`SphericalSurface`
* :class:`ConicalSurface`
* :class:`ToroidalSurface`

More info coming soon...

NURBS Surfaces
--------------

NURBS surfaces are defined by control points, weights, knots, knot multiplicities, and degrees in the U and V parameter directions.
Note that COMPAS doesn't provide an implementation of NURBS surfaces directly.
Instead, NURBS surfaces are pluggables and receive their implementation from plugins.
Two plugins exist.
The first one is based on the NURBS implementation of RhinoCommon, and is only available when COMPAS is used in Rhino or Grasshopper.
The second one is based on the NURBS implmentation of OpenCasCade, and is only available when :mod:`compas_occ` is installed in the same environment as COMPAS.

The following constructor methods are available to create NURBS surfaces from different types of geometric input.

* :meth:`NurbsSurface.from_points`
* :meth:`NurbsSurface.from_parameters`
* :meth:`NurbsSurface.from_meshgrid`
* :meth:`NurbsSurface.from_fill`

NURBS surfaces can also be loaded from a STEP file using :meth:`NurbsSurface.from_step`.

>>> surface = NurbsSurface.from_points([[[0, 0, 0], [0.5, 0, 0], [1, 0, 0]], [[0, 0.5, 0], [0.5, 0.5, 1], [1, 0.5, 0]], [[0, 1, 0], [0.5, 1, 0], [1, 1, 0]]])
>>> surface.weights
[[1.0, 1.0, 1.0], [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]]
>>> surface.u_knots
[0.0, 1.0]
>>> surface.v_knots
[0.0, 1.0]
>>> surface.u_mults
[3, 3]
>>> surface.v_mults
[3, 3]

NURBS surfaces can be evaluated at specific parameter values using the geometry methods listed above.

>>> surface.point_at(0.0, 0.0) == surface.points[0, 0]
True
>>> surface.point_at(1.0, 1.0) == surface.points[2, 2]
True
>>> surface.point_at(0.5, 0.5)
Point(0.500, 0.500, 0.125)

For a complete overview of the available methods, please refer to the documentation for :class:`NurbsSurface`.


Surfaces of Revolution
----------------------

More info coming soon...


Surfaces of Extrusion
---------------------

More info coming soon...


Shapes
======

More info coming soon...


Polygons and Polyhedrons
========================

Polygons are defined by a sequence of points, with a line segment defined between each two consecutive points.
The geometry of a polygon can be skewed, i.e. not planar.

>>> polygon = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
>>> polygon.points[0] == polygon.lines[0].start
True
>>> polygon.points[1] == polygon.lines[0].end
True

Polygons support basic boolean operations such as union, intersection, difference and symmetric difference.

>>> a = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
>>> b = Polygon([[0.5, 0.5, 0], [1.5, 0.5, 0], [1.5, 1.5, 0], [0.5, 1.5, 0]])
>>> c = a.boolean_union(b)
>>> c.area
1.75
>>> c = a.boolean_intersection(b)
>>> c.area
0.25
>>> c = a.boolean_difference(b)
>>> c.area
0.75

For a complete overview of the available methods, please refer to the documentation for :class:`Polygon`.

Polyhedrons are defined by vertices and faces.
The geometry of a polyhedron can be skewed, i.e. the faces of a polyhedron are not necessarily planar.
A polyhedron can be constructed explicitly, by providing a list of vertices and faces, or through alternative constructor methods.

* :meth:`Polyhedron.from_platonicsolid`
* :meth:`Polyhedron.from_halfspaces`
* :meth:`Polyhedron.from_planes`
* :meth:`Polyhedron.from_convex_hull`

.. more coming soon

Pointclouds
===========




Triangle Meshes
===============


Quad Meshes
===========


Intersections
=============


Boolean Operations
==================

