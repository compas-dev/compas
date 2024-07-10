# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from ast import literal_eval
from random import sample

from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.datastructures.attributes import CellAttributeView
from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import FaceAttributeView
from compas.datastructures.attributes import VertexAttributeView
from compas.datastructures.datastructure import Datastructure
from compas.files import OBJ
from compas.geometry import Line
from compas.geometry import Plane
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
from compas.geometry import project_point_plane
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import volume_polyhedron
from compas.itertools import pairwise
from compas.tolerance import TOL


class CellNetwork(Datastructure):
    """Geometric implementation of a data structure for a collection of mixed topologic entities such as cells, faces, edges and nodes.

    Parameters
    ----------
    default_vertex_attributes: dict, optional
        Default values for vertex attributes.
    default_edge_attributes: dict, optional
        Default values for edge attributes.
    default_face_attributes: dict, optional
        Default values for face attributes.
    default_cell_attributes: dict, optional
        Default values for cell attributes.
    name : str, optional
        The name of the cell network.
    **kwargs : dict, optional
        Additional keyword arguments, which are stored in the attributes dict.

    Attributes
    ----------
    default_vertex_attributes : dict[str, Any]
        Default attributes of the vertices.
    default_edge_attributes: dict[str, Any]
        Default values for edge attributes.
    default_face_attributes: dict[str, Any]
        Default values for face attributes.
    default_cell_attributes: dict[str, Any]
        Default values for cell attributes.

    Examples
    --------
    >>> from compas.datastructures import CellNetwork
    >>> cell_network = CellNetwork()
    >>> vertices = [(0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0), (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]
    >>> faces = [[0, 1, 2, 3], [0, 3, 5, 4], [3, 2, 6, 5], [2, 1, 7, 6], [1, 0, 4, 7], [4, 5, 6, 7]]
    >>> cells = [[0, 1, 2, 3, 4, 5]]
    >>> for x, y, z in vertices:
    ...     vertex = cell_network.add_vertex(x=x, y=y, z=z)
    >>> for face_vertices in faces:
    ...     face = cell_network.add_face(face_vertices)
    >>> for cell_faces in cells:
    ...     cell = cell_network.add_cell(cell_faces)
    >>> print(cell_network)
    <CellNetwork with 8 vertices, 6 faces, 1 cells, 12 edges>

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
            "edge": {
                "type": "object",
                "patternProperties": {
                    "^[0-9]+$": {
                        "type": "object",
                        "patternProperties": {"^[0-9]+$": {"type": "object"}},
                        "additionalProperties": False,
                    }
                },
                "additionalProperties": False,
            },
            "face": {
                "type": "object",
                "patternProperties": {
                    "^[0-9]+$": {
                        "type": "array",
                        "items": {"type": "integer", "minimum": 0},
                        "minItems": 3,
                    }
                },
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
                "patternProperties": {"^\\([0-9]+(, [0-9]+){3, }\\)$": {"type": "object"}},
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
            "default_cell_attributes",
            "vertex",
            "edge",
            "face",
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
        cell = {}
        for c in self._cell:
            faces = set()
            for u in self._cell[c]:
                for v in self._cell[c][u]:
                    faces.add(self._cell[c][u][v])
            cell[c] = sorted(list(faces))

        return {
            "attributes": self.attributes,
            "default_vertex_attributes": self.default_vertex_attributes,
            "default_edge_attributes": self.default_edge_attributes,
            "default_face_attributes": self.default_face_attributes,
            "default_cell_attributes": self.default_cell_attributes,
            "vertex": self._vertex,
            "edge": self._edge,
            "face": self._face,
            "cell": cell,
            "edge_data": {str(k): v for k, v in self._edge_data.items()},
            "face_data": self._face_data,
            "cell_data": self._cell_data,
            "max_vertex": self._max_vertex,
            "max_face": self._max_face,
            "max_cell": self._max_cell,
        }

    @classmethod
    def __from_data__(cls, data):
        cell_network = cls(
            default_vertex_attributes=data.get("default_vertex_attributes"),
            default_edge_attributes=data.get("default_edge_attributes"),
            default_face_attributes=data.get("default_face_attributes"),
            default_cell_attributes=data.get("default_cell_attributes"),
        )
        cell_network.attributes.update(data.get("attributes") or {})

        vertex = data["vertex"] or {}
        edge = data["edge"] or {}
        face = data["face"] or {}
        cell = data["cell"] or {}

        for key, attr in iter(vertex.items()):
            cell_network.add_vertex(key=int(key), attr_dict=attr)

        edge_data = {literal_eval(k): v for k, v in data.get("edge_data", {}).items()}
        for u in edge:
            for v in edge[u]:
                attr = edge_data.get(tuple(sorted((int(u), int(v)))), {})
                cell_network.add_edge(int(u), int(v), attr_dict=attr)

        face_data = data.get("face_data") or {}
        for key, vertices in iter(face.items()):
            cell_network.add_face(vertices, fkey=int(key), attr_dict=face_data.get(key))

        cell_data = data.get("cell_data") or {}
        for ckey, faces in iter(cell.items()):
            cell_network.add_cell(faces, ckey=int(ckey), attr_dict=cell_data.get(ckey))

        cell_network._max_vertex = data.get("max_vertex", cell_network._max_vertex)
        cell_network._max_face = data.get("max_face", cell_network._max_face)
        cell_network._max_cell = data.get("max_cell", cell_network._max_cell)

        return cell_network

    def __init__(self, default_vertex_attributes=None, default_edge_attributes=None, default_face_attributes=None, default_cell_attributes=None, name=None, **kwargs):  # fmt: skip
        super(CellNetwork, self).__init__(kwargs, name=name)
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1
        self._vertex = {}
        self._edge = {}
        self._face = {}
        self._plane = {}
        self._cell = {}
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
        tpl = "<CellNetwork with {} vertices, {} faces, {} cells, {} edges>"
        return tpl.format(
            self.number_of_vertices(),
            self.number_of_faces(),
            self.number_of_cells(),
            self.number_of_edges(),
        )

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    def clear(self):
        """Clear all the volmesh data.

        Returns
        -------
        None

        """
        del self._vertex
        del self._edge
        del self._face
        del self._cell
        del self._plane
        del self._face_data
        del self._cell_data
        self._vertex = {}
        self._edge = {}
        self._face = {}
        self._cell = {}
        self._plane = {}
        self._face_data = {}
        self._cell_data = {}
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1

    def vertex_sample(self, size=1):
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
        return sample(list(self.vertices()), size)

    def edge_sample(self, size=1):
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
        return sample(list(self.edges()), size)

    def face_sample(self, size=1):
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
        return sample(list(self.faces()), size)

    def cell_sample(self, size=1):
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
        return sample(list(self.cells()), size)

    def vertex_index(self):
        """Returns a dictionary that maps vertex identifiers to the corresponding index in a vertex list or array.

        Returns
        -------
        dict[int, int]
            A dictionary of vertex-index pairs.

        See Also
        --------
        :meth:`index_vertex`

        """
        return {key: index for index, key in enumerate(self.vertices())}

    def index_vertex(self):
        """Returns a dictionary that maps the indices of a vertex list to vertex identifiers.

        Returns
        -------
        dict[int, int]
            A dictionary of index-vertex pairs.

        See Also
        --------
        :meth:`vertex_index`

        """
        return dict(enumerate(self.vertices()))

    def vertex_gkey(self, precision=None):
        """Returns a dictionary that maps vertex identifiers to the corresponding *geometric key* up to a certain precision.

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
        return {vertex: gkey(xyz(vertex), precision) for vertex in self.vertices()}

    def gkey_vertex(self, precision=None):
        """Returns a dictionary that maps *geometric keys* of a certain precision to the corresponding vertex identifiers.

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
        return {gkey(xyz(vertex), precision): vertex for vertex in self.vertices()}

    # --------------------------------------------------------------------------
    # Builders
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex and specify its attributes.

        Parameters
        ----------
        key : int, optional
            The identifier of the vertex.
            Defaults to None.
        attr_dict : dict, optional
            A dictionary of vertex attributes.
            Defaults to None.
        **kwattr : dict, optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The identifier of the vertex.

        See Also
        --------
        :meth:`add_face`, :meth:`add_cell`, :meth:`add_edge`

        """
        if key is None:
            key = self._max_vertex = self._max_vertex + 1
        key = int(key)
        if key > self._max_vertex:
            self._max_vertex = key

        if key not in self._vertex:
            self._vertex[key] = {}
            self._edge[key] = {}
            self._plane[key] = {}

        attr = attr_dict or {}
        attr.update(kwattr)
        self._vertex[key].update(attr)

        return key

    def add_edge(self, u, v, attr_dict=None, **kwattr):
        """Add an edge and specify its attributes.

        Parameters
        ----------
        u : int
            The identifier of the first node of the edge.
        v : int
            The identifier of the second node of the edge.
        attr_dict : dict[str, Any], optional
            A dictionary of edge attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        tuple[int, int]
            The identifier of the edge.

        Raises
        ------
        ValueError
            If either of the vertices of the edge does not exist.

        Notes
        -----
        Edges can be added independently from faces or cells.
        However, whenever a face is added all edges of that face are added as well.

        """
        if u not in self._vertex:
            raise ValueError("Cannot add edge {}, {} has no vertex {}".format((u, v), self.name, u))
        if v not in self._vertex:
            raise ValueError("Cannot add edge {}, {} has no vertex {}".format((u, v), self.name, u))

        attr = attr_dict or {}
        attr.update(kwattr)

        uv = tuple(sorted((u, v)))

        data = self._edge_data.get(uv, {})
        data.update(attr)
        self._edge_data[uv] = data

        # @Romana
        # should the data not be added to this edge as well?
        # if that is the case, should we not store the data in an edge_data dict to avoid duplication?
        # True, but then _edge does not hold anything, we could also store the attr right here.
        # but I leave this to you as you have a better overview

        if v not in self._edge[u]:
            self._edge[v][u] = {}
        if v not in self._plane[u]:
            self._plane[u][v] = {}
        if u not in self._plane[v]:
            self._plane[v][u] = {}

        return u, v

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the cell network.

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

        See Also
        --------
        :meth:`add_vertex`, :meth:`add_cell`, :meth:`add_edge`

        Notes
        -----
        If no key is provided for the face, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        All edges of the faces are automatically added if they don't exsit yet.
        The vertices of the face should form a continuous closed loop.
        However, the cycle direction doesn't matter.

        """
        if len(vertices) < 3:
            return

        if vertices[-1] == vertices[0]:
            vertices = vertices[:-1]
        vertices = [int(key) for key in vertices]

        if fkey is None:
            fkey = self._max_face = self._max_face + 1
        fkey = int(fkey)
        if fkey > self._max_face:
            self._max_face = fkey

        self._face[fkey] = vertices

        attr = attr_dict or {}
        attr.update(kwattr)
        for name, value in attr.items():
            self.face_attribute(fkey, name, value)

        for u, v in pairwise(vertices + vertices[:1]):
            if v not in self._plane[u]:
                self._plane[u][v] = {}
            self._plane[u][v][fkey] = None

            if u not in self._plane[v]:
                self._plane[v][u] = {}
            self._plane[v][u][fkey] = None

            self.add_edge(u, v)

        return fkey

    def _faces_to_unified_mesh(self, faces):
        faces = list(set(faces))
        # 0. Check if all the faces have been added
        for face in faces:
            if face not in self._face:
                raise ValueError("Face {} does not exist.".format(face))
        # 2. Check if the faces can be unified
        mesh = self.faces_to_mesh(faces, data=False)
        try:
            mesh.unify_cycles()
        except Exception:
            return None
        return mesh

    def is_faces_closed(self, faces):
        """Checks if the faces form a closed cell."""
        mesh = self._faces_to_unified_mesh(faces)
        if mesh:
            return True
        return False

    def add_cell(self, faces, ckey=None, attr_dict=None, **kwattr):
        """Add a cell to the cell network object.

        In order to add a valid cell to the network, the faces must form a closed mesh.
        If the faces do not form a closed mesh, the cell is not added to the network.

        Parameters
        ----------
        faces : list[int]
            The face keys of the cell.
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
        ValueError
            If something is wrong with the passed faces.
        TypeError
            If the provided cell key is not an integer.

        Notes
        -----
        If no key is provided for the cell, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        """
        mesh = self._faces_to_unified_mesh(faces)
        if mesh is None:
            raise ValueError("Cannot add cell, faces {} do not form a closed cell.".format(faces))

        # 3. Check if the faces are oriented correctly
        # If the volume of the polyhedron is positive, we need to flip the faces to point inwards
        volume = volume_polyhedron(mesh.to_vertices_and_faces())
        if volume > 0:
            mesh.flip_cycles()

        if ckey is None:
            ckey = self._max_cell = self._max_cell + 1
        ckey = int(ckey)
        if ckey > self._max_cell:
            self._max_cell = ckey

        self._cell[ckey] = {}

        attr = attr_dict or {}
        attr.update(kwattr)
        for name, value in attr.items():
            self.cell_attribute(ckey, name, value)

        for fkey in mesh.faces():
            vertices = mesh.face_vertices(fkey)
            for u, v in pairwise(vertices + vertices[:1]):
                if u not in self._cell[ckey]:
                    self._cell[ckey][u] = {}
                self._plane[u][v][fkey] = ckey
                self._cell[ckey][u][v] = fkey

        return ckey

    # --------------------------------------------------------------------------
    # Modifiers
    # --------------------------------------------------------------------------

    # def delete_vertex(self, vertex):
    #     """Delete a vertex from the cell network and everything that is attached to it.

    #     Parameters
    #     ----------
    #     vertex : int
    #         The identifier of the vertex.

    #     Returns
    #     -------
    #     None

    #     See Also
    #     --------
    #     :meth:`delete_halfface`, :meth:`delete_cell`

    #     """
    #     for cell in self.vertex_cells(vertex):
    #         self.delete_cell(cell)

    def delete_edge(self, edge):
        """Delete an edge from the cell network.

        Parameters
        ----------
        edge : tuple
            The identifier of the edge.

        Returns
        -------
        None

        """
        u, v = edge
        if self._plane[u] and v in self._plane[u]:
            faces = self._plane[u][v].keys()
            if len(faces) > 0:
                print("Cannot delete edge %s, delete faces %s first" % (edge, list(faces)))
                return
        if self._plane[v] and u in self._plane[v]:
            faces = self._plane[v][u].keys()
            if len(faces) > 0:
                print("Cannot delete edge %s, delete faces %s first" % (edge, list(faces)))
                return
        if v in self._edge[u]:
            del self._edge[u][v]
        if u in self._edge[v]:
            del self._edge[v][u]
        if v in self._plane[u]:
            del self._plane[u][v]
        if u in self._plane[v]:
            del self._plane[v][u]

    def delete_face(self, face):
        """Delete a face from the cell network.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        None
        """
        vertices = self.face_vertices(face)
        # check first
        for u, v in pairwise(vertices + vertices[:1]):
            if self._plane[u][v][face] is not None:
                print("Cannot delete face %d, delete cell %s first" % (face, self._plane[u][v][face]))
                return
            if self._plane[v][u][face] is not None:
                print("Cannot delete face %d, delete cell %s first" % (face, self._plane[v][u][face]))
                return
        for u, v in pairwise(vertices + vertices[:1]):
            del self._plane[u][v][face]
            del self._plane[v][u][face]
        del self._face[face]
        if face in self._face_data:
            del self._face_data[face]

    def delete_cell(self, cell):
        """Delete a cell from the cell network.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        None

        See Also
        --------
        :meth:`delete_vertex`, :meth:`delete_halfface`

        """
        # remove the cell from the faces
        cell_faces = self.cell_faces(cell)
        for face in cell_faces:
            vertices = self.face_vertices(face)
            for u, v in pairwise(vertices + vertices[:1]):
                if self._plane[u][v][face] == cell:
                    self._plane[u][v][face] = None
                if self._plane[v][u][face] == cell:
                    self._plane[v][u][face] = None
        del self._cell[cell]
        if cell in self._cell_data:
            del self._cell_data[cell]

    # def remove_unused_vertices(self):
    #     """Remove all unused vertices from the cell network object.

    #     Returns
    #     -------
    #     None

    #     """
    #     for vertex in list(self.vertices()):
    #         if vertex not in self._plane:
    #             del self._vertex[vertex]
    #         else:
    #             if not self._plane[vertex]:
    #                 del self._vertex[vertex]
    #                 del self._plane[vertex]

    # --------------------------------------------------------------------------
    # Constructors
    # --------------------------------------------------------------------------

    # @classmethod
    # def from_meshgrid(cls, dx=10, dy=None, dz=None, nx=10, ny=None, nz=None):
    #     """Construct a cell network from a 3D meshgrid.

    #     Parameters
    #     ----------
    #     dx : float, optional
    #         The size of the grid in the x direction.
    #     dy : float, optional
    #         The size of the grid in the y direction.
    #         Defaults to the value of `dx`.
    #     dz : float, optional
    #         The size of the grid in the z direction.
    #         Defaults to the value of `dx`.
    #     nx : int, optional
    #         The number of elements in the x direction.
    #     ny : int, optional
    #         The number of elements in the y direction.
    #         Defaults to the value of `nx`.
    #     nz : int, optional
    #         The number of elements in the z direction.
    #         Defaults to the value of `nx`.

    #     Returns
    #     -------
    #     :class:`compas.datastructures.VolMesh`

    #     See Also
    #     --------
    #     :meth:`from_obj`, :meth:`from_vertices_and_cells`

    #     """
    #     dy = dy or dx
    #     dz = dz or dx
    #     ny = ny or nx
    #     nz = nz or nx

    #     vertices = [
    #         [x, y, z]
    #         for z, x, y in product(
    #             linspace(0, dz, nz + 1),
    #             linspace(0, dx, nx + 1),
    #             linspace(0, dy, ny + 1),
    #         )
    #     ]
    #     cells = []
    #     for k, i, j in product(range(nz), range(nx), range(ny)):
    #         a = k * ((nx + 1) * (ny + 1)) + i * (ny + 1) + j
    #         b = k * ((nx + 1) * (ny + 1)) + (i + 1) * (ny + 1) + j
    #         c = k * ((nx + 1) * (ny + 1)) + (i + 1) * (ny + 1) + j + 1
    #         d = k * ((nx + 1) * (ny + 1)) + i * (ny + 1) + j + 1
    #         aa = (k + 1) * ((nx + 1) * (ny + 1)) + i * (ny + 1) + j
    #         bb = (k + 1) * ((nx + 1) * (ny + 1)) + (i + 1) * (ny + 1) + j
    #         cc = (k + 1) * ((nx + 1) * (ny + 1)) + (i + 1) * (ny + 1) + j + 1
    #         dd = (k + 1) * ((nx + 1) * (ny + 1)) + i * (ny + 1) + j + 1
    #         bottom = [d, c, b, a]
    #         front = [a, b, bb, aa]
    #         right = [b, c, cc, bb]
    #         left = [a, aa, dd, d]
    #         back = [c, d, dd, cc]
    #         top = [aa, bb, cc, dd]
    #         cells.append([bottom, front, left, back, right, top])

    #     return cls.from_vertices_and_cells(vertices, cells)

    @classmethod
    def from_obj(cls, filepath, precision=None):
        """Construct a cell network object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : path string | file-like object | URL string
            A path, a file-like object or a URL pointing to a file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        :class:`compas.datastructures.VolMesh`
            A cell network object.

        See Also
        --------
        :meth:`to_obj`
        :meth:`from_meshgrid`, :meth:`from_vertices_and_cells`
        :class:`compas.files.OBJ`

        """
        obj = OBJ(filepath, precision)
        vertices = obj.parser.vertices or []  # type: ignore
        faces = obj.parser.faces or []  # type: ignore
        groups = obj.parser.groups or []  # type: ignore
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

    @classmethod
    def from_vertices_and_cells(cls, vertices, cells):
        """Construct a cell network object from vertices and cells.

        Parameters
        ----------
        vertices : list[list[float]]
            Ordered list of vertices, represented by their XYZ coordinates.
        cells : list[list[list[int]]]
            List of cells defined by their faces.

        Returns
        -------
        :class:`compas.datastructures.VolMesh`
            A cell network object.

        See Also
        --------
        :meth:`to_vertices_and_cells`
        :meth:`from_obj`

        """
        cellnetwork = cls()
        for x, y, z in vertices:
            cellnetwork.add_vertex(x=x, y=y, z=z)
        for cell in cells:
            faces = []
            for vertices in cell:
                face = cellnetwork.add_face(vertices)
                faces.append(face)
            cellnetwork.add_cell(faces)
        return cellnetwork

    # --------------------------------------------------------------------------
    # Conversions
    # --------------------------------------------------------------------------

    # def to_obj(self, filepath, precision=None, **kwargs):
    #     """Write the cell network to an OBJ file.

    #     Parameters
    #     ----------
    #     filepath : path string | file-like object
    #         A path or a file-like object pointing to a file.
    #     precision: str, optional
    #         The precision of the geometric map that is used to connect the lines.
    #     unweld : bool, optional
    #         If True, all faces have their own unique vertices.
    #         If False, vertices are shared between faces if this is also the case in the mesh.
    #         Default is False.

    #     Returns
    #     -------
    #     None

    #     See Also
    #     --------
    #     :meth:`from_obj`

    #     Warnings
    #     --------
    #     This function only writes geometric data about the vertices and
    #     the faces to the file.

    #     """
    #     obj = OBJ(filepath, precision=precision)
    #     obj.write(self, **kwargs)

    # def to_vertices_and_cells(self):
    #     """Return the vertices and cells of a cell network.

    #     Returns
    #     -------
    #     list[list[float]]
    #         A list of vertices, represented by their XYZ coordinates.
    #     list[list[list[int]]]
    #         A list of cells, with each cell a list of faces, and each face a list of vertex indices.

    #     See Also
    #     --------
    #     :meth:`from_vertices_and_cells`

    #     """
    #     vertex_index = self.vertex_index()
    #     vertices = [self.vertex_coordinates(vertex) for vertex in self.vertices()]
    #     cells = []
    #     for cell in self.cells():
    #         faces = [
    #             [vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in self.cell_faces(cell)
    #         ]
    #         cells.append(faces)
    #     return vertices, cells

    def edges_to_graph(self):
        """Convert the edges of the cell network to a graph.

        Returns
        -------
        :class:`compas.datastructures.Graph`
            A graph object.

        """
        graph = Graph()
        for vertex, attr in self.vertices(data=True):
            x, y, z = self.vertex_coordinates(vertex)
            graph.add_node(key=vertex, x=x, y=y, z=z, attr_dict=attr)
        for (u, v), attr in self.edges(data=True):
            graph.add_edge(u, v, attr_dict=attr)
        return graph

    def cells_to_graph(self):
        """Convert the cells the cell network to a graph.

        Returns
        -------
        :class:`compas.datastructures.Graph`
            A graph object.

        """
        graph = Graph()
        for cell, attr in self.cells(data=True):
            x, y, z = self.cell_centroid(cell)
            graph.add_node(key=cell, x=x, y=y, z=z, attr_dict=attr)
        for cell in self.cells():
            for nbr in self.cell_neighbors(cell):
                graph.add_edge(*sorted([cell, nbr]))
        return graph

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

        See Also
        --------
        :meth:`cell_to_mesh`

        """
        vertices = self.cell_vertices(cell)
        faces = self.cell_faces(cell)
        vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
        vertices = [self.vertex_coordinates(vertex) for vertex in vertices]
        faces = []
        for face in self.cell_faces(cell):
            faces.append([vertex_index[vertex] for vertex in self.cell_face_vertices(cell, face)])
        return vertices, faces

    def cell_to_mesh(self, cell):
        """Construct a mesh object from from a cell of a cell network.

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

    def faces_to_mesh(self, faces, data=False):
        """Construct a mesh from a list of faces.

        Parameters
        ----------
        faces : list
            A list of face identifiers.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh.

        """
        faces_vertices = [self.face_vertices(face) for face in faces]
        mesh = Mesh()
        for fkey, vertices in zip(faces, faces_vertices):
            for v in vertices:
                x, y, z = self.vertex_coordinates(v)
                mesh.add_vertex(key=v, x=x, y=y, z=z)
            if data:
                mesh.add_face(vertices, fkey=fkey, attr_dict=self.face_attributes(fkey))
            else:
                mesh.add_face(vertices, fkey=fkey)
        return mesh

    # --------------------------------------------------------------------------
    # General
    # --------------------------------------------------------------------------

    def centroid(self):
        """Compute the centroid of the cell network.

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
        list[[float, float, float]]
            XYZ coordinates of 8 points defining a box.

        """
        xyz = self.vertices_attributes("xyz")
        return bounding_box(xyz)

    def number_of_vertices(self):
        """Count the number of vertices in the cell network.

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
        """Count the number of edges in the cell network.

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
        """Count the number of faces in the cell network.

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
        """Count the number of faces in the cell network.

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
        """Verify that the cell network is valid.

        Returns
        -------
        bool
            True if the cell network is valid.
            False otherwise.

        """
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # Vertex Accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Iterate over the vertices of the cell network.

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
        """Verify that a vertex is in the cell network.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is in the cell network.
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
        return self._edge[vertex].keys()

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

    def vertex_faces(self, vertex):
        """Return all faces connected to a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of faces connected to a vertex.

        See Also
        --------
        :meth:`vertex_neighbors`, :meth:`vertex_cells`

        """
        faces = []
        for nbr in self._plane[vertex]:
            for face in self._plane[vertex][nbr]:
                if face is not None:
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
        cells = set()
        for nbr in self._plane[vertex]:
            for cell in self._plane[vertex][nbr].values():
                if cell is not None:
                    cells.add(cell)
        return list(cells)

    # def is_vertex_on_boundary(self, vertex):
    #     """Verify that a vertex is on a boundary.

    #     Parameters
    #     ----------
    #     vertex : int
    #         The identifier of the vertex.

    #     Returns
    #     -------
    #     bool
    #         True if the vertex is on the boundary.
    #         False otherwise.

    #     See Also
    #     --------
    #     :meth:`is_edge_on_boundary`, :meth:`is_face_on_boundary`, :meth:`is_cell_on_boundary`

    #     """
    #     halffaces = self.vertex_halffaces(vertex)
    #     for halfface in halffaces:
    #         if self.is_halfface_on_boundary(halfface):
    #             return True
    #     return False

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
        """
        return [self._vertex[vertex][axis] for axis in axes]

    def vertices_coordinates(self, vertices, axes="xyz"):
        """Return the coordinates of multiple vertices.

        Parameters
        ----------
        vertices : list of int
            The vertex identifiers.
        axes : str, optional
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list of list[float]
            Coordinates of the vertices.
        """
        return [self.vertex_coordinates(vertex, axes=axes) for vertex in vertices]

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
        """
        return Point(*self.vertex_coordinates(vertex))

    def vertices_points(self, vertices):
        """Returns the point representation of multiple vertices.

        Parameters
        ----------
         vertices : list of int
            The vertex identifiers.

        Returns
        -------
        list of :class:`compas.geometry.Point`
            The points.
        """
        return [self.vertex_point(vertex) for vertex in vertices]

    # --------------------------------------------------------------------------
    # Edge Accessors
    # --------------------------------------------------------------------------

    def edges(self, data=False):
        """Iterate over the edges of the cell network.

        Parameters
        ----------
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge identifier (u, v).
            If `data` is True, the next edge identifier and its attributes as a ((u, v), attr) tuple.

        """
        seen = set()
        for u, nbrs in iter(self._edge.items()):
            for v in nbrs:
                if (u, v) in seen or (v, u) in seen:
                    continue
                seen.add((u, v))
                seen.add((v, u))
                if data:
                    attr = self._edge_data[tuple(sorted([u, v]))]
                    yield (u, v), attr
                else:
                    yield u, v

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
        """
        if not self.has_edge(edge):
            raise KeyError(edge)

        attr = self._edge_data.get(tuple(sorted(edge)), {})

        if value is not None:
            attr.update({name: value})
            self._edge_data[tuple(sorted(edge))] = attr
            return
        if name in attr:
            return attr[name]
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
        if not self.has_edge(edge):
            raise KeyError(edge)

        del self._edge_data[tuple(sorted(edge))][name]

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
        if not self.has_edge(edge):
            raise KeyError(edge)

        if names and values:
            for name, value in zip(names, values):
                self._edge_data[tuple(sorted(edge))][name] = value
            return
        if not names:
            return EdgeAttributeView(self.default_edge_attributes, self._edge_data[tuple(sorted(edge))])
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

    def has_edge(self, edge, directed=False):
        """Verify that the cell network contains a directed edge (u, v).

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.
        directed : bool, optional
            If ``True``, the direction of the edge should be taken into account.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.

        See Also
        --------
        :meth:`has_vertex`, :meth:`has_face`, :meth:`has_cell`

        """
        u, v = edge
        if directed:
            return u in self._edge and v in self._edge[u]
        return (u in self._edge and v in self._edge[u]) or (v in self._edge and u in self._edge[v])

    def edge_faces(self, edge):
        """Return the faces adjacent to an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The edge identifier.

        Returns
        -------
        list[int]
            The identifiers of the adjacent faces.
        """
        u, v = edge
        faces = set()
        if v in self._plane[u]:
            faces.update(self._plane[u][v].keys())
        if u in self._plane[v]:
            faces.update(self._plane[v][u].keys())
        return sorted(list(faces))

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
        # @Roman: should v, u also be checked?
        u, v = edge
        cells = []
        for cell in self._plane[u][v].values():
            if cell is not None:
                cells.append(cell)
        return cells

    # def is_edge_on_boundary(self, edge):
    #     """Verify that an edge is on the boundary.

    #     Parameters
    #     ----------
    #     edge : tuple[int, int]
    #         The identifier of the edge.

    #     Returns
    #     -------
    #     bool
    #         True if the edge is on the boundary.
    #         False otherwise.

    #     See Also
    #     --------
    #     :meth:`is_vertex_on_boundary`, :meth:`is_face_on_boundary`, :meth:`is_cell_on_boundary`

    #     Notes
    #     -----
    #     This method simply checks if u-v or v-u is on the edge of the cell network.
    #     The direction u-v does not matter.

    #     """
    #     u, v = edge
    #     return None in self._plane[u][v].values()

    def edges_without_face(self):
        """Find the edges that are not part of a face.

        Returns
        -------
        list[int]
            The edges without face.

        """
        edges = {edge for edge in self.edges() if not self.edge_faces(edge)}
        return list(edges)

    def nonmanifold_edges(self):
        """Returns the edges that belong to more than two faces.

        Returns
        -------
        list[int]
            The edges without face.

        """
        edges = {edge for edge in self.edges() if len(self.edge_faces(edge)) > 2}
        return list(edges)

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
        """
        return Line(*self.edge_coordinates(edge))

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
    # Face Accessors
    # --------------------------------------------------------------------------

    def faces(self, data=False):
        """Iterate over the halffaces of the cell network and yield faces.

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
        for face in self._face:
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
        if face not in self._face:
            raise KeyError(face)

        if value is not None:
            if face not in self._face_data:
                self._face_data[face] = {}
            self._face_data[face][name] = value
            return
        if face in self._face_data and name in self._face_data[face]:
            return self._face_data[face][name]
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
        if face not in self._face:
            raise KeyError(face)

        if face in self._face_data and name in self._face_data[face]:
            del self._face_data[face][name]

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
        if face not in self._face:
            raise KeyError(face)

        if names and values:
            for name, value in zip(names, values):
                if face not in self._face_data:
                    self._face_data[face] = {}
                self._face_data[face][name] = value
            return

        if not names:
            return FaceAttributeView(self.default_face_attributes, self._face_data.setdefault(face, {}))

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

    def has_face(self, face):
        """Verify that a face is part of the cell network.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.

        See Also
        --------
        :meth:`has_vertex`, :meth:`has_edge`, :meth:`has_cell`

        """
        return face in self._face

    def face_vertices(self, face):
        """The vertices of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list[int]
            Ordered vertex identifiers.

        """
        return self._face[face]

    def face_edges(self, face):
        """The edges of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list[tuple[int, int]]
            Ordered edge identifiers.

        """
        vertices = self.face_vertices(face)
        edges = []
        for u, v in pairwise(vertices + vertices[:1]):
            # if v in self._edge[u]:
            #     edges.append((u, v))
            edges.append((u, v))
        return edges

    def face_cells(self, face):
        """Return the cells connected to a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        list[int]
            The identifiers of the cells connected to the face.

        """
        u, v = self.face_vertices(face)[:2]
        cells = []
        if v in self._plane[u]:
            cell = self._plane[u][v][face]
            if cell is not None:
                cells.append(cell)
            cell = self._plane[v][u][face]
            if cell is not None:
                cells.append(cell)
        return cells

    def faces_without_cell(self):
        """Find the faces that are not part of a cell.

        Returns
        -------
        list[int]
            The faces without cell.

        """
        faces = {fkey for fkey in self.faces() if not self.face_cells(fkey)}
        return list(faces)

    # @Romana: this logic only makes sense for a face belonging to a cell
    # # yep, if the face is not belonging to a cell, it returns False, which is correct
    def is_face_on_boundary(self, face):
        """Verify that a face is on the boundary.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        """
        u, v = self.face_vertices(face)[:2]
        cu = 1 if self._plane[u][v][face] is None else 0
        cv = 1 if self._plane[v][u][face] is None else 0
        return cu + cv == 1

    def faces_on_boundaries(self):
        """Find the faces that are on the boundary.

        Returns
        -------
        list[int]
            The faces on the boundary.

        """
        return [face for face in self.faces() if self.is_face_on_boundary(face)]

    # --------------------------------------------------------------------------
    # Face Geometry
    # --------------------------------------------------------------------------

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

    def face_plane(self, face):
        """Compute the plane of a face.

        Parameters
        ----------
        face : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Plane`
            The plane of the face.

        See Also
        --------
        :meth:`face_points`, :meth:`face_polygon`, :meth:`face_normal`, :meth:`face_centroid`, :meth:`face_center`

        """
        return Plane(self.face_centroid(face), self.face_normal(face))

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
        lengths = [self.edge_length(edge) for edge in self.face_edges(face)]
        return max(lengths) / min(lengths)

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
        This method is similar to :meth:`~compas.datastructures.HalfEdge.vertices`,
        but in the context of a cell of the `VolMesh`.

        """
        return list(set([vertex for face in self.cell_faces(cell) for vertex in self.face_vertices(face)]))

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
        This method is similar to :meth:`~compas.datastructures.HalfEdge.halfedges`,
        but in the context of a cell of the `VolMesh`.

        """
        halfedges = []
        for u in self._cell[cell]:
            for v in self._cell[cell][u]:
                halfedges.append((u, v))
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
        This method is similar to :meth:`~compas.datastructures.HalfEdge.edges`,
        but in the context of a cell of the `VolMesh`.

        """
        return self.cell_halfedges(cell)

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
        This method is similar to :meth:`~compas.datastructures.HalfEdge.faces`,
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

        This method is similar to :meth:`~compas.datastructures.HalfEdge.vertex_neighbors`,
        but in the context of a cell of the `VolMesh`.

        """
        if vertex not in self._cell[cell]:
            raise KeyError(vertex)

        nbrs = []
        for nbr in self._vertex[vertex]:
            if nbr in self._cell[cell]:
                nbrs.append(nbr)

        return nbrs

        # nbr_vertices = self._cell[cell][vertex].keys()
        # v = nbr_vertices[0]
        # ordered_vkeys = [v]
        # for i in range(len(nbr_vertices) - 1):
        #     face = self._cell[cell][vertex][v]
        #     v = self.halfface_vertex_ancestor(face, vertex)
        #     ordered_vkeys.append(v)
        # return ordered_vkeys

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

        This method is similar to :meth:`~compas.datastructures.HalfEdge.vertex_faces`,
        but in the context of a cell of the `VolMesh`.

        """
        # nbr_vertices = self._cell[cell][vertex].keys()
        # u = vertex
        # v = nbr_vertices[0]
        # ordered_faces = []
        # for i in range(len(nbr_vertices)):
        #     face = self._cell[cell][u][v]
        #     v = self.halfface_vertex_ancestor(face, u)
        #     ordered_faces.append(face)
        # return ordered_faces

        if vertex not in self._cell[cell]:
            raise KeyError(vertex)

        faces = []
        for nbr in self._cell[cell][vertex]:
            faces.append(self._cell[cell][vertex][nbr])

        return faces

    def cell_face_vertices(self, cell, face):
        """The vertices of a face of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        face : int
            Identifier of the face.

        Returns
        -------
        list[int]
            The vertices of the face of the cell.

        See Also
        --------
        :meth:`cell_face_halfedges`

        Notes
        -----
        All of the returned vertices are part of the cell.

        This method is similar to :meth:`~compas.datastructures.HalfEdge.face_vertices`,
        but in the context of a cell of the `VolMesh`.

        """
        if face not in self._face:
            raise KeyError(face)

        vertices = self.face_vertices(face)
        u, v = vertices[:2]
        if v in self._cell[cell][u] and self._cell[cell][u][v] == face:
            return self.face_vertices(face)
        if u in self._cell[cell][v] and self._cell[cell][v][u] == face:
            return self.face_vertices(face)[::-1]

        raise Exception("Face is not part of the cell")

    def cell_face_halfedges(self, cell, face):
        """The halfedges of a face of a cell.

        Parameters
        ----------
        cell : int
            Identifier of the cell.
        face : int
            Identifier of the face.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of the face of the cell.

        See Also
        --------
        :meth:`cell_face_vertices`

        Notes
        -----
        All of the returned halfedges are part of the cell.

        This method is similar to :meth:`~compas.datastructures.HalfEdge.face_halfedges`,
        but in the context of a cell of the `VolMesh`.

        """
        vertices = self.cell_face_vertices(cell, face)
        return list(pairwise(vertices + vertices[:1]))

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
        This method is similar to :meth:`~compas.datastructures.HalfEdge.halfedge_face`,
        but in the context of a cell of the `VolMesh`.

        """
        u, v = halfedge
        if u not in self._cell[cell] or v not in self._cell[cell][u]:
            raise KeyError(halfedge)
        return self._cell[cell][u][v]

    # def cell_halfedge_opposite_face(self, cell, halfedge):
    #     """Find the opposite face corresponding to a specific halfedge of a cell.

    #     Parameters
    #     ----------
    #     cell : int
    #         The identifier of the cell.
    #     halfedge : tuple[int, int]
    #         The identifier of the halfedge.

    #     Returns
    #     -------
    #     int
    #         The identifier of the face.

    #     See Also
    #     --------
    #     :meth:`cell_halfedge_face`

    #     """
    #     u, v = halfedge
    #     return self._cell[cell][v][u]

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
        This method is similar to :meth:`~compas.datastructures.HalfEdge.face_neighbors`,
        but in the context of a cell of the `VolMesh`.

        """
        # nbrs = []
        # for halfedge in self.halfface_halfedges(face):
        #     nbr = self.cell_halfedge_opposite_face(cell, halfedge)
        #     if nbr is not None:
        #         nbrs.append(nbr)
        # return nbrs

        nbrs = []
        for u in self.face_vertices(face):
            for v in self._cell[cell][u]:
                test = self._cell[cell][u][v]
                if test == face:
                    nbr = self._cell[cell][v][u]
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
        for face in self.cell_faces(cell):
            for nbr in self.face_cells(face):
                if nbr != cell:
                    nbrs.append(nbr)
        return list(set(nbrs))

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
            if self.is_face_on_boundary(face):
                return True
        return False

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
        cells = []
        for cell in self.cells():
            if self.is_cell_on_boundary(cell):
                cells.append(cell)
        return cells

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
        :meth:`cell_polygon`, :meth:`cell_centroid`, :meth:`cell_center`
        """
        return [self.vertex_point(vertex) for vertex in self.cell_vertices(cell)]

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

    # def cell_vertex_normal(self, cell, vertex):
    #     """Return the normal vector at the vertex of a boundary cell as the weighted average of the
    #     normals of the neighboring faces.

    #     Parameters
    #     ----------
    #     cell : int
    #         The identifier of the vertex of the cell.
    #     vertex : int
    #         The identifier of the vertex of the cell.

    #     Returns
    #     -------
    #     :class:`compas.geometry.Vector`
    #         The components of the normal vector.

    #     """
    #     cell_faces = self.cell_faces(cell)
    #     vectors = [self.face_normal(face) for face in self.vertex_halffaces(vertex) if face in cell_faces]
    #     return Vector(*normalize_vector(centroid_points(vectors)))

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

    def cell_volume(self, cell):
        """Compute the volume of a cell.

        Parameters
        ----------
        cell : int
            The identifier of the cell.

        Returns
        -------
        float
            The volume of the cell.

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return abs(volume_polyhedron((vertices, faces)))

    # # --------------------------------------------------------------------------
    # # Boundaries
    # # --------------------------------------------------------------------------

    # def vertices_on_boundaries(self):
    #     """Find the vertices on the boundary.

    #     Returns
    #     -------
    #     list[int]
    #         The vertices of the boundary.

    #     See Also
    #     --------
    #     :meth:`faces_on_boundaries`, :meth:`cells_on_boundaries`

    #     """
    #     vertices = set()
    #     for face in self._halfface:
    #         if self.is_halfface_on_boundary(face):
    #             vertices.update(self.halfface_vertices(face))
    #     return list(vertices)

    # def halffaces_on_boundaries(self):
    #     """Find the faces on the boundary.

    #     Returns
    #     -------
    #     list[int]
    #         The faces of the boundary.

    #     See Also
    #     --------
    #     :meth:`vertices_on_boundaries`, :meth:`cells_on_boundaries`

    #     """
    #     faces = set()
    #     for face in self._halfface:
    #         if self.is_halfface_on_boundary(face):
    #             faces.add(face)
    #     return list(faces)

    # def cells_on_boundaries(self):
    #     """Find the cells on the boundary.

    #     Returns
    #     -------
    #     list[int]
    #         The cells of the boundary.

    #     See Also
    #     --------
    #     :meth:`vertices_on_boundaries`, :meth:`faces_on_boundaries`

    #     """
    #     cells = set()
    #     for face in self.halffaces_on_boundaries():
    #         cells.add(self.halfface_cell(face))
    #     return list(cells)

    # # --------------------------------------------------------------------------
    # # Transformations
    # # --------------------------------------------------------------------------

    # def transform(self, T):
    #     """Transform the mesh.

    #     Parameters
    #     ----------
    #     T : :class:`Transformation`
    #         The transformation used to transform the mesh.

    #     Returns
    #     -------
    #     None
    #         The mesh is modified in-place.

    #     Examples
    #     --------
    #     >>> from compas.datastructures import Mesh
    #     >>> from compas.geometry import matrix_from_axis_and_angle
    #     >>> mesh = Mesh.from_polyhedron(6)
    #     >>> T = matrix_from_axis_and_angle([0, 0, 1], math.pi / 4)
    #     >>> mesh.transform(T)

    #     """
    #     points = transform_points(self.vertices_attributes("xyz"), T)
    #     for vertex, point in zip(self.vertices(), points):
    #         self.vertex_attributes(vertex, "xyz", point)
