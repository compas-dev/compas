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

from compas.utilities import linspace
from compas.utilities import pairwise
from compas.utilities import window

from compas.datastructures import HalfEdge


class Mesh(HalfEdge):
    """Geometric implementation of a half edge data structure for polygon meshses.

    Parameters
    ----------
    name: str, optional
        The name of the datastructure.
    default_vertex_attributes: dict[str, Any], optional
        Default values for vertex attributes.
    default_edge_attributes: dict[str, Any], optional
        Default values for edge attributes.
    default_face_attributes: dict[str, Any], optional
        Default values for face attributes.

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

    def __init__(
        self,
        name=None,
        default_vertex_attributes=None,
        default_edge_attributes=None,
        default_face_attributes=None,
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
            name=name or "Mesh",
            default_vertex_attributes=_default_vertex_attributes,
            default_edge_attributes=_default_edge_attributes,
            default_face_attributes=_default_face_attributes,
        )

    def __str__(self):
        tpl = "<Mesh with {} vertices, {} faces, {} edges>"
        return tpl.format(self.number_of_vertices(), self.number_of_faces(), self.number_of_edges())

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
        from compas.datastructures import network_find_cycles

        network = Network.from_lines(lines, precision=precision)
        vertices = network.to_points()
        faces = network_find_cycles(network)
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
    def from_points(cls, points, boundary=None, holes=None):  # type: (...) -> Mesh
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
        from compas.geometry import delaunay_from_points

        faces = delaunay_from_points(points, boundary=boundary, holes=holes)
        return cls.from_vertices_and_faces(points, faces)

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
        faces = [
            [
                i * (ny + 1) + j,
                (i + 1) * (ny + 1) + j,
                (i + 1) * (ny + 1) + j + 1,
                i * (ny + 1) + j + 1,
            ]
            for i, j in product(range(nx), range(ny))
        ]

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

    def join(self, other):
        """Add the vertices and faces of another mesh to the current mesh.

        Parameters
        ----------
        other : :class:`compas.datastructures.Mesh`
            The other mesh.

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

    # --------------------------------------------------------------------------
    # accessors
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # attributes
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # mesh info
    # --------------------------------------------------------------------------

    # def genus(self):
    #     """Calculate the genus.

    #     Returns
    #     -------
    #     int
    #         The genus.

    #     References
    #     ----------
    #     .. [1] Wolfram MathWorld. *Genus*.
    #            Available at: http://mathworld.wolfram.com/Genus.html.
    #     """
    #     X = self.euler()
    #     # each boundary must be taken into account as if it was one face
    #     B = len(self.boundaries())
    #     if self.is_orientable():
    #         return (2 - (X + B)) / 2
    #     else:
    #         return 2 - (X + B)

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

        # return the boundary groups in order of the length of the group
        return sorted(boundaries, key=lambda vertices: len(vertices))[::-1]

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


# =============================================================================
# Additional methods for the mesh class
# =============================================================================


from .operations.collapse import mesh_collapse_edge  # noqa: E402
from .operations.split import mesh_split_edge  # noqa: E402
from .operations.split import mesh_split_face  # noqa: E402
from .operations.split import mesh_split_strip  # noqa: E402
from .operations.merge import mesh_merge_faces  # noqa: E402

from .bbox import mesh_bounding_box  # noqa: E402
from .bbox import mesh_bounding_box_xy  # noqa: E402
from .combinatorics import mesh_is_connected  # noqa: E402
from .combinatorics import mesh_connected_components  # noqa: E402
from .duality import mesh_dual  # noqa: E402
from .orientation import mesh_face_adjacency  # noqa: E402
from .orientation import mesh_flip_cycles  # noqa: E402
from .orientation import mesh_unify_cycles  # noqa: E402
from .slice import mesh_slice_plane  # noqa: E402
from .smoothing import mesh_smooth_centroid  # noqa: E402
from .smoothing import mesh_smooth_area  # noqa: E402
from .subdivision import mesh_subdivide  # noqa: E402
from .transformations import mesh_transform  # noqa: E402
from .transformations import mesh_transformed  # noqa: E402
from .triangulation import mesh_quads_to_triangles  # noqa: E402


Mesh.bounding_box = mesh_bounding_box  # type: ignore
Mesh.bounding_box_xy = mesh_bounding_box_xy  # type: ignore
Mesh.collapse_edge = mesh_collapse_edge  # type: ignore
Mesh.connected_components = mesh_connected_components  # type: ignore
Mesh.dual = mesh_dual  # type: ignore
Mesh.face_adjacency = mesh_face_adjacency  # type: ignore
Mesh.flip_cycles = mesh_flip_cycles  # type: ignore
Mesh.is_connected = mesh_is_connected  # type: ignore
Mesh.merge_faces = mesh_merge_faces  # type: ignore
Mesh.slice_plane = mesh_slice_plane  # type: ignore
Mesh.smooth_centroid = mesh_smooth_centroid  # type: ignore
Mesh.smooth_area = mesh_smooth_area  # type: ignore
Mesh.split_edge = mesh_split_edge  # type: ignore
Mesh.split_face = mesh_split_face  # type: ignore
Mesh.split_strip = mesh_split_strip  # type: ignore
Mesh.subdivide = mesh_subdivide  # type: ignore
Mesh.transform = mesh_transform  # type: ignore
Mesh.transformed = mesh_transformed  # type: ignore
Mesh.unify_cycles = mesh_unify_cycles  # type: ignore
Mesh.quads_to_triangles = mesh_quads_to_triangles  # type: ignore

if not compas.IPY:
    from .bbox_numpy import mesh_oriented_bounding_box_numpy
    from .bbox_numpy import mesh_oriented_bounding_box_xy_numpy

    Mesh.obb_numpy = mesh_oriented_bounding_box_numpy  # type: ignore
    Mesh.obb_xy_numpy = mesh_oriented_bounding_box_xy_numpy  # type: ignore
