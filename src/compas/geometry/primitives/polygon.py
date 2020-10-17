from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from compas.geometry import cross_vectors
from compas.geometry import centroid_polygon
from compas.geometry import area_polygon
from compas.geometry import is_coplanar
from compas.geometry import is_polygon_convex
from compas.geometry import transform_points

from compas.geometry.primitives import Primitive
from compas.geometry.primitives import Point
from compas.geometry.primitives import Vector
from compas.geometry.primitives import Line

from compas.utilities import pairwise


__all__ = ['Polygon']


class Polygon(Primitive):
    """An object representing an ordered collection of points in space connected
    by straight line segments forming a closed boundary around the interior space.

    A polygon has a closed boundary that separates its interior from the
    exterior. The boundary does not intersect itself, and is described by an
    ordered set of of points.

    Parameters
    ----------
    points : list of point
        An ordered list of points.

    Attributes
    ----------
    data : dict
        The data representation of the polygon.
    points : list of :class:`compas.geometry.Point`
        The polygon points.
    lines : list of :class:`compas.geometry.Line`, read-only
        The polygon segments.
    centroid : :class:`compas.geometry.Point`, read-only
        The centroid of the polygon surface.
    normal : :class:`compas.geometry.Vector`, read-only
        The normal vector of the polygon plane.
    length : float, read-only
        The length of the polygon boundary.
    area : float, read-only
        The area of the polygon surface.

    Notes
    -----
    All ``Polygon`` objects are considered closed. Therefore the first and
    last element in the list of points are not the same. The existence of the
    closing edge is implied.

    Polygons are not necessarily planar by construction; they can be warped.

    Examples
    --------
    >>> polygon = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    >>> polygon.centroid
    Point(0.500, 0.500, 0.000)
    >>> polygon.area
    1.0
    """

    __slots__ = ["_points", "_lines"]

    def __init__(self, points):
        super(Polygon, self).__init__()
        self._points = []
        self._lines = []
        self.points = points

    @property
    def data(self):
        """dict : The data dictionary that represents the polygon."""
        return {'points': [list(point) for point in self.points]}

    @data.setter
    def data(self, data):
        self.points = data['points']

    @property
    def points(self):
        """list of :class:`compas.geometry.Point` : The points of the polygon."""
        return self._points

    @points.setter
    def points(self, points):
        if points[-1] == points[0]:
            del points[-1]
        self._points = [Point(*xyz) for xyz in points]
        self._lines = None

    # consider caching below based on point setter

    @property
    def lines(self):
        """list of :class:`compas.geometry.Line` : The lines of the polygon."""
        if not self._lines:
            self._lines = [Line(a, b) for a, b in pairwise(self.points + self.points[:1])]
        return self._lines

    @property
    def length(self):
        """float : The length of the boundary."""
        return sum(line.length for line in self.lines)

    @property
    def centroid(self):
        """int : The centroid of the polygon."""
        point = centroid_polygon(self.points)
        return Point(*point)

    @property
    def normal(self):
        """:class:`compas.geometry.Vector` : The (average) normal of the polygon."""
        o = self.centroid
        points = self.points
        a2 = 0
        normals = []
        for i in range(-1, len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]
            u = [p1[_] - o[_] for _ in range(3)]
            v = [p2[_] - o[_] for _ in range(3)]
            w = cross_vectors(u, v)
            a2 += sum(w[_] ** 2 for _ in range(3)) ** 0.5
            normals.append(w)
        n = [sum(axis) / a2 for axis in zip(*normals)]
        n = Vector(* n)
        return n

    @property
    def area(self):
        """float: The area of the polygon."""
        return area_polygon(self.points)

    # ==========================================================================
    # customization
    # ==========================================================================

    def __repr__(self):
        return "Polygon({})".format(", ".join(["{}".format(point) for point in self.points]))

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value

    def __iter__(self):
        return iter(self.points)

    def __eq__(self, other):
        return all(a == b for a, b in zip(self, other))

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a polygon from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            The constructed polygon.

        Examples
        --------
        >>> polygon = Polygon.from_data({'points': [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 1.0]]})
        >>> polygon.points[0]
        Point(0.000, 0.000, 0.000)
        """
        return cls(data['points'])

    @classmethod
    def from_sides_and_radius_xy(cls, n, radius):
        """Construct a polygon from a number of sides and a radius.
        The resulting polygon is planar, equilateral and equiangular.

        Parameters
        ----------
        n : int
            The number of sides.
        radius : float
            The radius of the circle the polygon will be circumscribed to.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            The constructed polygon.

        Notes
        -----
        The first point of the polygon aligns with the Y-axis.
        The order of the polygon's points is counterclockwise.

        Examples
        --------
        >>> from compas.geometry import dot_vectors
        >>> from compas.geometry import subtract_vectors
        >>> pentagon = Polygon.from_sides_and_radius_xy(5, 1.0)
        >>> len(pentagon.lines) == 5
        True
        >>> len({round(line.length, 6) for line in pentagon.lines}) == 1
        True
        >>> dot_vectors(pentagon.normal, [0.0, 0.0, 1.0]) == 1
        True
        >>> centertofirst = subtract_vectors(pentagon.points[0], pentagon.centroid)
        >>> dot_vectors(centertofirst, [0.0, 1.0, 0.0]) == 1
        True
        """
        assert n >= 3, "Supplied number of sides must be at least 3!"
        points = []
        side = math.pi * 2 / n
        for i in range(n):
            point = [math.sin(side * (n - i)) * radius,
                     math.cos(side * (n - i)) * radius,
                     0.0]
            points.append(point)
        return cls(points)

    # ==========================================================================
    # methods
    # ==========================================================================

    def is_convex(self):
        """Determine if the polygon is convex.

        Returns
        -------
        bool
            True if the polygon is convex.
            False otherwise.

        Examples
        --------
        >>> polygon = Polygon([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.4, 0.4, 0.0], [0.0, 1.0, 0.0]])
        >>> polygon.is_convex()
        False
        """
        return is_polygon_convex(self.points)

    def is_planar(self):
        """Determine if the polygon is planar.

        Returns
        -------
        bool
            True if all points of the polygon lie in one plane.
            False otherwise.

        Examples
        --------
        >>> polygon = Polygon([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.1]])
        >>> polygon.is_planar()
        False
        """
        return is_coplanar(self.points)

    def transform(self, T):
        """Transform this polygon.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` or list of list
            The transformation.

        Examples
        --------
        >>> from math import radians
        >>> from compas.geometry import Rotation
        >>> polygon = Polygon.from_sides_and_radius_xy(4, 1.0)
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(45))
        >>> polygon.transform(R)
        >>> polygon.points[0]
        Point(-0.707, 0.707, 0.000)
        """
        for index, point in enumerate(transform_points(self.points, T)):
            self.points[index].x = point[0]
            self.points[index].y = point[1]
            self.points[index].z = point[2]

    def contains(self, point):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
