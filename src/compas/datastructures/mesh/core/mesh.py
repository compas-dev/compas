from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import sys
from math import pi

from compas.datastructures.mesh.core.halfedge import HalfEdge

from compas.files import OBJ
from compas.files import OFF
from compas.files import PLY
from compas.files import STL

from compas.geometry import Polyhedron
from compas.geometry import angle_points
from compas.geometry import area_polygon
from compas.geometry import bestfit_plane
from compas.geometry import centroid_points
from compas.geometry import centroid_polygon
from compas.geometry import cross_vectors
from compas.geometry import distance_point_plane
from compas.geometry import distance_point_point
from compas.geometry import flatness
from compas.geometry import length_vector
from compas.geometry import normal_polygon
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import subtract_vectors
from compas.geometry import sum_vectors
from compas.geometry import midpoint_line

from compas.utilities import average
from compas.utilities import geometric_key
from compas.utilities import pairwise
from compas.utilities import window


__all__ = ['BaseMesh']


class BaseMesh(HalfEdge):
    """Geometric implementation of a half edge data structure for polygon meshses.

    Attributes
    ----------
    attributes : dict
        A dictionary of general mesh attributes.

        * ``'name': "Mesh"``

    default_vertex_attributes : dict
        The names of pre-assigned vertex attributes and their default values.

        * ``'x': 0.0``
        * ``'y': 0.0``
        * ``'z': 0.0``

    default_edge_attributes : dict
        The default data attributes assigned to every new edge.
    default_face_attributes : dict
        The default data attributes assigned to every new face.
    name : str
        The name of the mesh.
        Shorthand for ``mesh.attributes['name']``
    adjacency : dict, read-only
        The vertex adjacency dictionary.
    data : dict
        The data representing the mesh.
        The dict has the following structure:

        * 'attributes'   => dict
        * 'dva'          => dict
        * 'dea'          => dict
        * 'dfa'          => dict
        * 'vertex'       => dict
        * 'face'         => dict
        * 'facedata'     => dict
        * 'edgedata'     => dict
        * 'max_int_key'  => int
        * 'max_int_fkey' => int

    Examples
    --------
    >>> mesh = Mesh.from_polyhedron(6)
    >>> V = mesh.number_of_vertices()
    >>> E = mesh.number_of_edges()
    >>> F = mesh.number_of_faces()
    >>> mesh.euler() == V - E + F
    True

    """

    def __init__(self):
        super(BaseMesh, self).__init__()
        self.attributes.update({'name': 'Mesh'})
        self.default_vertex_attributes.update({'x': 0.0, 'y': 0.0, 'z': 0.0})

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
    def from_obj(cls, filepath, precision=None):
        """Construct a mesh object from the data described in an OBJ file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Mesh
            A mesh object.

        Note
        ----
        There are a few sample files available for testing and debugging:

        * faces.obj
        * faces_big.obj
        * faces_reversed.obj
        * hypar.obj
        * mesh.obj
        * quadmesh.obj

        Examples
        --------
        >>>
        """
        obj = OBJ(filepath, precision)
        obj.read()
        vertices = obj.vertices
        faces = obj.faces
        edges = obj.lines
        if faces:
            return cls.from_vertices_and_faces(vertices, faces)
        if edges:
            lines = [(vertices[u], vertices[v], 0) for u, v in edges]
            return cls.from_lines(lines)

    def to_obj(self, filepath, precision=None, unweld=False, **kwargs):
        """Write the mesh to an OBJ file.

        Parameters
        ----------
        filepath : str
            Full path of the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.
        unweld : bool, optional
            If true, all faces have their own unique vertices.
            If false, vertices are shared between faces if this is also the case in the mesh.
            Default is ``False``.

        Warning
        -------
        This function only writes geometric data about the vertices and
        the faces to the file.
        """
        obj = OBJ(filepath, precision=precision)
        obj.write(self, unweld=unweld, **kwargs)

    @classmethod
    def from_ply(cls, filepath, precision=None):
        """Construct a mesh object from the data described in a PLY file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        Mesh :
            A mesh object.

        Examples
        --------
        .. code-block:: python

            import compas
            from compas.datastructures import Mesh

            mesh = Mesh.from_obj(compas.get('bunny.ply'))

        """
        ply = PLY(filepath)
        vertices = ply.parser.vertices
        faces = ply.parser.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    def to_ply(self, filepath, **kwargs):
        """Write a mesh object to a PLY file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Examples
        --------
        >>>
        """
        ply = PLY(filepath)
        ply.write(self, **kwargs)

    @classmethod
    def from_stl(cls, filepath, precision=None):
        """Construct a mesh object from the data described in a STL file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Mesh :
            A mesh object.

        Examples
        --------
        >>>
        """
        stl = STL(filepath, precision)
        vertices = stl.parser.vertices
        faces = stl.parser.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    def to_stl(self, filepath, precision=None, **kwargs):
        """Write a mesh to an STL file.

        Parameters
        ----------
        filepath : str
            The path to the file.
        precision : str, optional
            Rounding precision for the vertex coordinates.
            Default is ``"3f"``.

        Returns
        -------
        None

        Notes
        -----
        STL files only support triangle faces.
        However, the writer does not perform any checks
        and will just treat every face as a triangle.
        It is your responsibility to convert all faces of your mesh to triangles.
        For example, with :func:`compas.datastructures.mesh_quads_to_triangles`.
        """
        stl = STL(filepath, precision)
        stl.write(self, **kwargs)

    @classmethod
    def from_off(cls, filepath):
        """Construct a mesh object from the data described in a OFF file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Returns
        -------
        Mesh :
            A mesh object.

        Examples
        --------
        >>>
        """
        off = OFF(filepath)
        vertices = off.reader.vertices
        faces = off.reader.faces
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    def to_off(self, filepath, **kwargs):
        """Write a mesh object to an OFF file.

        Parameters
        ----------
        filepath : str
            The path to the file.

        Examples
        --------
        >>>
        """
        off = OFF(filepath)
        off.write(self, **kwargs)

    @classmethod
    def from_lines(cls, lines, delete_boundary_face=False, precision=None):
        """Construct a mesh object from a list of lines described by start and end point coordinates.

        Parameters
        ----------
        lines : list
            A list of pairs of point coordinates.
        delete_boundary_face : bool, optional
            The algorithm that finds the faces formed by the connected lines
            first finds the face *on the outside*. In most cases this face is not expected
            to be there. Therefore, there is the option to have it automatically deleted.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        >>>
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

    def to_lines(self, filepath):
        raise NotImplementedError

    @classmethod
    def from_polylines(cls, boundary_polylines, other_polylines):
        """Construct mesh from polylines.

        Based on construction from_lines,
        with removal of vertices that are not polyline extremities
        and of faces that represent boundaries.

        This specific method is useful to get the mesh connectivity from a set of (discretised) curves,
        that could overlap and yield a wrong connectivity if using from_lines based on the polyline extremities only.

        Parameters
        ----------
        boundary_polylines : list
            List of polylines representing boundaries as lists of vertex coordinates.
        other_polylines : list
            List of the other polylines as lists of vertex coordinates.

        Returns
        -------
        Mesh
            A mesh object.
        """
        corner_vertices = [geometric_key(xyz) for polyline in boundary_polylines + other_polylines for xyz in [polyline[0], polyline[-1]]]
        boundary_vertices = [geometric_key(xyz) for polyline in boundary_polylines for xyz in polyline]
        mesh = cls.from_lines([(u, v) for polyline in boundary_polylines + other_polylines for u, v in pairwise(polyline)])
        # remove the vertices that are not from the polyline extremities and the faces with all their vertices on the boundary
        vertex_keys = [vkey for vkey in mesh.vertices() if geometric_key(mesh.vertex_coordinates(vkey)) in corner_vertices]
        vertex_map = {vkey: i for i, vkey in enumerate(vertex_keys)}
        vertices = [mesh.vertex_coordinates(vkey) for vkey in vertex_keys]
        faces = []
        for fkey in mesh.faces():
            if sum([geometric_key(mesh.vertex_coordinates(vkey)) not in boundary_vertices for vkey in mesh.face_vertices(fkey)]):
                faces.append([vertex_map[vkey] for vkey in mesh.face_vertices(fkey) if geometric_key(mesh.vertex_coordinates(vkey)) in corner_vertices])
        mesh.cull_vertices()
        return cls.from_vertices_and_faces(vertices, faces)

    def to_polylines(self):
        raise NotImplementedError

    @classmethod
    def from_vertices_and_faces(cls, vertices, faces):
        """Construct a mesh object from a list of vertices and faces.

        Parameters
        ----------
        vertices : list, dict
            A list of vertices, represented by their XYZ coordinates,
            or a dictionary of vertex keys pointing to their XYZ coordinates.
        faces : list, dict
            A list of faces, represented by a list of indices referencing the list of vertex coordinates,
            or a dictionary of face keys pointing to a list of indices referencing the list of vertex coordinates.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        >>>
        """
        mesh = cls()

        if sys.version_info[0] < 3:
            mapping = collections.Mapping
        else:
            mapping = collections.abc.Mapping

        if isinstance(vertices, mapping):
            for key, xyz in vertices.items():
                mesh.add_vertex(key=key, attr_dict={i: j for i, j in zip(['x', 'y', 'z'], xyz)})
        else:
            for x, y, z in iter(vertices):
                mesh.add_vertex(x=x, y=y, z=z)

        if isinstance(faces, mapping):
            for fkey, vertices in faces.items():
                mesh.add_face(vertices, fkey)
        else:
            for face in iter(faces):
                mesh.add_face(face)

        return mesh

    def to_vertices_and_faces(self):
        """Return the vertices and faces of a mesh.

        Returns
        -------
        tuple
            A 2-tuple containing

            * a list of vertices, represented by their XYZ coordinates, and
            * a list of faces.

            Each face is a list of indices referencing the list of vertex coordinates.

        Example
        -------
        >>>
        """
        key_index = self.key_index()
        vertices = [self.vertex_coordinates(key) for key in self.vertices()]
        faces = [[key_index[key] for key in self.face_vertices(fkey)] for fkey in self.faces()]
        return vertices, faces

    @classmethod
    def from_polyhedron(cls, f):
        """Construct a mesh from a platonic solid.

        Parameters
        ----------
        f : int
            The number of faces.
            Should be one of ``4, 6, 8, 12, 20``.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        >>>
        """
        p = Polyhedron(f)
        return cls.from_vertices_and_faces(p.vertices, p.faces)

    @classmethod
    def from_shape(cls, shape, **kwargs):
        """Construct a mesh from a primitive shape.

        Parameters
        ----------
        shape : :class: `compas.geometry.shape`
            The input shape to generate a mesh from.
        kwargs:
            Optional keyword arguments ``u`` and ``v`` for the resolution in u (Torus, Sphere, Cylinder, Cone) and v direction (Torus and Sphere).

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        >>>
        """
        vertices, faces = shape.to_vertices_and_faces(**kwargs)
        mesh = cls.from_vertices_and_faces(vertices, faces)
        return mesh

    @classmethod
    def from_points(cls, points, boundary=None, holes=None):
        """Construct a mesh from a delaunay triangulation of a set of points.

        Parameters
        ----------
        points : list
            XYZ coordinates of the points.
            Z coordinates should be zero.

        Returns
        -------
        Mesh
            A mesh object.

        Examples
        --------
        >>>
        """
        from compas.geometry import delaunay_from_points
        faces = delaunay_from_points(points, boundary=boundary, holes=holes)
        return cls.from_vertices_and_faces(points, faces)

    def to_points(self):
        raise NotImplementedError

    @classmethod
    def from_polygons(cls, polygons, precision=None):
        """Construct a mesh from a series of polygons.

        Parameters
        ----------
        polygons : list
            A list of polygons, with each polygon defined as an ordered list of
            XYZ coordinates of its corners.
        precision: str, optional
            The precision of the geometric map that is used to connect the lines.

        Returns
        -------
        Mesh
            A mesh object.
        """
        faces = []
        gkey_xyz = {}
        for points in polygons:
            face = []
            for xyz in points:
                gkey = geometric_key(xyz, precision=precision)
                gkey_xyz[gkey] = xyz
                face.append(gkey)
            faces.append(face)
        gkey_index = {gkey: index for index, gkey in enumerate(gkey_xyz)}
        vertices = gkey_xyz.values()
        faces[:] = [[gkey_index[gkey] for gkey in face] for face in faces]
        return cls.from_vertices_and_faces(vertices, faces)

    def to_polygons(self):
        return [self.face_coordinates(fkey) for fkey in self.faces()]

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def key_gkey(self, precision=None):
        """Returns a dictionary that maps vertex dictionary keys to the corresponding
        *geometric key* up to a certain precision.

        Parameters
        ----------
        precision : str (3f)
            The float precision specifier used in string formatting.

        Returns
        -------
        dict
            A dictionary of key-geometric key pairs.

        """
        gkey = geometric_key
        xyz = self.vertex_coordinates
        return {key: gkey(xyz(key), precision) for key in self.vertices()}

    def gkey_key(self, precision=None):
        """Returns a dictionary that maps *geometric keys* of a certain precision
        to the keys of the corresponding vertices.

        Parameters
        ----------
        precision : str (3f)
            The float precision specifier used in string formatting.

        Returns
        -------
        dict
            A dictionary of geometric key-key pairs.

        """
        gkey = geometric_key
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
        xyz : list, optional
            Specific XYZ coordinates for the inserted vertex.
        return_fkeys : bool, optional
            By default, this method returns only the key of the inserted vertex.
            This flag can be used to indicate that the keys of the newly created
            faces should be returned as well.

        Returns
        -------
        int
            The key of the inserted vertex, if ``return_fkeys`` is false.
        tuple
            The key of the newly created vertex
            and a list with the newly created faces, if ``return_fkeys`` is true.

        Examples
        --------
        >>>

        """
        fkeys = []
        if not xyz:
            x, y, z = self.face_center(fkey)
        else:
            x, y, z = xyz
        w = self.add_vertex(key=key, x=x, y=y, z=z)
        for u, v in self.face_halfedges(fkey):
            fkeys.append(self.add_face([u, v, w]))
        del self.face[fkey]
        if return_fkeys:
            return w, fkeys
        return w

    def join(self, other):
        """Add the vertices and faces of another mesh to the current mesh.

        Parameters
        ----------
        other : compas.datastructures.Mesh
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
        >>> T = Translation([2, 0, 0])
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

    # face strips?
    # edge chains?
    # ...?

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
        list
            The coordinates of the mesh centroid.
        """
        return scale_vector(sum_vectors([scale_vector(self.face_centroid(fkey), self.face_area(fkey)) for fkey in self.faces()]), 1. / self.area())

    def normal(self):
        """Calculate the average mesh normal.

        Returns
        -------
        list
            The coordinates of the mesh normal.
        """
        return scale_vector(sum_vectors([scale_vector(self.face_normal(fkey), self.face_area(fkey)) for fkey in self.faces()]), 1. / self.area())

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def vertex_coordinates(self, key, axes='xyz'):
        """Return the coordinates of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.
        axes : str, optional
            The axes along which to take the coordinates.
            Should be a combination of ``'x'``, ``'y'``, ``'z'``.
            Default is ``'xyz'``.

        Returns
        -------
        list
            Coordinates of the vertex.
        """
        return [self.vertex[key][axis] for axis in axes]

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

        Example
        -------
        >>>

        """
        area = 0.

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
        list
            The components of the vector.
        """
        c = self.vertex_neighborhood_centroid(key)
        p = self.vertex_coordinates(key)
        return subtract_vectors(c, p)

    def vertex_neighborhood_centroid(self, key):
        """Compute the centroid of the neighbors of a vertex.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        list
            The coordinates of the centroid.
        """
        return centroid_points([self.vertex_coordinates(nbr) for nbr in self.vertex_neighbors(key)])

    def vertex_normal(self, key):
        """Return the normal vector at the vertex as the weighted average of the
        normals of the neighboring faces.

        Parameters
        ----------
        key : int
            The identifier of the vertex.

        Returns
        -------
        list
            The components of the normal vector.
        """
        vectors = [self.face_normal(fkey, False) for fkey in self.vertex_faces(key) if fkey is not None]
        return normalize_vector(centroid_points(vectors))

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
        Based on [1]_

        .. [1] Botsch, Mario, et al. *Polygon mesh processing.* AK Peters/CRC Press, 2010.
        """
        C = 0
        for u, v in pairwise(self.vertex_neighbors(vkey, ordered=True) + self.vertex_neighbors(vkey, ordered=True)[:1]):
            C += angle_points(self.vertex_coordinates(vkey), self.vertex_coordinates(u), self.vertex_coordinates(v))
        return 2 * pi - C

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def edge_coordinates(self, u, v, axes='xyz'):
        """Return the coordinates of the start and end point of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.
        axes : str (xyz)
            The axes along which the coordinates should be included.

        Returns
        -------
        tuple
            The coordinates of the start point and the coordinates of the end point.

        """
        return self.vertex_coordinates(u, axes=axes), self.vertex_coordinates(v, axes=axes)

    def edge_length(self, u, v):
        """Return the length of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        float
            The length of the edge.

        """
        a, b = self.edge_coordinates(u, v)
        return distance_point_point(a, b)

    def edge_vector(self, u, v):
        """Return the vector of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        list
            The vector from u to v.

        """
        a, b = self.edge_coordinates(u, v)
        ab = subtract_vectors(b, a)
        return ab

    def edge_point(self, u, v, t=0.5):
        """Return the location of a point along an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.
        t : float (0.5)
            The location of the point on the edge.
            If the value of ``t`` is outside the range ``0-1``, the point will
            lie in the direction of the edge, but not on the edge vector.

        Returns
        -------
        list
            The XYZ coordinates of the point.

        """
        a, b = self.edge_coordinates(u, v)
        ab = subtract_vectors(b, a)
        return add_vectors(a, scale_vector(ab, t))

    def edge_midpoint(self, u, v):
        """Return the location of the midpoint of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        list
            The XYZ coordinates of the midpoint.

        """
        a, b = self.edge_coordinates(u, v)
        return midpoint_line((a, b))

    def edge_direction(self, u, v):
        """Return the direction vector of an edge.

        Parameters
        ----------
        u : int
            The key of the start vertex.
        v : int
            The key of the end vertex.

        Returns
        -------
        list
            The direction vector of the edge.

        """
        return normalize_vector(self.edge_vector(u, v))

    # --------------------------------------------------------------------------
    # face geometry
    # --------------------------------------------------------------------------

    def face_coordinates(self, fkey, axes='xyz'):
        """Compute the coordinates of the vertices of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.
        axes : str, optional
            The axes along which to take the coordinates.
            Should be a combination of ``'x'``, ``'y'``, ``'z'``.
            Default is ``'xyz'``.

        Returns
        -------
        list of list
            The coordinates of the vertices of the face.
        """
        return [self.vertex_coordinates(key, axes=axes) for key in self.face_vertices(fkey)]

    def face_normal(self, fkey, unitized=True):
        """Compute the normal of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.
        unitized : bool, optional
            Unitize the normal vector.
            Default is ``True``.

        Returns
        -------
        list
            The components of the normal vector.
        """
        return normal_polygon(self.face_coordinates(fkey), unitized=unitized)

    def face_centroid(self, fkey):
        """Compute the location of the centroid of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        list
            The coordinates of the centroid.
        """
        return centroid_points(self.face_coordinates(fkey))

    def face_center(self, fkey):
        """Compute the location of the center of mass of a face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        list
            The coordinates of the center of mass.
        """
        return centroid_polygon(self.face_coordinates(fkey))

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

    def face_flatness(self, fkey):
        """Compute the flatness of the mesh face.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        float
            The flatness.

        Note
        ----
        Flatness is computed as the ratio of the distance between the diagonals
        of the face to the average edge length. A practical limit on this value
        realted to manufacturing is 0.02 (2%).

        Warning
        -------
        This method only makes sense for quadrilateral faces.
        """
        vertices = self.face_coordinates(fkey)
        face = range(len(self.face_vertices(fkey)))
        return flatness(vertices, [face])[0]

    def face_aspect_ratio(self, fkey):
        """Face aspect ratio as the ratio between the lengths of the maximum and minimum face edges.

        Parameters
        ----------
        fkey : Key
            The face key.

        Returns
        -------
        float
            The aspect ratio.

        References
        ----------
        .. [1] Wikipedia. *Types of mesh*.
               Available at: https://en.wikipedia.org/wiki/Types_of_mesh.
        """
        face_edge_lengths = [self.edge_length(u, v) for u, v in self.face_halfedges(fkey)]
        return max(face_edge_lengths) / min(face_edge_lengths)

    def face_skewness(self, fkey):
        """Face skewness as the maximum absolute angular deviation from the ideal polygon angle.

        Parameters
        ----------
        fkey : Key
            The face key.

        Returns
        -------
        float
            The skewness.

        References
        ----------
        .. [1] Wikipedia. *Types of mesh*.
               Available at: https://en.wikipedia.org/wiki/Types_of_mesh.
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
        return max((max(angles) - ideal_angle) / (180 - ideal_angle), (ideal_angle - min(angles)) / ideal_angle)

    def face_curvature(self, fkey):
        """Dimensionless face curvature as the maximum face vertex deviation from
        the best-fit plane of the face vertices divided by the average lengths of
        the face vertices to the face centroid.

        Parameters
        ----------
        fkey : Key
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
        average_distances = average([distance_point_point(point, centroid) for point in points])
        return max_deviation / average_distances

    # --------------------------------------------------------------------------
    # boundary
    # --------------------------------------------------------------------------

    def vertices_on_boundary(self, ordered=False):
        """Find the vertices on the boundary.

        Parameters
        ----------
        ordered : bool, optional
            If ``True``, Return the vertices in the same order as they are found on the boundary.
            Default is ``False``.

        Returns
        -------
        list
            The vertices of the boundary.

        Warning
        -------
        If the vertices are requested in order, and the mesh has multiple borders,
        currently only the vertices of one of the borders will be returned.

        Examples
        --------
        >>>

        """
        vertices_set = set()
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, face in iter(nbrs.items()):
                if face is None:
                    vertices_set.add(key)
                    vertices_set.add(nbr)
        vertices = list(vertices_set)

        if not vertices:
            return vertices
        if not ordered:
            return vertices

        key = sorted([(key, self.vertex_coordinates(key)) for key in vertices], key=lambda x: (x[1][1], x[1][0]))[0][0]

        vertices = []
        start = key
        while 1:
            for nbr, fkey in iter(self.halfedge[key].items()):
                if fkey is None:
                    vertices.append(nbr)
                    key = nbr
                    break
            if key == start:
                break
        return vertices

    def edges_on_boundary(self, oriented=False):
        """Find the edges on the boundary.

        Parameters
        ----------
        oriented : bool, optional
            If ``False`` (default) the edges are aligned head-to-tail along the boundary.
            If ``True`` the edges have the same orientation as in the mesh.

        Returns
        -------
        edges : list
            The boundary edges.
        """
        vertices = self.vertices_on_boundary(ordered=True)
        edges = list(pairwise(vertices + vertices[:1]))
        if not oriented:
            return edges
        return [(u, v) if self.has_edge((u, v)) is None else (v, u) for u, v in edges]

    def faces_on_boundary(self):
        """Find the faces on the boundary.

        Returns
        -------
        list
            The faces on the boundary.
        """
        faces = []
        for u, v in self.edges_on_boundary():
            fkey = self.halfedge[v][u]
            if fkey not in faces:
                faces.append(fkey)
        return faces

    def vertices_on_boundaries(self):
        """Find the vertices on all boundaries of the mesh.

        Returns
        -------
        list of list
            A list of vertex keys per boundary.

        Examples
        --------
        >>>
        """
        vertices_set = set()
        for key, nbrs in iter(self.halfedge.items()):
            for nbr, face in iter(nbrs.items()):
                if face is None:
                    vertices_set.add(key)
                    vertices_set.add(nbr)
        vertices_all = list(vertices_set)

        if not vertices_all:
            return vertices_all

        key = sorted([(key, self.vertex_coordinates(key)) for key in vertices_all], key=lambda x: (x[1][1], x[1][0]))[0][0]

        boundaries = []
        while vertices_all:
            vertices = []
            start = key
            while 1:
                for nbr, fkey in iter(self.halfedge[key].items()):
                    if fkey is None:
                        vertices.append(nbr)
                        key = nbr
                        break
                if key == start:
                    boundaries.append(vertices)
                    vertices_all = [x for x in vertices_all if x not in vertices]
                    break
            if vertices_all:
                key = vertices_all[0]
        return boundaries

    def edges_on_boundaries(self):
        """"""
        vertexgroups = self.vertices_on_boundaries()
        edgegroups = []
        for vertices in vertexgroups:
            edgegroups.append(list(pairwise(vertices)))
        return edgegroups


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
