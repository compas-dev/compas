from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import sqrt

from compas.geometry import cross_vectors
from compas.geometry import bestfit_plane
from compas.geometry import Geometry
from .vector import Vector
from .point import Point


class Plane(Geometry):
    """A plane is defined by a base point and a normal vector.

    Parameters
    ----------
    point : [float, float, float] | :class:`~compas.geometry.Point`
        The base point of the plane.
    normal : [float, float, float] | :class:`~compas.geometry.Vector`
        The normal vector of the plane.

    Attributes
    ----------
    point : :class:`~compas.geometry.Plane`
        The base point of the plane.
    normal : :class:`~compas.geometry.Vector`
        The normal vector of the plane.
    d : float, read-only
        The *d* parameter of the linear equation describing the plane.
    abcd : list[float], read-only
        The coefficients of the plane equation.

    Examples
    --------
    >>> plane = Plane([0, 0, 0], [0, 0, 1])
    >>> plane.point
    Point(0.000, 0.000, 0.000)
    >>> plane.normal
    Vector(0.000, 0.000, 1.000)

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {
            "point": Point.JSONSCHEMA,
            "normal": Vector.JSONSCHEMA,
        },
        "required": ["point", "normal"],
    }

    def __init__(self, point, normal, **kwargs):
        super(Plane, self).__init__(**kwargs)
        self._point = None
        self._normal = None
        self.point = point
        self.normal = normal

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {"point": self.point, "normal": self.normal}

    @data.setter
    def data(self, data):
        self.point = data["point"]
        self.normal = data["normal"]

    @classmethod
    def from_data(cls, data):
        """Construct a plane from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Plane`
            The constructed plane.

        Examples
        --------
        >>> plane = Plane.from_data({'point': [0.0, 0.0, 0.0], 'normal': [0.0, 0.0, 1.0]})
        >>> plane.point
        Point(0.000, 0.000, 0.000)
        >>> plane.normal
        Vector(0.000, 0.000, 1.000)

        """
        return cls(data["point"], data["normal"])

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
    # Customization
    # ==========================================================================

    def __repr__(self):
        return "Plane({0!r}, {1!r})".format(self.point, self.normal)

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
    # Constructors
    # ==========================================================================

    @classmethod
    def from_three_points(cls, a, b, c):
        """Construct a plane from three points in three-dimensional space.

        Parameters
        ----------
        a : [float, float, float] | :class:`~compas.geometry.Point`
            The first point.
        b : [float, float, float] | :class:`~compas.geometry.Point`
            The second point.
        c : [float, float, float] | :class:`~compas.geometry.Point`
            The second point.

        Returns
        -------
        :class:`~compas.geometry.Plane`
            A plane with base point `a` and normal vector defined as the unitized
            cross product of the vectors `ab` and `ac`.

        Examples
        --------
        >>> plane = Plane.from_three_points([0.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 3.0, 0.0])
        >>> plane.point
        Point(0.000, 0.000, 0.000)
        >>> plane.normal
        Vector(0.000, 0.000, 1.000)

        """
        a = Point(*a)
        b = Point(*b)
        c = Point(*c)
        normal = Vector(*cross_vectors(b - a, c - a))
        return cls(a, normal)

    @classmethod
    def from_point_and_two_vectors(cls, point, u, v):
        """Construct a plane from a base point and two vectors.

        Parameters
        ----------
        point : [float, float, float] | :class:`~compas.geometry.Point`
            The base point.
        u : [float, float, float] | :class:`~compas.geometry.Vector`
            The first vector.
        v : [float, float, float] | :class:`~compas.geometry.Vector`
            The second vector.

        Returns
        -------
        :class:`~compas.geometry.Plane`
            A plane with base point `point` and normal vector defined as the unitized
            cross product of vectors `u` and `v`.

        Examples
        --------
        >>> plane = Plane.from_point_and_two_vectors([0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
        >>> plane.point
        Point(0.000, 0.000, 0.000)
        >>> plane.normal
        Vector(0.000, 0.000, 1.000)

        """
        normal = Vector(*cross_vectors(u, v))
        return cls(point, normal)

    @classmethod
    def from_abcd(cls, abcd):
        """Construct a plane from the plane equation coefficients.

        Parameters
        ----------
        abcd : [float, float, float, float]
            The equation coefficients.

        Returns
        -------
        :class:`~compas.geometry.Plane`

        """
        a, b, c, d = abcd
        x = 1 / sqrt(a**2 + b**2 + c**2)
        normal = [a, b, c]
        point = [a * d * x, b * d * x, c * d * x]
        return cls(point, normal)

    @classmethod
    def worldXY(cls):
        """Construct the world XY plane.

        Returns
        -------
        :class:`~compas.geometry.Plane`
            The world XY plane.

        """
        return cls([0, 0, 0], [0, 0, 1])

    @classmethod
    def from_frame(cls, frame):
        """Construct a plane from a frame.

        Returns
        -------
        :class:`~compas.geometry.Plane`
            A plane with the frame's `point` and the frame's `normal`.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> frame = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> Plane.from_frame(frame)
        Plane(Point(1.000, 1.000, 1.000), Vector(-0.299, -0.079, 0.951))

        """
        return cls(frame.point, frame.normal)

    @classmethod
    def from_points(cls, points):
        """Construct a plane from a list of points.

        If the list contains more than three points, a plane is constructed that minimizes the distance to all points.

        Parameters
        ----------
        points : list of [float, float, float] | :class:`~compas.geometry.Point`
            The points.

        Returns
        -------
        :class:`~compas.geometry.Plane`
            The plane defined by the points.

        See Also
        --------
        :func:`compas.geometry.bestfit_plane`

        Examples
        --------
        >>> points = [[0.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 3.0, 0.0]]
        >>> plane = Plane.from_points(points)
        >>> plane.point
        Point(0.000, 0.000, 0.000)
        >>> plane.normal
        Vector(0.000, 0.000, 1.000)

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
        T : :class:`~compas.geometry.Transformation` | list[list[float]]
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

    def is_parallel(self, other, tol=1e-06):
        """Verify if this plane is parallel to another plane.

        Parameters
        ----------
        other : :class:`~compas.geometry.Plane`
            The other plane.
        tol : float, optional
            Tolerance for the dot product of the normals.

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

        """
        return abs(self.normal.dot(other.normal)) == 1 - tol

    def is_perpendicular(self, other, tol=1e-06):
        """Verify if this plane is perpendicular to another plane.

        Parameters
        ----------
        other : :class:`~compas.geometry.Plane`
            The other plane.
        tol : float, optional
            Tolerance for the dot product of the normals.

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
        return abs(self.normal.dot(other.normal)) < tol

    def contains_point(self, point, tol=1e-06):
        """Verify if a given point lies in the plane.

        Parameters
        ----------
        point : [float, float, float] | :class:`~compas.geometry.Point`
            The point.
        tol : float, optional
            Tolerance for the distance from the point to the plane.

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
        return abs(self.normal.dot(vector)) < tol

    def distance_to_point(self, point):
        """Compute the distance from a given point to the plane.

        Parameters
        ----------
        point : [float, float, float] | :class:`~compas.geometry.Point`
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

    def closest_point(self, point):
        """Compute the closest point on the plane to a given point.

        Parameters
        ----------
        point : [float, float, float] | :class:`~compas.geometry.Point`
            The point.

        Returns
        -------
        :class:`~compas.geometry.Point`
            The closest point on the plane.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> plane.closest_point([1.0, 1.0, 1.0])
        Point(1.000, 1.000, 0.000)

        """
        vector = self.point - point
        distance = self.normal.dot(vector)
        return point + self.normal.scaled(distance)

    def projected_point(self, point, direction=None):
        """Returns the projection of a given point onto the plane.

        Parameters
        ----------
        point : [float, float, float] | :class:`~compas.geometry.Point`
            The point.

        Returns
        -------
        :class:`~compas.geometry.Point` | None
            The projected point, or None if a direction is given and it is parallel to the plane.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> plane.projected_point([1.0, 1.0, 1.0])
        Point(1.000, 1.000, 0.000)

        """
        if not direction:
            return self.closest_point(point)

        from compas.geometry import Line

        line = Line.from_point_and_vector(point, direction)
        intersection = self.intersection_with_line(line)
        return intersection

    def mirrored_point(self, point):
        """Returns the mirror image of a given point.

        Parameters
        ----------
        point : [float, float, float] | :class:`~compas.geometry.Point`
            The point.

        Returns
        -------
        :class:`~compas.geometry.Point`
            The mirrored point.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> plane.mirrored_point([1.0, 1.0, 1.0])
        Point(1.000, 1.000, -1.000)

        """
        vector = self.point - point
        distance = self.normal.dot(vector)
        return point + self.normal.scaled(2 * distance)

    def intersection_with_line(self, line, tol=1e-06):
        """Compute the intersection of a plane and a line.

        Parameters
        ----------
        line : :class:`~compas.geometry.Line`
            The line.
        tol : float, optional
            Tolerance for the dot product of the line vector and the plane normal.

        Returns
        -------
        :class:`~compas.geometry.Point` | None
            The intersection point, or ``None`` if the line is parallel to the plane.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> line = Line(Point(0, 0, 1), Vector(1, 1, 1))
        >>> plane.intersection_with_line(line)
        Point(0.000, 0.000, 0.000)

        """
        # The line is parallel to the plane
        if abs(self.normal.dot(line.vector)) < tol:
            return None

        t = (self.point - line.start).dot(self.normal) / line.vector.dot(self.normal)
        return line.point_at(t)

    def intersection_with_plane(self, plane):
        """Compute the intersection of two planes.

        Parameters
        ----------
        plane : :class:`~compas.geometry.Plane`
            The other plane.

        Returns
        -------
        :class:`~compas.geometry.Line` | None
            The intersection line, or None if the planes are parallel or coincident.

        Examples
        --------
        >>> plane1 = Plane.worldXY()
        >>> plane2 = Plane([1.0, 1.0, 1.0], [0.0, 0.0, 1.0])
        >>> plane1.intersection(plane2)
        Line(Point(0.000, 0.000, 0.000), Vector(0.000, 0.000, 1.000))

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

    def intersections_with_curve(self, curve, tol=1e-06):
        """Compute the intersection of a plane and a curve.

        Parameters
        ----------
        curve : :class:`~compas.geometry.Curve`
            The curve.
        tol : float, optional
            Tolerance for the dot product of the line vector and the plane normal.

        Returns
        -------
        list of :class:`~compas.geometry.Point`
            The intersection points.

        Examples
        --------
        >>> plane = Plane.worldXY()
        >>> line = Line(Point(0, 0, 1), Vector(1, 1, 1))
        >>> plane.intersection_with_curve(line)
        [Point(0.000, 0.000, 0.000)]

        """
        pass

    def intersections_with_surface(self, surface):
        pass

    def offset(self, distance):
        """Returns a new offset plane by a given distance.

        The plane normal is used as positive direction.

        Parameters
        ----------
        distance: float
            The offset distance.

        Returns
        -------
        :class:`~compas.geometry.Plane`
            The offset plane.

        """
        return Plane(self.point + self.normal.scaled(distance), self.normal)
