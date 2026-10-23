import math
from collections.abc import Iterator
from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Self
from typing import overload

from compas._typing import CoordinatesType
from compas.geometry import Frame
from compas.geometry import Geometry
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import area_polygon
from compas.geometry import bounding_box
from compas.geometry import centroid_polygon
from compas.geometry import earclip_polygon
from compas.geometry import is_coplanar
from compas.geometry import is_polygon_convex
from compas.geometry import normal_triangle
from compas.geometry import transform_points
from compas.itertools import pairwise
from compas.tolerance import TOL

from ._typing import CoordinateType
from ._typing import TransformationType

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Brep
    from compas.geometry import PlanarRegion
    from compas.geometry import Tessellation
    from compas.geometry import Vector


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
    points
        An ordered list of points.
    name
        The name of the polygon.

    See Also
    --------
    [`centroid_polygon`][compas.geometry.centroid_polygon]
    [`area_polygon`][compas.geometry.area_polygon]
    [`is_polygon_convex`][compas.geometry.is_polygon_convex]
    [`earclip_polygon`][compas.geometry.earclip_polygon]

    Examples
    --------
    >>> polygon = Polygon([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]])
    >>> point = polygon.centroid()
    >>> print(point)
    Point(x=0.500, y=0.500, z=0.000)
    >>> polygon.area()
    1.0

    """

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict:
        return {"points": [point.__data__ for point in self.points]}

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, points: CoordinatesType, name: str | None = None) -> None:
        super().__init__(name=name)
        self._points: list[Point] = []
        self._lines: list[Line] | None = None
        self.points = points

    def __repr__(self) -> str:
        return "{0}(points={1!r})".format(type(self).__name__, self.points)

    def __str__(self) -> str:
        return "{0}(points=[{1}])".format(type(self).__name__, ", ".join([str(point) for point in self.points]))

    def __len__(self) -> int:
        return len(self.points)

    @overload
    def __getitem__(self, key: int) -> Point: ...

    @overload
    def __getitem__(self, key: slice) -> list[Point]: ...

    def __getitem__(self, key: int | slice) -> Point | list[Point]:
        return self.points[key]

    def __setitem__(self, key: int, value: CoordinateType) -> None:
        self.points[key] = Point(value[0], value[1], value[2])
        self._lines = None

    def __iter__(self) -> Iterator[Point]:
        return iter(self.points)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, (Polygon, Sequence)) or len(self) != len(other):
            return False
        return TOL.is_allclose(self, other)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def points(self) -> list[Point]:
        """The ordered polygon points.

        Notes
        -----
        Assigning points removes consecutive duplicates and a repeated closing
        point. The boundary-line cache is invalidated.

        """
        return self._points

    @points.setter
    def points(self, points: CoordinatesType) -> None:
        previous = Point(points[0][0], points[0][1], points[0][2])
        self._points = [previous]
        for index, xyz in enumerate(points):
            if index == 0:
                continue
            if previous == xyz:
                continue
            previous = Point(xyz[0], xyz[1], xyz[2])
            self._points.append(previous)
        if self._points[0] == self._points[-1]:
            del self._points[-1]
        self._lines = None

    @property
    def lines(self) -> list[Line]:
        """The boundary segments, including the implicit closing segment."""
        if not self._lines:
            self._lines = [Line(a, b) for a, b in pairwise(self.points + self.points[:1])]
        return self._lines

    @property
    def vertices(self) -> list[Point]:
        """The polygon points as vertices."""
        return self.points

    @property
    def faces(self) -> list[list[int]]:
        """The single polygon face as point indices."""
        return [list(range(len(self.points)))]

    @property
    def length(self) -> float:
        """The length of the closed boundary."""
        return sum(line.length for line in self.lines)

    @property
    def plane(self) -> Plane:
        """The best-fit plane aligned with the point winding."""
        # by just taking the bestfit plane,
        # the normal might not be aligned with the winding direciton of the polygon
        # this can be solved by comparing the plane normal with the normal of one of the triangles of the polygon
        # for convex polygons this is always correct
        # in the case of concave polygons it may not be
        # to be entirely correct, the check should be done with one of the polygon ears after earclipping
        # however, this is costly
        # and even then it is only correct if we assume th polygon is plat enough to have a consistent direction
        normal = normal_triangle([self.centroid()] + self.points[:2])
        plane = Plane.from_points(self.points)
        if plane.normal.dot(normal) < 0:
            plane.normal.flip()
        return plane

    @property
    def frame(self) -> Frame:
        """A frame aligned with the polygon plane."""
        return Frame.from_plane(self.plane)

    @property
    def is_convex(self) -> bool:
        """Whether the polygon is convex."""
        return is_polygon_convex(self.points)

    @property
    def is_planar(self) -> bool:
        """Whether all polygon points are coplanar."""
        return is_coplanar(self.points)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_rectangle(cls, point: CoordinateType, width: float, height: float) -> Self:
        """Construct a rectangle.

        Parameters
        ----------
        point
            The lower left corner of the rectangle.
        width
            The width of the rectangle.
        height
            The height of the rectangle.

        Returns
        -------
        Self
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
    def from_sides_and_radius_xy(cls, n: int, radius: float) -> Self:
        """Construct a polygon from a number of sides and a radius.
        The resulting polygon is planar, equilateral and equiangular.

        Parameters
        ----------
        n
            The number of sides.
        radius
            The radius of the circle the polygon will be circumscribed to.

        Returns
        -------
        Self
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
        >>> from compas.linalg import dot_vectors
        >>> from compas.linalg import subtract_vectors
        >>> pentagon = Polygon.from_sides_and_radius_xy(5, 1.0)
        >>> len(pentagon.lines) == 5
        True
        >>> len({round(line.length, 6) for line in pentagon.lines}) == 1
        True
        >>> dot_vectors(pentagon.normal(), [0.0, 0.0, 1.0]) == 1
        True
        >>> centertofirst = subtract_vectors(pentagon.points[0], pentagon.centroid())
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

    def tessellated(self) -> "Tessellation":
        """Return a triangular tessellation of the polygon.

        Returns
        -------
        Tessellation
            The indexed triangular representation for visualization.

        """
        from compas.geometry import Tessellation

        return Tessellation(self.vertices, earclip_polygon(self))

    def to_vertices_and_faces(self, earclip: bool = False) -> tuple[list[Point], list[list[int]]]:
        """Return the polygon vertices and indexed faces.

        Parameters
        ----------
        earclip
            If `True`, triangulate the polygon using ear clipping.

        Returns
        -------
        tuple[list[Point], list[list[int]]]
            The polygon points and indexed faces.

        """
        if earclip:
            return self.vertices, earclip_polygon(self)
        return self.vertices, self.faces

    def to_mesh(self) -> "Mesh":
        """Convert the polygon to a mesh.

        Returns
        -------
        Mesh

        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces()
        return Mesh.from_vertices_and_faces(vertices, faces)

    def to_brep(self) -> "Brep":
        """Convert the polygon to a boundary representation.

        Returns
        -------
        Brep

        """
        from compas.geometry import Brep

        return Brep.from_polygons([self])

    # =============================================================================
    # Transformations
    # =============================================================================

    def transform(self, transformation: TransformationType) -> None:
        """Transform this polygon.

        Parameters
        ----------
        transformation
            The transformation.

        Examples
        --------
        >>> from math import radians
        >>> from compas.geometry import Rotation
        >>> polygon = Polygon.from_sides_and_radius_xy(4, 1.0)
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], radians(45))
        >>> polygon.transform(R)
        >>> point = polygon.points[0]
        >>> print(point)
        Point(x=-0.707, y=0.707, z=0.000)

        """
        for index, point in enumerate(transform_points(self.points, transformation)):
            self.points[index].x = point[0]
            self.points[index].y = point[1]
            self.points[index].z = point[2]
        self._lines = None

    # =============================================================================
    # Methods
    # =============================================================================

    def aabb(self) -> "Box":
        """Compute the axis-aligned bounding box.

        Returns
        -------
        Box

        """
        from compas.geometry import Box

        return Box.from_bounding_box(bounding_box(self.points))

    def obb(self) -> "Box":
        """Compute the oriented bounding box.

        Returns
        -------
        Box

        """
        from compas.geometry import Box
        from compas.geometry import oriented_bounding_box

        return Box.from_bounding_box(oriented_bounding_box(self.points))

    def area(self) -> float:
        """Compute the polygon surface area."""
        return area_polygon(self.points)

    def centroid(self) -> Point:
        """Compute the centroid of the polygon surface."""
        point = centroid_polygon(self.points)
        return Point(point[0], point[1], point[2])

    def normal(self) -> "Vector":
        """Compute the polygon normal aligned with the point winding."""
        return self.plane.normal

    def boolean_union(self, other: "Polygon") -> list["PlanarRegion"]:
        """Compute the boolean union of this polygon and another polygon.

        For this operation, both polygons are assumed to lie in the XY plane.
        Therefore, the Z components of the points defining the polygons are simply ignored.
        If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
        Otherwise the results are meaningless.

        Parameters
        ----------
        other
            The other polygon.

        Returns
        -------
        list[PlanarRegion]
            The connected components of the union.

        """
        from compas.geometry import boolean_union_polygon_polygon

        return boolean_union_polygon_polygon(self, other)

    def boolean_difference(self, other: "Polygon") -> list["PlanarRegion"]:
        """Compute the boolean difference of this polygon and another polygon.

        For this operation, both polygons are assumed to lie in the XY plane.
        Therefore, the Z components of the points defining the polygons are simply ignored.
        If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
        Otherwise the results are meaningless.

        Parameters
        ----------
        other
            The other polygon.

        Returns
        -------
        list[PlanarRegion]
            The connected components of the difference.

        """
        from compas.geometry import boolean_difference_polygon_polygon

        return boolean_difference_polygon_polygon(self, other)

    def boolean_symmetric_difference(self, other: "Polygon") -> list["PlanarRegion"]:
        """Compute the boolean symmetric difference of this polygon and another polygon.

        For this operation, both polygons are assumed to lie in the XY plane.
        Therefore, the Z components of the points defining the polygons are simply ignored.
        If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
        Otherwise the results are meaningless.

        Parameters
        ----------
        other
            The other polygon.

        Returns
        -------
        list[PlanarRegion]
            The connected components of the symmetric difference.

        """
        from compas.geometry import boolean_symmetric_difference_polygon_polygon

        return boolean_symmetric_difference_polygon_polygon(self, other)

    def boolean_intersection(self, other: "Polygon") -> list["PlanarRegion"]:
        """Compute the boolean intersection of this polygon and another polygon.

        For this operation, both polygons are assumed to lie in the XY plane.
        Therefore, the Z components of the points defining the polygons are simply ignored.
        If the polygons are not in the XY plane, it is the responibility of the user to transform them accordingly.
        Otherwise the results are meaningless.

        Parameters
        ----------
        other
            The other polygon.

        Returns
        -------
        list[PlanarRegion]
            The connected components of the intersection.

        """
        from compas.geometry import boolean_intersection_polygon_polygon

        return boolean_intersection_polygon_polygon(self, other)
