from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import product
from random import sample

import compas

if compas.PY2:
    from collections import Mapping  # type: ignore
else:
    from collections.abc import Mapping

from compas.datastructures import Mesh
from compas.datastructures.attributes import CellAttributeView
from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import FaceAttributeView
from compas.datastructures.attributes import VertexAttributeView
from compas.datastructures.datastructure import Datastructure
from compas.files import OBJ
from compas.geometry import Box
from compas.geometry import Line
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Vector
from compas.geometry import add_vectors
from compas.geometry import bestfit_plane
from compas.geometry import bounding_box
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import centroid_polyhedron
from compas.geometry import distance_point_point
from compas.geometry import length_vector
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import oriented_bounding_box
from compas.geometry import project_point_plane
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import transform_points
from compas.itertools import linspace
from compas.itertools import pairwise
from compas.tolerance import TOL


def uv_from_vertices(vertices):
    for i in range(-1, len(vertices) - 1):
        yield vertices[i], vertices[i + 1]


def uvw_from_vertices(vertices):
    for i in range(-2, len(vertices) - 2):
        yield vertices[i], vertices[i + 1], vertices[i + 2]


class VolMesh(Datastructure):
    """Geometric implementation of a face data structure for volumetric meshes.

    Parameters
    ----------
    default_vertex_attributes : dict, optional
        Default values for vertex attributes.
    default_edge_attributes : dict, optional
        Default values for edge attributes.
    default_face_attributes : dict, optional
        Default values for face attributes.
    default_cell_attributes : dict, optional
        Default values for cell attributes.
    name : str, optional
        The name of the volmesh.
    **kwargs : dict, optional
        Additional keyword arguments, which are stored in the attributes dict.

    Attributes
    ----------
    default_vertex_attributes : dict[str, Any]
        Default attributes of the vertices.
    default_edge_attributes : dict[str, Any]
        Default values for edge attributes.
    default_face_attributes : dict[str, Any]
        Default values for face attributes.
    default_cell_attributes : dict[str, Any]
        Default values for cell attributes.

    """

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "attributes": {"type": "object"},
            "default_vertex_attributes": {"type": "object"},
            "default_edge_attributes": {"type": "object"},
            "default_face_attributes": {"type": "object"},
            "default_cell_attributes": {"type": "object"},
            "vertex": {
                "type": "object",
                "patternProperties": {"^[0-9]+$": {"type": "object"}},
                "additionalProperties": False,
            },
            "cell": {
                "type": "object",
                "patternProperties": {
                    "^[0-9]+$": {
                        "type": "array",
                        "minItems": 4,
                        "items": {
                            "type": "array",
                            "minItems": 3,
                            "items": {"type": "integer", "minimum": 0},
                        },
                    }
                },
                "additionalProperties": False,
            },
            "edge_data": {
                "type": "object",
                "patternProperties": {"^\\([0-9]+, [0-9]+\\)$": {"type": "object"}},
                "additionalProperties": False,
            },
            "face_data": {
                "type": "object",
                "patternProperties": {"^\\([0-9]+(, [0-9]+){3, }\\)$": {"type": "object"}},
                "additionalProperties": False,
            },
            "cell_data": {
                "type": "object",
                "patternProperties": {"^[0-9]+$": {"type": "object"}},
                "additionalProperties": False,
            },
            "max_vertex": {"type": "number", "minimum": -1},
            "max_face": {"type": "number", "minimum": -1},
            "max_cell": {"type": "number", "minimum": -1},
        },
        "required": [
            "attributes",
            "default_vertex_attributes",
            "default_edge_attributes",
            "default_face_attributes",
            "vertex",
            "cell",
            "edge_data",
            "face_data",
            "cell_data",
            "max_vertex",
            "max_face",
            "max_cell",
        ],
    }

    @property
    def __data__(self):
        # type: () -> dict
        _cell = {}
        for c in self._cell:
            faces = []
            for u in sorted(self._cell[c]):
                for v in sorted(self._cell[c][u]):
                    faces.append(self._halfface[self._cell[c][u][v]])
            _cell[c] = faces

        return {
            "attributes": self.attributes,
            "default_vertex_attributes": self.default_vertex_attributes,
            "default_edge_attributes": self.default_edge_attributes,
            "default_face_attributes": self.default_face_attributes,
            "default_cell_attributes": self.default_cell_attributes,
            "vertex": {str(vertex): attr for vertex, attr in self._vertex.items()},
            "cell": {str(cell): faces for cell, faces in _cell.items()},
            "edge_data": self._edge_data,
            "face_data": self._face_data,
            "cell_data": {str(cell): attr for cell, attr in self._cell_data},
            "max_vertex": self._max_vertex,
            "max_face": self._max_face,
            "max_cell": self._max_cell,
        }

    @classmethod
    def __from_data__(cls, data):
        # type: (dict) -> VolMesh
        volmesh = cls(
            default_vertex_attributes=data.get("default_vertex_attributes"),
            default_edge_attributes=data.get("default_edge_attributes"),
            default_face_attributes=data.get("default_face_attributes"),
            default_cell_attributes=data.get("default_cell_attributes"),
        )
        volmesh.attributes.update(data["attributes"] or {})

        vertex = data["vertex"] or {}
        cell = data["cell"] or {}
        edge_data = data.get("edge_data") or {}
        face_data = data.get("face_data") or {}
        cell_data = data.get("cell_data") or {}

        for key, attr in iter(vertex.items()):
            volmesh.add_vertex(key=key, attr_dict=attr)

        for ckey, faces in iter(cell.items()):
            volmesh.add_cell(faces, ckey=ckey, attr_dict=cell_data.get(ckey))

        for edge in edge_data:
            volmesh._edge_data[edge] = edge_data[edge] or {}

        for face in face_data:
            volmesh._face_data[face] = face_data[face] or {}

        volmesh._max_vertex = data.get("max_vertex", volmesh._max_vertex)
        volmesh._max_face = data.get("max_face", volmesh._max_face)
        volmesh._max_cell = data.get("max_cell", volmesh._max_cell)

        return volmesh

    def __init__(self, default_vertex_attributes=None, default_edge_attributes=None, default_face_attributes=None, default_cell_attributes=None, name=None, **kwargs):  # fmt: skip
        # type: (dict | None, dict | None, dict | None, dict | None, str | None, dict) -> None
        super(VolMesh, self).__init__(kwargs, name=name)
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1
        self._vertex = {}
        self._halfface = {}
        self._cell = {}
        self._plane = {}
        self._edge_data = {}
        self._face_data = {}
        self._cell_data = {}
        self.default_vertex_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}
        self.default_cell_attributes = {}
        if default_vertex_attributes:
            self.default_vertex_attributes.update(default_vertex_attributes)
        if default_edge_attributes:
            self.default_edge_attributes.update(default_edge_attributes)
        if default_face_attributes:
            self.default_face_attributes.update(default_face_attributes)
        if default_cell_attributes:
            self.default_cell_attributes.update(default_cell_attributes)

    def __str__(self):
        # type: () -> str
        tpl = "<VolMesh with {} vertices, {} faces, {} cells, {} edges>"
        return tpl.format(
            self.number_of_vertices(),
            self.number_of_faces(),
            self.number_of_cells(),
            self.number_of_edges(),
        )

    # --------------------------------------------------------------------------
    # Customisation
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Special properties
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_meshgrid(cls, dx=10, dy=None, dz=None, nx=10, ny=None, nz=None):
        # type: (float, float | None, float | None, int, int | None, int | None) -> VolMesh
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
        :class:`compas.datastructures.VolMesh`

        See Also
        --------
        :meth:`from_obj`, :meth:`from_vertices_and_cells`

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
        # type: (str, int | None) -> VolMesh
        """Construct a volmesh object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : path string | file-like object | URL string
            A path, a file-like object or a URL pointing to a file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        :class:`compas.datastructures.VolMesh`
            A volmesh object.

        See Also
        --------
        :meth:`to_obj`
        :meth:`from_meshgrid`, :meth:`from_vertices_and_cells`
        :class:`compas.files.OBJ`

        """
        obj = OBJ(filepath, precision)
        vertices = obj.parser.vertices or []  # type: ignore
        faces = obj.parser.faces or []  # type: ignore
        groups = obj.parser.groups or {}  # type: ignore
        objects = obj.parser.objects or {}  # type: ignore

        if groups:
            cells = []
            for name, group in groups.items():
                cell = []
                for item in group:
                    if item[0] != "f":
                        continue
                    face = faces[item[1]]
                    cell.append(face)
                cells.append(cell)
            return cls.from_vertices_and_cells(vertices, cells)

        if objects:
            polyhedrons = []
            for name in objects:
                vertex_xyz = objects[name][0]
                vertex_index = {vertex: index for index, vertex in enumerate(vertex_xyz)}
                vertices = list(vertex_xyz.values())
                faces = [[vertex_index[vertex] for vertex in face] for face in objects[name][1]]
                polyhedron = Polyhedron(vertices, faces)
                polyhedrons.append(polyhedron)
            return cls.from_polyhedrons(polyhedrons)

        cell = [faces]
        return cls.from_vertices_and_cells(vertices, cell)

    @classmethod
    def from_vertices_and_cells(cls, vertices, cells):
        # type: (list[list[float]] | dict[int, list[float]], list[list[list[int]]]) -> VolMesh
        """Construct a volmesh object from vertices and cells.

        Parameters
        ----------
        vertices : list[list[float]]
            Ordered list of vertices, represented by their XYZ coordinates.
        cells : list[list[list[int]]]
            List of cells defined by their faces.

        Returns
        -------
        :class:`compas.datastructures.VolMesh`
            A volmesh object.

        See Also
        --------
        :meth:`to_vertices_and_cells`
        :meth:`from_obj`, :meth:`from_meshgrid`

        """
        volmesh = cls()

        if isinstance(vertices, Mapping):
            for key, xyz in vertices.items():  # type: ignore
                volmesh.add_vertex(key=key, attr_dict=dict(zip(("x", "y", "z"), xyz)))
        else:
            for x, y, z in iter(vertices):  # type: ignore
                volmesh.add_vertex(x=x, y=y, z=z)  # type: ignore

        for cell in cells:
            volmesh.add_cell(cell)
        return volmesh

    @classmethod
    def from_meshes(cls, meshes):
        # type: (list[Mesh]) -> VolMesh
        """Construct a volmesh from a list of faces.

        Parameters
        ----------
        meshes : list[:class:`Mesh`]
            The input meshes.

        Returns
        -------
        :class:`VolMesh`

        Notes
        -----
        The cycle directions of the faces of the meshes are neither checked, nor changed.
        This means that the cycle directions of the provided meshes have to be consistent.

        """
        gkey_xyz = {}
        cells = []

        for mesh in meshes:
            for vertex in mesh.vertices():
                xyz = mesh.vertex_attributes(vertex, "xyz")
                gkey = TOL.geometric_key(xyz)
                gkey_xyz[gkey] = xyz
            cell = []
            for face in mesh.faces():
                temp = []
                for vertex in mesh.face_vertices(face):
                    xyz = mesh.vertex_attributes(vertex, "xyz")
                    gkey = TOL.geometric_key(xyz)
                    temp.append(gkey)
                cell.append(temp)
            cells.append(cell)

        gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}
        vertices = list(gkey_xyz.values())
        cells = [[[gkey_index[gkey] for gkey in face] for face in cell] for cell in cells]

        return cls.from_vertices_and_cells(vertices, cells)

    @classmethod
    def from_polyhedrons(cls, polyhedrons):
        # type: (list[Polyhedron]) -> VolMesh
        """Construct a VolMesh from a list of polyhedrons.

        Parameters
        ----------
        polyhedrons : list[:class:`Polyhedron`]

        Returns
        -------
        :class:`VolMesh`

        """
        gkey_xyz = {}
        cells = []

        for polyhedron in polyhedrons:
            for vertex in polyhedron.vertices:
                gkey = TOL.geometric_key(vertex)
                gkey_xyz[gkey] = vertex
            cell = []
            for face in polyhedron.faces:
                temp = []
                for index in face:
                    xyz = polyhedron.vertices[index]
                    gkey = TOL.geometric_key(xyz)
                    temp.append(gkey)
                cell.append(temp)
            cells.append(cell)

        gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}
        vertices = list(gkey_xyz.values())
        cells = [[[gkey_index[gkey] for gkey in face] for face in cell] for cell in cells]

        return cls.from_vertices_and_cells(vertices, cells)

    # --------------------------------------------------------------------------
    # Conversions
    # --------------------------------------------------------------------------

    def to_obj(self, filepath, precision=None, **kwargs):
        # type: (str, int | None, dict) -> None
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

        See Also
        --------
        :meth:`from_obj`

        Warnings
        --------
        This function only writes geometric data about the vertices and
        the faces to the file.

        """
        meshes = [self.cell_to_mesh(cell) for cell in self.cells()]  # type: ignore
        obj = OBJ(filepath, precision=precision)
        obj.write(meshes, **kwargs)  # type: ignore

    def to_vertices_and_cells(self):
        # type: () -> tuple[list[list[float]], list[list[list[int]]]]
        """Return the vertices and cells of a volmesh.

        Returns
        -------
        list[list[float]]
            A list of vertices, represented by their XYZ coordinates.
        list[list[list[int]]]
            A list of cells, with each cell a list of faces, and each face a list of vertex indices.

        See Also
        --------
        :meth:`from_vertices_and_cells`

        """
        vertex_index = self.vertex_index()
        vertices = [self.vertex_coordinates(vertex) for vertex in self.vertices()]
        cells = []
        for cell in self.cells():
            faces = [[vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in self.cell_faces(cell)]
            cells.append(faces)
        return vertices, cells

    def cell_to_mesh(self, cell):
        # type: (int) -> Mesh
        """Construct a mesh object from from a cell of a volmesh.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        See Also
        --------
        :meth:`cell_to_vertices_and_faces`

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Mesh.from_vertices_and_faces(vertices, faces)

    def cell_to_vertices_and_faces(self, cell):
        # type: (int) -> tuple[list[list[float]], list[list[int]]]
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

        See Also
        --------
        :meth:`cell_to_mesh`

        """
        vertices = self.cell_vertices(cell)
        faces = self.cell_faces(cell)
        vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
        vertices = [self.vertex_coordinates(vertex) for vertex in vertices]
        faces = [[vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in faces]
        return vertices, faces

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    def clear(self):
        # type: () -> None
        """Clear all the volmesh data.

        Returns
        -------
        None

        """
        del self._vertex
        del self._halfface
        del self._cell
        del self._plane
        del self._edge_data
        del self._face_data
        del self._cell_data
        self._vertex = {}
        self._halfface = {}
        self._cell = {}
        self._plane = {}
        self._edge_data = {}
        self._face_data = {}
        self._cell_data = {}
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1

    def vertex_sample(self, size=1):
        # type: (int) -> list[int]
        """Get the identifiers of a set of random vertices.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the vertices.

        See Also
        --------
        :meth:`edge_sample`, :meth:`face_sample`, :meth:`cell_sample`

        """
        return sample(list(self.vertices()), size)  # type: ignore

    def edge_sample(self, size=1):
        # type: (int) -> list[tuple[int, int]]
        """Get the identifiers of a set of random edges.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[tuple[int, int]]
            The identifiers of the edges.

        See Also
        --------
        :meth:`vertex_sample`, :meth:`face_sample`, :meth:`cell_sample`

        """
        return sample(list(self.edges()), size)  # type: ignore

    def face_sample(self, size=1):
        # type: (int) -> list[int]
        """Get the identifiers of a set of random faces.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the faces.

        See Also
        --------
        :meth:`vertex_sample`, :meth:`edge_sample`, :meth:`cell_sample`

        """
        return sample(list(self.faces()), size)  # type: ignore

    def cell_sample(self, size=1):
        # type: (int) -> list[int]
        """Get the identifiers of a set of random cells.

        Parameters
        ----------
        size : int, optional
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the cells.

        See Also
        --------
        :meth:`vertex_sample`, :meth:`edge_sample`, :meth:`face_sample`

        """
        return sample(list(self.cells()), size)  # type: ignore

    def vertex_index(self):
        # type: () -> dict[int, int]
        """Returns a dictionary that maps vertex dictionary keys to the
        corresponding index in a vertex list or array.

        Returns
        -------
        dict[int, int]
            A dictionary of vertex-index pairs.

        See Also
        --------
        :meth:`index_vertex`

        """
        return {key: index for index, key in enumerate(self.vertices())}  # type: ignore

    def index_vertex(self):
        # type: () -> dict[int, int]
        """Returns a dictionary that maps the indices of a vertex list to
        keys in the vertex dictionary.

        Returns
        -------
        dict[int, int]
            A dictionary of index-vertex pairs.

        See Also
        --------
        :meth:`vertex_index`

        """
        return dict(enumerate(self.vertices()))  # type: ignore

    def vertex_gkey(self, precision=None):
        # type: (int | None) -> dict[int, str]
        """Returns a dictionary that maps vertex dictionary keys to the corresponding
        *geometric key* up to a certain precision.

        Parameters
        ----------
        precision : int, optional
            Precision for converting numbers to strings.
            Default is :attr:`TOL.precision`.

        Returns
        -------
        dict[int, str]
            A dictionary of vertex-geometric key pairs.

        See Also
        --------
        :meth:`gkey_vertex`

        """
        gkey = TOL.geometric_key
        xyz = self.vertex_coordinates
        return {vertex: gkey(xyz(vertex), precision) for vertex in self.vertices()}  # type: ignore

    def gkey_vertex(self, precision=None):
        # type: (int | None) -> dict[str, int]
        """Returns a dictionary that maps *geometric keys* of a certain precision
        to the keys of the corresponding vertices.

        Parameters
        ----------
        precision : int, optional
            Precision for converting numbers to strings.
            Default is :attr:`TOL.precision`.

        Returns
        -------
        dict[str, int]
            A dictionary of geometric key-vertex pairs.

        See Also
        --------
        :meth:`vertex_gkey`

        """
        gkey = TOL.geometric_key
        xyz = self.vertex_coordinates
        return {gkey(xyz(vertex), precision): vertex for vertex in self.vertices()}  # type: ignore

    # --------------------------------------------------------------------------
    # Builders & Modifiers
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        # type: (int | None, dict | None, dict) -> int
        """Add a vertex to the volmesh object.

        Parameters
        ----------
        key : int, optional
            The vertex identifier.
        attr_dict : dict[str, Any], optional
            dictionary of vertex attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The identifier of the vertex.

        See Also
        --------
        :meth:`add_halfface`, :meth:`add_cell`

        Notes
        -----
        If no key is provided for the vertex, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        """
        if key is None:
            key = self._max_vertex = self._max_vertex + 1
        key = int(key)
        if key > self._max_vertex:
            self._max_vertex = key
        if key not in self._vertex:
            self._vertex[key] = {}
            self._plane[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self._vertex[key].update(attr)
        return key

    def add_halfface(self, vertices, fkey=None, attr_dict=None, **kwattr):
        # type: (list[int], int | None, dict | None, dict) -> int
        """Add a face to the volmesh object.

        Parameters
        ----------
        vertices : list[int]
            A list of ordered vertex keys representing the face.
            For every vertex that does not yet exist, a new vertex is created.
        fkey : int, optional
            The face identifier.
        attr_dict : dict[str, Any], optional
            dictionary of halfface attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The key of the face.

        Raises
        ------
        ValueError
            If the number of vertices is less than 3.

        See Also
        --------
        :meth:`add_vertex`, :meth:`add_cell`

        Notes
        -----
        If no key is provided for the face, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        """
        if len(vertices) < 3:
            raise ValueError("A half-face should have at least 3 vertices: {}".format(vertices))

        if vertices[-1] == vertices[0]:
            vertices = vertices[:-1]
        vertices = [int(key) for key in vertices]

        if fkey is None:
            fkey = self._max_face = self._max_face + 1
        fkey = int(fkey)
        if fkey > self._max_face:
            self._max_face = fkey

        attr = attr_dict or {}
        attr.update(kwattr)
        self._halfface[fkey] = vertices

        for name, value in attr.items():
            self.face_attribute(fkey, name, value)

        for u, v, w in uvw_from_vertices(vertices):
            if v not in self._plane[u]:
                self._plane[u][v] = {}
            self._plane[u][v][w] = None
            if v not in self._plane[w]:
                self._plane[w][v] = {}
            if u not in self._plane[w][v]:
                self._plane[w][v][u] = None

        return fkey

    def add_cell(self, faces, ckey=None, attr_dict=None, **kwattr):
        """Add a cell to the volmesh object.

        Parameters
        ----------
        faces : list[list[int]]
            The faces of the cell defined as lists of vertices.
        ckey : int, optional
            The cell identifier.
        attr_dict : dict[str, Any], optional
            A dictionary of cell attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The key of the cell.

        Raises
        ------
        TypeError
            If the provided cell key is of an unhashable type.

        See also
        --------
        :meth:`add_vertex`, :meth:`add_halfface`

        Notes
        -----
        If no key is provided for the cell, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        """
        if ckey is None:
            ckey = self._max_cell = self._max_cell + 1
        ckey = int(ckey)
        if ckey > self._max_cell:
            self._max_cell = ckey

        attr = attr_dict or {}
        attr.update(kwattr)
        self._cell[ckey] = {}

        for name, value in attr.items():
            self.cell_attribute(ckey, name, value)

        for vertices in faces:
            fkey = self.add_halfface(vertices)
            vertices = self.halfface_vertices(fkey)

            for u, v, w in uvw_from_vertices(vertices):
                if u not in self._cell[ckey]:
                    self._cell[ckey][u] = {}
                self._cell[ckey][u][v] = fkey
                self._plane[u][v][w] = ckey

        return ckey

    def delete_vertex(self, vertex):
        """Delete a vertex from the volmesh and everything that is attached to it.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        None

        See Also
        --------
        :meth:`delete_halfface`, :meth:`delete_cell`

        """
        for cell in self.vertex_cells(vertex):
            self.delete_cell(cell)

    def delete_cell(self, cell):
        """Delete a cell from the volmesh.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the cell does not exist.

        See Also
        --------
        :meth:`delete_vertex`, :meth:`delete_halfface`

        Notes
        -----
        Remaining unused vertices are not automatically deleted.
        Use :meth:`remove_unused_vertices` to accomplish this.

        """
        cell_faces = self.cell_faces(cell)

        # remove edge data
        for face in cell_faces:
            for edge in self.halfface_halfedges(face):
                # this should also use a key map
                u, v = edge
                if (u, v) in self._edge_data:
                    del self._edge_data[u, v]
                if (v, u) in self._edge_data:
                    del self._edge_data[v, u]

        # remove face data
        for face in cell_faces:
            vertices = self.halfface_vertices(face)
            key = "-".join(map(str, sorted(vertices)))
            if key in self._face_data:
                del self._face_data[key]

        # remove cell data
        if cell in self._cell_data:
            del self._cell_data[cell]

        # remove planes and halffaces
        for face in cell_faces:
            vertices = self.halfface_vertices(face)
            for u, v, w in uvw_from_vertices(vertices):
                if self._plane[w][v][u] is None:
                    del self._plane[u][v][w]
                    del self._plane[w][v][u]
                    if not self._plane[u][v]:
                        del self._plane[u][v]
                    if not self._plane[w][v]:
                        del self._plane[w][v]
                else:
                    self._plane[u][v][w] = None
            del self._halfface[face]

        # remove cell
        del self._cell[cell]

    def remove_unused_vertices(self):
        """Remove all unused vertices from the volmesh object.

        Returns
        -------
        None

        """
        for vertex in list(self.vertices()):
            if vertex not in self._plane:
                del self._vertex[vertex]
            else:
                if not self._plane[vertex]:
                    del self._vertex[vertex]
                    del self._plane[vertex]

    # --------------------------------------------------------------------------
    # Volmesh Geometry
    # --------------------------------------------------------------------------

    def centroid(self):
        """Compute the centroid of the volmesh.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the centroid.

        """
        return Point(*centroid_points([self.vertex_coordinates(vertex) for vertex in self.vertices()]))

    def aabb(self):
        """Calculate the axis aligned bounding box of the mesh.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        xyz = self.vertices_attributes("xyz")
        return Box.from_bounding_box(bounding_box(xyz))

    def obb(self):
        """Calculate the oriented bounding box of the datastructure.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        xyz = self.vertices_attributes("xyz")
        return Box.from_bounding_box(oriented_bounding_box(xyz))

    # --------------------------------------------------------------------------
    # VolMesh Topology
    # --------------------------------------------------------------------------

    def number_of_vertices(self):
        """Count the number of vertices in the volmesh.

        Returns
        -------
        int
            The number of vertices.

        See Also
        --------
        :meth:`number_of_edges`, :meth:`number_of_faces`, :meth:`number_of_cells`

        """
        return len(list(self.vertices()))

    def number_of_edges(self):
        """Count the number of edges in the volmesh.

        Returns
        -------
        int
            The number of edges.

        See Also
        --------
        :meth:`number_of_vertices`, :meth:`number_of_faces`, :meth:`number_of_cells`

        """
        return len(list(self.edges()))

    def number_of_faces(self):
        """Count the number of faces in the volmesh.

        Returns
        -------
        int
            The number of faces.

        See Also
        --------
        :meth:`number_of_vertices`, :meth:`number_of_edges`, :meth:`number_of_cells`

        """
        return len(list(self.faces()))

    def number_of_cells(self):
        """Count the number of faces in the volmesh.

        Returns
        -------
        int
            The number of cells.

        See Also
        --------
        :meth:`number_of_vertices`, :meth:`number_of_edges`, :meth:`number_of_faces`

        """
        return len(list(self.cells()))

    def is_valid(self):
        """Verify that the volmesh is valid.

        Returns
        -------
        bool
            True if the volmesh is valid.
            False otherwise.

        """
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # Vertex Accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Iterate over the vertices of the volmesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex identifier.
            If `data` is True, the next vertex as a (vertex, attr) a tuple.

        See Also
        --------
        :meth:`edges`, :meth:`faces`, :meth:`cells`

        """
        for vertex in self._vertex:
            if not data:
                yield vertex
            else:
                yield vertex, self.vertex_attributes(vertex)

    def vertices_where(self, conditions=None, data=False, **kwargs):
        """Get vertices for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the vertex attributes in addition to the identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

        See Also
        --------
        :meth:`vertices_where_predicate`
        :meth:`edges_where`, :meth:`faces_where`, :meth:`cells_where`

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for key, attr in self.vertices(True):
            is_match = True

            attr = attr or {}

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if callable(method):
                    val = method(key)

                    if isinstance(val, list):
                        if value not in val:
                            is_match = False
                            break
                        break

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value
                        if val < minval or val > maxval:
                            is_match = False
                            break
                    else:
                        if value != val:
                            is_match = False
                            break

                else:
                    if name not in attr:
                        is_match = False
                        break

                    if isinstance(attr[name], list):
                        if value not in attr[name]:
                            is_match = False
                            break
                        break

                    if isinstance(value, (tuple, list)):
                        minval, maxval = value
                        if attr[name] < minval or attr[name] > maxval:
                            is_match = False
                            break
                    else:
                        if value != attr[name]:
                            is_match = False
                            break

            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key

    def vertices_where_predicate(self, predicate, data=False):
        """Get vertices for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters: the vertex identifier and the vertex attributes, and should return True or False.
        data : bool, optional
            If True, yield the vertex attributes in addition to the identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

        See Also
        --------
        :meth:`vertices_where`
        :meth:`edges_where_predicate`, :meth:`faces_where_predicate`, :meth:`cells_where_predicate`

        """
        for key, attr in self.vertices(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    # --------------------------------------------------------------------------
    # Vertex Attributes
    # --------------------------------------------------------------------------

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        """Update the default vertex attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_edge_attributes`, :meth:`update_default_face_attributes`, :meth:`update_default_cell_attributes`

        Notes
        -----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_vertex_attributes.update(attr_dict)

    def vertex_attribute(self, vertex, name, value=None):
        """Get or set an attribute of a vertex.

        Parameters
        ----------
        vertex : int
            The vertex identifier.
        name : str
            The name of the attribute
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute,
            or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the vertex does not exist.

        See Also
        --------
        :meth:`unset_vertex_attribute`
        :meth:`vertex_attributes`, :meth:`vertices_attribute`, :meth:`vertices_attributes`
        :meth:`edge_attribute`, :meth:`face_attribute`, :meth:`cell_attribute`

        """
        if vertex not in self._vertex:
            raise KeyError(vertex)
        if value is not None:
            self._vertex[vertex][name] = value
            return None
        if name in self._vertex[vertex]:
            return self._vertex[vertex][name]
        else:
            if name in self.default_vertex_attributes:
                return self.default_vertex_attributes[name]

    def unset_vertex_attribute(self, vertex, name):
        """Unset the attribute of a vertex.

        Parameters
        ----------
        vertex : int
            The vertex identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the vertex does not exist.

        See Also
        --------
        :meth:`vertex_attribute`

        Notes
        -----
        Unsetting the value of a vertex attribute implicitly sets it back to the value
        stored in the default vertex attribute dict.

        """
        if name in self._vertex[vertex]:
            del self._vertex[vertex][name]

    def vertex_attributes(self, vertex, names=None, values=None):
        """Get or set multiple attributes of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            the function returns a dictionary of all attribute name-value pairs of the vertex.
            If the parameter `names` is not empty,
            the function returns a list of the values corresponding to the requested attribute names.
            The function returns None if it is used as a "setter".

        Raises
        ------
        KeyError
            If the vertex does not exist.

        See Also
        --------
        :meth:`vertex_attribute`, :meth:`vertices_attribute`, :meth:`vertices_attributes`
        :meth:`edge_attributes`, :meth:`face_attributes`, :meth:`cell_attributes`

        """
        if vertex not in self._vertex:
            raise KeyError(vertex)
        if names and values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                self._vertex[vertex][name] = value
            return
        # use it as a getter
        if not names:
            # return all vertex attributes as a dict
            return VertexAttributeView(self.default_vertex_attributes, self._vertex[vertex])
        values = []
        for name in names:
            if name in self._vertex[vertex]:
                values.append(self._vertex[vertex][name])
            elif name in self.default_vertex_attributes:
                values.append(self.default_vertex_attributes[name])
            else:
                values.append(None)
        return values

    def vertices_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple vertices.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[int], optional
            A list of vertex identifiers.

        Returns
        -------
        list[Any] | None
            The value of the attribute for each vertex,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the vertices does not exist.

        See Also
        --------
        :meth:`vertex_attribute`, :meth:`vertex_attributes`, :meth:`vertices_attributes`
        :meth:`edges_attribute`, :meth:`faces_attribute`, :meth:`cells_attribute`

        """
        vertices = keys or self.vertices()
        if value is not None:
            for vertex in vertices:
                self.vertex_attribute(vertex, name, value)
            return
        return [self.vertex_attribute(vertex, name) for vertex in vertices]

    def vertices_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple vertices.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        key : list[Any], optional
            A list of vertex identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            the function returns a list containing an attribute dict per vertex.
            If the parameter `names` is not empty,
            the function returns a list containing a list of attribute values per vertex corresponding to the provided attribute names.
            The function returns None if it is used as a "setter".

        Raises
        ------
        KeyError
            If any of the vertices does not exist.

        See Also
        --------
        :meth:`vertex_attribute`, :meth:`vertex_attributes`, :meth:`vertices_attribute`
        :meth:`edges_attributes`, :meth:`faces_attributes`, :meth:`cells_attributes`

        """
        vertices = keys or self.vertices()
        if values:
            for vertex in vertices:
                self.vertex_attributes(vertex, names, values)
            return
        return [self.vertex_attributes(vertex, names) for vertex in vertices]

    # --------------------------------------------------------------------------
    # Vertex Topology
    # --------------------------------------------------------------------------

    def has_vertex(self, vertex):
        """Verify that a vertex is in the volmesh.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is in the volmesh.
            False otherwise.

        See Also
        --------
        :meth:`has_edge`, :meth:`has_face`, :meth:`has_cell`

        """
        return vertex in self._vertex

    def vertex_neighbors(self, vertex):
        """Return the vertex neighbors of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of neighboring vertices.

        See Also
        --------
        :meth:`vertex_degree`, :meth:`vertex_min_degree`, :meth:`vertex_max_degree`
        :meth:`vertex_faces`, :meth:`vertex_halffaces`, :meth:`vertex_cells`
        :meth:`vertex_neighborhood`

        """
        return self._plane[vertex].keys()

    def vertex_neighborhood(self, vertex, ring=1):
        """Return the vertices in the neighborhood of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.
        ring : int, optional
            The number of neighborhood rings to include.

        Returns
        -------
        list[int]
            The vertices in the neighborhood.

        See Also
        --------
        :meth:`vertex_neighbors`

        Notes
        -----
        The vertices in the neighborhood are unordered.

        """
        nbrs = set(self.vertex_neighbors(vertex))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr in nbrs:
                temp += self.vertex_neighbors(nbr)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([vertex]))

    def vertex_degree(self, vertex):
        """Count the neighbors of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        int
            The degree of the vertex.

        See Also
        --------
        :meth:`vertex_neighbors`, :meth:`vertex_min_degree`, :meth:`vertex_max_degree`

        """
        return len(self.vertex_neighbors(vertex))

    def vertex_min_degree(self):
        """Compute the minimum degree of all vertices.

        Returns
        -------
        int
            The lowest degree of all vertices.

        See Also
        --------
        :meth:`vertex_degree`, :meth:`vertex_max_degree`

        """
        if not self._vertex:
            return 0
        return min(self.vertex_degree(vertex) for vertex in self.vertices())

    def vertex_max_degree(self):
        """Compute the maximum degree of all vertices.

        Returns
        -------
        int
            The highest degree of all vertices.

        See Also
        --------
        :meth:`vertex_degree`, :meth:`vertex_min_degree`

        """
        if not self._vertex:
            return 0
        return max(self.vertex_degree(vertex) for vertex in self.vertices())

    def vertex_edges(self, vertex):
        """Compute the edges connected to a given vertex.

        Parameters
        ----------
        vertex : int
            The vertex identifier.

        Returns
        -------
        list[tuple[int, int]]
            The connected edges.

        """
        return [(vertex, nbr) for nbr in sorted(self.vertex_neighbors(vertex))]

    def vertex_halffaces(self, vertex):
        """Return all halffaces connected to a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of halffaces connected to a vertex.

        See Also
        --------
        :meth:`vertex_neighbors`, :meth:`vertex_faces`, :meth:`vertex_cells`

        """
        u = vertex
        faces = []
        for v in self._plane[u]:
            for w in self._plane[u][v]:
                cell = self._plane[u][v][w]
                if cell is not None:
                    face = self.cell_halfedge_face(cell, (u, v))
                    faces.append(face)
        return faces

    def vertex_cells(self, vertex):
        """Return all cells connected to a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of cells connected to a vertex.

        See Also
        --------
        :meth:`vertex_neighbors`, :meth:`vertex_faces`, :meth:`vertex_halffaces`

        """
        u = vertex
        cells = []
        for v in self._plane[u]:
            for w in self._plane[u][v]:
                cell = self._plane[u][v][w]
                if cell is not None:
                    if cell not in cells:
                        cells.append(cell)
        return cells

    def is_vertex_on_boundary(self, vertex):
        """Verify that a vertex is on a boundary.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is on the boundary.
            False otherwise.

        See Also
        --------
        :meth:`is_edge_on_boundary`, :meth:`is_face_on_boundary`, :meth:`is_cell_on_boundary`

        """
        halffaces = self.vertex_halffaces(vertex)
        for halfface in halffaces:
            if self.is_halfface_on_boundary(halfface):
                return True
        return False

    # --------------------------------------------------------------------------
    # Vertex Geometry
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

        See Also
        --------
        :meth:`vertex_point`, :meth:`vertex_laplacian`, :meth:`vertex_neighborhood_centroid`

        """
        return [self._vertex[vertex][axis] for axis in axes]

    def vertex_point(self, vertex):
        """Return the point representation of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point.

        See Also
        --------
        :meth:`vertex_laplacian`, :meth:`vertex_neighborhood_centroid`

        """
        return Point(*self.vertex_coordinates(vertex))

    def vertex_laplacian(self, vertex):
        """Compute the vector from a vertex to the centroid of its neighbors.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The laplacian vector.

        See Also
        --------
        :meth:`vertex_point`, :meth:`vertex_neighborhood_centroid`

        """
        c = self.vertex_neighborhood_centroid(vertex)
        p = self.vertex_coordinates(vertex)
        return Vector(*subtract_vectors(c, p))

    def vertex_neighborhood_centroid(self, vertex):
        """Compute the point at the centroid of the neighbors of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the centroid.

        See Also
        --------
        :meth:`vertex_point`, :meth:`vertex_laplacian`

        """
        return Point(*centroid_points([self.vertex_coordinates(nbr) for nbr in self.vertex_neighbors(vertex)]))

    # --------------------------------------------------------------------------
    # Edge Accessors
    # --------------------------------------------------------------------------

    def edges(self, data=False):
        """Iterate over the edges of the volmesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the edge attributes as well as the edge identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a ((u, v), attr) tuple.

        See Also
        --------
        :meth:`vertices`, :meth:`faces`, :meth:`cells`

        """
        seen = set()
        for vertex in self.vertices():
            for nbr in sorted(self.vertex_neighbors(vertex)):
                if (vertex, nbr) in seen or (nbr, vertex) in seen:
                    continue
                seen.add((vertex, nbr))
                seen.add((nbr, vertex))
                if not data:
                    yield vertex, nbr
                else:
                    yield (vertex, nbr), self.edge_attributes((vertex, nbr))

    def edges_where(self, conditions=None, data=False, **kwargs):
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the edge attributes in addition to the identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a (u, v, data) tuple.

        See Also
        --------
        :meth:`edges_where_predicate`
        :meth:`vertices_where`, :meth:`faces_where`, :meth:`cells_where`

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for key in self.edges():
            is_match = True

            attr = self.edge_attributes(key) or {}

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(key)
                elif name in attr:
                    val = attr[name]
                else:
                    is_match = False
                    break

                if isinstance(val, list):
                    if value not in val:
                        is_match = False
                        break
                elif isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if val < minval or val > maxval:
                        is_match = False
                        break
                else:
                    if value != val:
                        is_match = False
                        break

            if is_match:
                if data:
                    yield key, attr
                else:
                    yield key

    def edges_where_predicate(self, predicate, data=False):
        """Get edges for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters: the edge identifier and the edge attributes, and should return True or False.
        data : bool, optional
            If True, yield the edge attributes in addition to the identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a (u, v, data) tuple.

        See Also
        --------
        :meth:`edges_where`
        :meth:`vertices_where_predicate`, :meth:`faces_where_predicate`, :meth:`cells_where_predicate`

        """
        for key, attr in self.edges(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    # --------------------------------------------------------------------------
    # Edge Attributes
    # --------------------------------------------------------------------------

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_vertex_attributes`, :meth:`update_default_face_attributes`, :meth:`update_default_cell_attributes`

        Notes
        -----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)

    def edge_attribute(self, edge, name, value=None):
        """Get or set an attribute of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        :meth:`unset_edge_attribute`
        :meth:`edge_attributes`, :meth:`edges_attribute`, :meth:`edges_attributes`
        :meth:`vertex_attribute`, :meth:`face_attribute`, :meth:`cell_attribute`

        """
        u, v = edge
        if u not in self._plane or v not in self._plane[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if value is not None:
            if key not in self._edge_data:
                self._edge_data[key] = {}
            self._edge_data[key][name] = value
            return
        if key in self._edge_data and name in self._edge_data[key]:
            return self._edge_data[key][name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]

    def unset_edge_attribute(self, edge, name):
        """Unset the attribute of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.
        name : str
            The name of the attribute.

        Raises
        ------
        KeyError
            If the edge does not exist.

        Returns
        -------
        None

        See Also
        --------
        :meth:`edge_attribute`

        Notes
        -----
        Unsetting the value of an edge attribute implicitly sets it back to the value
        stored in the default edge attribute dict.

        """
        u, v = edge
        if u not in self._plane or v not in self._plane[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if key in self._edge_data and name in self._edge_data[key]:
            del self._edge_data[key][name]

    def edge_attributes(self, edge, names=None, values=None):
        """Get or set multiple attributes of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty, a dictionary of all attribute name-value pairs of the edge.
            If the parameter `names` is not empty, a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edges_attribute`, :meth:`edges_attributes`
        :meth:`vertex_attributes`, :meth:`face_attributes`, :meth:`cell_attributes`

        """
        u, v = edge
        if u not in self._plane or v not in self._plane[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if names and values:
            for name, value in zip(names, values):
                if key not in self._edge_data:
                    self._edge_data[key] = {}
                self._edge_data[key][name] = value
            return
        if not names:
            key = str(tuple(sorted(edge)))
            return EdgeAttributeView(self.default_edge_attributes, self._edge_data.setdefault(key, {}))
        values = []
        for name in names:
            value = self.edge_attribute(edge, name)
            values.append(value)
        return values

    def edges_attribute(self, name, value=None, edges=None):
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        edges : list[tuple[int, int]], optional
            A list of edge identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per edge of the requested attribute,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edge_attributes`, :meth:`edges_attributes`
        :meth:`vertex_attribute`, :meth:`face_attribute`, :meth:`cell_attribute`

        """
        edges = edges or self.edges()
        if value is not None:
            for edge in edges:
                self.edge_attribute(edge, name, value)
            return
        return [self.edge_attribute(edge, name) for edge in edges]

    def edges_attributes(self, names=None, values=None, edges=None):
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
        values : list[Any], optional
            The values of the attributes.
        edges : list[tuple[int, int]], optional
            A list of edge identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            a list containing per edge an attribute dict with all attributes (default + custom) of the edge.
            If the parameter `names` is not empty,
            a list containing per edge a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edge_attributes`, :meth:`edges_attribute`
        :meth:`vertex_attributes`, :meth:`face_attributes`, :meth:`cell_attributes`

        """
        edges = edges or self.edges()
        if values:
            for edge in edges:
                self.edge_attributes(edge, names, values)
            return
        return [self.edge_attributes(edge, names) for edge in edges]

    # --------------------------------------------------------------------------
    # Edge Topology
    # --------------------------------------------------------------------------

    def has_edge(self, edge):
        """Verify that the volmesh contains a directed edge (u, v).

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.

        See Also
        --------
        :meth:`has_vertex`, :meth:`has_face`, :meth:`has_cell`

        """
        return edge in set(self.edges())

    def edge_halffaces(self, edge):
        """Ordered halffaces around edge (u, v).

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        list[int]
            Ordered list of halfface identifiers.

        See Also
        --------
        :meth:`edge_cells`

        """
        u, v = edge
        halffaces = []
        for w in self._plane[u][v]:
            cell = self._plane[u][v][w]
            if cell is not None:
                face = self._cell[cell][u][v]
                halffaces.append(face)
        return halffaces

    def edge_cells(self, edge):
        """Ordered cells around edge (u, v).

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        list[int]
            Ordered list of keys identifying the ordered cells.

        See Also
        --------
        :meth:`edge_halffaces`

        """
        halffaces = self.edge_halffaces(edge)
        return [self.halfface_cell(halfface) for halfface in halffaces]

    def is_edge_on_boundary(self, edge):
        """Verify that an edge is on the boundary.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge is on the boundary.
            False otherwise.

        See Also
        --------
        :meth:`is_vertex_on_boundary`, :meth:`is_face_on_boundary`, :meth:`is_cell_on_boundary`

        Notes
        -----
        This method simply checks if u-v or v-u is on the edge of the volmesh.
        The direction u-v does not matter.

        """
        u, v = edge
        return None in self._plane[u][v].values()

    # --------------------------------------------------------------------------
    # Edge Geometry
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
        tuple[list[float], list[float]]
            The coordinates of the start point.
            The coordinates of the end point.

        See Also
        --------
        :meth:`edge_start`, :meth:`edge_end`, :meth:`edge_midpoint`, :meth:`edge_point`
        :meth:`edge_vector`, :meth:`edge_direction`, :meth:`edge_line`
        :meth:`edge_length`

        """
        u, v = edge
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_start(self, edge):
        """Return the start point of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Point`
            The start point.

        See Also
        --------
        :meth:`edge_end`, :meth:`edge_midpoint`, :meth:`edge_point`

        """
        return self.vertex_point(edge[0])

    def edge_end(self, edge):
        """Return the end point of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Point`
            The end point.

        See Also
        --------
        :meth:`edge_start`, :meth:`edge_midpoint`, :meth:`edge_point`

        """
        return self.vertex_point(edge[1])

    def edge_midpoint(self, edge):
        """Return the midpoint of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Point`
            The midpoint.

        See Also
        --------
        :meth:`edge_start`, :meth:`edge_end`, :meth:`edge_point`

        """
        a, b = self.edge_coordinates(edge)
        return Point(0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.5 * (a[2] + b[2]))

    def edge_point(self, edge, t=0.5):
        """Return the point at a parametric location along an edge.

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
        :class:`compas.geometry.Point`
            The XYZ coordinates of the point.

        See Also
        --------
        :meth:`edge_start`, :meth:`edge_end`, :meth:`edge_midpoint`

        """
        if t == 0:
            return self.edge_start(edge)
        if t == 1:
            return self.edge_end(edge)
        if t == 0.5:
            return self.edge_midpoint(edge)

        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return Point(*add_vectors(a, scale_vector(ab, t)))

    def edge_vector(self, edge):
        """Return the vector of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The vector from start to end.

        See Also
        --------
        :meth:`edge_direction`, :meth:`edge_line`

        """
        a, b = self.edge_coordinates(edge)
        return Vector.from_start_end(a, b)

    def edge_direction(self, edge):
        """Return the direction vector of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The direction vector of the edge.

        See Also
        --------
        :meth:`edge_vector`, :meth:`edge_line`

        """
        return Vector(*normalize_vector(self.edge_vector(edge)))

    def edge_line(self, edge):
        """Return the line representation of an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        :class:`compas.geometry.Line`
            The line.

        See Also
        --------
        :meth:`edge_vector`, :meth:`edge_direction`

        """
        return Line(self.edge_start(edge), self.edge_end(edge))

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

    # --------------------------------------------------------------------------
    # (Half)Face Accessors
    # --------------------------------------------------------------------------

    def halffaces(self, data=False):
        """Iterate over the halffaces of the volmesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the half-face attributes in addition to half-face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next halfface identifier.
            If `data` is True, the next halfface as a (halfface, attr) tuple.

        See Also
        --------
        :meth:`vertices`, :meth:`edges`, :meth:`cells`

        """
        for hface in self._halfface:
            if not data:
                yield hface
            else:
                yield hface, self.face_attributes(hface)

    def faces(self, data=False):
        """ "Iterate over the halffaces of the volmesh and yield faces.

        Parameters
        ----------
        data : bool, optional
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face identifier.
            If `data` is True, the next face as a (face, attr) tuple.

        See Also
        --------
        :meth:`vertices`, :meth:`edges`, :meth:`cells`

        Notes
        -----
        Volmesh faces have no topological meaning (analogous to an edge of a mesh).
        They are typically used for geometric operations (i.e. planarisation).
        Between the interface of two cells, there are two interior faces (one from each cell).
        Only one of these two interior faces are returned as a "face".
        The unique faces are found by comparing string versions of sorted vertex lists.

        """
        seen = set()
        faces = []
        for face in self._halfface:
            key = "-".join(map(str, sorted(self.halfface_vertices(face))))
            if key in seen:
                continue
            seen.add(key)
            faces.append(face)
        for face in faces:
            if not data:
                yield face
            else:
                yield face, self.face_attributes(face)

    def faces_where(self, conditions=None, data=False, **kwargs):
        """Get faces for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the face attributes in addition to the identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face that matches the condition.
            If `data` is True, the next face and its attributes.

        See Also
        --------
        :meth:`faces_where_predicate`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`cells_where`

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for fkey in self.faces():
            is_match = True

            attr = self.face_attributes(fkey) or {}

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(fkey)
                elif name in attr:
                    val = attr[name]
                else:
                    is_match = False
                    break

                if isinstance(val, list):
                    if value not in val:
                        is_match = False
                        break
                elif isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if val < minval or val > maxval:
                        is_match = False
                        break
                else:
                    if value != val:
                        is_match = False
                        break

            if is_match:
                if data:
                    yield fkey, attr
                else:
                    yield fkey

    def faces_where_predicate(self, predicate, data=False):
        """Get faces for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters: the face identifier and the the face attributes, and should return True or False.
        data : bool, optional
            If True, yield the face attributes in addition to the identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face that matches the condition.
            If `data` is True, the next face and its attributes.

        See Also
        --------
        :meth:`faces_where`
        :meth:`vertices_where_predicate`, :meth:`edges_where_predicate`, :meth:`cells_where_predicate`

        """
        for fkey, attr in self.faces(True):
            if predicate(fkey, attr):
                if data:
                    yield fkey, attr
                else:
                    yield fkey

    # --------------------------------------------------------------------------
    # Face Attributes
    # --------------------------------------------------------------------------

    def update_default_face_attributes(self, attr_dict=None, **kwattr):
        """Update the default face attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_vertex_attributes`, :meth:`update_default_edge_attributes`, :meth:`update_default_cell_attributes`

        Notes
        -----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_face_attributes.update(attr_dict)

    def face_attribute(self, face, name, value=None):
        """Get or set an attribute of a face.

        Parameters
        ----------
        face : int
            The face identifier.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        :meth:`unset_face_attribute`
        :meth:`face_attributes`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`vertex_attribute`, :meth:`edge_attribute`, :meth:`cell_attribute`

        """
        if face not in self._halfface:
            raise KeyError(face)
        key = str(tuple(sorted(self.halfface_vertices(face))))
        if value is not None:
            if key not in self._face_data:
                self._face_data[key] = {}
            self._face_data[key][name] = value
            return
        if key in self._face_data and name in self._face_data[key]:
            return self._face_data[key][name]
        if name in self.default_face_attributes:
            return self.default_face_attributes[name]

    def unset_face_attribute(self, face, name):
        """Unset the attribute of a face.

        Parameters
        ----------
        face : int
            The face identifier.
        name : str
            The name of the attribute.

        Raises
        ------
        KeyError
            If the face does not exist.

        Returns
        -------
        None

        See Also
        --------
        :meth:`face_attribute`

        Notes
        -----
        Unsetting the value of a face attribute implicitly sets it back to the value
        stored in the default face attribute dict.

        """
        if face not in self._halfface:
            raise KeyError(face)
        key = str(tuple(sorted(self.halfface_vertices(face))))
        if key in self._face_data and name in self._face_data[key]:
            del self._face_data[key][name]

    def face_attributes(self, face, names=None, values=None):
        """Get or set multiple attributes of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty, a dictionary of all attribute name-value pairs of the face.
            If the parameter `names` is not empty, a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`vertex_attributes`, :meth:`edge_attributes`, :meth:`cell_attributes`

        """
        if face not in self._halfface:
            raise KeyError(face)
        key = str(tuple(sorted(self.halfface_vertices(face))))
        if names and values:
            for name, value in zip(names, values):
                if key not in self._face_data:
                    self._face_data[key] = {}
                self._face_data[key][name] = value
            return
        if not names:
            return FaceAttributeView(self.default_face_attributes, self._face_data.setdefault(key, {}))
        values = []
        for name in names:
            value = self.face_attribute(face, name)
            values.append(value)
        return values

    def faces_attribute(self, name, value=None, faces=None):
        """Get or set an attribute of multiple faces.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        faces : list[int], optional
            A list of face identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per face of the requested attribute,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`face_attributes`, :meth:`faces_attributes`
        :meth:`vertex_attribute`, :meth:`edge_attribute`, :meth:`cell_attribute`

        """
        faces = faces or self.faces()
        if value is not None:
            for face in faces:
                self.face_attribute(face, name, value)
            return
        return [self.face_attribute(face, name) for face in faces]

    def faces_attributes(self, names=None, values=None, faces=None):
        """Get or set multiple attributes of multiple faces.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        faces : list[int], optional
            A list of face identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            a list containing per face an attribute dict with all attributes (default + custom) of the face.
            If the parameter `names` is not empty,
            a list containing per face a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`face_attributes`, :meth:`faces_attribute`
        :meth:`vertex_attributes`, :meth:`edge_attributes`, :meth:`cell_attributes`

        """
        faces = faces or self.faces()
        if values:
            for face in faces:
                self.face_attributes(face, names, values)
            return
        return [self.face_attributes(face, names) for face in faces]

    # --------------------------------------------------------------------------
    # Face Topology
    # --------------------------------------------------------------------------

    def has_halfface(self, halfface):
        """Verify that a face is part of the volmesh.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.

        See Also
        --------
        :meth:`has_vertex`, :meth:`has_edge`, :meth:`has_cell`

        """
        return halfface in self._halfface

    def halfface_vertices(self, halfface):
        """The vertices of a halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list[int]
            Ordered vertex identifiers.

        See Also
        --------
        :meth:`halfface_edges`, :meth:`halfface_halfedges`

        """
        return self._halfface[halfface]

    def halfface_halfedges(self, halfface):
        """The halfedges of a halfface.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of a halfface.

        See Also
        --------
        :meth:`halfface_edges`, :meth:`halfface_vertices`

        """
        vertices = self.halfface_vertices(halfface)
        return list(pairwise(vertices + vertices[0:1]))

    def halfface_cell(self, halfface):
        """The cell to which the halfface belongs to.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        int
            Identifier of the cell.

        See Also
        --------
        :meth:`halfface_opposite_cell`

        """
        u, v, w = self._halfface[halfface][:3]
        return self._plane[u][v][w]

    def halfface_opposite_cell(self, halfface):
        """The cell to which the opposite halfface belongs to.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        int
            Identifier of the cell.

        See Also
        --------
        :meth:`halfface_cell`

        """
        u, v, w = self._halfface[halfface][:3]
        return self._plane[w][v][u]

    def halfface_opposite_halfface(self, halfface):
        """The opposite face of a face.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        int
            Identifier of the opposite face.

        See Also
        --------
        :meth:`halfface_adjacent_halfface`

        Notes
        -----
        A face and its opposite face share the same vertices, but in reverse order.
        For a boundary face, the opposite face is None.

        """
        u, v, w = self._halfface[halfface][:3]
        nbr = self._plane[w][v][u]
        return None if nbr is None else self._cell[nbr][w][v]

    def halfface_vertex_ancestor(self, halfface, vertex):
        """Return the vertex before the specified vertex in a specific face.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        int
            The identifier of the vertex before the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        See Also
        --------
        :meth:`halfface_vertex_descendent`

        """
        i = self._halfface[halfface].index(vertex)
        return self._halfface[halfface][i - 1]

    def halfface_vertex_descendent(self, halfface, vertex):
        """Return the vertex after the specified vertex in a specific face.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        int
            The identifier of the vertex after the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        See Also
        --------
        :meth:`halfface_vertex_ancestor`

        """
        if self._halfface[halfface][-1] == vertex:
            return self._halfface[halfface][0]
        i = self._halfface[halfface].index(vertex)
        return self._halfface[halfface][i + 1]

    def halfface_manifold_neighbors(self, halfface):
        """Return the halfface neighbors of a halfface that are on the same manifold.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list[int]
            The list of neighboring halffaces.

        See Also
        --------
        :meth:`halfface_manifold_neighborhood`

        Notes
        -----
        Neighboring halffaces on the same cell are not included.

        """
        nbrs = []
        cell = self.halfface_cell(halfface)
        for u, v in self.halfface_halfedges(halfface):
            nbr_halfface = self._cell[cell][v][u]
            nbr_cell = self._plane[u][v][nbr_halfface]
            if nbr_cell is not None:
                nbr = self._cell[nbr_cell][v][u]
                nbrs.append(nbr)
        return nbrs

    def halfface_manifold_neighborhood(self, halfface, ring=1):
        """Return the halfface neighborhood of a halfface across their edges.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        list[int]
            The list of neighboring halffaces.

        See Also
        --------
        :meth:`halfface_manifold_neighbors`

        Notes
        -----
        Neighboring halffaces on the same cell are not included.

        """
        nbrs = set(self.halfface_manifold_neighbors(halfface))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for nbr in nbrs:
                temp += self.halfface_manifold_neighbors(nbr)
            nbrs.update(temp)
            i += 1
        return list(nbrs - set([halfface]))

    def is_halfface_on_boundary(self, halfface):
        """Verify that a face is on the boundary.

        Parameters
        ----------
        halfface : int
            The identifier of the halfface.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        See Also
        --------
        :meth:`is_vertex_on_boundary`, :meth:`is_edge_on_boundary`, :meth:`is_cell_on_boundary`

        """
        u, v, w = self._halfface[halfface][:3]
        return self._plane[w][v][u] is None

    # --------------------------------------------------------------------------
    # Face Geometry
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

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_centroid`, :meth:`face_center`
        :meth:`face_area`, :meth:`face_flatness`, :meth:`face_aspect_ratio`

        """
        return [self.vertex_coordinates(vertex, axes=axes) for vertex in self.face_vertices(face)]

    def face_points(self, face):
        """Compute the points of the vertices of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list[:class:`compas.geometry.Point`]
            The points of the vertices of the face.

        See Also
        --------
        :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_centroid`, :meth:`face_center`

        """
        return [self.vertex_point(vertex) for vertex in self.face_vertices(face)]

    def face_polygon(self, face):
        """Compute the polygon of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            The polygon of the face.

        See Also
        --------
        :meth:`face_points`, :meth:`face_normal`, :meth:`face_centroid`, :meth:`face_center`

        """
        return Polygon(self.face_points(face))

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
        :class:`compas.geometry.Vector`
            The normal vector.

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_centroid`, :meth:`face_center`

        """
        return Vector(*normal_polygon(self.face_coordinates(face), unitized=unitized))

    def face_centroid(self, face):
        """Compute the point at the centroid of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the centroid.

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_center`

        """
        return Point(*centroid_points(self.face_coordinates(face)))

    def face_center(self, face):
        """Compute the point at the center of mass of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the center of mass.

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_centroid`

        """
        return Point(*centroid_polygon(self.face_coordinates(face)))

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

        See Also
        --------
        :meth:`face_flatness`, :meth:`face_aspect_ratio`

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

        See Also
        --------
        :meth:`face_area`, :meth:`face_aspect_ratio`

        Notes
        -----
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

        See Also
        --------
        :meth:`face_area`, :meth:`face_flatness`

        References
        ----------
        .. [1] Wikipedia. *Types of mesh*.
               Available at: https://en.wikipedia.org/wiki/Types_of_mesh.

        """
        face_edge_lengths = [self.edge_length(edge) for edge in self.halfface_halfedges(face)]
        return max(face_edge_lengths) / min(face_edge_lengths)

    halfface_area = face_area
    halfface_centroid = face_centroid
    halfface_center = face_center
    halfface_coordinates = face_coordinates
    halfface_flatness = face_flatness
    halfface_normal = face_normal
    halfface_aspect_ratio = face_aspect_ratio

    # --------------------------------------------------------------------------
    # Cell Accessors
    # --------------------------------------------------------------------------

    def cells(self, data=False):
        """Iterate over the cells of the volmesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the cell attributes in addition to the cell identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next cell identifier.
            If `data` is True, the next cell as a (cell, attr) tuple.

        See Also
        --------
        :meth:`vertices`, :meth:`edges`, :meth:`faces`

        """
        for cell in self._cell:
            if not data:
                yield cell
            else:
                yield cell, self.cell_attributes(cell)

    def cells_where(self, conditions=None, data=False, **kwargs):
        """Get cells for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the cell attributes in addition to the identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next cell that matches the condition.
            If `data` is True, the next cell and its attributes.

        See Also
        --------
        :meth:`cells_where_predicate`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        conditions = conditions or {}
        conditions.update(kwargs)

        for ckey in self.cells():
            is_match = True

            attr = self.cell_attributes(ckey) or {}

            for name, value in conditions.items():
                method = getattr(self, name, None)

                if method and callable(method):
                    val = method(ckey)
                elif name in attr:
                    val = attr[name]
                else:
                    is_match = False
                    break

                if isinstance(val, list):
                    if value not in val:
                        is_match = False
                        break
                elif isinstance(value, (tuple, list)):
                    minval, maxval = value
                    if val < minval or val > maxval:
                        is_match = False
                        break
                else:
                    if value != val:
                        is_match = False
                        break

            if is_match:
                if data:
                    yield ckey, attr
                else:
                    yield ckey

    def cells_where_predicate(self, predicate, data=False):
        """Get cells for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate : callable
            The condition you want to evaluate.
            The callable takes 2 parameters: the cell identifier and the cell attributes, and should return True or False.
        data : bool, optional
            If True, yield the cell attributes in addition to the identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next cell that matches the condition.
            If `data` is True, the next cell and its attributes.

        See Also
        --------
        :meth:`cells_where`
        :meth:`vertices_where_predicate`, :meth:`edges_where_predicate`, :meth:`faces_where_predicate`

        """
        for ckey, attr in self.cells(True):
            if predicate(ckey, attr):
                if data:
                    yield ckey, attr
                else:
                    yield ckey

    # --------------------------------------------------------------------------
    # Cell Attributes
    # --------------------------------------------------------------------------

    def update_default_cell_attributes(self, attr_dict=None, **kwattr):
        """Update the default cell attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_vertex_attributes`, :meth:`update_default_edge_attributes`, :meth:`update_default_face_attributes`

        Notes
        -----
        Named arguments overwrite corresponding cell-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_cell_attributes.update(attr_dict)

    def cell_attribute(self, cell, name, value=None):
        """Get or set an attribute of a cell.

        Parameters
        ----------
        cell : int
            The cell identifier.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.

        Returns
        -------
        object | None
            The value of the attribute, or None when the function is used as a "setter".

        Raises
        ------
        KeyError
            If the cell does not exist.

        See Also
        --------
        :meth:`unset_cell_attribute`
        :meth:`cell_attributes`, :meth:`cells_attribute`, :meth:`cells_attributes`
        :meth:`vertex_attribute`, :meth:`edge_attribute`, :meth:`face_attribute`

        """
        if cell not in self._cell:
            raise KeyError(cell)
        if value is not None:
            if cell not in self._cell_data:
                self._cell_data[cell] = {}
            self._cell_data[cell][name] = value
            return
        if cell in self._cell_data and name in self._cell_data[cell]:
            return self._cell_data[cell][name]
        if name in self.default_cell_attributes:
            return self.default_cell_attributes[name]

    def unset_cell_attribute(self, cell, name):
        """Unset the attribute of a cell.

        Parameters
        ----------
        cell : int
            The cell identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the cell does not exist.

        See Also
        --------
        :meth:`cell_attribute`

        Notes
        -----
        Unsetting the value of a cell attribute implicitly sets it back to the value
        stored in the default cell attribute dict.

        """
        if cell not in self._cell:
            raise KeyError(cell)
        if cell in self._cell_data:
            if name in self._cell_data[cell]:
                del self._cell_data[cell][name]

    def cell_attributes(self, cell, names=None, values=None):
        """Get or set multiple attributes of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty, a dictionary of all attribute name-value pairs of the cell.
            If the parameter `names` is not empty, a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the cell does not exist.

        See Also
        --------
        :meth:`cell_attribute`, :meth:`cells_attribute`, :meth:`cells_attributes`
        :meth:`vertex_attributes`, :meth:`edge_attributes`, :meth:`face_attributes`

        """
        if cell not in self._cell:
            raise KeyError(cell)
        if names and values is not None:
            for name, value in zip(names, values):
                if cell not in self._cell_data:
                    self._cell_data[cell] = {}
                self._cell_data[cell][name] = value
            return
        if not names:
            return CellAttributeView(self.default_cell_attributes, self._cell_data.setdefault(cell, {}))
        values = []
        for name in names:
            value = self.cell_attribute(cell, name)
            values.append(value)
        return values

    def cells_attribute(self, name, value=None, cells=None):
        """Get or set an attribute of multiple cells.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
        cells : list[int], optional
            A list of cell identifiers.

        Returns
        -------
        list[Any] | None
            A list containing the value per face of the requested attribute,
            or None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the cells does not exist.

        See Also
        --------
        :meth:`cell_attribute`, :meth:`cell_attributes`, :meth:`cells_attributes`
        :meth:`vertex_attribute`, :meth:`edge_attribute`, :meth:`face_attribute`

        """
        if not cells:
            cells = self.cells()
        if value is not None:
            for cell in cells:
                self.cell_attribute(cell, name, value)
            return
        return [self.cell_attribute(cell, name) for cell in cells]

    def cells_attributes(self, names=None, values=None, cells=None):
        """Get or set multiple attributes of multiple cells.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        cells : list[int], optional
            A list of cell identifiers.

        Returns
        -------
        list[dict[str, Any]] | list[list[Any]] | None
            If the parameter `names` is empty,
            a list containing per cell an attribute dict with all attributes (default + custom) of the cell.
            If the parameter `names` is empty,
            a list containing per cell a list of attribute values corresponding to the requested names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        See Also
        --------
        :meth:`cell_attribute`, :meth:`cell_attributes`, :meth:`cells_attribute`
        :meth:`vertex_attributes`, :meth:`edge_attributes`, :meth:`face_attributes`

        """
        if not cells:
            cells = self.cells()
        if values is not None:
            for cell in cells:
                self.cell_attributes(cell, names, values)
            return
        return [self.cell_attributes(cell, names) for cell in cells]

    # --------------------------------------------------------------------------
    # Cell Topology
    # --------------------------------------------------------------------------

    def cell_vertices(self, cell):
        """The vertices of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list[int]
            The vertex identifiers of a cell.

        See Also
        --------
        :meth:`cell_edges`, :meth:`cell_faces`, :meth:`cell_halfedges`

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.Mesh.vertices`,
        but in the context of a cell of the `VolMesh`.

        """
        return list(set([vertex for face in self.cell_faces(cell) for vertex in self.halfface_vertices(face)]))

    def cell_halfedges(self, cell):
        """The halfedges of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of a cell.

        See Also
        --------
        :meth:`cell_edges`, :meth:`cell_faces`, :meth:`cell_vertices`

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.Mesh.halfedges`,
        but in the context of a cell of the `VolMesh`.

        """
        halfedges = []
        for face in self.cell_faces(cell):
            halfedges += self.halfface_halfedges(face)
        return halfedges

    def cell_edges(self, cell):
        """Return all edges of a cell.

        Parameters
        ----------
        cell : int
            The cell identifier.

        Returns
        -------
        list[tuple[int, int]]
            The edges of the cell.

        See Also
        --------
        :meth:`cell_halfedges`, :meth:`cell_faces`, :meth:`cell_vertices`

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.Mesh.edges`,
        but in the context of a cell of the `VolMesh`.

        """
        return list(set(self.cell_halfedges(cell)))

    def cell_faces(self, cell):
        """The faces of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        list[int]
            The faces of a cell.

        See Also
        --------
        :meth:`cell_halfedges`, :meth:`cell_edges`, :meth:`cell_vertices`

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.Mesh.faces`,
        but in the context of a cell of the `VolMesh`.

        """
        faces = set()
        for vertex in self._cell[cell]:
            faces.update(self._cell[cell][vertex].values())
        return list(faces)

    def cell_vertex_neighbors(self, cell, vertex):
        """Ordered vertex neighbors of a vertex of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        vertex : int
            Identifier of the vertex.

        Returns
        -------
        list[int]
            The list of neighboring vertices.

        See Also
        --------
        :meth:`cell_vertex_faces`

        Notes
        -----
        All of the returned vertices are part of the cell.

        This method is similar to :meth:`~compas.datastructures.Mesh.vertex_neighbors`,
        but in the context of a cell of the `VolMesh`.

        """
        if vertex not in self.cell_vertices(cell):
            raise KeyError(vertex)
        nbr_vertices = self._cell[cell][vertex].keys()
        v = nbr_vertices[0]
        ordered_vkeys = [v]
        for i in range(len(nbr_vertices) - 1):
            face = self._cell[cell][vertex][v]
            v = self.halfface_vertex_ancestor(face, vertex)
            ordered_vkeys.append(v)
        return ordered_vkeys

    def cell_vertex_faces(self, cell, vertex):
        """Ordered faces connected to a vertex of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        vertex : int
            Identifier of the vertex.

        Returns
        -------
        list[int]
            The ordered list of faces connected to a vertex of a cell.

        See Also
        --------
        :meth:`cell_vertex_neighbors`

        Notes
        -----
        All of the returned faces should are part of the same cell.

        This method is similar to :meth:`~compas.datastructures.Mesh.vertex_faces`,
        but in the context of a cell of the `VolMesh`.

        """
        nbr_vertices = self._cell[cell][vertex].keys()
        u = vertex
        v = nbr_vertices[0]
        ordered_faces = []
        for i in range(len(nbr_vertices)):
            face = self._cell[cell][u][v]
            v = self.halfface_vertex_ancestor(face, u)
            ordered_faces.append(face)
        return ordered_faces

    def cell_halfedge_face(self, cell, halfedge):
        """Find the face corresponding to a specific halfedge of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.
        halfedge : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        int
            The identifier of the face.

        See Also
        --------
        :meth:`cell_halfedge_opposite_face`

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.Mesh.halfedge_face`,
        but in the context of a cell of the `VolMesh`.

        """
        u, v = halfedge
        return self._cell[cell][u][v]

    def cell_halfedge_opposite_face(self, cell, halfedge):
        """Find the opposite face corresponding to a specific halfedge of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.
        halfedge : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        int
            The identifier of the face.

        See Also
        --------
        :meth:`cell_halfedge_face`

        """
        u, v = halfedge
        return self._cell[cell][v][u]

    def cell_face_neighbors(self, cell, face):
        """Find the faces adjacent to a given face of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.
        face : int
            The identifier of the face.

        Returns
        -------
        int
            The identifier of the face.

        See Also
        --------
        :meth:`cell_neighbors`

        Notes
        -----
        This method is similar to :meth:`~compas.datastructures.Mesh.face_neighbors`,
        but in the context of a cell of the `VolMesh`.

        """
        nbrs = []
        for halfedge in self.halfface_halfedges(face):
            nbr = self.cell_halfedge_opposite_face(cell, halfedge)
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def cell_neighbors(self, cell):
        """Find the neighbors of a given cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        list[int]
            The identifiers of the adjacent cells.

        See Also
        --------
        :meth:`cell_face_neighbors`

        """
        nbrs = []
        for u in self._cell[cell]:
            for face in self._cell[cell][u].values():
                a, b, c = self._halfface[face][:3]
                nbr = self._plane[c][b][a]
                if nbr is not None:
                    nbrs.append(nbr)
        return nbrs

    def is_cell_on_boundary(self, cell):
        """Verify that a cell is on the boundary.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        See Also
        --------
        :meth:`is_vertex_on_boundary`, :meth:`is_edge_on_boundary`, :meth:`is_face_on_boundary`

        """
        faces = self.cell_faces(cell)
        for face in faces:
            if self.is_halfface_on_boundary(face):
                return True
        return False

    # --------------------------------------------------------------------------
    # Cell Geometry
    # --------------------------------------------------------------------------

    def cell_points(self, cell):
        """Compute the points of the vertices of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        list[:class:`compas.geometry.Point`]
            The points of the vertices of the cell.

        See Also
        --------
        :meth:`cell_lines`, :meth:`cell_polygons`

        """
        return [self.vertex_point(vertex) for vertex in self.cell_vertices(cell)]

    def cell_lines(self, cell):
        """Compute the lines of the edges of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        list[:class:`compas.geometry.Line`]
            The lines of the edges of the cell.

        See Also
        --------
        :meth:`cell_points`, :meth:`cell_polygons`

        """
        return [self.edge_line(edge) for edge in self.cell_edges(cell)]

    def cell_polygons(self, cell):
        """Compute the polygons of the faces of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        list[:class:`compas.geometry.Polygon`]
            The polygons of the faces of the cell.

        See Also
        --------
        :meth:`cell_points`, :meth:`cell_lines`

        """
        return [self.face_polygon(face) for face in self.cell_faces(cell)]

    def cell_centroid(self, cell):
        """Compute the point at the centroid of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the centroid.

        See Also
        --------
        :meth:`cell_center`

        """
        vertices = self.cell_vertices(cell)
        return Point(*centroid_points([self.vertex_coordinates(vertex) for vertex in vertices]))

    def cell_center(self, cell):
        """Compute the point at the center of mass of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        :class:`compas.geometry.Point`
            The coordinates of the center of mass.

        See Also
        --------
        :meth:`cell_centroid`

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Point(*centroid_polyhedron((vertices, faces)))

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
        :class:`compas.geometry.Vector`
            The components of the normal vector.

        """
        cell_faces = self.cell_faces(cell)
        vectors = [self.face_normal(face) for face in self.vertex_halffaces(vertex) if face in cell_faces]
        return Vector(*normalize_vector(centroid_points(vectors)))

    def cell_polyhedron(self, cell):
        """Construct a polyhedron from the vertices and faces of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        :class:`compas.geometry.Polyhedron`
            The polyhedron.

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Polyhedron(vertices, faces)

    # --------------------------------------------------------------------------
    # Boundaries
    # --------------------------------------------------------------------------

    def vertices_on_boundaries(self):
        """Find the vertices on the boundary.

        Returns
        -------
        list[int]
            The vertices of the boundary.

        See Also
        --------
        :meth:`faces_on_boundaries`, :meth:`cells_on_boundaries`

        """
        vertices = set()
        for face in self._halfface:
            if self.is_halfface_on_boundary(face):
                vertices.update(self.halfface_vertices(face))
        return list(vertices)

    def halffaces_on_boundaries(self):
        """Find the faces on the boundary.

        Returns
        -------
        list[int]
            The faces of the boundary.

        See Also
        --------
        :meth:`vertices_on_boundaries`, :meth:`cells_on_boundaries`

        """
        faces = set()
        for face in self._halfface:
            if self.is_halfface_on_boundary(face):
                faces.add(face)
        return list(faces)

    def cells_on_boundaries(self):
        """Find the cells on the boundary.

        Returns
        -------
        list[int]
            The cells of the boundary.

        See Also
        --------
        :meth:`vertices_on_boundaries`, :meth:`faces_on_boundaries`

        """
        cells = set()
        for face in self.halffaces_on_boundaries():
            cells.add(self.halfface_cell(face))
        return list(cells)

    # --------------------------------------------------------------------------
    # Transformations
    # --------------------------------------------------------------------------

    def transform(self, T):
        """Transform the mesh.

        Parameters
        ----------
        T : :class:`Transformation`
            The transformation used to transform the mesh.

        Returns
        -------
        None
            The mesh is modified in-place.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> from compas.geometry import matrix_from_axis_and_angle
        >>> mesh = Mesh.from_polyhedron(6)
        >>> T = matrix_from_axis_and_angle([0, 0, 1], math.pi / 4)
        >>> mesh.transform(T)

        """
        points = transform_points(self.vertices_attributes("xyz"), T)
        for vertex, point in zip(self.vertices(), points):
            self.vertex_attributes(vertex, "xyz", point)
