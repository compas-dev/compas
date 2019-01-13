from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.basic import cross_vectors

from compas.geometry.average import centroid_points
from compas.geometry.average import centroid_polygon

from compas.geometry.size import area_polygon

from compas.geometry.queries import is_coplanar
from compas.geometry.queries import is_polygon_convex

from compas.geometry._primitives import Point
from compas.geometry._primitives import Vector
from compas.geometry._primitives import Line


__all__ = ['Polygon']


class Polygon(object):
    """An object representing an ordered collection of points in space connected
    by straight line segments forming a closed boundary around the interior space.

    A polygon has a closed boundary that separates its interior from the
    exterior. The boundary does not intersect itself, and is described by an
    ordered set of of points.

    Parameters
    ----------
    points : list of point
        An ordered list of points.

    Examples
    --------
    >>> polygon = Polygon([[0,0,0], [1,0,0], [1,1,0], [0,1,0]])
    >>> polygon.centroid
    [0.5, 0.5, 0.0]
    >>> polygon.area
    1.0

    Notes
    -----
    All ``Polygon`` objects are considered closed. Therefore the first and
    last element in the list of points are not the same. The existence of the
    closing edge is implied.

    Polygons are not necessarily planar by construction; they can be warped.

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
        """list of Point: The points of the polygon."""
        return self._points

    @points.setter
    def points(self, points):
        if points[-1] == points[0]:
            del points[-1]
        self._points = [Point(*xyz) for xyz in points]
        self._lines  = [Line(self.points[i], self.points[i + 1]) for i in range(-1, len(points) - 1)]

    @property
    def lines(self):
        """list of Line: The lines of the polyline."""
        return self._lines

    @property
    def p(self):
        """int: The number of points."""
        return self._p

    @property
    def l(self):
        """int: The number of lines."""
        return self._l

    @property
    def length(self):
        """float: The length of the boundary."""
        return sum([line.length for line in self.lines])

    @property
    def centroid(self):
        """int: The centroid of the polygon."""
        return Point(* centroid_points(self.points))

    @property
    def center(self):
        """Point: The center (of mass) of the polygon."""
        return Point(* centroid_polygon(self.points))

    @property
    def normal(self):
        """Vector: The (average) normal of the polygon."""
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

    # @property
    # def tangent(self):
    #     """The (average) tangent plane."""
    #     o = self.center
    #     a, b, c = self.normal
    #     d = - (a * o.x + b * o.y + c * o.z)
    #     return a, b, c, d

    # @property
    # def frame(self):
    #     """The local coordinate frame."""
    #     o  = self.center
    #     w  = self.normal
    #     p  = self.points[0]
    #     u  = Vector.from_start_end(o, p)
    #     u.unitize()
    #     v = Vector.cross(w, u)

    #     a, b, c = self.normal
    #     u = 1.0, 0.0, - a / c
    #     v = 0.0, 1.0, - b / c
    #     u, v = orthonormalize_vectors([u, v])
    #     u = Vector(*u)
    #     v = Vector(*v)
    #     u.unitize()
    #     v.unitize()
    #     return self.point, u, v

    #     return o, u, v, w

    @property
    def area(self):
        """float: The area of the polygon."""
        return area_polygon(self.points)

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Polygon({0})'.format(", ".join(map(lambda point: format(point, ""), self.points)))

    def __len__(self):
        return self.p

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = value

    def __iter__(self):
        return iter(self.points)

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other):
        raise NotImplementedError

    # ==========================================================================
    # operators
    # ==========================================================================

    # ==========================================================================
    # inplace operators
    # ==========================================================================

    # ==========================================================================
    # helpers
    # ==========================================================================

    def copy(self):
        """Make a copy of this ``Polygon``.

        Returns
        -------
        Polygon
            The copy.

        """
        cls = type(self)
        return cls([point.copy() for point in self.points])

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

        """
        return is_polygon_convex(self.points)

    def is_planar(self):
        """Determine if the polygon is planar.

        Returns
        -------
        bool
            True if all points of the polygon lie in one plane.
            False otherwise.

        """
        return is_coplanar(self.points)

    # ==========================================================================
    # transformations
    # ==========================================================================

    def transform(self, matrix):
        """Transform this ``Polygon`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        """
        for index, point in enumerate(transform_points(self.points, matrix)):
            self.points[index].x = point[0]
            self.points[index].y = point[1]
            self.points[index].z = point[2]

    def transformed(self, matrix):
        """Return a transformed copy of this ``Polygon`` using a given transformation matrix.

        Parameters
        ----------
        matrix : list of list
            The transformation matrix.

        Returns
        -------
        Polygon
            The transformed copy.

        """
        polygon = self.copy()
        polygon.transform(matrix)
        return polygon


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.plotters import Plotter

    polygon = Polygon([[1, 1, 0], [0, 1, 0], [0, 0, 0], [1, 0, 0]])

    for point in polygon.points:
        print(point[0:2])

    plotter = Plotter(figsize=(10, 7))
    plotter.draw_polygons([{'points': polygon.points}])
    plotter.show()
