from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import sqrt

from compas.geometry import Geometry
from compas.geometry import bestfit_plane
from compas.geometry import cross_vectors
from compas.tolerance import TOL

from .point import Point
from .vector import Vector


class Plane(Geometry):
    """A plane is defined by a base point and a normal vector.

    Parameters
    ----------
    point : [float, float, float] | :class:`compas.geometry.Point`
        The base point of the plane.
    normal : [float, float, float] | :class:`compas.geometry.Vector`
        The normal vector of the plane.
    name : str, optional
        The name of the plane.

    Attributes
    ----------
    abcd : list[float], read-only
        The coefficients of the plane equation.
    d : float, read-only
        The *d* parameter of the linear equation describing the plane.
    normal : :class:`compas.geometry.Vector`
        The normal vector of the plane.
    point : :class:`compas.geometry.Plane`
        The base point of the plane.

    Examples
    --------
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> print(plane.point)
    Point(x=0.000, y=0.000, z=0.000)
    >>> print(plane.normal)
    Vector(x=0.000, y=0.000, z=1.000)

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "point": Point.DATASCHEMA,
            "normal": Vector.DATASCHEMA,
        },
        "required": ["point", "normal"],
    }

    @property
    def __data__(self):
        return {
            "point": self.point.__data__,
            "normal": self.normal.__data__,
        }

    def __init__(self, point, normal, name=None):
        super(Plane, self).__init__(name=name)
        self._point = None
        self._normal = None
        self.point = point
        self.normal = normal

    def __repr__(self):
        return "{0}(point={1!r}, normal={2!r})".format(
            type(self).__name__,
            self.point,
            self.normal,
        )

    def __str__(self):
        return "{0}(point={1}, normal={2})".format(
            type(self).__name__,
            str(self.point),
            str(self.normal),
        )

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.point
        if key == 1:
            return self.normal
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.point = value
            return
        if key == 1:
            self.normal = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.point, self.normal])

    def __eq__(self, other):
        return self.point == other[0] and self.normal == other[1]

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def point(self):
        if not self._point:
            raise ValueError("The plane has no point.")
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def normal(self):
        if not self._normal:
            raise ValueError("The plane has no normal.")
        return self._normal

    @normal.setter
    def normal(self, vector):
        self._normal = Vector(*vector)
        self._normal.unitize()

    @property
    def d(self):
        a, b, c = self.normal
        x, y, z = self.point
        return -a * x - b * y - c * z

    @property
    def abcd(self):
        a, b, c = self.normal
        d = self.d
        return a, b, c, d

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_three_points(cls, a, b, c):  # type: (...) -> Plane
        """Construct a plane from three points in three-dimensional space.

        Parameters
        ----------
        a : [float, float, float] | :class:`compas.geometry.Point`
            The first point.
        b : [float, float, float] | :class:`compas.geometry.Point`
            The second point.
        c : [float, float, float] | :class:`compas.geometry.Point`
            The second point.

        Returns
        -------
        :class:`compas.geometry.Plane`
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
        a = Point(*a)
        b = Point(*b)
        c = Point(*c)
        normal = Vector(*cross_vectors(b - a, c - a))
        return cls(a, normal)

    @classmethod
    def from_point_and_two_vectors(cls, point, u, v):  # type: (...) -> Plane
        """Construct a plane from a base point and two vectors.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The base point.
        u : [float, float, float] | :class:`compas.geometry.Vector`
            The first vector.
        v : [float, float, float] | :class:`compas.geometry.Vector`
            The second vector.

        Returns
        -------
        :class:`compas.geometry.Plane`
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
        normal = Vector(*cross_vectors(u, v))
        return cls(point, normal)

    @classmethod
    def from_abcd(cls, abcd):  # type: (...) -> Plane
        """Construct a plane from the plane equation coefficients.

        Parameters
        ----------
        abcd : [float, float, float, float]
            The equation coefficients.

        Returns
        -------
        :class:`compas.geometry.Plane`

        """
        a, b, c, d = abcd
        x = 1 / sqrt(a**2 + b**2 + c**2)
        normal = [a, b, c]
        point = [a * d * x, b * d * x, c * d * x]
        return cls(point, normal)

    @classmethod
    def worldXY(cls):  # type: (...) -> Plane
        """Construct the world XY plane.

        Returns
        -------
        :class:`compas.geometry.Plane`
            The world XY plane.

        """
        return cls([0, 0, 0], [0, 0, 1])

    @classmethod
    def worldYZ(cls):  # type: (...) -> Plane
        """Construct the world YZ plane.

        Returns
        -------
        :class:`compas.geometry.Plane`
            The world YZ plane.

        """
        return cls([0, 0, 0], [1, 0, 0])

    @classmethod
    def worldZX(cls):  # type: (...) -> Plane
        """Construct the world ZX plane.

        Returns
        -------
        :class:`compas.geometry.Plane`
            The world ZX plane.

        """
        return cls([0, 0, 0], [0, 1, 0])

    @classmethod
    def from_frame(cls, frame):  # type: (...) -> Plane
        """Construct a plane from a frame.

        Returns
        -------
        :class:`compas.geometry.Plane`
            A plane with the frame's `point` and the frame's `normal`.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> plane = Plane.from_frame(frame)
        >>> print(plane.point)
        Point(x=1.000, y=1.000, z=1.000)
        >>> print(plane.normal)  # doctest: +SKIP
        Vector(x=-0.299, y=-0.079, z=0.951))

        """
        return cls(frame.point, frame.normal)

    @classmethod
    def from_points(cls, points):  # type: (...) -> Plane
        """Construct a plane from a list of points.

        If the list contains more than three points, a plane is constructed that minimizes the distance to all points.

        Parameters
        ----------
        points : list of [float, float, float] | :class:`compas.geometry.Point`
            The points.

        Returns
        -------
        :class:`compas.geometry.Plane`
            The plane defined by the points.

        See Also
        --------
        :func:`compas.geometry.bestfit_plane`

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

    def transform(self, T):
        """Transform this plane.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None

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
        self.point.transform(T)
        self.normal.transform(T)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def is_parallel(self, other, tol=None):
        """Verify if this plane is parallel to another plane.

        Parameters
        ----------
        other : :class:`compas.geometry.Plane`
            The other plane.
        tol : float, optional
            Tolerance for the dot product of the normals.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        bool
            ``True`` if the planes are parallel.
            ``False`` otherwise.

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

    def is_perpendicular(self, other, tol=None):
        """Verify if this plane is perpendicular to another plane.

        Parameters
        ----------
        other : :class:`compas.geometry.Plane`
            The other plane.
        tol : float, optional
            Tolerance for the dot product of the normals.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        bool
            ``True`` if the planes are perpendicular.
            ``False`` otherwise.

        Examples
        --------
        >>> plane1 = Plane.worldXY()
        >>> plane2 = Plane([1.0, 1.0, 1.0], [0.0, 0.0, 1.0])
        >>> plane1.is_perpendicular(plane2)
        False

        """
        return TOL.is_zero(self.normal.dot(other.normal), tol)

    def contains_point(self, point, tol=None):
        """Verify if a given point lies in the plane.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The point.
        tol : float, optional
            Tolerance for the distance from the point to the plane.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        bool
            ``True`` if the point lies in the plane.
            ``False`` otherwise.

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
    def distance_to_point(self, point):
        """Compute the distance from a given point to the plane.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
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
    def closest_point(self, point):
        """Compute the closest point on the plane to a given point.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The point.

        Returns
        -------
        :class:`compas.geometry.Point`
            The closest point on the plane.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> point = plane.closest_point([1.0, 1.0, 1.0])
        >>> print(point)
        Point(x=1.000, y=1.000, z=0.000)

        """
        point = Point(*point)
        vector = self.point - point
        distance = self.normal.dot(vector)
        return point + self.normal.scaled(distance)

    # move to Point.proejcted_on_plane?
    # point.projected_on_plane(plane)
    # point.project_on_plane(plane)
    def projected_point(self, point, direction=None):
        """Returns the projection of a given point onto the plane.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The point.

        Returns
        -------
        :class:`compas.geometry.Point` | None
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
    def mirrored_point(self, point):
        """Returns the mirror image of a given point.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The point.

        Returns
        -------
        :class:`compas.geometry.Point`
            The mirrored point.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> point = plane.mirrored_point([1.0, 1.0, 1.0])
        >>> print(point)
        Point(x=1.000, y=1.000, z=-1.000)

        """
        point = Point(*point)
        vector = self.point - point
        distance = self.normal.dot(vector)
        return point + self.normal.scaled(2 * distance)

    def intersection_with_line(self, line, tol=None):
        """Compute the intersection of a plane and a line.

        Parameters
        ----------
        line : :class:`compas.geometry.Line`
            The line.
        tol : float, optional
            Tolerance for the dot product of the line vector and the plane normal.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        :class:`compas.geometry.Point` | None
            The intersection point, or ``None`` if the line is parallel to the plane.

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

    def intersection_with_plane(self, plane):
        """Compute the intersection of two planes.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The other plane.

        Returns
        -------
        :class:`compas.geometry.Line` | None
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

        return Line(point, point + direction)

    def intersections_with_curve(self, curve, tol=None):
        """Compute the intersection of a plane and a curve.

        Parameters
        ----------
        curve : :class:`compas.geometry.Curve`
            The curve.
        tol : float, optional
            Tolerance for the dot product of the line vector and the plane normal.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        list of :class:`compas.geometry.Point`
            The intersection points.

        """
        raise NotImplementedError

    def intersections_with_surface(self, surface):
        """Compute the intersection of a plane and a surface.

        Parameters
        ----------
        surface : :class:`compas.geometry.Surface`
            The surface.

        Returns
        -------
        list of :class:`compas.geometry.Point`
            The intersection points.

        """
        raise NotImplementedError

    def offset(self, distance):
        """Returns a new offset plane by a given distance.

        The plane normal is used as positive direction.

        Parameters
        ----------
        distance: float
            The offset distance.

        Returns
        -------
        :class:`compas.geometry.Plane`
            The offset plane.

        """
        return Plane(self.point + self.normal.scaled(distance), self.normal)
