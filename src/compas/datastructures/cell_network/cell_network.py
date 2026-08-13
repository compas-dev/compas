from ast import literal_eval
from random import sample
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Iterator
from typing import Literal
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Union
from typing import overload

from typing_extensions import Self

from compas.datastructures import Graph
from compas.datastructures import Mesh
from compas.datastructures.attributes import CellAttributeView
from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import FaceAttributeView
from compas.datastructures.attributes import VertexAttributeView
from compas.datastructures.datastructure import Datastructure
from compas.files import read_obj
from compas.files import weld_obj_data
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

from .types import AttributeDict
from .types import Cell
from .types import Edge
from .types import Face
from .types import PointCoordinates
from .types import Vertex

_MISSING = object()


def _edge_data_key(edge: Edge) -> Edge:
    u, v = edge
    return (u, v) if u < v else (v, u)


class CellNetwork(Datastructure):
    """Geometric implementation of a data structure for a collection of mixed topologic entities such as cells, faces, edges and nodes.

    Parameters
    ----------
    default_vertex_attributes
        Default values for vertex attributes.
    default_edge_attributes
        Default values for edge attributes.
    default_face_attributes
        Default values for face attributes.
    default_cell_attributes
        Default values for cell attributes.
    name
        The name of the cell network.
    **kwargs
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

    @property
    def __data__(self) -> dict[str, Any]:
        cell: dict[Cell, list[Face]] = {}
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
    def __from_data__(cls, data: dict[str, Any]) -> Self:
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
                attr = edge_data.get(_edge_data_key((int(u), int(v))), {})
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

    def __init__(
        self,
        default_vertex_attributes: Optional[AttributeDict] = None,
        default_edge_attributes: Optional[AttributeDict] = None,
        default_face_attributes: Optional[AttributeDict] = None,
        default_cell_attributes: Optional[AttributeDict] = None,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(kwargs, name=name)
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1
        self._vertex: dict[Vertex, AttributeDict] = {}
        self._edge: dict[Vertex, dict[Vertex, AttributeDict]] = {}
        self._face: dict[Face, list[Vertex]] = {}
        self._plane: dict[Vertex, dict[Vertex, dict[Face, Optional[Cell]]]] = {}
        self._cell: dict[Cell, dict[Vertex, dict[Vertex, Face]]] = {}
        self._edge_data: dict[Edge, AttributeDict] = {}
        self._face_data: dict[Face, AttributeDict] = {}
        self._cell_data: dict[Cell, AttributeDict] = {}
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

    def __str__(self) -> str:
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

    def clear(self) -> None:
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
        del self._edge_data
        del self._face_data
        del self._cell_data
        self._vertex = {}
        self._edge = {}
        self._face = {}
        self._cell = {}
        self._plane = {}
        self._edge_data = {}
        self._face_data = {}
        self._cell_data = {}
        self._max_vertex = -1
        self._max_face = -1
        self._max_cell = -1

    def vertex_sample(self, size: int = 1) -> list[Vertex]:
        """Get the identifiers of a set of random vertices.

        Parameters
        ----------
        size
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the vertices.

        See Also
        --------
        edge_sample, face_sample, cell_sample

        """
        return sample(list(self.vertices()), size)

    def edge_sample(self, size: int = 1) -> list[Edge]:
        """Get the identifiers of a set of random edges.

        Parameters
        ----------
        size
            The size of the sample.

        Returns
        -------
        list[tuple[int, int]]
            The identifiers of the edges.

        See Also
        --------
        vertex_sample, face_sample, cell_sample

        """
        return sample(list(self.edges()), size)

    def face_sample(self, size: int = 1) -> list[Face]:
        """Get the identifiers of a set of random faces.

        Parameters
        ----------
        size
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the faces.

        See Also
        --------
        vertex_sample, edge_sample, cell_sample

        """
        return sample(list(self.faces()), size)

    def cell_sample(self, size: int = 1) -> list[Cell]:
        """Get the identifiers of a set of random cells.

        Parameters
        ----------
        size
            The size of the sample.

        Returns
        -------
        list[int]
            The identifiers of the cells.

        See Also
        --------
        vertex_sample, edge_sample, face_sample

        """
        return sample(list(self.cells()), size)

    def vertex_index(self) -> dict[Vertex, int]:
        """Returns a dictionary that maps vertex identifiers to the corresponding index in a vertex list or array.

        Returns
        -------
        dict[int, int]
            A dictionary of vertex-index pairs.

        See Also
        --------
        index_vertex

        """
        return {key: index for index, key in enumerate(self.vertices())}

    def index_vertex(self) -> dict[int, Vertex]:
        """Returns a dictionary that maps the indices of a vertex list to vertex identifiers.

        Returns
        -------
        dict[int, int]
            A dictionary of index-vertex pairs.

        See Also
        --------
        vertex_index

        """
        return dict(enumerate(self.vertices()))

    def vertex_gkey(self, precision: Optional[int] = None) -> dict[Vertex, str]:
        """Returns a dictionary that maps vertex identifiers to the corresponding *geometric key* up to a certain precision.

        Parameters
        ----------
        precision
            Precision for converting numbers to strings.
            Default is `TOL.precision`.

        Returns
        -------
        dict[int, str]
            A dictionary of vertex-geometric key pairs.

        See Also
        --------
        gkey_vertex

        """
        gkey = TOL.geometric_key
        xyz = self.vertex_coordinates
        return {vertex: gkey(xyz(vertex), precision) for vertex in self.vertices()}

    def gkey_vertex(self, precision: Optional[int] = None) -> dict[str, Vertex]:
        """Returns a dictionary that maps *geometric keys* of a certain precision to the corresponding vertex identifiers.

        Parameters
        ----------
        precision
            Precision for converting numbers to strings.
            Default is `TOL.precision`.

        Returns
        -------
        dict[str, int]
            A dictionary of geometric key-vertex pairs.

        See Also
        --------
        vertex_gkey

        """
        gkey = TOL.geometric_key
        xyz = self.vertex_coordinates
        return {gkey(xyz(vertex), precision): vertex for vertex in self.vertices()}

    # --------------------------------------------------------------------------
    # Builders
    # --------------------------------------------------------------------------

    def add_vertex(
        self,
        key: Optional[Vertex] = None,
        attr_dict: Optional[Mapping[str, Any]] = None,
        **kwattr: Any,
    ) -> Vertex:
        """Add a vertex and specify its attributes.

        Parameters
        ----------
        key
            The identifier of the vertex.
            Defaults to None.
        attr_dict
            A dictionary of vertex attributes.
            Defaults to None.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The identifier of the vertex.

        See Also
        --------
        add_face, add_cell, add_edge

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

        attr = dict(attr_dict or {})
        attr.update(kwattr)
        self._vertex[key].update(attr)

        return key

    def add_edge(
        self,
        u: Vertex,
        v: Vertex,
        attr_dict: Optional[Mapping[str, Any]] = None,
        **kwattr: Any,
    ) -> Edge:
        """Add an edge and specify its attributes.

        Parameters
        ----------
        u
            The identifier of the first node of the edge.
        v
            The identifier of the second node of the edge.
        attr_dict
            A dictionary of edge attributes.
        **kwattr
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
            raise ValueError("Cannot add edge {}, {} has no vertex {}".format((u, v), self.name, v))

        attr = dict(attr_dict or {})
        attr.update(kwattr)

        uv = _edge_data_key((u, v))

        data = self._edge_data.get(uv, {})
        data.update(attr)
        self._edge_data[uv] = data

        if v not in self._edge[u]:
            self._edge[u][v] = {}
        if v not in self._plane[u]:
            self._plane[u][v] = {}
        if u not in self._plane[v]:
            self._plane[v][u] = {}

        return u, v

    def add_face(
        self,
        vertices: Sequence[Vertex],
        fkey: Optional[Face] = None,
        attr_dict: Optional[Mapping[str, Any]] = None,
        **kwattr: Any,
    ) -> Face:
        """Add a face to the cell network.

        Parameters
        ----------
        vertices
            A list of ordered vertex keys representing the face.
        fkey
            The face identifier.
        attr_dict
            dictionary of halfface attributes.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The key of the face.

        Raises
        ------
        ValueError
            If the face has fewer than three vertices, or if a vertex is not part
            of the cell network.

        See Also
        --------
        add_vertex, add_cell, add_edge

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
            raise ValueError("A face should have at least 3 vertices.")

        if vertices[-1] == vertices[0]:
            vertices = vertices[:-1]
        vertices = [int(key) for key in vertices]

        missing = [vertex for vertex in vertices if vertex not in self._vertex]
        if missing:
            raise ValueError(f"The following vertices are not part of the cell network: {missing}")

        if fkey is None:
            fkey = self._max_face = self._max_face + 1
        fkey = int(fkey)
        if fkey > self._max_face:
            self._max_face = fkey

        self._face[fkey] = vertices

        attr = dict(attr_dict or {})
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

    def _faces_to_unified_mesh(self, faces: Iterable[Face]) -> Optional[Mesh]:
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

    def is_faces_closed(self, faces: Iterable[Face]) -> bool:
        """Checks if the faces form a closed cell."""
        mesh = self._faces_to_unified_mesh(faces)
        if mesh:
            return True
        return False

    def add_cell(
        self,
        faces: Iterable[Face],
        ckey: Optional[Cell] = None,
        attr_dict: Optional[Mapping[str, Any]] = None,
        **kwattr: Any,
    ) -> Cell:
        """Add a cell to the cell network object.

        In order to add a valid cell to the network, the faces must form a closed mesh.
        If the faces do not form a closed mesh, the cell is not added to the network.

        Parameters
        ----------
        faces
            The face keys of the cell.
        ckey
            The cell identifier.
        attr_dict
            A dictionary of cell attributes.
        **kwattr
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
        faces = list(faces)
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

        attr = dict(attr_dict or {})
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
    #     delete_halfface, delete_cell

    #     """
    #     for cell in self.vertex_cells(vertex):
    #         self.delete_cell(cell)

    def delete_edge(self, edge: Edge) -> None:
        """Delete an edge from the cell network.

        Parameters
        ----------
        edge
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
        key = _edge_data_key(edge)
        if key in self._edge_data:
            del self._edge_data[key]

    def delete_face(self, face: Face) -> None:
        """Delete a face from the cell network.

        Parameters
        ----------
        face
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

    def delete_cell(self, cell: Cell) -> None:
        """Delete a cell from the cell network.

        Parameters
        ----------
        cell
            The identifier of the cell.

        Returns
        -------
        None

        See Also
        --------
        delete_vertex, delete_halfface

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
    #     VolMesh

    #     See Also
    #     --------
    #     from_obj, from_vertices_and_cells

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
    def from_obj(cls, filepath: Any, precision: Optional[int] = None) -> Self:
        """Construct a cell network object from the data described in an OBJ file.

        Parameters
        ----------
        filepath
            A path, a file-like object or a URL pointing to a file.
        precision
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        VolMesh
            A cell network object.

        See Also
        --------
        to_obj
        from_meshgrid, from_vertices_and_cells
        read_obj

        """
        data = weld_obj_data(read_obj(filepath), precision)
        vertices = data.vertices
        faces = data.faces
        groups = data.groups
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
    def from_vertices_and_cells(
        cls,
        vertices: Sequence[PointCoordinates],
        cells: Sequence[Sequence[Sequence[Vertex]]],
    ) -> Self:
        """Construct a cell network object from vertices and cells.

        Parameters
        ----------
        vertices
            Ordered list of vertices, represented by their XYZ coordinates.
        cells
            List of cells defined by their faces.

        Returns
        -------
        VolMesh
            A cell network object.

        See Also
        --------
        to_vertices_and_cells
        from_obj

        """
        cellnetwork = cls()
        for x, y, z in vertices:
            cellnetwork.add_vertex(x=x, y=y, z=z)
        for cell in cells:
            faces = []
            for face_vertices in cell:
                face = cellnetwork.add_face(face_vertices)
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
    #     from_obj

    #     Warnings
    #     --------
    #     This function only writes geometric data about the vertices and
    #     the faces to the file.

    #     """
    #     write_obj(filepath, self, precision=precision, **kwargs)

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
    #     from_vertices_and_cells

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

    def edges_to_graph(self) -> Graph:
        """Convert the edges of the cell network to a graph.

        Returns
        -------
        Graph
            A graph object.

        """
        graph = Graph()
        for vertex, attr in self.vertices(data=True):
            x, y, z = self.vertex_coordinates(vertex)
            graph.add_node(key=vertex, x=x, y=y, z=z, attr_dict=dict(attr))
        for (u, v), attr in self.edges(data=True):
            graph.add_edge(u, v, attr_dict=dict(attr))
        return graph

    def cells_to_graph(self) -> Graph:
        """Convert the cells the cell network to a graph.

        Returns
        -------
        Graph
            A graph object.

        """
        graph = Graph()
        for cell, attr in self.cells(data=True):
            x, y, z = self.cell_centroid(cell)
            graph.add_node(key=cell, x=x, y=y, z=z, attr_dict=dict(attr))
        for cell in self.cells():
            for nbr in self.cell_neighbors(cell):
                u, v = _edge_data_key((cell, nbr))
                graph.add_edge(u, v)
        return graph

    def cell_to_vertices_and_faces(self, cell: Cell) -> tuple[list[list[float]], list[list[Vertex]]]:
        """Return the vertices and faces of a cell.

        Parameters
        ----------
        cell
            Identifier of the cell.

        Returns
        -------
        list[list[float]]
            A list of vertices, represented by their XYZ coordinates,
        list[list[int]]
            A list of faces, with each face a list of vertex indices.

        See Also
        --------
        cell_to_mesh

        """
        vertices = self.cell_vertices(cell)
        faces = self.cell_faces(cell)
        vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
        vertices = [self.vertex_coordinates(vertex) for vertex in vertices]
        faces = []
        for face in self.cell_faces(cell):
            faces.append([vertex_index[vertex] for vertex in self.cell_face_vertices(cell, face)])
        return vertices, faces

    def cell_to_mesh(self, cell: Cell) -> Mesh:
        """Construct a mesh object from from a cell of a cell network.

        Parameters
        ----------
        cell
            Identifier of the cell.

        Returns
        -------
        Mesh
            A mesh object.

        See Also
        --------
        cell_to_vertices_and_faces

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Mesh.from_vertices_and_faces(vertices, faces)

    def faces_to_mesh(self, faces: Iterable[Face], data: bool = False) -> Mesh:
        """Construct a mesh from a list of faces.

        Parameters
        ----------
        faces
            A list of face identifiers.

        Returns
        -------
        Mesh
            A mesh.

        """
        faces = list(faces)
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

    def vertices_to_points(self) -> list[list[float]]:
        """Convert the vertices of the cell network to a collection of points.

        Returns
        -------
        list[list[float]]
            The points representing the vertices of the cell network.

        """
        return [self.vertex_coordinates(vertex) for vertex in self.vertices()]

    # --------------------------------------------------------------------------
    # General
    # --------------------------------------------------------------------------

    def centroid(self) -> Point:
        """Compute the centroid of the cell network.

        Returns
        -------
        Point
            The point at the centroid.

        """
        return Point(*centroid_points([self.vertex_coordinates(vertex) for vertex in self.vertices()]))

    def aabb(self) -> list[list[float]]:
        """Calculate the axis aligned bounding box of the mesh.

        Returns
        -------
        list[[float, float, float]]
            XYZ coordinates of 8 points defining a box.

        """
        xyz = self.vertices_attributes("xyz")
        return bounding_box(xyz)

    def number_of_vertices(self) -> int:
        """Count the number of vertices in the cell network.

        Returns
        -------
        int
            The number of vertices.

        See Also
        --------
        number_of_edges, number_of_faces, number_of_cells

        """
        return len(list(self.vertices()))

    def number_of_edges(self) -> int:
        """Count the number of edges in the cell network.

        Returns
        -------
        int
            The number of edges.

        See Also
        --------
        number_of_vertices, number_of_faces, number_of_cells

        """
        return len(list(self.edges()))

    def number_of_faces(self) -> int:
        """Count the number of faces in the cell network.

        Returns
        -------
        int
            The number of faces.

        See Also
        --------
        number_of_vertices, number_of_edges, number_of_cells

        """
        return len(list(self.faces()))

    def number_of_cells(self) -> int:
        """Count the number of faces in the cell network.

        Returns
        -------
        int
            The number of cells.

        See Also
        --------
        number_of_vertices, number_of_edges, number_of_faces

        """
        return len(list(self.cells()))

    def is_valid(self) -> bool:
        """Verify that the cell network is valid.

        Returns
        -------
        bool
            True if the cell network is valid.
            False otherwise.

        Raises
        ------
        NotImplementedError
            This validation method is not implemented yet.

        """
        raise NotImplementedError

    # --------------------------------------------------------------------------
    # Vertex Accessors
    # --------------------------------------------------------------------------

    @overload
    def vertices(self, data: Literal[False] = False) -> Iterator[Vertex]: ...

    @overload
    def vertices(self, data: Literal[True]) -> Iterator[tuple[Vertex, VertexAttributeView]]: ...

    @overload
    def vertices(self, data: bool) -> Iterator[Union[Vertex, tuple[Vertex, VertexAttributeView]]]: ...

    def vertices(self, data: bool = False) -> Iterator[Any]:
        """Iterate over the vertices of the cell network.

        Parameters
        ----------
        data
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int
            The vertex identifier if `data` is `False`.
        tuple[int, VertexAttributeView]
            The vertex identifier and its attributes if `data` is `True`.

        See Also
        --------
        edges, faces, cells

        """
        for vertex in self._vertex:
            if not data:
                yield vertex
            else:
                yield vertex, self.vertex_attributes(vertex)

    @overload
    def vertices_where(
        self,
        conditions: Optional[Mapping[str, Any]] = None,
        data: Literal[False] = False,
        **kwargs: Any,
    ) -> Iterator[Vertex]: ...

    @overload
    def vertices_where(
        self,
        conditions: Optional[Mapping[str, Any]],
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Vertex, VertexAttributeView]]: ...

    @overload
    def vertices_where(
        self,
        *,
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Vertex, VertexAttributeView]]: ...

    @overload
    def vertices_where(
        self,
        conditions: Optional[Mapping[str, Any]],
        data: bool,
        **kwargs: Any,
    ) -> Iterator[Union[Vertex, tuple[Vertex, VertexAttributeView]]]: ...

    def vertices_where(
        self,
        conditions: Optional[Mapping[str, Any]] = None,
        data: bool = False,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """Get vertices for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data
            If True, yield the vertex attributes in addition to the identifiers.
        **kwargs
            Additional conditions provided as named function arguments.

        Yields
        ------
        int
            A matching vertex identifier if `data` is `False`.
        tuple[int, VertexAttributeView]
            A matching vertex identifier and its attributes if `data` is `True`.

        See Also
        --------
        vertices_where_predicate
        edges_where, faces_where, cells_where

        """
        conditions = dict(conditions or {})
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
                        continue

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
                        continue

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

    @overload
    def vertices_where_predicate(
        self,
        predicate: Callable[[Vertex, VertexAttributeView], bool],
        data: Literal[False] = False,
    ) -> Iterator[Vertex]: ...

    @overload
    def vertices_where_predicate(
        self,
        predicate: Callable[[Vertex, VertexAttributeView], bool],
        data: Literal[True],
    ) -> Iterator[tuple[Vertex, VertexAttributeView]]: ...

    @overload
    def vertices_where_predicate(
        self,
        predicate: Callable[[Vertex, VertexAttributeView], bool],
        data: bool,
    ) -> Iterator[Union[Vertex, tuple[Vertex, VertexAttributeView]]]: ...

    def vertices_where_predicate(
        self,
        predicate: Callable[[Vertex, VertexAttributeView], bool],
        data: bool = False,
    ) -> Iterator[Any]:
        """Get vertices for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate
            The condition you want to evaluate.
            The callable takes 2 parameters: the vertex identifier and the vertex attributes, and should return True or False.
        data
            If True, yield the vertex attributes in addition to the identifiers.

        Yields
        ------
        int
            A matching vertex identifier if `data` is `False`.
        tuple[int, VertexAttributeView]
            A matching vertex identifier and its attributes if `data` is `True`.

        See Also
        --------
        vertices_where
        edges_where_predicate, faces_where_predicate, cells_where_predicate

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

    def update_default_vertex_attributes(
        self,
        attr_dict: Optional[Mapping[str, Any]] = None,
        **kwattr: Any,
    ) -> None:
        """Update the default vertex attributes.

        Parameters
        ----------
        attr_dict
            A dictionary of attributes with their default values.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        update_default_edge_attributes, update_default_face_attributes, update_default_cell_attributes

        Notes
        -----
        Named arguments overwrite correpsonding name-value pairs in the attribute dictionary.

        """
        attr_dict = dict(attr_dict or {})
        attr_dict.update(kwattr)
        self.default_vertex_attributes.update(attr_dict)

    @overload
    def vertex_attribute(self, vertex: Vertex, name: str) -> Any: ...

    @overload
    def vertex_attribute(self, vertex: Vertex, name: str, value: Any) -> None: ...

    def vertex_attribute(self, vertex: Vertex, name: str, value: Any = _MISSING) -> Any:
        """Get or set an attribute of a vertex.

        Parameters
        ----------
        vertex
            The vertex identifier.
        name
            The name of the attribute
        value
            The value of the attribute.

        Returns
        -------
        Any
            The attribute value when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If the vertex does not exist.

        See Also
        --------
        unset_vertex_attribute
        vertex_attributes, vertices_attribute, vertices_attributes
        edge_attribute, face_attribute, cell_attribute

        """
        if vertex not in self._vertex:
            raise KeyError(vertex)
        if value is not _MISSING:
            self._vertex[vertex][name] = value
            return None
        if name in self._vertex[vertex]:
            return self._vertex[vertex][name]
        else:
            if name in self.default_vertex_attributes:
                return self.default_vertex_attributes[name]

    def unset_vertex_attribute(self, vertex: Vertex, name: str) -> None:
        """Unset the attribute of a vertex.

        Parameters
        ----------
        vertex
            The vertex identifier.
        name
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
        vertex_attribute

        Notes
        -----
        Unsetting the value of a vertex attribute implicitly sets it back to the value
        stored in the default vertex attribute dict.

        """
        if name in self._vertex[vertex]:
            del self._vertex[vertex][name]

    @overload
    def vertex_attributes(self, vertex: Vertex, names: None = None, values: None = None) -> VertexAttributeView: ...

    @overload
    def vertex_attributes(self, vertex: Vertex, names: None, values: Sequence[Any]) -> VertexAttributeView: ...

    @overload
    def vertex_attributes(
        self, vertex: Vertex, names: Sequence[str], values: None = None
    ) -> list[Any]: ...

    @overload
    def vertex_attributes(self, vertex: Vertex, names: Sequence[str], values: Sequence[Any]) -> None: ...

    def vertex_attributes(
        self,
        vertex: Vertex,
        names: Optional[Sequence[str]] = None,
        values: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Get or set multiple attributes of a vertex.

        Parameters
        ----------
        vertex
            The identifier of the vertex.
        names
            A list of attribute names.
        values
            A list of attribute values.

        Returns
        -------
        VertexAttributeView
            All attributes when `names` is not provided.
        list[Any]
            The requested attribute values when `names` is provided and `values` is not provided.
        None
            When both `names` and `values` are provided.

        Raises
        ------
        KeyError
            If the vertex does not exist.

        See Also
        --------
        vertex_attribute, vertices_attribute, vertices_attributes
        edge_attributes, face_attributes, cell_attributes

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

    @overload
    def vertices_attribute(
        self,
        name: str,
        *,
        keys: Optional[Iterable[Vertex]] = None,
    ) -> list[Any]: ...

    @overload
    def vertices_attribute(
        self,
        name: str,
        value: Any,
        keys: Optional[Iterable[Vertex]] = None,
    ) -> None: ...

    def vertices_attribute(
        self,
        name: str,
        value: Any = _MISSING,
        keys: Optional[Iterable[Vertex]] = None,
    ) -> Optional[list[Any]]:
        """Get or set an attribute of multiple vertices.

        Parameters
        ----------
        name
            The name of the attribute.
        value
            The value of the attribute.
            Default is None.
        keys
            A list of vertex identifiers.

        Returns
        -------
        list[Any]
            The attribute values when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If any of the vertices does not exist.

        See Also
        --------
        vertex_attribute, vertex_attributes, vertices_attributes
        edges_attribute, faces_attribute, cells_attribute

        """
        vertices = self.vertices() if keys is None else keys
        if value is not _MISSING:
            for vertex in vertices:
                self.vertex_attribute(vertex, name, value)
            return
        return [self.vertex_attribute(vertex, name) for vertex in vertices]

    @overload
    def vertices_attributes(
        self,
        names: None = None,
        values: None = None,
        keys: Optional[Iterable[Vertex]] = None,
    ) -> list[VertexAttributeView]: ...

    @overload
    def vertices_attributes(
        self,
        names: Sequence[str],
        values: None = None,
        keys: Optional[Iterable[Vertex]] = None,
    ) -> list[list[Any]]: ...

    @overload
    def vertices_attributes(
        self,
        names: Sequence[str],
        values: Sequence[Any],
        keys: Optional[Iterable[Vertex]] = None,
    ) -> None: ...

    @overload
    def vertices_attributes(
        self,
        names: None,
        values: Sequence[Any],
        keys: Optional[Iterable[Vertex]] = None,
    ) -> None: ...

    def vertices_attributes(
        self,
        names: Optional[Sequence[str]] = None,
        values: Optional[Sequence[Any]] = None,
        keys: Optional[Iterable[Vertex]] = None,
    ) -> Optional[list[Any]]:
        """Get or set multiple attributes of multiple vertices.

        Parameters
        ----------
        names
            The names of the attribute.
            Default is None.
        values
            The values of the attributes.
            Default is None.
        key
            A list of vertex identifiers.

        Returns
        -------
        list[VertexAttributeView]
            All attributes when `names` is not provided.
        list[list[Any]]
            The requested attribute values when `names` is provided and `values` is not provided.
        None
            When `values` is provided.

        Raises
        ------
        KeyError
            If any of the vertices does not exist.

        See Also
        --------
        vertex_attribute, vertex_attributes, vertices_attribute
        edges_attributes, faces_attributes, cells_attributes

        """
        vertices = self.vertices() if keys is None else keys
        if values is not None:
            for vertex in vertices:
                self.vertex_attributes(vertex, names, values)
            return
        return [self.vertex_attributes(vertex, names) for vertex in vertices]

    # --------------------------------------------------------------------------
    # Vertex Topology
    # --------------------------------------------------------------------------

    def has_vertex(self, vertex: Vertex) -> bool:
        """Verify that a vertex is in the cell network.

        Parameters
        ----------
        vertex
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is in the cell network.
            False otherwise.

        See Also
        --------
        has_edge, has_face, has_cell

        """
        return vertex in self._vertex

    def vertex_neighbors(self, vertex: Vertex) -> list[Vertex]:
        """Return the vertex neighbors of a vertex.

        Parameters
        ----------
        vertex
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of neighboring vertices.

        See Also
        --------
        vertex_degree, vertex_min_degree, vertex_max_degree
        vertex_faces, vertex_halffaces, vertex_cells
        vertex_neighborhood

        """
        return list(self._edge[vertex])

    def vertex_neighborhood(self, vertex: Vertex, ring: int = 1) -> list[Vertex]:
        """Return the vertices in the neighborhood of a vertex.

        Parameters
        ----------
        vertex
            The identifier of the vertex.
        ring
            The number of neighborhood rings to include.

        Returns
        -------
        list[int]
            The vertices in the neighborhood.

        See Also
        --------
        vertex_neighbors

        Notes
        -----
        The vertices in the neighborhood are unordered.

        Raises
        ------
        ValueError
            If `ring` is smaller than 1.

        """
        if ring < 1:
            raise ValueError("The neighborhood ring should be at least 1.")
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

    def vertex_degree(self, vertex: Vertex) -> int:
        """Count the neighbors of a vertex.

        Parameters
        ----------
        vertex
            The identifier of the vertex.

        Returns
        -------
        int
            The degree of the vertex.

        See Also
        --------
        vertex_neighbors, vertex_min_degree, vertex_max_degree

        """
        return len(self.vertex_neighbors(vertex))

    def vertex_min_degree(self) -> int:
        """Compute the minimum degree of all vertices.

        Returns
        -------
        int
            The lowest degree of all vertices.

        See Also
        --------
        vertex_degree, vertex_max_degree

        """
        if not self._vertex:
            return 0
        return min(self.vertex_degree(vertex) for vertex in self.vertices())

    def vertex_max_degree(self) -> int:
        """Compute the maximum degree of all vertices.

        Returns
        -------
        int
            The highest degree of all vertices.

        See Also
        --------
        vertex_degree, vertex_min_degree

        """
        if not self._vertex:
            return 0
        return max(self.vertex_degree(vertex) for vertex in self.vertices())

    def vertex_faces(self, vertex: Vertex) -> list[Face]:
        """Return all faces connected to a vertex.

        Parameters
        ----------
        vertex
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of faces connected to a vertex.

        See Also
        --------
        vertex_neighbors, vertex_cells

        """
        faces = []
        for nbr in self._plane[vertex]:
            for face in self._plane[vertex][nbr]:
                if face is not None:
                    faces.append(face)
        return faces

    def vertex_cells(self, vertex: Vertex) -> list[Cell]:
        """Return all cells connected to a vertex.

        Parameters
        ----------
        vertex
            The identifier of the vertex.

        Returns
        -------
        list[int]
            The list of cells connected to a vertex.

        See Also
        --------
        vertex_neighbors, vertex_faces, vertex_halffaces

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
    #     is_edge_on_boundary, is_face_on_boundary, is_cell_on_boundary

    #     """
    #     halffaces = self.vertex_halffaces(vertex)
    #     for halfface in halffaces:
    #         if self.is_halfface_on_boundary(halfface):
    #             return True
    #     return False

    # --------------------------------------------------------------------------
    # Vertex Geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, vertex: Vertex, axes: str = "xyz") -> list[float]:
        """Return the coordinates of a vertex.

        Parameters
        ----------
        vertex
            The identifier of the vertex.
        axes
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list[float]
            Coordinates of the vertex.

        """
        return [self._vertex[vertex][axis] for axis in axes]

    def vertices_coordinates(self, vertices: Iterable[Vertex], axes: str = "xyz") -> list[list[float]]:
        """Return the coordinates of multiple vertices.

        Parameters
        ----------
        vertices
            The vertex identifiers.
        axes
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list of list[float]
            Coordinates of the vertices.

        """
        return [self.vertex_coordinates(vertex, axes=axes) for vertex in vertices]

    def vertex_point(self, vertex: Vertex) -> Point:
        """Return the point representation of a vertex.

        Parameters
        ----------
        vertex
            The identifier of the vertex.

        Returns
        -------
        Point
            The point.

        """
        return Point(*self.vertex_coordinates(vertex))

    def vertices_points(self, vertices: Iterable[Vertex]) -> list[Point]:
        """Returns the point representation of multiple vertices.

        Parameters
        ----------
         vertices
            The vertex identifiers.

        Returns
        -------
        list of Point
            The points.

        """
        return [self.vertex_point(vertex) for vertex in vertices]

    # --------------------------------------------------------------------------
    # Edge Accessors
    # --------------------------------------------------------------------------

    @overload
    def edges(self, data: Literal[False] = False) -> Iterator[Edge]: ...

    @overload
    def edges(self, data: Literal[True]) -> Iterator[tuple[Edge, EdgeAttributeView]]: ...

    @overload
    def edges(self, data: bool) -> Iterator[Union[Edge, tuple[Edge, EdgeAttributeView]]]: ...

    def edges(self, data: bool = False) -> Iterator[Any]:
        """Iterate over the edges of the cell network.

        Parameters
        ----------
        data
            If True, yield the edge attributes in addition to the edge identifiers.

        Yields
        ------
        tuple[int, int]
            The edge identifier if `data` is `False`.
        tuple[tuple[int, int], EdgeAttributeView]
            The edge identifier and its attributes if `data` is `True`.

        """
        seen = set()
        for u, nbrs in iter(self._edge.items()):
            for v in nbrs:
                if (u, v) in seen or (v, u) in seen:
                    continue
                seen.add((u, v))
                seen.add((v, u))
                if data:
                    yield (u, v), self.edge_attributes((u, v))
                else:
                    yield u, v

    @overload
    def edges_where(
        self,
        conditions: Optional[Mapping[str, Any]] = None,
        data: Literal[False] = False,
        **kwargs: Any,
    ) -> Iterator[Edge]: ...

    @overload
    def edges_where(
        self,
        conditions: Optional[Mapping[str, Any]],
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Edge, EdgeAttributeView]]: ...

    @overload
    def edges_where(
        self,
        *,
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Edge, EdgeAttributeView]]: ...

    @overload
    def edges_where(
        self,
        conditions: Optional[Mapping[str, Any]],
        data: bool,
        **kwargs: Any,
    ) -> Iterator[Union[Edge, tuple[Edge, EdgeAttributeView]]]: ...

    def edges_where(
        self,
        conditions: Optional[Mapping[str, Any]] = None,
        data: bool = False,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data
            If True, yield the edge attributes in addition to the identifiers.
        **kwargs
            Additional conditions provided as named function arguments.

        Yields
        ------
        tuple[int, int]
            A matching edge identifier if `data` is `False`.
        tuple[tuple[int, int], EdgeAttributeView]
            A matching edge identifier and its attributes if `data` is `True`.

        See Also
        --------
        edges_where_predicate
        vertices_where, faces_where, cells_where

        """
        conditions = dict(conditions or {})
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

    @overload
    def edges_where_predicate(
        self,
        predicate: Callable[[Edge, EdgeAttributeView], bool],
        data: Literal[False] = False,
    ) -> Iterator[Edge]: ...

    @overload
    def edges_where_predicate(
        self,
        predicate: Callable[[Edge, EdgeAttributeView], bool],
        data: Literal[True],
    ) -> Iterator[tuple[Edge, EdgeAttributeView]]: ...

    @overload
    def edges_where_predicate(
        self,
        predicate: Callable[[Edge, EdgeAttributeView], bool],
        data: bool,
    ) -> Iterator[Union[Edge, tuple[Edge, EdgeAttributeView]]]: ...

    def edges_where_predicate(
        self,
        predicate: Callable[[Edge, EdgeAttributeView], bool],
        data: bool = False,
    ) -> Iterator[Any]:
        """Get edges for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate
            The condition you want to evaluate.
            The callable takes 2 parameters: the edge identifier and the edge attributes, and should return True or False.
        data
            If True, yield the edge attributes in addition to the identifiers.

        Yields
        ------
        tuple[int, int]
            A matching edge identifier if `data` is `False`.
        tuple[tuple[int, int], EdgeAttributeView]
            A matching edge identifier and its attributes if `data` is `True`.

        See Also
        --------
        edges_where
        vertices_where_predicate, faces_where_predicate, cells_where_predicate

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

    def update_default_edge_attributes(
        self,
        attr_dict: Optional[Mapping[str, Any]] = None,
        **kwattr: Any,
    ) -> None:
        """Update the default edge attributes.

        Parameters
        ----------
        attr_dict
            A dictionary of attributes with their default values.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        update_default_vertex_attributes, update_default_face_attributes, update_default_cell_attributes

        Notes
        -----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary.

        """
        attr_dict = dict(attr_dict or {})
        attr_dict.update(kwattr)
        self.default_edge_attributes.update(attr_dict)

    @overload
    def edge_attribute(self, edge: Edge, name: str) -> Any: ...

    @overload
    def edge_attribute(self, edge: Edge, name: str, value: Any) -> None: ...

    def edge_attribute(self, edge: Edge, name: str, value: Any = _MISSING) -> Any:
        """Get or set an attribute of an edge.

        Parameters
        ----------
        edge
            The edge identifier.
        name
            The name of the attribute.
        value
            The value of the attribute.

        Returns
        -------
        Any
            The attribute value when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If the edge does not exist.

        """
        if not self.has_edge(edge):
            raise KeyError(edge)

        key = _edge_data_key(edge)
        attr = self._edge_data.get(key, {})

        if value is not _MISSING:
            attr.update({name: value})
            self._edge_data[key] = attr
            return
        if name in attr:
            return attr[name]
        if name in self.default_edge_attributes:
            return self.default_edge_attributes[name]

    def unset_edge_attribute(self, edge: Edge, name: str) -> None:
        """Unset the attribute of an edge.

        Parameters
        ----------
        edge
            The edge identifier.
        name
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
        edge_attribute

        Notes
        -----
        Unsetting the value of an edge attribute implicitly sets it back to the value
        stored in the default edge attribute dict.

        """
        if not self.has_edge(edge):
            raise KeyError(edge)

        attr = self._edge_data[_edge_data_key(edge)]
        if name in attr:
            del attr[name]

    @overload
    def edge_attributes(self, edge: Edge, names: None = None, values: None = None) -> EdgeAttributeView: ...

    @overload
    def edge_attributes(self, edge: Edge, names: None, values: Sequence[Any]) -> EdgeAttributeView: ...

    @overload
    def edge_attributes(self, edge: Edge, names: Sequence[str], values: None = None) -> list[Any]: ...

    @overload
    def edge_attributes(self, edge: Edge, names: Sequence[str], values: Sequence[Any]) -> None: ...

    def edge_attributes(
        self,
        edge: Edge,
        names: Optional[Sequence[str]] = None,
        values: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Get or set multiple attributes of an edge.

        Parameters
        ----------
        edge
            The identifier of the edge.
        names
            A list of attribute names.
        values
            A list of attribute values.

        Returns
        -------
        EdgeAttributeView
            All attributes when `names` is not provided.
        list[Any]
            The requested attribute values when `names` is provided and `values` is not provided.
        None
            When both `names` and `values` are provided.

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        edge_attribute, edges_attribute, edges_attributes
        vertex_attributes, face_attributes, cell_attributes

        """
        if not self.has_edge(edge):
            raise KeyError(edge)

        if names and values is not None:
            for name, value in zip(names, values):
                self._edge_data[_edge_data_key(edge)][name] = value
            return
        if not names:
            return EdgeAttributeView(self.default_edge_attributes, self._edge_data[_edge_data_key(edge)])
        values = []
        for name in names:
            value = self.edge_attribute(edge, name)
            values.append(value)
        return values

    @overload
    def edges_attribute(
        self,
        name: str,
        *,
        edges: Optional[Iterable[Edge]] = None,
    ) -> list[Any]: ...

    @overload
    def edges_attribute(
        self,
        name: str,
        value: Any,
        edges: Optional[Iterable[Edge]] = None,
    ) -> None: ...

    def edges_attribute(
        self,
        name: str,
        value: Any = _MISSING,
        edges: Optional[Iterable[Edge]] = None,
    ) -> Optional[list[Any]]:
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name
            The name of the attribute.
        value
            The value of the attribute.
            Default is None.
        edges
            A list of edge identifiers.

        Returns
        -------
        list[Any]
            The attribute values when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        See Also
        --------
        edge_attribute, edge_attributes, edges_attributes
        vertex_attribute, face_attribute, cell_attribute

        """
        edges = self.edges() if edges is None else edges
        if value is not _MISSING:
            for edge in edges:
                self.edge_attribute(edge, name, value)
            return
        return [self.edge_attribute(edge, name) for edge in edges]

    @overload
    def edges_attributes(
        self,
        names: None = None,
        values: None = None,
        edges: Optional[Iterable[Edge]] = None,
    ) -> list[EdgeAttributeView]: ...

    @overload
    def edges_attributes(
        self,
        names: Sequence[str],
        values: None = None,
        edges: Optional[Iterable[Edge]] = None,
    ) -> list[list[Any]]: ...

    @overload
    def edges_attributes(
        self,
        names: Sequence[str],
        values: Sequence[Any],
        edges: Optional[Iterable[Edge]] = None,
    ) -> None: ...

    @overload
    def edges_attributes(
        self,
        names: None,
        values: Sequence[Any],
        edges: Optional[Iterable[Edge]] = None,
    ) -> None: ...

    def edges_attributes(
        self,
        names: Optional[Sequence[str]] = None,
        values: Optional[Sequence[Any]] = None,
        edges: Optional[Iterable[Edge]] = None,
    ) -> Optional[list[Any]]:
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names
            The names of the attribute.
        values
            The values of the attributes.
        edges
            A list of edge identifiers.

        Returns
        -------
        list[EdgeAttributeView]
            All attributes when `names` is not provided.
        list[list[Any]]
            The requested attribute values when `names` is provided and `values` is not provided.
        None
            When `values` is provided.

        Raises
        ------
        KeyError
            If any of the edges does not exist.

        See Also
        --------
        edge_attribute, edge_attributes, edges_attribute
        vertex_attributes, face_attributes, cell_attributes

        """
        edges = self.edges() if edges is None else edges
        if values is not None:
            for edge in edges:
                self.edge_attributes(edge, names, values)
            return
        return [self.edge_attributes(edge, names) for edge in edges]

    # --------------------------------------------------------------------------
    # Edge Topology
    # --------------------------------------------------------------------------

    def has_edge(self, edge: Edge, directed: bool = False) -> bool:
        """Verify that the cell network contains a directed edge (u, v).

        Parameters
        ----------
        edge
            The identifier of the edge.
        directed
            If `True`, the direction of the edge should be taken into account.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.

        See Also
        --------
        has_vertex, has_face, has_cell

        """
        u, v = edge
        if directed:
            return u in self._edge and v in self._edge[u]
        return (u in self._edge and v in self._edge[u]) or (v in self._edge and u in self._edge[v])

    def edge_faces(self, edge: Edge) -> list[Face]:
        """Return the faces adjacent to an edge.

        Parameters
        ----------
        edge
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

    def edge_cells(self, edge: Edge) -> list[Cell]:
        """Ordered cells around edge (u, v).

        Parameters
        ----------
        edge
            The identifier of the edge.

        Returns
        -------
        list[int]
            Ordered list of keys identifying the ordered cells.

        See Also
        --------
        edge_halffaces

        """
        u, v = edge
        cells = []
        for cell in list(self._plane[u].get(v, {}).values()) + list(self._plane[v].get(u, {}).values()):
            if cell is not None and cell not in cells:
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
    #     is_vertex_on_boundary, is_face_on_boundary, is_cell_on_boundary

    #     Notes
    #     -----
    #     This method simply checks if u-v or v-u is on the edge of the cell network.
    #     The direction u-v does not matter.

    #     """
    #     u, v = edge
    #     return None in self._plane[u][v].values()

    def edges_without_face(self) -> list[Edge]:
        """Find the edges that are not part of a face.

        Returns
        -------
        list[int]
            The edges without face.

        """
        edges = {edge for edge in self.edges() if not self.edge_faces(edge)}
        return list(edges)

    def nonmanifold_edges(self) -> list[Edge]:
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

    def edge_coordinates(self, edge: Edge, axes: str = "xyz") -> tuple[list[float], list[float]]:
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        edge
            The edge identifier.
        axes
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple[list[float], list[float]]
            The coordinates of the start point.
            The coordinates of the end point.

        """
        u, v = edge
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_start(self, edge: Edge) -> Point:
        """Return the start point of an edge.

        Parameters
        ----------
        edge
            The edge identifier.

        Returns
        -------
        Point
            The start point.

        """
        return self.vertex_point(edge[0])

    def edge_end(self, edge: Edge) -> Point:
        """Return the end point of an edge.

        Parameters
        ----------
        edge
            The edge identifier.

        Returns
        -------
        Point
            The end point.

        """
        return self.vertex_point(edge[1])

    def edge_midpoint(self, edge: Edge) -> Point:
        """Return the midpoint of an edge.

        Parameters
        ----------
        edge
            The edge identifier.

        Returns
        -------
        Point
            The midpoint.

        See Also
        --------
        edge_start, edge_end, edge_point

        """
        a, b = self.edge_coordinates(edge)
        return Point(0.5 * (a[0] + b[0]), 0.5 * (a[1] + b[1]), 0.5 * (a[2] + b[2]))

    def edge_point(self, edge: Edge, t: float = 0.5) -> Point:
        """Return the point at a parametric location along an edge.

        Parameters
        ----------
        edge
            The edge identifier.
        t
            The location of the point on the edge.
            If the value of `t` is outside the range 0-1, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        Point
            The XYZ coordinates of the point.

        See Also
        --------
        edge_start, edge_end, edge_midpoint

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

    def edge_vector(self, edge: Edge) -> Vector:
        """Return the vector of an edge.

        Parameters
        ----------
        edge
            The edge identifier.

        Returns
        -------
        Vector
            The vector from start to end.

        """
        a, b = self.edge_coordinates(edge)
        return Vector.from_start_end(a, b)

    def edge_direction(self, edge: Edge) -> Vector:
        """Return the direction vector of an edge.

        Parameters
        ----------
        edge
            The edge identifier.

        Returns
        -------
        Vector
            The direction vector of the edge.

        """
        return Vector(*normalize_vector(self.edge_vector(edge)))

    def edge_line(self, edge: Edge) -> Line:
        """Return the line representation of an edge.

        Parameters
        ----------
        edge
            The edge identifier.

        Returns
        -------
        Line
            The line.

        """
        return Line(*self.edge_coordinates(edge))

    def edge_length(self, edge: Edge) -> float:
        """Return the length of an edge.

        Parameters
        ----------
        edge
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

    @overload
    def faces(self, data: Literal[False] = False) -> Iterator[Face]: ...

    @overload
    def faces(self, data: Literal[True]) -> Iterator[tuple[Face, FaceAttributeView]]: ...

    @overload
    def faces(self, data: bool) -> Iterator[Union[Face, tuple[Face, FaceAttributeView]]]: ...

    def faces(self, data: bool = False) -> Iterator[Any]:
        """Iterate over the faces of the cell network.

        Parameters
        ----------
        data
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int
            The face identifier if `data` is `False`.
        tuple[int, FaceAttributeView]
            The face identifier and its attributes if `data` is `True`.

        See Also
        --------
        vertices, edges, cells

        """
        for face in self._face:
            if not data:
                yield face
            else:
                yield face, self.face_attributes(face)

    @overload
    def faces_where(
        self,
        conditions: Optional[Mapping[str, Any]] = None,
        data: Literal[False] = False,
        **kwargs: Any,
    ) -> Iterator[Face]: ...

    @overload
    def faces_where(
        self,
        conditions: Optional[Mapping[str, Any]],
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Face, FaceAttributeView]]: ...

    @overload
    def faces_where(
        self,
        *,
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Face, FaceAttributeView]]: ...

    @overload
    def faces_where(
        self,
        conditions: Optional[Mapping[str, Any]],
        data: bool,
        **kwargs: Any,
    ) -> Iterator[Union[Face, tuple[Face, FaceAttributeView]]]: ...

    def faces_where(
        self,
        conditions: Optional[Mapping[str, Any]] = None,
        data: bool = False,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """Get faces for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data
            If True, yield the face attributes in addition to the identifiers.
        **kwargs
            Additional conditions provided as named function arguments.

        Yields
        ------
        int
            A matching face identifier if `data` is `False`.
        tuple[int, FaceAttributeView]
            A matching face identifier and its attributes if `data` is `True`.

        See Also
        --------
        faces_where_predicate
        vertices_where, edges_where, cells_where

        """
        conditions = dict(conditions or {})
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

    @overload
    def faces_where_predicate(
        self,
        predicate: Callable[[Face, FaceAttributeView], bool],
        data: Literal[False] = False,
    ) -> Iterator[Face]: ...

    @overload
    def faces_where_predicate(
        self,
        predicate: Callable[[Face, FaceAttributeView], bool],
        data: Literal[True],
    ) -> Iterator[tuple[Face, FaceAttributeView]]: ...

    @overload
    def faces_where_predicate(
        self,
        predicate: Callable[[Face, FaceAttributeView], bool],
        data: bool,
    ) -> Iterator[Union[Face, tuple[Face, FaceAttributeView]]]: ...

    def faces_where_predicate(
        self,
        predicate: Callable[[Face, FaceAttributeView], bool],
        data: bool = False,
    ) -> Iterator[Any]:
        """Get faces for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate
            The condition you want to evaluate.
            The callable takes 2 parameters: the face identifier and the the face attributes, and should return True or False.
        data
            If True, yield the face attributes in addition to the identifiers.

        Yields
        ------
        int
            A matching face identifier if `data` is `False`.
        tuple[int, FaceAttributeView]
            A matching face identifier and its attributes if `data` is `True`.

        See Also
        --------
        faces_where
        vertices_where_predicate, edges_where_predicate, cells_where_predicate

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

    def update_default_face_attributes(
        self,
        attr_dict: Optional[Mapping[str, Any]] = None,
        **kwattr: Any,
    ) -> None:
        """Update the default face attributes.

        Parameters
        ----------
        attr_dict
            A dictionary of attributes with their default values.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        update_default_vertex_attributes, update_default_edge_attributes, update_default_cell_attributes

        Notes
        -----
        Named arguments overwrite correpsonding key-value pairs in the attribute dictionary.

        """
        attr_dict = dict(attr_dict or {})
        attr_dict.update(kwattr)
        self.default_face_attributes.update(attr_dict)

    @overload
    def face_attribute(self, face: Face, name: str) -> Any: ...

    @overload
    def face_attribute(self, face: Face, name: str, value: Any) -> None: ...

    def face_attribute(self, face: Face, name: str, value: Any = _MISSING) -> Any:
        """Get or set an attribute of a face.

        Parameters
        ----------
        face
            The face identifier.
        name
            The name of the attribute.
        value
            The value of the attribute.

        Returns
        -------
        Any
            The attribute value when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        unset_face_attribute
        face_attributes, faces_attribute, faces_attributes
        vertex_attribute, edge_attribute, cell_attribute

        """
        if face not in self._face:
            raise KeyError(face)

        if value is not _MISSING:
            if face not in self._face_data:
                self._face_data[face] = {}
            self._face_data[face][name] = value
            return
        if face in self._face_data and name in self._face_data[face]:
            return self._face_data[face][name]
        if name in self.default_face_attributes:
            return self.default_face_attributes[name]

    def unset_face_attribute(self, face: Face, name: str) -> None:
        """Unset the attribute of a face.

        Parameters
        ----------
        face
            The face identifier.
        name
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
        face_attribute

        Notes
        -----
        Unsetting the value of a face attribute implicitly sets it back to the value
        stored in the default face attribute dict.

        """
        if face not in self._face:
            raise KeyError(face)

        if face in self._face_data and name in self._face_data[face]:
            del self._face_data[face][name]

    @overload
    def face_attributes(self, face: Face, names: None = None, values: None = None) -> FaceAttributeView: ...

    @overload
    def face_attributes(self, face: Face, names: None, values: Sequence[Any]) -> FaceAttributeView: ...

    @overload
    def face_attributes(self, face: Face, names: Sequence[str], values: None = None) -> list[Any]: ...

    @overload
    def face_attributes(self, face: Face, names: Sequence[str], values: Sequence[Any]) -> None: ...

    def face_attributes(
        self,
        face: Face,
        names: Optional[Sequence[str]] = None,
        values: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Get or set multiple attributes of a face.

        Parameters
        ----------
        face
            The identifier of the face.
        names
            A list of attribute names.
        values
            A list of attribute values.

        Returns
        -------
        FaceAttributeView
            All attributes when `names` is not provided.
        list[Any]
            The requested attribute values when `names` is provided and `values` is not provided.
        None
            When both `names` and `values` are provided.

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        face_attribute, faces_attribute, faces_attributes
        vertex_attributes, edge_attributes, cell_attributes

        """
        if face not in self._face:
            raise KeyError(face)

        if names and values is not None:
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

    @overload
    def faces_attribute(
        self,
        name: str,
        *,
        faces: Optional[Iterable[Face]] = None,
    ) -> list[Any]: ...

    @overload
    def faces_attribute(
        self,
        name: str,
        value: Any,
        faces: Optional[Iterable[Face]] = None,
    ) -> None: ...

    def faces_attribute(
        self,
        name: str,
        value: Any = _MISSING,
        faces: Optional[Iterable[Face]] = None,
    ) -> Optional[list[Any]]:
        """Get or set an attribute of multiple faces.

        Parameters
        ----------
        name
            The name of the attribute.
        value
            The value of the attribute.
            Default is None.
        faces
            A list of face identifiers.

        Returns
        -------
        list[Any]
            The attribute values when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        See Also
        --------
        face_attribute, face_attributes, faces_attributes
        vertex_attribute, edge_attribute, cell_attribute

        """
        faces = self.faces() if faces is None else faces
        if value is not _MISSING:
            for face in faces:
                self.face_attribute(face, name, value)
            return
        return [self.face_attribute(face, name) for face in faces]

    @overload
    def faces_attributes(
        self,
        names: None = None,
        values: None = None,
        faces: Optional[Iterable[Face]] = None,
    ) -> list[FaceAttributeView]: ...

    @overload
    def faces_attributes(
        self,
        names: Sequence[str],
        values: None = None,
        faces: Optional[Iterable[Face]] = None,
    ) -> list[list[Any]]: ...

    @overload
    def faces_attributes(
        self,
        names: Sequence[str],
        values: Sequence[Any],
        faces: Optional[Iterable[Face]] = None,
    ) -> None: ...

    @overload
    def faces_attributes(
        self,
        names: None,
        values: Sequence[Any],
        faces: Optional[Iterable[Face]] = None,
    ) -> None: ...

    def faces_attributes(
        self,
        names: Optional[Sequence[str]] = None,
        values: Optional[Sequence[Any]] = None,
        faces: Optional[Iterable[Face]] = None,
    ) -> Optional[list[Any]]:
        """Get or set multiple attributes of multiple faces.

        Parameters
        ----------
        names
            The names of the attribute.
            Default is None.
        values
            The values of the attributes.
            Default is None.
        faces
            A list of face identifiers.

        Returns
        -------
        list[FaceAttributeView]
            All attributes when `names` is not provided.
        list[list[Any]]
            The requested attribute values when `names` is provided and `values` is not provided.
        None
            When `values` is provided.

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        See Also
        --------
        face_attribute, face_attributes, faces_attribute
        vertex_attributes, edge_attributes, cell_attributes

        """
        faces = self.faces() if faces is None else faces
        if values is not None:
            for face in faces:
                self.face_attributes(face, names, values)
            return
        return [self.face_attributes(face, names) for face in faces]

    # --------------------------------------------------------------------------
    # Face Topology
    # --------------------------------------------------------------------------

    def has_face(self, face: Face) -> bool:
        """Verify that a face is part of the cell network.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.

        See Also
        --------
        has_vertex, has_edge, has_cell

        """
        return face in self._face

    def face_vertices(self, face: Face) -> list[Vertex]:
        """The vertices of a face.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        list[int]
            Ordered vertex identifiers.

        """
        return self._face[face]

    def face_edges(self, face: Face) -> list[Edge]:
        """The edges of a face.

        Parameters
        ----------
        face
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

    def face_cells(self, face: Face) -> list[Cell]:
        """Return the cells connected to a face.

        Parameters
        ----------
        face
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
            if cell is not None and cell not in cells:
                cells.append(cell)
            cell = self._plane[v][u][face]
            if cell is not None and cell not in cells:
                cells.append(cell)
        return cells

    def faces_without_cell(self) -> list[Face]:
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
    def is_face_on_boundary(self, face: Face) -> bool:
        """Verify that a face is on the boundary.

        Parameters
        ----------
        face
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

    def faces_on_boundaries(self) -> list[Face]:
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

    def face_coordinates(self, face: Face, axes: str = "xyz") -> list[list[float]]:
        """Compute the coordinates of the vertices of a face.

        Parameters
        ----------
        face
            The identifier of the face.
        axes
            The axes alon which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list[list[float]]
            The coordinates of the vertices of the face.

        See Also
        --------
        face_points, face_polygon, face_normal, face_centroid, face_center
        face_area, face_flatness, face_aspect_ratio

        """
        return [self.vertex_coordinates(vertex, axes=axes) for vertex in self.face_vertices(face)]

    def face_points(self, face: Face) -> list[Point]:
        """Compute the points of the vertices of a face.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        list[Point]
            The points of the vertices of the face.

        See Also
        --------
        face_polygon, face_normal, face_centroid, face_center

        """
        return [self.vertex_point(vertex) for vertex in self.face_vertices(face)]

    def face_polygon(self, face: Face) -> Polygon:
        """Compute the polygon of a face.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        Polygon
            The polygon of the face.

        See Also
        --------
        face_points, face_normal, face_centroid, face_center

        """
        return Polygon(self.face_points(face))

    def face_normal(self, face: Face, unitized: bool = True) -> Vector:
        """Compute the oriented normal of a face.

        Parameters
        ----------
        face
            The identifier of the face.
        unitized
            If True, unitize the normal vector.

        Returns
        -------
        Vector
            The normal vector.

        See Also
        --------
        face_points, face_polygon, face_centroid, face_center

        """
        return Vector(*normal_polygon(self.face_coordinates(face), unitized=unitized))

    def face_centroid(self, face: Face) -> Point:
        """Compute the point at the centroid of a face.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        Point
            The coordinates of the centroid.

        See Also
        --------
        face_points, face_polygon, face_normal, face_center

        """
        return Point(*centroid_points(self.face_coordinates(face)))

    def face_center(self, face: Face) -> Point:
        """Compute the point at the center of mass of a face.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        Point
            The coordinates of the center of mass.

        See Also
        --------
        face_points, face_polygon, face_normal, face_centroid

        """
        return Point(*centroid_polygon(self.face_coordinates(face)))

    def face_area(self, face: Face) -> float:
        """Compute the oriented area of a face.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        float
            The non-oriented area of the face.

        See Also
        --------
        face_flatness, face_aspect_ratio

        """
        return length_vector(self.face_normal(face, unitized=False))

    def face_plane(self, face: Face) -> Plane:
        """Compute the plane of a face.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        Plane
            The plane of the face.

        See Also
        --------
        face_points, face_polygon, face_normal, face_centroid, face_center

        """
        return Plane(self.face_centroid(face), self.face_normal(face))

    def face_flatness(self, face: Face, maxdev: float = 0.02) -> float:
        """Compute the flatness of a face.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        float
            The flatness.

        See Also
        --------
        face_area, face_aspect_ratio

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

    def face_aspect_ratio(self, face: Face) -> float:
        """Face aspect ratio as the ratio between the lengths of the maximum and minimum face edges.

        Parameters
        ----------
        face
            The identifier of the face.

        Returns
        -------
        float
            The aspect ratio.

        See Also
        --------
        face_area, face_flatness

        References
        ----------
        * Wikipedia. *Types of mesh*. Available at: https://en.wikipedia.org/wiki/Types_of_mesh.

        """
        lengths = [self.edge_length(edge) for edge in self.face_edges(face)]
        return max(lengths) / min(lengths)

    # --------------------------------------------------------------------------
    # Cell Accessors
    # --------------------------------------------------------------------------

    @overload
    def cells(self, data: Literal[False] = False) -> Iterator[Cell]: ...

    @overload
    def cells(self, data: Literal[True]) -> Iterator[tuple[Cell, CellAttributeView]]: ...

    @overload
    def cells(self, data: bool) -> Iterator[Union[Cell, tuple[Cell, CellAttributeView]]]: ...

    def cells(self, data: bool = False) -> Iterator[Any]:
        """Iterate over the cells of the cell network.

        Parameters
        ----------
        data
            If True, yield the cell attributes in addition to the cell identifiers.

        Yields
        ------
        int
            The cell identifier if `data` is `False`.
        tuple[int, CellAttributeView]
            The cell identifier and its attributes if `data` is `True`.

        See Also
        --------
        vertices, edges, faces

        """
        for cell in self._cell:
            if not data:
                yield cell
            else:
                yield cell, self.cell_attributes(cell)

    @overload
    def cells_where(
        self,
        conditions: Optional[Mapping[str, Any]] = None,
        data: Literal[False] = False,
        **kwargs: Any,
    ) -> Iterator[Cell]: ...

    @overload
    def cells_where(
        self,
        conditions: Optional[Mapping[str, Any]],
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Cell, CellAttributeView]]: ...

    @overload
    def cells_where(
        self,
        *,
        data: Literal[True],
        **kwargs: Any,
    ) -> Iterator[tuple[Cell, CellAttributeView]]: ...

    @overload
    def cells_where(
        self,
        conditions: Optional[Mapping[str, Any]],
        data: bool,
        **kwargs: Any,
    ) -> Iterator[Union[Cell, tuple[Cell, CellAttributeView]]]: ...

    def cells_where(
        self,
        conditions: Optional[Mapping[str, Any]] = None,
        data: bool = False,
        **kwargs: Any,
    ) -> Iterator[Any]:
        """Get cells for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data
            If True, yield the cell attributes in addition to the identifiers.
        **kwargs
            Additional conditions provided as named function arguments.

        Yields
        ------
        int
            A matching cell identifier if `data` is `False`.
        tuple[int, CellAttributeView]
            A matching cell identifier and its attributes if `data` is `True`.

        See Also
        --------
        cells_where_predicate
        vertices_where, edges_where, faces_where

        """
        conditions = dict(conditions or {})
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

    @overload
    def cells_where_predicate(
        self,
        predicate: Callable[[Cell, CellAttributeView], bool],
        data: Literal[False] = False,
    ) -> Iterator[Cell]: ...

    @overload
    def cells_where_predicate(
        self,
        predicate: Callable[[Cell, CellAttributeView], bool],
        data: Literal[True],
    ) -> Iterator[tuple[Cell, CellAttributeView]]: ...

    @overload
    def cells_where_predicate(
        self,
        predicate: Callable[[Cell, CellAttributeView], bool],
        data: bool,
    ) -> Iterator[Union[Cell, tuple[Cell, CellAttributeView]]]: ...

    def cells_where_predicate(
        self,
        predicate: Callable[[Cell, CellAttributeView], bool],
        data: bool = False,
    ) -> Iterator[Any]:
        """Get cells for which a certain condition or set of conditions is true using a lambda function.

        Parameters
        ----------
        predicate
            The condition you want to evaluate.
            The callable takes 2 parameters: the cell identifier and the cell attributes, and should return True or False.
        data
            If True, yield the cell attributes in addition to the identifiers.

        Yields
        ------
        int
            A matching cell identifier if `data` is `False`.
        tuple[int, CellAttributeView]
            A matching cell identifier and its attributes if `data` is `True`.

        See Also
        --------
        cells_where
        vertices_where_predicate, edges_where_predicate, faces_where_predicate

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

    def update_default_cell_attributes(
        self,
        attr_dict: Optional[Mapping[str, Any]] = None,
        **kwattr: Any,
    ) -> None:
        """Update the default cell attributes.

        Parameters
        ----------
        attr_dict
            A dictionary of attributes with their default values.
        **kwattr
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        update_default_vertex_attributes, update_default_edge_attributes, update_default_face_attributes

        Notes
        -----
        Named arguments overwrite corresponding cell-value pairs in the attribute dictionary.

        """
        attr_dict = dict(attr_dict or {})
        attr_dict.update(kwattr)
        self.default_cell_attributes.update(attr_dict)

    @overload
    def cell_attribute(self, cell: Cell, name: str) -> Any: ...

    @overload
    def cell_attribute(self, cell: Cell, name: str, value: Any) -> None: ...

    def cell_attribute(self, cell: Cell, name: str, value: Any = _MISSING) -> Any:
        """Get or set an attribute of a cell.

        Parameters
        ----------
        cell
            The cell identifier.
        name
            The name of the attribute.
        value
            The value of the attribute.

        Returns
        -------
        Any
            The attribute value when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If the cell does not exist.

        See Also
        --------
        unset_cell_attribute
        cell_attributes, cells_attribute, cells_attributes
        vertex_attribute, edge_attribute, face_attribute

        """
        if cell not in self._cell:
            raise KeyError(cell)
        if value is not _MISSING:
            if cell not in self._cell_data:
                self._cell_data[cell] = {}
            self._cell_data[cell][name] = value
            return
        if cell in self._cell_data and name in self._cell_data[cell]:
            return self._cell_data[cell][name]
        if name in self.default_cell_attributes:
            return self.default_cell_attributes[name]

    def unset_cell_attribute(self, cell: Cell, name: str) -> None:
        """Unset the attribute of a cell.

        Parameters
        ----------
        cell
            The cell identifier.
        name
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
        cell_attribute

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

    @overload
    def cell_attributes(self, cell: Cell, names: None = None, values: None = None) -> CellAttributeView: ...

    @overload
    def cell_attributes(self, cell: Cell, names: None, values: Sequence[Any]) -> CellAttributeView: ...

    @overload
    def cell_attributes(self, cell: Cell, names: Sequence[str], values: None = None) -> list[Any]: ...

    @overload
    def cell_attributes(self, cell: Cell, names: Sequence[str], values: Sequence[Any]) -> None: ...

    def cell_attributes(
        self,
        cell: Cell,
        names: Optional[Sequence[str]] = None,
        values: Optional[Sequence[Any]] = None,
    ) -> Any:
        """Get or set multiple attributes of a cell.

        Parameters
        ----------
        cell
            The identifier of the cell.
        names
            A list of attribute names.
        values
            A list of attribute values.

        Returns
        -------
        CellAttributeView
            All attributes when `names` is not provided.
        list[Any]
            The requested attribute values when `names` is provided and `values` is not provided.
        None
            When both `names` and `values` are provided.

        Raises
        ------
        KeyError
            If the cell does not exist.

        See Also
        --------
        cell_attribute, cells_attribute, cells_attributes
        vertex_attributes, edge_attributes, face_attributes

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

    @overload
    def cells_attribute(
        self,
        name: str,
        *,
        cells: Optional[Iterable[Cell]] = None,
    ) -> list[Any]: ...

    @overload
    def cells_attribute(
        self,
        name: str,
        value: Any,
        cells: Optional[Iterable[Cell]] = None,
    ) -> None: ...

    def cells_attribute(
        self,
        name: str,
        value: Any = _MISSING,
        cells: Optional[Iterable[Cell]] = None,
    ) -> Optional[list[Any]]:
        """Get or set an attribute of multiple cells.

        Parameters
        ----------
        name
            The name of the attribute.
        value
            The value of the attribute.
        cells
            A list of cell identifiers.

        Returns
        -------
        list[Any]
            The attribute values when `value` is not provided.
        None
            When `value` is provided.

        Raises
        ------
        KeyError
            If any of the cells does not exist.

        See Also
        --------
        cell_attribute, cell_attributes, cells_attributes
        vertex_attribute, edge_attribute, face_attribute

        """
        cells = self.cells() if cells is None else cells
        if value is not _MISSING:
            for cell in cells:
                self.cell_attribute(cell, name, value)
            return
        return [self.cell_attribute(cell, name) for cell in cells]

    @overload
    def cells_attributes(
        self,
        names: None = None,
        values: None = None,
        cells: Optional[Iterable[Cell]] = None,
    ) -> list[CellAttributeView]: ...

    @overload
    def cells_attributes(
        self,
        names: Sequence[str],
        values: None = None,
        cells: Optional[Iterable[Cell]] = None,
    ) -> list[list[Any]]: ...

    @overload
    def cells_attributes(
        self,
        names: Sequence[str],
        values: Sequence[Any],
        cells: Optional[Iterable[Cell]] = None,
    ) -> None: ...

    @overload
    def cells_attributes(
        self,
        names: None,
        values: Sequence[Any],
        cells: Optional[Iterable[Cell]] = None,
    ) -> None: ...

    def cells_attributes(
        self,
        names: Optional[Sequence[str]] = None,
        values: Optional[Sequence[Any]] = None,
        cells: Optional[Iterable[Cell]] = None,
    ) -> Optional[list[Any]]:
        """Get or set multiple attributes of multiple cells.

        Parameters
        ----------
        names
            The names of the attribute.
            Default is None.
        values
            The values of the attributes.
            Default is None.
        cells
            A list of cell identifiers.

        Returns
        -------
        list[CellAttributeView]
            All attributes when `names` is not provided.
        list[list[Any]]
            The requested attribute values when `names` is provided and `values` is not provided.
        None
            When `values` is provided.

        Raises
        ------
        KeyError
            If any of the faces does not exist.

        See Also
        --------
        cell_attribute, cell_attributes, cells_attribute
        vertex_attributes, edge_attributes, face_attributes

        """
        cells = self.cells() if cells is None else cells
        if values is not None:
            for cell in cells:
                self.cell_attributes(cell, names, values)
            return
        return [self.cell_attributes(cell, names) for cell in cells]

    # --------------------------------------------------------------------------
    # Cell Topology
    # --------------------------------------------------------------------------

    def has_cell(self, cell: Cell) -> bool:
        """Verify that a cell is part of the cell network.

        Parameters
        ----------
        cell
            The identifier of the cell.

        Returns
        -------
        bool
            True if the cell exists, and False otherwise.

        See Also
        --------
        has_vertex, has_edge, has_face

        """
        return cell in self._cell

    def cell_vertices(self, cell: Cell) -> list[Vertex]:
        """The vertices of a cell.

        Parameters
        ----------
        cell
            Identifier of the cell.

        Returns
        -------
        list[int]
            The vertex identifiers of a cell.

        See Also
        --------
        cell_edges, cell_faces, cell_halfedges

        Notes
        -----
        This method is similar to ~compas.datastructures.HalfEdge.vertices,
        but in the context of a cell of the `VolMesh`.

        """
        return list(set([vertex for face in self.cell_faces(cell) for vertex in self.face_vertices(face)]))

    def cell_halfedges(self, cell: Cell) -> list[Edge]:
        """The halfedges of a cell.

        Parameters
        ----------
        cell
            Identifier of the cell.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of a cell.

        See Also
        --------
        cell_edges, cell_faces, cell_vertices

        Notes
        -----
        This method is similar to ~compas.datastructures.HalfEdge.halfedges,
        but in the context of a cell of the `VolMesh`.

        """
        halfedges = []
        for u in self._cell[cell]:
            for v in self._cell[cell][u]:
                halfedges.append((u, v))
        return halfedges

    def cell_edges(self, cell: Cell) -> list[Edge]:
        """Return all edges of a cell.

        Parameters
        ----------
        cell
            The cell identifier.

        Returns
        -------
        list[tuple[int, int]]
            The edges of the cell.

        See Also
        --------
        cell_halfedges, cell_faces, cell_vertices

        Notes
        -----
        This method is similar to ~compas.datastructures.HalfEdge.edges,
        but in the context of a cell of the `VolMesh`.

        """
        seen = set()
        edges = []
        for edge in self.cell_halfedges(cell):
            key = _edge_data_key(edge)
            if key in seen:
                continue
            seen.add(key)
            edges.append(edge)
        return edges

    def cell_faces(self, cell: Cell) -> list[Face]:
        """The faces of a cell.

        Parameters
        ----------
        cell
            Identifier of the cell.

        Returns
        -------
        list[int]
            The faces of a cell.

        See Also
        --------
        cell_halfedges, cell_edges, cell_vertices

        Notes
        -----
        This method is similar to ~compas.datastructures.HalfEdge.faces,
        but in the context of a cell of the `VolMesh`.

        """
        faces = set()
        for vertex in self._cell[cell]:
            faces.update(self._cell[cell][vertex].values())
        return list(faces)

    def cell_vertex_neighbors(self, cell: Cell, vertex: Vertex) -> list[Vertex]:
        """Ordered vertex neighbors of a vertex of a cell.

        Parameters
        ----------
        cell
            Identifier of the cell.
        vertex
            Identifier of the vertex.

        Returns
        -------
        list[int]
            The list of neighboring vertices.

        See Also
        --------
        cell_vertex_faces

        Notes
        -----
        All of the returned vertices are part of the cell.

        This method is similar to ~compas.datastructures.HalfEdge.vertex_neighbors,
        but in the context of a cell of the `VolMesh`.

        """
        if vertex not in self._cell[cell]:
            raise KeyError(vertex)

        nbrs = []
        for nbr in self._edge[vertex]:
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

    def cell_vertex_faces(self, cell: Cell, vertex: Vertex) -> list[Face]:
        """Ordered faces connected to a vertex of a cell.

        Parameters
        ----------
        cell
            Identifier of the cell.
        vertex
            Identifier of the vertex.

        Returns
        -------
        list[int]
            The ordered list of faces connected to a vertex of a cell.

        See Also
        --------
        cell_vertex_neighbors

        Notes
        -----
        All of the returned faces should are part of the same cell.

        This method is similar to ~compas.datastructures.HalfEdge.vertex_faces,
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

    def cell_face_vertices(self, cell: Cell, face: Face) -> list[Vertex]:
        """The vertices of a face of a cell.

        Parameters
        ----------
        cell
            Identifier of the cell.
        face
            Identifier of the face.

        Returns
        -------
        list[int]
            The vertices of the face of the cell.

        Raises
        ------
        KeyError
            If the face does not exist.
        ValueError
            If the face is not part of the cell.

        See Also
        --------
        cell_face_halfedges

        Notes
        -----
        All of the returned vertices are part of the cell.

        This method is similar to ~compas.datastructures.HalfEdge.face_vertices,
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

        raise ValueError("Face {} is not part of cell {}.".format(face, cell))

    def cell_face_halfedges(self, cell: Cell, face: Face) -> list[Edge]:
        """The halfedges of a face of a cell.

        Parameters
        ----------
        cell
            Identifier of the cell.
        face
            Identifier of the face.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of the face of the cell.

        See Also
        --------
        cell_face_vertices

        Notes
        -----
        All of the returned halfedges are part of the cell.

        This method is similar to ~compas.datastructures.HalfEdge.face_halfedges,
        but in the context of a cell of the `VolMesh`.

        """
        vertices = self.cell_face_vertices(cell, face)
        return list(pairwise(vertices + vertices[:1]))

    def cell_halfedge_face(self, cell: Cell, halfedge: Edge) -> Face:
        """Find the face corresponding to a specific halfedge of a cell.

        Parameters
        ----------
        cell
            The identifier of the cell.
        halfedge
            The identifier of the halfedge.

        Returns
        -------
        int
            The identifier of the face.

        See Also
        --------
        cell_halfedge_opposite_face

        Notes
        -----
        This method is similar to ~compas.datastructures.HalfEdge.halfedge_face,
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
    #     cell_halfedge_face

    #     """
    #     u, v = halfedge
    #     return self._cell[cell][v][u]

    def cell_face_neighbors(self, cell: Cell, face: Face) -> list[Face]:
        """Find the faces adjacent to a given face of a cell.

        Parameters
        ----------
        cell
            The identifier of the cell.
        face
            The identifier of the face.

        Returns
        -------
        int
            The identifier of the face.

        See Also
        --------
        cell_neighbors

        Notes
        -----
        This method is similar to ~compas.datastructures.HalfEdge.face_neighbors,
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

    def cell_neighbors(self, cell: Cell) -> list[Cell]:
        """Find the neighbors of a given cell.

        Parameters
        ----------
        cell
            The identifier of the cell.

        Returns
        -------
        list[int]
            The identifiers of the adjacent cells.

        See Also
        --------
        cell_face_neighbors

        """
        nbrs = []
        for face in self.cell_faces(cell):
            for nbr in self.face_cells(face):
                if nbr != cell:
                    nbrs.append(nbr)
        return list(set(nbrs))

    def is_cell_on_boundary(self, cell: Cell) -> bool:
        """Verify that a cell is on the boundary.

        Parameters
        ----------
        cell
            Identifier of the cell.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        See Also
        --------
        is_vertex_on_boundary, is_edge_on_boundary, is_face_on_boundary

        """
        faces = self.cell_faces(cell)
        for face in faces:
            if self.is_face_on_boundary(face):
                return True
        return False

    def cells_on_boundaries(self) -> list[Cell]:
        """Find the cells on the boundary.

        Returns
        -------
        list[int]
            The cells of the boundary.

        See Also
        --------
        vertices_on_boundaries, faces_on_boundaries

        """
        cells = []
        for cell in self.cells():
            if self.is_cell_on_boundary(cell):
                cells.append(cell)
        return cells

    # --------------------------------------------------------------------------
    # Cell Geometry
    # --------------------------------------------------------------------------

    def cell_points(self, cell: Cell) -> list[Point]:
        """Compute the points of the vertices of a cell.

        Parameters
        ----------
        cell
            The identifier of the cell.

        Returns
        -------
        list[Point]
            The points of the vertices of the cell.

        See Also
        --------
        cell_polygon, cell_centroid, cell_center

        """
        return [self.vertex_point(vertex) for vertex in self.cell_vertices(cell)]

    def cell_centroid(self, cell: Cell) -> Point:
        """Compute the point at the centroid of a cell.

        Parameters
        ----------
        cell
            The identifier of the cell.

        Returns
        -------
        Point
            The coordinates of the centroid.

        See Also
        --------
        cell_center

        """
        vertices = self.cell_vertices(cell)
        return Point(*centroid_points([self.vertex_coordinates(vertex) for vertex in vertices]))

    def cell_center(self, cell: Cell) -> Point:
        """Compute the point at the center of mass of a cell.

        Parameters
        ----------
        cell
            The identifier of the cell.

        Returns
        -------
        Point
            The coordinates of the center of mass.

        See Also
        --------
        cell_centroid

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
    #     Vector
    #         The components of the normal vector.

    #     """
    #     cell_faces = self.cell_faces(cell)
    #     vectors = [self.face_normal(face) for face in self.vertex_halffaces(vertex) if face in cell_faces]
    #     return Vector(*normalize_vector(centroid_points(vectors)))

    def cell_polyhedron(self, cell: Cell) -> Polyhedron:
        """Construct a polyhedron from the vertices and faces of a cell.

        Parameters
        ----------
        cell
            The identifier of the cell.

        Returns
        -------
        Polyhedron
            The polyhedron.

        """
        vertices, faces = self.cell_to_vertices_and_faces(cell)
        return Polyhedron(vertices, faces)

    def cell_volume(self, cell: Cell) -> float:
        """Compute the volume of a cell.

        Parameters
        ----------
        cell
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
    #     faces_on_boundaries, cells_on_boundaries

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
    #     vertices_on_boundaries, cells_on_boundaries

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
    #     vertices_on_boundaries, faces_on_boundaries

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
    #     T : Transformation
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
