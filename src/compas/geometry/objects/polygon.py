from compas.geometry.objects import Point
from compas.geometry.objects import Vector
from compas.geometry.objects import Line

from compas.geometry import area_polygon
from compas.geometry import cross_vectors
from compas.geometry import centroid_points
from compas.geometry import center_of_mass_polygon
from compas.geometry import is_coplanar
from compas.geometry import is_polygon_convex


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Polygon']


class Polygon(object):
    """An object representing ...

    A polygon has a closed boundary that separates its interior from the
    exterior. The boundary does not intersect itself, and is described by an
    ordered set of of points.

    Note:
        All ``Polygon`` objects are considered closed. Therefore the first and
        last element in the list of points are not the same. The existence of the
        closing edge is implied.

    Parameters:
        points (sequence): A sequence of XYZ coordinates.

    Attributes:
        points (list): A list of ``Point`` objects.
        lines (list): A list of ``Line`` objects.
        length (float): The total length of the boundary.
        centroid (Point): A ``Point`` object at the location of the centroid.
        area (float): The size of the area enclosed by the boundary.

    Examples:
        >>> polygon = Polygon([[0,0,0], [1,0,0], [1,1,0], [0,1,0]])
        >>> polygon.centroid
        [0.5, 0.5, 0.0]
        >>> polygon.area
        1.0

    """
    def __init__(self, points):
        self._points = []
        self._lines = []
        self._p = 0
        self._l = 0
        self.points = points

    # ==========================================================================
    # factory
    # ==========================================================================

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def points(self):
        """The points of the polygon.

        Parameters:
            points (sequence): A sequence of XYZ coordinates.

        Returns:
            list: A list of ``Point`` objects.
        """
        return self._points

    @points.setter
    def points(self, points):
        if points[-1] == points[0]:
            del points[-1]
        self._points = [Point(*xyz) for xyz in points]
        self._lines  = [Line(self.points[i], self.points[i + 1]) for i in range(-1, len(points) - 1)]

    @property
    def lines(self):
        """The lines of the polyline.

        Parameters:
            None

        Returns:
            list: A list of ``Line`` objects.
        """
        return self._lines

    @property
    def p(self):
        """The number of points."""
        return self._p

    @property
    def l(self):
        """The number of lines."""
        return self._l

    @property
    def length(self):
        """The length of the boundary."""
        return sum([line.length for line in self.lines])

    @property
    def centroid(self):
        """The centroid of the polygon."""
        return Point(* centroid_points(self.points))

    @property
    def normal(self):
        """The (average) normal of the polygon."""
        o = self.center
        points = self.points
        a2 = 0
        normals = []
        for i in range(-1, len(points) - 1):
            p1  = points[i]
            p2  = points[i + 1]
            u   = [p1[_] - o[_] for _ in range(3)]
            v   = [p2[_] - o[_] for _ in range(3)]
            w   = cross_vectors(u, v)
            a2 += sum(w[_] ** 2 for _ in range(3)) ** 0.5
            normals.append(w)
        n = [sum(axis) / a2 for axis in zip(*normals)]
        n = Vector(* n)
        return n

    @property
    def tangent(self):
        """The (average) tangent plane."""
        o = self.center
        a, b, c = self.normal
        d = - (a * o.x + b * o.y + c * o.z)
        return a, b, c, d

    @property
    def frame(self):
        """The local coordinate frame."""
        o  = self.center
        w  = self.normal
        p  = self.points[0]
        u  = Vector.from_start_end(o, p)
        u.unitize()
        v = Vector.cross(w, u)
        return o, u, v, w

    @property
    def center(self):
        """The center (of mass) of the polygon."""
        return Point(* center_of_mass_polygon(self.points))

    @property
    def area(self):
        """The area of the polygon.

        The area is computed as the sum of the areas of the triangles formed
        by each of the lines of the boundary and the centroid.
        """
        return area_polygon(self.points)

    @property
    def is_convex(self):
        return is_polygon_convex(self.points)

    @property
    def is_coplanar(self):
        return is_coplanar(self.points)

    # ==========================================================================
    # representation
    # ==========================================================================

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        try:
            return self.points[key]
        except IndexError:
            raise KeyError

    def __setitem__(self, key, value):
        try:
            self.points[key] = value
        except IndexError:
            raise KeyError

    def __iter__(self):
        return iter(self.points)

    # ==========================================================================
    # comparison
    # ==========================================================================

    # ==========================================================================
    # operators
    # ==========================================================================

    # ==========================================================================
    # inplace operators
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    # ==========================================================================
    # transformations
    # ==========================================================================


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == '__main__':

    polygon = Polygon([[1, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0]])

    print(polygon.centroid)
    print(polygon.center)
    print(polygon.area)
    print(polygon.length)
    print(polygon.normal)
    print(polygon.frame)

    print(polygon.is_convex)
    print(polygon.is_coplanar)
