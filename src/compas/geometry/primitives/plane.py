from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt
from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Vector
from compas.geometry.primitives import Point


class Plane(Primitive):
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

    __slots__ = ["_point", "_normal"]

    def __init__(self, point, normal, **kwargs):
        super(Plane, self).__init__(**kwargs)
        self._point = None
        self._normal = None
        self.point = point
        self.normal = normal

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        from schema import Schema

        return Schema(
            {
                "point": Point.DATASCHEMA.fget(None),
                "normal": Vector.DATASCHEMA.fget(None),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "plane"

    @property
    def data(self):
        """dict : The data dictionary that represents the plane."""
        return {"point": self.point.data, "normal": self.normal.data}

    @data.setter
    def data(self, data):
        self.point = Point.from_data(data["point"])
        self.normal = Vector.from_data(data["normal"])

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
        return cls(Point.from_data(data["point"]), Vector.from_data(data["normal"]))

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, point):
        self._point = Point(*point)

    @property
    def normal(self):
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
    # customization
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
    # constructors
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
        normal = Vector.cross(b - a, c - a)
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
        >>> plane = Plane.from_three_points([0.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 3.0, 0.0])
        >>> plane.point
        Point(0.000, 0.000, 0.000)
        >>> plane.normal
        Vector(0.000, 0.000, 1.000)

        """
        normal = Vector.cross(u, v)
        return cls(point, normal)

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

    # ==========================================================================
    # methods
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

    def offset(self, distance):
        """Returns a new offset plane by a given distance.
        Plane normal is used as positive direction.

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
