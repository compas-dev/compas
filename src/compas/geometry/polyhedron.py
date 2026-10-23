from collections.abc import Iterator
from collections.abc import Sequence
from math import sqrt
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import PolygonalSurface
from compas.geometry import Transformation
from compas.geometry import centroid_polyhedron
from compas.geometry import transform_points
from compas.geometry import volume_polyhedron
from compas.tolerance import TOL

from ._typing import PlaneType
from .geometry import Geometry

if TYPE_CHECKING:
    from compas.datastructures import Mesh
    from compas.geometry import Box
    from compas.geometry import Tessellation


def tetrahedron():
    faces = [[0, 1, 2], [0, 3, 1], [0, 2, 3], [1, 3, 2]]
    vertices = []
    L = 2.0
    r = L * sqrt(6) / 4.0
    c = 1.0 / r
    for i in (-1, 1):
        i *= c
        vertices.append([i, 0.0, -c / sqrt(2)])
        vertices.append([0.0, i, +c / sqrt(2)])
    return vertices, faces


def hexahedron():
    faces = [
        [0, 3, 2, 1],
        [0, 1, 7, 6],
        [0, 6, 5, 3],
        [4, 2, 3, 5],
        [4, 7, 1, 2],
        [4, 5, 6, 7],
    ]
    vertices = []
    L = 1.0
    r = L * sqrt(3) / 2.0
    c = 1.0 / r
    for i in -1.0, +1.0:
        i *= c
        vertices.append([+i, +i, +i])
        vertices.append([-i, +i, +i])
        vertices.append([-i, -i, +i])
        vertices.append([+i, -i, +i])
    return vertices, faces


def octahedron():
    faces = [
        [0, 1, 5],
        [1, 3, 5],
        [3, 4, 5],
        [0, 5, 4],
        [0, 2, 1],
        [1, 2, 3],
        [3, 2, 4],
        [0, 4, 2],
    ]
    vertices = []
    L = sqrt(2)
    r = L * sqrt(2) / 2.0
    c = 1.0 / r
    for i in -1.0, +1.0:
        i *= c
        vertices.append([i, 0.0, 0.0])
        vertices.append([0.0, i, 0.0])
        vertices.append([0.0, 0.0, i])
    return vertices, faces


def dodecahedron():
    phi = 0.5 * (1 + sqrt(5))
    vertices = []
    faces = [
        [0, 13, 11, 1, 3],
        [0, 3, 2, 8, 10],
        [0, 10, 18, 12, 13],
        [1, 4, 7, 2, 3],
        [1, 11, 14, 5, 4],
        [2, 7, 9, 6, 8],
        [5, 15, 9, 7, 4],
        [5, 14, 17, 19, 15],
        [6, 16, 18, 10, 8],
        [6, 9, 15, 19, 16],
        [12, 17, 14, 11, 13],
        [12, 18, 16, 19, 17],
    ]
    L = 2.0 / phi
    r = L * phi * sqrt(3) / 2.0
    c = 1.0 / r
    for i in -1, +1:
        i *= c
        for j in -1, +1:
            j *= c
            vertices.append([0, i / phi, j * phi])
            vertices.append([i / phi, j * phi, 0])
            vertices.append([i * phi, 0, j / phi])
            for k in -1, +1:
                k *= c
                vertices.append([i * 1.0, j * 1.0, k * 1.0])
    return vertices, faces


def icosahedron():
    phi = (1 + sqrt(5)) / 2.0
    vertices = [
        (-1, phi, 0),
        (1, phi, 0),
        (-1, -phi, 0),
        (1, -phi, 0),
        (0, -1, phi),
        (0, 1, phi),
        (0, -1, -phi),
        (0, 1, -phi),
        (phi, 0, -1),
        (phi, 0, 1),
        (-phi, 0, -1),
        (-phi, 0, 1),
    ]
    faces = [
        # 5 faces around point 0
        [0, 11, 5],
        [0, 5, 1],
        [0, 1, 7],
        [0, 7, 10],
        [0, 10, 11],
        # Adjacent faces
        [1, 5, 9],
        [5, 11, 4],
        [11, 10, 2],
        [10, 7, 6],
        [7, 1, 8],
        # 5 faces around 3
        [3, 9, 4],
        [3, 4, 2],
        [3, 2, 6],
        [3, 6, 8],
        [3, 8, 9],
        # Adjacent faces
        [4, 9, 5],
        [2, 4, 11],
        [6, 2, 10],
        [8, 6, 7],
        [9, 8, 1],
    ]
    return vertices, faces


class Polyhedron(Geometry):
    """A closed polygonal solid defined by its boundary vertices and faces.

    Parameters
    ----------
    vertices
        The point locations of the vertices of the polyhedron.
    faces
        The faces as a list of index lists.
    name
        The name of the polyhedron.

    Notes
    -----
    The boundary must be closed, manifold, consistently oriented, and composed
    of planar faces. Inward-facing boundaries are automatically reversed.

    """

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict:
        return {"vertices": self.vertices, "faces": self.faces}

    @classmethod
    def __from_data__(cls, data: dict) -> Self:
        return cls(data["vertices"], data["faces"])

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, vertices: CoordinatesType, faces: list[list[int]], name: str | None = None) -> None:
        super().__init__(name=name)
        self._boundary = PolygonalSurface(vertices, faces)
        self._volume = 0.0
        self._validate_boundary()

    def __repr__(self) -> str:
        return "{0}(vertices={1!r}, faces={2!r})".format(
            type(self).__name__,
            self.vertices,
            self.faces,
        )

    def __str__(self) -> str:
        return "{0}(vertices={1}, faces={2})".format(
            type(self).__name__,
            [[TOL.format_number(num) for num in vertice] for vertice in self.vertices],
            self.faces,
        )

    def __len__(self) -> int:
        return 2

    def __getitem__(self, key: int) -> list[list[float]] | list[list[int]]:
        if key == 0:
            return self.vertices
        elif key == 1:
            return self.faces
        else:
            raise KeyError

    def __iter__(self) -> Iterator[list[list[float]] | list[list[int]]]:
        return iter([self.vertices, self.faces])

    def __add__(self, other: "Polyhedron") -> Self:
        from compas.geometry import boolean_union_mesh_mesh

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_union_mesh_mesh(A, B)
        return type(self)(V, F)

    def __sub__(self, other: "Polyhedron") -> Self:
        from compas.geometry import boolean_difference_mesh_mesh

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_difference_mesh_mesh(A, B)
        return type(self)(V, F)

    def __and__(self, other: "Polyhedron") -> Self:
        from compas.geometry import boolean_intersection_mesh_mesh

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_intersection_mesh_mesh(A, B)
        return type(self)(V, F)

    def __or__(self, other: "Polyhedron") -> Self:
        return self.__add__(other)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def boundary(self) -> PolygonalSurface:
        """The polygonal boundary of the solid."""
        return self._boundary

    @property
    def vertices(self) -> list[list[float]]:
        """The boundary vertex coordinates."""
        return self.boundary.vertices

    @property
    def faces(self) -> list[list[int]]:
        """The oriented planar boundary faces."""
        return self.boundary.faces

    @property
    def edges(self) -> list[tuple[int, int]]:
        """The unique boundary edges."""
        return self.boundary.edges

    @property
    def points(self) -> list[Point]:
        """The boundary vertices as points."""
        return self.boundary.points

    @property
    def lines(self) -> list[Line]:
        """The boundary edges as lines."""
        return self.boundary.lines

    @property
    def polygons(self) -> list[Polygon]:
        """The boundary faces as polygons."""
        return self.boundary.polygons

    @property
    def triangles(self) -> list[list[int]]:
        """A triangulation of the boundary faces."""
        return self.boundary.triangles

    @property
    def planes(self) -> list[Plane]:
        """The planes of the boundary faces."""
        return [polygon.plane for polygon in self.polygons]

    @property
    def is_convex(self) -> bool:
        """Whether the polyhedron is convex."""
        for plane in self.planes:
            for vertex in self.vertices:
                if plane.normal.dot(plane.point - vertex) < 0:
                    return False
        return True

    @property
    def is_closed(self) -> bool:
        """Whether the boundary is closed, which is always `True`."""
        return True

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_platonicsolid(cls, f: int) -> Self:
        """Construct a polyhedron from one of the platonic solids.

        A Platonic solid is a regular, convex polyhedron. It is constructed by
        congruent regular polygonal faces with the same number of faces meeting
        at each vertex.[^polyhedron-platonic-solids]

        Parameters
        ----------
        f
            The number of faces: `4`, `6`, `8`, `12`, or `20`.

        Returns
        -------
        Self
            The constructed polyhedron.

        Examples
        --------
        >>> solid = Polyhedron.from_platonicsolid(6)
        >>> len(solid.faces)
        6

        References
        ----------
        [^polyhedron-platonic-solids]: Wikipedia. [*Platonic solid*](https://en.wikipedia.org/wiki/Platonic_solid).

        """
        if f == 4:
            vertices, faces = tetrahedron()
        elif f == 6:
            vertices, faces = hexahedron()
        elif f == 8:
            vertices, faces = octahedron()
        elif f == 12:
            vertices, faces = dodecahedron()
        elif f == 20:
            vertices, faces = icosahedron()
        else:
            raise ValueError("The number of sides of a platonic solid must be one of: 4, 6, 8, 12, 20.")
        return cls(vertices, faces)

    @classmethod
    def from_halfspaces(cls, halfspaces: Sequence[Sequence[float]], interior_point: CoordinateType) -> Self:
        """Construct a polyhedron from its half-spaces and one interior point.

        Parameters
        ----------
        halfspaces
            The coefficients of the half-space equations in normal form.
        interior_point
            A point on the interior.

        Returns
        -------
        Self

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> left = Plane([-1, 0, 0], [-1, 0, 0])
        >>> right = Plane([+1, 0, 0], [+1, 0, 0])
        >>> top = Plane([0, 0, +1], [0, 0, +1])
        >>> bottom = Plane([0, 0, -1], [0, 0, -1])
        >>> front = Plane([0, -1, 0], [0, -1, 0])
        >>> back = Plane([0, +1, 0], [0, +1, 0])

        >>> import numpy as np
        >>> halfspaces = np.array([left.abcd, right.abcd, top.abcd, bottom.abcd, front.abcd, back.abcd], dtype=float)
        >>> interior = np.array([0, 0, 0], dtype=float)

        >>> p = Polyhedron.from_halfspaces(halfspaces, interior)

        """
        from itertools import combinations

        from numpy import asarray  # type: ignore
        from scipy.spatial import ConvexHull  # type: ignore
        from scipy.spatial import HalfspaceIntersection  # type: ignore

        from compas.datastructures import Mesh
        from compas.linalg.vectors import cross_vectors
        from compas.linalg.vectors import dot_vectors
        from compas.linalg.vectors import length_vector

        halfspaces_array = asarray(halfspaces, dtype=float)
        interior_point_array = asarray(interior_point, dtype=float)
        hsi = HalfspaceIntersection(halfspaces_array, interior_point_array)
        hull = ConvexHull(hsi.intersections)
        mesh = Mesh.from_vertices_and_faces([hsi.intersections[i] for i in hull.vertices], hull.simplices.tolist())
        mesh.unify_cycles()
        to_merge = []
        for a, b in combinations(mesh.faces(), 2):
            na = mesh.face_normal(a)
            nb = mesh.face_normal(b)
            if dot_vectors(na, nb) >= 1:
                if length_vector(cross_vectors(na, nb)) < 1e-6:
                    to_merge.append([a, b])
        for faces in to_merge:
            mesh.merge_faces(faces)
        vertices, faces = mesh.to_vertices_and_faces()
        return cls(vertices, faces)

    @classmethod
    def from_planes(cls, planes: Sequence[PlaneType]) -> Self:
        """Construct a polyhedron from intersecting planes.

        Parameters
        ----------
        planes
            The intersecting planes.

        Returns
        -------
        Self

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> left = Plane([-1, 0, 0], [-1, 0, 0])
        >>> right = Plane([+1, 0, 0], [+1, 0, 0])
        >>> top = Plane([0, 0, +1], [0, 0, +1])
        >>> bottom = Plane([0, 0, -1], [0, 0, -1])
        >>> front = Plane([0, -1, 0], [0, -1, 0])
        >>> back = Plane([0, +1, 0], [0, +1, 0])
        >>> p = Polyhedron.from_planes([left, right, top, bottom, front, back])

        """
        from compas.geometry import Plane
        from compas.geometry import centroid_points

        planes = [Plane(point, normal) for point, normal in planes]
        interior = centroid_points([plane.point for plane in planes])
        return cls.from_halfspaces([plane.abcd for plane in planes], interior)

    @classmethod
    def from_convex_hull(cls, points: CoordinatesType) -> Self:
        """Construct a polyhedron from the convex hull of a set of points.

        Parameters
        ----------
        points
            The XYZ coordinates of the points.

        Returns
        -------
        Self

        Examples
        --------
        >>> from compas.geometry import Polyhedron
        >>> points = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
        >>> p = Polyhedron.from_convex_hull(points)  # doctest: +SKIP

        """
        from compas.geometry import convex_hull
        from compas.topology import unify_cycles

        indices, faces = convex_hull(points)
        index = {vertex: local for local, vertex in enumerate(indices)}
        vertices = [points[vertex] for vertex in indices]
        remapped = [[index[vertex] for vertex in face] for face in faces]
        unify_cycles(vertices, remapped)
        return cls(vertices, remapped)

    # =============================================================================
    # Conversions
    # =============================================================================

    def tessellated(self) -> "Tessellation":
        """Return a triangular tessellation of the polyhedron boundary.

        Returns
        -------
        Tessellation
            The indexed triangular representation for visualization.

        """
        return self.boundary.tessellated()

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
        return self.boundary.to_vertices_and_faces(triangulated=triangulated)

    def to_mesh(self) -> "Mesh":
        """Return a mesh representation of the polyhedron.

        Returns
        -------
        Mesh
            A mesh object.

        """
        return self.boundary.to_mesh()

    # =============================================================================
    # Transformations
    # =============================================================================

    def transform(self, transformation: Transformation) -> None:
        """Transform the polyhedron.

        Parameters
        ----------
        transformation

        """
        vertices = transform_points(self.vertices, transformation)
        faces = self.faces
        volume = volume_polyhedron((vertices, faces))
        if TOL.is_zero(volume):
            raise ValueError("A transformation should not collapse a polyhedron.")
        if volume < 0:
            faces = [face[::-1] for face in faces]
            volume = -volume
        self._boundary = PolygonalSurface(vertices, faces)
        self._volume = volume

    # =============================================================================
    # Methods
    # =============================================================================

    def aabb(self) -> "Box":
        """Compute the axis-aligned bounding box.

        Returns
        -------
        Box

        """
        return self.boundary.aabb()

    def obb(self) -> "Box":
        """Compute the oriented bounding box.

        Returns
        -------
        Box

        """
        return self.boundary.obb()

    def area(self) -> float:
        """Compute the area of the polygonal boundary."""
        return sum(polygon.area() for polygon in self.polygons)

    def volume(self) -> float:
        """Compute the volume enclosed by the polyhedron."""
        return self._volume

    def centroid(self) -> Point:
        """Compute the center of mass of the polyhedron."""
        vertices, faces = self.to_vertices_and_faces()
        centroid_vertices: list[Sequence[float]] = [vertex for vertex in vertices]
        x, y, z = centroid_polyhedron((centroid_vertices, faces))
        return Point(x, y, z)

    def boolean_union(self, other: "Polyhedron") -> Self:
        """Compute the boolean union of this polyhedron and another.

        Parameters
        ----------
        other
            The polyhedron to add.

        Returns
        -------
        Self
            The resulting polyhedron.

        Examples
        --------
        >>> from compas.geometry import Box, Polyhedron, Sphere
        >>> A = Polyhedron(*Box(2).tessellated().to_vertices_and_triangles())
        >>> B = Polyhedron(*Sphere.from_point_and_radius([1, 1, 1], 1.0).tessellated().to_vertices_and_triangles())
        >>> C = A.boolean_union(B)  # doctest: +SKIP

        """
        from compas.geometry import boolean_union_mesh_mesh

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_union_mesh_mesh(A, B)

        return type(self)(V, F)

    def boolean_difference(self, other: "Polyhedron") -> Self:
        """Compute the boolean difference of this polyhedron and another.

        Parameters
        ----------
        other
            The polyhedron to subtract.

        Returns
        -------
        Self
            The resulting polyhedron.

        Examples
        --------
        >>> from compas.geometry import Box, Polyhedron, Sphere
        >>> A = Polyhedron(*Box(2).tessellated().to_vertices_and_triangles())
        >>> B = Polyhedron(*Sphere.from_point_and_radius([1, 1, 1], 1.0).tessellated().to_vertices_and_triangles())
        >>> C = A.boolean_difference(B)  # doctest: +SKIP

        """
        from compas.geometry import boolean_difference_mesh_mesh

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_difference_mesh_mesh(A, B)

        return type(self)(V, F)

    def boolean_intersection(self, other: "Polyhedron") -> Self:
        """Compute the boolean intersection of this polyhedron and another.

        Parameters
        ----------
        other
            The polyhedron to intersect with.

        Returns
        -------
        Self
            The resulting polyhedron.

        Examples
        --------
        >>> from compas.geometry import Box, Polyhedron, Sphere
        >>> A = Polyhedron(*Box(2).tessellated().to_vertices_and_triangles())
        >>> B = Polyhedron(*Sphere.from_point_and_radius([1, 1, 1], 1.0).tessellated().to_vertices_and_triangles())
        >>> C = A.boolean_intersection(B)  # doctest: +SKIP

        """
        from compas.geometry import boolean_intersection_mesh_mesh

        A = self.to_vertices_and_faces(triangulated=True)
        B = other.to_vertices_and_faces(triangulated=True)
        V, F = boolean_intersection_mesh_mesh(A, B)

        return type(self)(V, F)

    # =============================================================================
    # Private helpers
    # =============================================================================

    def _validate_boundary(self) -> None:
        if len(self.vertices) < 4:
            raise ValueError("A polyhedron requires at least four vertices.")
        closed, manifold, _, oriented = self.boundary._analyze_topology()
        if not closed:
            raise ValueError("The boundary of a polyhedron should be closed.")
        if not manifold:
            raise ValueError("The boundary of a polyhedron should be manifold.")
        if not oriented:
            raise ValueError("The boundary faces of a polyhedron should be consistently oriented.")
        if not all(polygon.is_planar for polygon in self.polygons):
            raise ValueError("The boundary faces of a polyhedron should be planar.")

        vertices, faces = self.to_vertices_and_faces()
        volume = volume_polyhedron((vertices, faces))
        if TOL.is_zero(volume):
            raise ValueError("A polyhedron should enclose a nonzero volume.")
        if volume < 0:
            self.boundary.faces = [face[::-1] for face in self.faces]
            volume = -volume
        self._volume = volume
