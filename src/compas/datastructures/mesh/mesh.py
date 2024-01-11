from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from math import pi
from itertools import product

import compas

if compas.PY2:
    from collections import Mapping
else:
    from collections.abc import Mapping

from compas.tolerance import TOL

from compas.files import OBJ
from compas.files import OFF
from compas.files import PLY
from compas.files import STL

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Line
from compas.geometry import Plane
from compas.geometry import Polygon
from compas.geometry import Circle
from compas.geometry import Frame
from compas.geometry import Polyhedron
from compas.geometry import angle_points
from compas.geometry import area_polygon
from compas.geometry import bestfit_plane
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import cross_vectors
from compas.geometry import distance_point_plane
from compas.geometry import distance_point_point
from compas.geometry import distance_line_line
from compas.geometry import length_vector
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import sum_vectors
from compas.geometry import midpoint_line
from compas.geometry import vector_average
from compas.geometry import bounding_box
from compas.geometry import oriented_bounding_box
from compas.geometry import transform_points

from compas.utilities import linspace
from compas.utilities import pairwise
from compas.utilities import window

from compas.topology import breadth_first_traverse
from compas.topology import face_adjacency

from compas.datastructures import HalfEdge

from .operations.collapse import mesh_collapse_edge
from .operations.merge import mesh_merge_faces
from .operations.split import mesh_split_edge
from .operations.split import mesh_split_face
from .operations.split import mesh_split_strip
from .operations.weld import mesh_unweld_edges
from .operations.weld import mesh_unweld_vertices

from .subdivision import mesh_subdivide
from .duality import mesh_dual
from .slice import mesh_slice_plane

from .smoothing import mesh_smooth_centroid
from .smoothing import mesh_smooth_area


class Mesh(HalfEdge):
    """Geometric implementation of a half edge data structure for polygon meshses.

    Parameters
    ----------
    default_vertex_attributes: dict[str, Any], optional
        Default values for vertex attributes.
    default_edge_attributes: dict[str, Any], optional
        Default values for edge attributes.
    default_face_attributes: dict[str, Any], optional
        Default values for face attributes.
    **kwargs : dict, optional
        Additional attributes to add to the mesh object.

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
    # split
    # trim
    unweld_vertices = mesh_unweld_vertices
    unweld_edges = mesh_unweld_edges

    smooth_centroid = mesh_smooth_centroid
    smooth_area = mesh_smooth_area

    def __init__(
        self, default_vertex_attributes=None, default_edge_attributes=None, default_face_attributes=None, **kwargs
    ):
        _default_vertex_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        _default_edge_attributes = {}
        _default_face_attributes = {}
        if default_vertex_attributes:
            _default_vertex_attributes.update(default_vertex_attributes)
        if default_edge_attributes:
            _default_edge_attributes.update(default_edge_attributes)
        if default_face_attributes:
            _default_face_attributes.update(default_face_attributes)
        super(Mesh, self).__init__(
            default_vertex_attributes=_default_vertex_attributes,
            default_edge_attributes=_default_edge_attributes,
            default_face_attributes=_default_face_attributes,
            **kwargs
        )

    def __str__(self):
        tpl = "<Mesh with {} vertices, {} faces, {} edges>"
        return tpl.format(self.number_of_vertices(), self.number_of_faces(), self.number_of_edges())

    # --------------------------------------------------------------------------
    # from/to
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
        For example, with :func:`compas.datastructures.mesh_quads_to_triangles`.

        """
        stl = STL(filepath, precision)
        stl.write(self, binary=binary, **kwargs)

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
        from compas.datastructures import Network

        network = Network.from_lines(lines, precision=precision)
        vertices = network.to_points()
        faces = network.find_cycles()
        mesh = cls.from_vertices_and_faces(vertices, faces)
        if delete_boundary_face:
            mesh.delete_face(0)
            mesh.cull_vertices()
        return mesh

    def to_lines(self):
        """Return the lines of the mesh as pairs of start and end point coordinates.

        Returns
        -------
        list[tuple[list[float], list[float]]]
            A list of lines each defined by a pair of point coordinates.

        """
        return [self.edge_coordinates(edge) for edge in self.edges()]

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

    def to_polylines(self):
        """Convert the mesh to a collection of polylines.

        Returns
        -------
        list[list[list[float]]]
            A list of polylines which are each defined as a list of points.

        """
        raise NotImplementedError

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
    def from_shape(cls, shape, **kwargs):  # type: (...) -> Mesh
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

    def to_points(self):
        """Convert the mesh to a collection of points.

        Returns
        -------
        list[list[float]]
            The points representing the vertices of the mesh.

        """
        raise NotImplementedError

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

    def to_polygons(self):
        """Convert the mesh to a collection of polygons.

        Returns
        -------
        list[list[list[float]]]
            A list of polygons defined each as a list of points.

        """
        return [self.face_coordinates(fkey) for fkey in self.faces()]

    @classmethod
    def from_meshgrid(cls, dx, nx, dy=None, ny=None):  # type: (...) -> Mesh
        """Create a mesh from faces and vertices on a regular grid.

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
    # helpers
    # --------------------------------------------------------------------------

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
    # builders
    # --------------------------------------------------------------------------

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

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

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
    # cleanup
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
        >>> mesh = Mesh.from_obj(compas.get('faces.obj'))
        >>> mesh.number_of_vertices()
        36
        >>> for x, y, z in mesh.vertices_attributes('xyz', keys=list(mesh.vertices())[:5]):
        ...     mesh.add_vertex(x=x, y=y, z=z)
        ...
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
    def unify_cycles(self, root=None):
        """Unify the cycles of the mesh.

        Returns
        -------
        None
            The mesh is modified in place.

        """

        def unify(node, nbr):
            # find the common edge
            for u, v in self.face_halfedges(nbr):
                if u in self.face[node] and v in self.face[node]:
                    # node and nbr have edge u-v in common
                    i = self.face[node].index(u)
                    j = self.face[node].index(v)
                    if i == j - 1 or (j == 0 and u == self.face[node][-1]):
                        # if the traversal of a neighboring halfedge
                        # is in the same direction
                        # flip the neighbor
                        self.face[nbr][:] = self.face[nbr][::-1]
                        return

        if root is None:
            root = self.face_sample(size=1)[0]

        index_face = {index: face for index, face in enumerate(self.faces())}
        points = self.vertices_attributes("xyz")
        faces = [self.face_vertices(face) for face in self.faces()]

        adj = face_adjacency(points, faces)
        adjacency = {}
        for face in adj:
            adjacency[index_face[face]] = [index_face[nbr] for nbr in adj[face]]

        visited = breadth_first_traverse(adjacency, root, unify)

        if len(list(visited)) != self.number_of_faces():
            raise Exception("Not all faces were visited.")

        self.halfedge = {key: {} for key in self.vertices()}
        for fkey in self.faces():
            for u, v in self.face_halfedges(fkey):
                self.halfedge[u][v] = fkey
                if u not in self.halfedge[v]:
                    self.halfedge[v][u] = None

    # --------------------------------------------------------------------------
    # vertex topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # edge topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # polyedge topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # face topology
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # mesh geometry
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
        list[[float, float, float]]
            XYZ coordinates of 8 points defining a box.

        """
        xyz = self.vertices_attributes("xyz")
        return bounding_box(xyz)

    def obb(self):
        """Calculate the oriented bounding box of the mesh.

        Returns
        -------
        list[[float, float, float]]
            XYZ coordinates of 8 points defining a box.

        """
        xyz = self.vertices_attributes("xyz")
        return oriented_bounding_box(xyz)

    # --------------------------------------------------------------------------
    # vertex geometry
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
    # edge geometry
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
    # face geometry
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
        """Face skewness as the maximum absolute angular deviation from the ideal polygon angle.

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
        ideal_angle = 180 * (1 - 2 / float(len(self.face_vertices(fkey))))
        angles = []
        vertices = self.face_vertices(fkey)
        for u, v, w in window(vertices + vertices[:2], n=3):
            o = self.vertex_coordinates(v)
            a = self.vertex_coordinates(u)
            b = self.vertex_coordinates(w)
            angle = angle_points(o, a, b, deg=True)
            angles.append(angle)
        return max(
            (max(angles) - ideal_angle) / (180 - ideal_angle),  # type: ignore
            (ideal_angle - min(angles)) / ideal_angle,  # type: ignore
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
        return Circle((point, normal), radius)

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
    # boundary
    # --------------------------------------------------------------------------

    def vertices_on_boundaries(self):
        """Find the vertices on the boundaries of the mesh.

        Returns
        -------
        list[list[int]]
            A list of vertex keys per boundary.
            The longest boundary is returned first.

        """

        def length(boundary):
            return sum(self.edge_length(edge) for edge in pairwise(boundary + boundary[:1]))  # type: ignore

        boundaries = super(Mesh, self).vertices_on_boundaries()
        return sorted(boundaries, key=length, reverse=True)

    # --------------------------------------------------------------------------
    # transformations
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
        >>> from compas.geometry import matrix_from_axis_and_angle_numpy
        >>> mesh = Mesh.from_polyhedron(6)
        >>> T = matrix_from_axis_and_angle_numpy([0, 0, 1], math.pi / 4)
        >>> mesh.transform_numpy(T)

        """
        from compas.geometry import transform_points_numpy

        points = transform_points_numpy(self.vertices_attributes("xyz"), T)
        for vertex, point in zip(self.vertices(), points):
            self.vertex_attributes(vertex, "xyz", point)

    # --------------------------------------------------------------------------
    # other methods
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
        >>> from compas.datastructures import Mesh, mesh_offset
        >>> from compas.geometry import distance_point_point as dist
        >>> mesh = Mesh.from_vertices_and_faces([[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0]], [[0, 1, 2, 3]])
        >>> mesh.offset()
        <compas.datastructures.mesh.mesh.Mesh object at 0x109eaad60>

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
        >>> mesh.thicken(mesh)
        <compas.datastructures.mesh.mesh.Mesh object at 0x109eaad60>

        """
        if thickness <= 0:
            raise ValueError("Thickness should be a positive number.")

        if both:
            mesh_top = self.offset(+0.5 * thickness)
            mesh_bottom = self.offset(-0.5 * thickness)
        else:
            mesh_top = self.offset(thickness)
            mesh_bottom = self.copy()

        # flip bottom part
        mesh_bottom.flip_cycles()

        # join parts
        thickened_mesh = mesh_top.join(mesh_bottom)

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
