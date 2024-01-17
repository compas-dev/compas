from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from compas.utilities import pairwise
from compas.geometry import allclose
from compas.geometry import area_polygon
from compas.geometry import centroid_polygon
from compas.geometry import is_coplanar
from compas.geometry import is_polygon_convex
from compas.geometry import transform_points
from compas.geometry import earclip_polygon
from compas.geometry import bounding_box
from compas.geometry import Geometry
from compas.geometry import Transformation
from compas.geometry import Point
from compas.geometry import Plane
from compas.geometry import Frame
from compas.geometry import Line


class Polygon(Geometry):
    """A polygon is a geometric object defined by a sequence of points forming a closed loop.

    A polygon is defined by a sequence of points connected by line segments
    forming a closed boundary that separates its interior from the exterior.

    In the sequence of points, the first and last element are not the same.
    The existence of the closing edge is implied.
    The boundary should not intersect itself.

    Polygons are not necessarily planar by construction; they can be warped or skewed.

    The polygon does not have a coordinate frame.
    Its geometry is always defined with respect to the world coordinate system.

    Polygons can be constructed parametrically by the number of sides and a radius,
    but the geometry of the resulting object is defined by a list of explicit point locations.

    Parameters
    ----------
    points : list[[float, float, float] | :class:`compas.geometry.Point`]
        An ordered list of points.

    Attributes
    ----------
    points : list of :class:`compas.geometry.Point`
        The points of the polygon.
    lines : list of :class:`compas.geometry.Line`, read-only
        The lines of the polygon.
    length : float, read-only
        The length of the boundary.
    centroid : :class:`compas.geometry.Point`, read-only
        The centroid of the polygon.
    normal : :class:`compas.geometry.Vector`, read-only
        The (average) normal of the polygon.
    area : float, read-only
        The area of the polygon.
    is_convex : bool, read-only
        True if the polygon is convex.
    is_planar : bool, read-only
        True if the polygon is planar.

    See Also
    --------
    :func:`compas.geometry.centroid_polygon`,
    :func:`compas.geometry.area_polygon`,
    :func:`compas.geometry.is_polygon_convex`,
    :func:`earclip_polygon`

    Examples
    --------
    >>> polygon = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    >>> polygon.centroid
    Point(0.500, 0.500, 0.000)
    >>> polygon.area
    1.0

    """

    JSONSCHEMA = {
        "type": "object",
        "properties": {"points": {"type": "array", "minItems": 2, "items": Point.JSONSCHEMA}},
        "required": ["points"],
    }

    def __init__(self, points, **kwargs):
        super(Polygon, self).__init__(**kwargs)
        self._points = []
        self._lines = []
        self._vertices = []
        self._faces = []
        self.points = points

    def __repr__(self):
        return "{0}(points={1!r})".format(type(self).__name__, self.points)

    def __len__(self):
        return len(self.points)

    def __getitem__(self, key):
        return self.points[key]

    def __setitem__(self, key, value):
        self.points[key] = Point(*value)
        self._lines = None

    def __iter__(self):
        return iter(self.points)

    def __eq__(self, other):
        if not hasattr(other, "__iter__") or not hasattr(other, "__len__") or len(self) != len(other):
            return False
        return allclose(self, other)

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def data(self):
        return {"points": [point.data for point in self.points]}

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, points):
        if points[-1] == points[0]:
            points = points[:-1]
        self._points = [Point(*xyz) for xyz in points]
        self._lines = None

    @property
    def lines(self):
        if not self._lines:
            self._lines = [Line(a, b) for a, b in pairwise(self.points + self.points[:1])]
        return self._lines

    @property
    def vertices(self):
        if not self._vertices:
            return self.points
        return self._vertices

    @property
    def faces(self):
        if not self._faces:
            return [list(range(len(self.points)))]
        return self._faces

    @property
    def length(self):
        return sum(line.length for line in self.lines)

    @property
    def centroid(self):
        point = centroid_polygon(self.points)
        return Point(*point)

    @property
    def normal(self):
        return self.plane.normal

    @property
    def plane(self):
        return Plane.from_points(self.points)

    @property
    def frame(self):
        return Frame.from_plane(self.plane)

    @property
    def area(self):
        return area_polygon(self.points)

    @property
    def is_convex(self):
        return is_polygon_convex(self.points)

    @property
    def is_planar(self):
        return is_coplanar(self.points)

    @property
    def bounding_box(self):
        from compas.geometry import Box

        return Box.from_bounding_box(bounding_box(self.points))

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_rectangle(cls, point, width, height):
        """Construct a rectangle.

        Parameters
        ----------
        point : :class:`compas.geometry.Point`
            The lower left corner of the rectangle.
        width : float
            The width of the rectangle.
        height : float
            The height of the rectangle.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            A rectangle.

        """
        x, y, z = point
        points = [
            [x, y, z],
            [x + width, y, z],
            [x + width, y + height, z],
            [x, y + height, z],
        ]
        return cls(points)

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

        Raises
        ------
        ValueError
            If the number of sides is smaller than 3.

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
        if n < 3:
            raise ValueError("Supplied number of sides must be at least 3!")

        points = []
        side = math.pi * 2 / n
        for i in range(n):
            point = [
                math.sin(side * (n - i)) * radius,
                math.cos(side * (n - i)) * radius,
                0.0,
            ]
            points.append(point)
        return cls(points)

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_vertices_and_faces(self, earclip=False):
        """Returns a list of vertices and faces.

        Parameters
        ----------
        earclip : bool, optional
            Earclip the polygon before returning the vertices and faces.

        Returns
        -------
        list[list[float]], list[list[int]]
            A list of vertex locations, and a list of faces,
            with each face defined as a list of indices into the list of vertices.

        """
        if earclip:
            T = Transformation.from_change_of_basis(Frame.worldXY(), self.frame)
            points = transform_points(self.points, T)
            self._faces = earclip_polygon(points)
        return self.vertices, self.faces

    def to_mesh(self, earclip=False):
        """Returns a mesh representation of the polygon.

        Parameters
        ----------
        earclip : bool, optional
            Earclip the polygon before converting to a mesh.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces(earclip=earclip)
        return Mesh.from_vertices_and_faces(vertices, faces)

    def to_brep(self):
        """Returns a brep representation of the polygon.

        Returns
        -------
        :class:`compas.geometry.Brep`
            A boundary representation of the polygon.

        """
        from compas.geometry import Brep

        return Brep.from_polygons([self])

    # =============================================================================
    # Transformations
    # =============================================================================

    def transform(self, T):
        """Transform this polygon.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None

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

    # =============================================================================
    # Methods
    # =============================================================================

    def boolean_union(self, other):
        """Compute the boolean union of this polygon and another polygon.

        For this operation, both polygons are assumed to lie in the XY plane.
        Therefore, the Z components of the points defining the polygons are simply ignored.
        If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
        Otherwise the results are meaningless.

        Parameters
        ----------
        other : :class:`compas.geometry.Polygon`
            The other polygon.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            The union polygon.

        """
        from compas.geometry import boolean_union_polygon_polygon

        coords = boolean_union_polygon_polygon(self, other)
        return Polygon([[x, y, 0] for x, y in coords])  # type: ignore

    def boolean_difference(self, other):
        """Compute the boolean difference of this polygon and another polygon.

        For this operation, both polygons are assumed to lie in the XY plane.
        Therefore, the Z components of the points defining the polygons are simply ignored.
        If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
        Otherwise the results are meaningless.

        Parameters
        ----------
        other : :class:`compas.geometry.Polygon`
            The other polygon.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            The difference polygon.

        """
        from compas.geometry import boolean_difference_polygon_polygon

        coords = boolean_difference_polygon_polygon(self, other)
        return Polygon([[x, y, 0] for x, y in coords])  # type: ignore

    def boolean_symmetric_difference(self, other):
        """Compute the boolean symmetric difference of this polygon and another polygon.

        For this operation, both polygons are assumed to lie in the XY plane.
        Therefore, the Z components of the points defining the polygons are simply ignored.
        If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
        Otherwise the results are meaningless.

        Parameters
        ----------
        other : :class:`compas.geometry.Polygon`
            The other polygon.

        Returns
        -------
        list[:class:`compas.geometry.Polygon`]
            The resulting polygons.

        """
        from compas.geometry import boolean_symmetric_difference_polygon_polygon

        coordsets = boolean_symmetric_difference_polygon_polygon(self, other)
        polygons = [Polygon([[x, y, 0] for x, y in coords]) for coords in coordsets]  # type: ignore
        return polygons

    def boolean_intersection(self, other):
        """Compute the boolean intersection of this polygon and another polygon.

        For this operation, both polygons are assumed to lie in the XY plane.
        Therefore, the Z components of the points defining the polygons are simply ignored.
        If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
        Otherwise the results are meaningless.

        Parameters
        ----------
        other : :class:`compas.geometry.Polygon`
            The other polygon.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            The intersection polygon.

        """
        from compas.geometry import boolean_intersection_polygon_polygon

        coords = boolean_intersection_polygon_polygon(self, other)
        return Polygon([[x, y, 0] for x, y in coords])  # type: ignore
