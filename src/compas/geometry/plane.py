from math import sqrt
from typing import TYPE_CHECKING
from typing import Iterator
from typing import Optional
from typing import Sequence
from typing import Union

from typing_extensions import Self

from compas._typing import Coordinates
from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Geometry
from compas.geometry import bestfit_plane
from compas.linalg.vectors import cross_vectors
from compas.tolerance import TOL

from ._typing import TransformationType
from .point import Point
from .vector import Vector

if TYPE_CHECKING:
    from compas.geometry import Frame
    from compas.geometry import Line


class Plane(Geometry):
    """A plane is defined by a base point and a normal vector.

    Parameters
    ----------
    point
        The base point of the plane.
    normal
        The normal vector of the plane.
    name
        The name of the plane.

    Examples
    --------
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> print(plane.point)
    Point(x=0.000, y=0.000, z=0.000)
    >>> print(plane.normal)
    Vector(x=0.000, y=0.000, z=1.000)

    A plane behaves as a two-item sequence containing its point and normal.

    >>> len(plane)
    2
    >>> list(plane) == [plane.point, plane.normal]
    True
    >>> plane[0] = [1, 2, 3]
    >>> plane.point == [1, 2, 3]
    True
    >>> plane[1] = [0, 1, 0]
    >>> plane.normal == [0, 1, 0]
    True
    >>> plane == [[1, 2, 3], [0, 1, 0]]
    True

    Planes can be constructed from points and vectors, equation coefficients,
    frames, point collections, or world-axis presets.

    >>> Plane.from_three_points([0, 0, 0], [1, 0, 0], [0, 1, 0]) == Plane.worldXY()
    True
    >>> Plane.from_point_and_two_vectors([0, 0, 0], [1, 0, 0], [0, 1, 0]) == Plane.worldXY()
    True
    >>> Plane.from_abcd([0, 0, 1, 0]) == Plane.worldXY()
    True
    >>> from compas.geometry import Frame
    >>> Plane.from_frame(Frame.worldXY()) == Plane.worldXY()
    True
    >>> Plane.from_points([[0, 0, 0], [1, 0, 0], [0, 1, 0]]) == Plane.worldXY()
    True
    >>> Plane.worldYZ().normal == [1, 0, 0]
    True
    >>> Plane.worldZX().normal == [0, 1, 0]
    True

    """

    @property
    def __data__(self) -> dict[str, list[float]]:
        """The data representation of the plane."""
        return {
            "point": self.point.__data__,
            "normal": self.normal.__data__,
        }

    def __init__(self, point: CoordinateType, normal: CoordinateType, name: Optional[str] = None) -> None:
        super().__init__(name=name)
        self._point: Optional[Point] = None
        self._normal: Optional[Vector] = None
        self.point = point
        self.normal = normal

    def __repr__(self) -> str:
        return "{0}(point={1!r}, normal={2!r})".format(
            type(self).__name__,
            self.point,
            self.normal,
        )

    def __str__(self) -> str:
        return "{0}(point={1}, normal={2})".format(
            type(self).__name__,
            str(self.point),
            str(self.normal),
        )

    def __len__(self) -> int:
        return 2

    def __getitem__(self, key: int) -> Union[Point, Vector]:
        if key == 0:
            return self.point
        if key == 1:
            return self.normal
        raise KeyError

    def __setitem__(self, key: int, value: CoordinateType) -> None:
        if key == 0:
            self.point = value
            return
        if key == 1:
            self.normal = value
            return
        raise KeyError

    def __iter__(self) -> Iterator[Union[Point, Vector]]:
        return iter([self.point, self.normal])

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Coordinates):
            return False
        if len(other) != 2:
            return False
        return self.point == other[0] and self.normal == other[1]

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def point(self) -> Point:
        """The base point of the plane.

        Notes
        -----
        Assigning a `Point` or three-component coordinate sequence creates an
        independent `Point` with the same coordinates.

        Examples
        --------
        >>> source = Point(1, 2, 3)
        >>> plane = Plane.worldXY()
        >>> plane.point = source
        >>> plane.point == source and plane.point is not source
        True
        >>> source.x = 10
        >>> plane.point == [1, 2, 3]
        True

        """
        if not self._point:
            raise ValueError("The plane has no point.")
        return self._point

    @point.setter
    def point(self, point: CoordinateType) -> None:
        self._point = Point(point[0], point[1], point[2])

    @property
    def normal(self) -> Vector:
        """The unit normal vector of the plane.

        Notes
        -----
        Assigning a `Vector` or three-component coordinate sequence creates an
        independent `Vector` and unitizes it.

        Examples
        --------
        >>> source = Vector(0, 0, 2)
        >>> plane = Plane.worldXY()
        >>> plane.normal = source
        >>> plane.normal == [0, 0, 1] and plane.normal is not source
        True
        >>> source.z = 4
        >>> plane.normal == [0, 0, 1]
        True

        """
        if not self._normal:
            raise ValueError("The plane has no normal.")
        return self._normal

    @normal.setter
    def normal(self, vector: CoordinateType) -> None:
        self._normal = Vector(vector[0], vector[1], vector[2])
        self._normal.unitize()

    @property
    def d(self) -> float:
        """The constant $d$ of the equation $ax + by + cz + d = 0$.

        Examples
        --------
        >>> Plane([0, 0, 2], [0, 0, 1]).d
        -2.0

        """
        a, b, c = self.normal
        x, y, z = self.point
        return -a * x - b * y - c * z

    @property
    def abcd(self) -> tuple[float, float, float, float]:
        """The coefficients of the equation $ax + by + cz + d = 0$.

        Examples
        --------
        >>> Plane([0, 0, 2], [0, 0, 1]).abcd
        (0.0, 0.0, 1.0, -2.0)

        """
        a, b, c = self.normal
        d = self.d
        return a, b, c, d

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_three_points(cls, a: CoordinateType, b: CoordinateType, c: CoordinateType) -> Self:
        """Construct a plane from three points in three-dimensional space.

        Parameters
        ----------
        a
            The first point.
        b
            The second point.
        c
            The third point.

        Returns
        -------
        Plane
            A plane with base point `a` and normal vector defined as the unitized
            cross product of the vectors `ab` and `ac`.

        Examples
        --------
        >>> plane = Plane.from_three_points([0.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 3.0, 0.0])
        >>> print(plane.point)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(plane.normal)
        Vector(x=0.000, y=0.000, z=1.000)

        """
        a = Point(a[0], a[1], a[2])
        b = Point(b[0], b[1], b[2])
        c = Point(c[0], c[1], c[2])
        normal_data = cross_vectors(b - a, c - a)
        normal = Vector(normal_data[0], normal_data[1], normal_data[2])
        return cls(a, normal)

    @classmethod
    def from_point_and_two_vectors(cls, point: CoordinateType, u: CoordinateType, v: CoordinateType) -> Self:
        """Construct a plane from a base point and two vectors.

        Parameters
        ----------
        point
            The base point.
        u
            The first vector.
        v
            The second vector.

        Returns
        -------
        Plane
            A plane with base point `point` and normal vector defined as the unitized
            cross product of vectors `u` and `v`.

        Examples
        --------
        >>> plane = Plane.from_point_and_two_vectors([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        >>> print(plane.point)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(plane.normal)
        Vector(x=0.000, y=0.000, z=1.000)

        """
        normal_data = cross_vectors(u, v)
        normal = Vector(normal_data[0], normal_data[1], normal_data[2])
        return cls(point, normal)

    @classmethod
    def from_abcd(cls, abcd: Sequence[float]) -> Self:
        """Construct a plane from the plane equation coefficients.

        Parameters
        ----------
        abcd
            The coefficients $a$, $b$, $c$, and $d$ of the equation
            $ax + by + cz + d = 0$.

        Returns
        -------
        Plane
            A plane satisfying the provided equation.

        Examples
        --------
        >>> plane = Plane.from_abcd([0, 0, 2, -4])
        >>> plane.point == [0, 0, 2]
        True
        >>> plane.normal == [0, 0, 1]
        True

        """
        a, b, c, d = abcd
        length = sqrt(a**2 + b**2 + c**2)
        normal = [a, b, c]
        factor = -d / length**2
        point = [a * factor, b * factor, c * factor]
        return cls(point, normal)

    @classmethod
    def worldXY(cls) -> Self:
        """Construct the world XY plane.

        Returns
        -------
        Plane
            The world XY plane.

        """
        return cls([0, 0, 0], [0, 0, 1])

    @classmethod
    def worldYZ(cls) -> Self:
        """Construct the world YZ plane.

        Returns
        -------
        Plane
            The world YZ plane.

        """
        return cls([0, 0, 0], [1, 0, 0])

    @classmethod
    def worldZX(cls) -> Self:
        """Construct the world ZX plane.

        Returns
        -------
        Plane
            The world ZX plane.

        """
        return cls([0, 0, 0], [0, 1, 0])

    @classmethod
    def from_frame(cls, frame: "Frame") -> Self:
        """Construct a plane from a frame.

        Parameters
        ----------
        frame
            The frame defining the plane.

        Returns
        -------
        Plane
            A plane with the frame's `point` and the frame's `normal`.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> plane = Plane.from_frame(frame)
        >>> print(plane.point)
        Point(x=1.000, y=1.000, z=1.000)
        >>> print(plane.normal)
        Vector(x=-0.299, y=-0.079, z=0.951)

        """
        return cls(frame.point, frame.normal)

    @classmethod
    def from_points(cls, points: CoordinatesType) -> Self:
        """Construct a plane from a collection of points.

        If the list contains more than three points, a plane is constructed that minimizes the distance to all points.

        Parameters
        ----------
        points
            The points.

        Returns
        -------
        Plane
            The plane defined by the points.

        See Also
        --------
        [`bestfit_plane`][compas.geometry.bestfit_plane] computes the best-fit
        plane used for collections containing other than three points.

        Examples
        --------
        >>> points = [[0.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 3.0, 0.0]]
        >>> plane = Plane.from_points(points)
        >>> print(plane.point)
        Point(x=0.000, y=0.000, z=0.000)
        >>> print(plane.normal)
        Vector(x=0.000, y=0.000, z=1.000)

        """
        if len(points) == 3:
            return cls.from_three_points(*points)
        point, normal = bestfit_plane(points)
        return cls(point, normal)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, transformation: TransformationType) -> None:
        """Transform this plane.

        Parameters
        ----------
        transformation
            The transformation.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> from compas.geometry import Transformation
        >>> from compas.geometry import Plane
        >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f)
        >>> plane = Plane.worldXY()
        >>> plane.transform(T)

        """
        self.point.transform(transformation)
        self.normal.transform(transformation)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def is_parallel(self, other: "Plane", tol: Optional[float] = None) -> bool:
        """Verify if this plane is parallel to another plane.

        Parameters
        ----------
        other
            The other plane.
        tol
            Tolerance for the dot product of the normals.
            Default is `TOL.absolute`.

        Returns
        -------
        bool
            `True` if the planes are parallel.
            `False` otherwise.

        Examples
        --------
        >>> plane1 = Plane.worldXY()
        >>> plane2 = Plane([1.0, 1.0, 1.0], [0.0, 0.0, 1.0])
        >>> plane1.is_parallel(plane2)
        True
        >>> plane1 = Plane.worldXY()
        >>> plane2 = Plane([1.0, 1.0, 1.0], [0.0, 0.0, -1.0])
        >>> plane1.is_parallel(plane2)
        True

        """
        return TOL.is_close(abs(self.normal.dot(other.normal)), 1, rtol=0, atol=tol)

    def is_perpendicular(self, other: "Plane", tol: Optional[float] = None) -> bool:
        """Verify if this plane is perpendicular to another plane.

        Parameters
        ----------
        other
            The other plane.
        tol
            Tolerance for the dot product of the normals.
            Default is `TOL.absolute`.

        Returns
        -------
        bool
            `True` if the planes are perpendicular.
            `False` otherwise.

        Examples
        --------
        >>> plane1 = Plane.worldXY()
        >>> plane2 = Plane([1.0, 1.0, 1.0], [0.0, 0.0, 1.0])
        >>> plane1.is_perpendicular(plane2)
        False

        """
        return TOL.is_zero(self.normal.dot(other.normal), tol)

    def contains_point(self, point: CoordinateType, tol: Optional[float] = None) -> bool:
        """Verify if a given point lies in the plane.

        Parameters
        ----------
        point
            The point.
        tol
            Tolerance for the distance from the point to the plane.
            Default is `TOL.absolute`.

        Returns
        -------
        bool
            `True` if the point lies in the plane.
            `False` otherwise.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> plane.contains_point([1.0, 1.0, 0.0])
        True

        """
        vector = self.point - point
        return TOL.is_zero(self.normal.dot(vector), tol)

    # move to Point.distance_to_plane?
    # point.distance_to_plane(plane)
    def distance_to_point(self, point: CoordinateType) -> float:
        """Compute the distance from a given point to the plane.

        Parameters
        ----------
        point
            The point.

        Returns
        -------
        float
            The distance from the point to the plane.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> plane.distance_to_point([1.0, 1.0, 1.0])
        1.0

        """
        vector = self.point - point
        return abs(self.normal.dot(vector))

    # move to Point.closest_on_plane?
    # point.closest_on_plane(plane)
    # remove entirely?
    def closest_point(self, point: CoordinateType) -> Point:
        """Compute the closest point on the plane to a given point.

        Parameters
        ----------
        point
            The point.

        Returns
        -------
        Point
            The closest point on the plane.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> point = plane.closest_point([1.0, 1.0, 1.0])
        >>> print(point)
        Point(x=1.000, y=1.000, z=0.000)

        """
        point = Point(point[0], point[1], point[2])
        vector = self.point - point
        distance = self.normal.dot(vector)
        return point + self.normal.scaled(distance)

    # move to Point.proejcted_on_plane?
    # point.projected_on_plane(plane)
    # point.project_on_plane(plane)
    def projected_point(self, point: CoordinateType, direction: Optional[CoordinateType] = None) -> Optional[Point]:
        """Returns the projection of a given point onto the plane.

        Parameters
        ----------
        point
            The point.
        direction
            The projection direction. If omitted, the projection follows the
            plane normal.

        Returns
        -------
        Optional[Point]
            The projected point, or None if a direction is given and it is parallel to the plane.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> point = plane.projected_point([1.0, 1.0, 1.0])
        >>> print(point)
        Point(x=1.000, y=1.000, z=0.000)

        """
        if not direction:
            return self.closest_point(point)

        from compas.geometry import Line

        line = Line.from_point_and_vector(point, direction)
        intersection = self.intersection_with_line(line)
        return intersection

    # move to Point.mirrored_by_plane?
    # point.mirrored_by_plane(plane)
    # point.mirror_by_plane(plane)
    def mirrored_point(self, point: CoordinateType) -> Point:
        """Returns the mirror image of a given point.

        Parameters
        ----------
        point
            The point.

        Returns
        -------
        Point
            The mirrored point.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> point = plane.mirrored_point([1.0, 1.0, 1.0])
        >>> print(point)
        Point(x=1.000, y=1.000, z=-1.000)

        """
        point = Point(point[0], point[1], point[2])
        vector = self.point - point
        distance = self.normal.dot(vector)
        return point + self.normal.scaled(2 * distance)

    def intersection_with_line(self, line: "Line", tol: Optional[float] = None) -> Optional[Point]:
        """Compute the intersection of a plane and a line.

        Parameters
        ----------
        line
            The line.
        tol
            Tolerance for the dot product of the line vector and the plane normal.
            Default is `TOL.absolute`.

        Returns
        -------
        Optional[Point]
            The intersection point, or `None` if the line is parallel to the plane.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> plane = Plane.worldXY()
        >>> line = Line.from_point_and_vector(Point(0, 0, 1), Vector(1, 1, 1))
        >>> point = plane.intersection_with_line(line)
        >>> print(point)
        Point(x=-1.000, y=-1.000, z=0.000)

        """
        # The line is parallel to the plane
        if TOL.is_zero(self.normal.dot(line.vector), tol):
            return None

        t = (self.point - line.start).dot(self.normal) / line.vector.dot(self.normal)
        return line.point_at(t)

    def intersection_with_plane(self, plane: "Plane") -> Optional["Line"]:
        """Compute the intersection of two planes.

        Parameters
        ----------
        plane
            The other plane.

        Returns
        -------
        Optional[Line]
            The intersection line, or None if the planes are parallel or coincident.

        Examples
        --------
        >>> plane1 = Plane.worldXY()
        >>> plane2 = Plane([1.0, 1.0, 1.0], [0.0, 0.0, 1.0])
        >>> line = plane1.intersection_with_plane(plane2)

        """
        from compas.geometry import Line

        if self.is_parallel(plane):
            return None

        # direction of the line
        direction = self.normal.cross(plane.normal)

        # point on the line
        line = Line(self.point, self.point + self.normal.cross(direction))
        point = plane.intersection_with_line(line)
        if point is None:
            return None

        return Line(point, point + direction)

    def offset(self, distance: float) -> Self:
        """Returns a new offset plane by a given distance.

        The plane normal is used as positive direction.

        Parameters
        ----------
        distance
            The offset distance.

        Returns
        -------
        Plane
            The offset plane.

        """
        return type(self)(self.point + self.normal.scaled(distance), self.normal)
