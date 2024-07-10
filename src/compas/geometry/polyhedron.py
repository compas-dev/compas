from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import sqrt

from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import transform_points
from compas.itertools import pairwise
from compas.tolerance import TOL

from .geometry import Geometry


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
    """A polyhedron is a geometric object defined by its vertices and faces.

    Parameters
    ----------
    vertices : list[[float, float, float] | :class:`compas.geometry.Point`]
        The point locations of the vertices of the polyhedron.
    faces : list[list[int]]
        The faces as a list of index lists.
    name : str, optional
        The name of the polyhedron.

    Attributes
    ----------
    vertices : list[list[float]]
        The XYZ coordinates of the vertices of the polyhedron.
    faces : list[list[int]]
        The faces of the polyhedron defined as lists of vertex indices.
    edges : list[tuple[int, int]], read-only
        The edges of the polyhedron as vertex index pairs.

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "vertices": {
                "type": "array",
                "minItems": 4,
                "items": {
                    "type": "array",
                    "minItems": 3,
                    "maxItems": 3,
                    "items": {"type": "number"},
                },
            },
            "faces": {
                "type": "array",
                "minItems": 4,
                "items": {
                    "type": "array",
                    "minItems": 3,
                    "items": {"type": "integer", "minimum": 0},
                },
            },
        },
        "required": ["vertices", "faces"],
    }

    @property
    def __data__(self):
        return {"vertices": self.vertices, "faces": self.faces}

    def __init__(self, vertices, faces, name=None):
        super(Polyhedron, self).__init__(name=name)
        self._vertices = None
        self._faces = None
        self.vertices = vertices
        self.faces = faces

    def __repr__(self):
        return "{0}(vertices={1!r}, faces={2!r})".format(
            type(self).__name__,
            self.vertices,
            self.faces,
        )

    def __str__(self):
        return "{0}(vertices={1}, faces={2})".format(
            type(self).__name__,
            [[TOL.format_number(num) for num in vertice] for vertice in self.vertices],
            self.faces,
        )

    def __len__(self):
        return 2

    def __getitem__(self, key):
        if key == 0:
            return self.vertices
        elif key == 1:
            return self.faces
        else:
            raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.vertices = value
        elif key == 1:
            self.faces = value
        else:
            raise KeyError

    def __iter__(self):
        return iter([self.vertices, self.faces])

    def __add__(self, other):
        from compas.geometry import boolean_union_mesh_mesh

        A = self.vertices, self.faces
        B = other.vertices, other.faces
        V, F = boolean_union_mesh_mesh(A, B)  # type: ignore
        return Polyhedron(V, F)

    def __sub__(self, other):
        from compas.geometry import boolean_difference_mesh_mesh

        A = self.vertices, self.faces
        B = other.vertices, other.faces
        V, F = boolean_difference_mesh_mesh(A, B)  # type: ignore
        return Polyhedron(V, F)

    def __and__(self, other):
        from compas.geometry import boolean_intersection_mesh_mesh

        A = self.vertices, self.faces
        B = other.vertices, other.faces
        V, F = boolean_intersection_mesh_mesh(A, B)  # type: ignore
        return Polyhedron(V, F)

    def __or__(self, other):
        return self.__add__(other)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def vertices(self):
        if self._vertices is None:
            self._vertices = []
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def faces(self):
        if self._faces is None:
            self._faces = []
        return self._faces

    @faces.setter
    def faces(self, faces):
        self._faces = faces

    @property
    def edges(self):
        seen = set()
        for face in self.faces:
            for u, v in pairwise(face + face[:1]):
                if (u, v) not in seen:
                    seen.add((u, v))
                    seen.add((v, u))
                    yield u, v

    @property
    def points(self):
        return [Point(x, y, z) for x, y, z in self.vertices]

    @property
    def lines(self):
        return [Line(self.vertices[u], self.vertices[v]) for u, v in self.edges]

    @property
    def polygons(self):
        return [Polygon([self.vertices[index] for index in face]) for face in self.faces]

    @property
    def planes(self):
        return [polygon.plane for polygon in self.polygons]

    @property
    def is_convex(self):
        for plane in self.planes:
            for vertex in self.vertices:
                if plane.normal.dot(plane.point - vertex) < 0:
                    return False
        return True

    @property
    def area(self):
        """Compute the area of the polyhedron.

        Returns
        -------
        float
            The area of the polyhedron.

        """
        return sum(polygon.area for polygon in self.polygons)

    @property
    def volume(self):
        """Compute the volume of the polyhedron."""
        raise NotImplementedError

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_platonicsolid(cls, f):
        """Construct a polyhedron from one of the platonic solids.

        A Platonic solid is a regular, convex polyhedron. It is constructed by
        congruent regular polygonal faces with the same number of faces meeting
        at each vertex [1]_.

        Parameters
        ----------
        f : {4, 6, 8, 12, 20}

        Returns
        -------
        :class:`compas.geometry.Polyhedron`
            The constructed polyhedron.

        References
        ----------
        .. [1] Wikipedia. *Platonic solids*.
            Available at: https://en.wikipedia.org/wiki/Platonic_solid.

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
        solid = cls(vertices, faces)
        return solid

    @classmethod
    def from_halfspaces(cls, halfspaces, interior_point):
        """Construct a polyhedron from its half-spaces and one interior point.

        Parameters
        ----------
        halfspaces : array-like
            The coefficients of the hgalfspace equations in normal form.
        interior_point : array-like
            A point on the interior.

        Returns
        -------
        :class:`compas.geometry.Polyhedron`

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

        from numpy import asarray
        from scipy.spatial import ConvexHull  # type: ignore
        from scipy.spatial import HalfspaceIntersection  # type: ignore

        from compas.datastructures import Mesh
        from compas.geometry import cross_vectors
        from compas.geometry import dot_vectors
        from compas.geometry import length_vector

        halfspaces = asarray(halfspaces, dtype=float)
        interior_point = asarray(interior_point, dtype=float)
        hsi = HalfspaceIntersection(halfspaces, interior_point)
        hull = ConvexHull(hsi.intersections)
        mesh = Mesh.from_vertices_and_faces([hsi.intersections[i] for i in hull.vertices], hull.simplices)
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
    def from_planes(cls, planes):
        """Construct a polyhedron from intersecting planes.

        Parameters
        ----------
        planes : list[[point, normal] | :class:`compas.geometry.Plane`]

        Returns
        -------
        :class:`compas.geometry.Polyhedron`

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
    def from_convex_hull(cls, points):
        """Construct a polyhedron from the convex hull of a set of points.

        Parameters
        ----------
        points : list[point]
            The XYZ coordinates of the points.

        Returns
        -------
        :class:`compas.geometry.Polyhedron`

        Examples
        --------
        >>> from compas.geometry import Polyhedron
        >>> points = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
        >>> p = Polyhedron.from_convex_hull(points)  # doctest: +SKIP

        """
        from compas.geometry import convex_hull_numpy

        vertices, faces = convex_hull_numpy(points)
        return cls(vertices, faces)

    # =============================================================================
    # Conversions
    # =============================================================================

    def to_vertices_and_faces(self):
        """Returns a list of vertices and faces.

        Returns
        -------
        tuple[list[float], list[int]
            A list of vertices and a list of faces.

        """
        return self.vertices, self.faces

    def to_mesh(self):
        """Returns a mesh representation of the polyhedron.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        from compas.datastructures import Mesh

        return Mesh.from_vertices_and_faces(self.vertices, self.faces)

    # =============================================================================
    # Transformations
    # =============================================================================

    def transform(self, transformation):
        """Transform the polyhedron.

        Parameters
        ----------
        transformation : :class:`compas.geometry.Transformation`

        Returns
        -------
        None

        """
        self.vertices = transform_points(self.vertices, transformation)

    # =============================================================================
    # Methods
    # =============================================================================

    def is_closed(self):
        """Verify that the polyhedron forms a closed surface.

        Returns
        -------
        bool
            True if the polyhedron is closed.
            False otherwise.

        """
        mesh = self.to_mesh()
        return mesh.is_closed()

    def boolean_union(self, other):
        """Compute the boolean union of this polyhedron and another.

        Parameters
        ----------
        other : :class:`compas.geometry.Polyhedron`
            The polyhedron to add.

        Returns
        -------
        :class:`compas.geometry.Polyhedron`
            The resulting polyhedron.

        Examples
        --------
        >>> from compas.geometry import Box, Sphere
        >>> A = Box(2).to_polyhedron(triangulated=True)
        >>> B = Sphere(point=[1, 1, 1], radius=1.0).to_polyhedron(triangulated=True)
        >>> C = A.boolean_union(B)

        """
        from compas.geometry import boolean_union_mesh_mesh

        A = self.vertices, self.faces
        B = other.vertices, other.faces
        V, F = boolean_union_mesh_mesh(A, B)  # type: ignore

        return Polyhedron(V, F)

    def boolean_difference(self, other):
        """Compute the boolean difference of this polyhedron and another.

        Parameters
        ----------
        other : :class:`compas.geometry.Polyhedron`
            The polyhedron to subtract.

        Returns
        -------
        :class:`compas.geometry.Polyhedron`
            The resulting polyhedron.

        Examples
        --------
        >>> from compas.geometry import Box, Sphere
        >>> A = Box(2).to_polyhedron(triangulated=True)
        >>> B = Sphere(point=[1, 1, 1], radius=1.0).to_polyhedron(triangulated=True)
        >>> C = A.boolean_difference(B)

        """
        from compas.geometry import boolean_difference_mesh_mesh

        A = self.vertices, self.faces
        B = other.vertices, other.faces
        V, F = boolean_difference_mesh_mesh(A, B)  # type: ignore

        return Polyhedron(V, F)

    def boolean_intersection(self, other):
        """Compute the boolean intersection of this polyhedron and another.

        Parameters
        ----------
        other : :class:`compas.geometry.Polyhedron`
            The polyhedron to intersect with.

        Returns
        -------
        :class:`compas.geometry.Polyhedron`
            The resulting polyhedron.

        Examples
        --------
        >>> from compas.geometry import Box, Sphere
        >>> A = Box(2).to_polyhedron(triangulated=True)
        >>> B = Sphere(point=[1, 1, 1], radius=1.0).to_polyhedron(triangulated=True)
        >>> C = A.boolean_intersection(B)

        """
        from compas.geometry import boolean_intersection_mesh_mesh

        A = self.vertices, self.faces
        B = other.vertices, other.faces
        V, F = boolean_intersection_mesh_mesh(A, B)  # type: ignore

        return Polyhedron(V, F)
