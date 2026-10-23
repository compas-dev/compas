from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

from compas._typing import CoordinatesType

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import PolygonalSurface

__all__ = ["Tessellation"]

VerticesBuffer = TypeVar("VerticesBuffer", bound=CoordinatesType)
TrianglesBuffer = TypeVar("TrianglesBuffer", bound=Sequence[Sequence[int]])


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
    vertex_normals: CoordinatesType | None = None
    texture_coordinates: Sequence[Sequence[float]] | None = None
    polylines: Sequence[CoordinatesType] = ()

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
        tuple[CoordinatesType, Sequence[Sequence[int]]]
            The vertex and triangle buffers.

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

        return PolygonalSurface(self.vertices, [list(triangle) for triangle in self.triangles])

    def to_mesh(self) -> "Mesh":
        """Convert the tessellation to an independent half-edge mesh.

        Returns
        -------
        Mesh
            The half-edge mesh.

        """
        from compas.datastructures import Mesh

        return Mesh.from_vertices_and_faces(list(self.vertices), [list(triangle) for triangle in self.triangles])
