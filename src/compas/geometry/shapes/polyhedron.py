from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import sqrt
from compas.geometry import transform_points
from compas.geometry import centroid_polygon
from compas.utilities import pairwise

from ._shape import Shape


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


class Polyhedron(Shape):
    """A polyhedron is defined by its vertices and faces.

    Parameters
    ----------
    vertices : list[[float, float, float] | :class:`~compas.geometry.Point`]
        The point locations of the vertices of the polyhedron.
    faces : list[list[int]]
        The faces as a list of index lists.

    Attributes
    ----------
    vertices : list[list[float]]
        The XYZ coordinates of the vertices of the polyhedron.
    faces : list[list[int]]
        The faces of the polyhedron defined as lists of vertex indices.
    edges : list[tuple[int, int]], read-only
        The edges of the polyhedron as vertex index pairs.

    """

    __slots__ = ["_vertices", "_faces"]

    def __init__(self, vertices, faces, **kwargs):
        super(Polyhedron, self).__init__(**kwargs)
        self._vertices = None
        self._faces = None
        self.vertices = vertices
        self.faces = faces

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        import schema
        from compas.data import is_float3, is_sequence_of_int

        return schema.Schema(
            {
                "vertices": lambda items: all(is_float3(item) for item in items),
                "faces": lambda items: all(is_sequence_of_int(item) for item in items),
            }
        )

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        return "polyhedron"

    @property
    def data(self):
        """dict : Returns the data dictionary that represents the polyhedron."""
        return {"vertices": self.vertices, "faces": self.faces}

    @data.setter
    def data(self, data):
        self.vertices = data["vertices"]
        self.faces = data["faces"]

    @classmethod
    def from_data(cls, data):
        """Construct a polyhedron from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`~compas.geometry.Polyhedron`
            The constructed polyhedron.

        Examples
        --------
        >>> from compas.geometry import Polyhedron
        >>> p = Polyhedron.from_platonicsolid(4)
        >>> q = Polyhedron.from_data(p.data)

        """
        return cls(data["vertices"], data["faces"])

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self._vertices = vertices

    @property
    def faces(self):
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

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __repr__(self):
        return "<Polyhedron with {} vertices and {} faces>".format(len(self.vertices), len(self.faces))

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

    # ==========================================================================
    # constructors
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
        :class:`~compas.geometry.Polyhedron`
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
        :class:`~compas.geometry.Polyhedron`

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
        from scipy.spatial import HalfspaceIntersection, ConvexHull
        from compas.datastructures import Mesh, mesh_merge_faces
        from compas.geometry import length_vector, dot_vectors, cross_vectors

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
            mesh_merge_faces(mesh, faces)
        vertices, faces = mesh.to_vertices_and_faces()
        return cls(vertices, faces)

    @classmethod
    def from_planes(cls, planes):
        """Construct a polyhedron from intersecting planes.

        Parameters
        ----------
        planes : list[[point, normal] | :class:`~compas.geometry.Plane`]

        Returns
        -------
        :class:`~compas.geometry.Polyhedron`

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

    # ==========================================================================
    # methods
    # ==========================================================================

    def to_vertices_and_faces(self, triangulated=False):
        """Returns a list of vertices and faces.

        Parameters
        ----------
        triangulated: bool, optional
            If True, triangulate the faces.

        Returns
        -------
        list[list[float]]
            A list of vertex locations.
        list[list[int]]
            And a list of faces,
            with each face defined as a list of indices into the list of vertices.

        """
        if triangulated:
            vertices = self.vertices[:]
            faces = []
            for face in self.faces:
                if len(face) > 3:
                    centroid = centroid_polygon([vertices[index] for index in face])
                    index = len(vertices)
                    vertices.append(centroid)
                    for a, b in pairwise(face):
                        faces.append([a, b, index])
                else:
                    faces.append(face)
        else:
            vertices = self.vertices
            faces = self.faces
        return vertices, faces

    def is_closed(self):
        """Verify that the polyhedron forms a closed surface.

        Returns
        -------
        bool
            True if the polyhedron is closed.
            False otherwise.

        """
        from compas.datastructures import Mesh

        mesh = Mesh.from_vertices_and_faces(self.vertices, self.faces)
        return mesh.is_closed()

    def transform(self, transformation):
        """Transform the polyhedron.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`

        Returns
        -------
        None

        """
        self.vertices = transform_points(self.vertices, transformation)
