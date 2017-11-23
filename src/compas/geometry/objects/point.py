from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry.objects import Vector

from compas.geometry import distance_point_point
from compas.geometry import distance_point_line
from compas.geometry import distance_point_plane
from compas.geometry import project_point_plane
from compas.geometry import project_point_line
from compas.geometry import is_point_in_triangle
from compas.geometry import transform


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'GNU - General Public License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['Point']


class Point(object):
    """A three-dimensional location in space.

    Parameters
    ----------
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float, optional
        The Z coordinate of the point.
        Default is ``0.0``.

    Attributes
    ----------
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float
        The Z coordinate of the point.

    Examples
    --------
    >>> p1 = Point([1, 2, 3])
    >>> p2 = Point([4, 5, 6])

    >>> p1.x
    1.0
    >>> p1[0]
    1.0
    >>> p1[5]
    1.0
    >>> p1[-3]
    1.0
    >>> p1[-6]
    1.0

    >>> p1 + p2
    [5.0, 7.0, 9.0]
    >>> p1 + [4, 5, 6]
    [5.0, 7.0, 9.0]
    >>> p1 * 2
    [2.0, 4.0, 6.0]
    >>> p1 ** 2
    [1.0, 4.0, 9.0]
    >>> p1
    [1.0, 2.0, 3.0]

    >>> p1 += p2
    >>> p1 *= 2
    >>> p1 **= 2
    >>> p1
    [100.0, 196.0, 324.0]

    Note
    ----
    A ``Point`` object supports direct access to its xyz coordinates through
    the dot notation, as well list-style access using indices. Indexed
    access is implemented such that the ``Point`` behaves like a circular
    list.

    References
    ----------
    * http://stackoverflow.com/questions/8951020/pythonic-circular-list

    """

    __slots__ = ['_x', '_y', '_z', 'precision']

    def __init__(self, x, y, z=0.0):
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self.x = x
        self.y = y
        self.z = z
        self.precision = '3f'

    # ==========================================================================
    # factory
    # ==========================================================================

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    # ==========================================================================
    # representation
    # ==========================================================================

    def __repr__(self):
        return 'Point({0:.{3}}, {1:.{3}}, {2:.{3}})'.format(self.x, self.y, self.z, self.precision)

    def __len__(self):
        return 3

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        i = key % 3
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z
        raise KeyError

    def __setitem__(self, key, value):
        i = key % 3
        if i == 0:
            self.x = value
            return
        if i == 1:
            self.y = value
            return
        if i == 2:
            self.z = value
            return
        raise KeyError

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other):
        """Is this point equal to the other point? Tow points are considered
        equal if their XYZ coordinates are identical.

        Note:
            Perhaps it makes sense to add a *precision* attribute to the point
            class. This would allow comparisons to be made up to a certain
            tolerance.

        Parameters:
            other (sequence, Point): The point to compare.
        """
        return self.x == other[0] and self.y == other[1] and self.z == other[2]

    # ==========================================================================
    # operators
    # ==========================================================================

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        """Create a vector from other to self.

        Parameters:
            other (sequence, Point): The point to subtract.

        Returns:
            Vector: A vector from other to self
        """
        x = self.x - other[0]
        y = self.y - other[1]
        z = self.z - other[2]
        return Vector(x, y, z)

    def __mul__(self, n):
        return Point(n * self.x, n * self.y, n * self.z)

    def __pow__(self, n):
        return Point(self.x ** n, self.y ** n, self.z ** n)

    # ==========================================================================
    # in-place operators
    # ==========================================================================

    def __iadd__(self, other):
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]
        return self

    def __isub__(self, other):
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]
        return self

    def __imul__(self, n):
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    def __ipow__(self, n):
        self.x **= n
        self.y **= n
        self.z **= n
        return self

    # ==========================================================================
    # methods: other
    # ==========================================================================

    def distance_to_point(self, point):
        return distance_point_point(self, point)

    def distance_to_line(self, line):
        return distance_point_line(self, line)

    def distance_to_plane(self, plane):
        return distance_point_plane(self, plane)

    def in_triangle(self, triangle):
        return is_point_in_triangle(self, triangle)

    def in_polygon(self, polygon):
        raise NotImplementedError

    def in_polyhedron(self, polyhedron):
        raise NotImplementedError

    # ==========================================================================
    # tranformations
    # ==========================================================================

    def transform(self, matrix):
        points = transform([self, ], matrix)
        self.x = points[0][0]
        self.x = points[0][0]
        self.x = points[0][0]

    def translate(self, vector):
        self.x += vector.x
        self.y += vector.y
        self.z += vector.z
        return self

    def project_to_line(self, line):
        pass

    def project_to_plane(self, plane):
        plane = (plane.point, plane.normal)
        return project_point_plane(self, plane)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    from compas.geometry import Point
    from compas.geometry import Vector
    from compas.geometry import Plane
    from compas.geometry import Line
    from compas.geometry import Polygon

    from compas.geometry import projection_matrix

    point    = Point(0.0, 0.0, 0.0)
    normal   = Vector(0.0, 0.0, 1.0)
    plane    = Plane.from_point_and_normal(point, normal)
    line     = Line([0.0, 0.0, 0.0], [1.0, 0.0, 0.0])
    triangle = Polygon([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0]])
    polygon  = Polygon([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]])

    p = Point(1.0, 1.0, 1.0)

    print(repr(p))

    print(p.distance_to_point(point))
    print(p.distance_to_line(line))
    print(p.distance_to_plane(plane))
    print(p.in_triangle(triangle))

    # print(p.in_polygon(polygon))
    # print(p.in_polyhedron())

    # p.transform()
    # p.translate()
    # p.project_to_line()
    # p.project_to_plane()

