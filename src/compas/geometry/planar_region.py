from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas.geometry import Geometry
from compas.geometry import Polygon
from compas.geometry import is_coplanar

from .triangulation_earclip import _earclip_boundaries

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Plane
    from compas.geometry import PolygonalSurface
    from compas.geometry import Tessellation
    from compas.geometry import Transformation


class PlanarRegion(Geometry):
    """A planar area defined by an exterior boundary and optional holes.

    Parameters
    ----------
    outer
        The exterior boundary.
    holes
        The interior boundaries.
    name
        The name of the region.

    Notes
    -----
    All boundaries are copied. Construction checks that they are coplanar and
    contain at least three points. Tessellation additionally requires simple,
    non-intersecting loops, holes strictly inside the exterior boundary, and
    mutually disjoint holes. These more expensive topology checks run only when
    `triangles`, `to_vertices_and_faces()`, `to_polygonal_surface()`, or
    `to_mesh()` requests a tessellation.

    Examples
    --------
    >>> outer = [[0, 0, 0], [4, 0, 0], [4, 4, 0], [0, 4, 0]]
    >>> hole = [[1, 1, 0], [1, 3, 0], [3, 3, 0], [3, 1, 0]]
    >>> region = PlanarRegion(outer, holes=[hole])
    >>> region.area()
    12.0
    >>> len(region.triangles)
    8

    """

    # =============================================================================
    # Data
    # =============================================================================

    @property
    def __data__(self) -> dict:
        return {
            "outer": [list(point) for point in self.outer.points],
            "holes": [[list(point) for point in hole.points] for hole in self.holes],
        }

    @classmethod
    def __from_data__(cls, data: dict) -> Self:
        return cls(data["outer"], holes=data.get("holes", []))

    # =============================================================================
    # Dunder methods
    # =============================================================================

    def __init__(
        self,
        outer: Polygon | CoordinatesType,
        holes: Sequence[Polygon | CoordinatesType] | None = None,
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self._outer = self._copy_boundary(outer)
        self._holes = [self._copy_boundary(hole) for hole in holes or []]
        self._validate()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(outer={self.outer.points!r}, holes={[hole.points for hole in self.holes]!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlanarRegion):
            return False
        return self.outer == other.outer and self.holes == other.holes

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def outer(self) -> Polygon:
        """The exterior boundary."""
        return self._outer

    @property
    def holes(self) -> list[Polygon]:
        """The interior boundaries."""
        return self._holes

    @property
    def boundaries(self) -> list[Polygon]:
        """The exterior boundary followed by the interior boundaries."""
        return [self.outer, *self.holes]

    @property
    def plane(self) -> "Plane":
        """The plane of the region, oriented with the exterior boundary."""
        return self.outer.plane

    @property
    def vertices(self) -> list[list[float]]:
        """Independent coordinates of all flattened boundary vertices."""
        return [[float(value) for value in point] for boundary in self.boundaries for point in boundary.points]

    @property
    def triangles(self) -> list[list[int]]:
        """The triangulation as indices into `vertices`.

        Raises
        ------
        ValueError
            If a boundary self-intersects, a hole is not strictly inside the
            exterior boundary, or holes overlap, touch, or contain one another.

        """
        _, triangles = _earclip_boundaries(self.outer, self.holes)
        return triangles

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_vertices_and_faces(self) -> tuple[list[list[float]], list[list[int]]]:
        """Return the flattened boundary vertices and triangulated faces.

        Returns
        -------
        tuple[list[list[float]], list[list[int]]]
            The exterior vertices followed by each hole's vertices, and the
            triangles indexing that flattened vertex list.

        Raises
        ------
        ValueError
            If the boundary topology is invalid for tessellation.

        """
        return _earclip_boundaries(self.outer, self.holes)

    def tessellated(self) -> "Tessellation":
        """Return a triangular tessellation of the planar region.

        Returns
        -------
        Tessellation
            The indexed triangular representation.

        """
        from compas.geometry import Tessellation

        vertices, triangles = self.to_vertices_and_faces()
        return Tessellation(vertices, triangles)

    def to_polygonal_surface(self) -> "PolygonalSurface":
        """Convert the region to a triangulated polygonal surface.

        Returns
        -------
        PolygonalSurface

        """
        return self.tessellated().to_polygonal_surface()

    def to_mesh(self) -> "Mesh":
        """Convert the region to a triangulated half-edge mesh.

        Returns
        -------
        Mesh

        """
        return self.tessellated().to_mesh()

    # =============================================================================
    # Methods
    # =============================================================================

    def area(self) -> float:
        """Compute the exterior area minus the areas of the holes."""
        return self.outer.area() - sum(hole.area() for hole in self.holes)

    def aabb(self) -> "Box":
        """Compute the axis-aligned bounding box.

        Returns
        -------
        Box

        """
        return self.to_polygonal_surface().aabb()

    def obb(self) -> "Box":
        """Compute the oriented bounding box.

        Returns
        -------
        Box

        """
        return self.to_polygonal_surface().obb()

    # =============================================================================
    # Transformations
    # =============================================================================

    def transform(self, transformation: "Transformation") -> None:
        """Transform all region boundaries.

        Parameters
        ----------
        transformation
            The transformation applied to the region.

        """
        for boundary in self.boundaries:
            boundary.transform(transformation)

    # =============================================================================
    # Private helpers
    # =============================================================================

    @staticmethod
    def _copy_boundary(boundary: Polygon | CoordinatesType) -> Polygon:
        points = boundary.points if isinstance(boundary, Polygon) else boundary
        return Polygon(points)

    def _validate(self) -> None:
        for boundary in self.boundaries:
            if len(boundary) < 3:
                raise ValueError("A planar-region boundary requires at least three points.")
        points = [list(point) for boundary in self.boundaries for point in boundary.points]
        if not is_coplanar(points):
            raise ValueError("All planar-region boundaries must be coplanar.")
