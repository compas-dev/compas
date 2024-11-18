from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from itertools import product
from math import pi
from random import sample

import compas

if compas.PY2:
    from collections import Mapping
else:
    from collections.abc import Mapping

from compas.datastructures.attributes import EdgeAttributeView
from compas.datastructures.attributes import FaceAttributeView
from compas.datastructures.attributes import VertexAttributeView
from compas.datastructures.datastructure import Datastructure
from compas.files import OBJ
from compas.files import OFF
from compas.files import PLY
from compas.files import STL
from compas.geometry import Box
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Point
from compas.geometry import Polygon
from compas.geometry import Polyhedron
from compas.geometry import Shape  # noqa: F401
from compas.geometry import Vector
from compas.geometry import add_vectors
from compas.geometry import angle_points
from compas.geometry import area_polygon
from compas.geometry import bestfit_plane
from compas.geometry import bounding_box
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import cross_vectors
from compas.geometry import distance_line_line
from compas.geometry import distance_point_plane
from compas.geometry import distance_point_point
from compas.geometry import length_vector
from compas.geometry import midpoint_line
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import oriented_bounding_box
from compas.geometry import scale_vector
from compas.geometry import subtract_vectors
from compas.geometry import sum_vectors
from compas.geometry import transform_points
from compas.geometry import vector_average
from compas.itertools import linspace
from compas.itertools import pairwise
from compas.itertools import window
from compas.tolerance import TOL
from compas.topology import breadth_first_traverse
from compas.topology import connected_components
from compas.topology import unify_cycles

from .duality import mesh_dual
from .operations.collapse import mesh_collapse_edge
from .operations.merge import mesh_merge_faces
from .operations.split import mesh_split_edge
from .operations.split import mesh_split_face
from .operations.split import mesh_split_strip
from .operations.weld import mesh_unweld_edges
from .operations.weld import mesh_unweld_vertices
from .slice import mesh_slice_plane
from .smoothing import mesh_smooth_area
from .smoothing import mesh_smooth_centroid
from .subdivision import mesh_subdivide


class Mesh(Datastructure):
    """Data structure for representing open or closed surface meshes.

    Parameters
    ----------
    default_vertex_attributes : dict[str, Any], optional
        Default values for vertex attributes.
    default_edge_attributes : dict[str, Any], optional
        Default values for edge attributes.
    default_face_attributes : dict[str, Any], optional
        Default values for face attributes.
    name : str, optional
        Then name of the mesh.
    **kwargs : dict, optional
        Additional keyword arguments, which are stored in the attributes dict.

    Attributes
    ----------
    default_vertex_attributes : dict[str, Any]
        Dictionary containing default values for the attributes of vertices.
        It is recommended to add a default to this dictionary using :meth:`update_default_vertex_attributes`
        for every vertex attribute used in the data structure.
    default_edge_attributes : dict[str, Any]
        Dictionary containing default values for the attributes of edges.
        It is recommended to add a default to this dictionary using :meth:`update_default_edge_attributes`
        for every edge attribute used in the data structure.
    default_face_attributes : dict[str, Any]
        Dictionary contnaining default values for the attributes of faces.
        It is recommended to add a default to this dictionary using :meth:`update_default_face_attributes`
        for every face attribute used in the data structure.

    Examples
    --------
    >>> from compas.datastructures import Mesh
    >>> mesh = Mesh.from_polyhedron(6)
    >>> V = mesh.number_of_vertices()
    >>> E = mesh.number_of_edges()
    >>> F = mesh.number_of_faces()
    >>> mesh.euler() == V - E + F
    True

    """

    collapse_edge = mesh_collapse_edge
    merge_faces = mesh_merge_faces
    split_edge = mesh_split_edge
    split_face = mesh_split_face
    split_strip = mesh_split_strip
    subdivided = mesh_subdivide
    dual = mesh_dual
    slice = mesh_slice_plane
    unweld_vertices = mesh_unweld_vertices
    unweld_edges = mesh_unweld_edges
    smooth_centroid = mesh_smooth_centroid
    smooth_area = mesh_smooth_area

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "attributes": {"type": "object"},
            "default_vertex_attributes": {"type": "object"},
            "default_edge_attributes": {"type": "object"},
            "default_face_attributes": {"type": "object"},
            "vertex": {
                "type": "object",
                "patternProperties": {"^[0-9]+$": {"type": "object"}},
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
            "facedata": {
                "type": "object",
                "patternProperties": {"^[0-9]+$": {"type": "object"}},
                "additionalProperties": False,
            },
            "edgedata": {
                "type": "object",
                "patternProperties": {"^\\([0-9]+, [0-9]+\\)$": {"type": "object"}},
                "additionalProperties": False,
            },
            "max_vertex": {"type": "integer", "minimum": -1},
            "max_face": {"type": "integer", "minimum": -1},
        },
        "required": [
            "attributes",
            "default_vertex_attributes",
            "default_edge_attributes",
            "default_face_attributes",
            "vertex",
            "face",
            "facedata",
            "edgedata",
            "max_vertex",
            "max_face",
        ],
    }

    @property
    def __data__(self):
        return self.__before_json_dump__(
            {
                "attributes": self.attributes,
                "default_vertex_attributes": self.default_vertex_attributes,
                "default_edge_attributes": self.default_edge_attributes,
                "default_face_attributes": self.default_face_attributes,
                "vertex": self.vertex,
                "face": self.face,
                "facedata": self.facedata,
                "edgedata": self.edgedata,
                "max_vertex": self._max_vertex,
                "max_face": self._max_face,
            }
        )

    def __before_json_dump__(self, data):
        data["vertex"] = {str(vertex): attr for vertex, attr in data["vertex"].items()}
        data["face"] = {str(face): vertices for face, vertices in data["face"].items()}
        data["facedata"] = {str(face): attr for face, attr in data["facedata"].items()}
        return data

    @classmethod
    def __from_data__(cls, data):
        mesh = cls(
            default_vertex_attributes=data.get("default_vertex_attributes"),
            default_face_attributes=data.get("default_face_attributes"),
            default_edge_attributes=data.get("default_edge_attributes"),
        )
        mesh.attributes.update(data.get("attributes") or {})

        vertex = data["vertex"] or {}
        face = data["face"] or {}
        facedata = data.get("facedata") or {}
        edgedata = data.get("edgedata") or {}

        for key, attr in iter(vertex.items()):
            mesh.add_vertex(key=key, attr_dict=attr)

        for fkey, vertices in iter(face.items()):
            mesh.add_face(vertices, fkey=fkey, attr_dict=facedata.get(fkey))

        mesh.edgedata = edgedata
        mesh._max_vertex = data.get("max_vertex", mesh._max_vertex)
        mesh._max_face = data.get("max_face", mesh._max_face)

        return mesh

    def __init__(self, default_vertex_attributes=None, default_edge_attributes=None, default_face_attributes=None, name=None, **kwargs):  # fmt: skip
        super(Mesh, self).__init__(kwargs, name=name)
        self._max_vertex = -1
        self._max_face = -1
        self.vertex = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self.edgedata = {}
        self.default_vertex_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.default_edge_attributes = {}
        self.default_face_attributes = {}
        if default_vertex_attributes:
            self.default_vertex_attributes.update(default_vertex_attributes)
        if default_edge_attributes:
            self.default_edge_attributes.update(default_edge_attributes)
        if default_face_attributes:
            self.default_face_attributes.update(default_face_attributes)

    def __str__(self):
        tpl = "<Mesh with {} vertices, {} faces, {} edges>"
        return tpl.format(self.number_of_vertices(), self.number_of_faces(), self.number_of_edges())

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def adjacency(self):
        return self.halfedge

    # --------------------------------------------------------------------------
    # Constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_obj(cls, filepath, precision=None):  # type: (...) -> Mesh
        """Construct a mesh object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        Notes
        -----
        There are a few sample files available for testing and debugging:

        * faces.obj
        * faces_big.obj
        * faces_reversed.obj
        * hypar.obj
        * mesh.obj
        * quadmesh.obj

        """
        obj = OBJ(filepath, precision)
        obj.read()
        vertices = obj.vertices
        faces = obj.faces
        edges = obj.lines
        if not vertices:
            return cls()
        if faces:
            return cls.from_vertices_and_faces(vertices, faces)
        if edges:
            lines = [(vertices[u], vertices[v], 0) for u, v in edges]
            return cls.from_lines(lines)
        return cls()

    @classmethod
    def from_ply(cls, filepath, precision=None):  # type: (...) -> Mesh
        """Construct a mesh object from the data described in a PLY file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        ply = PLY(filepath)
        vertices = ply.parser.vertices  # type: ignore
        faces = ply.parser.faces  # type: ignore
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    @classmethod
    def from_stl(cls, filepath, precision=None):  # type: (...) -> Mesh
        """Construct a mesh object from the data described in a STL file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        stl = STL(filepath, precision)
        vertices = stl.parser.vertices  # type: ignore
        faces = stl.parser.faces  # type: ignore
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    @classmethod
    def from_off(cls, filepath):  # type: (...) -> Mesh
        """Construct a mesh object from the data described in a OFF file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        off = OFF(filepath)
        vertices = off.reader.vertices  # type: ignore
        faces = off.reader.faces  # type: ignore
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    @classmethod
    def from_lines(cls, lines, delete_boundary_face=False, precision=None):  # type: (...) -> Mesh
        """Construct a mesh object from a list of lines described by start and end point coordinates.

        Parameters
        ----------
        lines : list[tuple[list[float], list[float]]]
            A list of pairs of point coordinates.
        delete_boundary_face : bool, optional
            The algorithm that finds the faces formed by the connected lines
            first finds the face *on the outside*. In most cases this face is not expected
            to be there. Therefore, there is the option to have it automatically deleted.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.
            Defaults to the value of :attr:`compas.PRECISION`.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        from compas.datastructures import Graph

        graph = Graph.from_lines(lines, precision=precision)
        vertices = graph.to_points()
        faces = graph.find_cycles()
        mesh = cls.from_vertices_and_faces(vertices, faces)
        if delete_boundary_face:
            mesh.delete_face(0)
            mesh.cull_vertices()
        return mesh

    @classmethod
    def from_polylines(cls, boundary_polylines, other_polylines):  # type: (...) -> Mesh
        """Construct mesh from polylines.

        Based on construction from_lines,
        with removal of vertices that are not polyline extremities
        and of faces that represent boundaries.

        This specific method is useful to get the mesh connectivity from a set of (discretised) curves,
        that could overlap and yield a wrong connectivity if using from_lines based on the polyline extremities only.

        Parameters
        ----------
        boundary_polylines : list[list[float]]
            List of polylines representing boundaries as lists of vertex coordinates.
        other_polylines : list[list[float]]
            List of the other polylines as lists of vertex coordinates.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        corners = []
        for polyline in boundary_polylines + other_polylines:
            corners.append(TOL.geometric_key(polyline[0]))
            corners.append(TOL.geometric_key(polyline[-1]))

        boundary = []
        for polyline in boundary_polylines:
            for xyz in polyline:
                boundary.append(TOL.geometric_key(xyz))

        lines = []
        for polyline in boundary_polylines + other_polylines:
            for u, v in pairwise(polyline):
                lines.append((u, v))

        mesh = cls.from_lines(lines)

        # remove the vertices that are not from the polyline extremities
        # and the faces with all their vertices on the boundary

        internal = []
        for vertex in mesh.vertices():
            if TOL.geometric_key(mesh.vertex_coordinates(vertex)) in corners:
                internal.append(vertex)

        vertices = [mesh.vertex_coordinates(vertex) for vertex in internal]
        vertex_index = {vertex: index for index, vertex in enumerate(internal)}

        faces = []
        for face in mesh.faces():
            notonboundary = []
            for vertex in mesh.face_vertices(face):
                gkey = TOL.geometric_key(mesh.vertex_coordinates(vertex))
                if gkey not in boundary:
                    notonboundary.append(vertex)

            if len(notonboundary):
                indices = []
                for vertex in mesh.face_vertices(face):
                    gkey = TOL.geometric_key(mesh.vertex_coordinates(vertex))
                    if gkey in corners:
                        indices.append(vertex_index[vertex])
                faces.append(indices)

        return cls.from_vertices_and_faces(vertices, faces)

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces):  # type: (...) -> Mesh
        """Construct a mesh object from a list of vertices and faces.

        Parameters
        ----------
        vertices : list[list[float]] | dict[int, list[float]]
            A list of vertices, represented by their XYZ coordinates,
            or a dictionary of vertex keys pointing to their XYZ coordinates.
        faces : list[list[int]] | dict[int, list[int]]
            A list of faces, represented by a list of indices referencing the list of vertex coordinates,
            or a dictionary of face keys pointing to a list of indices referencing the list of vertex coordinates.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        mesh = cls()

        if isinstance(vertices, Mapping):
            for key, xyz in vertices.items():
                mesh.add_vertex(key=key, attr_dict=dict(zip(("x", "y", "z"), xyz)))
        else:
            for x, y, z in iter(vertices):
                mesh.add_vertex(x=x, y=y, z=z)

        if isinstance(faces, Mapping):
            for fkey, vertices in faces.items():
                mesh.add_face(vertices, fkey)
        else:
            for face in iter(faces):
                mesh.add_face(face)

        return mesh

    @classmethod
    def from_polyhedron(cls, f):  # type: (...) -> Mesh
        """Construct a mesh from a platonic solid.

        Parameters
        ----------
        f : {4, 6, 8, 12, 20}
            The number of faces.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        p = Polyhedron.from_platonicsolid(f)
        return cls.from_vertices_and_faces(p.vertices, p.faces)

    @classmethod
    def from_shape(cls, shape, **kwargs):  # type: (Shape, dict) -> Mesh
        """Construct a mesh from a primitive shape.

        Parameters
        ----------
        shape : :class:`compas.geometry.Shape`
            The input shape to generate a mesh from.
        **kwargs : dict[str, Any], optional
            Optional keyword arguments to be passed on to :meth:`compas.geometry.Shape.to_vertices_and_faces`.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        vertices, faces = shape.to_vertices_and_faces(**kwargs)
        mesh = cls.from_vertices_and_faces(vertices, faces)
        mesh.name = shape.name
        return mesh

    @classmethod
    def from_points(cls, points):  # type: (...) -> Mesh
        """Construct a mesh from a delaunay triangulation of a set of points.

        Parameters
        ----------
        points : list[list[float]]
            XYZ coordinates of the points.
            Z coordinates should be zero.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        from compas.geometry import delaunay_triangulation

        vertices, faces = delaunay_triangulation(points)
        return cls.from_vertices_and_faces(vertices, faces)

    @classmethod
    def from_polygons(cls, polygons, precision=None):  # type: (...) -> Mesh
        """Construct a mesh from a series of polygons.

        Parameters
        ----------
        polygons : list[list[float]]
            A list of polygons, with each polygon defined as an ordered list of
            XYZ coordinates of its corners.
        precision : int, optional
            Precision for converting numbers to strings.
            Default is :attr:`TOL.precision`.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        faces = []
        gkey_xyz = {}
        for points in polygons:
            face = []
            for xyz in points:
                gkey = TOL.geometric_key(xyz, precision=precision)
                gkey_xyz[gkey] = xyz
                face.append(gkey)
            faces.append(face)
        gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}
        vertices = gkey_xyz.values()
        faces[:] = [[gkey_index[gkey] for gkey in face] for face in faces]
        return cls.from_vertices_and_faces(vertices, faces)

    @classmethod
    def from_meshgrid(cls, dx, nx, dy=None, ny=None):  # type: (...) -> Mesh
        """Construct a mesh from faces and vertices on a regular grid.

        Parameters
        ----------
        dx : float
            The size of the grid in the X direction.
        nx : int
            The number of faces in the X direction.
        dy : float, optional
            The size of the grid in the Y direction.
            Defaults to the value of `dx`.
        ny : int, optional
            The number of faces in the Y direction.
            Defaults to the value of `nx`.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            A mesh object.

        """
        dy = dy or dx
        ny = ny or nx

        vertices = [[x, y, 0.0] for x, y in product(linspace(0, dx, nx + 1), linspace(0, dy, ny + 1))]
        faces = []
        for i, j in product(range(nx), range(ny)):
            faces.append(
                [
                    i * (ny + 1) + j,
                    (i + 1) * (ny + 1) + j,
                    (i + 1) * (ny + 1) + j + 1,
                    i * (ny + 1) + j + 1,
                ]
            )

        return cls.from_vertices_and_faces(vertices, faces)

    # --------------------------------------------------------------------------
    # Conversions
    # --------------------------------------------------------------------------

    def to_lines(self):
        """Return the lines of the mesh as pairs of start and end point coordinates.

        Returns
        -------
        list[tuple[list[float], list[float]]]
            A list of lines each defined by a pair of point coordinates.

        """
        return [self.edge_coordinates(edge) for edge in self.edges()]

    def to_polylines(self):
        """Convert the mesh to a collection of polylines.

        Returns
        -------
        list[list[list[float]]]
            A list of polylines which are each defined as a list of points.

        """
        raise NotImplementedError

    def to_vertices_and_faces(self, triangulated=False):
        """Return the vertices and faces of a mesh.

        Parameters
        ----------
        triangulated: bool, optional
            If True, triangulate the faces.

        Returns
        -------
        list[list[float]]
            The vertices as a list of XYZ coordinates.
        list[list[int]]
            The faces as a list of lists of vertex indices.

        """
        vertex_index = self.vertex_index()
        vertices = [self.vertex_coordinates(vertex) for vertex in self.vertices()]

        if not triangulated:
            faces = [[vertex_index[vertex] for vertex in self.face_vertices(face)] for face in self.faces()]
            return vertices, faces

        faces = []

        for fkey in self.faces():
            face_vertices = self.face_vertices(fkey)

            if len(face_vertices) == 3:
                a, b, c = face_vertices
                faces.append([vertex_index[a], vertex_index[b], vertex_index[c]])
            elif len(face_vertices) == 4:
                a, b, c, d = face_vertices
                faces.append([vertex_index[a], vertex_index[b], vertex_index[c]])
                faces.append([vertex_index[a], vertex_index[c], vertex_index[d]])
            else:
                centroid = centroid_polygon([vertices[vertex_index[vertex]] for vertex in face_vertices])
                c = len(vertices)
                vertices.append(centroid)

                for a, b in pairwise(face_vertices + face_vertices[:1]):
                    faces.append([vertex_index[a], vertex_index[b], c])

        return vertices, faces

    def to_points(self):
        """Convert the mesh to a collection of points.

        Returns
        -------
        list[list[float]]
            The points representing the vertices of the mesh.

        """
        raise NotImplementedError

    def to_polygons(self):
        """Convert the mesh to a collection of polygons.

        Returns
        -------
        list[list[list[float]]]
            A list of polygons defined each as a list of points.

        """
        return [self.face_coordinates(fkey) for fkey in self.faces()]

    def to_obj(self, filepath, precision=None, unweld=False, **kwargs):
        """Write the mesh to an OBJ file.

        Parameters
        ----------
        filepath : str
            Full path of the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.
        unweld : bool, optional
            If True, all faces have their own unique vertices.
            If False (default), vertices are shared between faces if this is also the case in the mesh.

        Returns
        -------
        None

        Warnings
        --------
        This function only writes geometric data about the vertices and
        the faces to the file.

        """
        obj = OBJ(filepath, precision=precision)
        obj.write(self, unweld=unweld, **kwargs)

    def to_ply(self, filepath, **kwargs):
        """Write a mesh object to a PLY file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        None

        """
        ply = PLY(filepath)
        ply.write(self, **kwargs)

    def to_stl(self, filepath, precision=None, binary=False, **kwargs):
        """Write a mesh to an STL file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision : str, optional
            Rounding precision for the vertex coordinates.
            Defaults to the value of :attr:`compas.PRECISION`.
        binary : bool, optional
            If True, the file will be written in binary format.
            ASCII otherwise.

        Returns
        -------
        None

        Notes
        -----
        STL files only support triangle faces.
        It is the user's responsibility to convert all faces of a mesh to triangles.
        For example, with :meth:`compas.datastructures.Mesh.quads_to_triangles`.

        """
        stl = STL(filepath, precision)
        stl.write(self, binary=binary, **kwargs)

    def to_off(self, filepath, **kwargs):
        """Write a mesh object to an OFF file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        None

        """
        off = OFF(filepath)
        off.write(self, **kwargs)

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    def clear(self):
        """Clear all the mesh data.

        Returns
        -------
        None

        """
        del self.vertex
        del self.edgedata
        del self.halfedge
        del self.face
        del self.facedata
        self.vertex = {}
        self.edgedata = {}
        self.halfedge = {}
        self.face = {}
        self.facedata = {}
        self._max_vertex = -1
        self._max_face = -1

    def vertex_sample(self, size=1):
        """A random sample of the vertices.

        Parameters
        ----------
        size : int, optional
            The number of vertices in the random sample.

        Returns
        -------
        list[int]
            The identifiers of the vertices.

        See Also
        --------
        :meth:`edge_sample`, :meth:`face_sample`

        """
        return sample(list(self.vertices()), size)

    def edge_sample(self, size=1):
        """A random sample of the edges.

        Parameters
        ----------
        size : int, optional
            The number of edges in the random sample.

        Returns
        -------
        list[tuple[int, int]]
            The identifiers of the edges.

        See Also
        --------
        :meth:`vertex_sample`, :meth:`face_sample`

        """
        return sample(list(self.edges()), size)

    def face_sample(self, size=1):
        """A random sample of the faces.

        Parameters
        ----------
        size : int, optional
            The number of faces in the random sample.

        Returns
        -------
        list[int]
            The identifiers of the faces.

        See Also
        --------
        :meth:`vertex_sample`, :meth:`edge_sample`

        """
        return sample(list(self.faces()), size)

    def vertex_index(self):
        """Returns a dictionary that maps vertex identifiers to the
        corresponding index in a vertex list or array.

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
        """Returns a dictionary that maps the indices of a vertex list to
        the corresponding vertex identifiers.

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
            A dictionary of key-geometric key pairs.

        """
        gkey = TOL.geometric_key
        xyz = self.vertex_coordinates
        return {key: gkey(xyz(key), precision) for key in self.vertices()}

    def gkey_vertex(self, precision=None):
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
            A dictionary of geometric key-key pairs.

        """
        gkey = TOL.geometric_key
        xyz = self.vertex_coordinates
        return {gkey(xyz(key), precision): key for key in self.vertices()}

    # --------------------------------------------------------------------------
    # Builders & Modifiers
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        """Add a vertex to the mesh object.

        Parameters
        ----------
        key : int, optional
            The vertex identifier.
        attr_dict : dict[str, Any], optional
            A dictionary of vertex attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        Returns
        -------
        int
            The identifier of the vertex.

        See Also
        --------
        :meth:`add_face`
        :meth:`delete_vertex`, :meth:`delete_face`

        Notes
        -----
        If no key is provided for the vertex, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh()
        >>> mesh.add_vertex()
        0
        >>> mesh.add_vertex(x=0, y=0, z=0)
        1
        >>> mesh.add_vertex(key=2)
        2
        >>> mesh.add_vertex(key=0, x=1)
        0

        """
        if key is None:
            key = self._max_vertex = self._max_vertex + 1
        key = int(key)
        if key > self._max_vertex:
            self._max_vertex = key
        if key not in self.vertex:
            self.vertex[key] = {}
            self.halfedge[key] = {}
        attr = attr_dict or {}
        attr.update(kwattr)
        self.vertex[key].update(attr)
        return key

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        """Add a face to the mesh object.

        Parameters
        ----------
        vertices : list[int]
            A list of vertex keys.
        attr_dict : dict[str, Any], optional
            A dictionary of face attributes.
        **kwattr : dict[str, Any], optional
            A dictionary of additional attributes compiled of remaining named arguments.

        See Also
        --------
        :meth:`add_vertex`
        :meth:`delete_face`, :meth:`delete_vertex`

        Returns
        -------
        int
            The key of the face.

        Raises
        ------
        TypeError
            If the provided face key is of an unhashable type.

        Notes
        -----
        If no key is provided for the face, one is generated
        automatically. An automatically generated key is an integer that increments
        the highest integer value of any key used so far by 1.

        If a key with an integer value is provided that is higher than the current
        highest integer key value, then the highest integer value is updated accordingly.

        """
        if vertices[-1] == vertices[0]:
            vertices = vertices[:-1]
        vertices = [int(key) for key in vertices]
        vertices[:] = [u for u, v in pairwise(vertices + vertices[:1]) if u != v]
        if len(vertices) < 3:
            return
        if fkey is None:
            fkey = self._max_face = self._max_face + 1
        fkey = int(fkey)
        if fkey > self._max_face:
            self._max_face = fkey
        attr = attr_dict or {}
        attr.update(kwattr)
        self.face[fkey] = vertices
        self.facedata.setdefault(fkey, attr)
        for u, v in pairwise(vertices + vertices[:1]):
            self.halfedge[u][v] = fkey
            if u not in self.halfedge[v]:
                self.halfedge[v][u] = None
        return fkey

    # rename this to "add"
    # and add an alias
    def join(self, other, weld=False, precision=None):
        """Add the vertices and faces of another mesh to the current mesh.

        Parameters
        ----------
        other : :class:`compas.datastructures.Mesh`
            The other mesh.
        weld : bool, optional
            If True, weld close vertices after joining.
            Default is False.
        precision : int, optional
            The precision used for welding.
            Default is :attr:`TOL.precision`.

        Returns
        -------
        None
            The mesh is modified in place.

        Examples
        --------
        >>> from compas.geometry import Box
        >>> from compas.geometry import Translation
        >>> from compas.datastructures import Mesh
        >>> a = Box.from_width_height_depth(1, 1, 1)
        >>> b = Box.from_width_height_depth(1, 1, 1)
        >>> T = Translation.from_vector([2, 0, 0])
        >>> b.transform(T)
        >>> a = Mesh.from_shape(a)
        >>> b = Mesh.from_shape(b)
        >>> a.number_of_vertices()
        8
        >>> a.number_of_faces()
        6
        >>> b.number_of_vertices()
        8
        >>> b.number_of_faces()
        6
        >>> a.join(b)
        >>> a.number_of_vertices()
        16
        >>> a.number_of_faces()
        12

        """
        self.default_vertex_attributes.update(other.default_vertex_attributes)
        self.default_edge_attributes.update(other.default_edge_attributes)
        self.default_face_attributes.update(other.default_face_attributes)

        vertex_old_new = {}

        for vertex, attr in other.vertices(True):
            key = self.add_vertex(attr_dict=attr)
            vertex_old_new[vertex] = key

        for face, attr in other.faces(True):
            vertices = [vertex_old_new[key] for key in other.face_vertices(face)]
            self.add_face(vertices, attr_dict=attr)

        if weld:
            self.weld(precision=precision)

    def delete_vertex(self, key):
        """Delete a vertex from the mesh and everything that is attached to it.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        None

        See Also
        --------
        :meth:`delete_face`
        :meth:`add_vertex`, :meth:`add_face`

        Notes
        -----
        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

        """
        nbrs = self.vertex_neighbors(key)
        for nbr in nbrs:
            fkey = self.halfedge[key][nbr]
            if fkey is None:
                continue
            for u, v in self.face_halfedges(fkey):
                self.halfedge[u][v] = None
            del self.face[fkey]
            if fkey in self.facedata:
                del self.facedata[fkey]
        for nbr in nbrs:
            del self.halfedge[nbr][key]
            edge = "-".join(map(str, sorted([nbr, key])))
            if edge in self.edgedata:
                del self.edgedata[edge]
        for nbr in nbrs:
            for n in self.vertex_neighbors(nbr):
                if self.halfedge[nbr][n] is None and self.halfedge[n][nbr] is None:
                    del self.halfedge[nbr][n]
                    del self.halfedge[n][nbr]
                    edge = "-".join(map(str, sorted([nbr, n])))
                    if edge in self.edgedata:
                        del self.edgedata[edge]
        del self.halfedge[key]
        del self.vertex[key]

    def delete_face(self, fkey):
        """Delete a face from the mesh object.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        None

        See Also
        --------
        :meth:`delete_vertex`
        :meth:`add_vertex`, :meth:`add_face`

        Notes
        -----
        In some cases, disconnected vertices can remain after application of this
        method. To remove these vertices as well, combine this method with vertex
        culling (:meth:`cull_vertices`).

        """
        for u, v in self.face_halfedges(fkey):
            if self.halfedge[u][v] == fkey:
                # if the halfedge still points to the face
                # this might not be the case of the deletion is executed
                # during the procedure of adding a new (replacement) face
                self.halfedge[u][v] = None
                if self.halfedge[v][u] is None:
                    del self.halfedge[u][v]
                    del self.halfedge[v][u]
                    edge = "-".join(map(str, sorted([u, v])))
                    if edge in self.edgedata:
                        del self.edgedata[edge]
        del self.face[fkey]
        if fkey in self.facedata:
            del self.facedata[fkey]

    def remove_unused_vertices(self):
        """Remove all unused vertices from the mesh object.

        Returns
        -------
        None

        See Also
        --------
        :meth:`delete_vertex`

        """
        for u in list(self.vertices()):
            if u not in self.halfedge:
                del self.vertex[u]
            else:
                if not self.halfedge[u]:
                    del self.vertex[u]
                    del self.halfedge[u]

    cull_vertices = remove_unused_vertices

    def flip_cycles(self):
        """Flip the cycle directions of all faces.

        Returns
        -------
        None
            The mesh is modified in place.

        Notes
        -----
        This function does not care about the directions being unified or not. It
        just reverses whatever direction it finds.

        """
        self.halfedge = {key: {} for key in self.vertices()}
        for fkey in self.faces():
            self.face[fkey][:] = self.face[fkey][::-1]
            for u, v in self.face_halfedges(fkey):
                self.halfedge[u][v] = fkey
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None

    def insert_vertex(self, fkey, key=None, xyz=None, return_fkeys=False):
        """Insert a vertex in the specified face.

        Parameters
        ----------
        fkey : int
            The key of the face in which the vertex should be inserted.
        key : int, optional
            The key to be used to identify the inserted vertex.
        xyz : list[float], optional
            Specific XYZ coordinates for the inserted vertex.
        return_fkeys : bool, optional
            If True, return the identifiers of the newly created faces in addition to the identifier of the inserted vertex.

        Returns
        -------
        int | tuple[int, list[int]]
            If `return_fkeys` is False, the key of the inserted vertex.
            If `return_fkeys` is True, the key of the newly created vertex and a list with the newly created faces.

        """
        fkeys = []
        if not xyz:
            x, y, z = self.face_center(fkey)
        else:
            x, y, z = xyz
        w = self.add_vertex(key=key, x=x, y=y, z=z)
        for u, v in self.face_halfedges(fkey):
            fkeys.append(self.add_face([u, v, w]))
        self.delete_face(fkey)
        if return_fkeys:
            return w, fkeys
        return w

    # --------------------------------------------------------------------------
    # Accessors
    # --------------------------------------------------------------------------

    def vertices(self, data=False):
        """Iterate over the vertices of the mesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex identifier.
            If `data` is True, the next vertex as a (key, attr) tuple.

        See Also
        --------
        :meth:`faces`, :meth:`edges`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for key in self.vertex:
            if not data:
                yield key
            else:
                yield key, self.vertex_attributes(key)

    def faces(self, data=False):
        """Iterate over the faces of the mesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face identifier.
            If `data` is True, the next face as a (fkey, attr) tuple.

        See Also
        --------
        :meth:`vertices`, :meth:`edges`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for key in self.face:
            if not data:
                yield key
            else:
                yield key, self.face_attributes(key)

    def edges(self, data=False):
        """Iterate over the edges of the mesh.

        Parameters
        ----------
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a ((u, v), data) tuple.

        See Also
        --------
        :meth:`vertices`, :meth:`faces`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        Notes
        -----
        Mesh edges have no topological meaning. They are only used to store data.
        Edges are not automatically created when vertices and faces are added to
        the mesh. Instead, they are created when data is stored on them, or when
        they are accessed using this method.

        This method yields the directed edges of the mesh.
        Unless edges were added explicitly using :meth:`add_edge` the order of
        edges is *as they come out*. However, as long as the toplogy remains
        unchanged, the order is consistent.

        """
        seen = set()
        for u in self.halfedge:
            for v in self.halfedge[u]:
                key = u, v
                ikey = v, u
                if key in seen or ikey in seen:
                    continue
                seen.add(key)
                seen.add(ikey)
                if not data:
                    yield key
                else:
                    yield key, self.edge_attributes(key)

    def vertices_where(self, conditions=None, data=False, **kwargs):
        """Get vertices for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

        See Also
        --------
        :meth:`faces_where`, :meth:`edges_where`
        :meth:`vertices_where_predicate`, :meth:`edges_where_predicate`, :meth:`faces_where_predicate`

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
            The callable takes 2 parameters: the vertex identifier and the vertex attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the vertex attributes in addition to the vertex identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next vertex that matches the condition.
            If `data` is True, the next vertex and its attributes.

        See Also
        --------
        :meth:`faces_where_predicate`, :meth:`edges_where_predicate`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for key, attr in self.vertices(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    def edges_where(self, conditions=None, data=False, **kwargs):
        """Get edges for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the edge attributes in addition to the edge identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a (u, v, data) tuple.

        See Also
        --------
        :meth:`vertices_where`, :meth:`faces_where`
        :meth:`vertices_where_predicate`, :meth:`edges_where_predicate`, :meth:`faces_where_predicate`

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
            The callable takes 3 parameters:
            the identifier of the first vertex, the identifier of the second vertex, and the edge attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the vertex attributes in addition ot the vertex identifiers.

        Yields
        ------
        tuple[int, int] | tuple[tuple[int, int], dict[str, Any]]
            If `data` is False, the next edge as a (u, v) tuple.
            If `data` is True, the next edge as a (u, v, data) tuple.

        See Also
        --------
        :meth:`faces_where_predicate`, :meth:`vertices_where_predicate`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for key, attr in self.edges(True):
            if predicate(key, attr):
                if data:
                    yield key, attr
                else:
                    yield key

    def faces_where(self, conditions=None, data=False, **kwargs):
        """Get faces for which a certain condition or set of conditions is true.

        Parameters
        ----------
        conditions : dict, optional
            A set of conditions in the form of key-value pairs.
            The keys should be attribute names. The values can be attribute
            values or ranges of attribute values in the form of min/max pairs.
        data : bool, optional
            If True, yield the face attributes in addition to face identifiers.
        **kwargs : dict[str, Any], optional
            Additional conditions provided as named function arguments.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face that matches the condition.
            If `data` is True, the next face and its attributes.

        See Also
        --------
        :meth:`vertices_where`, :meth:`edges_where`
        :meth:`vertices_where_predicate`, :meth:`edges_where_predicate`, :meth:`faces_where_predicate`

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
            The callable takes 2 parameters: the face identifier and the face attributes,
            and should return True or False.
        data : bool, optional
            If True, yield the face attributes in addition to the face identifiers.

        Yields
        ------
        int | tuple[int, dict[str, Any]]
            If `data` is False, the next face that matches the condition.
            If `data` is True, the next face and its attributes.

        See Also
        --------
        :meth:`edges_where_predicate`, :meth:`vertices_where_predicate`
        :meth:`vertices_where`, :meth:`edges_where`, :meth:`faces_where`

        """
        for fkey, attr in self.faces(True):
            if predicate(fkey, attr):
                if data:
                    yield fkey, attr
                else:
                    yield fkey

    # --------------------------------------------------------------------------
    # Attributes
    # --------------------------------------------------------------------------

    def update_default_vertex_attributes(self, attr_dict=None, **kwattr):
        """Update the default vertex attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_edge_attributes`
        :meth:`update_default_face_attributes`

        Notes
        -----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_vertex_attributes.update(attr_dict)

    def vertex_attribute(self, key, name, value=None):
        """Get or set an attribute of a vertex.

        Parameters
        ----------
        key : int
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
        :meth:`vertex_attributes`, :meth:`vertices_attribute`, :meth:`vertices_attributes`
        :meth:`unset_vertex_attribute`
        :meth:`edge_attribute`
        :meth:`face_attribute`

        """
        if key not in self.vertex:
            raise KeyError(key)
        if value is not None:
            self.vertex[key][name] = value
            return None
        if name in self.vertex[key]:
            return self.vertex[key][name]
        else:
            if name in self.default_vertex_attributes:
                return self.default_vertex_attributes[name]

    def unset_vertex_attribute(self, key, name):
        """Unset the attribute of a vertex.

        Parameters
        ----------
        key : int
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
        :meth:`vertex_attribute`, :meth:`vertex_attributes`, :meth:`vertices_attribute`, :meth:`vertices_attributes`
        :meth:`unset_edge_attribute`
        :meth:`unset_face_attribute`

        Notes
        -----
        Unsetting the value of a vertex attribute implicitly sets it back to the value
        stored in the default vertex attribute dict.

        """
        if name in self.vertex[key]:
            del self.vertex[key][name]

    def vertex_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a vertex.

        Parameters
        ----------
        key : int
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
        :meth:`edge_attributes`
        :meth:`face_attributes`

        """
        if key not in self.vertex:
            raise KeyError(key)
        if names and values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                self.vertex[key][name] = value
            return
        # use it as a getter
        if not names:
            # return all vertex attributes as a dict
            return VertexAttributeView(self.default_vertex_attributes, self.vertex[key])
        values = []
        for name in names:
            if name in self.vertex[key]:
                values.append(self.vertex[key][name])
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
        :meth:`edges_attribute`
        :meth:`faces_attribute`

        """
        if not keys:
            keys = self.vertices()
        if value is not None:
            for key in keys:
                self.vertex_attribute(key, name, value)
            return
        return [self.vertex_attribute(key, name) for key in keys]

    def vertices_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple vertices.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
        values : list[Any], optional
            The values of the attributes.
        keys : list[int], optional
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
        :meth:`edges_attributes`
        :meth:`faces_attributes`

        """
        if not keys:
            keys = self.vertices()
        if values is not None:
            for key in keys:
                self.vertex_attributes(key, names, values)
            return
        return [self.vertex_attributes(key, names) for key in keys]

    def update_default_face_attributes(self, attr_dict=None, **kwattr):
        """Update the default face attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_vertex_attributes`
        :meth:`update_default_edge_attributes`

        Notes
        -----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

        """
        if not attr_dict:
            attr_dict = {}
        attr_dict.update(kwattr)
        self.default_face_attributes.update(attr_dict)

    def face_attribute(self, key, name, value=None):
        """Get or set an attribute of a face.

        Parameters
        ----------
        key : int
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
        :meth:`face_attributes`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`unset_face_attribute`
        :meth:`edge_attribute`
        :meth:`vertex_attribute`

        """
        if key not in self.face:
            raise KeyError(key)
        if value is not None:
            if key not in self.facedata:
                self.facedata[key] = {}
            self.facedata[key][name] = value
            return
        if key in self.facedata and name in self.facedata[key]:
            return self.facedata[key][name]
        if name in self.default_face_attributes:
            return self.default_face_attributes[name]

    def unset_face_attribute(self, key, name):
        """Unset the attribute of a face.

        Parameters
        ----------
        key : int
            The face identifier.
        name : str
            The name of the attribute.

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`face_attributes`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`unset_edge_attribute`
        :meth:`unset_vertex_attribute`

        Notes
        -----
        Unsetting the value of a face attribute implicitly sets it back to the value
        stored in the default face attribute dict.

        """
        if key not in self.face:
            raise KeyError(key)
        if key in self.facedata:
            if name in self.facedata[key]:
                del self.facedata[key][name]

    def face_attributes(self, key, names=None, values=None):
        """Get or set multiple attributes of a face.

        Parameters
        ----------
        key : int
            The identifier of the face.
        names : list[str], optional
            A list of attribute names.
        values : list[Any], optional
            A list of attribute values.

        Returns
        -------
        dict[str, Any] | list[Any] | None
            If the parameter `names` is empty,
            a dictionary of all attribute name-value pairs of the face.
            If the parameter `names` is not empty,
            a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the face does not exist.

        See Also
        --------
        :meth:`face_attribute`, :meth:`faces_attribute`, :meth:`faces_attributes`
        :meth:`edge_attributes`
        :meth:`vertex_attributes`

        """
        if key not in self.face:
            raise KeyError(key)
        if names and values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                if key not in self.facedata:
                    self.facedata[key] = {}
                self.facedata[key][name] = value
            return
        # use it as a getter
        if not names:
            return FaceAttributeView(self.default_face_attributes, self.facedata.setdefault(key, {}))
        values = []
        for name in names:
            value = self.face_attribute(key, name)
            values.append(value)
        return values

    def faces_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple faces.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[int], optional
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
        :meth:`edges_attribute`
        :meth:`vertices_attribute`

        """
        if not keys:
            keys = self.faces()
        if value is not None:
            for key in keys:
                self.face_attribute(key, name, value)
            return
        return [self.face_attribute(key, name) for key in keys]

    def faces_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple faces.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        keys : list[int], optional
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
        :meth:`edges_attributes`
        :meth:`vertices_attributes`

        """
        if not keys:
            keys = self.faces()
        if values is not None:
            for key in keys:
                self.face_attributes(key, names, values)
            return
        return [self.face_attributes(key, names) for key in keys]

    def update_default_edge_attributes(self, attr_dict=None, **kwattr):
        """Update the default edge attributes.

        Parameters
        ----------
        attr_dict : dict[str, Any], optional
            A dictionary of attributes with their default values.
        **kwattr : dict[str, Any], optional
            A dictionary compiled of remaining named arguments.

        Returns
        -------
        None

        See Also
        --------
        :meth:`update_default_vertex_attributes`
        :meth:`update_default_face_attributes`

        Notes
        -----
        Named arguments overwrite corresponding key-value pairs in the attribute dictionary.

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
            The identifier of the edge as a pair of vertex identifiers.
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.

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
        :meth:`edge_attributes`, :meth:`edges_attribute`, :meth:`edges_attributes`
        :meth:`unset_edge_attribute`
        :meth:`vertex_attribute`
        :meth:`face_attribute`

        """
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if value is not None:
            if key not in self.edgedata:
                self.edgedata[key] = {}
            self.edgedata[key][name] = value
            return
        if key in self.edgedata and name in self.edgedata[key]:
            return self.edgedata[key][name]
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

        Returns
        -------
        None

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edge_attributes`, :meth:`edges_attribute`, :meth:`edges_attributes`
        :meth:`unset_vertex_attribute`
        :meth:`unset_face_attribute`

        Notes
        -----
        Unsetting the value of an edge attribute implicitly sets it back to the value
        stored in the default edge attribute dict.

        """
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        key = str(tuple(sorted(edge)))
        if key in self.edgedata and name in self.edgedata[key]:
            del self.edgedata[key][name]

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
            If the parameter `names` is empty,
            a dictionary of all attribute name-value pairs of the edge.
            If the parameter `names` is not empty,
            a list of the values corresponding to the provided names.
            None if the function is used as a "setter".

        Raises
        ------
        KeyError
            If the edge does not exist.

        See Also
        --------
        :meth:`edge_attribute`, :meth:`edges_attribute`, :meth:`edges_attributes`
        :meth:`vertex_attributes`
        :meth:`face_attributes`

        """
        u, v = edge
        if u not in self.halfedge or v not in self.halfedge[u]:
            raise KeyError(edge)
        if names and values is not None:
            # use it as a setter
            for name, value in zip(names, values):
                self.edge_attribute(edge, name, value)
            return
        # use it as a getter
        if not names:
            key = str(tuple(sorted(edge)))
            # get the entire attribute dict
            return EdgeAttributeView(self.default_edge_attributes, self.edgedata.setdefault(key, {}))
        # get only the values of the named attributes
        values = []
        for name in names:
            value = self.edge_attribute(edge, name)
            values.append(value)
        return values

    def edges_attribute(self, name, value=None, keys=None):
        """Get or set an attribute of multiple edges.

        Parameters
        ----------
        name : str
            The name of the attribute.
        value : object, optional
            The value of the attribute.
            Default is None.
        keys : list[tuple[int, int]], optional
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
        :meth:`vertex_attributes`
        :meth:`face_attributes`

        """
        edges = keys or self.edges()
        if value is not None:
            for edge in edges:
                self.edge_attribute(edge, name, value)
            return
        return [self.edge_attribute(edge, name) for edge in edges]

    def edges_attributes(self, names=None, values=None, keys=None):
        """Get or set multiple attributes of multiple edges.

        Parameters
        ----------
        names : list[str], optional
            The names of the attribute.
            Default is None.
        values : list[Any], optional
            The values of the attributes.
            Default is None.
        keys : list[tuple[int, int]], optional
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
        :meth:`vertex_attributes`
        :meth:`face_attributes`

        """
        edges = keys or self.edges()
        if values is not None:
            for edge in edges:
                self.edge_attributes(edge, names, values)
            return
        return [self.edge_attributes(edge, names) for edge in edges]

    # --------------------------------------------------------------------------
    # Info
    # --------------------------------------------------------------------------

    def summary(self):
        """Print a summary of the mesh.

        Returns
        -------
        str
            The formatted summary text.

        """
        tpl = "\n".join(
            [
                "{} summary",
                "=" * (len(self.name) + len(" summary")),
                "- vertices: {}",
                "- edges: {}",
                "- faces: {}",
            ]
        )
        return tpl.format(
            self.name,
            self.number_of_vertices(),
            self.number_of_edges(),
            self.number_of_faces(),
        )

    def number_of_vertices(self):
        """Count the number of vertices in the mesh.

        Returns
        -------
        int

        See Also
        --------
        :meth:`number_of_edges`
        :meth:`number_of_faces`

        """
        return len(list(self.vertices()))

    def number_of_edges(self):
        """Count the number of edges in the mesh.

        Returns
        -------
        int

        See Also
        --------
        :meth:`number_of_vertices`
        :meth:`number_of_faces`

        """
        return len(list(self.edges()))

    def number_of_faces(self):
        """Count the number of faces in the mesh.

        Returns
        -------
        int

        See Also
        --------
        :meth:`number_of_vertices`
        :meth:`number_of_edges`

        """
        return len(list(self.faces()))

    def is_valid(self):
        """Verify that the mesh is valid.

        A mesh is valid if the following conditions are fulfilled:

        * halfedges don't point at non-existing faces
        * all vertices are in the halfedge dict
        * there are no None-None halfedges
        * all faces have corresponding halfedge entries

        Returns
        -------
        bool
            True, if the mesh is valid.
            False, otherwise.

        See Also
        --------
        :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        for key in self.vertices():
            if key not in self.halfedge:
                return False

        for u in self.halfedge:
            if u not in self.vertex:
                return False
            for v in self.halfedge[u]:
                if v not in self.vertex:
                    return False
                if self.halfedge[u][v] is None and self.halfedge[v][u] is None:
                    return False
                fkey = self.halfedge[u][v]
                if fkey is not None:
                    if fkey not in self.face:
                        return False

        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                if u not in self.vertex:
                    return False
                if v not in self.vertex:
                    return False
                if u not in self.halfedge:
                    return False
                if v not in self.halfedge[u]:
                    return False
                if fkey != self.halfedge[u][v]:
                    return False
        return True

    def is_regular(self):
        """Verify that the mesh is regular.

        A mesh is regular if the following conditions are fulfilled:

        * All faces have the same number of edges.
        * All vertices have the same degree, i.e. they are incident to the same number of edges.

        Returns
        -------
        bool
            True, if the mesh is regular.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if not self.vertex or not self.face:
            return False

        vkey = self.vertex_sample(size=1)[0]
        degree = self.vertex_degree(vkey)

        for vkey in self.vertices():
            if self.vertex_degree(vkey) != degree:
                return False

        fkey = self.face_sample(size=1)[0]
        vcount = len(self.face_vertices(fkey))

        for fkey in self.faces():
            vertices = self.face_vertices(fkey)
            if len(vertices) != vcount:
                return False

        return True

    def is_manifold(self):
        """Verify that the mesh is manifold.

        A mesh is manifold if the following conditions are fulfilled:

        * Each edge is incident to only one or two faces.
        * The faces incident to a vertex form a closed or an open fan.

        Returns
        -------
        bool
            True, if the mesh is manifold.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if not self.vertex:
            return False

        for key in self.vertices():
            if list(self.halfedge[key].values()).count(None) > 1:
                return False

            nbrs = self.vertex_neighbors(key, ordered=True)

            if not nbrs:
                return False

            if self.halfedge[nbrs[0]][key] is None:
                for nbr in nbrs[1:-1]:
                    if self.halfedge[key][nbr] is None:
                        return False

                if self.halfedge[key][nbrs[-1]] is not None:
                    return False
            else:
                for nbr in nbrs[1:]:
                    if self.halfedge[key][nbr] is None:
                        return False

        return True

    def is_orientable(self):
        """Verify that the mesh is orientable.

        A manifold mesh is orientable if any two adjacent faces have compatible orientation,
        i.e. the faces have a unified cycle direction.

        Returns
        -------
        bool
            True, if the mesh is orientable.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        raise NotImplementedError

    def is_trimesh(self):
        """Verify that the mesh consists of only triangles.

        Returns
        -------
        bool
            True, if the mesh is a triangle mesh.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_quadmesh`

        """
        if not self.face:
            return False
        return not any(3 != len(self.face_vertices(fkey)) for fkey in self.faces())

    def is_quadmesh(self):
        """Verify that the mesh consists of only quads.

        Returns
        -------
        bool
            True, if the mesh is a quad mesh.
            False, otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_closed`, :meth:`is_trimesh`

        """
        if not self.face:
            return False
        return not any(4 != len(self.face_vertices(fkey)) for fkey in self.faces())

    def is_empty(self):
        """Verify that the mesh is empty.

        Returns
        -------
        bool
            True if the mesh has no vertices.
            False otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_closed`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if self.number_of_vertices() == 0:
            return True
        return False

    def is_closed(self):
        """Verify that the mesh is closed.

        Returns
        -------
        bool
            True if the mesh is not empty and has no naked edges.
            False otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if self.is_empty():
            return False
        for edge in self.edges():
            if self.is_edge_on_boundary(edge):
                return False
        return True

    def is_connected(self):
        """Verify that the mesh is connected.

        Returns
        -------
        bool
            True if the mesh is not empty and has no naked edges.
            False otherwise.

        See Also
        --------
        :meth:`is_valid`, :meth:`is_regular`, :meth:`is_manifold`, :meth:`is_orientable`, :meth:`is_empty`, :meth:`is_trimesh`, :meth:`is_quadmesh`

        """
        if not self.vertex:
            return False
        nodes = breadth_first_traverse(self.adjacency, self.vertex_sample(size=1)[0])
        return len(nodes) == self.number_of_vertices()

    def euler(self):
        """Calculate the Euler characteristic.

        Returns
        -------
        int
            The Euler characteristic.

        See Also
        --------
        :meth:`genus`

        """
        V = len([vkey for vkey in self.vertices() if len(self.vertex_neighbors(vkey)) != 0])
        E = self.number_of_edges()
        F = self.number_of_faces()
        return V - E + F

    # --------------------------------------------------------------------------
    # Cleanup
    # --------------------------------------------------------------------------

    def weld(self, precision=None):
        """Weld vertices that are closer than a given precision.

        Parameters
        ----------
        precision : int, optional
            The precision of the geometric map that is used to connect the lines.
            Defaults to the value of :attr:`compas.PRECISION`.

        Returns
        -------
        None
            The mesh is modified in place.

        """
        self.remove_duplicate_vertices(precision=precision)

    def remove_duplicate_vertices(self, precision=None):
        """Remove all duplicate vertices and clean up any affected faces.

        Parameters
        ----------
        precision : int, optional
            Precision for converting numbers to strings.
            Default is :attr:`TOL.precision`.

        Returns
        -------
        None
            The mesh is modified in-place.

        Examples
        --------
        >>> import compas
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_obj(compas.get("faces.obj"))
        >>> mesh.number_of_vertices()
        36
        >>> for x, y, z in mesh.vertices_attributes("xyz", keys=list(mesh.vertices())[:5]):
        ...     mesh.add_vertex(x=x, y=y, z=z)
        36
        37
        38
        39
        40
        >>> mesh.number_of_vertices()
        41
        >>> mesh.remove_duplicate_vertices()
        >>> mesh.number_of_vertices()
        36

        """
        vertex_gkey = {}
        for vertex in self.vertices():
            gkey = TOL.geometric_key(self.vertex_coordinates(vertex), precision=precision)
            vertex_gkey[vertex] = gkey

        gkey_vertex = {gkey: vertex for vertex, gkey in iter(vertex_gkey.items())}

        for boundary in self.vertices_on_boundaries():
            for vertex in boundary:
                gkey = TOL.geometric_key(self.vertex_coordinates(vertex), precision=precision)
                gkey_vertex[gkey] = vertex

        for vertex in list(self.vertices()):
            test = gkey_vertex[vertex_gkey[vertex]]
            if test != vertex:
                del self.vertex[vertex]
                del self.halfedge[vertex]
                for u in self.halfedge:
                    nbrs = list(self.halfedge[u].keys())
                    for v in nbrs:
                        if v == vertex:
                            del self.halfedge[u][v]

        for face in self.faces():
            seen = set()
            vertices = []
            for vertex in [gkey_vertex[vertex_gkey[vertex]] for vertex in self.face_vertices(face)]:
                if vertex not in seen:
                    seen.add(vertex)
                    vertices.append(vertex)
            self.face[face] = vertices
            for u, v in self.face_halfedges(face):
                self.halfedge[u][v] = face
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None

    # only reason this is here is because of the potential angles check
    def quads_to_triangles(self, check_angles=False):
        """Convert all quadrilateral faces to triangles by adding a diagonal edge.

        Parameters
        ----------
        check_angles : bool, optional
            Flag indicating that the angles of the quads should be checked to choose the best diagonal.

        Returns
        -------
        None
            The mesh is modified in place.

        """
        for face in list(self.faces()):
            attr = self.face_attributes(face)
            vertices = self.face_vertices(face)
            if len(vertices) == 4:
                a, b, c, d = vertices
                t1, t2 = self.split_face(face, b, d)
                self.face_attributes(t1, names=attr.keys(), values=attr.values())  # type: ignore
                self.face_attributes(t2, names=attr.keys(), values=attr.values())  # type: ignore
                # self.facedata[t1] = attr.copy()
                # self.facedata[t2] = attr.copy()
                if face in self.facedata:
                    del self.facedata[face]

    # only reason this is here and not on the halfedge is because of the spatial tree
    def unify_cycles(self, root=None, nmax=None, max_distance=None):
        """Unify the cycles of the mesh.

        Parameters
        ----------
        root : int, optional
            The key of the root face.
        nmax : int, optional
            The maximum number of neighboring faces to consider. If neither nmax nor max_distance is specified, all faces will be considered.
        max_distance : float, optional
            The max_distance of the search sphere for neighboring faces. If neither nmax nor max_distance is specified, all faces will be considered.

        Returns
        -------
        None
            The mesh is modified in place.

        """
        vertex_index = {}
        index_vertex = {}
        for index, vertex in enumerate(self.vertices()):
            vertex_index[vertex] = index
            index_vertex[index] = vertex
        index_face = {index: face for index, face in enumerate(self.faces())}

        vertices = self.vertices_attributes("xyz")
        faces = [[vertex_index[vertex] for vertex in self.face_vertices(face)] for face in self.faces()]

        unify_cycles(vertices, faces, root=root, nmax=nmax, max_distance=max_distance)

        self.halfedge = {key: {} for key in self.vertices()}
        for index, vertices in enumerate(faces):
            face = index_face[index]
            vertices = [index_vertex[vertex] for vertex in vertices]
            self.face[face] = vertices
            for u, v in pairwise(vertices + vertices[:1]):
                self.halfedge[u][v] = face
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None

    # --------------------------------------------------------------------------
    # Components
    # --------------------------------------------------------------------------

    def connected_vertices(self):
        """Find groups of connected vertices.

        Returns
        -------
        list[list[int]]
            Groups of connected vertices.

        """
        return connected_components(self.adjacency)

    def connected_faces(self):
        """Find groups of connected faces.

        Returns
        -------
        list[list[int]]
            Groups of connected faces.

        """
        # return connected_components(self.face_adjacency)
        parts = self.connected_vertices()
        return [set([face for vertex in part for face in self.vertex_faces(vertex)]) for part in parts]

    # --------------------------------------------------------------------------
    # Vertex topology
    # --------------------------------------------------------------------------

    def has_vertex(self, key):
        """Verify that a vertex is in the mesh.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is in the mesh.
            False otherwise.

        """
        return key in self.vertex

    def is_vertex_connected(self, key):
        """Verify that a vertex is connected.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is connected to at least one other vertex.
            False otherwise.

        """
        return self.vertex_degree(key) > 0

    def is_vertex_on_boundary(self, key):
        """Verify that a vertex is on a boundary.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        bool
            True if the vertex is on the boundary.
            False otherwise.

        """
        for nbr in self.halfedge[key]:
            if self.halfedge[key][nbr] is None:
                return True
        return False

    def vertex_neighbors(self, key, ordered=False):
        """Return the neighbors of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        ordered : bool, optional
            If True, return the neighbors in the cycling order of the faces.

        Returns
        -------
        list[int]
            The list of neighboring vertices.
            If the vertex lies on the boundary of the mesh,
            an ordered list always starts and ends with with boundary vertices.

        Notes
        -----
        Due to the nature of the ordering algorithm, the neighbors cycle around
        the node in the opposite direction as the cycling direction of the faces.
        For some algorithms this produces the expected results. For others it doesn't.
        For example, a dual mesh constructed relying on these conventions will have
        oposite face cycle directions compared to the original.

        """
        temp = list(self.halfedge[key])
        if not ordered:
            return temp
        if not temp:
            return temp
        if len(temp) == 1:
            return temp
        # if one of the neighbors points to the *outside* face
        # start there
        # otherwise the starting point can be random
        start = temp[0]
        for nbr in temp:
            if self.halfedge[key][nbr] is None:
                start = nbr
                break
        # start in the opposite direction
        # to avoid pointing at an *outside* face again
        fkey = self.halfedge[start][key]
        nbrs = [start]
        count = 1000
        while count:
            count -= 1
            nbr = self.face_vertex_descendant(fkey, key)
            fkey = self.halfedge[nbr][key]
            if nbr == start:
                break
            nbrs.append(nbr)
            if fkey is None:
                break
        return nbrs

    def vertex_neighborhood(self, key, ring=1):
        """Return the vertices in the neighborhood of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        ring : int, optional
            The number of neighborhood rings to include.

        Returns
        -------
        list[int]
            The vertices in the neighborhood.

        Notes
        -----
        The vertices in the neighborhood are unordered.

        """
        nbrs = set(self.vertex_neighbors(key))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for key in nbrs:
                temp += self.vertex_neighbors(key)
            nbrs.update(temp)
            i += 1
        return nbrs

    def vertex_degree(self, key):
        """Count the neighbors of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        int
            The degree of the vertex.

        """
        return len(self.vertex_neighbors(key))

    def vertex_min_degree(self):
        """Compute the minimum degree of all vertices.

        Returns
        -------
        int
            The lowest degree of all vertices.

        """
        if not self.vertex:
            return 0
        return min(self.vertex_degree(key) for key in self.vertices())

    def vertex_max_degree(self):
        """Compute the maximum degree of all vertices.

        Returns
        -------
        int
            The highest degree of all vertices.

        """
        if not self.vertex:
            return 0
        return max(self.vertex_degree(key) for key in self.vertices())

    def vertex_faces(self, key, ordered=False, include_none=False):
        """The faces connected to a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        ordered : bool, optional
            If True, return the faces in cycling order.
        include_none : bool, optional
            If True, include *outside* faces in the list.

        Returns
        -------
        list[int]
            The faces connected to a vertex.

        """
        if not ordered:
            faces = list(self.halfedge[key].values())
        else:
            nbrs = self.vertex_neighbors(key, ordered=True)
            faces = [self.halfedge[key][n] for n in nbrs]
        if include_none:
            return faces
        return [fkey for fkey in faces if fkey is not None]

    # --------------------------------------------------------------------------
    # Edge topology
    # --------------------------------------------------------------------------

    def has_edge(self, key):
        """Verify that the mesh contains a specific edge.

        Warnings
        --------
        This method may produce unexpected results.

        Parameters
        ----------
        key : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        bool
            True if the edge exists.
            False otherwise.

        """
        return key in set(self.edges())

    def has_halfedge(self, key):
        """Verify that a halfedge is part of the mesh.

        Parameters
        ----------
        key : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        bool
            True if the halfedge is part of the mesh.
            False otherwise.

        """
        u, v = key
        return u in self.halfedge and v in self.halfedge[u]

    def edge_faces(self, edge):
        """Find the two faces adjacent to an edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the edge.

        Returns
        -------
        tuple[int, int]
            The identifiers of the adjacent faces.
            If the edge is on the boundary, one of the identifiers is None.

        """
        u, v = edge
        return self.halfedge[u][v], self.halfedge[v][u]

    def halfedge_face(self, edge):
        """Find the face corresponding to a halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the halfedge.

        Returns
        -------
        int | None
            The identifier of the face corresponding to the halfedge.
            None, if the halfedge is on the outside of a boundary.

        Raises
        ------
        KeyError
            If the halfedge does not exist.

        """
        u, v = edge
        return self.halfedge[u][v]

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

        """
        u, v = edge
        return self.halfedge[v][u] is None or self.halfedge[u][v] is None

    # --------------------------------------------------------------------------
    # Polyedge topology
    # --------------------------------------------------------------------------

    def edge_loop(self, edge):
        """Find all edges on the same loop as a given edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        u, v = edge
        uv_loop = self.halfedge_loop((u, v))
        if uv_loop[0][0] == uv_loop[-1][1]:
            return uv_loop
        vu_loop = self.halfedge_loop((v, u))
        vu_loop[:] = [(u, v) for v, u in vu_loop[::-1]]
        return vu_loop + uv_loop[1:]

    def halfedge_loop(self, edge):
        """Find all edges on the same loop as the halfedge, in the direction of the halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        if self.is_edge_on_boundary(edge):
            return self._halfedge_loop_on_boundary(edge)
        edges = [edge]
        u, v = edge
        while True:
            nbrs = self.vertex_neighbors(v, ordered=True)
            if len(nbrs) != 4:
                break
            i = nbrs.index(u)
            u = v
            v = nbrs[i - 2]
            edges.append((u, v))
            if v == edges[0][0]:
                break
        return edges

    def _halfedge_loop_on_boundary(self, edge):
        """Find all edges on the same loop as the halfedge, in the direction of the halfedge, if the halfedge is on the boundary.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same loop as the given edge.

        """
        edges = [edge]
        u, v = edge
        while True:
            nbrs = self.vertex_neighbors(v)
            if len(nbrs) == 2:
                break
            nbr = None
            for temp in nbrs:
                if temp == u:
                    continue
                if self.is_edge_on_boundary((v, temp)):
                    nbr = temp
                    break
            if nbr is None:
                break
            u, v = v, nbr
            edges.append((u, v))
            if v == edges[0][0]:
                break
        return edges

    def edge_strip(self, edge, return_faces=False):
        """Find all edges on the same strip as a given edge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.
        return_faces : bool, optional
            Return the faces on the strip in addition to the edges.

        Returns
        -------
        list[tuple[int, int]] | tuple[list[tuple[int, int]], list[int]]
            If `return_faces` is False, the edges on the same strip as the given edge.
            If `return_faces` is False, the edges on the same strip and the corresponding faces.

        """
        u, v = edge
        if self.halfedge[v][u] is None:
            strip = self.halfedge_strip((u, v))
        elif self.halfedge[u][v] is None:
            edges = self.halfedge_strip((v, u))
            strip = [(u, v) for v, u in edges[::-1]]
        else:
            vu_strip = self.halfedge_strip((v, u))
            vu_strip[:] = [(u, v) for v, u in vu_strip[::-1]]
            if vu_strip[0] == vu_strip[-1]:
                strip = vu_strip
            else:
                uv_strip = self.halfedge_strip((u, v))
                strip = vu_strip[:-1] + uv_strip
        if not return_faces:
            return strip
        faces = [self.halfedge_face(edge) for edge in strip[:-1]]
        return strip, faces

    def halfedge_strip(self, edge):
        """Find all edges on the same strip as a given halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting edge.

        Returns
        -------
        list[tuple[int, int]]
            The edges on the same strip as the given halfedge.

        """
        u, v = edge
        edges = [edge]
        while True:
            face = self.halfedge[u][v]
            if face is None:
                break
            vertices = self.face_vertices(face)
            if len(vertices) != 4:
                break
            i = vertices.index(u)
            u = vertices[i - 1]
            v = vertices[i - 2]
            edges.append((u, v))
            if (u, v) == edge:
                break
        return edges

    # --------------------------------------------------------------------------
    # Face topology
    # --------------------------------------------------------------------------

    def has_face(self, fkey):
        """Verify that a face is part of the mesh.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face exists.
            False otherwise.

        """
        return fkey in self.face

    def face_vertices(self, fkey):
        """The vertices of a face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        list[int]
            Ordered vertex identifiers.

        """
        return self.face[fkey]

    def face_halfedges(self, fkey):
        """The halfedges of a face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        list[tuple[int, int]]
            The halfedges of a face.

        """
        vertices = self.face_vertices(fkey)
        return list(pairwise(vertices + vertices[0:1]))

    def face_corners(self, fkey):
        """Return triplets of face vertices forming the corners of the face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        list[int]
            The corners of the face in the form of a list of vertex triplets.

        """
        vertices = self.face_vertices(fkey)
        return list(window(vertices + vertices[0:2], 3))

    def face_neighbors(self, fkey):
        """Return the neighbors of a face across its edges.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        list[int]
            The identifiers of the neighboring faces.

        """
        nbrs = []
        for u, v in self.face_halfedges(fkey):
            nbr = self.halfedge[v][u]
            if nbr is not None:
                nbrs.append(nbr)
        return nbrs

    def face_neighborhood(self, key, ring=1):
        """Return the faces in the neighborhood of a face.

        Parameters
        ----------
        key : int
            The identifier of the face.
        ring : int, optional
            The size of the neighborhood.

        Returns
        -------
        list[int]
            A list of face identifiers.

        """
        nbrs = set(self.face_neighbors(key))
        i = 1
        while True:
            if i == ring:
                break
            temp = []
            for key in nbrs:
                temp += self.face_neighbors(key)
            nbrs.update(temp)
            i += 1
        return list(nbrs)

    def face_degree(self, fkey):
        """Count the neighbors of a face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.

        Returns
        -------
        int
            The count.

        """
        return len(self.face_neighbors(fkey))

    def face_min_degree(self):
        """Compute the minimum degree of all faces.

        Returns
        -------
        int
            The lowest degree.

        """
        if not self.face:
            return 0
        return min(self.face_degree(fkey) for fkey in self.faces())

    def face_max_degree(self):
        """Compute the maximum degree of all faces.

        Returns
        -------
        int
            The highest degree.

        """
        if not self.face:
            return 0
        return max(self.face_degree(fkey) for fkey in self.faces())

    def face_vertex_ancestor(self, fkey, key, n=1):
        """Return the n-th vertex before the specified vertex in a specific face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.
        key : int
            The identifier of the vertex.
        n : int, optional
            The index of the vertex ancestor.
            Default is 1, meaning the previous vertex.

        Returns
        -------
        int
            The identifier of the vertex before the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        """
        i = self.face[fkey].index(key)
        return self.face[fkey][(i - n) % len(self.face[fkey])]

    def face_vertex_descendant(self, fkey, key, n=1):
        """Return the n-th vertex after the specified vertex in a specific face.

        Parameters
        ----------
        fkey : int
            Identifier of the face.
        key : int
            The identifier of the vertex.
        n : int, optional
            The index of the vertex descendant.
            Default is 1, meaning the next vertex.

        Returns
        -------
        int
            The identifier of the vertex after the given vertex in the face cycle.

        Raises
        ------
        ValueError
            If the vertex is not part of the face.

        """
        i = self.face[fkey].index(key)
        return self.face[fkey][(i + n) % len(self.face[fkey])]

    def face_adjacency_halfedge(self, f1, f2):
        """Find one half-edge over which two faces are adjacent.

        Parameters
        ----------
        f1 : int
            The identifier of the first face.
        f2 : int
            The identifier of the second face.

        Returns
        -------
        tuple[int, int] | None
            The half-edge separating face 1 from face 2,
            or None, if the faces are not adjacent.

        Notes
        -----
        For use in form-finding algorithms, that rely on form-force duality information,
        further checks relating to the orientation of the corresponding are required.

        """
        for u, v in self.face_halfedges(f1):
            if self.halfedge[v][u] == f2:
                return u, v

    def face_adjacency_vertices(self, f1, f2):
        """Find all vertices over which two faces are adjacent.

        Parameters
        ----------
        f1 : int
            The identifier of the first face.
        f2 : int
            The identifier of the second face.

        Returns
        -------
        list[int] | None
            The vertices separating face 1 from face 2,
            or None, if the faces are not adjacent.

        """
        return [vkey for vkey in self.face_vertices(f1) if vkey in self.face_vertices(f2)]

    def is_face_on_boundary(self, key):
        """Verify that a face is on a boundary.

        Parameters
        ----------
        key : int
            The identifier of the face.

        Returns
        -------
        bool
            True if the face is on the boundary.
            False otherwise.

        """
        a = [self.halfedge[v][u] for u, v in self.face_halfedges(key)]
        if None in a:
            return True
        else:
            return False

    face_vertex_after = face_vertex_descendant
    face_vertex_before = face_vertex_ancestor

    def halfedge_after(self, edge):
        """Find the halfedge after the given halfedge in the same face.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting halfedge.

        Returns
        -------
        tuple[int, int]
            The next halfedge.

        """
        u, v = edge
        face = self.halfedge_face(edge)
        if face is not None:
            w = self.face_vertex_after(face, v)
            return v, w
        nbrs = self.vertex_neighbors(v, ordered=True)
        w = nbrs[0]
        return v, w

    def halfedge_before(self, edge):
        """Find the halfedge before the given halfedge in the same face.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting halfedge.

        Returns
        -------
        tuple[int, int]
            The previous halfedge.

        """
        u, v = edge
        face = self.halfedge_face(edge)
        if face is not None:
            t = self.face_vertex_before(face, u)
            return t, u
        nbrs = self.vertex_neighbors(u, ordered=True)
        t = nbrs[-1]
        return t, u

    def vertex_edges(self, vertex):
        """Find all edges connected to a given vertex.

        Parameters
        ----------
        vertex : int

        Returns
        -------
        list[tuple[int, int]]

        """
        edges = []
        for nbr in self.vertex_neighbors(vertex):
            if self.has_edge((vertex, nbr)):
                edges.append((vertex, nbr))
            else:
                edges.append((nbr, vertex))
        return edges

    def halfedge_loop_vertices(self, edge):
        """Find all vertices on the same loop as a given halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting halfedge.
        Returns
        -------
        list[int]
            The vertices on the same loop as the given halfedge.

        """
        loop = self.halfedge_loop(edge)
        return [loop[0][0]] + [edge[1] for edge in loop]

    def halfedge_strip_faces(self, edge):
        """Find all faces on the same strip as a given halfedge.

        Parameters
        ----------
        edge : tuple[int, int]
            The identifier of the starting halfedge.

        Returns
        -------
        list[int]
            The faces on the same strip as the given halfedge.

        """
        strip = self.halfedge_strip(edge)
        return [self.halfedge_face(edge) for edge in strip]

    # --------------------------------------------------------------------------
    # Mesh geometry
    # --------------------------------------------------------------------------

    def area(self):
        """Calculate the total mesh area.

        Returns
        -------
        float
            The area.

        """
        return sum(self.face_area(fkey) for fkey in self.faces())

    def centroid(self):
        """Calculate the mesh centroid.

        Returns
        -------
        list[float]
            The coordinates of the mesh centroid.

        """
        return scale_vector(
            sum_vectors([scale_vector(self.face_centroid(fkey), self.face_area(fkey)) for fkey in self.faces()]),
            1.0 / self.area(),
        )

    def normal(self):
        """Calculate the average mesh normal.

        Returns
        -------
        list[float]
            The coordinates of the mesh normal.

        """
        return scale_vector(
            sum_vectors([scale_vector(self.face_normal(fkey), self.face_area(fkey)) for fkey in self.faces()]),
            1.0 / self.area(),
        )

    def aabb(self):
        """Calculate the axis aligned bounding box of the mesh.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        xyz = self.vertices_attributes("xyz")
        return Box.from_bounding_box(bounding_box(xyz))

    def obb(self):
        """Calculate the oriented bounding box of the mesh.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        xyz = self.vertices_attributes("xyz")
        return Box.from_bounding_box(oriented_bounding_box(xyz))

    # --------------------------------------------------------------------------
    # Vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, key, axes="xyz"):
        """Return the coordinates of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        axes : str, optional
            The axes along which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list[float]
            Coordinates of the vertex.

        """
        return self.vertex_attributes(key, axes)

    def vertex_point(self, key):
        """Return the point of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point of the vertex.
        """
        return Point(*self.vertex_coordinates(key))  # type: ignore

    def vertices_points(self, vertices):
        """Return the points of multiple vertices.

        Parameters
        ----------
        vertices : list[int]
            The identifiers of the vertices.

        Returns
        -------
        list[:class:`compas.geometry.Point`]
            The points of the vertices.
        """
        return [self.vertex_point(vertex) for vertex in vertices]

    def set_vertex_point(self, vertex, point):
        """Set the point of a vertex.

        Parameters
        ----------
        vertex : int
            The identifier of the vertex.
        point : :class:`compas.geometry.Point`
            The point to set.

        Returns
        -------
        None

        """
        self.vertex_attributes(vertex, "xyz", point)

    def vertex_area(self, key):
        """Compute the tributary area of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        float
            The tributary are.

        """
        area = 0.0

        p0 = self.vertex_coordinates(key)

        for nbr in self.halfedge[key]:
            p1 = self.vertex_coordinates(nbr)
            v1 = subtract_vectors(p1, p0)

            fkey = self.halfedge[key][nbr]
            if fkey is not None:
                p2 = self.face_centroid(fkey)
                v2 = subtract_vectors(p2, p0)
                area += length_vector(cross_vectors(v1, v2))

            fkey = self.halfedge[nbr][key]
            if fkey is not None:
                p3 = self.face_centroid(fkey)
                v3 = subtract_vectors(p3, p0)
                area += length_vector(cross_vectors(v1, v3))

        return 0.25 * area

    def vertex_laplacian(self, key):
        """Compute the vector from a vertex to the centroid of its neighbors.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The Laplacian vector.

        """
        c = self.vertex_neighborhood_centroid(key)
        p = self.vertex_coordinates(key)
        return Vector(*subtract_vectors(c, p))

    def vertex_neighborhood_centroid(self, key):
        """Compute the centroid of the neighbors of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        :class:`compas.geometry.Point`
            The centroid of the vertex neighbors.

        """
        return Point(*centroid_points([self.vertex_coordinates(nbr) for nbr in self.vertex_neighbors(key)]))

    def vertex_normal(self, key):
        """Return the normal vector at the vertex as the weighted average of the
        normals of the neighboring faces.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The normal vector.

        """
        vectors = [self.face_normal(fkey, False) for fkey in self.vertex_faces(key) if fkey is not None]
        return Vector(*normalize_vector(centroid_points(vectors)))

    def vertex_curvature(self, vkey):
        """Dimensionless vertex curvature.

        Parameters
        ----------
        fkey : int
            The face key.

        Returns
        -------
        float
            The dimensionless curvature.

        References
        ----------
        Based on [#]_.

        .. [#] Botsch, Mario, et al. *Polygon mesh processing.* AK Peters/CRC Press, 2010.

        """
        C = 0
        for u, v in pairwise(self.vertex_neighbors(vkey, ordered=True) + self.vertex_neighbors(vkey, ordered=True)[:1]):
            C += angle_points(
                self.vertex_coordinates(vkey),
                self.vertex_coordinates(u),
                self.vertex_coordinates(v),
            )
        return 2 * pi - C

    # --------------------------------------------------------------------------
    # Edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, edge, axes="xyz"):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        edge : tuple(int, int)
            The identifier of the edge.
        axes : str, optional
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple(point, point)
            The coordinates of the start point.
            The coordinates of the end point.

        """
        return self.vertex_coordinates(edge[0], axes=axes), self.vertex_coordinates(edge[1], axes=axes)

    def edge_start(self, edge):
        """Return the point at the start of an edge.

        Parameters
        ----------
        edge : tuple(int, int)
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the start.

        """
        return self.vertex_point(edge[0])

    def edge_end(self, edge):
        """Return the point at the end of an edge.

        Parameters
        ----------
        edge : tuple(int, int)
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the end.

        """
        return self.vertex_point(edge[1])

    def edge_length(self, edge):
        """Return the length of an edge.

        Parameters
        ----------
        edge : tuple(int, int)
            The identifier of the edge.

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
        edge : tuple(int, int)
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Vector`

        """
        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return Vector(*ab)

    def edge_point(self, edge, t=0.5):
        """Return a point along an edge.

        Parameters
        ----------
        edge : tuple(int, int)
            The identifier of the edge.
        t : float, optional
            The location of the point on the edge.
            If the value of `t` is outside the range 0-1, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at parameter ``t``.

        """
        a, b = self.edge_coordinates(edge)
        ab = subtract_vectors(b, a)
        return Point(*add_vectors(a, scale_vector(ab, t)))

    def edge_midpoint(self, edge):
        """Return the midpoint of an edge.

        Parameters
        ----------
        edge : tuple(int, int)
            The identifier of the edge.

        Returns
        -------
        list[float]
            The XYZ coordinates of the midpoint.

        """
        a, b = self.edge_coordinates(edge)
        return Point(*midpoint_line((a, b)))

    def edge_direction(self, edge):
        """Return the direction vector of an edge.

        Parameters
        ----------
        edge : tuple(int, int)
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Vector`
            The direction vector of the edge.

        """
        vector = self.edge_vector(edge)
        vector.unitize()
        return vector

    def edge_line(self, edge):
        """Return the line of an edge.

        Parameters
        ----------
        edge : tuple(int, int)
            The identifier of the edge.

        Returns
        -------
        :class:`compas.geometry.Line`
            The line of the edge.

        """
        return Line(*self.edge_coordinates(edge))

    # --------------------------------------------------------------------------
    # Face geometry
    # --------------------------------------------------------------------------

    def face_coordinates(self, fkey, axes="xyz"):
        """Compute the coordinates of the vertices of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.
        axes : str, optional
            The axes along which to take the coordinates.
            Should be a combination of x, y, and z.

        Returns
        -------
        list[list[float]]
            The coordinates of the vertices of the face.

        """
        return [self.vertex_coordinates(key, axes=axes) for key in self.face_vertices(fkey)]

    def face_points(self, fkey):
        """Compute the points of the vertices of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        list[:class:`compas.geometry.Point`]
            The points of the vertices of the face.

        """
        return [self.vertex_point(key) for key in self.face_vertices(fkey)]

    def face_normal(self, fkey, unitized=True):
        """Compute the normal of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.
        unitized : bool, optional
            If True, the vector is unitized.

        Returns
        -------
        :class:`compas.geometry.Vector`

        """
        return Vector(*normal_polygon(self.face_coordinates(fkey), unitized=unitized))

    def face_centroid(self, fkey):
        """Compute the point at the centroid of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the centroid.

        """
        return Point(*centroid_points(self.face_coordinates(fkey)))

    def face_center(self, fkey):
        """Compute the point at the center of mass of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        :class:`compas.geometry.Point`
            The point at the center of mass.

        """
        return Point(*centroid_polygon(self.face_coordinates(fkey)))  # type: ignore

    def face_area(self, fkey):
        """Compute the area of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        float
            The area of the face.

        """
        return area_polygon(self.face_coordinates(fkey))

    def face_flatness(self, fkey, maxdev=0.02):
        """Compute the flatness of the mesh face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.
        maxdev : float, optional
            A maximum value for the allowed deviation from flatness.

        Returns
        -------
        float
            The flatness.

        Raises
        ------
        Exception
            If the face has more than 4 vertices.

        Notes
        -----
        Flatness is computed as the ratio of the distance between the diagonals
        of the face to the average edge length. A practical limit on this value
        realted to manufacturing is 0.02 (2%).

        Warnings
        --------
        This method only makes sense for quadrilateral faces.

        """
        vertices = self.face_vertices(fkey)
        f = len(vertices)

        if f == 3:
            return 0.0
        if f > 4:
            raise Exception("Computing face flatness for faces with more than 4 vertices is not supported.")

        points = self.vertices_attributes("xyz", keys=vertices) or []
        lengths = [distance_point_point(a, b) for a, b in pairwise(points + points[:1])]
        length = sum(lengths) / f
        d = distance_line_line((points[0], points[2]), (points[1], points[3]))
        return (d / length) / maxdev

    def face_aspect_ratio(self, fkey):
        """Face aspect ratio as the ratio between the lengths of the maximum and minimum face edges.

        Parameters
        ----------
        fkey : int
            The face key.

        Returns
        -------
        float
            The aspect ratio.

        References
        ----------
        * Wikipedia. *Types of mesh*. Available at: https://en.wikipedia.org/wiki/Types_of_mesh.

        """
        face_edge_lengths = [self.edge_length(edge) for edge in self.face_halfedges(fkey)]
        return max(face_edge_lengths) / min(face_edge_lengths)

    def face_skewness(self, fkey):
        """Face skewness as the maximum absolute angular deviation from the idefault_edge_attributesl polygon angle.

        Parameters
        ----------
        fkey : int
            The face key.

        Returns
        -------
        float
            The skewness.

        References
        ----------
        * Wikipedia. *Types of mesh*. Available at: https://en.wikipedia.org/wiki/Types_of_mesh.

        """
        idefault_edge_attributesl_angle = 180 * (1 - 2 / float(len(self.face_vertices(fkey))))
        angles = []
        vertices = self.face_vertices(fkey)
        for u, v, w in window(vertices + vertices[:2], n=3):
            o = self.vertex_coordinates(v)
            a = self.vertex_coordinates(u)
            b = self.vertex_coordinates(w)
            angle = angle_points(o, a, b, deg=True)
            angles.append(angle)
        return max(
            (max(angles) - idefault_edge_attributesl_angle) / (180 - idefault_edge_attributesl_angle),  # type: ignore
            (idefault_edge_attributesl_angle - min(angles)) / idefault_edge_attributesl_angle,  # type: ignore
        )

    def face_curvature(self, fkey):
        """Dimensionless face curvature.

        Face curvature is defined as the maximum face vertex deviation from
        the best-fit plane of the face vertices divided by the average lengths of
        the face vertices to the face centroid.

        Parameters
        ----------
        fkey : int
            The face key.

        Returns
        -------
        float
            The dimensionless curvature.

        """
        vertices = self.face_vertices(fkey)
        points = [self.vertex_coordinates(key) for key in vertices]
        centroid = self.face_centroid(fkey)
        plane = bestfit_plane(points)
        max_deviation = max([distance_point_plane(point, plane) for point in points])
        average_distances = vector_average([distance_point_point(point, centroid) for point in points])
        return max_deviation / average_distances

    def face_plane(self, face):
        """A plane defined by the centroid and the normal of the face.

        Parameters
        ----------
        face : int
            The face identifier.

        Returns
        -------
        :class:`compas.geometry.Plane`
            The plane of the face.

        """
        return Plane(self.face_centroid(face), self.face_normal(face))

    def face_polygon(self, face):
        """The polygon of a face.

        Parameters
        ----------
        face : int
            The face identifier.

        Returns
        -------
        :class:`compas.geometry.Polygon`
            The polygon of the face.

        """
        return Polygon(self.face_coordinates(face))

    def face_circle(self, face):
        """The circle of a face.

        Parameters
        ----------
        face : int
            The face identifier.

        Returns
        -------
        :class:`compas.geometry.Circle`
            The circle of the face.

        """
        from compas.geometry import bestfit_circle_numpy

        point, normal, radius = bestfit_circle_numpy(self.face_coordinates(face))
        return Circle.from_plane_and_radius(Plane(point, normal), radius)

    def face_frame(self, face):
        """The frame of a face.

        Parameters
        ----------
        face : int
            The face identifier.

        Returns
        -------
        :class:`compas.geometry.Frame`
            The frame of the face.

        """
        from compas.geometry import bestfit_frame_numpy

        point, xaxis, yaxis = bestfit_frame_numpy(self.face_coordinates(face))
        return Frame(point, xaxis, yaxis)

    # --------------------------------------------------------------------------
    # Boundaries
    # --------------------------------------------------------------------------

    def vertices_on_boundary(self):
        """Find the vertices on the longest boundary.

        Returns
        -------
        list[int]
            The vertices of the longest boundary.

        """
        boundaries = self.vertices_on_boundaries()
        return boundaries[0] if boundaries else []

    def edges_on_boundary(self):
        """Find the edges on the longest boundary.

        Returns
        -------
        list[tuple[int, int]]
            The edges of the longest boundary.

        """
        boundaries = self.edges_on_boundaries()
        return boundaries[0] if boundaries else []

    def faces_on_boundary(self):
        """Find the faces on the longest boundary.

        Returns
        -------
        list[int]
            The faces on the longest boundary.

        """
        boundaries = self.faces_on_boundaries()
        return boundaries[0] if boundaries else []

    def vertices_on_boundaries(self):
        """Find the vertices on all boundaries of the mesh.

        Returns
        -------
        list[list[int]]
            A list of vertex keys per boundary.
            The boundary with the most vertices is returned first.

        """
        # all boundary vertices
        vertices_set = set()
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, face in iter(nbrs.items()):
                if face is None:
                    vertices_set.add(key)
                    vertices_set.add(nbr)
        vertices_all = list(vertices_set)

        # return an empty list if there are no boundary vertices
        if not vertices_all:
            return []

        # init container for boundary groups
        boundaries = []

        # identify *special* vertices
        # these vertices are non-manifold
        # and should be processed differently
        special = []
        for key in vertices_all:
            count = 0
            for nbr in self.vertex_neighbors(key):
                face = self.halfedge_face((key, nbr))
                if face is None:
                    count += 1
                    if count > 1:
                        if key not in special:
                            special.append(key)

        superspecial = special[:]

        # process the special vertices first
        while special:
            start = special.pop()
            nbrs = []
            # find all neighbors of the current special vertex
            # that are on the mesh boundary
            for nbr in self.vertex_neighbors(start):
                face = self.halfedge_face((start, nbr))
                if face is None:
                    nbrs.append(nbr)
            # for normal mesh vertices
            # there should be only 1 boundary neighbor
            # for special vertices there are more and they all have to be processed
            while nbrs:
                vertex = nbrs.pop()
                vertices = [start, vertex]
                while True:
                    # this is a *super* special case
                    if vertex in superspecial:
                        boundaries.append(vertices)
                        break
                    # find the boundary loop for the current starting halfedge
                    for nbr in self.vertex_neighbors(vertex):
                        if nbr == vertices[-2]:
                            continue
                        face = self.halfedge_face((vertex, nbr))
                        if face is None:
                            vertices.append(nbr)
                            vertex = nbr
                            break
                    if vertex == start:
                        boundaries.append(vertices)
                        break
                # remove any neighbors that might be part of an already identified boundary
                nbrs = [vertex for vertex in nbrs if vertex not in vertices]

        # remove all boundary vertices that were already identified
        vertices_all = [vertex for vertex in vertices_all if all(vertex not in vertices for vertices in boundaries)]

        # process the remaining boundary vertices if any
        if vertices_all:
            key = vertices_all[0]
            while vertices_all:
                vertices = [key]
                start = key
                while True:
                    for nbr in self.vertex_neighbors(key):
                        face = self.halfedge_face((key, nbr))
                        if face is None:
                            vertices.append(nbr)
                            key = nbr
                            break
                    if key == start:
                        boundaries.append(vertices)
                        vertices_all = [x for x in vertices_all if x not in vertices]
                        break
                if vertices_all:
                    key = vertices_all[0]

        def length(boundary):
            return sum(self.edge_length(edge) for edge in pairwise(boundary + boundary[:1]))  # type: ignore

        return sorted(boundaries, key=length, reverse=True)

    def edges_on_boundaries(self):
        """Find the edges on all boundaries of the mesh.

        Returns
        -------
        list[list[tuple[int, int]]]
            A list of edges per boundary.

        """
        vertexgroups = self.vertices_on_boundaries()
        edgegroups = []
        for vertices in vertexgroups:
            edgegroups.append(list(pairwise(vertices)))
        return edgegroups

    def faces_on_boundaries(self):
        """Find the faces on all boundaries of the mesh.

        Returns
        -------
        list[list[int]]
            lists of faces, grouped and sorted per boundary.

        """
        vertexgroups = self.vertices_on_boundaries()
        facegroups = []
        for vertices in vertexgroups:
            temp = [self.halfedge_face((v, u)) for u, v in pairwise(vertices)]
            faces = []
            for face in temp:
                if face is None:
                    continue
                if face not in faces and all(face not in group for group in facegroups):
                    faces.append(face)
            if faces:
                facegroups.append(faces)
        return facegroups

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

    def transform_numpy(self, T):
        """Transform the mesh.

        Parameters
        ----------
        T : :class:`numpy.ndarray`
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
        >>> mesh.transform_numpy(T)

        """
        from compas.geometry import transform_points_numpy

        points = transform_points_numpy(self.vertices_attributes("xyz"), T)
        for vertex, point in zip(self.vertices(), points):
            self.vertex_attributes(vertex, "xyz", point)

    # --------------------------------------------------------------------------
    # Matrices
    # --------------------------------------------------------------------------

    def adjacency_matrix(self, rtype="array"):
        """Compute the adjacency matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The adjacency matrix.

        """
        from compas.matrices import adjacency_matrix

        vertex_index = self.vertex_index()
        adjacency = [[vertex_index[nbr] for nbr in self.vertex_neighbors(vertex)] for vertex in self.vertices()]
        return adjacency_matrix(adjacency, rtype=rtype)

    def connectivity_matrix(self, rtype="array"):
        """Compute the connectivity matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The connectivity matrix.

        """
        from compas.matrices import connectivity_matrix

        vertex_index = self.vertex_index()
        adjacency = [[vertex_index[nbr] for nbr in self.vertex_neighbors(vertex)] for vertex in self.vertices()]
        return connectivity_matrix(adjacency, rtype=rtype)

    def degree_matrix(self, rtype="array"):
        """Compute the degree matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The degree matrix.

        """
        from compas.matrices import degree_matrix

        vertex_index = self.vertex_index()
        adjacency = [[vertex_index[nbr] for nbr in self.vertex_neighbors(vertex)] for vertex in self.vertices()]
        return degree_matrix(adjacency, rtype=rtype)

    def face_matrix(self, rtype="array"):
        r"""Compute the face matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The face matrix.

        Notes
        -----
        The face matrix represents the relationship between faces and vertices.
        Each row of the matrix represents a face. Each column represents a vertex.
        The matrix is filled with zeros except where a relationship between a vertex
        and a face exist.

        .. math::

            F_{ij} =
            \begin{cases}
                1 & \text{if vertex j is part of face i} \\
                0 & \text{otherwise}
            \end{cases}

        The face matrix can for example be used to compute the centroids of all
        faces of a mesh.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_polyhedron(6)
        >>> F = mesh.face_matrix()
        >>> type(F)
        <class 'numpy.ndarray'>

        >>> from numpy import allclose, asarray
        >>> xyz = asarray(mesh.vertices_attributes('xyz'))
        >>> F = mesh.face_matrix(rtype='csr')
        >>> c1 = F.dot(xyz) / F.sum(axis=1)
        >>> c2 = [mesh.face_centroid(fkey) for fkey in mesh.faces()]
        >>> allclose(c1, c2)
        True

        """
        from compas.matrices import face_matrix

        vertex_index = self.vertex_index()
        faces = [[vertex_index[vertex] for vertex in self.face_vertices(face)] for face in self.faces()]
        return face_matrix(faces, rtype=rtype)

    def laplacian_matrix(self, rtype="array"):
        r"""Compute the Laplacian matrix of the mesh.

        Parameters
        ----------
        rtype : Literal['array', 'csc', 'csr', 'coo', 'list'], optional
            Format of the result.

        Returns
        -------
        array-like
            The Laplacian matrix.

        Notes
        -----
        The :math:`n \times n` uniform Laplacian matrix :math:`\mathbf{L}` of a mesh
        with vertices :math:`\mathbf{V}` and edges :math:`\mathbf{E}` is defined as
        follows [1]_

        .. math::

            \mathbf{L}_{ij} =
            \begin{cases}
                -1               & i = j \\
                \frac{1}{deg(i)} & (i, j) \in \mathbf{E} \\
                0                & \text{otherwise}
            \end{cases}

        with :math:`deg(i)` the degree of vertex :math:`i`.

        Therefore, the uniform Laplacian of a vertex :math:`\mathbf{v}_{i}` points to
        the centroid of its neighboring vertices.

        References
        ----------
        .. [1] Nealen A., Igarashi T., Sorkine O. and Alexa M.
            `Laplacian Mesh Optimization <https://igl.ethz.ch/projects/Laplacian-mesh-processing/Laplacian-mesh-optimization/lmo.pdf>`_.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_polyhedron(6)
        >>> L = mesh.laplacian_matrix(rtype='array')
        >>> type(L)
        <class 'numpy.ndarray'>

        >>> from numpy import asarray
        >>> xyz = asarray(mesh.vertices_attributes('xyz'))
        >>> L = mesh.laplacian_matrix(mesh)
        >>> d = L.dot(xyz)

        """
        from compas.matrices import laplacian_matrix

        vertex_index = self.vertex_index()
        adjacency = [[vertex_index[nbr] for nbr in self.vertex_neighbors(vertex)] for vertex in self.vertices()]
        return laplacian_matrix(adjacency, rtype=rtype)

    # --------------------------------------------------------------------------
    # Other methods
    # --------------------------------------------------------------------------

    def offset(self, distance=1.0):
        """Generate an offset mesh.

        Parameters
        ----------
        distance : float, optional
            The offset distance.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            The offset mesh.

        Notes
        -----
        If the offset distance is a positive value, the offset is in the direction of the vertex normal.
        If the value is negative, the offset is in the opposite direction.
        In both cases, the orientation of the offset mesh is the same as the orientation of the original.

        In areas with high degree of curvature, the offset mesh can have self-intersections.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> from compas.geometry import distance_point_point as dist
        >>> mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
        >>> mesh.offset()  # doctest: +ELLIPSIS
        <compas.datastructures.mesh.mesh.Mesh object at ...>

        """
        offset = self.copy()

        for vertex in offset.vertices():
            normal = self.vertex_normal(vertex)
            xyz = self.vertex_coordinates(vertex)
            offset.vertex_attributes(vertex, "xyz", add_vectors(xyz, scale_vector(normal, distance)))

        return offset

    def thickened(self, thickness=1.0, both=True):
        """Generate a thicknened mesh.

        Parameters
        ----------
        thickness : float, optional
            The mesh thickness.
            This should be a positive value.
        both : bool, optional
            If true, the mesh is thickened on both sides of the original.
            Otherwise, the mesh is thickened on the side of the positive normal.

        Returns
        -------
        :class:`compas.datastructures.Mesh`
            The thickened mesh.

        Raises
        ------
        ValueError
            If `thickness` is not a positive number.

        Examples
        --------
        >>> from compas.datastructures import Mesh
        >>> mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
        >>> mesh.thickened()  # doctest: +ELLIPSIS
        <compas.datastructures.mesh.mesh.Mesh object at ...>

        """
        if thickness <= 0:
            raise ValueError("Thickness should be a positive number.")

        if both:
            mesh_top = self.offset(+0.5 * thickness)  # type: Mesh
            mesh_bottom = self.offset(-0.5 * thickness)  # type: Mesh
        else:
            mesh_top = self.offset(thickness)
            mesh_bottom = self.copy()

        # flip bottom part
        mesh_bottom.flip_cycles()

        # join parts
        thickened_mesh = mesh_top.copy()  # type: Mesh
        thickened_mesh.join(mesh_bottom)

        # close boundaries
        n = thickened_mesh.number_of_vertices() / 2

        edges_on_boundary = [edge for boundary in list(thickened_mesh.edges_on_boundaries()) for edge in boundary]

        for u, v in edges_on_boundary:
            if u < n and v < n:
                thickened_mesh.add_face([u, v, v + n, u + n])

        return thickened_mesh

    # the only reason this function is here and not in halfedge
    # is because "from_vertices_and_faces" doesn't accept general vertex data
    # perhaps there should be
    # * from_vertices_and_faces
    # * from_points_and_faces
    def exploded(self):
        """Explode the mesh into its connected components.

        Returns
        -------
        list[:class:`compas.datastructures.Mesh`]
            The list of the meshes from the exploded mesh parts.

        """
        cls = type(self)
        meshes = []
        for part in self.connected_faces():
            vertexkeys = list(set([vertex for face in part for vertex in self.face_vertices(face)]))
            vertices = self.vertices_attributes("xyz", keys=vertexkeys)
            vertex_index = {vertex: index for index, vertex in enumerate(vertexkeys)}
            faces = [[vertex_index[vertex] for vertex in self.face_vertices(face)] for face in part]
            meshes.append(cls.from_vertices_and_faces(vertices, faces))
        return meshes
