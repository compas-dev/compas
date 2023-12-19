******************************************************************************
Planes and Frames
******************************************************************************

[...intro...]

Planes
==============================================================================

A plane is defined by a point and a normal vector.

>>> from compas.geometry import Point, Vector
>>> from compas.geometry import Plane
>>> plane = Plane(Point(0, 0, 0), Vector(0, 0, 1))
>>> plane
Plane(point=Point(x=0.0, y=0.0, z=0.0), normal=Vector(x=0.0, y=0.0, z=1.0))

Pure Python inputs are automatically converted.

>>> plane = Plane([0, 0, 0], [0, 0, 1])
>>> plane
Plane(point=Point(x=0.0, y=0.0, z=0.0), normal=Vector(x=0.0, y=0.0, z=1.0))
>>> plane.point
Point(x=0.0, y=0.0, z=0.0)
>>> plane.normal
Vector(x=0.0, y=0.0, z=1.0)

The input vector is automatically normalized.

>>> plane = Plane([0, 0, 0], [0, 0, 10])
>>> plane.normal
Vector(x=0.0, y=0.0, z=1.0)

Both point and normal can be modified.

>>> plane.point = [1, 2, 3]
>>> plane.normal = [10, 0, 0]
>>> plane.point
Point(x=1.0, y=2.0, z=3.0)
>>> plane.normal
Vector(x=1.0, y=0.0, z=0.0)

The coefficients of the plane equation can be accessed as well.

>>> plane = Plane([0, 0, 10], [0, 0, 10])
>>> plane.abcd
(0.0, 0.0, 1.0, -10.0)

Special planes can be constructed using predefined contructor methods.

>>> xy = Plane.worldXY()
>>> xy.normal
Vector(x=0.0, y=0.0, z=1.0)
>>> yz = Plane.worldYZ()
>>> yz.normal
Vector(x=1.0, y=0.0, z=0.0)
>>> zx = Plane.worldZX()
>>> zx.normal
Vector(x=0.0, y=1.0, z=0.0)

Planes can also be contructed from other inputs than point and normal.

>>> plane = Plane.from_abcd(...)
>>> plane = Plane.from_frame(...)
>>> plane = Plane.from_point_and_two_vectors(...)
>>> plane = Plane.from_three_points(...)

For distance calculations and membership verifications involving planes, see :doc:`/userguide/basics.geometry.distance_and_membership`.
For intersections between planes and other objects, see :doc:`/userguide/basics.geometry.intersections`.


Frames
==============================================================================

Frames are defined by a point and two vectors,
and are used to represent local coordinate systems.

>>> from compas.geometry import Point, Vector
>>> from compas.geometry import Frame
>>> frame = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0))
>>> frame
Frame(point=Point(x=0.0, y=0.0, z=0.0), xaxis=Vector(x=1.0, y=0.0, z=0.0), yaxis=Vector(x=0.0, y=1.0, z=0.0))

As with planes, pure Python inputs are automatically converted.

>>> frame = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
>>> frame
Frame(point=Point(x=0.0, y=0.0, z=0.0), xaxis=Vector(x=1.0, y=0.0, z=0.0), yaxis=Vector(x=0.0, y=1.0, z=0.0))

The first input vector is the X-axis of the corrdinate system.
The second input vector should be a vector in the XY-plane of the coordinate system.
It is automatically converted to the Y-axis of the coordinate system.
From the two input vectors, the Z-axis is computed.

>>> frame = Frame([0, 0, 0], [1, 0, 0], [0, 0, 1])
>>> frame.xaxis
Vector(x=1.0, y=0.0, z=0.0)
>>> frame.yaxis
Vector(x=0.0, y=1.0, z=0.0)
>>> frame.zaxis
Vector(x=0.0, y=0.0, z=1.0)

The input vectors are automatically normalized.

>>> frame = Frame([0, 0, 0], [10, 0, 0], [0, 10, 0])
>>> frame.xaxis
Vector(x=1.0, y=0.0, z=0.0)
>>> frame.yaxis
Vector(x=0.0, y=1.0, z=0.0)

Specific frames can be constructed using predefined constructor methods.

>>> frame = Frame.worldXY()
>>> frame.xaxis
Vector(x=1.0, y=0.0, z=0.0)
>>> frame.yaxis
Vector(x=0.0, y=1.0, z=0.0)
>>> frame.zaxis
Vector(x=0.0, y=0.0, z=1.0)

>>> frame = Frame.worldYZ()
>>> frame.xaxis
Vector(x=0.0, y=1.0, z=0.0)
>>> frame.yaxis
Vector(x=0.0, y=0.0, z=1.0)
>>> frame.zaxis
Vector(x=1.0, y=0.0, z=0.0)

>>> frame = Frame.worldZX()
>>> frame.xaxis
Vector(x=0.0, y=0.0, z=1.0)
>>> frame.yaxis
Vector(x=1.0, y=0.0, z=0.0)
>>> frame.zaxis
Vector(x=0.0, y=1.0, z=0.0)

Frames can also be constructed from other inputs than point and two vectors.

>>> frame = Frame.from_axis_angle_vector(...)
>>> frame = Frame.from_euler_angles(...)
>>> frame = Frame.from_change_of_basis(...)
>>> frame = Frame.from_list(...)
>>> frame = Frame.from_matrix(...)
>>> frame = Frame.from_plane(...)
>>> frame = Frame.from_points(...)
>>> frame = Frame.from_quaternion(...)
>>> frame = Frame.from_rotation(...)
>>> frame = Frame.from_transformation(...)

Frames are closely related to transformations.
For more information on transformations and their relationship to frames, see :doc:`/userguide/basics.geometry.transformations`.


Plane/Frame Conversions
==============================================================================

A plane can be constructed from a frame.
The plane will have the same origin as the frame,
and its normal vector will be equal to the Z-axis of the frame.

>>> from compas.geometry import Frame
>>> from compas.geometry import Plane
>>> frame = Frame.worldXY()
>>> plane = Plane.from_frame(frame)
>>> plane.point == frame.point
True
>>> plane.normal == frame.zaxis
True

Note that during the conversion, some information is lost.

>>> from compas.geometry import Frame
>>> from compas.geometry import Plane
>>> frame1 = Frame([0, 0, 0], [0, 1, 0], [-1, 0, 0])
>>> plane = Plane.from_frame(frame1)
>>> frame2 = Frame.from_plane(plane)
>>> frame1.point == frame2.point
True
>>> frame1.zaxis == frame2.zaxis
True
>>> frame1.xaxis == frame2.xaxis
False
>>> frame1.yaxis == frame2.yaxis
False
