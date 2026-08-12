from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import centroid_points
from compas.geometry import distance_point_line
from compas.geometry import distance_point_plane
from compas.geometry import distance_point_point
from compas.geometry import is_point_behind_plane
from compas.geometry import is_point_in_circle
from compas.geometry import is_point_in_convex_polygon_xy
from compas.geometry import is_point_in_polygon_xy
from compas.geometry import is_point_in_triangle
from compas.geometry import is_point_on_polyline
from compas.geometry import is_point_on_segment
from compas.geometry import normal_polygon
from compas.geometry import transform_points
from compas.tolerance import TOL

from .geometry import Geometry
from .vector import Vector


class Point(Geometry):
    """A point is defined by XYZ coordinates.

    Parameters
    ----------
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float, optional
        The Z coordinate of the point.
    name : str, optional
        The name of the point.

    Attributes
    ----------
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float
        The Z coordinate of the point.

    Notes
    -----
    A `Point` object supports direct access to its xyz coordinates through
    the dot notation, as well list-style access using indices. Indexed
    access is implemented such that the `Point` behaves like a circular
    list [1]_.

    References
    ----------
    .. [1] Stack Overflow. *Pythonic Circular List*.
           Available at: https://stackoverflow.com/questions/8951020/pythonic-circular-list.

    Examples
    --------
    >>> p1 = Point(1, 2, 3)
    >>> p2 = Point(4, 5, 6)

    The XYZ coordinates of point objects can be accessed as object attributes or by trating the points as lists.

    >>> p1.x
    1.0
    >>> p1.y
    2.0
    >>> p1.z
    3.0
    >>> p1[0]
    1.0
    >>> p1[1]
    2.0
    >>> p1[2]
    3.0

    Point objects support basic arithmetic operations.

    >>> result = p1 + p2
    >>> print(result)
    Point(x=5.000, y=7.000, z=9.000)

    >>> result = p1 * 2
    >>> print(result)
    Point(x=2.000, y=4.000, z=6.000)

    >>> result = p1**2
    >>> print(result)
    Point(x=1.000, y=4.000, z=9.000)

    >>> print(p1)
    Point(x=1.000, y=2.000, z=3.000)

    Points and lists can be used interchangeably.

    >>> result = p1 + [4, 5, 6]
    >>> print(result)
    Point(x=5.000, y=7.000, z=9.000)

    Arithmetic operations can also be applied to modify a point object in-place.

    >>> p1 += p2
    >>> p1 *= 2
    >>> p1 **= 2
    >>> print(p1)
    Point(x=100.000, y=196.000, z=324.000)

    """

    DATASCHEMA = {
        "type": "array",
        "minItems": 3,
        "maxItems": 3,
        "items": {"type": "number"},
    }

    @property
    def __data__(self):
        return list(self)

    @classmethod
    def __from_data__(cls, data):
        return cls(*data)

    def __init__(self, x, y, z=0.0, name=None):
        super(Point, self).__init__(name=name)
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "{0}(x={1}, y={2}, z={3})".format(
            type(self).__name__,
            self.x,
            self.y,
            self.z,
        )

    def __str__(self):
        return "{0}(x={1}, y={2}, z={3})".format(
            type(self).__name__,
            TOL.format_number(self.x),
            TOL.format_number(self.y),
            TOL.format_number(self.z),
        )

    def __len__(self):
        return 3

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]
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

    def __eq__(self, other):
        return TOL.is_allclose(self, other)

    def __add__(self, other):
        return Point(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other):
        x = self.x - other[0]
        y = self.y - other[1]
        z = self.z - other[2]
        return Vector(x, y, z)

    def __mul__(self, n):
        return Point(n * self.x, n * self.y, n * self.z)

    def __truediv__(self, n):
        return Point(self.x / n, self.y / n, self.z / n)

    def __pow__(self, n):
        return Point(self.x**n, self.y**n, self.z**n)

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

    def __itruediv__(self, n):
        self.x /= n
        self.y /= n
        self.z /= n
        return self

    def __ipow__(self, n):
        self.x **= n
        self.y **= n
        self.z **= n
        return self

    # ==========================================================================
    # Properties
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
    # Methods
    # ==========================================================================

    def distance_to_point(self, point):
        """Compute the distance to another point.

        Parameters
        ----------
        point : [float, float, float] | :class:`compas.geometry.Point`
            The other point.

        Returns
        -------
        float
            The distance.

        Examples
        --------
        >>> a = Point(0.0, 0.0, 0.0)
        >>> b = Point(1.0, 0.0, 0.0)
        >>> a.distance_to_point(b)
        1.0

        """
        return distance_point_point(self, point)

    def distance_to_line(self, line):
        """Compute the distance to a line.

        Parameters
        ----------
        line : [point, point] | :class:`compas.geometry.Line`
            The line.

        Returns
        -------
        float
            The distance.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> point = Point(0.0, 0.0, 0.0)
        >>> line = Line(Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0))
        >>> point.distance_to_line(line)
        1.0

        """
        return distance_point_line(self, line)

    def distance_to_plane(self, plane):
        """Compute the distance to a plane.

        Parameters
        ----------
        plane : [point, vector] | :class:`compas.geometry.Plane`
            The plane.

        Returns
        -------
        float
            The distance.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Vector
        >>> point = Point(0.0, 0.0, 0.0)
        >>> plane = Plane(Point(1.0, 0.0, 0.0), Vector(1.0, 0.0, 0.0))
        >>> point.distance_to_plane(plane)
        1.0

        """
        return distance_point_plane(self, plane)

    # ==========================================================================
    # 2D predicates
    # ==========================================================================

    def in_polygon(self, polygon):
        """Determine if the point lies inside the given polygon.

        For this test, the point and polygon are assumed to lie in the XY plane.
        The Z coordinates of the point and of the points of the polygon are ignored.
        If the point and/or polygon do not lie in the XY plane, the result of this test is meaningless.
        It is up to the user to apply the necessary transformations beforehand.

        The polygon can be convex or concave.

        Parameters
        ----------
        polygon : sequence[point] | :class:`compas.geometry.Polygon`
            The polygon.

        Returns
        -------
        bool
            True, if the point lies in the polygon.
            False, otherwise.

        See Also
        --------
        :meth:`in_convex_polygon`

        Examples
        --------
        >>> from compas.geometry import Polygon
        >>> poly = Polygon([Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0), Point(0.0, 1.0, 0.0)])
        >>> point = Point(0.5, 0.5, 0.0)
        >>> point.in_polygon(poly)
        True

        """
        return is_point_in_polygon_xy(self, polygon)

    def in_convex_polygon(self, polygon):
        """Determine if the point lies inside the given convex polygon.

        For this test, the point and polygon are assumed to lie in the XY plane.
        The Z coordinates of the point and of the points of the polygon are ignored.
        If the point and/or polygon do not lie in the XY plane, the result of this test is meaningless.
        It is up to the user to apply the necessary transformations beforehand.

        The polygon must be convex.
        However, the method will not check that this is indeed the case.

        Parameters
        ----------
        polygon : sequence[point] | :class:`compas.geometry.Polygon`
            The polygon.

        Returns
        -------
        bool
            True, if the point lies in the polygon.
            False, otherwise.

        See Also
        --------
        :meth:`in_polygon`

        Examples
        --------
        >>> from compas.geometry import Polygon
        >>> poly = Polygon([Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0), Point(0.0, 1.0, 0.0)])
        >>> point = Point(0.5, 0.5, 0.0)
        >>> point.in_convex_polygon(poly)
        True

        """
        return is_point_in_convex_polygon_xy(self, polygon)

    # ==========================================================================
    # 3D predicates
    # ==========================================================================

    def on_line(self, line, tol=None):
        """Determine if the point lies on the given line.

        Parameters
        ----------
        line : [point, point] | :class:`compas.geometry.Line`
            The line.
        tol : float, optional
            A tolerance value for the distance between the point and the line.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        bool
            True, if the point lies on the line.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> line = Line(Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0))
        >>> point = line.point_at(1.5)
        >>> point.on_line(line)
        True

        """
        return TOL.is_zero(self.distance_to_line(line), tol)

    def on_segment(self, segment, tol=None):
        """Determine if the point lies on the given segment.

        Parameters
        ----------
        segment : [point, point] | :class:`compas.geometry.Line`
            The segment.
        tol : float, optional
            A tolerance value for the distance between the point and the segment.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        bool
            True, if the point lies on the segment.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Line
        >>> line = Line(Point(1.0, 0.0, 0.0), Point(1.0, 1.0, 0.0))
        >>> point = line.point_at(1.5)
        >>> point.on_segment(line)
        False

        """
        return is_point_on_segment(self, segment, tol=tol)

    def on_polyline(self, polyline):
        """Determine if the point lies on the given polyline.

        Parameters
        ----------
        polyline : sequence[point] | :class:`compas.geometry.Polyline`
            The polyline.

        Returns
        -------
        bool
            True, if the point lies on the polyline.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Polyline
        >>> poly = Polyline([Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0), Point(2.0, 0.0, 0.0)])
        >>> point = poly.point_at(0.5)
        >>> point.on_polyline(poly)
        True

        """
        return is_point_on_polyline(self, polyline)

    def on_plane(self, plane, tol=None):
        """Determine if the point lies on the given plane.

        Parameters
        ----------
        plane : :class:`compas.geometry.Plane`
            The plane.
        tol : float, optional
            A tolerance value for the distance between the point and the plane.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        bool
            True, if the point lies on the plane.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Vector
        >>> plane = Plane(Point(0.0, 0.0, 0.0), Vector(0.0, 0.0, 1.0))
        >>> point = Point(0.5, 0.5, 0.0)
        >>> point.on_plane(plane)
        True

        """
        return TOL.is_zero(self.distance_to_plane(plane), tol)

    def on_circle(self, circle, tol=None):
        """Determine if the point lies on the given circle.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`
            The circle.
        tol : float, optional
            A tolerance value for the distance between the point and the circle.
            Default is :attr:`TOL.absolute`.

        Returns
        -------
        bool
            True, if the point lies on the circle.
            False, otherwise.

        """
        if not self.on_plane(circle.plane, tol):
            return False
        return TOL.is_close(self.distance_to_point(circle.center), circle.radius, rtol=0, atol=tol)

    def on_curve(self, curve, tol=None):
        """Determine if the point lies on the given curve.

        Parameters
        ----------
        curve : :class:`compas.geometry.Curve`
            The curve.
        tol : float, optional
            A tolerance value for the distance between the point and the curve.

        Returns
        -------
        bool
            True, if the point lies on the curve.
            False, otherwise.

        """
        return TOL.is_zero(self.distance_to_point(curve.closest_point(self)), tol)

    def in_triangle(self, triangle):
        """Determine if the point lies inside the given triangle.

        Parameters
        ----------
        triangle : [point, point, point] | :class:`compas.geometry.Polygon`
            The triangle.

        Returns
        -------
        bool
            True, if the point lies in the triangle.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Polygon
        >>> tri = Polygon([Point(0.0, 0.0, 0.0), Point(1.0, 0.0, 0.0), Point(0.5, 1.0, 0.0)])
        >>> point = Point(0.5, 0.5, 0.0)
        >>> point.in_triangle(tri)
        True

        """
        return is_point_in_triangle(self, triangle)

    def in_circle(self, circle):
        """Determine if the point lies inside the given circle.

        Parameters
        ----------
        circle : :class:`compas.geometry.Circle`
            The circle.

        Returns
        -------
        bool
            True, if the point lies inside the circle.
            False, otherwise.

        Examples
        --------
        >>> from compas.geometry import Vector
        >>> from compas.geometry import Plane
        >>> from compas.geometry import Circle
        >>> circle = Circle(1.0)
        >>> point = Point(0.5, 0.0, 0.0)
        >>> point.in_circle(circle)
        True

        """
        return is_point_in_circle(self, (circle.plane, circle.radius))

    def in_polyhedron(self, polyhedron):
        """Determine if the point lies inside the given polyhedron.

        This method verifies that the point lies behind the planes of all the faces of the polyhedron.
        Therefore, if the polyhedron is not convex, or if the faces are not planar, the result of this test is meaningless.
        Convexity and planarity are not checked.

        Parameters
        ----------
        polyhedron : [vertices, faces] | :class:`compas.geometry.Polyhedron`
            The polyhedron.

        Returns
        -------
        bool
            True, if the point lies on the polyline.
            False, otherwise.

        """
        vertices, faces = polyhedron
        polygons = [[vertices[index] for index in face] for face in faces]
        planes = [[centroid_points(polygon), normal_polygon(polygon)] for polygon in polygons]
        return all(is_point_behind_plane(self, plane) for plane in planes)

    # ==========================================================================
    # Transformations
    # ==========================================================================

    def transform(self, T):
        """Transform this point.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation matrix.

        Examples
        --------
        >>> from compas.geometry import Translation
        >>> point = Point(0.0, 0.0, 0.0)
        >>> T = Translation.from_vector([1.0, 1.0, 1.0])
        >>> point.transform(T)
        >>> point.x == 1.0
        True

        """
        point = transform_points([self], T)[0]
        self.x = point[0]
        self.y = point[1]
        self.z = point[2]
