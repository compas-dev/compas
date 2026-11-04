from dataclasses import dataclass
from math import isfinite
from numbers import Integral
from numbers import Real
from operator import index as integer_index
from typing import TYPE_CHECKING
from typing import Generic
from typing import TypeVar

import numpy as np

from compas._typing import CoordinatesCollectionInput
from compas._typing import CoordinatesInput
from compas._typing import IndicesCollectionInput
from compas.data import Data

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import PolygonalSurface

__all__ = [
    "Adaptive",
    "Deflection",
    "Native",
    "Tessellation",
    "TessellationStrategy",
    "UGrid",
    "UVGrid",
]

VerticesBuffer = TypeVar("VerticesBuffer", bound=CoordinatesInput)
TrianglesBuffer = TypeVar("TrianglesBuffer", bound=IndicesCollectionInput)


def _positive_integer(value: int, name: str) -> int:
    if not isinstance(value, Integral) or isinstance(value, bool):
        raise TypeError(f"{name} should be an integer.")
    if value <= 0:
        raise ValueError(f"{name} should be positive.")
    return int(value)


def _positive_finite(value: float, name: str) -> float:
    if not isinstance(value, Real) or isinstance(value, bool):
        raise TypeError(f"{name} should be a real number.")
    value = float(value)
    if not isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} should be positive and finite.")
    return value


class TessellationStrategy(Data):
    """Base class for serializable tessellation policy configurations.

    Strategies describe approximation policy. Geometry producers own the
    algorithms that implement the supported strategies.

    """

    def __init__(self) -> None:
        super().__init__()
        self._frozen = False

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_frozen", False) and name not in {"_guid", "_name"}:
            raise AttributeError(f"{type(self).__name__} is immutable.")
        super().__setattr__(name, value)

    def __eq__(self, other: object) -> bool:
        return type(self) is type(other) and isinstance(other, TessellationStrategy) and self.__data__ == other.__data__

    def __hash__(self) -> int:
        return hash((type(self), tuple(self.__data__.items())))

    def _freeze(self) -> None:
        self._frozen = True


class Native(TessellationStrategy):
    """Use a geometry's fixed natural topology."""

    @property
    def __data__(self) -> dict:
        return {}

    def __init__(self) -> None:
        super().__init__()
        self._freeze()


class UGrid(TessellationStrategy):
    """A one-dimensional parameter-grid strategy.

    Parameters
    ----------
    u
        The number of faces in the U direction.

    """

    @property
    def __data__(self) -> dict:
        return {"u": self.u}

    def __init__(self, u: int) -> None:
        super().__init__()
        self.u = _positive_integer(u, "u")
        self._freeze()


class UVGrid(TessellationStrategy):
    """A two-dimensional parameter-grid strategy.

    Parameters
    ----------
    u
        The number of faces in the U direction.
    v
        The number of faces in the V direction.

    """

    @property
    def __data__(self) -> dict:
        return {"u": self.u, "v": self.v}

    def __init__(self, u: int, v: int) -> None:
        super().__init__()
        self.u = _positive_integer(u, "u")
        self.v = _positive_integer(v, "v")
        self._freeze()


class Deflection(TessellationStrategy):
    """A linear and angular deflection strategy.

    Parameters
    ----------
    linear
        The positive linear deflection in model units.
    angular
        The positive angular deflection in degrees, at most 180.

    """

    @property
    def __data__(self) -> dict:
        return {"linear": self.linear, "angular": self.angular}

    def __init__(self, linear: float, angular: float) -> None:
        super().__init__()
        self.linear = _positive_finite(linear, "linear")
        self.angular = _positive_finite(angular, "angular")
        if self.angular > 180.0:
            raise ValueError("angular should be at most 180 degrees.")
        self._freeze()


class Adaptive(TessellationStrategy):
    """An adaptive tessellation request.

    Parameters
    ----------
    max_deviation
        The optional maximum deviation in model units.
    max_angle
        The optional maximum normal angle in degrees.
    max_edge_length
        The optional maximum edge length in model units.

    """

    @property
    def __data__(self) -> dict:
        return {
            "max_deviation": self.max_deviation,
            "max_angle": self.max_angle,
            "max_edge_length": self.max_edge_length,
        }

    def __init__(
        self,
        max_deviation: float | None = None,
        max_angle: float | None = None,
        max_edge_length: float | None = None,
    ) -> None:
        super().__init__()
        if max_deviation is None and max_angle is None and max_edge_length is None:
            raise ValueError("At least one adaptive constraint is required.")
        self.max_deviation = None if max_deviation is None else _positive_finite(max_deviation, "max_deviation")
        self.max_angle = None if max_angle is None else _positive_finite(max_angle, "max_angle")
        if self.max_angle is not None and self.max_angle > 180.0:
            raise ValueError("max_angle should be at most 180 degrees.")
        self.max_edge_length = None if max_edge_length is None else _positive_finite(max_edge_length, "max_edge_length")
        self._freeze()


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
    vertex_normals: CoordinatesInput | None = None
    texture_coordinates: CoordinatesInput | None = None
    polylines: CoordinatesCollectionInput = ()

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
    def _validate_coordinates(coordinates: CoordinatesInput, name: str, dimension: int) -> None:
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
