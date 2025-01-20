from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import Geometry
from compas.geometry import Transformation
from compas.geometry import argmax
from compas.geometry import axis_angle_vector_from_matrix
from compas.geometry import basis_vectors_from_matrix
from compas.geometry import cross_vectors
from compas.geometry import decompose_matrix
from compas.geometry import euler_angles_from_matrix
from compas.geometry import matrix_from_axis_angle_vector
from compas.geometry import matrix_from_basis_vectors
from compas.geometry import matrix_from_euler_angles
from compas.geometry import matrix_from_quaternion
from compas.geometry import quaternion_from_matrix
from compas.geometry import subtract_vectors
from compas.itertools import linspace

from .point import Point
from .quaternion import Quaternion
from .vector import Vector


class Frame(Geometry):
    """A frame is defined by a base point and two orthonormal base vectors.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        The origin of the frame.
    xaxis : [float, float, float] | :class:`compas.geometry.Vector`, optional
        The x-axis of the frame. Defaults to the unit X vector.
    yaxis : [float, float, float] | :class:`compas.geometry.Vector`, optional
        The y-axis of the frame. Defaults to the unit Y vector.
    name : str, optional
        The name of the frame.

    Attributes
    ----------
    axes : list of :class:`compas.geometry.Vector`, read-only
        The XYZ axes of the frame.
    axis_angle_vector : :class:`compas.geometry.Vector`, read-only
        The axis-angle vector representing the rotation of the frame.
    normal : :class:`compas.geometry.Vector`, read-only
        The normal of the base plane of the frame.
    point : :class:`compas.geometry.Point`
        The base point of the frame.
    quaternion : :class:`compas.geometry.Quaternion`, read-only
        The quaternion from the rotation given by the frame.
    xaxis : :class:`compas.geometry.Vector`
        The local X axis of the frame.
    yaxis : :class:`compas.geometry.Vector`
        The local Y axis of the frame.
    zaxis : :class:`compas.geometry.Vector`, read-only
        The Z axis of the frame.

    Notes
    -----
    All input vectors are orthonormalized when creating a frame, with the first
    vector as starting point.

    Examples
    --------
    >>> from compas.geometry import Point
    >>> from compas.geometry import Vector
    >>> f = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
    >>> f = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0))
    >>> f = Frame([0, 0, 0])

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "point": Point.DATASCHEMA,
            "xaxis": Vector.DATASCHEMA,
            "yaxis": Vector.DATASCHEMA,
        },
        "required": ["point", "xaxis", "yaxis"],
    }

    @property
    def __data__(self):
        return {
            "point": self.point.__data__,
            "xaxis": self.xaxis.__data__,
            "yaxis": self.yaxis.__data__,
        }

    def __init__(self, point, xaxis=None, yaxis=None, name=None):
        super(Frame, self).__init__(name=name)
        self._point = None
        self._xaxis = None
        self._yaxis = None
        self._zaxis = None
        self.point = point
        self.xaxis = Vector(1, 0, 0) if xaxis is None else xaxis
        self.yaxis = Vector(0, 1, 0) if yaxis is None else yaxis

    def __repr__(self):
        return "{0}(point={1!r}, xaxis={2!r}, yaxis={3!r})".format(
            type(self).__name__,
            self.point,
            self.xaxis,
            self.yaxis,
        )

    def __str__(self):
        return "{0}(point={1}, xaxis={2}, yaxis={3})".format(
            type(self).__name__,
            str(self.point),
            str(self.xaxis),
            str(self.yaxis),
        )

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if key == 0:
            return self.point
        if key == 1:
            return self.xaxis
        if key == 2:
            return self.yaxis
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.point = value
            return
        if key == 1:
            self.xaxis = value
            return
        if key == 2:
            self.yaxis = value
        raise KeyError

    def __iter__(self):
        return iter([self.point, self.xaxis, self.yaxis])

    def __eq__(self, other):
        if not hasattr(other, "__iter__") or not hasattr(other, "__len__") or len(self) != len(other):
            return False
        return self.point == other[0] and self.xaxis == other[1] and self.yaxis == other[2]

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def point(self):
        if not self._point:
            raise ValueError("The frame has no origin.")
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def xaxis(self):
        if not self._xaxis:
            raise ValueError("The frame has no x-axis.")
        return self._xaxis

    @xaxis.setter
    def xaxis(self, vector):
        xaxis = Vector(*vector)
        xaxis.unitize()
        self._xaxis = xaxis
        self._zaxis = None

    @property
    def yaxis(self):
        if not self._yaxis:
            raise ValueError("The frame has no y-axis.")
        return self._yaxis

    @yaxis.setter
    def yaxis(self, vector):
        yaxis = Vector(*vector)
        yaxis.unitize()
        zaxis = self.xaxis.cross(yaxis)
        zaxis.unitize()
        self._yaxis = zaxis.cross(self.xaxis)
        self._zaxis = None

    @property
    def normal(self):
        return self.zaxis

    @property
    def zaxis(self):
        if not self._zaxis:
            self._zaxis = self.xaxis.cross(self.yaxis)
        return self._zaxis

    def axes(self):
        return [self.xaxis, self.yaxis, self.zaxis]

    @property
    def quaternion(self):
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return Quaternion(*quaternion_from_matrix(R))

    @property
    def axis_angle_vector(self):
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return Vector(*axis_angle_vector_from_matrix(R))

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def worldXY(cls):  # type: () -> Frame
        """Construct the world XY frame.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The world XY frame.

        Examples
        --------
        >>> frame = Frame.worldXY()
        >>> print(frame.point)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(frame.xaxis)
        Vector(x=1.000, y=0.000, z=0.000)
        >>> print(frame.yaxis)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        return cls([0, 0, 0], [1, 0, 0], [0, 1, 0])

    @classmethod
    def worldZX(cls):  # type: () -> Frame
        """Construct the world ZX frame.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The world ZX frame.

        Examples
        --------
        >>> frame = Frame.worldZX()
        >>> print(frame.point)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(frame.xaxis)
        Vector(x=0.000, y=0.000, z=1.000)
        >>> print(frame.yaxis)
        Vector(x=1.000, y=0.000, z=0.000)

        """
        return cls([0, 0, 0], [0, 0, 1], [1, 0, 0])

    @classmethod
    def worldYZ(cls):  # type: () -> Frame
        """Construct the world YZ frame.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The world YZ frame.

        Examples
        --------
        >>> frame = Frame.worldYZ()
        >>> print(frame.point)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(frame.xaxis)
        Vector(x=0.000, y=1.000, z=0.000)
        >>> print(frame.yaxis)
        Vector(x=0.000, y=0.000, z=1.000)

        """
        return cls([0, 0, 0], [0, 1, 0], [0, 0, 1])

    @classmethod
    def from_points(cls, point, point_xaxis, point_xyplane):  # type: (...) -> Frame
        """Constructs a frame from 3 points.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The origin of the frame.
        point_xaxis : [float, float, float] | :class:`compas.geometry.Point`
            A point on the x-axis of the frame.
        point_xyplane : [float, float, float] | :class:`compas.geometry.Point`
            A point within the xy-plane of the frame.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> frame = Frame.from_points([0, 0, 0], [1, 0, 0], [0, 1, 0])
        >>> print(frame.point)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(frame.xaxis)
        Vector(x=1.000, y=0.000, z=0.000)
        >>> print(frame.yaxis)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        xaxis = subtract_vectors(point_xaxis, point)
        xyvec = subtract_vectors(point_xyplane, point)
        yaxis = cross_vectors(cross_vectors(xaxis, xyvec), xaxis)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_rotation(cls, rotation, point=[0, 0, 0]):  # type: (...) -> Frame
        """Constructs a frame from a Rotation.

        Parameters
        ----------
        rotation : :class:`compas.geometry.Rotation`
            The rotation defines the orientation of the frame.
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            The origin of the frame.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.geometry import Rotation
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> R = Rotation.from_frame(f1)
        >>> f2 = Frame.from_rotation(R, point=f1.point)
        >>> f1 == f2
        True

        """
        xaxis, yaxis = rotation.basis_vectors
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_transformation(cls, transformation):  # type: (...) -> Frame
        """Constructs a frame from a Transformation.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`
            The transformation defines the orientation of the frame through the
            rotation and the origin through the translation.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.geometry import Transformation
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.from_transformation(T)
        >>> f1 == f2
        True

        """
        xaxis, yaxis = transformation.basis_vectors
        point = transformation.translation_vector
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_matrix(cls, matrix):  # type: (...) -> Frame
        """Construct a frame from a matrix.

        Parameters
        ----------
        matrix : list[list[float]]
            The 4x4 transformation matrix in row-major order.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.geometry import matrix_from_euler_angles
        >>> from compas.tolerance import TOL
        >>> ea1 = [0.5, 0.4, 0.8]
        >>> M = matrix_from_euler_angles(ea1)
        >>> f = Frame.from_matrix(M)
        >>> ea2 = f.euler_angles()
        >>> TOL.is_allclose(ea1, ea2)
        True

        """
        _, _, angles, point, _ = decompose_matrix(matrix)
        R = matrix_from_euler_angles(angles, static=True, axes="xyz")
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_list(cls, values):  # type: (...) -> Frame
        """Construct a frame from a list of 12 or 16 float values.

        Parameters
        ----------
        values : list[float]
            The list of 12 or 16 values representing a 4x4 matrix.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Raises
        ------
        ValueError
            If the length of the list is neither 12 nor 16.

        Notes
        -----
        Since the transformation matrix follows the row-major order, the
        translational components must be at the list's indices 3, 7, 11.

        Examples
        --------
        >>> l = [-1.0, 0.0, 0.0, 8110, 0.0, 0.0, -1.0, 7020, 0.0, -1.0, 0.0, 1810]
        >>> f = Frame.from_list(l)

        """
        if len(values) == 12:
            values.extend([0.0, 0.0, 0.0, 1.0])
        if len(values) != 16:
            raise ValueError("Expected 12 or 16 floats but got %d" % len(values))

        matrix = [[0.0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                matrix[i][j] = float(values[i * 4 + j])

        return cls.from_matrix(matrix)

    @classmethod
    def from_quaternion(cls, quaternion, point=[0, 0, 0]):  # type: (...) -> Frame
        """Construct a frame from a rotation represented by quaternion coefficients.

        Parameters
        ----------
        quaternion : [float, float, float, float] | :class:`compas.geometry.Quaternion`
            Four numbers that represent the four coefficient values of a quaternion.
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            The point of the frame.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> q1 = [0.945, -0.021, -0.125, 0.303]
        >>> f = Frame.from_quaternion(q1, point=[1.0, 1.0, 1.0])
        >>> q2 = f.quaternion
        >>> TOL.is_allclose(q1, q2, atol=1e-3)
        True

        """
        R = matrix_from_quaternion(quaternion)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_axis_angle_vector(cls, axis_angle_vector, point=[0, 0, 0]):  # type: (...) -> Frame
        """Construct a frame from an axis-angle vector representing the rotation.

        Parameters
        ----------
        axis_angle_vector : [float, float, float]
            Three numbers that represent the axis of rotation and angle of
            rotation by its magnitude.
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            The point of the frame.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> aav1 = [-0.043, -0.254, 0.617]
        >>> f = Frame.from_axis_angle_vector(aav1, point=[0, 0, 0])
        >>> aav2 = f.axis_angle_vector
        >>> TOL.is_allclose(aav1, aav2, atol=1e-3)
        True

        """
        R = matrix_from_axis_angle_vector(axis_angle_vector)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_euler_angles(cls, euler_angles, static=True, axes="xyz", point=[0, 0, 0]):  # type: (...) -> Frame
        """Construct a frame from a rotation represented by Euler angles.

        Parameters
        ----------
        euler_angles : [float, float, float]
            Three numbers that represent the angles of rotations about the defined axes.
        static : bool, optional
            If True, the rotations are applied to a static frame.
            If False, to a rotational.
        axes : str, optional
            A 3 character string specifying the order of the axes.
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            The point of the frame.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> ea1 = 1.4, 0.5, 2.3
        >>> f = Frame.from_euler_angles(ea1, static=True, axes="xyz")
        >>> ea2 = f.euler_angles(static=True, axes="xyz")
        >>> TOL.is_allclose(ea1, ea2)
        True

        """
        R = matrix_from_euler_angles(euler_angles, static, axes)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_plane(cls, plane):  # type: (...) -> Frame
        """Constructs a frame from a plane.

        Xaxis and yaxis are arbitrarily selected based on the plane's normal.

        Parameters
        ----------
        plane : [point, vector] | :class:`compas.geometry.Plane`
            A plane.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The constructed frame.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.tolerance import TOL
        >>> plane = Plane([0, 0, 0], [0, 0, 1])
        >>> frame = Frame.from_plane(plane)
        >>> TOL.is_allclose(frame.normal, plane.normal)
        True

        """
        point, normal = plane
        # To construct a frame we need to find a vector v that is perpendicular
        # to the plane's normal. This means that the dot-product of v with the
        # normal must be equal to 0, which is true for the following vectors:
        vectors = [
            Vector(-normal[1], normal[0], 0),
            Vector(0, -normal[2], normal[1]),
            Vector(normal[2], 0, -normal[0]),
        ]
        # But if we are unlucky, one of these vectors is (0, 0, 0), so we
        # choose the vector with the longest length as xaxis.
        idx = argmax([v.length for v in vectors])
        xaxis = vectors[idx]
        yaxis = cross_vectors(normal, xaxis)
        return cls(point, xaxis, yaxis)

    # ==========================================================================
    # Conversions
    # ==========================================================================

    def to_transformation(self):
        """Convert the frame to a transformation.

        Returns
        -------
        :class:`compas.geometry.Transformation`
            The transformation.

        """
        return Transformation.from_frame(self)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def invert(self):
        """Invert the frame while keeping the X axis fixed."""
        self._yaxis = self.yaxis * -1
        self._zaxis = None

    flip = invert

    def inverted(self):
        """Return an inverted copy of the frame."""
        frame = self.copy()  # type: Frame
        frame.invert()
        return frame

    flipped = inverted

    def interpolate_frame(self, other, t):
        """Interpolates between two frames at a given parameter t in the range [0, 1]

        Parameters
        ----------
        other : :class:`compas.geometry.Frame`
        t : float
            A parameter in the range [0-1].

        Returns
        -------
        :class:`compas.geometry.Frame`
            A list of the interpolated :class:`compas.geometry.Frame` instances.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> frame1 = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0))
        >>> frame2 = Frame(Point(1, 1, 1), Vector(0, 0, 1), Vector(0, 1, 0))
        >>> start_frame = frame1.interpolate_frame(frame2, 0)
        >>> TOL.is_allclose(start_frame.point, frame1.point) and TOL.is_allclose(start_frame.quaternion, frame1.quaternion)
        True
        """
        quat1 = Quaternion.from_frame(self)
        quat2 = Quaternion.from_frame(other)

        # Interpolate origin
        origin_interpolated = (self.point * (1.0 - t)) + other.point * t

        rot_interpolated = quat1.slerp(quat2, t)

        # Create a new frame with the interpolated position and orientation
        interpolated_frame = Frame.from_quaternion(rot_interpolated, point=origin_interpolated)

        return interpolated_frame

    def interpolate_frames(self, other, steps):
        """Generates a specified number of interpolated frames between two given frames

        Parameters
        ----------
        other : :class:`compas.geometry.Frame`
        steps : int
            The number of interpolated frames to return.

        Returns
        -------
        list of :class:`compas.geometry.Frame`

        Examples
        --------
        >>> frame1 = Frame(Point(0, 0, 0), Vector(1, 0, 0), Vector(0, 1, 0))
        >>> frame2 = Frame(Point(1, 1, 1), Vector(0, 0, 1), Vector(0, 1, 0))
        >>> steps = 5
        >>> frames = frame1.interpolate_frames(frame2, steps)
        >>> print(len(frames) == steps)
        True
        """
        return [self.interpolate_frame(other, t) for t in linspace(0, 1, steps)]

    def euler_angles(self, static=True, axes="xyz"):
        """The Euler angles from the rotation given by the frame.

        Parameters
        ----------
        static : bool, optional
            If True the rotations are applied to a static frame.
            If False, to a rotational.
        axes : str, optional
            A 3 character string specifying the order of the axes.

        Returns
        -------
        list[float]
            Three numbers that represent the angles of rotations about the defined axes.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> ea1 = 1.4, 0.5, 2.3
        >>> f = Frame.from_euler_angles(ea1, static=True, axes="xyz")
        >>> ea2 = f.euler_angles(static=True, axes="xyz")
        >>> TOL.is_allclose(ea1, ea2)
        True

        """
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return euler_angles_from_matrix(R, static, axes)

    def to_local_coordinates(self, obj_in_wcf):
        """Returns the object's coordinates in the local coordinate system of the frame.

        Parameters
        ----------
        obj_in_wcf : [float, float, float] | :class:`compas.geometry.Geometry`
            An object in the world coordinate frame.

        Returns
        -------
        :class:`compas.geometry.Geometry`
            The object in the local coordinate system of the frame.

        Notes
        -----
        If you pass a list of floats, it is assumed to represent a point.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> pw = Point(2, 2, 2)  # point in wcf
        >>> pl = frame.to_local_coordinates(pw)  # point in frame
        >>> print(frame.to_world_coordinates(pl))
        Point(x=2.000, y=2.000, z=2.000)

        """
        T = Transformation.from_change_of_basis(Frame.worldXY(), self)
        if isinstance(obj_in_wcf, (list, tuple)):
            return Point(*obj_in_wcf).transformed(T)
        return obj_in_wcf.transformed(T)

    def to_world_coordinates(self, obj_in_lcf):
        """Returns the object's coordinates in the global coordinate frame.

        Parameters
        ----------
        obj_in_lcf : [float, float, float] | :class:`compas.geometry.Geometry`
            An object in local coordinate system of the frame.

        Returns
        -------
        :class:`compas.geometry.Geometry`
            The object in the world coordinate frame.

        Notes
        -----
        If you pass a list of floats, it is assumed to represent a point.

        Examples
        --------
        >>> from compas.geometry import Point
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> pl = Point(1.632, -0.090, 0.573)  # point in frame
        >>> pw = frame.to_world_coordinates(pl)  # point in wcf
        >>> print(frame.to_local_coordinates(pw))
        Point(x=1.632, y=-0.090, z=0.573)

        """
        T = Transformation.from_change_of_basis(self, Frame.worldXY())
        if isinstance(obj_in_lcf, list):
            return Point(*obj_in_lcf).transformed(T)
        return obj_in_lcf.transformed(T)

    def transform(self, T):
        """Transform the frame.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation`
            The transformation.

        Examples
        --------
        >>> from compas.geometry import Transformation
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.worldXY()
        >>> f2.transform(T)
        >>> f1 == f2
        True

        """
        X = T * Transformation.from_frame(self)
        point = X.translation_vector
        xaxis, yaxis = X.basis_vectors
        self.point = point
        self.xaxis = xaxis
        self.yaxis = yaxis
