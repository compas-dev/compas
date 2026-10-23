from collections import defaultdict
from collections import deque
from numbers import Real
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas.geometry import Geometry
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Transformation
from compas.geometry import transform_points
from compas.itertools import pairwise
from compas.tolerance import TOL

from .triangulation_earclip import earclip_polygon

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Tessellation


class PolygonalSurface(Geometry):
    """A lightweight polygonal surface defined by indexed vertices and faces.

    A polygonal surface stores geometry and face indices without maintaining a
    half-edge data structure. It may be open or closed, connected or
    disconnected, and manifold or non-manifold.

    Parameters
    ----------
    vertices
        The vertex coordinates.
    faces
        The faces as sequences of vertex indices.
    name
        The name of the surface.

    Notes
    -----
    The input vertices and faces are copied. This prevents subsequent mutation
    of the input collections from changing the surface.

    Examples
    --------
    >>> surface = PolygonalSurface(
    ...     [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
    ...     [[0, 1, 2, 3]],
    ... )
    >>> surface.is_closed
    False
    >>> surface.area()
    1.0

    """

    @property
    def __data__(self) -> dict:
        return {"vertices": self.vertices, "faces": self.faces}

    @classmethod
    def __from_data__(cls, data: dict) -> Self:
        return cls(data["vertices"], data["faces"])

    def __init__(
        self,
        vertices: CoordinatesType,
        faces: list[list[int]],
        name: str | None = None,
    ) -> None:
        super().__init__(name=name)
        self._vertices: list[list[float]] = []
        self._faces: list[list[int]] = []
        self.vertices = vertices
        self.faces = faces

    def __repr__(self) -> str:
        return "{0}(vertices={1!r}, faces={2!r})".format(type(self).__name__, self.vertices, self.faces)

    def __str__(self) -> str:
        vertices = [[TOL.format_number(value) for value in vertex] for vertex in self.vertices]
        return "{0}(vertices={1}, faces={2})".format(type(self).__name__, vertices, self.faces)

    # =============================================================================
    # Properties
    # =============================================================================

    @property
    def vertices(self) -> list[list[float]]:
        """The vertex coordinates of the surface.

        Notes
        -----
        Assigning vertices creates an independent copy and requires exactly
        three coordinates per vertex.

        """
        return self._vertices

    @vertices.setter
    def vertices(self, vertices: CoordinatesType) -> None:
        copied = []
        for vertex in vertices:
            if len(vertex) != 3:
                raise ValueError("A polygonal-surface vertex requires exactly three coordinates.")
            if not all(isinstance(value, Real) and not isinstance(value, bool) for value in vertex):
                raise TypeError("Polygonal-surface vertex coordinates should be real numbers.")
            copied.append([float(vertex[0]), float(vertex[1]), float(vertex[2])])
        self._validate_faces(self._faces, vertex_count=len(copied))
        self._vertices = copied

    @property
    def faces(self) -> list[list[int]]:
        """The faces as lists of vertex indices.

        Notes
        -----
        Assigning faces creates an independent copy and validates all indices.

        """
        return self._faces

    @faces.setter
    def faces(self, faces: list[list[int]]) -> None:
        copied = [list(face) for face in faces]
        self._validate_faces(copied)
        self._faces = copied

    @property
    def edges(self) -> list[tuple[int, int]]:
        """The unique unoriented edges as vertex-index pairs."""
        edges = []
        seen = set()
        for face in self.faces:
            for u, v in pairwise(face + face[:1]):
                edge = (min(u, v), max(u, v))
                if edge not in seen:
                    seen.add(edge)
                    edges.append((u, v))
        return edges

    @property
    def points(self) -> list[Point]:
        """The vertices as independent points."""
        return [Point(vertex[0], vertex[1], vertex[2]) for vertex in self.vertices]

    @property
    def lines(self) -> list[Line]:
        """The unique edges as lines."""
        return [Line(self.vertices[u], self.vertices[v]) for u, v in self.edges]

    @property
    def polygons(self) -> list[Polygon]:
        """The faces as polygons."""
        return [Polygon([self.vertices[index] for index in face]) for face in self.faces]

    @property
    def triangles(self) -> list[list[int]]:
        """A triangulation of all faces using the existing vertex indices.

        General polygonal faces are triangulated by ear clipping, which supports
        concave planar faces without introducing additional vertices.

        """
        triangles = []
        for face in self.faces:
            if len(face) == 3:
                triangles.append(face[:])
                continue
            polygon = Polygon([self.vertices[index] for index in face])
            triangles.extend([[face[index] for index in triangle] for triangle in earclip_polygon(polygon)])
        return triangles

    @property
    def is_closed(self) -> bool:
        """Whether every edge belongs to exactly two faces."""
        closed, _, _, _ = self._analyze_topology()
        return closed

    @property
    def is_manifold(self) -> bool:
        """Whether the surface is a two-manifold, possibly with boundary."""
        _, manifold, _, _ = self._analyze_topology()
        return manifold

    @property
    def is_orientable(self) -> bool:
        """Whether face orientations can be made consistent."""
        _, _, orientable, _ = self._analyze_topology()
        return orientable

    @property
    def is_oriented(self) -> bool:
        """Whether adjacent faces use every shared edge in opposite directions."""
        _, _, _, oriented = self._analyze_topology()
        return oriented

    # =============================================================================
    # Constructors
    # =============================================================================

    @classmethod
    def from_mesh(cls, mesh: "Mesh") -> Self:
        """Construct a polygonal surface from a mesh.

        Parameters
        ----------
        mesh
            The mesh providing the vertices and faces.

        Returns
        -------
        Self

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [0, 1, 0]], [[0, 1, 2]])
        >>> surface = PolygonalSurface.from_mesh(mesh)
        >>> surface.faces
        [[0, 1, 2]]

        """
        vertices, faces = mesh.to_vertices_and_faces()
        return cls(vertices, faces)

    # =============================================================================
    # Conversions
    # =============================================================================

    def tessellated(self) -> "Tessellation":
        """Return a triangular tessellation of the polygonal surface.

        Returns
        -------
        Tessellation
            The indexed triangular representation for visualization.

        Notes
        -----
        The result references the surface's vertex buffer directly. Treat the
        buffer as immutable while using the tessellation.

        """
        from compas.geometry import Tessellation

        return Tessellation(self.vertices, self.triangles)

    def to_vertices_and_faces(self, triangulated: bool = False) -> tuple[list[list[float]], list[list[int]]]:
        """Return independent copies of the vertices and faces.

        Parameters
        ----------
        triangulated
            If `True`, triangulate all polygonal faces.

        Returns
        -------
        tuple[list[list[float]], list[list[int]]]
            The vertex coordinates and indexed faces.

        """
        faces = self.triangles if triangulated else self.faces
        return [vertex[:] for vertex in self.vertices], [face[:] for face in faces]

    def to_mesh(self) -> "Mesh":
        """Convert the polygonal surface to a half-edge mesh.

        Returns
        -------
        Mesh

        """
        from compas.datastructures import Mesh

        vertices, faces = self.to_vertices_and_faces()
        return Mesh.from_vertices_and_faces(vertices, faces)

    # =============================================================================
    # Methods
    # =============================================================================

    def area(self) -> float:
        """Compute the sum of the polygonal face areas."""
        return sum(polygon.area() for polygon in self.polygons)

    def aabb(self) -> "Box":
        """Compute the axis-aligned bounding box.

        Returns
        -------
        Box

        """
        from compas.geometry import Box
        from compas.geometry import bounding_box

        if not self.vertices:
            raise ValueError("An empty polygonal surface has no bounding box.")
        return Box.from_bounding_box(bounding_box(self.vertices))

    def obb(self) -> "Box":
        """Compute the oriented bounding box.

        Returns
        -------
        Box

        """
        from compas.geometry import Box
        from compas.geometry import oriented_bounding_box

        if not self.vertices:
            raise ValueError("An empty polygonal surface has no bounding box.")
        return Box.from_bounding_box(oriented_bounding_box(self.vertices))

    # =============================================================================
    # Transformations
    # =============================================================================

    def transform(self, transformation: Transformation) -> None:
        """Transform the vertices of the surface.

        Parameters
        ----------
        transformation
            The transformation applied to the vertices.

        """
        self._vertices = transform_points(self.vertices, transformation)

    # =============================================================================
    # Private helpers
    # =============================================================================

    def _validate_faces(self, faces: list[list[int]], vertex_count: int | None = None) -> None:
        if vertex_count is None:
            vertex_count = len(self._vertices)
        for face in faces:
            if len(face) < 3:
                raise ValueError("A polygonal-surface face requires at least three vertices.")
            if len(set(face)) != len(face):
                raise ValueError("A polygonal-surface face cannot repeat vertex indices.")
            for index in face:
                if not isinstance(index, int):
                    raise TypeError("Polygonal-surface face indices should be integers.")
                if index < 0 or index >= vertex_count:
                    raise IndexError("A polygonal-surface face index is outside the vertex range.")

    def _analyze_topology(self) -> tuple[bool, bool, bool, bool]:
        edge_uses: dict[tuple[int, int], list[tuple[int, int, int]]] = defaultdict(list)
        vertex_faces: dict[int, set[int]] = defaultdict(set)
        vertex_edges: dict[int, set[tuple[int, int]]] = defaultdict(set)

        for f, face in enumerate(self.faces):
            for u, v in pairwise(face + face[:1]):
                edge = (min(u, v), max(u, v))
                edge_uses[edge].append((f, u, v))
                vertex_faces[u].add(f)
                vertex_faces[v].add(f)
                vertex_edges[u].add(edge)
                vertex_edges[v].add(edge)

        closed = bool(self.faces) and all(len(uses) == 2 for uses in edge_uses.values())
        manifold = not any(len(uses) > 2 for uses in edge_uses.values())
        oriented = all(len(uses) < 2 or uses[0][1:] == uses[1][1:][::-1] for uses in edge_uses.values())

        face_adjacency: dict[int, list[tuple[int, bool]]] = defaultdict(list)
        for uses in edge_uses.values():
            if len(uses) != 2:
                continue
            (a, au, av), (b, bu, bv) = uses
            must_flip = (au, av) == (bu, bv)
            face_adjacency[a].append((b, must_flip))
            face_adjacency[b].append((a, must_flip))

        if manifold:
            for vertex, incident in vertex_faces.items():
                adjacency = {face: set() for face in incident}
                boundary_edges = 0
                for edge in vertex_edges[vertex]:
                    uses = edge_uses[edge]
                    if len(uses) == 1:
                        boundary_edges += 1
                    elif len(uses) == 2:
                        a = uses[0][0]
                        b = uses[1][0]
                        adjacency[a].add(b)
                        adjacency[b].add(a)
                if boundary_edges not in (0, 2):
                    manifold = False
                    break
                visited = set()
                pending = [next(iter(incident))]
                while pending:
                    face = pending.pop()
                    if face in visited:
                        continue
                    visited.add(face)
                    pending.extend(adjacency[face] - visited)
                if len(visited) != len(incident):
                    manifold = False
                    break

        orientable = manifold
        if orientable:
            flips: dict[int, bool] = {}
            for start in range(len(self.faces)):
                if start in flips:
                    continue
                flips[start] = False
                pending = deque([start])
                while pending:
                    face = pending.popleft()
                    for neighbor, must_flip in face_adjacency[face]:
                        expected = flips[face] != must_flip
                        if neighbor in flips and flips[neighbor] != expected:
                            orientable = False
                            break
                        if neighbor not in flips:
                            flips[neighbor] = expected
                            pending.append(neighbor)
                    if not orientable:
                        break
                if not orientable:
                    break

        return closed, manifold, orientable, oriented
