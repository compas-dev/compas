from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import product

from compas.datastructures import HalfFace
from compas.datastructures import Mesh

from compas.files import OBJ

from compas.geometry import add_vectors
from compas.geometry import bestfit_plane
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import centroid_polyhedron
from compas.geometry import distance_point_point
from compas.geometry import length_vector
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import project_point_plane
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors

from compas.utilities import geometric_key
from compas.utilities import linspace

from .bbox import volmesh_bounding_box
from .transformations import volmesh_transform
from .transformations import volmesh_transformed


class VolMesh(HalfFace):
    """Geometric implementation of a face data structure for volumetric meshes.

    Parameters
    ----------
    name: str, optional
        The name of the data structure.
    default_vertex_attributes: dict, optional
        Default values for vertex attributes.
    default_edge_attributes: dict, optional
        Default values for edge attributes.
    default_face_attributes: dict, optional
        Default values for face attributes.
    default_cell_attributes: dict, optional
        Default values for cell attributes.

    """

    bounding_box = volmesh_bounding_box
    transform = volmesh_transform
    transformed = volmesh_transformed

    def __init__(
        self,
        name=None,
        default_vertex_attributes=None,
        default_edge_attributes=None,
        default_face_attributes=None,
        default_cell_attributes=None,
    ):
        _default_vertex_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        _default_edge_attributes = {}
        _default_face_attributes = {}
        _default_cell_attributes = {}
        if default_vertex_attributes:
            _default_vertex_attributes.update(default_vertex_attributes)
        if default_edge_attributes:
            _default_edge_attributes.update(default_edge_attributes)
        if default_face_attributes:
            _default_face_attributes.update(default_face_attributes)
        if default_cell_attributes:
            _default_cell_attributes.update(default_cell_attributes)
        super(VolMesh, self).__init__(
            name=name or "VolMesh",
            default_vertex_attributes=_default_vertex_attributes,
            default_edge_attributes=_default_edge_attributes,
            default_face_attributes=_default_face_attributes,
            default_cell_attributes=_default_cell_attributes,
        )

    def __str__(self):
        tpl = "<VolMesh with {} vertices, {} faces, {} cells, {} edges>"
        return tpl.format(
            self.number_of_vertices(),
            self.number_of_faces(),
            self.number_of_cells(),
            self.number_of_edges(),
        )

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # from/to
    # --------------------------------------------------------------------------

    @classmethod
    def from_meshgrid(cls, dx=10, dy=None, dz=None, nx=10, ny=None, nz=None):
        """Construct a volmesh from a 3D meshgrid.

        Parameters
        ----------
        dx : float, optional
            The size of the grid in the x direction.
        dy : float, optional
            The size of the grid in the y direction.
            Defaults to the value of `dx`.
        dz : float, optional
            The size of the grid in the z direction.
            Defaults to the value of `dx`.
        nx : int, optional
            The number of elements in the x direction.
        ny : int, optional
            The number of elements in the y direction.
            Defaults to the value of `nx`.
        nz : int, optional
            The number of elements in the z direction.
            Defaults to the value of `nx`.

        Returns
        -------
        :class:`~compas.datastructures.VolMesh`

        """
        dy = dy or dx
        dz = dz or dx
        ny = ny or nx
        nz = nz or nx

        vertices = [
            [x, y, z]
            for z, x, y in product(
                linspace(0, dz, nz + 1),
                linspace(0, dx, nx + 1),
                linspace(0, dy, ny + 1),
            )
        ]
        cells = []
        for k, i, j in product(range(nz), range(nx), range(ny)):
            a = k * ((nx + 1) * (ny + 1)) + i * (ny + 1) + j
            b = k * ((nx + 1) * (ny + 1)) + (i + 1) * (ny + 1) + j
            c = k * ((nx + 1) * (ny + 1)) + (i + 1) * (ny + 1) + j + 1
            d = k * ((nx + 1) * (ny + 1)) + i * (ny + 1) + j + 1
            aa = (k + 1) * ((nx + 1) * (ny + 1)) + i * (ny + 1) + j
            bb = (k + 1) * ((nx + 1) * (ny + 1)) + (i + 1) * (ny + 1) + j
            cc = (k + 1) * ((nx + 1) * (ny + 1)) + (i + 1) * (ny + 1) + j + 1
            dd = (k + 1) * ((nx + 1) * (ny + 1)) + i * (ny + 1) + j + 1
            bottom = [d, c, b, a]
            front = [a, b, bb, aa]
            right = [b, c, cc, bb]
            left = [a, aa, dd, d]
            back = [c, d, dd, cc]
            top = [aa, bb, cc, dd]
            cells.append([bottom, front, left, back, right, top])

        return cls.from_vertices_and_cells(vertices, cells)

    @classmethod
    def from_obj(cls, filepath, precision=None):
        """Construct a volmesh object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : path string | file-like object | URL string
            A path, a file-like object or a URL pointing to a file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        :class:`~compas.datastructures.VolMesh`
            A volmesh object.

        """
        obj = OBJ(filepath, precision)
        vertices = obj.parser.vertices
        faces = obj.parser.faces
        groups = obj.parser.groups
        cells = []
        for name in groups:
            group = groups[name]
            cell = []
            for item in group:
                if item[0] != "f":
                    continue
                face = faces[item[1]]
                cell.append(face)
            cells.append(cell)
        return cls.from_vertices_and_cells(vertices, cells)

    def to_obj(self, filepath, precision=None, **kwargs):
        """Write the volmesh to an OBJ file.

        Parameters
        ----------
        filepath : path string | file-like object
            A path or a file-like object pointing to a file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.
        unweld : bool, optional
            If True, all faces have their own unique vertices.
            If False, vertices are shared between faces if this is also the case in the mesh.
            Default is False.

        Returns
        -------
        None

        Warnings
        --------
        This function only writes geometric data about the vertices and
        the faces to the file.

        """
        obj = OBJ(filepath, precision=precision)
        obj.write(self, **kwargs)

    @classmethod
    def from_vertices_and_cells(cls, vertices, cells):
        """Construct a volmesh object from vertices and cells.

        Parameters
        ----------
        vertices : list[list[float]]
            Ordered list of vertices, represented by their XYZ coordinates.
        cells : list[list[list[int]]]
            List of cells defined by their faces.

        Returns
        -------
        :class:`~compas.datastructures.VolMesh`
            A volmesh object.

        """
        volmesh = cls()
        for x, y, z in vertices:
            volmesh.add_vertex(x=x, y=y, z=z)
        for cell in cells:
            volmesh.add_cell(cell)
        return volmesh

    def to_vertices_and_cells(self):
        """Return the vertices and cells of a volmesh.

        Returns
        -------
        list[list[float]]
            A list of vertices, represented by their XYZ coordinates.
        list[list[list[int]]]
            A list of cells, with each cell a list of faces, and each face a list of vertex indices.

        """
        vertex_index = self.vertex_index()
        vertices = [self.vertex_coordinates(vertex) for vertex in self.vertices()]
        cells = []
        for cell in self.cell:
            faces = [
                [vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in self.cell_faces(cell)
            ]
            cells.append(faces)
        return vertices, cells

    def cell_to_mesh(self, cell):
        """Construct a mesh object from from a cell of a volmesh.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`
            A mesh object.

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Mesh.from_vertices_and_faces(vertices, faces)

    def cell_to_vertices_and_faces(self, cell):
        """Return the vertices and faces of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list[list[float]]
            A list of vertices, represented by their XYZ coordinates,
        list[list[int]]
            A list of faces, with each face a list of vertex indices.

        """
        vertices = self.cell_vertices(cell)
        faces = self.cell_faces(cell)
        vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
        vertices = [self.vertex_coordinates(vertex) for vertex in vertices]
        faces = [[vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in faces]
        return vertices, faces

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def vertex_gkey(self, precision=None):
        """Returns a dictionary that maps vertex dictionary keys to the corresponding
        *geometric key* up to a certain precision.

        Parameters
        ----------
        precision : str, optional
            The float precision specifier used in string formatting.

        Returns
        -------
        dict[int, str]
            A dictionary of vertex-geometric key pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {vertex: gkey(xyz(vertex), precision) for vertex in self.vertices()}

    def gkey_vertex(self, precision=None):
        """Returns a dictionary that maps *geometric keys* of a certain precision
        to the keys of the corresponding vertices.

        Parameters
        ----------
        precision : str, optional
            The float precision specifier used in string formatting.

        Returns
        -------
        dict[str, int]
            A dictionary of geometric key-vertex pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {gkey(xyz(vertex), precision): vertex for vertex in self.vertices()}

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # volmesh geometry
    # --------------------------------------------------------------------------

    def centroid(self):
        """Compute the centroid of the volmesh.

        Returns
        -------
        list[float]
            The coordinates of the centroid.

        """
        return centroid_points([self.vertex_coordinates(vertex) for vertex in self.vertices()])

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, vertex, axes="xyz"):
        """Return the coordinates of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list[float]
            Coordinates of the vertex.

        """
        return [self._vertex[vertex][axis] for axis in axes]

    def vertex_laplacian(self, vertex):
        """Compute the vector from a vertex to the centroid of its neighbors.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[float]
            The components of the vector.

        """
        c = self.vertex_neighborhood_centroid(vertex)
        p = self.vertex_coordinates(vertex)
        return subtract_vectors(c, p)

    def vertex_neighborhood_centroid(self, vertex):
        """Compute the centroid of the neighbors of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[float]
            The coordinates of the centroid.

        """
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.vertex_neighbors(vertex)])

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, edge, axes="xyz"):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.
        axes : str, optional
            The axes along which the coordinates should be included.

        Returns
        -------
        list[float]
            The coordinates of the start point.
        list[float]
            The coordinates of the end point.

        """
        u, v = edge
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_length(self, edge):
        """Return the length of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        float
            The length of the edge.

        """
        a, b = self.edge_coordinates(edge)
        return distance_point_point(a, b)

    def edge_vector(self, edge):
        """Return the vector of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        list[float]
            The vector from u to v.

        """
        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return ab

    def edge_point(self, edge, t=0.5):
        """Return the location of a point along an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.
        t : float, optional
            The location of the point on the edge.
            If the value of `t` is outside the range 0-1, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        list[float]
            The XYZ coordinates of the point.

        """
        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return add_vectors(a, scale_vector(ab, t))

    def edge_direction(self, edge):
        """Return the direction vector of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        list[float]
            The direction vector of the edge.

        """
        return normalize_vector(self.edge_vector(edge))

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    def face_vertices(self, face):
        """The vertices of a face.

        Parameters
        ----------
        halfface : int
            The identifier of the face.

        Returns
        -------
        list[int]
            Ordered vertex identifiers.

        """
        return self.halfface_vertices(face)

    def face_coordinates(self, face, axes="xyz"):
        """Compute the coordinates of the vertices of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list[list[float]]
            The coordinates of the vertices of the face.

        """
        return [self.vertex_coordinates(vertex, axes=axes) for vertex in self.face_vertices(face)]

    def face_normal(self, face, unitized=True):
        """Compute the oriented normal of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.
        unitized : bool, optional
            If True, unitize the normal vector.

        Returns
        -------
        list[float]
            The components of the normal vector.

        """
        return normal_polygon(self.face_coordinates(face), unitized=unitized)

    def face_centroid(self, face):
        """Compute the location of the centroid of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list[float]
            The coordinates of the centroid.

        """
        return centroid_points(self.face_coordinates(face))

    def face_center(self, face):
        """Compute the location of the center of mass of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list[float]
            The coordinates of the center of mass.

        """
        return centroid_polygon(self.face_coordinates(face))

    def face_area(self, face):
        """Compute the oriented area of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        float
            The non-oriented area of the face.

        """
        return length_vector(self.face_normal(face, unitized=False))

    def face_flatness(self, face, maxdev=0.02):
        """Compute the flatness of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        float
            The flatness.

        Note
        ----
        compas.geometry.mesh_flatness function currently only works for quadrilateral faces.
        This function uses the distance between each face vertex and its projected point
        on the best-fit plane of the face as the flatness metric.

        """
        deviation = 0
        polygon = self.face_coordinates(face)
        plane = bestfit_plane(polygon)
        for pt in polygon:
            pt_proj = project_point_plane(pt, plane)
            dev = distance_point_point(pt, pt_proj)
            if dev > deviation:
                deviation = dev
        return deviation

    def face_aspect_ratio(self, face):
        """Face aspect ratio as the ratio between the lengths of the maximum and minimum face edges.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        float
            The aspect ratio.

        References
        ----------
        .. [1] Wikipedia. *Types of mesh*.
               Available at: https://en.wikipedia.org/wiki/Types_of_mesh.

        """
        face_edge_lengths = [self.edge_length(edge) for edge in self.face_halfedges(face)]
        return max(face_edge_lengths) / min(face_edge_lengths)

    halfface_area = face_area
    halfface_centroid = face_centroid
    halfface_center = face_center
    halfface_coordinates = face_coordinates
    halfface_flatness = face_flatness
    halfface_normal = face_normal
    halfface_aspect_ratio = face_aspect_ratio

    # --------------------------------------------------------------------------
    # cell geometry
    # --------------------------------------------------------------------------

    def cell_centroid(self, cell):
        """Compute the location of the centroid of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        list[float]
            The coordinates of the centroid.

        """
        vertices = self.cell_vertices(cell)
        return centroid_points([self.vertex_coordinates(vertex) for vertex in vertices])

    def cell_center(self, cell):
        """Compute the location of the center of mass of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        list[float]
            The coordinates of the center of mass.

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return centroid_polyhedron((vertices, faces))

    def cell_vertex_normal(self, cell, vertex):
        """Return the normal vector at the vertex of a boundary cell as the weighted average of the
        normals of the neighboring faces.

        Parameters
        ----------
        cell : int
            The identifier of the vertex of the cell.
        vertex : int
            The identifier of the vertex of the cell.

        Returns
        -------
        list[float]
            The components of the normal vector.

        """
        cell_faces = self.cell_faces(cell)
        vectors = [self.face_normal(face) for face in self.vertex_faces(vertex) if face in cell_faces]
        return normalize_vector(centroid_points(vectors))
