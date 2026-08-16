from typing import Iterator
from typing import MutableSequence
from typing import Optional
from typing import Sequence
from typing import TypeVar
from typing import Union
from typing import overload

from typing_extensions import Self

from compas._typing import Coordinates
from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Geometry
from compas.geometry import Transformation
from compas.itertools import linspace
from compas.linalg.transformations import axis_angle_vector_from_matrix
from compas.linalg.transformations import basis_vectors_from_matrix
from compas.linalg.transformations import decompose_matrix
from compas.linalg.transformations import euler_angles_from_matrix
from compas.linalg.transformations import matrix_from_axis_angle_vector
from compas.linalg.transformations import matrix_from_basis_vectors
from compas.linalg.transformations import matrix_from_euler_angles
from compas.linalg.transformations import matrix_from_quaternion
from compas.linalg.transformations import quaternion_from_matrix
from compas.linalg.vectors import argmax
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import subtract_vectors

from ._typing import PlaneType
from ._typing import QuaternionType
from ._typing import TransformationType
from .point import Point
from .quaternion import Quaternion
from .vector import Vector

GeometryType = TypeVar("GeometryType", bound=Geometry)


class Frame(Geometry):
    """A frame is defined by a base point and two orthonormal base vectors.

    Parameters
    ----------
    point
        The origin of the frame.
    xaxis
        The x-axis of the frame. Defaults to the unit X vector.
    yaxis
        The y-axis of the frame. Defaults to the unit Y vector.
    name
        The name of the frame.

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

    `Frame` implements `__len__`, `__iter__`, `__getitem__`, and `__setitem__`.
    Its three items are the origin, X axis, and Y axis, in that order.

    >>> len(f)
    3
    >>> list(f) == [f.point, f.xaxis, f.yaxis]
    True
    >>> f[0] = [1.0, 2.0, 3.0]
    >>> f.point == [1.0, 2.0, 3.0]
    True

    Frames compare equal to other three-item frame representations when their
    origin and axes are equal within the configured tolerance.

    >>> f == [f.point, f.xaxis, f.yaxis]
    True

    Frames can be constructed from world-axis presets or three points.

    >>> Frame.worldXY() == Frame.from_points([0, 0, 0], [1, 0, 0], [0, 1, 0])
    True
    >>> Frame.worldZX().xaxis == [0, 0, 1]
    True
    >>> Frame.worldYZ().xaxis == [0, 1, 0]
    True

    Transformations, rotations, matrices, and flat matrix data can also define
    a frame.

    >>> from compas.geometry import Rotation
    >>> from compas.geometry import Transformation
    >>> identity = Frame.worldXY()
    >>> Frame.from_rotation(Rotation()) == identity
    True
    >>> transformation = Transformation.from_frame(identity)
    >>> Frame.from_transformation(transformation) == identity
    True
    >>> Frame.from_matrix(transformation.matrix) == identity
    True
    >>> values = [value for row in transformation.matrix for value in row]
    >>> Frame.from_list(values) == identity
    True

    Rotation coefficients and planes provide further constructor forms.

    >>> Frame.from_quaternion([1, 0, 0, 0]) == identity
    True
    >>> Frame.from_axis_angle_vector([0, 0, 0]) == identity
    True
    >>> Frame.from_euler_angles([0, 0, 0]) == identity
    True
    >>> from compas.geometry import Plane
    >>> Frame.from_plane(Plane.worldXY()).normal == [0, 0, 1]
    True

    """

    @property
    def __data__(self) -> dict[str, list[float]]:
        """The data representation of the frame."""
        return {
            "point": self.point.__data__,
            "xaxis": self.xaxis.__data__,
            "yaxis": self.yaxis.__data__,
        }

    def __init__(
        self,
        point: CoordinateType,
        xaxis: Optional[CoordinateType] = None,
        yaxis: Optional[CoordinateType] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self._point = None
        self._xaxis = None
        self._yaxis = None
        self._zaxis = None
        self.point = point
        self.xaxis = Vector(1, 0, 0) if xaxis is None else xaxis
        self.yaxis = Vector(0, 1, 0) if yaxis is None else yaxis

    def __repr__(self) -> str:
        return "{0}(point={1!r}, xaxis={2!r}, yaxis={3!r})".format(
            type(self).__name__,
            self.point,
            self.xaxis,
            self.yaxis,
        )

    def __str__(self) -> str:
        return "{0}(point={1}, xaxis={2}, yaxis={3})".format(
            type(self).__name__,
            str(self.point),
            str(self.xaxis),
            str(self.yaxis),
        )

    def __len__(self) -> int:
        return 3

    def __getitem__(self, key: int) -> Union[Point, Vector]:
        if key == 0:
            return self.point
        if key == 1:
            return self.xaxis
        if key == 2:
            return self.yaxis
        raise KeyError

    def __setitem__(self, key: int, value: CoordinateType) -> None:
        if key == 0:
            self.point = value
            return
        if key == 1:
            self.xaxis = value
            return
        if key == 2:
            self.yaxis = value
            return
        raise KeyError

    def __iter__(self) -> Iterator[Union[Point, Vector]]:
        return iter([self.point, self.xaxis, self.yaxis])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinates):
            return False
        if len(self) != len(other):
            return False
        return self.point == other[0] and self.xaxis == other[1] and self.yaxis == other[2]

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def point(self) -> Point:
        """The origin of the frame.

        Notes
        -----
        Assigning a `Point` or three-component coordinate sequence creates an
        independent `Point` with the same coordinates.

        Examples
        --------
        >>> source = Point(1, 2, 3)
        >>> frame = Frame.worldXY()
        >>> frame.point = source
        >>> frame.point == source and frame.point is not source
        True
        >>> source.x = 10
        >>> frame.point == [1, 2, 3]
        True

        """
        if not self._point:
            raise ValueError("The frame has no origin.")
        return self._point

    @point.setter
    def point(self, point: CoordinateType) -> None:
        self._point = Point(point[0], point[1], point[2])

    @property
    def xaxis(self) -> Vector:
        """The unit X axis of the frame.

        Notes
        -----
        Assigning a `Vector` or three-component coordinate sequence creates an
        independent, unitized `Vector`. The Y axis is made orthogonal to the new
        X axis and the cached Z axis is invalidated.

        Examples
        --------
        >>> source = Vector(1, 1, 0)
        >>> frame = Frame.worldXY()
        >>> frame.xaxis = source
        >>> frame.xaxis is not source
        True
        >>> frame.xaxis.dot(frame.yaxis)
        0.0

        """
        if not self._xaxis:
            raise ValueError("The frame has no x-axis.")
        return self._xaxis

    @xaxis.setter
    def xaxis(self, vector: CoordinateType) -> None:
        xaxis = Vector(vector[0], vector[1], vector[2])
        if not xaxis.length:
            raise ValueError("The X axis cannot be a zero vector.")
        xaxis.unitize()
        yaxis = self._yaxis
        if self._yaxis is not None:
            zaxis = xaxis.cross(self._yaxis)
            if not zaxis.length:
                raise ValueError("The X and Y axes cannot be parallel.")
            zaxis.unitize()
            yaxis = zaxis.cross(xaxis)
        self._xaxis = xaxis
        self._yaxis = yaxis
        self._zaxis = None

    @property
    def yaxis(self) -> Vector:
        """The unit Y axis of the frame.

        Notes
        -----
        Assigning a `Vector` or three-component coordinate sequence creates an
        independent vector. The input is unitized and then made orthogonal to
        the X axis; the cached Z axis is invalidated.

        Examples
        --------
        >>> source = Vector(1, 1, 0)
        >>> frame = Frame.worldXY()
        >>> frame.yaxis = source
        >>> frame.yaxis == [0, 1, 0] and frame.yaxis is not source
        True
        >>> frame.xaxis.dot(frame.yaxis)
        0.0

        """
        if not self._yaxis:
            raise ValueError("The frame has no y-axis.")
        return self._yaxis

    @yaxis.setter
    def yaxis(self, vector: CoordinateType) -> None:
        yaxis = Vector(vector[0], vector[1], vector[2])
        if not yaxis.length:
            raise ValueError("The Y axis cannot be a zero vector.")
        yaxis.unitize()
        zaxis = self.xaxis.cross(yaxis)
        if not zaxis.length:
            raise ValueError("The X and Y axes cannot be parallel.")
        zaxis.unitize()
        self._yaxis = zaxis.cross(self.xaxis)
        self._zaxis = None

    @property
    def normal(self) -> Vector:
        """The normal of the frame, equivalent to its Z axis.

        Examples
        --------
        >>> frame = Frame.worldXY()
        >>> frame.normal is frame.zaxis
        True

        """
        return self.zaxis

    @property
    def zaxis(self) -> Vector:
        """The unit Z axis defined by the cross product of X and Y.

        Notes
        -----
        The Z axis is computed on first access and cached until either input
        axis changes.

        Examples
        --------
        >>> frame = Frame.worldXY()
        >>> frame.zaxis == [0, 0, 1]
        True
        >>> frame.zaxis is frame.zaxis
        True

        """
        if not self._zaxis:
            self._zaxis = self.xaxis.cross(self.yaxis)
        return self._zaxis

    def axes(self) -> list[Vector]:
        return [self.xaxis, self.yaxis, self.zaxis]

    @property
    def quaternion(self) -> Quaternion:
        """The rotation of the frame represented as a quaternion.

        Examples
        --------
        >>> Frame.worldXY().quaternion == [1, 0, 0, 0]
        True

        """
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        values = quaternion_from_matrix(R)
        return Quaternion(values[0], values[1], values[2], values[3])

    @property
    def axis_angle_vector(self) -> Vector:
        """The rotation of the frame represented as an axis-angle vector.

        Examples
        --------
        >>> Frame.worldXY().axis_angle_vector == [0, 0, 0]
        True

        """
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        values = axis_angle_vector_from_matrix(R)
        return Vector(values[0], values[1], values[2])

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def worldXY(cls) -> Self:
        """Construct the world XY frame.

        Returns
        -------
        Self
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
    def worldZX(cls) -> Self:
        """Construct the world ZX frame.

        Returns
        -------
        Self
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
    def worldYZ(cls) -> Self:
        """Construct the world YZ frame.

        Returns
        -------
        Self
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
    def from_points(cls, point: CoordinateType, point_xaxis: CoordinateType, point_xyplane: CoordinateType) -> Self:
        """Constructs a frame from 3 points.

        Parameters
        ----------
        point
            The origin of the frame.
        point_xaxis
            A point on the x-axis of the frame.
        point_xyplane
            A point within the xy-plane of the frame.

        Returns
        -------
        Self
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
    def from_rotation(cls, rotation: Transformation, point: CoordinateType = (0, 0, 0)) -> Self:
        """Constructs a frame from a Rotation.

        Parameters
        ----------
        rotation
            The rotation defines the orientation of the frame.
        point
            The origin of the frame.

        Returns
        -------
        Self
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
    def from_transformation(cls, transformation: Transformation) -> Self:
        """Constructs a frame from a Transformation.

        Parameters
        ----------
        transformation
            The transformation defines the orientation of the frame through the
            rotation and the origin through the translation.

        Returns
        -------
        Self
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
    def from_matrix(cls, matrix: CoordinatesType) -> Self:
        """Construct a frame from a matrix.

        Parameters
        ----------
        matrix
            The 4x4 transformation matrix in row-major order.

        Returns
        -------
        Self
            The constructed frame.

        Examples
        --------
        >>> from compas.linalg import matrix_from_euler_angles
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
    def from_list(cls, values: MutableSequence[float]) -> Self:
        """Construct a frame from a list of 12 or 16 float values.

        Parameters
        ----------
        values
            The list of 12 or 16 values representing a 4x4 matrix.

        Returns
        -------
        Self
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
    def from_quaternion(cls, quaternion: QuaternionType, point: CoordinateType = (0, 0, 0)) -> Self:
        """Construct a frame from a rotation represented by quaternion coefficients.

        Parameters
        ----------
        quaternion
            Four numbers that represent the four coefficient values of a quaternion.
        point
            The point of the frame.

        Returns
        -------
        Self
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
    def from_axis_angle_vector(cls, axis_angle_vector: CoordinateType, point: CoordinateType = (0, 0, 0)) -> Self:
        """Construct a frame from an axis-angle vector representing the rotation.

        Parameters
        ----------
        axis_angle_vector
            Three numbers that represent the axis of rotation and angle of
            rotation by its magnitude.
        point
            The point of the frame.

        Returns
        -------
        Self
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
    def from_euler_angles(
        cls,
        euler_angles: Sequence[float],
        static: bool = True,
        axes: str = "xyz",
        point: CoordinateType = (0, 0, 0),
    ) -> Self:
        """Construct a frame from a rotation represented by Euler angles.

        Parameters
        ----------
        euler_angles
            Three numbers that represent the angles of rotations about the defined axes.
        static
            If True, the rotations are applied to a static frame.
            If False, to a rotational.
        axes
            A 3 character string specifying the order of the axes.
        point
            The point of the frame.

        Returns
        -------
        Self
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
    def from_plane(cls, plane: PlaneType) -> Self:
        """Constructs a frame from a plane.

        Xaxis and yaxis are arbitrarily selected based on the plane's normal.

        Parameters
        ----------
        plane
            A plane.

        Returns
        -------
        Self
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

    def to_transformation(self) -> Transformation:
        """Convert the frame to a transformation.

        Returns
        -------
        Transformation
            The transformation.

        """
        return Transformation.from_frame(self)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def invert(self) -> None:
        """Invert the frame while keeping the X axis fixed."""
        self._yaxis = self.yaxis * -1
        self._zaxis = None

    flip = invert

    def inverted(self) -> Self:
        """Return an inverted copy of the frame."""
        frame = self.copy()
        frame.invert()
        return frame

    flipped = inverted

    def interpolate_frame(self, other: "Frame", t: float) -> Self:
        """Interpolates between two frames at a given parameter t in the range [0, 1]

        Parameters
        ----------
        other
            The other frame.
        t
            A parameter in the range [0-1].

        Returns
        -------
        Self
            The interpolated frame.

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
        interpolated_frame = type(self).from_quaternion(rot_interpolated, point=origin_interpolated)

        return interpolated_frame

    def interpolate_frames(self, other: "Frame", steps: int) -> list[Self]:
        """Generates a specified number of interpolated frames between two given frames

        Parameters
        ----------
        other
            The other frame.
        steps
            The number of interpolated frames to return.

        Returns
        -------
        list[Self]
            The interpolated frames.

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

    def euler_angles(self, static: bool = True, axes: str = "xyz") -> list[float]:
        """The Euler angles from the rotation given by the frame.

        Parameters
        ----------
        static
            If True the rotations are applied to a static frame.
            If False, to a rotational.
        axes
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

    @overload
    def to_local_coordinates(self, obj_in_wcf: CoordinateType) -> Point: ...

    @overload
    def to_local_coordinates(self, obj_in_wcf: GeometryType) -> GeometryType: ...

    def to_local_coordinates(self, obj_in_wcf: Union[CoordinateType, GeometryType]) -> Union[Point, GeometryType]:
        """Returns the object's coordinates in the local coordinate system of the frame.

        Parameters
        ----------
        obj_in_wcf
            An object in the world coordinate frame.

        Returns
        -------
        Point
            A point in local coordinates if `obj_in_wcf` is raw coordinates.
        GeometryType
            A transformed geometry of the same type if `obj_in_wcf` is a geometry object.

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
        if isinstance(obj_in_wcf, Geometry):
            return obj_in_wcf.transformed(T)
        return Point(obj_in_wcf[0], obj_in_wcf[1], obj_in_wcf[2]).transformed(T)

    @overload
    def to_world_coordinates(self, obj_in_lcf: CoordinateType) -> Point: ...

    @overload
    def to_world_coordinates(self, obj_in_lcf: GeometryType) -> GeometryType: ...

    def to_world_coordinates(self, obj_in_lcf: Union[CoordinateType, GeometryType]) -> Union[Point, GeometryType]:
        """Returns the object's coordinates in the global coordinate frame.

        Parameters
        ----------
        obj_in_lcf
            An object in local coordinate system of the frame.

        Returns
        -------
        Point
            A point in world coordinates if `obj_in_lcf` is raw coordinates.
        GeometryType
            A transformed geometry of the same type if `obj_in_lcf` is a geometry object.

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
        if isinstance(obj_in_lcf, Geometry):
            return obj_in_lcf.transformed(T)
        return Point(obj_in_lcf[0], obj_in_lcf[1], obj_in_lcf[2]).transformed(T)

    def transform(self, transformation: TransformationType) -> None:
        """Transform the frame.

        Parameters
        ----------
        transformation
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
        # Frame transformation uses concatenation, so raw matrix inputs need the
        # same lightweight wrapper accepted by the base geometry API.
        if not isinstance(transformation, Transformation):
            transformation = Transformation(transformation)
        X = transformation * Transformation.from_frame(self)
        point = X.translation_vector
        xaxis, yaxis = X.basis_vectors
        self.point = point
        self.xaxis = xaxis
        self.yaxis = yaxis
