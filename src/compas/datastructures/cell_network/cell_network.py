from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import HalfFace
from compas.datastructures import Mesh, Network, HalfEdge

from compas.geometry import Point, Vector, Line, Polygon, Polyhedron

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
from compas.utilities import pairwise
from compas.topology import face_adjacency
from compas.topology import unify_cycles


class CellNetwork(HalfFace):
    """Geometric implementation of a data structure for a collection of mixed topologic entities such as cells, faces, edges and nodes.


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

    # notes on the implementation
    # we derive from HalfFace, but we need to be able to add edges without faces as well, that is why we have a separate _partial edge dictionary

    def __init__(self, name=None, default_vertex_attributes=None, default_edge_attributes=None, default_face_attributes=None, default_cell_attributes=None):
        _default_vertex_attributes = {"x": 0.0, "y": 0.0, "z": 0.0}
        _default_edge_attributes = default_edge_attributes or {}
        _default_face_attributes = default_face_attributes or {}
        _default_cell_attributes = default_cell_attributes or {}
        if default_vertex_attributes:
            _default_vertex_attributes.update(default_vertex_attributes)
        super(CellNetwork, self).__init__(
            name=name or "CellNetwork",
            default_vertex_attributes=_default_vertex_attributes,
            default_edge_attributes=_default_edge_attributes,
            default_face_attributes=_default_face_attributes,
            default_cell_attributes=_default_cell_attributes,
        )
        self.partial_edge = {}
        self._edge = {}

    def __str__(self):
        tpl = "<CellNetwork with {} vertices, {} faces, {} cells, {} edges>"
        return tpl.format(
            self.number_of_vertices(),
            self.number_of_faces(),
            self.number_of_cells(),
            self.number_of_edges(),
        )

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    def add_face(self, vertices, fkey=None, attr_dict=None, **kwattr):
        fkey = self.add_halfface(vertices, fkey=fkey, attr_dict=attr_dict, **kwattr)

        for edge in self.face_edges(fkey):
            self.add_edge(*edge)
            self.partial_edge[edge[0]][edge[1]].add(fkey)  # why double
            # self.partial_edge[edge[1]][edge[0]].add(fkey)  # why double
        return fkey

        # self.partial_edge[u][v] = fkey
        #    if u not in self.halfedge[v]:
        #        self.halfedge[v][u] = None

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    def cell_to_mesh(self, cell):
        """Construct a mesh object from from a cell of a cell network.

        Parameters
        ----------
        cell : int
            Identifier of the cell.

        Returns
        -------
        :class:`~compas.datastructures.Mesh`
            A mesh object.

        See Also
        --------
        :meth:`cell_to_vertices_and_faces`

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

        See Also
        --------
        :meth:`cell_to_mesh`

        """
        vertices = self.cell_vertices(cell)
        faces = self.cell_faces(cell)
        vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
        vertices = [self.vertex_coordinates(vertex) for vertex in vertices]
        faces = [[vertex_index[vertex] for vertex in self.halfface_vertices(face)] for face in faces]
        return vertices, faces

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # builders
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # modifiers
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # cell network geometry
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # vertex geometry
    # --------------------------------------------------------------------------

    def add_vertex(self, key=None, attr_dict=None, **kwattr):
        key = super(CellNetwork, self).add_vertex(key=key, attr_dict=attr_dict, **kwattr)
        if key not in self.partial_edge:
            self.partial_edge[key] = {}
        if key not in self._edge:
            self._edge[key] = {}
        return key

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

    def vertices_coordinates(self, vertices, axes="xyz"):
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

        See Also
        --------
        :meth:`vertex_laplacian`, :meth:`vertex_neighborhood_centroid`

        """
        return Point(*self.vertex_coordinates(vertex))

    def vertices_points(self, vertices):
        return [self.vertex_point(vertex) for vertex in vertices]

    # --------------------------------------------------------------------------
    # edge geometry
    # --------------------------------------------------------------------------

    def add_edge(self, u, v, attr_dict=None, **kwattr):
        attr = attr_dict or {}
        attr.update(kwattr)
        assert u in self._vertex
        assert v in self._vertex
        data = self._edge[u].get(v, {})
        data.update(attr)
        self._edge[u][v] = data  # or is this edge data?
        if v not in self.partial_edge[u]:  # here we need to store the faces
            self.partial_edge[u][v] = set()  # the face(s)
        if u not in self.partial_edge[v]:
            self.partial_edge[v][u] = set()
        return u, v

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
        faces = []
        if v in self.partial_edge[u]:
            faces += list(self.partial_edge[u][v])  # we don't need double assignment, or do we?
        if u in self.partial_edge[v]:
            faces += list(self.partial_edge[v][u])  # we don't need double assignment, or do we?
        return faces

    def edges(self, data=False):
        for u, nbrs in iter(self._edge.items()):
            for v, attr in iter(nbrs.items()):
                if data:
                    yield (u, v), attr
                else:
                    yield u, v

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

    def face_edges(self, face):
        return self.halfface_halfedges(face)

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
    # cell geometry
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

    @property
    def data(self):
        """Returns a dictionary of structured data representing the volmesh data object.

        Note that some of the data stored internally in the data structure object is not included in the dictionary representation of the object.
        This is the case for data that is considered private and/or redundant.
        Specifically, the halfface dictionary and the plane dictionary are not included.
        This is because the information in these dictionaries can be reconstructed from the other data.
        Therefore, to keep the dictionary representation as compact as possible, these dictionaries are not included.

        To reconstruct the complete object representation from the compact data, the setter of the data property uses the vertex and cell builder methods (:meth:`add_vertex`, :meth:`add_cell`).

        Returns
        -------
        dict
            The structured data representing the volmesh.

        """
        cell = {}
        for c in self._cell:
            faces = []
            for u in sorted(self._cell[c]):
                for v in sorted(self._cell[c][u]):
                    # faces.append(self._halfface[self._cell[c][u][v]])
                    faces.append(self._cell[c][u][v])
            cell[c] = faces
        return {
            "attributes": self.attributes,
            "dva": self.default_vertex_attributes,
            "dea": self.default_edge_attributes,
            "dfa": self.default_face_attributes,
            "dca": self.default_cell_attributes,
            "vertex": self._vertex,
            "cell": cell,
            "face": self._halfface,
            "edge": self._edge,
            "edge_data": self._edge_data,
            "face_data": self._face_data,
            "cell_data": self._cell_data,
            "max_vertex": self._max_vertex,
            "max_face": self._max_face,
            "max_cell": self._max_cell,
        }

    @data.setter
    def data(self, data):
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
        vertex = data.get("vertex", {})
        cell = data.get("cell", {})
        face = data.get("face", {})
        edge = data.get("edge", {})
        edge_data = data.get("edge_data", {})
        face_data = data.get("face_data", {})
        cell_data = data.get("cell_data", {})
        self.attributes.update(data.get("attributes", {}))
        self.default_vertex_attributes.update(data.get("dva") or {})
        self.default_edge_attributes.update(data.get("dea") or {})
        self.default_face_attributes.update(data.get("dfa") or {})
        self.default_cell_attributes.update(data.get("dca") or {})
        for key, attr in iter(vertex.items()):
            print(key)
            self.add_vertex(key=key, attr_dict=attr)
        # for u in edge:
        #    for v in edge[u]:
        #        try:
        #            self.add_edge(u, v)
        #        except AssertionError:
        #            pass
        #            # print("has u", u, u in self._vertex)
        #            # print("has v", v, v in self._vertex)
        for key, vertices in iter(face.items()):
            attr = face_data.get(key) or {}
            self.add_halfface(vertices, fkey=key, attr_dict=attr)
        for ckey, faces in iter(cell.items()):
            attr = cell_data.get(ckey) or {}
            print("ckey, faces", ckey, faces)
            self.add_cell(faces, ckey=ckey, attr_dict=attr)
        for edge in edge_data:
            self._edge_data[edge] = edge_data[edge] or {}
        for face in face_data:
            self._face_data[face] = face_data[face] or {}
        self._max_vertex = data.get("max_vertex", self._max_vertex)
        self._max_face = data.get("max_face", self._max_face)
        self._max_cell = data.get("max_cell", self._max_cell)

    def to_network(self):
        network = Network()
        for vertex in self.vertices():
            x, y, z = self.vertex_coordinates(vertex)
            network.add_node(key=vertex, x=x, y=y, z=z)
        for u, v in self.edges():
            network.add_edge(u, v)
        return network

    def edge_face_adjacency(self, faces=None):
        adjacency = {}
        for face in faces:
            for u, v in self.face_edges(face):
                key = (u, v) if u < v else (v, u)
                if key not in adjacency:
                    adjacency[key] = {face}
                else:
                    adjacency[key].add(face)
        return adjacency

    def halfedge_from_faces(self, faces):
        """Construct a halfedge dictionary from a list of faces.

        Parameters
        ----------
        faces : list
            A list of faces.

        Returns
        -------
        dict
            A halfedge dictionary.

        """
        faces_vertices = self.unified_faces_vertices(faces)
        if not faces_vertices:
            return None
        halfedge = HalfEdge()
        for fkey, vertices in zip(faces, faces_vertices):
            for v in vertices:
                halfedge.add_vertex(v)
            halfedge.add_face(vertices, fkey=fkey)
        return halfedge

    def face_neighbors(self, fkey):
        """Return the neighbors of a face across its edges.

        Parameters
        ----------
        fkey : int
            The identifier of the face.

        Returns
        -------
        list[int]
            The identifiers of the neighboring faces.
        """
        nbrs = set()
        for edge in self.face_edges(fkey):
            nbrs.update(self.edge_faces(edge))
        return list(nbrs - {fkey})

    def face_adjacency(self, faces=None):
        """Construct a face adjacency dictionary from a list of faces.

        Parameters
        ----------
        faces : list
            A list of faces.

        Returns
        -------
        dict
            A face adjacency dictionary.
        """
        faces_vertices = [self.face_vertices(face) for face in faces]
        vertices = list({v: None for face in faces_vertices for v in face}.keys())  # unique vertices
        return face_adjacency(vertices, faces)

    def unified_faces_vertices(self, faces):
        faces_vertices = [self.face_vertices(face) for face in faces]
        vertices = list({v: None for face in faces_vertices for v in face}.keys())
        try:
            return unify_cycles(vertices, faces_vertices, root=0)
        except Exception:
            print("Cannot unify faces vertices.")
            raise
            return None

    def add_cell(self, faces, ckey=None, attr_dict=None, **kwattr):
        """Add a cell to the volmesh object.

        Parameters
        ----------
        faces : list[int]
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

        def flip_cycles(mesh):
            mesh.halfedge = {key: {} for key in mesh.vertices()}
            for fkey in mesh.faces():
                mesh.face[fkey][:] = mesh.face[fkey][::-1]
                for u, v in mesh.face_halfedges(fkey):
                    mesh.halfedge[u][v] = fkey
                    if u not in mesh.halfedge[v]:
                        mesh.halfedge[v][u] = None

        faces = list(set(faces))
        # First check if the faces are valid and form a closed cell
        halfedge = self.halfedge_from_faces(faces)
        if not halfedge or not halfedge.is_closed():
            print("Cannot add cell {}, faces {} can not be unified or are not closed.".format(ckey, faces))
            return

        # we know that the faces are unified, but do they all look in the correct direction?
        # first we now go to the faces and check if one of them is already part of a cell
        if self.number_of_cells() > 0:
            for face in faces:
                a_cell = self.halfface_cell(face)
                b_cell = self.halfface_opposite_cell(face)
                if a_cell is not None:
                    a_vertices = self.face_vertices(face)
                elif b_cell is not None:
                    a_vertices = list(reversed(self.face_vertices(face)))
                else:
                    continue
                # compare with the calculated vertices
                u, v = halfedge.face_vertices(face)[:2]
                i = a_vertices.index(u)
                j = a_vertices.index(v)
                if i == j - 1 or (j == 0 and u == a_vertices[-1]):
                    print("flipping halfedge")
                    flip_cycles(halfedge)
                    break
            else:
                print("We cannot detect if we need to flip the halfedge")
                return
                # if we dont find a cell.. we actually dont know ..

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
        for fkey in halfedge.faces():
            vertices = halfedge.face_vertices(fkey)
            for i in range(-2, len(vertices) - 2):
                u = vertices[i]
                v = vertices[i + 1]
                w = vertices[i + 2]
                if u not in self._cell[ckey]:
                    self._cell[ckey][u] = {}
                # self._plane[u][v][w] = ckey
                # self._plane[u][v][fkey] = ckey
                self._plane[u][v][fkey] = ckey
                self._cell[ckey][u][v] = fkey
        return ckey

    def face_cells(self, fkey):
        """Return the cells connected to a face."""
        cells = []
        for cell in [self.halfface_cell(fkey), self.halfface_opposite_cell(fkey)]:
            if cell is not None:
                cells.append(cell)
        return cells


if __name__ == "__main__":
    # import doctest
    from compas.colors import Color
    from compas.geometry import Point, Vector, Line, Polygon, Polyhedron, Box, Frame
    from ast import literal_eval
    import compas
    import json
    import os

    path = "/Users/romanarust/workspace/refmodel/data/model_12"

    # cell_network = CellNetwork.from_json(os.path.join(path, "cell_network.json"))
    # for cell in cell_network.cells():
    #    print(cell)

    # """
    def invert_dictionary(dictionary):
        inverted = {}
        for k, v in dictionary.items():
            vlist = v if isinstance(v, list) else [v]
            for v in vlist:
                if v not in inverted:
                    inverted[v] = [k]
                else:
                    inverted[v].append(k)
        return {k: list(set(v)) for k, v in inverted.items()}

    filepath = "/Users/romanarust/workspace/refmodel/data/model_12/refmodel_spaces.json"
    # data = compas.json_load(filepath)
    with open(filepath, "r") as f:
        data = json.load(f)

    network = Network.from_data(data["network"])
    faces = {literal_eval(key): attr for key, attr in data["faces"].items()}
    # spaces = {literal_eval(key): attr for key, attr in data["spaces"].items()}

    halfedge = {literal_eval(key): attr for key, attr in data["halfedge"].items()}
    halfface = {literal_eval(key): attr for key, attr in data["halfface"].items()} if "halfface" in data else {}
    # print(halfface)

    # 1. add vertices
    cell_network = CellNetwork()
    for node in network.nodes():
        x, y, z = network.node_coordinates(node)
        cell_network.add_vertex(key=node, x=x, y=y, z=z)

    # 2. add faces
    for face, vertices in faces.items():
        nfkey = cell_network.add_face(vertices, fkey=face)
        assert nfkey == face

    print("============================")

    cells = invert_dictionary(halfface)
    try_later = []
    for ckey, faces in cells.items():
        print(faces)
        print(list(set(faces)))
        ok = cell_network.add_cell(faces)
        if ok != ckey:
            print("Cannot add cell", ckey)
            try_later.append(ckey)
        break

    print(cell_network.face_vertices(29))
    print(cell_network.face_vertices(57))
    # add neighbors
    nbrs = set()
    for face in cells[ckey]:
        ckeys = halfface[face]

        for k in ckeys:
            if k != ckey:
                nbrs.add(k)
    print(nbrs)
    for nbr in nbrs:
        faces = cells[nbr]
        print(faces)
        ok = cell_network.add_cell(faces)
        if ok != ckey:
            print("Cannot add cell", ckey)
            try_later.append(ckey)
    print("1")

    def try_adding_cells_recursively(try_later, cell_network):
        next_round = []
        for ckey in try_later:
            faces = cells[ckey]
            ok = cell_network.add_cell(faces, ckey=ckey)
            if ok != ckey:
                next_round.append(ckey)
            else:
                print("added cell", ckey)
        if len(next_round) < len(try_later):
            try_adding_cells_recursively(next_round, cell_network)
        elif len(next_round) > 0:
            print("Could not add cells", next_round)

    # try_adding_cells_recursively(try_later, cell_network)
    print("2    ")
    import os

    path = os.path.dirname(filepath)
    cell_network.to_json(os.path.join(path, "cell_network.json"))

    print("3 ")

    # for face, vertices in faces.items():
    #    print(face, vertices)
    # """
    """

    # doctest.testmod(globs=globals())
    network = CellNetwork()

    

    frame = Frame.worldXY()
    frame.point = Point(0.5, 0.5, 0.5)
    box = Box(1, 1, 1, frame)

    from scipy.spatial import cKDTree

    def add_box_to_cell_network(box, network, tree=None, nodes=None, tol=1e-3):
        vertices, faces = box.to_vertices_and_faces()
        map_vtx = {}
        for i, point in enumerate(vertices):
            if tree:
                (d,), (n,) = tree.query([point])
                vkey = nodes[n]
                if d < tol:
                    map_vtx[i] = vkey
                    continue
            x, y, z = point
            vkey = network.add_vertex(x=x, y=y, z=z)
            nodes = list(network.vertices())
            tree = cKDTree(network.vertices_coordinates(nodes))
            map_vtx[i] = vkey
        fkeys = []
        for face in faces:
            fkey = network.add_face([map_vtx[f] for f in face])
            fkeys.append(fkey)
        # network.add_cell(fkeys)
        return fkeys, tree, nodes

    a_keys, tree, nodes = add_box_to_cell_network(box, network)
    print("a_keys", a_keys)
    network.add_cell(a_keys)
    print(a_keys)

    # get the face of the box that is on the right side
    box_b = box.copy()
    box_b.frame.point += Vector(1, 0, 0)

    b_keys = add_box_to_cell_network(box_b, network, tree, nodes)

    # 0 [0, 1, 2, 3, 4, 5]
    # 1 [6, 7, 8, 9, 10, 11]
    # 1 [6, 7, 8, 9, 2, 11]

    network.add_cell([6, 7, 8, 9, 2, 11])

    print(b_keys)
    # add_box_to_cell_network(box_b, network)

    na, nb = 4, 5
    pta, ptb = network.vertices_points([na, nb])
    v = Vector(0, 0, 1)
    ptd, ptc = pta + v, ptb + v
    nc = network.add_vertex(x=ptc[0], y=ptc[1], z=ptc[2])
    nd = network.add_vertex(x=ptd[0], y=ptd[1], z=ptd[2])
    network.add_face([na, nb, nc, nd])

    for cell in network.cells():
        print(cell, network.cell_faces(cell))

    # for k, v in CellNetwork.from_data(network.data).data.items():
    #    print(k, v)
    """
    from compas.geometry import project_points_plane, normal_polygon, centroid_polygon, Plane
    from compas_view2.app import App

    # colorisation
    color_yellow = Color(255 / 255.0, 175 / 255.0, 10 / 255.0)
    color_blue = Color(0, 0, 1)  # faces not belonging
    color_lila = Color(127 / 255.0, 137 / 255.0, 255 / 255.0)  # faces on border
    color_grey = Color(212 / 255.0, 212 / 255.0, 212 / 255.0)  # faces belonging to 2 cells
    opacity = 0.5
    viewer = App()

    for face in cell_network.faces():
        # print(face, network.face_vertices(face))
        cells = cell_network.face_cells(face)
        vertices = cell_network.face_coordinates(face)

        if not len(cells):
            # viewer.add(Polygon(vertices), facecolor=color_lila, opacity=opacity)
            pass
        elif len(cells) == 1:
            viewer.add(Polygon(vertices), facecolor=color_blue, opacity=opacity)
        else:
            print(face, cells[0] != cells[1], cells)
            viewer.add(Polygon(vertices), facecolor=color_yellow, opacity=opacity)
        # break

    viewer.view.camera.zoom_extents()
    viewer.show()
    # """

    # viewer.add(cell_network.to_network(), show_lines=True)
    # viewer.add(network, show_lines=True)
