from dataclasses import dataclass
from math import isfinite
from operator import index as integer_index
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

import numpy as np

from compas.typing import IndexGroupsLike
from compas.typing import PointGroupsLike
from compas.typing import PointsLike

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import PolygonalSurface

__all__ = ["Tessellation"]

VerticesBuffer = TypeVar("VerticesBuffer", bound=PointsLike)
TrianglesBuffer = TypeVar("TrianglesBuffer", bound=IndexGroupsLike)


@dataclass(frozen=True, slots=True, eq=False)
class Tessellation(Generic[VerticesBuffer, TrianglesBuffer]):
    """An indexed triangular representation for visualization.

    Parameters
    ----------
    vertices
        The vertex-coordinate buffer.
    triangles
        The triangles as indices into `vertices`.
    vertex_normals
        Optional vertex normals using the same indexing as `vertices`.
    texture_coordinates
        Optional UV coordinates using the same indexing as `vertices`.
    polylines
        Optional independent polylines, for example discretized Brep edges.

    Notes
    -----
    Tessellation is distinct from discretisation. Discretisation samples the
    defining geometry and may retain polygonal faces and domain edges.
    Tessellation converts geometry to triangles for visualization or
    triangle-based processing and may duplicate vertices at attribute seams.

    The supplied buffers are retained without copying or conversion. They may
    therefore be ordinary Python sequences, NumPy arrays, or compatible native
    buffer wrappers. Callers should treat them as immutable for the lifetime of
    the tessellation.

    Vertex normals and texture coordinates are indexed together with the
    vertices. Tessellators should duplicate vertices at normal or texture seams
    rather than introduce separate attribute-index buffers. This keeps the
    representation directly usable by mesh consumers and GPU vertex buffers.

    `Tessellation` is an ephemeral operation result rather than serialized
    geometry. Use `to_polygonal_surface()` or `to_mesh()` when an independent
    COMPAS object is required.

    Examples
    --------
    >>> tessellation = Tessellation(
    ...     vertices=[[0, 0, 0], [1, 0, 0], [0, 1, 0]],
    ...     triangles=[[0, 1, 2]],
    ... )
    >>> tessellation.number_of_vertices
    3
    >>> tessellation.number_of_triangles
    1

    """

    vertices: VerticesBuffer
    triangles: TrianglesBuffer
    vertex_normals: PointsLike | None = None
    texture_coordinates: PointsLike | None = None
    polylines: PointGroupsLike = ()

    def __post_init__(self) -> None:
        self._validate()

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def number_of_vertices(self) -> int:
        """The number of vertices."""
        return len(self.vertices)

    @property
    def number_of_triangles(self) -> int:
        """The number of triangles."""
        return len(self.triangles)

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_vertices_and_triangles(self) -> tuple[VerticesBuffer, TrianglesBuffer]:
        """Return the original vertex and triangle buffers without copying.

        Returns
        -------
        tuple[VerticesBuffer, TrianglesBuffer]
            The original vertex and triangle buffer types.

        """
        return self.vertices, self.triangles

    def to_polygonal_surface(self) -> "PolygonalSurface":
        """Convert the tessellation to an independent polygonal surface.

        Returns
        -------
        PolygonalSurface
            The polygonal surface.

        """
        from compas.geometry import PolygonalSurface

        vertices = [[float(value) for value in vertex] for vertex in self.vertices]
        triangles = [[integer_index(index) for index in triangle] for triangle in self.triangles]
        return PolygonalSurface(vertices, triangles)

    def to_mesh(self) -> "Mesh":
        """Convert the tessellation to an independent half-edge mesh.

        Returns
        -------
        Mesh
            The half-edge mesh.

        """
        from compas.datastructures import Mesh

        vertices = [[float(value) for value in vertex] for vertex in self.vertices]
        triangles = [[integer_index(index) for index in triangle] for triangle in self.triangles]
        return Mesh.from_vertices_and_faces(vertices, triangles)

    # =============================================================================
    # Validation
    # =============================================================================

    def _validate(self) -> None:
        vertex_count = len(self.vertices)
        self._validate_coordinates(self.vertices, "vertex", 3)

        for triangle in self.triangles:
            if len(triangle) != 3:
                raise ValueError("A tessellation triangle requires exactly three indices.")
            for index in triangle:
                if isinstance(index, (bool, np.bool_)):
                    raise TypeError("Tessellation triangle indices should be integers.")
                try:
                    checked_index = integer_index(index)
                except TypeError:
                    raise TypeError("Tessellation triangle indices should be integers.")
                if checked_index < 0 or checked_index >= vertex_count:
                    raise IndexError("Tessellation triangle index is out of range.")

        if self.vertex_normals is not None:
            if len(self.vertex_normals) != vertex_count:
                raise ValueError("Tessellation vertex normals should align with the vertices.")
            self._validate_coordinates(self.vertex_normals, "vertex normal", 3)

        if self.texture_coordinates is not None:
            if len(self.texture_coordinates) != vertex_count:
                raise ValueError("Tessellation texture coordinates should align with the vertices.")
            self._validate_coordinates(self.texture_coordinates, "texture coordinate", 2)

        for polyline in self.polylines:
            self._validate_coordinates(polyline, "polyline point", 3)

    @staticmethod
    def _validate_coordinates(coordinates: PointsLike, name: str, dimension: int) -> None:
        for coordinate in coordinates:
            if len(coordinate) != dimension:
                raise ValueError(f"A tessellation {name} requires exactly {dimension} coordinates.")
            for value in coordinate:
                if isinstance(value, (bool, np.bool_)):
                    raise TypeError(f"Tessellation {name} coordinates should be real numbers.")
                try:
                    finite = isfinite(value)
                except (TypeError, ValueError):
                    raise TypeError(f"Tessellation {name} coordinates should be real numbers.")
                if not finite:
                    raise ValueError(f"Tessellation {name} coordinates should be finite.")
